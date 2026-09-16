# 046. Checking the animal count against the keepers' ledger

**Go straight to:** [Home](../../README.md) · [ADRs](README.md) · [Diagrams](../diagrams/README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

## Status

Proposed

## Context

- Piranha population levels are unknown and the animals jump, so counts drift ([P6](../requirements.md#problems))
- The brief asks for population levels to be checked ([R7](../requirements.md#requirements))
- AI results must be validated, including detecting misbehaviour in production ([R13](../requirements.md#requirements))
- Generative and perceptual AI behaviour is not deterministic ([C12](../requirements.md#constraints))

A camera that counts fish is a model, and models drift. The risk in checking a model is
checking it with another model: if a second model reads the keeper's handwriting, a misread
digit and a missing animal look identical in the data. The check has to come from outside the
system.

## Decision

The keeper's count is the record. The camera's count is an estimate compared against it. When
the two disagree we investigate, and we do not assume which is wrong.

### How it works

- A keeper counts during a round they already do and types the number in. Not a photograph,
  not handwriting recognition. A typed number from a person who was standing there
- The camera publishes its count, its confidence and its model version, not its images
  ([ADR-041](041-hybrid-transport.md))
- The system records both and the difference between them
- Inside tolerance for that enclosure, nothing happens. Outside it, a reconciliation task goes
  to the keeper

### Counting through murky water

We assume underwater visibility in the lagoon is poor, as is usual in a densely stocked
outdoor freshwater pond. The brief does not state this, and if it turns out to be wrong a
submerged camera becomes worth revisiting.

Two things are observable regardless. The piranhas jump, which the brief states, and they feed
at the surface. A camera above the water sees both without needing to see through anything.

That camera undercounts the population by an unknown amount, which is acceptable because it is
never used as the population figure. It is a second opinion, and an undercount that stays
consistent is useful the moment it stops being consistent.

### Counting the jumps

A jump is a surface disturbance, visible to the same camera and audible at the bank. Jump rate
over a feeding window, tracked across weeks, moves with the size and condition of the
population without requiring any individual fish to be seen clearly.

Jump rate is a trend, not a number. It cannot give a population figure. It can say something
changed when the keeper's count has not, which is worth walking down to look at.

It costs almost nothing: the camera is already there for the surface count, and this is the
same footage read a second way.

### Comparing ratios, not raw numbers

The surface count is always a fraction of the real population, so the comparison is the ratio
between the two numbers. Once that ratio settles for an enclosure, a change in it is what
matters.

| Ratio moves | Possible causes | Treated as |
|---|---|---|
| **Falls** | An animal is dead, missing or escaped. Fewer fish surfacing to feed, itself a welfare signal. Or the model is under-counting because the water or the light changed | A welfare concern. Keeper checks physically. If all animals are present, the problem is the model, not the animals |
| **Rises** | Breeding. Or the model is double-counting. Or the ledger is out of date | A data question. Keeper confirms. If there are fry, the ledger is updated and the birth recorded |

A fall may mean something is wrong with an animal. A rise usually means something good
happened or a number needs correcting. They should not arrive with the same urgency.

### Detecting drift

One disagreement is ordinary. Fish move, water is cloudy, keepers miscount.

A disagreement that grows steadily in one direction over weeks is the camera model drifting
away from reality, and it is otherwise invisible, because a model that slowly gets worse never
announces it. So the difference is tracked over time, not just per reading. A widening gap is
the alarm.

### Where the numbers live

The keeper's count is stored as a fact. The camera's count is stored beside it as an
assessment carrying model version and confidence, per
[ADR-042](042-telemetry-model.md). Neither overwrites the other, because the record of them
disagreeing is the useful part.

Counts continue during a cloud outage, since the camera counts on the estate
([ADR-044](044-disconnected-operation.md)). Only the image files wait.

## Consequences

| Decision | Cost |
|---|---|
| A keeper types the count | Ten seconds per round, and the check happens only as often as they do it |
| The keeper's number is the record | We learn the model is wrong only as often as someone counts by hand |
| Investigate in both directions | Breeding triggers investigations that turn out to be good news |
| A camera above the water | An undercount rather than a census, dependent on fish surfacing to feed |
| Jump rate as a second signal | A trend, not a number. It says something changed, never what the population is |

## Alternatives rejected

| Option | Why not |
|---|---|
| Photograph the ledger and read it with a vision model | Checks a model with a model. A misread digit and a missing animal become indistinguishable |
| Trust the camera because it counts far more often | Nothing outside the system would then be checking it ([R13](../requirements.md#requirements)) |
| Acoustic imaging | The only method that genuinely counts fish in water this murky, and far beyond a family estate with no technology staff ([C13](../requirements.md#constraints)) and a budget for MQTT devices ([C3](../requirements.md#constraints), [C14](../requirements.md#constraints)) |

## Assumptions

- Underwater visibility in the lagoon is poor
- A keeper count fits an existing round rather than adding a new task. Worth confirming with a
  keeper

## Open questions

- Tolerance per enclosure. How far the ratio can move before it means anything depends on the
  species, the water and the enclosure. A keeper should set it, and it cannot be set until the
  ratio has been observed long enough to have a normal
- How often keepers count, which decides how quickly drift is detectable
- Whether jump rate correlates with population usefully at all. It is cheap enough to collect
  while finding out

## Related

- **[ADR-041](041-hybrid-transport.md)** the camera publishes counts, not images
- **[ADR-042](042-telemetry-model.md)** how the estimate is stored beside the fact
- **[ADR-043](043-welfare-loop.md)** what happens when a count suggests an animal is unwell
- **[ADR-044](044-disconnected-operation.md)** what happens to counts recorded while cut off
- **[ADR-047](047-environment-and-weather.md)** applies the same recording rules more widely

---

<p align="center">❦</p>

<p align="right"><a href="#046-checking-the-animal-count-against-the-keepers-ledger">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="README.md">All ADRs</a> · <a href="../diagrams/README.md">All diagrams</a></p>
