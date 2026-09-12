# 04. Edge connectivity

How a reading travels from an enclosure to the cloud, and what keeps working when the
estate loses its connection.

```mermaid
flowchart LR

  subgraph enclosures["In the enclosures"]
    aq[/Aquatic sensors/]
    terr[/Terrestrial sensors/]
    cam[/Surface camera/]
  end

  subgraph estate["On the estate — survives a partition"]
    sat[Satellite brokers]
    central[Central broker]
    server[Estate server]
    local[(Buffered readings)]
    keeper([Keeper])
  end

  subgraph cloud["In the cloud — needs the link"]
    analytics[Trends and reporting]
    hosted[[Hosted models]]
  end

  aq -->|Readings, MQTT| sat
  terr -->|Readings, MQTT| sat
  cam -->|Counts, MQTT| sat

  sat -->|MQTT bridge| central
  central -->|Delivers readings| server
  server -->|Holds until sent| local

  server -->|Raises alerts| keeper
  keeper -->|Confirms outcome| server

  local -.->|Uploads when link is up| analytics
  server -.->|Assessment, when link is up| hosted

  classDef t1 fill:#EAF3DE,stroke:#639922,color:#173404
  classDef t2 fill:#FAEEDA,stroke:#BA7517,color:#412402
  classDef t3 fill:#EEEDFE,stroke:#7F77DD,color:#26215C
  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef cloud fill:#E6F1FB,stroke:#378ADD,color:#042C53
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528
  classDef ext fill:#FCEBEB,stroke:#E24B4A,color:#501313

  class aq,terr,cam,sat,central,server edge
  class local store
  class keeper human
  class analytics cloud
  class hosted ext
```

Solid arrows always work. Dotted arrows only work while the link is up.

Everything in the middle group runs on the estate, so safety alarms, the vet's limits and
a keeper's working day carry on when the connection does not. The satellite brokers buffer
for their own patch of the park; the estate server buffers for the estate as a whole.

Nothing in the cloud group is on the path to an alert. That is deliberate: an assessment we
cannot reach is an assessment we can do without.

See [040](../adrs/040-connectivity-topology.md) for the topology,
[042](../adrs/042-telemetry-model.md) for what travels,
[044](../adrs/044-disconnected-operation.md) for behaviour during an outage.
