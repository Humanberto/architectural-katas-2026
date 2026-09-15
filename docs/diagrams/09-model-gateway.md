# 09. Model gateway

What sits between the two Tier 3 capabilities and any external provider: one gateway,
a ranked fallback per capability, and the log that feeds evaluation, drift detection
and cost control from a single source. Behind [020](../adrs/020-model-gateway.md).

```mermaid
flowchart LR
  concierge[Visitor concierge]
  copilot[Operations copilot]

  gateway[Model Gateway]

  active[[Active model]]
  fb1[[Fallback model]]
  static{{Static FAQ / raw filter UI}}

  log[(Call log: tier, model, version, cost, confidence)]

  gate[021 release gate]
  drift[022 drift monitor]
  cost[023 cost ceiling]

  opslead([Operations lead])

  concierge --> gateway
  copilot --> gateway
  gateway --> active
  gateway -. circuit breaker .-> fb1
  gateway -. ceiling or breach .-> static
  gateway --> log
  log --> drift
  log --> cost
  gate -- promotes version --> gateway
  drift -- Tier 3 breach: auto-revert --> gateway
  drift -- alert --> opslead
  cost -- alert --> opslead
  opslead -- switches active version --> gateway

  classDef t1 fill:#EAF3DE,stroke:#639922,color:#173404
  classDef t2 fill:#FAEEDA,stroke:#BA7517,color:#412402
  classDef t3 fill:#EEEDFE,stroke:#7F77DD,color:#26215C
  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef cloud fill:#E6F1FB,stroke:#378ADD,color:#042C53
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528
  classDef ext fill:#FCEBEB,stroke:#E24B4A,color:#501313

  class concierge,copilot,gateway,gate,drift,cost cloud
  class active,fb1 ext
  class static t1
  class log store
  class opslead human
```

## Reading it

- **Solid arrows** are the request path. Both capabilities only ever call the gateway —
  neither holds a provider SDK.
- **Dashed arrows** are what happens when things go wrong: the circuit breaker to a
  cheaper or self-hosted fallback, and the drop to the Tier 1 static path when a cost
  ceiling or drift breach forces it. The static path depends on no provider at all.
- The **call log** is one write, read by three consumers — 021 needs it for audit
  sampling, 022 needs it for drift, 023 needs it for cost. One schema, not three.
- Only the operations lead can move the active pointer, and only to a version 021 has
  already passed.

## Open questions

- Whether shadowing (calling a candidate silently alongside the incumbent) is worth
  building before canarying is needed at real volume, or whether canary-only is enough
  given C8's growth curve.
