# Edge and animals

Diagrams for the estate network and the animal welfare monitoring. Track C.

---

## From the enclosure to the cloud

How a reading travels, and what still works when the estate loses its connection.

```mermaid
flowchart LR

  subgraph field["In the enclosures"]
    aq["Aquatic sensors<br/>temperature, oxygen,<br/>chemistry, flow"]
    terr["Terrestrial sensors<br/>temperature, humidity,<br/>lamps, containment"]
    cam["Surface camera<br/>lagoon only"]
  end

  subgraph estate["On the estate — keeps working with no connection"]
    sat1["Satellite broker<br/>buffers locally"]
    sat2["Satellite broker<br/>buffers locally"]
    central["Central broker"]
    server["Estate server<br/>vet limits, alarms,<br/>store and forward"]
    keeper["Keeper"]
  end

  subgraph cloud["In the cloud — needs the connection"]
    analytics["Long-term analysis<br/>and reporting"]
    hosted["Hosted models"]
  end

  aq -->|MQTT| sat1
  terr -->|MQTT| sat1
  cam -->|MQTT| sat2

  sat1 -->|MQTT| central
  sat2 -->|MQTT| central
  central --> server

  server -->|"alerts"| keeper
  keeper -->|"acknowledges,<br/>records what happened"| server

  server -.->|"when the link is up"| analytics
  server -.-> hosted

  classDef person fill:#08427B,stroke:#052E56,color:#FFFFFF
  classDef container fill:#438DD5,stroke:#2E6295,color:#FFFFFF
  classDef external fill:#999999,stroke:#6B6B6B,color:#FFFFFF

  class keeper person
  class aq,terr,cam,sat1,sat2,central,server container
  class analytics,hosted external
```

**Key**

| | Meaning |
|---|---|
| Dark blue | A person |
| Mid blue | Something we are building or running |
| Grey | Something outside the estate that we depend on |
| Solid arrow | Always available |
| Dashed arrow | Only when the connection is up |

Everything inside the middle group runs on the estate. Safety alarms, the vet's limits, and a keeper's whole working day sit on that side of the line, so none of them stop when the connection does. Decided in ADR-040, with the readings themselves defined in ADR-042 and the behaviour during an outage in ADR-044.
