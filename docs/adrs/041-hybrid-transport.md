# 041. Two radios, one protocol

## Status

Proposed. Amends the first two tiers of ADR-040.

## Context

ADR-040 placed satellite brokers around the park so that every sensor had one within radio
range. This addressed patchy wifi coverage (C1) by distributing hardware.

A better option is to change the radio the sensors use. LoRaWAN carries small messages over
long distances at low power, typically a few hundred bytes per message and several kilometres
of range. An enclosure reading is well within that limit.

The significant effect is that the coverage requirement moves. Under ADR-040, all 55
enclosures (C5) needed network coverage. Under this decision, only the gateways do, and
gateways can be placed where power and a network connection already exist.

LoRaWAN and MQTT operate at different layers and are not alternatives. LoRaWAN is the radio
link to the sensor. MQTT is the application protocol from the gateway onward. Commercial
LoRaWAN gateways generally publish directly to MQTT.

## Decision

Sensors report over LoRaWAN. Cameras and any equipment the system controls use estate wifi or
a wired connection. Both paths deliver MQTT messages to a single machine on the estate that
runs the broker, the LoRaWAN network server and the estate server.

| Traffic | Transport | Reason |
|---|---|---|
| Enclosure readings, containment state, feed weights, visitor counts | LoRaWAN | Small, frequent, and originating where wifi is unreliable |
| Camera results and image files | Estate wifi | A LoRaWAN message cannot carry an image |
| Commands to misters, lamps, coolers and pumps | Estate wifi or wired | LoRaWAN cannot deliver a command promptly |
| All of the above, once received | MQTT | One topic tree and one set of delivery rules, per ADR-042 |
| Batched uploads to the cloud | The estate uplink | Only when available, and never on the alert path |

### Cameras publish results rather than images

A camera performs its counting locally or on the estate server and publishes the result: a
count, a confidence value and a model version. Image files remain on the estate and are
uploaded only when a keeper disputes a count or the model reports low confidence. Those
uploads use HTTP rather than the broker, because MQTT is a message bus and a queue of large
files would consume broker memory.

This follows the rule already set in ADR-040: anything with a consequence in minutes runs on
the estate.

### Commands do not use LoRaWAN

A standard LoRaWAN device listens for a reply only in two short windows immediately after it
transmits. This is adequate for configuration changes and inadequate for operating equipment
in response to a reading.

Equipment the system may switch on is therefore connected by wifi or cable. An enclosure that
cannot be given that connection receives alerts instead of automatic remediation. The question
of what may act at all remains with ADR-043.

### Number of gateways

The brief gives no estate dimensions, so we are not proposing a number. A LoRaWAN gateway
typically covers several kilometres in open ground and under one kilometre where buildings and
vegetation obstruct the signal. An estate with 40 rides and 55 enclosures is likely to fall
within the range of a single gateway.

Our planning assumption is two gateways, positioned for power and backhaul rather than for
coverage alone, so that the failure of one does not stop all sensor traffic. The final number
requires a site survey.

Capacity is not a limiting factor. Several hundred sensors reporting at quarter-hourly
intervals is well within the throughput of one gateway.

### The network server runs on the estate

LoRaWAN requires a network server to manage device joins, keys and message decoding. It is
commonly run as a cloud service. That arrangement would make sensor data unreadable whenever
the uplink was down, which conflicts with R15.

It therefore runs on the estate machine alongside the broker. This adds a component for the
single IT staff member (C13) to maintain.

## Consequences

| Decision | Alternative | Cost |
|---|---|---|
| LoRaWAN for the sensor link | Wifi sensors reporting to distributed satellite brokers | A second radio technology on the estate, with its own gateways, key management and operational knowledge |
| One machine running broker, network server and estate server | Distributed brokers by zone | All sensor traffic depends on one machine, and an outage stops reception until it is replaced |
| Cameras publish results, not images | Streaming video to the estate or the cloud | Footage that was not retained cannot be reviewed, so a disputed count is only answerable if the file was kept |
| Wifi retained for cameras and equipment | LoRaWAN throughout | Wifi coverage remains a requirement wherever a camera or controllable equipment is installed |
| A planning assumption rather than a fixed count | A stated number of gateways | The design is incomplete until a survey is carried out |

### The single point of failure

ADR-040 identified the central broker as its largest open risk. Consolidating to one machine
increases that exposure.

Two factors reduce it. A single machine can be kept as a spare and replaced by one person,
whereas four distributed devices are four separate maintenance obligations. LoRaWAN sensors
also buffer their own readings, so an outage of hours delays the record rather than losing it.

If budget existed for one piece of redundancy, a second estate machine would be the
appropriate choice.

### Budget

The brief funds MQTT-capable devices throughout the park (C3) and is silent on anything beyond
that (C14). LoRaWAN sensors and gateways are a different specification and require
justification.

The argument is that this is a substitution rather than an addition: two gateways in place of
four satellite brokers, and battery-powered sensors in place of devices requiring mains power
or frequent visits to restricted enclosures (C10). We expect this to cost less to install and
significantly less to operate. The brief does not contain the figures to prove it, so this
remains an assumption.

## Alternatives considered

**Retain the tiered topology unchanged.** It is workable and already documented. Rejected
because it uses hardware to solve a coverage problem that the radio addresses more directly,
and because four outdoor devices represent four maintenance obligations for one IT staff
member (C13).

**Full wifi coverage.** Install sufficient access points to cover the park. Rejected on cost
and on the constraint that the rides and buildings are historically important with limited
scope for physical modification (C7). Mains power at every enclosure also cannot be assumed.

**Cellular or NB-IoT for each sensor.** This removes the need for estate infrastructure
entirely. Rejected because it introduces a recurring per-device cost to an estate that is
currently unprofitable (P1), and makes welfare alarms dependent on an external carrier.

## Open questions

- Gateway siting and final count, which require a site survey.
- Message budget. A LoRaWAN device may transmit for only a small proportion of each hour, and
  the intervals in ADR-042 need to be checked against that limit.
- Whether containment sensors should use LoRaWAN at all. They are the only stream where
  response time is measured in seconds, and a wired connection may be more appropriate for the
  small number of doors involved.

## Related

- **ADR-040** established what runs on the estate and what runs in the cloud. Unchanged.
- **ADR-042** defines the topic structure and delivery guarantees for both transports.
- **ADR-043** defines what may act automatically, and depends on the command path above.
- **ADR-046** depends on camera results rather than camera images.
- **ADR-047** adds weather and equipment streams using the same transports.
