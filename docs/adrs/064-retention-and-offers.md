# 064. Retention and next-best-offer

## Status

Proposed — Context drafted by A, Decision belongs to D

## Context

Increasing returning visitors is a stated requirement (R10) and the estate has no
understanding of how to do it (P4). Commercially this is the strongest lever available:
converting a day visitor into a member or a repeat visitor raises revenue (R9) without
needing another body through the gate, which matters because the volume target (P5, C8)
is hard.

Once [012](012-admissions-and-ticketing.md) is running there is a visit history to work
with — party composition, frequency, what was bought, when. Combined with C's presence
data there is also a picture of what a party actually did on the day.

Two cautions worth designing around from the start.

The first is authorship. An offer is a commitment: once sent, a discount is a liability
the estate has to honour. Under [011](011-ai-determinism-tiers.md) nothing generative may
actuate, and an offer sent to a customer is close to an action. Selecting from a fixed
catalogue written by a human is materially different from generating an offer, and this
record should be explicit about which is happening.

The second is fairness. A model that systematically withholds offers from some group,
or targets discounts at people who would have paid full price, is both a commercial
error and a reputational one for a family estate.

Questions D will want to settle:

- Fixed offer catalogue, or generated? If fixed, who writes it and how many offers are
  there?
- What signals drive the propensity model, and which tier is it? A propensity model is
  Tier 1, which makes it cheap and verifiable.
- Is uplift measured, or assumed? Holdout groups on every campaign are the only way to
  know whether this works at all.
- Can a member of staff see why a given offer was selected, and explain it to a visitor
  who asks?
- What are the fairness checks and who reviews them?
- How many campaigns get human review before anything runs unattended?

Honest scoping note: this is the most droppable capability in the submission. It
depends on visit history that does not exist yet (P8), and it delivers least in the
first season. If the week gets tight, this is the one to cut, and saying so here is
better than discovering it on the 15th.

Alternatives worth considering and rejecting explicitly: generative offer copywriting
sent unreviewed; untargeted blanket discounting; and a simple rules-based loyalty scheme
with no model at all.

## Decision

_To be written by D._

## Consequences

_To be written by D._
