# 040. Tiered MQTT topology with prioritised local buffering

**Go straight to:** [Home](../../README.md) · [ADRs](README.md) · [Diagrams](../diagrams/README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

## Status

Proposed. **Tiers 1 and 2 are amended by [ADR-041](041-hybrid-transport.md)**, which replaces
the sensor radio with LoRaWAN and the satellite brokers with gateways feeding a single estate
machine. The split between what runs on the estate and what runs in the cloud, below, is
unchanged and still stands.

## Context

- The estate is large and sprawling with patchy wifi coverage ([C1](../requirements.md#constraints))
- Budget covers MQTT-capable devices installed throughout the park ([C3](../requirements.md#constraints))
- Cloud services are permitted, but the estate-to-cloud path must be designed rather than assumed ([C2](../requirements.md#constraints))
- 200+ animals across 55 enclosures ([C5](../requirements.md#constraints)), aquatic and land-based, some venomous ([C6](../requirements.md#constraints)), with restricted and hazardous physical access ([C10](../requirements.md#constraints))
- 40 rides ([C4](../requirements.md#constraints)), and the Countess needs to know which parts of the estate are popular ([P2](../requirements.md#problems))
- A family estate with a small operations staff and no technology department ([C13](../requirements.md#constraints)), so any topology has to be operable by very few people

## Decision

A three-tier MQTT topology with local processing and prioritised, opportunistic cloud sync.

| Tier | What it is | Responsibility |
|---|---|---|
| 1 | Sensors in enclosures, on rides, at path pinch points | Publish, and buffer their own recent readings |
| 2 | Satellite brokers distributed across the park | Keep every sensor in radio range, bridge to the central broker, buffer when that link is down |
| 3 | Central broker and estate server | Pre-process, then process, analyse and decide locally |

Cloud sync is opportunistic and prioritised: the server ships data when connectivity allows,
ordering the outbound queue by priority rather than arrival time.

Tiers 1 and 2 are amended by [ADR-041](041-hybrid-transport.md). Tier 3 and everything below
are unaffected.

### What runs where

The split is by consequence and time horizon, not by data type.

| Runs on the estate | Runs in the cloud |
|---|---|
| Enclosure environment control and alarms | Visitor movement and behaviour analysis |
| Security and access control | Long-horizon animal welfare trends |
| Feeding events and immediate welfare alerts | Revenue and commercial analysis |
| Anything with a safety consequence in minutes | Anything measured in hours or days |

The rule: **if failing to act within minutes has a safety or revenue consequence, it runs
locally.** A tank heater failing at 2am cannot wait on an uplink. Footfall analysis can wait
until morning.

Whether model-derived instructions may travel back down to actuate enclosure controls is an
authority question, decided in [ADR-043](043-welfare-loop.md), not here.

## Alternatives rejected

| Option | Why not |
|---|---|
| Sensors publish directly to a cloud IoT service | No on-site infrastructure to own, but every reading then depends on wifi known to be unreliable, and nothing on the estate works when the uplink is down |
| A single central broker, all sensors publishing directly to it | Range and obstruction make full coverage from one point unrealistic, and it concentrates all risk in one device. ADR-041 revisits this, because LoRaWAN changes the range argument |

## Consequences

| Decision | Cost |
|---|---|
| Local processing and buffering | The estate owns physical hardware needing power, weatherproofing and patching, with very little staff to do it ([C13](../requirements.md#constraints)) |
| Distributed satellite brokers | Each one is another device that can fail unnoticed, and siting is a survey problem rather than a map exercise |
| A central broker | It is a single point of failure, and everything upstream of tier 2 depends on it. Redundancy has not been costed. This is the largest open risk in this record |
| Opportunistic cloud sync | Cloud data is stale by an unpredictable amount, so nothing time-critical can rely on it |
| Logic in two places | Local and cloud processing have to be kept consistent, which is ongoing effort |
| A prioritised queue | Only as good as the classification behind it, and that classification will drift as features are added |

### What this provides

- Safety monitoring, alarms and access control have no cloud dependency
- Buffering turns data lost to an outage into data delayed by one
- A weak uplink is spent on what matters rather than first in, first out
- Adding an enclosure is a local change

## Assumptions

- Day-to-day operation is handled by very few staff, none of them specialists. The brief does
  not describe the technology staffing, so this follows from the estate being a family
  business rather than a technology company ([C13](../requirements.md#constraints))
- The funded MQTT budget covers the brokers. Anything beyond it needs a separate case
  ([C14](../requirements.md#constraints))

## Related

- **[ADR-041](041-hybrid-transport.md)** amends tiers 1 and 2
- **[ADR-042](042-telemetry-model.md)** defines what travels across this topology
- **[ADR-043](043-welfare-loop.md)** decides what may act on it
- **[ADR-044](044-disconnected-operation.md)** covers behaviour during an outage

---

<p align="center">❦</p>

<p align="right"><a href="#040-tiered-mqtt-topology-with-prioritised-local-buffering">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="README.md">All ADRs</a> · <a href="../diagrams/README.md">All diagrams</a></p>
