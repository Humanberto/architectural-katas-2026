# 041. Hybrid transport: LoRaWAN for sensors, wifi for everything else

## Status

Proposed. Amends the first two tiers of [ADR-040](040-connectivity-topology.md).

## Context

- Wifi coverage across the park is patchy ([C1](../requirements.md#constraints))
- [ADR-040](040-connectivity-topology.md) answered that by distributing satellite brokers so every sensor had one in range
- 55 enclosures ([C5](../requirements.md#constraints)), restricted and hazardous access to some ([C10](../requirements.md#constraints))
- Budget covers MQTT-capable devices ([C3](../requirements.md#constraints)); the brief is silent beyond that ([C14](../requirements.md#constraints))

LoRaWAN carries small messages over long distances at low power. An enclosure reading fits
comfortably. Changing the radio moves the coverage requirement: instead of 55 enclosures
needing network, only the gateways do, and gateways can sit where power and backhaul already
exist.

LoRaWAN and MQTT are not alternatives. LoRaWAN is the radio link to the sensor; MQTT is the
application protocol from the gateway onward. Commercial gateways generally publish straight
to MQTT.

## Decision

Sensors report over LoRaWAN. Cameras and controlled equipment use wifi or cable. Both deliver
MQTT to one machine on the estate running the broker, the LoRaWAN network server and the
estate server.

| Traffic | Transport | Why |
|---|---|---|
| Readings, containment state, feed weights, visitor counts | LoRaWAN | Small, frequent, from places wifi does not reach |
| Camera results and image files | Wifi | A LoRaWAN message cannot carry an image |
| Commands to misters, lamps, coolers, pumps | Wifi or cable | LoRaWAN cannot deliver a command promptly |
| All of the above, once received | MQTT | One topic tree, one set of delivery rules ([ADR-042](042-telemetry-model.md)) |
| Batched uploads to cloud | Estate uplink | Only when available, never on the alert path |

**Cameras publish results, not images.** Counting happens locally; the camera publishes a
count, a confidence and a model version. Image files stay on the estate and upload over HTTP
only when a count is disputed or confidence is low. MQTT is a message bus, and a queue of
large files would consume broker memory. This follows [ADR-040](040-connectivity-topology.md)'s rule: anything with a
consequence in minutes runs on the estate.

**Commands do not use LoRaWAN.** A standard device listens for a reply only in two short
windows just after transmitting. Adequate for configuration, inadequate for operating
equipment in response to a reading. An enclosure that cannot be given a wifi or cable
connection gets alerts instead of automatic remediation. What may act at all stays in [ADR-043](043-welfare-loop.md).

**Network server runs on the estate.** It handles joins, keys and decoding. Run as a cloud
service, sensor data would be unreadable whenever the uplink was down, conflicting with [R15](../requirements.md#requirements).
On-estate costs the single IT staff member ([C13](../requirements.md#constraints)) another component to maintain.

**Gateway count.** The brief gives no dimensions, so we propose no number. A gateway covers
several kilometres in the open and under one kilometre among buildings and vegetation; an
estate with 40 rides and 55 enclosures likely falls inside one. Planning assumption is two, so
one failure does not stop all sensor traffic. Final count needs a site survey. Capacity is not
the constraint: several hundred sensors at quarter-hourly intervals is well within one
gateway's throughput.

## Consequences

| Decision | Cost |
|---|---|
| LoRaWAN for the sensor link | A second radio technology, with its own gateways, key management and operational knowledge |
| One machine for broker, network server and estate server | All sensor traffic depends on it; an outage stops reception until it is replaced |
| Cameras publish results, not images | Footage not retained cannot be reviewed, so a disputed count is only answerable if the file was kept |
| Wifi retained for cameras and equipment | Wifi coverage is still required wherever either is installed |
| A planning assumption, not a fixed count | The design is incomplete until a survey is done |

**On the single point of failure.** [ADR-040](040-connectivity-topology.md) named the central broker as its largest open risk,
and consolidating increases that exposure. Two things reduce it: one machine can be kept as a
spare and replaced by one person, where four distributed devices are four maintenance
obligations; and LoRaWAN sensors buffer their own readings, so an outage of hours delays the
record rather than losing it.

**On budget.** LoRaWAN sensors and gateways are outside [C3](../requirements.md#constraints) and need the [C14](../requirements.md#constraints) argument. The case
is substitution, not addition: two gateways instead of four satellite brokers, and battery
sensors instead of devices needing mains power or frequent visits to restricted enclosures
([C10](../requirements.md#constraints)). The brief contains no figures to prove it, so this is an assumption.

## Alternatives rejected

| Option | Why not |
|---|---|
| Keep the tiered topology unchanged | Uses hardware to solve a coverage problem the radio addresses directly, and four outdoor devices are four maintenance obligations for one IT person ([C13](../requirements.md#constraints)) |
| Full wifi coverage | Cost, plus limited scope for physical modification of historically important rides and buildings ([C7](../requirements.md#constraints)). Mains power at every enclosure cannot be assumed |
| Cellular or NB-IoT per sensor | Recurring per-device cost to an unprofitable estate ([P1](../requirements.md#problems)), and welfare alarms dependent on an external carrier |

## Open questions

- Gateway siting and final count, pending a survey
- Message budget. A LoRaWAN device transmits for only a small proportion of each hour, and
  [ADR-042](042-telemetry-model.md)'s intervals need checking against that
- Whether containment sensors should use LoRaWAN at all. They are the only stream measured in
  seconds, and cable may suit the small number of doors better

## Related

- **[ADR-040](040-connectivity-topology.md)** established what runs on the estate and what runs in the cloud. Unchanged
- **[ADR-042](042-telemetry-model.md)** topic structure and delivery guarantees for both transports
- **[ADR-043](043-welfare-loop.md)** what may act automatically, dependent on the command path above
- **[ADR-046](046-count-reconciliation.md)** depends on camera results rather than images
- **[ADR-047](047-environment-and-weather.md)** adds weather and equipment streams on the same transports
