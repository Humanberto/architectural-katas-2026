# 04. Edge connectivity

**Go straight to:** [Home](../../README.md) · [ADRs](../adrs/README.md) · [Diagrams](README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

How a reading reaches the estate, and what keeps working when the estate loses its connection
to the outside world.

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 75, 'curve': 'basis', 'padding': 12}}}%%
flowchart LR

  subgraph enclosures["In the enclosures"]
    aq[/Aquatic sensors/]
    terr[/Terrestrial sensors/]
    door[/Containment sensors/]
    counters[/Path counters/]
    cam[/Surface camera/]
    kit[/Misters, lamps, pumps/]
  end

  subgraph estate["On the estate — survives a cloud outage"]
    gw[LoRaWAN gateways]
    box[Estate machine: broker, network server, estate server]
    local[(Buffered readings and clips)]
    keeper([Keeper])
  end

  subgraph cloud["In the cloud — needs the link"]
    analytics[Trends and reporting]
    forecast[[Weather forecast]]
    hosted[[Hosted models]]
  end

  aq -->|Readings, LoRaWAN| gw
  terr -->|Readings, LoRaWAN| gw
  door -->|Events, LoRaWAN| gw
  counters -->|Counts, LoRaWAN| gw
  cam -->|Counts, wifi| box
  kit -->|State, wifi or cable| box
  box -->|Commands, wifi or cable| kit

  gw -->|Publishes, MQTT| box
  box -->|Holds until sent| local
  box -->|Raises alerts| keeper
  keeper -->|Confirms outcome| box

  local -.->|Uploads when link is up| analytics
  forecast -.->|Pulled when link is up| box
  box -.->|Assessment, when link is up| hosted

  classDef t1 fill:#EAF3DE,stroke:#639922,color:#173404
  classDef t2 fill:#FAEEDA,stroke:#BA7517,color:#412402
  classDef t3 fill:#EEEDFE,stroke:#7F77DD,color:#26215C
  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef cloud fill:#E6F1FB,stroke:#378ADD,color:#042C53
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528
  classDef ext fill:#FCEBEB,stroke:#E24B4A,color:#501313

  class aq,terr,door,counters,cam,kit,gw,box edge
  class local store
  class keeper human
  class analytics cloud
  class forecast,hosted ext
```

### Key

```mermaid
flowchart LR
  k1[/Sensor or device/] ~~~ k2[Runs on the estate] ~~~ k3[(Data store)] ~~~ k4([A person]) ~~~ k5[Runs in the cloud] ~~~ k6[[External third party]]

  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef cloud fill:#E6F1FB,stroke:#378ADD,color:#042C53
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528
  classDef ext fill:#FCEBEB,stroke:#E24B4A,color:#501313

  class k1,k2 edge
  class k3 store
  class k4 human
  class k5 cloud
  class k6 ext
```

| Arrow | Meaning |
|---|---|
| Solid | Always works, connection or not |
| Dotted | Only while the link to the cloud is up |

Full team key in [README](README.md).

### Reading it

**Two radios, one protocol.** Sensors speak LoRaWAN, which reaches the middle of the estate
from anywhere on it, including the wifi dead zones. A LoRaWAN message is a few dozen bytes, so
anything larger stays on wifi: the camera publishes counts rather than frames, and the
equipment is reached over wifi or cable because LoRaWAN cannot deliver a command promptly
([041](../adrs/041-hybrid-transport.md)).

**Equipment reports back.** The arrow from the equipment is as important as the one to it.
Commanded on and actually on are different facts, and only the second is evidence
([047](../adrs/047-environment-and-weather.md)).

**One box, not four.** The broker, the LoRaWAN network server and the estate server run on one
machine. Keeping the network server on the estate is what lets sensor data stay readable during
a cloud outage. It is also a single point of failure, named as the largest open risk in
[041](../adrs/041-hybrid-transport.md).

**Nothing in the cloud group is on the path to an alert.** An assessment we cannot reach is one
we can do without. The forecast is the only inbound cloud arrow, and it buys warning time
rather than triggering anything ([047](../adrs/047-environment-and-weather.md)).

See [040](../adrs/040-connectivity-topology.md) for what runs on the estate and what runs in
the cloud, [042](../adrs/042-telemetry-model.md) for what travels, and
[044](../adrs/044-disconnected-operation.md) for the three kinds of outage and how each behaves.

---

<p align="center">❦</p>

<p align="right"><a href="#04-edge-connectivity">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="../adrs/README.md">All ADRs</a> · <a href="README.md">All diagrams</a></p>
