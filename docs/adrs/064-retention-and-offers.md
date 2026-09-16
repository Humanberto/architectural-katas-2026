# 064. Retention and next-best-offer

**Go straight to:** [Home](../../README.md) · [ADRs](README.md) · [Diagrams](../diagrams/README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

## Status

Proposed.

## Context

Few visitors return, and nobody understands why ([P4](../requirements.md#problems)). Increasing returning visitors is
one of the Countess's stated requirements ([R10](../requirements.md#requirements)), and it is the cheapest route to
tripling attendance ([C8](../requirements.md#constraints)) — a visitor who already knows the way costs less to
attract than one who has never heard of the place.

The obvious approach is to track individuals around the park, learn what they liked, and
target them. **This architecture cannot do that, deliberately.**
[045](045-presence-and-flow.md) makes visitors unidentifiable by construction: zone
counting produces numbers, not people, and there is no way to join a person to a
movement.

That is a real cost, and [045](045-presence-and-flow.md) says so itself. This record is
what retention looks like when you accept it.

## Decision

**Retention works from the purchase, not the visit.** The only thing the estate knows
about a person is what [012](012-admissions-and-ticketing.md) recorded when they bought:
ticket type, date, party size, whether they have bought before. That is a smaller,
duller dataset than movement tracking, and it is the honest one.

**Propensity to return is Tier 1** under [011](011-ai-determinism-tiers.md). Predicting
whether a past purchaser buys again from purchase history is a classical classification
problem with an obvious measure. Nothing generative belongs anywhere near it.

**Offers act within bounds a person set**, in the same shape as
[061](061-demand-forecasting-and-pricing.md):

| Rule | Reason |
|---|---|
| A fixed catalogue of offers, written by a person | The model chooses which one, never what it says |
| A declared cap on discount depth and frequency per person | Nobody wakes up to a promotion the estate cannot afford |
| Offers land only where someone opted in | A ticket purchase is not consent to be contacted |
| No offer is made on the strength of where somebody walked | There is no such data, by construction |

**Uplift is measured against a holdout, not against itself.** A fraction of eligible
people receive no offer. The difference between the two groups is the effect; without it
the estate would be paying for visits that were going to happen anyway, which is the
normal way retention programmes fail. The holdout is the evidence
[021](021-evaluating-ai-before-release.md) gates on and
[022](022-detecting-ai-misbehaviour.md) watches.

**Aggregate popularity still informs the offers.** [045](045-presence-and-flow.md)'s zone
counts say which parts of the estate are busy and which are ignored
([P2](../requirements.md#problems), [R3](../requirements.md#requirements)), and
[061](061-demand-forecasting-and-pricing.md)'s forecast says which days need filling. An
offer aimed at a quiet Tuesday and an under-visited part of the park is aimed with
population data, not personal data.

## Consequences

| Decision | Cost |
|---|---|
| Purchase data only | A weaker model than one with movement data, and lower expected uplift. The alternative was not available |
| Holdout group | A portion of eligible people get no offer, so some revenue is deliberately forgone to learn whether the rest worked |
| Fixed offer catalogue | Less responsive than generated copy, and no chance of the estate emailing something it did not write |
| Opt-in only | A smaller reachable audience than the full purchase list |

### What this provides

- A return rate that can be measured and improved, where today neither is possible ([P4](../requirements.md#problems))
- An answer to "did the offers work" that survives someone asking how we know
- Nothing to lose if the data leaks, because there is very little in it

## Alternatives rejected

| Option | Why not |
|---|---|
| Identify and track visitors to personalise offers | [045](045-presence-and-flow.md) rules it out by construction, and undoing that would reopen every question that record closes |
| Generative offer copy per person | [C12](../requirements.md#constraints) non-determinism in outbound marketing means the estate sends words nobody approved |
| Measure uplift by comparing to last year | Confounded by weather, pricing, opening hours, and everything else that changed. A holdout is the only clean comparison |
| No retention programme | Leaves [R10](../requirements.md#requirements) unanswered and [P4](../requirements.md#problems) unexplained |

## Assumptions

- Enough visitors buy more than once for a propensity model to have signal. The estate
  has no ticketing history today ([P8](../requirements.md#problems)), so this is unmeasurable until a season has
  passed, and the model should not ship before then
- Somebody owns the offer catalogue and the caps
- Opt-in is collected at purchase, which is a change to [012](012-admissions-and-ticketing.md)'s flow and should be
  agreed with A rather than assumed here

## Open questions

- How large the holdout needs to be, and for how long, before uplift means anything
- Whether family passes should be modelled separately, since a family returning is a
  different decision from an individual returning
- Whether an offer that goes unredeemed repeatedly should stop being offered
  automatically, or whether that is a person's call

## Related

- **[011](011-ai-determinism-tiers.md)** sets the tier and the authority limit
- **[012](012-admissions-and-ticketing.md)** is the only source of what we know about a purchaser
- **[045](045-presence-and-flow.md)** is why this record looks the way it does
- **[061](061-demand-forecasting-and-pricing.md)** supplies the forecast that says which days need filling
- **[021](021-evaluating-ai-before-release.md)**, **[022](022-detecting-ai-misbehaviour.md)** gate and monitor it
- Diagram: [03 AI capability map](../diagrams/03-ai-capability-map.md)

---

<p align="center">❦</p>

<p align="right"><a href="#064-retention-and-next-best-offer">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="README.md">All ADRs</a> · <a href="../diagrams/README.md">All diagrams</a></p>
