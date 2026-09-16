# 02. Container view

**Go straight to:** [Home](../../README.md) · [ADRs](../adrs/README.md) · [Diagrams](README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

The whole system on one page. This is the picture the Countess and her managers will
study longest, and the one most likely to be wrong. Shapes and colours are in the [key](README.md#the-key).

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 75, 'curve': 'basis', 'padding': 12}}}%%
flowchart TB
  subgraph estate["On the estate"]
    sensors[/Enclosure and ride sensors/]
    counters[/Zone counting devices/]
    scanner[/Gate scanners/]
    broker[Satellite broker]
    localinf{{Local anomaly and counting models}}
    buffer[(Local buffer)]
  end

  subgraph cloud["In the cloud"]
    backbone[Event backbone]
    welfare[Welfare service]
    presence[Presence service]
    admissions[Admissions monolith]
    commercial[Commercial service]
    gateway[Model gateway]
    warehouse[(Analytics store)]
    ledger[(Welfare ledger)]
    passdb[(Admissions database)]
  end

  subgraph clients["Clients"]
    app[Visitor app]
    keeperapp[Keeper app]
    console[Management console]
  end

  providers[[Model providers]]
  payment[[Payment provider]]

  sensors --> broker
  counters --> broker
  scanner --> broker
  broker --- buffer
  broker --- localinf
  broker -->|Store and forward| backbone

  backbone --> welfare
  backbone --> presence
  backbone --> warehouse
  welfare --- ledger
  admissions --- passdb
  admissions -->|Admission events| backbone
  admissions --> payment
  presence --> warehouse
  commercial --- warehouse

  gateway --> providers
  commercial --- gateway
  console --- gateway

  app --> admissions
  app --- gateway
  keeperapp --- welfare
  console --- commercial

  classDef t1 fill:#EAF3DE,stroke:#639922,color:#173404
  classDef t2 fill:#FAEEDA,stroke:#BA7517,color:#412402
  classDef t3 fill:#EEEDFE,stroke:#7F77DD,color:#26215C
  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef cloud fill:#E6F1FB,stroke:#378ADD,color:#042C53
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528
  classDef ext fill:#FCEBEB,stroke:#E24B4A,color:#501313

  class sensors,counters,scanner,broker edge
  class localinf t1
  class buffer,ledger,passdb,warehouse store
  class backbone,welfare,presence,admissions,commercial,gateway cloud
  class app,keeperapp,console cloud
  class providers,payment ext
```

## What the picture is arguing

The seam from [010](../adrs/010-architecture-style.md) is the point of this diagram.
Everything inside "On the estate" keeps working when the link to the cloud drops.
Everything transactional sits in one box with one database.

Gate scanners publish through the broker rather than calling admissions directly. That
is deliberate: a scan is a fact to be forwarded, not a request needing an answer, which
is what makes offline validation possible in
[012](../adrs/012-admissions-and-ticketing.md).

The model gateway is the only thing that talks to model providers, per
[020](../adrs/020-model-gateway.md). Nothing else does.

## Known limitations of this view

- The keeper app should arguably sit on the estate, since keepers need it when the link
  is down.
- Ride condition sensing is bundled into "enclosure and ride sensors". D may want it
  separate.
- "Commercial service" is doing a lot of unexamined work — pricing, retention and
  reporting are three different things.
- No line shows the reconciliation path from cloud back to the estate, and there is one.

---

<p align="center">❦</p>

<p align="right"><a href="#02-container-view">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="../adrs/README.md">All ADRs</a> · <a href="README.md">All diagrams</a></p>
