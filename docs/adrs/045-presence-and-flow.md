# 045. Counting visitors without being able to identify them

**Go straight to:** [Home](../../README.md) · [ADRs](README.md) · [Diagrams](../diagrams/README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

## Status

Proposed. Baseline settled. The card section at the end is not yet agreed.

## Context

- No idea which parts of the estate are popular, so investment and staffing are guesswork ([P2](../requirements.md#problems))
- Must measure area popularity ([R3](../requirements.md#requirements)) and act on it ([R4](../requirements.md#requirements))
- 5,000 visitors a day now, 15,000 expected within three years ([C8](../requirements.md#constraints))
- Ticket and family pass purchase is the only transaction in the brief ([R1](../requirements.md#requirements)). No food or retail
- The animal collection was private and is opening to the public ([P7](../requirements.md#problems)). We infer from this that
  there is no existing visitor data practice to build on

The usual methods are cameras with people detection and wifi or Bluetooth device counting.
Both produce a record of where an individual went.

## Decision

Count with equipment that cannot identify anyone. Calibrate it against ticket validation.
Treat movement between areas as an inference and label it as one.

| What we measure | How | Certainty | Tier ([ADR-011](011-ai-determinism-tiers.md)) |
|---|---|---|---|
| Daily entries | Ticket validation, [ADR-012](012-admissions-and-ticketing.md) | Fact | 1 |
| People passing a point | Beam-break, thermal or time-of-flight counters | Error margin set on site | 1 |
| Route and dwell | Inferred from counter readings | Inference | 2 |

**Why the hardware matters.** These counters record no image, no device address, nothing
linkable to a person. This is a property of the equipment, not a policy that has to be
followed correctly. Asked later for records of individual movement, the estate has none.

Counters send a few bytes and run on battery, so they use LoRaWAN ([ADR-041](041-hybrid-transport.md)).

**Calibration.** Counters undercount groups walking abreast, and family passes mean groups are
expected. Daily gate entries against daily counter totals gives a correction factor per
counter. Same pattern as [ADR-046](046-count-reconciliation.md): frequent cheap estimate, corrected by a scarcer reliable
figure.

**Validation is thin.** The gate total is the only independent check, and it is one figure a
day. It catches gross errors in the movement inference, not subtle ones.

**Crowds are animal welfare data.** Recording visitor counts by area on the same clock as
feeding and enclosure conditions ([ADR-047](047-environment-and-weather.md)) makes it possible to test later whether species
feed differently on busy days. We are not claiming they do.

## Consequences

| Decision | Cost |
|---|---|
| Equipment that cannot identify | No question needing the same visitor twice, including returning visitors ([R10](../requirements.md#requirements)) |
| Counting at pinch points | Describes paths, not where people linger off them |
| Movement labelled as inference | The most presentable output carries a caveat |
| Daily calibration | Corrects a daily total, not an unusual hour |
| One independent check | Thinner than [ADR-046](046-count-reconciliation.md), which has a keeper's count as a second source |

## Alternatives rejected

| Option | Why not |
|---|---|
| Wifi / Bluetooth device counting | Counts devices carried by people. Also degraded by address randomisation, in ways that are hard to detect |
| Cameras with people counting | Puts a camera on every visitor. Cameras stay at enclosures ([ADR-046](046-count-reconciliation.md)) and that boundary is part of the decision |
| Visitor mobile app | Needs a smartphone and a download, depends on patchy wifi ([C1](../requirements.md#constraints)), and holds worse data than anything above |

## Assumptions

- Visitors move mainly along paths, so pinch points exist. The brief does not describe the
  layout
- Ticket validation records a timestamp, or can be configured to

## Open questions

- Pinch point locations and count. Needs a busy day observed
- Whether dwell time is measurable without following individuals
- Whether the Countess wants comparison over time or a live view. The brief implies the former
- [R10](../requirements.md#requirements) belongs to the retention seat, and this record makes it harder, not easier

---

## Optional addition: visitor cards

**Not agreed. If rejected, delete to the next rule. Nothing above depends on it.**

Every visitor gets a card on entry. Readers at attraction entrances register it as they pass.

**What it adds that counters cannot.** Counters say how many passed. Cards say which
attractions a visit included, in what order, for how long, and which cards moved together as a
group. That separates a quiet area visitors walked past, which is a signposting problem, from
one they never approached, which is a routing problem. Different fixes.

**Keeping it consistent with the decision above.** A unique card number is an identifier, and
linking it to a ticket purchase would link a movement record to a name. So it is never linked:
cards are issued from a pool in no recorded order, returned at the exit, reissued later to
someone else. The result is a path with nothing attached to it. This does not recover [R10](../requirements.md#requirements) —
a card recognises nothing about a person, including that they have been before.

**Technology.** Passive cards read at short range by fixed readers. Not LoRaWAN: thousands of
cards reporting through the day would exceed the airtime and gateway limits [ADR-041](041-hybrid-transport.md) depends
on. Readers have power, so they use wifi or cable and publish to MQTT. Read events are
discrete, so the record is a list of visits rather than a position stream.

| Decision | Cost |
|---|---|
| Cards unlinked from tickets | No question needing to know which visitor, including lost property and complaints |
| Cards for everyone on entry | Handing out and collecting at 5,000 rising to 15,000 a day. Operational, not technical |
| Readers at entrances | Which attractions a visit included, not the route between them |
| Additional hardware | Well outside the MQTT budget ([C3](../requirements.md#constraints)), so needs the [C14](../requirements.md#constraints) argument |

Some visitors will lose or discard a card, so some visits are invisible. That is an inference,
not a measured figure, and it is why the counters stay in place either way.

**If outlets are introduced.** The brief has none and recommending them is outside this seat.
If they appear, transactions by location and time become a further signal and a second
independent check, consumable with no structural change: same topic tree ([ADR-042](042-telemetry-model.md)), same clock
([ADR-047](047-environment-and-weather.md)).

---

## Related

- **[ADR-011](011-ai-determinism-tiers.md)** tiers used here
- **[ADR-012](012-admissions-and-ticketing.md)** ticket validation, used for calibration
- **[ADR-041](041-hybrid-transport.md)** carries the counters, and explains why cards would not use LoRaWAN
- **[ADR-046](046-count-reconciliation.md)** same estimate-and-correct pattern, applied to animals
- **[ADR-047](047-environment-and-weather.md)** records visitor counts alongside weather and feeding

---

<p align="center">❦</p>

<p align="right"><a href="#045-counting-visitors-without-being-able-to-identify-them">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="README.md">All ADRs</a> · <a href="../diagrams/README.md">All diagrams</a></p>
