# Edge and animals

Diagrams for the estate network and animal welfare monitoring. Track C.

---

## From the enclosure to the cloud

C4 container view. How a reading travels, and what still works when the estate loses its connection.

```mermaid
flowchart LR

  subgraph field["In the enclosures"]
    aq["<b>Aquatic sensors</b><br/>[Container: MQTT device]<br/>Water condition in the lagoon"]
    terr["<b>Terrestrial sensors</b><br/>[Container: MQTT device]<br/>Conditions and containment"]
    cam["<b>Surface camera</b><br/>[Container: MQTT device]<br/>Sees fish that surface to feed"]
  end

  subgraph estate["On the estate — keeps working with no connection"]
    sat["<b>Satellite brokers</b><br/>[Container: MQTT broker]<br/>Buffer when the centre is unreachable"]
    central["<b>Central broker</b><br/>[Container: MQTT broker]<br/>Every reading passes through here"]
    server["<b>Estate server</b><br/>[Container: application and local store]<br/>Applies the vet's limits, raises alarms,<br/>holds readings until they can be sent"]
    keeper["<b>Keeper</b><br/>[Person]<br/>Acts on alerts"]
  end

  subgraph cloud["In the cloud — needs the connection"]
    analytics["<b>Analysis and reporting</b><br/>[Container: cloud service]<br/>Trends and reports over months"]
    hosted["<b>Hosted models</b><br/>[External system]<br/>Assessments we cannot run on the estate"]
  end

  aq -->|"Publishes readings [MQTT]"| sat
  terr -->|"Publishes readings [MQTT]"| sat
  cam -->|"Publishes counts [MQTT]"| sat

  sat -->|"Forwards [MQTT bridge]"| central
  central -->|"Delivers readings"| server

  server -->|"Raises alerts"| keeper
  keeper -->|"Confirms, records outcome"| server

  server -.->|"Uploads when the link is up"| analytics
  server -.->|"Requests assessment<br/>when the link is up [HTTPS]"| hosted

  classDef person fill:#08427B,stroke:#052E56,color:#FFFFFF
  classDef container fill:#438DD5,stroke:#2E6295,color:#FFFFFF
  classDef external fill:#999999,stroke:#6B6B6B,color:#FFFFFF

  class keeper person
  class aq,terr,cam,sat,central,server,analytics container
  class hosted external
```

**Key**

| | Meaning |
|---|---|
| Dark blue | A person |
| Mid blue | A container. Something we build, run or store data in |
| Grey | An external system we depend on but do not control |
| Solid arrow | Always available |
| Dashed arrow | Only while the connection is up |

Every box names what it is and what technology it runs on. Every arrow names its purpose, and its protocol where that matters.

Everything inside the middle group runs on the estate, so safety alarms, the vet's limits and a keeper's working day continue when the connection does not. See ADR-040 for the topology, ADR-042 for the readings, ADR-044 for behaviour during an outage.
