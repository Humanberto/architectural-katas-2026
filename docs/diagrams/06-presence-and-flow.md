# 06. Presence and flow

Counting visitors without creating anything that identifies one. Decided in
[045](../adrs/045-presence-and-flow.md).

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

## Counting, and checking the count

```mermaid
flowchart LR

  counters[/Path counters/]
  gate[/Ticket validation/]

  subgraph estate["On the estate"]
    tally[Counts by area and hour]
    calib[Daily calibration]
    flow{{Movement inference}}
    store[(Visitor record)]
  end

  countess([Countess and managers])

  counters -->|Counts, LoRaWAN| tally
  gate -->|Daily entries| calib
  tally --> calib
  calib -->|Corrected counts| store
  store --> flow
  flow -.->|Route and dwell, inferred| store
  store -->|Where to invest and deploy staff| countess

  classDef t1 fill:#EAF3DE,stroke:#639922,color:#173404
  classDef t2 fill:#FAEEDA,stroke:#BA7517,color:#412402
  classDef t3 fill:#EEEDFE,stroke:#7F77DD,color:#26215C
  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef cloud fill:#E6F1FB,stroke:#378ADD,color:#042C53
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528
  classDef ext fill:#FCEBEB,stroke:#E24B4A,color:#501313

  class counters,gate,tally edge
  class calib t1
  class flow t2
  class store store
  class countess human
```

**Nothing here can identify a visitor.** Beam-break, thermal and time-of-flight counters
produce a number and nothing else: no image, no device address, nothing linkable to a person
afterwards. That is a property of the equipment rather than a policy, so there is no record to
protect and none to hand over.

Counters undercount groups walking abreast, and family passes mean groups are common. Daily
gate entries against daily counter totals give a correction factor per counter. Same pattern as
[046](../adrs/046-count-reconciliation.md): a frequent cheap estimate corrected by a scarcer
reliable figure.

Only the movement inference is a model, and it is the only dotted arrow. The gate total is its
one independent check, which catches gross errors and not subtle ones.

## The same counts are welfare data

```mermaid
flowchart LR

  store[(Visitor record)]
  conditions[(Enclosure conditions)]
  feeding[(Feeding record)]
  question{{Do animals behave differently on busy days?}}

  store --> question
  conditions --> question
  feeding --> question

  classDef t2 fill:#FAEEDA,stroke:#BA7517,color:#412402
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528

  class store,conditions,feeding store
  class question t2
```

Visitor counts are recorded by area on the same clock as feeding and enclosure conditions
([047](../adrs/047-environment-and-weather.md)), so whether crowding affects particular species
becomes answerable later. We are not claiming it does. The data to test it costs nothing extra
once the counters exist.

If a relationship turns out to be real, feeding schedules move, which would be a welfare
improvement derived from a visitor sensor.
