# 023. AI cost control and graceful degradation

## Status

Accepted

## Context

The estate is unprofitable (P1) and must become profitable or be sold up (P5). The brief
is silent on budget beyond MQTT-capable devices, and we have agreed to treat that as the
funded baseline and require anything further to be argued for (C14). Model providers
change their pricing (C11).

That combination makes AI running cost an architectural concern rather than a finance
one. A capability whose cost scales with visitor numbers has a perverse property here:
it gets more expensive exactly as the estate succeeds at growing from 5,000 to 15,000
visitors a day (C8). A design that is affordable today and ruinous at target volume has
failed.

[011](011-ai-determinism-tiers.md) already does most of the work by keeping most
capabilities in Tier 1 and Tier 2, which run on hardware already paid for. The residual
exposure is Tier 3 and any cloud inference.

Questions B will want to settle:

- What is the unit of budget? Cost per thousand visitors is proposed, because it stays
  meaningful as volume grows, but B should decide.
- Does every capability declare a ceiling, and who signs it off?
- What happens when a ceiling is reached? Degrading the feature is very different from
  disabling it, and each capability needs a stated fallback — what the concierge does
  when it cannot call a model, what the copilot offers instead of an answer.
- How much of the traffic is genuinely repeated? If most visitor questions are the same
  forty questions about height restrictions and feeding times, caching changes the
  economics entirely.
- Is a cheap small model tried before an expensive large one, and who decides when to
  escalate?
- How do we notice a price rise within a day rather than at the end of the month?

Worth stating plainly: a capability that cannot state its cost per thousand visitors
should not ship. That is a strong claim and B should either adopt it or argue it down.

Alternatives worth considering and rejecting explicitly: a single overall budget rather
than per-capability ceilings; hard cut-off rather than degradation; and treating cost
as a finance problem to be reviewed monthly rather than an architectural constraint.

## Decision

**The unit of budget is cost per 1,000 visitors, per capability.** It is the number
proposed in the context, adopted as-is, because it is the one figure that stays
meaningful across the whole three-year, 5,000-to-15,000 growth curve (C8, C9); an
absolute monthly figure would need re-deriving at every stage of that growth and
invites exactly the kind of drift this record exists to prevent.

**Every Tier 3 capability declares a ceiling — a cost-per-1,000-visitors figure — in its
gateway config from [020](020-model-gateway.md), before it ships.** B proposes the
number at design time from the golden-set cost in [021](021-evaluating-ai-before-release.md)'s
release gate; the operations-lead role signs it off, because there is no separate
finance function here (C13) and the person who can switch a model version is the person
who should own what that switch is allowed to cost. **A capability that cannot state
this figure at design time does not ship.** The context proposes this as a strong claim
to adopt or argue down; it is adopted, because the alternative is discovering the cost
of a Tier 3 capability from the first invoice after launch, at exactly the visitor
volumes C8 is trying to reach.

**Reaching the ceiling degrades the capability; it does not disable it.** Each
capability has a stated ladder, not a cliff, reusing the fallback chain already declared
in 020:

1. Serve from cache if the question or query matches a cached, still-valid answer.
2. Try the cheaper model in the gateway's ranked list before the more expensive one;
   escalate only if the cheap model fails its own fast confidence/grounding check from
   021, not on a person's judgement call each time.
3. If the ceiling is still reached, fall back to the Tier 1 static path already named in
   020 — the FAQ decision tree for the concierge, the raw filter UI for the copilot.
   Both pre-date the AI feature and depend on no provider, so "the budget ran out" is a
   worse visitor experience, never an outage.

**Caching is treated as the primary lever, not an optimisation.** The brief's own
framing — most visitor questions are a small repeated set about height restrictions and
feeding times — is taken at face value: the concierge caches by canonicalised question
plus the version of the grounding source it was answered from, invalidating only when
that source changes. We target a majority of concierge traffic served from cache at
target volume; without that, cost scales with visitors exactly as the context warns,
and the capability becomes more expensive precisely as it succeeds.

**Price changes are detected same-day, by the same mechanism as
[022](022-detecting-ai-misbehaviour.md), not discovered on an invoice.** The gateway's
per-call log already carries actual cost per call (020); a daily job compares that
day's mean cost per call against the trailing 7-day mean per capability, and a rise past
a set percentage is a same-day alert to the operations lead — reusing 022's alerting
path rather than building a second one.

Two alternatives were rejected beyond hard cut-off, which the context already names and
which the degradation ladder above replaces directly.

**A. A single overall AI budget rather than per-capability ceilings.** Rejected because
a shared pool lets one capability's cost spike silently consume the other's headroom —
the copilot could starve the concierge, or vice versa, with no signal until the pool is
empty. Per-capability ceilings also map directly onto the degradation ladder each
capability needs regardless of budget, so they cost nothing extra to maintain
separately.

**B. Treating cost as a finance problem, reviewed monthly.** Rejected because C11 says
provider prices move fast, and a monthly review discovers a price rise weeks after it
happened, during which the estate has been paying it on every visitor. This is exactly
the "discovered on the invoice" failure mode the context's background section warns
against, restated as a review cadence rather than a design.

## Consequences

### Positive

- Cost per 1,000 visitors gives one comparable figure across capabilities and across the
  whole growth curve, so "can we afford this at 15,000 visitors a day" is answerable at
  design time rather than discovered at launch.
- The degradation ladder means peak season — when the concierge and copilot are most
  needed — is never the moment either gets switched off; it is the moment they get
  cheaper and slightly less capable instead.
- Same-day price-change detection reuses infrastructure 022 already requires, so this
  record adds a comparison job, not a new system.
- A capability that cannot state its cost does not ship — this keeps the estate from
  ever operating a capability whose economics nobody actually checked.

### Negative

- Caching a majority of concierge traffic assumes the "same forty questions" pattern the
  brief suggests actually holds; if visitor questions turn out to be more varied than
  expected, the cost model this record relies on weakens and the ceiling may need to be
  set higher or the fallback triggered more often.
- Per-capability ceilings mean B (or whoever holds the operations-lead role) is doing
  small ongoing arithmetic — checking that the sum of ceilings is still something the
  estate can afford — that a single pool would have done automatically. This is an
  accepted manual step given C13 offers no finance function to own it otherwise.
- Escalating from a cheap to an expensive model only on a failed confidence check means
  some fraction of traffic pays for both calls; this is the price of not requiring a
  person to decide per-request.

### Assumptions

- The operations-lead role has visibility into actual provider pricing, not just the
  gateway's own log, so the daily comparison reflects reality and not a stale assumed
  rate.
- The initial ceilings B proposes at launch are estimates from golden-set cost, not
  production traffic; they should be revisited against the first month of real usage
  once the estate is live.

## Related

- Diagram: [09 — Model gateway](../diagrams/09-model-gateway.md)
- Implementation: [Cost](../implementation.md#cost-b)
- [020](020-model-gateway.md) holds the ceiling config and the fallback chain this
  degrades into
- [012](012-admissions-and-ticketing.md) is the source of the visitor count in the
  cost-per-1,000-visitors figure
