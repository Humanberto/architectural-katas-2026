# 023. AI cost control and graceful degradation

## Status

Proposed — Context drafted by A, Decision belongs to B

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

_To be written by B._

## Consequences

_To be written by B._
