# 020. Model gateway and provider abstraction

**Go straight to:** [Home](../../README.md) · [ADRs](README.md) · [Diagrams](../diagrams/README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

## Status

Accepted

## Context

The brief requires that we survive a model or provider changing, repricing, or shutting
down ([R14](../requirements.md#requirements)), and tells us that models and providers change fast, including pricing and
availability ([C11](../requirements.md#constraints)). This is a family estate with a small operations staff and no
in-house ML team ([C13](../requirements.md#constraints)), and no budget beyond the funded MQTT hardware baseline ([C14](../requirements.md#constraints)).

The problem is coupling. If business logic calls a vendor SDK directly, then a provider
change is a code change in every place that calls it, a price rise is discovered on the
invoice, and a shutdown is an outage. None of those are recoverable in a week by a team
this size.

[011](011-ai-determinism-tiers.md) limits our exposure by keeping most capabilities in
Tier 1 and Tier 2, which run on the estate and depend on no provider at all. This record
covers what to do about the remainder, where an external model genuinely is the right
answer.

Three scenarios need answering distinctly, and the brief names all three:

- A better model appears. How do we adopt it without rewriting anything?
- A provider raises prices. How do we find out quickly, and what happens then?
- A provider shuts down. What still works?

Questions this record has to answer:

- What is the unit of abstraction — a capability name such as "answer visitor question",
  or a thinner wrapper over a chat completion?
- Where do prompts and model choices live, and are they versioned artefacts subject to
  the same release process as code?
- Is there a self-hosted fallback per capability, and do we know what quality it gives
  us, or are we guessing?
- How is a candidate model evaluated against the incumbent — offline against a fixed
  set, shadowed against live traffic, or both?
- Who can switch the active model, and is that a deployment or a configuration change?

Alternatives considered and rejected explicitly: calling vendor SDKs directly
and accepting the coupling; adopting a third-party gateway or router product; and
committing to a single provider deliberately in exchange for simplicity.

## Decision

**Every Tier 3 capability calls a single internal Model Gateway; nothing else in the
codebase holds a vendor SDK key.** The unit of abstraction is the capability, not the
chat completion — `answerVisitorQuestion`, `draftOperationsQuery` — because a thinner
wrapper still leaks provider-specific request shape into business code the moment a
second provider is added, which is precisely the day we need it not to.

**The gateway holds, per capability, an active model and prompt version, one or more
ranked fallbacks, and a circuit breaker.** Concretely:

| Capability | Active | Fallback 1 | Fallback 2 |
|---|---|---|---|
| Visitor concierge | Hosted LLM | Smaller/cheaper hosted LLM | Static FAQ decision tree (Tier 1, on the estate) |
| Operations copilot | Hosted LLM | — | Raw filter UI the copilot sits in front of (pre-AI baseline) |

The last fallback in each row depends on no provider at all. A provider shutting down
degrades the estate to a state it already had, not to nothing ([R14](../requirements.md#requirements)).

**Prompts and model identifiers are versioned config in this repository, reviewed like
code, not literals in application code.** A prompt change and a model change are the
same kind of event — both are a new *version* of the capability, and both are subject
to the release gate in [021](021-evaluating-ai-before-release.md) before they can become
active.

**Switching the active model or prompt version is a configuration change, not a
deployment** — a row update read by the gateway at request time — but it may only be
made by whoever holds the operations-lead role, and only to a version that has already
passed [021](021-evaluating-ai-before-release.md)'s gate. Fast to flip; not fast to flip *unsafely*.

**A candidate is evaluated offline against [021](021-evaluating-ai-before-release.md)'s golden set first.** If it passes, it
is promoted to a canary slice of live traffic (10% of calls, minimum 48 hours or 200
interactions, whichever is longer) under [022](022-detecting-ai-misbehaviour.md)'s
monitoring before it takes 100%. Shadowing — calling the candidate silently alongside
the incumbent with no user impact — is used additionally whenever the capability's
volume makes waiting for a canary too slow to be useful; at current visitor volumes
([C8](../requirements.md#constraints)) it usually will not be needed, so it is available but not mandatory.

**Every call the gateway makes is logged with capability, tier, model identifier and
version, prompt version, latency, cost, and a confidence figure where the model
provides one.** This is the record [011](011-ai-determinism-tiers.md)'s third rule requires, and it is what
[022](022-detecting-ai-misbehaviour.md) and [023](023-ai-cost-control.md) both read
from — one log, two downstream uses, not two logging systems.

Two alternatives were rejected, beyond calling vendor SDKs directly, which the context
already dismisses on coupling grounds.

**A. A third-party gateway or router product (e.g. a hosted LLM router).** Attractive
given [C13](../requirements.md#constraints) — nobody here has to build request routing from scratch. Rejected because it
substitutes one provider dependency for another: [R14](../requirements.md#requirements) asks us to survive *a* provider
disappearing, and routing through a single third-party router just moves the single
point of failure one layer up without removing it. At two Tier 3 capabilities, the
routing logic this ADR needs is a lookup table and a circuit breaker, not a product.
Worth revisiting if the number of generative capabilities grows well beyond two.

**B. Committing to a single provider deliberately, in exchange for simplicity.**
Rejected outright by [R14](../requirements.md#requirements) and [C11](../requirements.md#constraints) — this is the scenario the brief specifically asks us
to be able to survive, and choosing it because it is simpler answers a different
question than the one being asked.

## Consequences

### Positive

- A provider price rise, model deprecation, or outage is a configuration change at the
  gateway, not an incident response across the codebase ([R14](../requirements.md#requirements)).
- Business logic — the concierge's dialogue flow, the copilot's UI — never imports a
  vendor SDK, so [010](010-architecture-style.md)'s module-boundary discipline extends cleanly into the AI surface.
- One log schema serves evaluation, drift detection and cost tracking, so this is one
  piece of infrastructure rather than three.
- Every fallback bottoms out on the estate with no provider dependency, which is the
  same guarantee [011](011-ai-determinism-tiers.md) already gives Tier 1 and 2, now extended to what happens when
  Tier 3 fails.

### Negative

- The gateway itself becomes a single internal dependency both Tier 3 capabilities
  share; a bug in it affects both at once. It must be simple enough that this is an
  acceptable concentration of risk for a two-capability estate.
- Canary and shadow evaluation add latency to adopting a genuinely better model — the
  48-hour minimum bake is a deliberate trade of speed for the verification [R13](../requirements.md#requirements) demands.
- Config-driven prompts and model choice mean a bad config change is possible without a
  code review catching it in the usual place; this is why [021](021-evaluating-ai-before-release.md) requires the gate to run
  on every version change, not just code changes.

### Assumptions

- Two generative capabilities is the right scale for a hand-rolled gateway. If a third
  generative capability appears, this record should be revisited against buying a router product.
- The operations-lead role that may switch active versions is staffed continuously; if
  nobody holds it, canaries have nobody to promote them.

## Related

- Diagram: [09 — Model gateway](../diagrams/09-model-gateway.md)
- [021](021-evaluating-ai-before-release.md) gates what may become active here
- [022](022-detecting-ai-misbehaviour.md) reads this gateway's call log and can trigger
  an automatic revert
- [023](023-ai-cost-control.md) sets the ceiling that triggers the static fallback

---

<p align="center">❦</p>

<p align="right"><a href="#top">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="README.md">All ADRs</a> · <a href="../diagrams/README.md">All diagrams</a></p>
