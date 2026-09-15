# 05. Welfare monitoring

Two views. What is allowed to act on equipment, and how we find out whether the model is still
any good.

### Key

```mermaid
flowchart LR
  k1[/Sensor or device/] ~~~ k2[Runs on the estate] ~~~ k3[Fixed rule, reproducible] ~~~ k4{{Perceptual model}} ~~~ k5([A person]) ~~~ k6[(Data store)]

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
| Solid | Happens on its own |
| Dotted | Advice only, a person decides |

Green is tier 1 and amber is tier 2, from [011](../adrs/011-ai-determinism-tiers.md). Full team
key in [README](README.md).

## Who may act

```mermaid
flowchart LR

  readings[/Enclosure readings/]
  door[/Containment sensor/]
  equipstate[/Equipment state/]

  subgraph auto["May act on equipment"]
    limits[Vet's limits]
  end

  subgraph advise["May only advise"]
    model{{Welfare model}}
  end

  kit[Enclosure equipment]
  keeper([Keeper])
  security([Security])

  readings -->|LoRaWAN| limits
  readings -->|LoRaWAN| model
  equipstate -->|Wifi| model
  limits -->|Starts remediation, wifi or cable| kit
  kit -->|Reports what it did| equipstate
  limits -->|Raises alert| keeper
  model -.->|Recommendation only| keeper
  door -->|Immediately, on estate| security
  door -->|Immediately, on estate| keeper

  classDef t1 fill:#EAF3DE,stroke:#639922,color:#173404
  classDef t2 fill:#FAEEDA,stroke:#BA7517,color:#412402
  classDef t3 fill:#EEEDFE,stroke:#7F77DD,color:#26215C
  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef cloud fill:#E6F1FB,stroke:#378ADD,color:#042C53
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528
  classDef ext fill:#FCEBEB,stroke:#E24B4A,color:#501313

  class readings,door,equipstate,kit edge
  class limits t1
  class model t2
  class keeper,security human
```

The model has no arrow to the equipment. A limit written by a vet can start a pump on its own.
Anything the model works out reaches a person and stops there, which is why its one arrow is
dotted. Decided in [043](../adrs/043-welfare-loop.md).

Readings arrive over LoRaWAN, but commands do not travel back that way: a LoRaWAN device only
listens briefly after transmitting, so equipment is reached over wifi or cable
([041](../adrs/041-hybrid-transport.md)).

Equipment reports its own state rather than only receiving instructions. Commanded on and
actually on are different facts, and only one is evidence
([047](../adrs/047-environment-and-weather.md)). That loop is also how a failed mister or lamp
is distinguished from a sick animal.

The containment sensor passes both boxes. A door is open or it is not, so nothing interprets it
and nobody waits on a model.

## How we know the model still works

```mermaid
flowchart LR

  cohort[(Cohort baselines)]
  model{{Welfare model}}
  alert[Alert, version, confidence]
  keeper([Keeper])
  record[(Alert outcomes)]

  cohort -->|Expected range for a new animal| model
  model --> alert
  alert --> keeper
  keeper -->|Confirms or dismisses| record
  record -.->|Labelled evidence| model
  record -.->|Individual history| cohort

  classDef t1 fill:#EAF3DE,stroke:#639922,color:#173404
  classDef t2 fill:#FAEEDA,stroke:#BA7517,color:#412402
  classDef t3 fill:#EEEDFE,stroke:#7F77DD,color:#26215C
  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef cloud fill:#E6F1FB,stroke:#378ADD,color:#042C53
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528
  classDef ext fill:#FCEBEB,stroke:#E24B4A,color:#501313

  class alert edge
  class model t2
  class keeper human
  class cohort,record store
```

Every alert a keeper closes tells us whether the model was right. That evidence costs no extra
staff time, because closing an alert has to happen anyway.

A new animal has no history, so its expected range starts as its cohort's, meaning same
species, archetype and season, and becomes its own as outcomes accumulate
([047](../adrs/047-environment-and-weather.md)).

One wrong alert is noise. The same animal repeatedly means our idea of its normal is wrong.
Many animals at once means the model has drifted, a sensor is dirty, or something changed that
nobody recorded.

Also in [043](../adrs/043-welfare-loop.md).
