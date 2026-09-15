# 043. Watching animal health, and what the system may do on its own

## Status

Proposed

## Context

- Animal care is costly and much more so when animals get sick ([P3](../requirements.md#problems))
- Nothing currently records whether an animal ate ([P9](../requirements.md#problems))
- Piranha population levels are unknown ([P6](../requirements.md#problems))
- Generative and perceptual AI behaviour is not deterministic ([C12](../requirements.md#constraints))
- No in-house ML team ([C13](../requirements.md#constraints)), so nobody on site could diagnose a model making bad calls at three in the morning

[ADR-042](042-telemetry-model.md) covers the readings coming out of the enclosures. This
record covers what may be done with them.

## Decision

Fixed rules written by a vet may switch equipment on by themselves. Anything a model works out
may only be a suggestion to a person.

|  | May switch equipment on | May raise an alert and explain it |
|---|---|---|
| A fixed limit set by a vet | Yes | Yes |
| Anything a model infers | **No** | Yes |

This holds even where the model is better at spotting problems than the fixed limit. If a pump
runs because oxygen fell below a number a vet wrote down, that can be explained to anyone
afterwards, exactly. If it runs because a model decided something, explaining it needs someone
who understands the model, and the estate does not employ that person ([C13](../requirements.md#constraints)).

The model's job is to spot trouble earlier than a fixed limit would, and to notice patterns a
person would take longer to see. It tells a person. The person acts.

### How the instruction reaches the equipment

Sensors report over LoRaWAN, which is built for sending small readings out rather than
receiving commands promptly ([ADR-041](041-hybrid-transport.md)). Misters, lamps, coolers and
pumps are therefore reached over wifi or cable.

An enclosure that cannot be given that connection receives alerts instead of automatic
remediation. This is a siting decision rather than a software one.

### The vet decides what unwell means

A vet supplies the safe range per species, the point at which to worry, and what to do about
it. Settings are versioned, so it is always possible to say which were in use when an alert
fired.

Each setting also records where its number came from: published guidance for the species, the
estate's own historical records, or a vet's judgement about this animal in this enclosure
([ADR-047](047-environment-and-weather.md)). Those are different kinds of fact, and a keeper
deciding whether to act at three in the morning should know which they are looking at.

The system never invents its own definition of a sick animal.

### Starting before we know the animal

On the first day nothing is known about any individual, which normally makes this kind of
monitoring useless for a year.

With 200+ animals across 55 enclosures ([C5](../requirements.md#constraints)), an individual's
expected range starts as its cohort's, meaning same species, same enclosure archetype, same
season, and diverges as its own history accumulates
([ADR-047](047-environment-and-weather.md)). A new arrival is useful immediately.

### Three kinds of problem

| Kind | Example | Automatic action | Who hears, and when |
|---|---|---|---|
| **People in danger** | A door opens on a venomous enclosure | No. Alarm only | Security and the keeper on duty, immediately, using equipment on the estate |
| **Animal in danger now** | Oxygen in the lagoon falls below the vet's limit | Yes. The backup pump starts | The keeper on duty, immediately, then updates until the reading recovers |
| **Animal may be unwell** | A fish has not fed for three days | No | Added to the keeper's list for that day |

A door is open or it is not, so nothing interprets it and no model is involved in the first
row. The third develops over days, leaving time for a person to walk over and look.

For the first two rows someone must confirm they have seen the alert. If nobody confirms within
a set time it escalates to the next person. An unconfirmed alert is treated as unseen.

### The animals are sensors too

A fish that stops coming up to feed may be reporting on the water before the oxygen probe has
drifted far enough to notice. A lizard that stops basking may be reporting a failed lamp.

So an unusual behaviour raises one question with two branches: is the animal unwell, or is the
enclosure wrong? Because equipment reports its own state
([ADR-047](047-environment-and-weather.md)), that can often be answered from the record before
anyone walks out there. It costs nothing extra, being the same observation read a second way.

### Fish are different from lizards

In a land enclosure an alert concerns one animal a keeper can go and look at. In the lagoon
that is not realistic, so an alert says feeding looks wrong across the group and asks a keeper
to watch the next feed.

Individual fish are still tracked, because it surfaces problems sooner than averages would, but
what a keeper receives is information rather than an instruction to catch a particular fish.
Recognising the same individual week after week may become possible later. Nothing here depends
on it.

### Knowing when we get it wrong

A keeper closes each alert with one of three answers: there was a problem, there was not, or
unclear. That answer is stored beside the readings that caused the alert and the settings in
force at the time.

| Pattern | Usual meaning |
|---|---|
| The same animal keeps triggering false alerts | Our idea of normal for that animal is wrong |
| Many animals start triggering false alerts | Something changed: model drift, a dirty sensor, or an enclosure change nobody recorded |

The false alert rate is how we know whether the system still works. Those keeper answers are
also the only real evidence of what a sick animal looks like here, and they cost nothing
because closing an alert has to happen anyway.

### Set to over-alert rather than miss

Missing a genuinely sick animal is worse than a false alarm, so thresholds are set to catch as
much as possible.

The cost is that keepers who keep getting alerts about healthy animals stop reading them, and a
system nobody reads misses sick animals too. Two things help: slow alerts go on a list rather
than interrupting anyone, and the false alert rate is watched so declining trust is visible
before keepers give up.

If keepers start calling alerts noise, the answer is a better model or a corrected baseline for
that animal. Raising the limits to quieten the system would hide the misses.

## Consequences

| Decision | Cost |
|---|---|
| A vet sets every limit | Someone maintains settings for 55 enclosures, and no vet is on staff by default |
| Only fixed rules may switch equipment on | The model may spot a problem hours early and still wait for a person to read the alert |
| Equipment reached over wifi or cable | Wifi or cabling becomes a siting requirement for any enclosure with controllable equipment |
| Cohort baselines before individual ones | Genuinely unusual individuals are flagged wrongly until we learn they are unusual |
| Lagoon alerts cover the group | We can say feeding looks wrong, but not which fish to catch |
| Alert whenever there is doubt | Keepers walk to healthy animals, and too much of that erodes trust in alerts |

## Assumptions

- A vet supplies limits and procedures per species and reviews them periodically
- Where no vet is on site, a senior keeper responds first, following those procedures
- Security are on the estate during opening hours and reachable outside them

## Open questions

- What the acceptable false alert rate is, and who decides it
- Whether the escalation list is per enclosure, per area, or one rota
- How a vet's settings are entered and reviewed, given the estate has no technology staff

## Related

- **[ADR-040](040-connectivity-topology.md)** put the network on the estate so safety alarms work without the internet
- **[ADR-041](041-hybrid-transport.md)** determines how commands reach equipment
- **[ADR-042](042-telemetry-model.md)** defines the readings this uses
- **[ADR-044](044-disconnected-operation.md)** covers what happens when the connection drops
- **[ADR-046](046-count-reconciliation.md)** covers what happens when a count suggests an animal is unwell
- **[ADR-047](047-environment-and-weather.md)** supplies cohort baselines, threshold provenance and equipment state
