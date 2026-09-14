# 041. Two radios, one protocol

## Status

Proposed. Amends the first two tiers of ADR-040.

## The decision

Sensors reach the estate over LoRaWAN, a radio built to carry very little data a very long
way. Cameras and anything the system switches on stay on wifi. Both paths arrive as MQTT
messages at a single box on the estate that is the broker, the LoRaWAN network server and
the estate server together.

## Why we are changing part of 040

ADR-040 scattered small brokers around the park so that every sensor had one in radio range.
That solved patchy wifi (C1) by spending hardware. The radio solves it better.

LoRaWAN trades bandwidth for range. A few dozen bytes, several kilometres, through walls,
on a battery that lasts years. An enclosure reading is a few dozen bytes, so the trade is
exactly the one we want.

The important consequence is not the radio. It is that **the coverage problem moves**. Before,
55 enclosures each needed to reach a network. Now only the gateways do, and gateways can be
sited where power and backhaul already exist. Two hard places instead of fifty-five.

## What runs on what

| Carries | Over | Why |
|---|---|---|
| Enclosure readings, containment state, feed weights, footfall counts | LoRaWAN | Tiny, frequent, and coming from places wifi does not reach |
| Camera results and clips | Estate wifi | A LoRaWAN message cannot hold an image |
| Commands to misters, lamps, pumps, coolers | Estate wifi or wired | LoRaWAN cannot take a command promptly. See below |
| Everything, once it has landed | MQTT on the estate | One topic tree, one set of delivery rules, per ADR-042 |
| Batched uploads to the cloud | The estate's single uplink | When it is up. Never on the alert path |

LoRaWAN and MQTT are not alternatives. LoRaWAN is the last hop to a sensor; MQTT is
everything from the gateway inward. The gateway is the bridge, and most commercial gateways
publish straight onto MQTT.

## The camera does not send video

A clip is megabytes. A count is forty bytes.

So the camera does the counting where it is, or on the estate server, and publishes the
result: a number, a confidence, a model version. The clip stays on the estate. It is uploaded
only when a keeper disputes a count or the model flags itself as uncertain, and then over
HTTP rather than through the broker, because a message bus is not a media pipe and a backlog
of queued clips would sit in broker memory.

When the uplink is down, results still reach the keeper. Clips wait. Neither is urgent.

This is the same rule ADR-040 already set: if failure to act within minutes has a
consequence, it happens on the estate.

## Commands do not travel on LoRaWAN

An ordinary LoRaWAN device listens for a reply only in two short windows just after it
transmits. That is fine for "your settings changed, apply them next time". It is not fine
for "turn the backup pump on now".

So anything the system may switch on is reached over wifi or a wired run. That makes it a
siting requirement: an enclosure with controllable equipment in it needs that connection, and
an enclosure that cannot have one gets alerts rather than automatic remediation. The
authority question — what may act at all — stays in ADR-043.

## How many gateways

We do not know, and the brief gives no dimensions, so we will not invent a number.

What we can say: a gateway covers kilometres in the open and something under one kilometre
among buildings and trees. An estate with 40 rides, 55 enclosures, a lagoon and a house is
a large park, not a region. One gateway probably covers it.

**Planning assumption: two.** The second is not for range. It is for the lagoon sitting low
behind its bank, the stone menagerie, and the Venom House walls, and it means one failed
gateway does not leave the estate deaf. Final count is a site survey output, sited for power
and backhaul rather than for radio.

Capacity is not the constraint. A few hundred sensors reporting every fifteen minutes is
well inside what one gateway handles. Geometry is the constraint, and geometry cannot be
settled from a map.

## The network server lives on the estate

LoRaWAN needs a network server to handle joins, keys and decoding. Run as a cloud service,
which is the common way, sensor data would stop being readable the moment the uplink dropped.
That would break the one thing this architecture exists to protect (R15).

So it runs on the estate box, beside the broker. One more thing for one IT person (C13) to
look after, and the price of staying operable when the estate is cut off.

## What we chose, and what it cost us

| We chose | Instead of | What it costs us |
|---|---|---|
| LoRaWAN for the sensor hop | Wifi sensors reaching scattered satellite brokers | A second radio on the estate, with its own gateways, keys and vocabulary |
| One box: broker, network server, estate server | Distributed brokers per zone | Every reading depends on one machine. It fails and the estate is deaf until someone swaps it |
| Cameras publish results, not frames | Streaming video to the estate or the cloud | We cannot look back at footage we never kept, so a disputed count is only answerable if the clip was retained locally |
| Wifi kept for cameras and equipment | LoRaWAN everywhere | Wifi does not go away. It still has to reach the lagoon camera and every enclosure with a mister in it |
| A planning assumption rather than a number | A confident gateway count | The design is not finished until someone walks the estate with a signal meter |

## The single point of failure

ADR-040 named the central broker as its largest open risk. Collapsing to one box makes that
sharper, and we would rather say so than bury it.

Two things make it tolerable. One machine is something a single IT person can keep a spare
for, and swapping a spare in is a job they can actually do; four boxes in hedges are four
things to find and four things to forget. And LoRaWAN sensors buffer their own readings, so
an outage of minutes to hours is a delay in the record rather than a hole in it.

If there were budget for one piece of redundancy on this estate, it is a second estate box.

## Budget

The brief funds MQTT-capable devices throughout the park (C3) and is silent beyond that (C14).
LoRaWAN sensors and gateways are a different bill of materials, so this needs arguing.

The case is that it is a swap rather than an addition: two gateways instead of four satellite
brokers, and battery sensors instead of devices needing mains power or frequent visits into
restricted enclosures (C10). We believe that is cheaper to buy and considerably cheaper to
run. We cannot prove it from the brief and we are flagging it as an assumption.

## Alternatives we rejected

**Keep the tiered topology unchanged.** It works and it was already written. Rejected because
it spends hardware to solve a problem the radio solves better, and four outdoor devices on an
estate with one IT person are four quiet failures waiting to happen.

**Wifi everywhere, properly.** Blanket the park in access points. Rejected on cost and on the
fabric: the rides and buildings are historically important and physical modification is
limited (C7), and mains power at every enclosure is not a given.

**Cellular or NB-IoT per sensor.** No estate infrastructure at all. Rejected because it puts
a recurring per-device bill on an estate that cannot pay its own way (P1), and makes animal
welfare alarms depend on an outside carrier.

## Still to settle

- **Gateway siting.** A survey, not a map exercise.
- **Message budget.** A LoRaWAN device may only transmit for a small fraction of each hour.
  The intervals in ADR-042 need checking against that before we commit to them.
- **Whether containment sensors belong on LoRaWAN at all.** They are the one stream where
  seconds matter. A wired run may be the honest answer, and it is a small number of doors.

## Related

- **ADR-040** established what runs on the estate and what runs in the cloud. Unchanged.
- **ADR-042** defines the topic tree and delivery guarantees, now fed by two transports.
- **ADR-043** defines what may act automatically, and is affected by the command path above.
- **ADR-046** depends on camera results rather than camera frames.
- **ADR-047** adds the weather and equipment streams that ride the same transports.
