# 011. AI determinism tiers, and using the lowest tier that works

**Go straight to:** [Home](../../README.md) · [ADRs](README.md) · [Diagrams](../diagrams/README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

## Status

Proposed

## Context

The brief asks us to use AI innovatively ([R12](../requirements.md#requirements)), to validate and verify its results
including detecting misbehaviour in production ([R13](../requirements.md#requirements)), and to survive a model or provider
changing, repricing or shutting down ([R14](../requirements.md#requirements)). It also tells us models and providers change
fast ([C11](../requirements.md#constraints)), generative behaviour is non-deterministic ([C12](../requirements.md#constraints)), and this is a family estate
with a small operations staff and no in-house ML team ([C13](../requirements.md#constraints)).

Read together, those pull against each other. The obvious way to look innovative is to
put a language model in front of every problem. The obvious way to be verifiable,
affordable and survivable is to use one as rarely as possible.

We think the tension is a false one, and that resolving it is where this submission can
differentiate. Most of the Countess's problems are measurement and forecasting problems.
Is this reading abnormal for this species at this time of year, how many fish are there,
how busy will Saturday be, which enclosure is nobody stopping at. These are statistics
questions. A language model would answer them more slowly, less reproducibly, more
expensively and less accurately than a well-chosen classical model.

Without a stated rule, three things happen. Every capability drifts towards a language
model because it is the interesting option. Verification becomes impossible, because
nothing has a deterministic reference. And the estate acquires an operating cost that
scales with visitors and is set by a third party.

Two alternatives were considered.

**A. Generative-first, with a single model behind everything.** One integration, one
skill to learn, maximally impressive on the surface. Rejected: it maximises exposure to
[C11](../requirements.md#constraints) and [C12](../requirements.md#constraints) precisely where [R13](../requirements.md#requirements) is hardest to satisfy, and it makes the estate's welfare
monitoring dependent on an external provider's uptime and pricing.

**B. Prohibit generative AI entirely.** Maximally verifiable and cheap. Rejected: it
fails [R12](../requirements.md#requirements), and it is wrong on the merits. There are two places here where the interface
genuinely is open-ended natural language, and refusing to use the right tool there would
be as unthinking as using it everywhere.

## Decision

Every AI capability is placed in one of three tiers, and we use the lowest tier that
solves the problem.

**Tier 1, deterministic and classical.** Statistical and classical machine learning:
threshold and seasonal anomaly detection, forecasting, counting from structured signals.
Reproducible given the same input. Verified by ordinary regression tests against a
held-out set with an accuracy threshold. Runs at the satellite broker or cheaply in
cloud.

**Tier 2, perceptual.** Computer vision and audio models: population estimation from
video, body-condition scoring, vibration signatures. Non-deterministic in output value
but bounded in output shape. Verified against an independent physical ground truth — a
stock ledger, a turnstile count, an inspection, a vet's score — and the disagreement is
published rather than hidden.

**Tier 3, generative.** Language models. Non-deterministic in both value and shape.
Requires a golden question set, grounding checks, drift monitoring and a named fallback
before it ships.

Three rules follow.

1. **Choosing Tier 3 requires justification in that capability's own ADR**, stating what
   the Tier 1 or Tier 2 version would have looked like and why it is insufficient.
   Choosing Tier 1 requires no justification at all.
2. **No generative output may actuate anything.** This extends the rule already set in
   [043](043-welfare-loop.md) — fixed rules written by a human may switch equipment on,
   anything a model infers may only advise — from welfare to the whole system. Nothing
   generative moves money, opens a ride, or overrules a person.
3. **Every AI output is stored with its tier, model identifier, version, confidence and a
   reference to the input that produced it.** Without this, [R13](../requirements.md#requirements) is unachievable, because
   there is nothing to compare a suspect output against.

## Consequences

### Positive

- [R13](../requirements.md#requirements) becomes tractable. Most capabilities are verifiable by conventional testing, and
  the few that are not have a named independent ground truth.
- [R14](../requirements.md#requirements) exposure is confined to a small number of capabilities rather than spread across
  the system. A provider shutting down costs us features, not revenue or animal welfare.
- Cost scales with the cheap tiers rather than the expensive one, which matters given
  [C14](../requirements.md#constraints).
- Tier 1 and 2 models run on the estate, so they keep working while disconnected ([R15](../requirements.md#requirements),
  [C1](../requirements.md#constraints)) — something no hosted language model can offer.
- It gives the team a one-line answer to "should this be AI?" that does not need
  relitigating each time.

### Negative

- The rule will occasionally be wrong. A generative approach may be genuinely better for
  a problem we have classed as Tier 1, and the justification requirement adds friction to
  discovering that.
- Three tiers means three verification approaches to build and maintain rather than one.
- It may read as unambitious to anyone expecting AI in every component. The overview has
  to make the argument to the Countess explicitly rather than assume it is self-evident.
- Storing provenance on every AI output adds volume to the welfare and analytics stores.

### Assumptions

- Classical models will in fact prove adequate for the anomaly detection and forecasting
  capabilities. If several turn out to need Tier 3, the ratio argument weakens and this
  record should be revisited.
- The team has, or can acquire, enough classical modelling skill to build Tier 1 well. A
  badly built Tier 1 model is worse than a competent Tier 3 one.

---

<p align="center">❦</p>

<p align="right"><a href="#011-ai-determinism-tiers-and-using-the-lowest-tier-that-works">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="README.md">All ADRs</a> · <a href="../diagrams/README.md">All diagrams</a></p>
