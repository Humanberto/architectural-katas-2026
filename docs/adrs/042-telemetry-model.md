# 042. Telemetry model, topic taxonomy, and delivery guarantees

**Go straight to:** [Home](../../README.md) · [ADRs](README.md) · [Diagrams](../diagrams/README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

## Status

Proposed

## Context

ADR-040 established a tiered MQTT topology. This record defines what travels across it. It specifies which measurements are taken, how topics are named, and what delivery guarantee each stream receives.

The estate holds more than 200 animals across 55 displays and enclosures ([C5](https://github.com/Humanberto/architectural-katas-2026/blob/adr/040-connectivity/docs/requirements.md#:~:text=C5,displays%20and%20enclosures)). They are split between aquatic and land-based species, several of them venomous, in enclosures where physical access is restricted and hazardous ([C6](https://github.com/Humanberto/architectural-katas-2026/blob/adr/040-connectivity/docs/requirements.md#:~:text=C6,animals%3B%20some%20poisonous), [C10](https://github.com/Humanberto/architectural-katas-2026/blob/adr/040-connectivity/docs/requirements.md#:~:text=C10,restricted%20and%20hazardous)). Keepers cannot inspect every enclosure continuously, and the estate runs on a small operations staff ([C13](https://github.com/Humanberto/architectural-katas-2026/blob/adr/040-connectivity/docs/requirements.md#:~:text=C13,house%20ML%20team)). Wifi coverage is patchy ([C1](https://github.com/Humanberto/architectural-katas-2026/blob/adr/040-connectivity/docs/requirements.md#:~:text=C1,park%20is%20patchy)) and only MQTT-capable hardware is funded as a baseline ([C3](https://github.com/Humanberto/architectural-katas-2026/blob/adr/040-connectivity/docs/requirements.md#:~:text=C3,park%20is%20funded), [C14](https://github.com/Humanberto/architectural-katas-2026/blob/adr/040-connectivity/docs/requirements.md#:~:text=C14,be%20argued%20for)).

We have two questions that need a decision now rather than at implementation time.

The first is naming. Fifty-five enclosures, forty rides, and the gates together produce a large topic space with several different consumers. Without an agreed shape, every consumer writes its own parsing, and adding a single enclosure becomes a change that ripples outward.

The second is delivery. MQTT offers three quality-of-service levels at different costs. Using the strongest one everywhere spends constrained uplink bandwidth on data that does not need it. Using the weakest one everywhere loses information that can never be recovered.

## Decision

### Topic taxonomy

```
estate/enclosure/{enclosure_id}/{measure}
estate/enclosure/{enclosure_id}/status
estate/ride/{ride_id}/{measure}
estate/gate/{gate_id}/footfall
estate/gateway/{gateway_id}/status
```

Four rules govern it.

Segments are lowercase, hyphenated nouns. No spaces and no display names, because display names change and topics should not.

An `{enclosure_id}` stays fixed for the life of the enclosure and is never reused, even after one is decommissioned. Reusing an identifier silently merges the history of two unrelated habitats.

Each topic carries one measurement. Consumers subscribe to what they need using wildcards, so `estate/enclosure/+/water-temp` reaches all 55 enclosures without listing any of them.

Adding an enclosure or a new measure is additive. Nothing that already subscribes has to change.

### What belongs on the backbone

Not every system on the estate should publish here. The backbone is for telemetry
from constrained or remote devices, sent one way, where the sender does not need
an answer and can tolerate delay.

That covers enclosure sensors, gate and path counters, ride cycle events, queue
sensors, and check-in points in parts of the park with no power and no reliable
signal.

It does not cover anything that needs a synchronous response, a strong security
boundary, or transactional guarantees. Payment authorisation, ticket purchase and
point-of-sale transactions use the estate API instead, because a fire-and-forget
protocol is the wrong tool for money.

Systems on the API side may still publish an anonymised event to the backbone once
their transaction has completed, so that anything measuring how the park is used has
a single place to look.

### What is measured

**Aquatic enclosures**

| Measure | Topic segment | Interval |
|---|---|---|
| Water temperature | `water-temp` | 1 min |
| Dissolved oxygen | `dissolved-oxygen` | 1 min |
| pH | `ph` | 15 min |
| Ammonia | `ammonia` | 15 min |
| Nitrite and nitrate | `nitrite`, `nitrate` | 15 min |
| Filtration flow rate | `filter-flow` | 5 min |
| Water level | `water-level` | 5 min |
| Turbidity | `turbidity` | 15 min |
| Feed dispensed | `feed-dispensed` | on event |

Dissolved oxygen is sampled as often as temperature because an oxygen crash kills faster than temperature drift or ammonia buildup. It is the shortest fuse in an aquatic system.

**Terrestrial enclosures**

| Measure | Topic segment | Interval |
|---|---|---|
| Air temperature | `air-temp` | 5 min |
| Humidity | `humidity` | 5 min |
| Heat and UV lamp state | `lamp-state` | on change |
| Containment state, door and latch | `containment` | on change |
| Movement and activity | `activity` | 5 min |
| Water dish level | `water-level` | 15 min |
| Feed dispensed | `feed-dispensed` | on event |
| Feed remaining after interval | `feed-remaining` | on event |

Every venomous enclosure reports containment state. An escape is the most serious event that can happen on this estate, and the sensor costs very little compared to that.

Lamp state earns its place because heat and UV lamp failure is common, invisible without instrumentation, and harms reptiles within hours.

### Delivery guarantees

The rule we apply is recoverability rather than importance.

A lost sample from a continuous stream is replaced by the next one within minutes, and the trend survives. A lost discrete event is gone for good. Nothing arriving later can tell us whether an animal ate.

| QoS | Applied to | Reasoning |
|---|---|---|
| 0, at most once | Continuous samples. Temperature, dissolved oxygen, pH, ammonia, nitrite, nitrate, flow, humidity, activity, turbidity, levels | Another reading follows within 1 to 15 minutes. Losing one does not lose the trend. |
| 1, at least once | Discrete events. Feed dispensed, feed remaining, containment change, lamp state change, threshold alarms, gateway online and offline | Singular and impossible to reconstruct. Duplicates are tolerable, loss is not. |
| 2, exactly once | Not used | The extra handshake is not worth its cost on a constrained uplink. Where exactly-once behaviour is genuinely required, publishers attach an idempotency key and consumers discard repeats. That approach is cheaper and also protects against duplicates arriving from anywhere else. |

Alarms are events rather than samples. A temperature reading goes out at QoS 0. An alarm raised because that reading crossed a threshold goes out at QoS 1 on `estate/enclosure/{id}/alarm`. The raw stream stays cheap while the signal that matters is guaranteed.

### Retained messages and last known state

Status topics are published with the retained flag set. A keeper's tablet, or a dashboard that has just started, receives the current state of all 55 enclosures the moment it subscribes. No database query and no round trip to the cloud.

Measurement topics are not retained. A retained reading looks current even when it is hours old, and a stale value presented as live is more dangerous than a visible gap.

### Sensor liveness

Every publishing device registers a last will and testament on its status topic. When a device disconnects without saying goodbye, whether from battery failure, water ingress or physical damage, the broker publishes `offline` on its behalf.

This closes a gap that is easy to miss. A dead sensor and a healthy animal in a stable enclosure produce identical data, which is to say none at all. The last will makes the difference visible.

## Out of scope

The following are deliberately excluded and recorded elsewhere.

- Where inference on this data runs, at the edge or in the cloud. See the AI platform ADRs (020–039).
- Camera-based piranha counting and the animal welfare model. See ADR-043
  and ADR-046.
- Behaviour when a gateway or the uplink is unavailable. See ADR-044.
- Visitor and footfall analytics beyond the topic namespace reserved above.

## Consequences

### Positive

One naming convention serves every consumer. Visitor footfall arrives on the same backbone as enclosure telemetry, with no separate integration to build or maintain.

Wildcards scale past 55 enclosures without anyone enumerating them, so growth in the collection is an operational change rather than a software one.

Bandwidth is spent where loss cannot be undone. On a patchy uplink, the guaranteed traffic is a small fraction of the total volume, which leaves headroom for it.

Dead sensors become detectable. Retained status combined with the last will separates "nothing to report" from "nothing is reporting".

Message volume stays modest. Fifty-five enclosures with a handful of measures each, mostly at 1 to 15 minute intervals, produces a few thousand messages an hour. That sits comfortably inside what MQTT was built for and inside what the funded hardware can carry.

### Negative

Stable identifiers depend on discipline. Never reusing an enclosure ID is an operational rule that a small staff has to remember, with nothing in the system enforcing it. A reused identifier corrupts history quietly, and the corruption is hard to spot afterwards.

QoS 1 delivers duplicates. Every consumer of an event stream has to tolerate seeing the same feeding event twice. That is real work downstream, not something we get for free.

We accept losing individual samples. Through a long outage, a QoS 0 stream has genuine holes in it. Any analysis built on this data has to cope with gaps rather than assume even sampling.

The sensor count grows. Adding dissolved oxygen, containment and lamp state raises the per-enclosure hardware cost and the number of devices somebody has to maintain, measured against a funded baseline ([C3](../requirements.md#constraints), [C14](../requirements.md#constraints)) that nobody has itemised yet.

The intervals above are estimates. They come from general practice rather than from husbandry requirements for the specific species held here, and a keeper should review them before anyone treats them as settled.

### Assumptions

Dissolved oxygen, containment and lamp state sensors are available as MQTT-capable devices, or can be attached to one, and therefore sit inside the funded baseline ([C3](../requirements.md#constraints), [C14](../requirements.md#constraints)).

Safe ranges for each measure come from keepers with species knowledge, not from this team.

---

<p align="center">❦</p>

<p align="right"><a href="#042-telemetry-model-topic-taxonomy-and-delivery-guarantees">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="README.md">All ADRs</a> · <a href="../diagrams/README.md">All diagrams</a></p>
