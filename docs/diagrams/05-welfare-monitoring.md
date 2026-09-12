# 05. Welfare monitoring

Two views. What is allowed to act on equipment, and how we find out whether the model is
still any good.

## Who may act

```mermaid
flowchart LR

  readings[/Enclosure readings/]
  door[/Containment sensor/]

  subgraph auto["May act on equipment"]
    limits[Vet's limits]
    kit[Enclosure equipment]
  end

  subgraph advise["May only advise"]
    model{{Welfare model}}
  end

  keeper([Keeper])
  security([Security])

  readings --> limits
  readings --> model
  limits -->|Starts remediation| kit
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

  class readings,door,kit edge
  class limits t1
  class model t2
  class keeper,security human
```

The model has no arrow to the equipment, and that absence is the decision. A limit written
by a vet can start a pump on its own. Anything the model works out reaches a person and
stops there, which is why its one arrow is dotted.

The containment sensor passes both. A door is open or it is not, so nothing interprets it
and nobody waits on a model.

Decided in [043](../adrs/043-welfare-loop.md).

## How we know the model still works

```mermaid
flowchart LR

  model{{Welfare model}}
  alert[Alert, version, confidence]
  keeper([Keeper])
  record[(Alert outcomes)]

  model --> alert
  alert --> keeper
  keeper -->|Confirms or dismisses| record
  record -.->|Labelled evidence| model

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
  class record store
```

Every alert a keeper closes tells us whether the model was right. That evidence costs no
extra staff time, because closing an alert has to happen anyway.

One wrong alert is noise. The same animal repeatedly means our idea of its normal is wrong.
Many animals at once means the model has drifted, a sensor is dirty, or something changed
that nobody recorded.

Also in [043](../adrs/043-welfare-loop.md).
