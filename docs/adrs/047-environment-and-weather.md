# 047. Recording conditions so the data is worth learning from

## Status

Proposed

## Context

- Animal care is costly and much more so when animals get sick ([P3](../requirements.md#problems))
- Nothing currently records whether an animal ate ([P9](../requirements.md#problems)), and the brief asks for it ([R6](../requirements.md#requirements))
- The brief asks for AI to be used and its results validated ([R12](../requirements.md#requirements), [R13](../requirements.md#requirements))
- No in-house ML team ([C13](../requirements.md#constraints))

Seat C does not build the models. It produces the data they would be trained on. That makes
collection a decision rather than a detail, because data not recorded now cannot be recovered
later.

## Decision

Record conditions, interventions and outcomes as one structured set, on one clock, kept the
same way over time.

| Stream | Source |
|---|---|
| Weather on the estate | On-site station: temperature, humidity, rainfall, wind, light |
| Weather forecast | External service, pulled when the uplink is up |
| Enclosure conditions | Per-archetype sensors, [ADR-042](042-telemetry-model.md) |
| Equipment state | Misters, lamps, coolers, pumps, each reporting its own on/off |
| Feeding | Feed dispensed and feed remaining, by weight |
| Behaviour | Camera-derived counts and activity, keeper observations |
| Visitors | Counts by area, [ADR-045](045-presence-and-flow.md) |

**Equipment reports state, not commands.** Commanded on and actually on are different facts.
Only one is evidence. Without it, a record showing temperature falling after a mister ran
teaches a model that enclosures cool themselves. Equipment sits on wifi or cable ([ADR-041](041-hybrid-transport.md)).

**Every reading carries species, enclosure and archetype**, so cohorts can be formed without a
separate spreadsheet.

### Where the first numbers come from

| Source | Trust |
|---|---|
| Estate's own history: keeper notebooks, vet records, feeding logs | Best available if it exists. The collection was private for a long time, so it may be paper or partial |
| Published husbandry and veterinary guidance per species | Sound, but describes the species, not this animal in this enclosure |
| Our own observations from day one | Correct by definition, and useless until there is enough |

Start from published ranges, narrow with any estate history, replace with observation as it
accumulates. **Every threshold records which of the three it came from**, extending the
versioning [ADR-043](043-welfare-loop.md) already requires.

When observation disagrees with the published range, that is raised for a vet rather than
resolved automatically. The animal may be acclimatised, the range may be conservative, the
sensor may be wrong, or the enclosure may be harming it.

### Old paper may be read by a model, the present may not

[ADR-046](046-count-reconciliation.md) refuses to read a keeper's handwriting with a vision model. This record allows it for
historical notebooks. The distinction:

- **A count is a control signal.** Something acts on it, and a misread digit is
  indistinguishable from a missing animal
- **History is not.** Nothing acts on it, a vet approves any range derived from it, and a
  transcription error shows up as an outlier

Transcribed history is marked as transcribed and never used as ground truth to check another
model.

### Cohort baselines

The system knows nothing about an individual on day one, which normally makes this kind of
monitoring useless for a year. With 200+ animals across 55 enclosures ([C5](../requirements.md#constraints)), an individual's
expected range starts as its cohort's — same species, archetype and season — and diverges as
its own history accumulates.

### What this makes answerable later

- Which conditions precede a species going off its food
- Whether an individual differs from its species, and how long that takes to establish
- Whether certain animals eat less on busy days, and whether feeding should move
- Which enclosures will struggle first in forecast heat, and whether misting capacity covers
  them at once
- Whether an unusual behaviour means the animal is unwell or the equipment has failed

We are not building these. We are making them possible, and naming them so the collection is
shaped by what will be asked of it.

### Acting on a forecast

Anything derived from a forecast is a suggestion to a person. A forecast is an external model
whose workings we cannot inspect, and [ADR-043](043-welfare-loop.md)'s rule applies: only fixed limits written by a
vet may switch equipment on by themselves. What the forecast buys is warning time.

## Consequences

| Decision | Cost |
|---|---|
| Weather station on site | A device to buy and maintain, when a forecast API looked adequate |
| Equipment reports its own state | A sensor on every fitting, roughly doubling them per enclosure |
| Keep raw readings indefinitely | Storage grows and most will never be read |
| Forecast recorded as a stream | Storing an external prediction that nobody is yet scoring |
| Published ranges as the starting point | Early months governed by numbers written about animals elsewhere |
| Cohort before individual baselines | Unusual individuals flagged wrongly until we learn they are unusual |
| A model may transcribe historical paper | Transcription errors enter the record, marked, never used to check another model |

## Assumptions

- A weather station can be sited somewhere representative. The brief does not describe the
  layout
- Species-level husbandry guidance is obtainable for the collection

## Open questions

- Retention period for raw readings. We say indefinitely; somebody should cost that
- Whether one weather station is representative of a large, sprawling estate
- Whether keeper observations are structured or free text. Free text is easier to collect and
  far harder to learn from. Needs a keeper in the room
- Whether any estate history exists at all. The brief does not say. We plan as though none
  does, so finding some is upside rather than a dependency

## Related

- **[ADR-041](041-hybrid-transport.md)** carries these streams: conditions on LoRaWAN, equipment on wifi
- **[ADR-042](042-telemetry-model.md)** defines the topic tree
- **[ADR-043](043-welfare-loop.md)** decides what may act; anything forecast-derived goes to a person
- **[ADR-045](045-presence-and-flow.md)** supplies the visitor counts
- **[ADR-046](046-count-reconciliation.md)** uses the same recording rules for the piranha count
