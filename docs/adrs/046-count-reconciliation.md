# 046. Checking the animal count against the keepers' ledger

## Status

Proposed

## The decision

The keeper's count is the record. The camera's count is an estimate checked against it. When the two disagree we investigate, and we do not assume which one is wrong.

## Why we need to decide this

Nobody knows how many piranhas there are (P6), and they jump, so the number moves on its own. A camera counting them is a model, and models drift (C12). The brief asks us to detect that drift in production (R13).

The problem with checking a model is that it is easy to check it with another model and learn nothing. If a second model reads the keeper's handwriting, a misread digit and a missing animal look the same in the data.

So the check has to come from outside the system.

## How it works

A keeper counts the animals during a round they already do and types the number in. Not a photograph, not handwriting recognition. A typed number from a person who was standing there.

The system compares that number against the camera's count for the same period and records both, along with the difference.

If the difference sits inside the tolerance for that enclosure, nothing happens. If it sits outside, a reconciliation task goes to the keeper.

## Counting through muddy water

The lagoon is turbid. Underwater visibility is a few inches at best, so a submerged camera would return sediment rather than fish. That rules out the obvious approach.

Two things are still observable. The piranhas jump, and they feed at the surface, so a camera mounted above the water sees real activity without having to see through anything.

Acoustic imaging is the only method that genuinely counts fish in water this murky. We are not proposing it. The hardware, the underwater housing, the armoured cabling needed against a species that bites cables, and the expertise to operate it are all far beyond a family estate with one IT person (C13) and a budget for MQTT devices (C3, C14).

So the camera in this record is a surface camera. It counts fish visible at the surface during a feed, which undercounts the population by an unknown amount. That is acceptable, because we never use it as the population figure. We use it as a second opinion to check the keeper's count against, and an undercount that stays consistent is still useful the moment it stops being consistent.

## The two directions mean different things

Because the surface count is always a fraction of the real population, we compare the ratio between the two numbers rather than the raw difference. Once that ratio settles for an enclosure, a change in it is what matters.

| Surface count, against its usual ratio | Possible causes | What happens |
|---|---|---|
| **Falls** | An animal is dead, missing or escaped. Or fewer fish are coming up to feed, which is itself a welfare signal. Or the model is under-counting because the water is murkier than usual or the light is poor | Treated as a welfare concern. Keeper does a physical check. If the animals are all present, we have a model problem, not an animal problem |
| **Rises** | The piranhas have bred and there are fry. Or the model is double-counting. Or the ledger is out of date | Treated as a data question, not an emergency. Keeper confirms. If there are fry, the ledger is updated and the birth is recorded |

The asymmetry matters. A ratio that falls might mean something is wrong with an animal. A ratio that rises usually means something good has happened, or that a number needs correcting. They should not arrive with the same urgency.

## What the pattern tells us

One disagreement is ordinary. Fish move, water is cloudy, keepers miscount.

A disagreement that grows steadily in one direction over weeks is not ordinary. That is the camera model drifting away from reality, and it is exactly the thing that is otherwise invisible, because a model that slowly gets worse never announces it.

So we track the difference over time, not just each reading. A widening gap is the alarm, more than any single mismatch.

## Where the numbers live

The keeper's count is stored as a fact. The camera's count is stored beside it as an assessment, carrying the model version and its confidence, in line with ADR-042.

The camera count never overwrites the keeper's number, and the keeper's number never silently corrects the camera's history. Both stay, because the record of them disagreeing is the useful part.

## What we chose, and what it cost us

| We chose | Instead of | What it costs us |
|---|---|---|
| A keeper types the count | Photographing the ledger and reading it with a vision model | Ten seconds of a keeper's time per round, and the check only happens as often as they do it |
| The keeper's number is the record | Trusting the camera because it counts far more often | We only find out the model is wrong as often as someone counts by hand |
| We investigate in both directions | Only reacting when the count drops | Breeding will trigger investigations that turn out to be good news |
| A camera above the water | Acoustic imaging, the only thing that sees through turbid water | We get an undercount rather than a census, and the signal depends on the fish surfacing to feed |

## What this gives us

- The AI is checked by something that is not AI.
- Drift is detected by a method that costs no extra staff time.
- A missing animal and a mistaken model are separated instead of averaged.
- Breeding gets noticed and recorded rather than dismissed as a counting error.

## Still to settle

- **Tolerance per enclosure.** How far the ratio can move before it means anything depends on the species, the water and the enclosure. A keeper should set it, not us. It also cannot be set until the ratio has been observed for long enough to have a normal.
- **How often keepers count.** We assume this fits an existing round rather than adding a new task. Worth confirming with a keeper before we commit to it.

## Related

- **ADR-042** defines how the camera's estimate is stored beside the fact
- **ADR-043** covers what happens when the count suggests an animal is unwell
- **ADR-044** covers what happens to counts recorded while the estate is cut off
