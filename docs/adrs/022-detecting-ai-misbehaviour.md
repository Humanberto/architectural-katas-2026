# 022. Detecting AI misbehaviour in production

**Go straight to:** [Home](../../README.md) · [ADRs](README.md) · [Diagrams](../diagrams/README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

## Status

Accepted

## Context

The brief asks specifically for detection of AI misbehaviour once in production ([R13](../requirements.md#requirements)),
not merely testing before release. This is the harder half. A model that passed its gate
in September can degrade in November without anything visibly breaking — no exception,
no error rate, just worse answers.

Three things can drift underneath us. The inputs change: a new species arrives, a ride
reopens, a heatwave falls outside anything in the training data. The model changes: a
provider updates it, or we switch it under [020](020-model-gateway.md). Or the world
changes and the model is now answering a question nobody is asking.

Two features of this system help, and the design below uses both.

The first is that a human already acts on most AI output. [043](043-welfare-loop.md)
establishes that a keeper closes every welfare alert with an outcome — real, not real,
or unclear. That disposition is a free, continuous accuracy measurement, because closing
the alert has to happen anyway. The same pattern is available wherever a person acts on
a model's suggestion.

The second is that several capabilities have an independent physical ground truth that
keeps reporting forever: admission totals from [012](012-admissions-and-ticketing.md)
against zone counts from [045](045-presence-and-flow.md), a keeper's typed count against a camera's population estimate
([046](046-count-reconciliation.md)), an inspection against
a condition advisory. Divergence between the two is a detector that needs no labels.

Questions this record has to answer:

- What is measured, at what cadence, and where does it surface? A metric nobody looks at
  is not detection.
- What are the thresholds, and what does breaching one actually do — alert someone, or
  automatically revert?
- Is rollback a configuration change at the gateway or a deployment? How long does it
  take?
- Does a new model go out to everything at once, or to a slice first?
- Who is on the receiving end of a drift alert, given [C13](../requirements.md#constraints) means there is nobody whose
  job this is?

There is a trap worth naming. It is easy to design monitoring that requires an ML
engineer to interpret. This estate does not have one and will not hire one, so any
signal that cannot be acted on by a generalist is decoration.

Alternatives considered and rejected explicitly: periodic manual review rather
than continuous monitoring; relying on user complaints as the detection mechanism; and
full observability tooling that the estate cannot operate.

## Decision

**Every capability generalises the disposition pattern [043](043-welfare-loop.md) already sets for welfare
alerts: whoever acts on an AI output records whether it was right, wrong, or unclear,
and that record is the primary drift signal — not a second monitoring system.** For
Tier 1/2 capabilities this is nearly free, because a human already acts on the output
(a keeper checking an alert, an inspector reading a ride advisory). For Tier 3, the
equivalent disposition is: did the visitor's follow-up indicate the concierge answered
the question, and did the ops user run the copilot's generated query as offered or
edit it heavily first. Both are cheap to capture at the point of use.

**Where an independent physical ground truth exists, divergence from it is a second,
label-free detector**, read continuously rather than only at release: admission totals
against zone counts ([012](012-admissions-and-ticketing.md) vs [045](045-presence-and-flow.md)), the keeper's typed count against the camera's piranha
population estimate ([046](046-count-reconciliation.md)). This needs no golden set and no human disposition — it is the
same comparison [021](021-evaluating-ai-before-release.md)'s Tier 2 gate makes, just running forever instead of once.

**Metric, cadence, and threshold.** For every capability, a rolling 14-day
false-positive/false-disposition rate is computed daily from the disposition log and
compared to the rate the capability had when it passed its [021](021-evaluating-ai-before-release.md) gate. A rise of more
than 10 percentage points above that baseline is a drift alert. Fourteen days is chosen
to smooth over a single bad day without waiting so long that a real drift goes
unnoticed for weeks.

**What breaching the threshold does differs by tier, and this is deliberate, not an
oversight.**

- Tier 1/2: alert-only, to a named person, because a human is already positioned
  downstream of every one of these outputs and is the right party to judge what
  changed.
- Tier 3: the gateway automatically reverts the affected capability to its last
  known-good model/prompt version — a configuration change per [020](020-model-gateway.md),
  typically live within minutes — and *then* alerts. Tier 3 gets automatic rollback
  because, unlike Tier 1/2, there is no vet-set limit or keeper's count standing
  behind it if it goes wrong; the gateway's last-known-good pointer is the only safety
  net available, so it is used immediately rather than waiting for a person to notice.

**Canary bake-in, set here and referenced by [020](020-model-gateway.md)**: a new Tier 3 version serves 10% of
traffic for a minimum of 48 hours or 200 interactions before taking the rest, and drift
detection runs on that slice with the same thresholds — a bad release is caught while it
is still only a tenth of the exposure.

**Surfacing.** One weekly digest, not a dashboard: capability name, current disposition
rate, baseline, and any breach in the last seven days, sent to whoever holds the
operations-lead role from [020](020-model-gateway.md). A breach also sends an immediate
message the day it happens; the digest is for the steady state, not the incident.
Given [C13](../requirements.md#constraints), this is deliberately the only surface — a generalist can read seven lines
once a week, and will not maintain a dashboard nobody assigned them to own.

Two alternatives were rejected beyond periodic manual review, which the context already
correctly identifies as too slow to catch drift that develops over weeks between
reviews.

**A. Relying on user complaints as the detection mechanism.** Rejected because it is
biased toward the wrong failures: a concierge that answers confidently and wrongly is
worse than one that visibly fails, and confident wrong answers are exactly the ones
visitors are least likely to notice or report. The failure mode we most need to catch
is the one this mechanism is worst at catching.

**B. Full observability/APM tooling.** Rejected by [C13](../requirements.md#constraints) directly — it is built for
someone whose job is reading it, and that role does not exist here. The weekly digest
and the disposition log are deliberately smaller than what a well-resourced platform
team would build, because a bigger system unused is worse than a smaller one that gets
read.

## Consequences

### Positive

- Detection cost is close to zero for Tier 1/2, because it reuses work a person was
  already doing ([043](043-welfare-loop.md)'s pattern, generalised).
- Tier 3's automatic rollback means the worst case for a bad release is bounded to
  roughly 48 hours of a 10% slice, not an open-ended production incident.
- One digest, one recipient role, no dashboard to build or forget — matches [C13](../requirements.md#constraints).
- The same disposition log that detects drift here is the evidence [021](021-evaluating-ai-before-release.md)'s audit-rate
  ramp uses to decide whether a capability has earned a lighter release check.

### Negative

- A capability with nobody acting on its output — nothing to disposition — has no free
  signal and needs its ground-truth divergence check to carry the entire load, or it is
  effectively unmonitored. This should be flagged explicitly for any future capability
  that has neither.
- Automatic rollback on Tier 3 can revert a genuinely good new version because of a
  noisy 10% sample, especially early in a bake-in window; the 200-interaction floor is
  a guess at a sample size that avoids most of this, not a proven one.
- A 14-day baseline window means a slow, steady drift under 10 points a fortnight can
  still creep past the threshold in small steps; this is a deliberate trade against
  false alarms, and should be revisited if it proves too forgiving in practice.

### Assumptions

- The operations-lead role from [020](020-model-gateway.md) is checked at least weekly; a digest nobody opens is
  the same as no detection.
- Fourteen days and ten percentage points are reasonable starting thresholds, not
  validated ones — there is no production history yet to tune them against.

## Related

- Diagram: [10 — Evaluation and drift loop](../diagrams/10-evaluation-loop.md)
- [043](043-welfare-loop.md) is the origin of the disposition pattern this generalises
- [020](020-model-gateway.md) executes the automatic revert on a Tier 3 breach
- [021](021-evaluating-ai-before-release.md) covers the same capability before release
- [045](045-presence-and-flow.md) and [046](046-count-reconciliation.md) supply the ground truths the divergence detector reads

---

<p align="center">❦</p>

<p align="right"><a href="#022-detecting-ai-misbehaviour-in-production">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="README.md">All ADRs</a> · <a href="../diagrams/README.md">All diagrams</a></p>
