# Diagrams

Diagrams are written as Mermaid inside Markdown. GitHub renders them, so the source and
the picture are the same file and cannot drift apart. No export step, no `.png` to keep
in sync.

To edit one, edit the fenced block. To add one, copy an existing file.

| Diagram | Shows | Seat |
|---|---|---|
| [01 System context](01-system-context.md) | Who uses the estate systems and what we depend on | A |
| [02 Container view](02-container-view.md) | The whole system, one page | A |
| [03 AI capability map](03-ai-capability-map.md) | Every AI capability, its tier and its authority | A |
| _04 Edge connectivity_ | Satellite brokers, buffering, what survives a partition | C |
| _05 Welfare monitoring_ | Sensors to alert to keeper | C |
| _06 Presence and flow_ | Counting without identifying | C |
| _07 Ride condition_ | Sensing, advisory, and the inspection boundary | D |
| _08 Concierge offline behaviour_ | What is cached and what needs signal | D |
| [09 Pass lifecycle](09-pass-lifecycle.md) | States a pass moves through, and what the gate does in each | A |

Italics are not yet drawn. 01 to 03 are strawmen — argue with them.

## The key

Every diagram uses these shapes and colours and nothing else. If you need a new one, add
it here first so the rest of us know what it means.

```mermaid
flowchart LR
  comp[Component we build]
  person([A person])
  store[(Data store)]
  model{{AI or ML model}}
  device[/Physical sensor or device/]
  ext[[External third party]]

  comp --- person --- store --- model --- device --- ext

  classDef t1 fill:#EAF3DE,stroke:#639922,color:#173404
  classDef t2 fill:#FAEEDA,stroke:#BA7517,color:#412402
  classDef t3 fill:#EEEDFE,stroke:#7F77DD,color:#26215C
  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef cloud fill:#E6F1FB,stroke:#378ADD,color:#042C53
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528
  classDef ext fill:#FCEBEB,stroke:#E24B4A,color:#501313

  class comp cloud
  class person human
  class store store
  class model t1
  class device edge
  class ext ext
```

**Shapes**

| Shape | Meaning |
|---|---|
| Rectangle | A component we build |
| Stadium | A person |
| Cylinder | A data store |
| Hexagon | An AI or ML model |
| Parallelogram | A physical sensor or device |
| Subroutine box | An external third party |

**Colours**

| Colour | Meaning |
|---|---|
| Green | Tier 1, classical and reproducible |
| Amber | Tier 2, perceptual |
| Purple | Tier 3, generative |
| Teal | Runs on the estate |
| Blue | Runs in the cloud |
| Grey | A person |
| Pink | A data store |
| Red | External third party |

Tier colours come from [011](../adrs/011-ai-determinism-tiers.md). Where a node is both
a model and on the estate, colour it by tier — the estate placement is usually obvious
from which subgraph it sits in.

Paste the eight `classDef` lines verbatim into any new diagram.

## State diagrams

The shapes and colours above describe components: things we build, people, stores, models,
devices, third parties. A state diagram has none of those — its boxes are states of one
thing — so the key does not apply to it.

Leave state diagrams uncoloured. Carry the meaning in transition labels and notes instead.
Reusing the tier colours would be actively misleading: amber means "Tier 2, perceptual" and
nothing else, and a state coloured amber in a diagram with no model in it invites exactly
the wrong reading. [09](09-pass-lifecycle.md) is the example to copy.

## House rules

- Keep node labels under about 30 characters.
- If a label needs a bracket, quote the whole label: `A["Gate scanner (offline)"]`.
- Reference every diagram from an ADR or `docs/overview.md`. Judges only see what is
  linked.
- Fewer boxes is better. If a diagram needs more than about 25, it is two diagrams.
