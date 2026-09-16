# 060. Ride condition monitoring

**Go straight to:** [Home](../../README.md) · [ADRs](README.md) · [Diagrams](../diagrams/README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

## Status

Proposed.

## Context

Forty rides ([C4](../requirements.md#constraints)), all 18th-century and historically important, recently passed safety
inspection after the asbestos, broken glass and garden gnomes were removed. Their
historic value limits what may be physically modified ([C7](../requirements.md#constraints), derived).

A ride out of service is lost revenue on an estate that cannot afford it
([P1](../requirements.md#problems)), and an unplanned closure on a busy day is worse than a planned one on a quiet
day. The opportunity is to notice a change in a ride's mechanical behaviour before it
becomes a fault, so maintenance is scheduled rather than forced.

The risk is obvious enough to state plainly: this is safety-adjacent equipment, and a
model that is wrong in the confident direction would be worse than no model at all.

## Decision

**A ride's condition is a perceptual signal, so it is Tier 2 under
[011](011-ai-determinism-tiers.md), and it advises only.** Each ride has a normal
vibration and acoustic signature. A model learns that signature per ride and reports
divergence from it. It does not classify faults, and it does not have a safe or unsafe
output.

**No model, and no rule, may stop a ride.** Only a person may take a ride out of
service. The system raises an advisory; the decision and the liability stay with the
inspector, which is the same boundary [043](043-welfare-loop.md) draws for animals.

**Sensing is non-invasive.** Clamp-on or surface-mounted accelerometers and microphones,
mounted on structure rather than fabric, nothing drilled, bolted or bonded to historic
material ([C7](../requirements.md#constraints)). Where a ride offers no acceptable mounting point it gets no sensor and
stays on inspection alone. Coverage is a consequence of what the rides permit, not a
target to hit.

**Per-ride baselines, not a fleet model.** Forty rides of different ages and mechanisms
have nothing useful in common. Each ride is compared against its own recorded history,
in the form [047](047-environment-and-weather.md) defines, with ambient temperature
carried alongside because metal sounds different on a cold morning.

**Transport and behaviour under partition are inherited, not reinvented.** Summary
features travel over LoRaWAN, raw audio over wifi when available, per
[041](041-hybrid-transport.md); the topic shape and delivery guarantees are
[042](042-telemetry-model.md)'s; buffering and replay during an outage are
[044](044-disconnected-operation.md)'s.

**Every advisory is closed by the person who acted on it** — genuine, not genuine, or
unclear. That disposition is the accuracy measurement, and it is the signal
[022](022-detecting-ai-misbehaviour.md) reads. The independent ground truth is the
inspection outcome, which arrives on its own schedule and owes the system nothing.

## Consequences

| Decision | Cost |
|---|---|
| Advisory only | A real fault the model saw can still reach a visitor, because nothing acts on it automatically. This is the correct trade, and it must be said out loud rather than implied |
| Non-invasive sensing | Weaker signal than a properly instrumented machine, and some rides cannot be covered at all |
| Per-ride baselines | Forty baselines to establish, each needing a season of history before it means much. The first months produce noise |
| Advisories closed by hand | Adds a step to the inspector's day. It is the only thing making the model measurable, so it is not optional |

### What this provides

- A maintenance signal that arrives before a failure does, on equipment that cannot be
  replaced
- Evidence of correctness that does not depend on a model grading itself
- No new authority granted to anything non-deterministic

## Alternatives rejected

| Option | Why not |
|---|---|
| Automatic shutdown on a threshold breach | A false positive closes a ride on a busy day, and a true positive that nobody inspected is a liability nobody accepted. The estate has no appetite for either |
| A fault-classification model | Requires labelled examples of failures that have not happened yet on rides that are three hundred years old |
| Fixed thresholds instead of learned baselines | Forty different mechanisms do not share a threshold, and a number chosen in advance would be wrong on nearly all of them |
| Scheduled inspection alone, no sensing | The status quo, and it is defensible. Rejected because it cannot see between inspections, which is where deterioration happens |

## Assumptions

- Rides run repeatable cycles, so a signature is a meaningful thing to learn. Untested,
  and a ride that fails this simply produces no usable baseline and falls back to
  inspection
- Sensors can be mounted on enough rides to be worth the effort. Unknown until someone
  walks the park with an inspector
- The inspector is willing to record a disposition against each advisory

## Open questions

- Who is accountable when an advisory is raised and not acted on, and where that is
  recorded
- Whether advisories should be visible to the Countess as a report, and at what cadence
- Whether a ride with no sensor should be marked as such in the operations view, so
  absence of alerts is not read as absence of problems

## Related

- **[011](011-ai-determinism-tiers.md)** sets the tier and the authority limit
- **[043](043-welfare-loop.md)** is the same advisory pattern applied to animals
- **[041](041-hybrid-transport.md)**, **[042](042-telemetry-model.md)**, **[044](044-disconnected-operation.md)** carry and buffer the readings
- **[047](047-environment-and-weather.md)** records conditions alongside them
- **[022](022-detecting-ai-misbehaviour.md)** reads the disposition log this produces
- Diagram: [03 AI capability map](../diagrams/03-ai-capability-map.md)

---

<p align="center">❦</p>

<p align="right"><a href="#060-ride-condition-monitoring">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="README.md">All ADRs</a> · <a href="../diagrams/README.md">All diagrams</a></p>
