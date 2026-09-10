# 061. Demand forecasting and pricing

## Status

Proposed — Context drafted by A, Decision belongs to D

## Context

The estate must roughly triple visitor volume or sell the carnivorous plant collection
(P5, C8), over a three-year horizon (C9), while also becoming more profitable (R9).
Those are different goals and they can conflict: the easiest way to grow volume is to
cut prices, and the easiest way to raise margin is to raise them.

Forecasting is also how several other things get decided. Staff deployment is currently
guesswork (P2, R4). Knowing that Saturday will bring 12,000 people and Tuesday 3,000
changes rostering, catering, and which enclosures need a keeper present.

Pricing at a family heritage estate carries reputational risk that a pure optimisation
would miss. A visitor who discovers they paid more than the family next to them for the
same day does not come back (R10), and may say so publicly.

Questions D will want to settle:

- What drives the forecast? Historical admissions from [012](012-admissions-and-ticketing.md),
  day of week, school holidays, weather forecast, local events and booking lead-time
  curves are the usual set. Which are actually available?
- What horizon matters — same day for staffing, weeks ahead for pricing? They may need
  different models.
- Does pricing move automatically, and if so inside what bounds? Human-set floors and
  ceilings per ticket type are the obvious guardrail.
- Is personalised pricing ruled out? There is a strong argument that it should be,
  explicitly, and that saying so is worth more than the revenue it forgoes.
- How is accuracy measured, at what threshold does it stop being trusted, and what does
  pricing fall back to — presumably a static schedule?
- Which tier is this under [011](011-ai-determinism-tiers.md)? A gradient-boosted
  forecast is Tier 1, which makes verification straightforward.

Cold-start is worth a sentence: there is no ticketing system today (P8), so there is no
historical admissions data. The first season's model has nothing to learn from. What
happens in the meantime is part of this decision.

Alternatives worth considering and rejecting explicitly: personalised or surge pricing;
a fixed price list with no forecasting; and forecasting for staffing only, leaving price
alone.

## Decision

_To be written by D._

## Consequences

_To be written by D._
