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

Everything inside the middle group runs on the estate, so safety alarms, the vet's limits and a keeper's working day continue when the connection does not. See ADR-040 for the topology, ADR-042 for the readings, ADR-044 for behaviour during an outage.

---

## Who may act

Three kinds of input, and what each is allowed to do on its own.

```mermaid
flowchart LR

  readings["<b>Enclosure readings</b><br/>[Container: MQTT]<br/>Temperature, oxygen,<br/>feeding, activity"]
  door["<b>Containment sensor</b><br/>[Container: MQTT device]<br/>Open or closed"]

  subgraph auto["May act on equipment by itself"]
    limits["<b>Vet's limits</b><br/>[Container: rules]<br/>Fixed thresholds, versioned"]
    kit["<b>Enclosure equipment</b><br/>[Container: pumps, heaters, lamps]"]
  end

  subgraph advise["May only tell a person"]
    model["<b>Welfare model</b><br/>[AI component]<br/>Spots trouble earlier,<br/>finds patterns"]
  end

  keeper["<b>Keeper</b><br/>[Person]<br/>Decides what happens"]
  security["<b>Security</b><br/>[Person]"]

  readings --> limits
  readings --> model
  limits -->|"Starts standing remediation"| kit
  limits -->|"Raises alert"| keeper
  model -.->|"Recommendation only"| keeper
  door -->|"Immediately, on the estate"| security
  door -->|"Immediately, on the estate"| keeper

  linkStyle 4 stroke:#C0442A,stroke-width:2px

  classDef person fill:#08427B,stroke:#052E56,color:#FFFFFF
  classDef container fill:#438DD5,stroke:#2E6295,color:#FFFFFF
  classDef ai fill:#8A5A00,stroke:#5E3D00,color:#FFFFFF

  class keeper,security person
  class readings,door,limits,kit container
  class model ai
```

**Key**

| | Meaning |
|---|---|
| Dark blue | A person |
| Mid blue | Something we build, run or store data in |
| Amber | A component whose behaviour comes from a model |
| Red dashed arrow | Cannot proceed without a person |

The model has no arrow to the equipment, and that absence is the decision. A limit written by a vet can start a pump on its own. Anything the model works out reaches a person and stops there.

The containment sensor passes both. A door is open or it is not, so nothing interprets it and nobody waits on a model. Decided in ADR-043.

---

## How we know the model still works

```mermaid
flowchart LR

  model["<b>Welfare model</b><br/>[AI component]"]
  alert["<b>Alert</b><br/>with confidence score<br/>and model version"]
  keeper["<b>Keeper</b><br/>[Person]<br/>Goes and looks"]
  record["<b>Alert record</b><br/>[Container: store]<br/>Was it real, or not"]

  model --> alert
  alert --> keeper
  keeper -->|"Confirms or dismisses"| record
  record -.->|"Labelled evidence"| model

  linkStyle 3 stroke:#C0442A,stroke-width:2px

  classDef person fill:#08427B,stroke:#052E56,color:#FFFFFF
  classDef container fill:#438DD5,stroke:#2E6295,color:#FFFFFF
  classDef ai fill:#8A5A00,stroke:#5E3D00,color:#FFFFFF

  class keeper person
  class alert,record container
  class model ai
```

Every alert a keeper closes tells us whether the model was right. That evidence costs no extra staff time, because closing an alert has to happen anyway.

One wrong alert is noise. The same animal repeatedly means its normal is wrong. Many animals at once means the model has drifted, a sensor is dirty, or something changed that nobody recorded. See ADR-043.
