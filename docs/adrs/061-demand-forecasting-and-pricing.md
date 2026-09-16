# 061. Demand forecasting and pricing

**Go straight to:** [Home](../../README.md) · [ADRs](README.md) · [Diagrams](../diagrams/README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

## Status

Proposed.

## Context

The estate must become profitable or the carnivorous plant collection is sold
([P1](../requirements.md#problems), [P5](../requirements.md#problems)), and visitor numbers must roughly triple over three years
([C8](../requirements.md#constraints), [C9](../requirements.md#constraints)). Today nobody knows which parts of the park are popular
([P2](../requirements.md#problems)), so staffing and investment are guesswork ([R4](../requirements.md#requirements)).

Two decisions depend on knowing tomorrow's demand: how many people to roster, and what
to charge. Both are currently made by feel.

Pricing is where an AI system can most easily do harm to a business that depends on
goodwill. A visitor who learns they paid more than the family behind them, for reasons
nobody can explain, does not come back — which works directly against
[R10](../requirements.md#requirements).

## Decision

**Forecasting is Tier 1 under [011](011-ai-determinism-tiers.md).** Predicting daily
admissions from season, day of week, school holidays, weather forecast and history is a
classical regression problem with an obvious accuracy measure. Nothing generative
belongs here.

**Prices move within bounds a person sets, and never outside them.** The model proposes
a price for a future date; a declared floor and ceiling per ticket type bound what it
may propose; anything outside the band needs a person. The model is choosing a point in
a range somebody already agreed, not setting a price.

**Price varies by date, never by visitor.** Everyone buying for the same day at the same
moment sees the same price. This is partly principle and partly a property of the
design: [045](045-presence-and-flow.md) makes visitors deliberately unidentifiable, so
there is no individual to price against even if we wanted one.

| Rule | Reason |
|---|---|
| A published price never rises for a date already on sale | A visitor who waited is not punished for waiting |
| A family pass is never more than the singles it replaces | [R1](../requirements.md#requirements) names family passes as a product, not a penalty |
| Every price change is recorded with the forecast that caused it | Somebody has to be able to answer "why was it that much" |

**The forecast feeds staffing before it feeds pricing.** Knowing Saturday will be busy is
worth more as a rota than as a price, and it answers [R4](../requirements.md#requirements)
directly. Zone-level distribution comes from [045](045-presence-and-flow.md), which is
what turns a day-level number into a decision about where people should stand.

**Accuracy is measured against admissions, continuously.** Every forecast is compared to
what [012](012-admissions-and-ticketing.md) actually recorded. That comparison needs no
labelling and never stops, so it is both the release gate under
[021](021-evaluating-ai-before-release.md) and the drift signal under
[022](022-detecting-ai-misbehaviour.md).

## Consequences

| Decision | Cost |
|---|---|
| Bounded pricing | Leaves money on the table at genuine peaks, which is the price of never having to explain a surprise |
| One price per date | Forgoes the revenue that individual pricing might produce, and the design could not support it anyway |
| Published prices never rise | Constrains how late the model may react to a demand signal |
| Forecast recorded with every price | More to store, and it is what makes the pricing defensible later |

### What this provides

- A staffing decision with a number behind it rather than a hunch ([R4](../requirements.md#requirements))
- Revenue that responds to demand without a mechanism that can embarrass the estate
- Accuracy measured against something physical, forever, at no extra cost

## Alternatives rejected

| Option | Why not |
|---|---|
| Per-visitor dynamic pricing | Actively harmful to returning visitors ([R10](../requirements.md#requirements), [P4](../requirements.md#problems)), and impossible under [045](045-presence-and-flow.md) |
| A generative model for pricing | A price is a number with consequences. Non-determinism ([C12](../requirements.md#constraints)) has nothing to offer here and a great deal to cost |
| Fixed prices, no forecasting | The status quo. Cheap and safe, but leaves the estate unable to answer either of the questions it needs answered |
| Fully automatic price setting with no bounds | Nobody at the estate could explain an output, and [C13](../requirements.md#constraints) means nobody could debug one either |

## Assumptions

- Admission history accumulates fast enough to forecast on within the first season. The
  estate has no ticketing history today ([P8](../requirements.md#problems)), so early forecasts will be poor and should
  be labelled as such rather than trusted
- Weather forecast data can be obtained for the estate's location. This is the same
  external feed [047](047-environment-and-weather.md) relies on
- Somebody holds the authority to set the floor and ceiling, and reviews them

## Open questions

- Who sets the bands, how often they are revisited, and on what evidence
- Whether a family pass should be priced on a formula from the single price rather than
  forecast separately
- How far ahead prices are published, which decides how much the forecast can react

## Related

- **[011](011-ai-determinism-tiers.md)** places this in Tier 1 and bounds its authority
- **[012](012-admissions-and-ticketing.md)** sells the tickets and supplies the ground truth
- **[045](045-presence-and-flow.md)** supplies zone distribution, and rules out per-visitor pricing by construction
- **[047](047-environment-and-weather.md)** supplies the weather feed the forecast reads
- **[064](064-retention-and-offers.md)** uses the same forecast to decide when an offer is worth making
- Diagram: [03 AI capability map](../diagrams/03-ai-capability-map.md)

---

<p align="center">❦</p>

<p align="right"><a href="#061-demand-forecasting-and-pricing">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="README.md">All ADRs</a> · <a href="../diagrams/README.md">All diagrams</a></p>
