# Architecture decision records

Every significant decision in this proposal, with the alternatives we rejected and what
each choice costs. Requirement identifiers cited inline come from
[requirements](../requirements.md).

| # | Decision | Status |
|---|----------|--------|
| 010 | [Edge-first data plane with a conventional transactional core](010-architecture-style.md) | Proposed |
| 011 | [AI determinism tiers, and using the lowest tier that works](011-ai-determinism-tiers.md) | Proposed |
| 012 | [Admissions and ticketing, with gates that work offline](012-admissions-and-ticketing.md) | Proposed |
| 013 | [Pass lifecycle: amendment, revocation, and key rotation](013-pass-lifecycle.md) | Proposed |
| 020 | [Model gateway and provider abstraction](020-model-gateway.md) | Proposed |
| 021 | [Evaluating AI before release](021-evaluating-ai-before-release.md) | Proposed |
| 022 | [Detecting AI misbehaviour in production](022-detecting-ai-misbehaviour.md) | Proposed |
| 023 | [AI cost control and graceful degradation](023-ai-cost-control.md) | Proposed |
| 040 | [Tiered MQTT topology with prioritised local buffering](040-connectivity-topology.md) | Proposed |
| 041 | [Hybrid transport: LoRaWAN for sensors, wifi for everything else](041-hybrid-transport.md) | Proposed |
| 042 | [Telemetry model, topic taxonomy, and delivery guarantees](042-telemetry-model.md) | Proposed |
| 043 | [Watching animal health, and what the system may do on its own](043-welfare-loop.md) | Proposed |
| 044 | [Working while disconnected, and putting the records back together](044-disconnected-operation.md) | Proposed |
| 045 | [Counting visitors without being able to identify them](045-presence-and-flow.md) | Proposed |
| 046 | [Checking the animal count against the keepers' ledger](046-count-reconciliation.md) | Proposed |
| 047 | [Recording conditions so the data is worth learning from](047-environment-and-weather.md) | Proposed |
| 060 | [Ride condition monitoring](060-ride-condition-monitoring.md) | Proposed |
| 061 | [Demand forecasting and pricing](061-demand-forecasting-and-pricing.md) | Proposed |
| 062 | [Visitor concierge](062-visitor-concierge.md) | Proposed |
| 063 | [Estate operations copilot](063-operations-copilot.md) | Proposed |
| 064 | [Retention and next-best-offer](064-retention-and-offers.md) | Proposed |

New records use [000-template.md](000-template.md).

## Reading order

Two records carry the argument. Start there.

- **[010](010-architecture-style.md)** — the shape of the system. If a decision must
  survive a network partition it lives on the estate; if it must be atomic it lives in
  the transactional core.
- **[011](011-ai-determinism-tiers.md)** — how AI is bounded. Prefer classical, then
  perceptual, then generative, and justify any exception.

Everything else elaborates one of those two.

**The estate and its network** — 040, 041, 042, 044, 047. Patchy wifi is the constraint
that shapes the whole design, and these are where it is answered.

**Admissions** — 012 and 013. The one part of the system with no AI in it, and the
reason gates keep working when the network does not.

**The animals** — 043 and 046. Welfare monitoring, the boundary between what a fixed
rule may do and what a model may only suggest, and the count reconciled against an
independent record kept by keepers.

**The visitors** — 045, 060 to 064. Counting without identifying, ride condition,
pricing, the concierge, the copilot, and returning visitors.

**Assurance across all of it** — 020 to 023. How a model is replaced, evaluated,
monitored in production, and kept inside a budget.

## Numbering

Numbers are grouped by area and are not sequential. 010s are foundations and admissions,
020s assurance, 040s the estate and its animals, 060s the visitor-facing capabilities.
Gaps are deliberate and leave room for records we have not written.
