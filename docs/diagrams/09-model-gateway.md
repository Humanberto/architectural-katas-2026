# 09. Model gateway

**Go straight to:** [Home](../../README.md) · [ADRs](../adrs/README.md) · [Diagrams](README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

What sits between the two Tier 3 capabilities and any external provider: one gateway,
a ranked fallback per capability, and the log that feeds evaluation, drift detection
and cost control from a single source. Behind [020](../adrs/020-model-gateway.md).

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 75, 'curve': 'basis', 'padding': 12}}}%%
flowchart LR
  concierge[Visitor concierge<br/>Tier 3, answers the public]
  copilot[Operations copilot<br/>Tier 3, answers staff]

  gateway[Model Gateway<br/>the only holder of a provider key]

  subgraph prov["External provider — the part we do not control"]
    active{{Active model<br/>version pinned in config}}
    fb1{{Fallback model<br/>cheaper, same capability}}
  end

  static[Static FAQ tree and raw filter UI<br/>Tier 1, no provider, always available]

  log[(Gateway call log<br/>tier, model, version, cost, confidence)]

  gate[021 release gate<br/>nothing unproven becomes active]
  drift[022 drift monitor<br/>14-day rate vs release baseline]
  cost[023 cost ceiling<br/>cost per 1,000 visitors]

  opslead([Operations lead<br/>the only role that may switch a version])

  concierge --> gateway
  copilot --> gateway
  gateway -- normal path --> active
  gateway -. provider erroring or slow .-> fb1
  gateway -. ceiling hit or drift breach .-> static
  gateway -- one row per call --> log
  log --> drift
  log --> cost
  gate -- promotes a passing version --> gateway
  drift -- Tier 3 breach: reverts within minutes --> gateway
  drift -- Tier 1 and 2 breach: alerts only --> opslead
  cost -- price rise, same day --> opslead
  opslead -- config change, not a deploy --> gateway

  classDef t1 fill:#EAF3DE,stroke:#639922,color:#173404
  classDef t2 fill:#FAEEDA,stroke:#BA7517,color:#412402
  classDef t3 fill:#EEEDFE,stroke:#7F77DD,color:#26215C
  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef cloud fill:#E6F1FB,stroke:#378ADD,color:#042C53
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528
  classDef ext fill:#FCEBEB,stroke:#E24B4A,color:#501313

  class concierge,copilot,gateway,gate,drift,cost cloud
  class active,fb1 t3
  class static t1
  class log store
  class opslead human
```

## Reading it

- **Solid arrows** are the request path. Both capabilities only ever call the gateway,
  so a provider change is one config row rather than an edit everywhere.
- **Dashed arrows** are the failure paths, and the important one is the second: when the
  cost ceiling is hit or the drift monitor breaches, the capability drops to the green
  box. Green is Tier 1 — a fixed decision tree and a plain filter interface that existed
  before the AI did. It cannot be taken away by a provider, because it does not have one.
- The **call log** is one write read by three consumers. [021](../adrs/021-evaluating-ai-before-release.md) samples it for audit,
  [022](../adrs/022-detecting-ai-misbehaviour.md) reads it for drift, [023](../adrs/023-ai-cost-control.md) reads it for cost. One schema, not three.
- The two models sit inside the provider box and are coloured by tier rather than by who
  hosts them, per the [diagram key](README.md#the-key). Everything outside that box keeps working if the box goes dark.
- Only the operations lead can move the active pointer, and only to a version [021](../adrs/021-evaluating-ai-before-release.md) has
  already passed. Fast to flip, not fast to flip unsafely.

## Open questions

- Whether shadowing (calling a candidate silently alongside the incumbent) is worth
  building before canarying is needed at real volume, or whether canary-only is enough
  given [C8](../requirements.md#constraints)'s growth curve.

---
  ### Key

```mermaid
flowchart LR
  k1[/Sensor or device/] ~~~ k2[Runs on the estate] ~~~ k3[Deterministic, reproducible] ~~~ k4{{Perceptual model}} ~~~ k5([A person]) ~~~ k6[(Data store)]

  classDef t1 fill:#EAF3DE,stroke:#639922,color:#173404
  classDef t2 fill:#FAEEDA,stroke:#BA7517,color:#412402
  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528

  class k1,k2 edge
  class k3 t1
  class k4 t2
  class k5 human
  class k6 store
```
| Arrow | Meaning |
|---|---|
| Solid | A recorded fact |
| Dotted | An inference, presented as one |

Green is tier 1 and amber is tier 2, from [011](../adrs/011-ai-determinism-tiers.md). Full team
key in [README](README.md).


---

<p align="center">❦</p>

<p align="right"><a href="#09-model-gateway">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="../adrs/README.md">All ADRs</a> · <a href="README.md">All diagrams</a></p>
