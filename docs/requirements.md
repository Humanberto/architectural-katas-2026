# Problems, requirements and constraints

**Go straight to:** [Home](../README.md) · [ADRs](adrs/README.md) · [Diagrams](diagrams/README.md) · [Implementation](implementation.md) · [Requirements](requirements.md) · [Characteristics](architecture-characteristics.md) · [Brief](kata-brief.pdf)

Everything the Von Digitalis brief tells us, given an ID so ADRs and diagrams can cite it.

Each item is marked **stated** (it appears in the brief) or **derived** (a reasonable inference the team has agreed to treat as true). Derived items are assumptions, and are called out as such in the overview.

---

## Problems

What hurts today.

| ID | Problem | Source |
|---|---|---|
| P1 | The estates are unprofitable and the former revenue source (garden gnomes) is gone | stated |
| P2 | No visibility into which parts of the estate are popular, so investment and staff deployment are guesswork | stated |
| P3 | Animal care is costly, and significantly more so when animals get sick | stated |
| P4 | Few returning visitors, and no understanding of how to increase them | stated |
| P5 | Visitor volume must roughly triple or the carnivorous plant collection must be sold | stated |
| P6 | Piranha population levels are unknown, and the animals jump, so counts drift | stated |
| P7 | The animal collection was private and is newly public, so no public-facing operation exists for it | stated |
| P8 | There is no ticketing or admission system today | derived |
| P9 | Feeding is currently unmeasured, so nobody knows whether an animal ate or how well | derived |

---

## Requirements

What the system must do.

| ID | Requirement | Source |
|---|---|---|
| R1 | Sell tickets, including family passes, for access to the estates | stated |
| R2 | Validate admission at entry at scale | derived |
| R3 | Measure the popularity of different areas of the park | stated |
| R4 | Turn that measurement into staffing and investment decisions | stated |
| R5 | Monitor animal health | stated |
| R6 | Track how much and how well animals are eating | stated |
| R7 | Count piranha population levels | stated |
| R8 | Grow visitor numbers | stated |
| R9 | Increase profitability | stated |
| R10 | Increase returning visitors | stated |
| R11 | Move information from the estate to the cloud | stated |
| R12 | Use AI in the solution, and demonstrate that use is innovative | stated |
| R13 | Validate and verify AI results, including detecting misbehaviour in production | stated |
| R14 | Survive model or provider change, price change, or shutdown | stated |
| R15 | Keep operating when the estate is disconnected from the cloud | derived |

---

## Constraints

What limits or shapes any solution.

| ID | Constraint | Source |
|---|---|---|
| C1 | Wifi coverage across the park is patchy | stated |
| C2 | Cloud is permitted, but the estate-to-cloud path must be designed, not assumed | stated |
| C3 | Budget exists for MQTT-capable hardware throughout the park is funded | stated |
| C4 | 40 rides | stated |
| C5 | 200+ animals across 55 displays and enclosures | stated |
| C6 | Mix of aquatic and land-based animals; some poisonous | stated |
| C7 | Rides are 18th-century and historically important, so physical modification is limited | derived |
| C8 | Load must scale from 5,000 to 15,000+ visitors per day | stated |
| C9 | Three-year horizon for that growth | stated |
| C10 | Physical access to venomous and aquatic enclosures is restricted and hazardous | derived |
| C11 | AI models and providers change fast, including pricing and availability | stated |
| C12 | GenAI behaviour is non-deterministic | stated |
| C13 | A family estate, not a technology company — a small operations staff and no in-house ML team | derived |
| C14 | The brief is silent on budget beyond MQTT-capable devices. We treat that as the funded baseline and require anything further to be argued for | derived |

---

## How to use these IDs

Cite them inline in ADRs and diagram notes: `... has patchy wifi coverage (C1)`.

---

<p align="center">❦</p>

<p align="right"><a href="#problems-requirements-and-constraints">↑ Back to top</a> · <a href="../README.md">Home</a> · <a href="adrs/README.md">All ADRs</a> · <a href="diagrams/README.md">All diagrams</a></p>
