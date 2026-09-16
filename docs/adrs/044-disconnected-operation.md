# 044. Working while disconnected, and putting the records back together

**Go straight to:** [Home](../../README.md) · [ADRs](README.md) · [Diagrams](../diagrams/README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

## Status

Proposed

## Context

- Wifi coverage across the park is patchy ([C1](../requirements.md#constraints))
- Cloud services are allowed, but the estate-to-cloud path must be designed ([C2](../requirements.md#constraints))
- The system has to keep working while cut off ([R15](../requirements.md#requirements))

A partition is any break that leaves part of the system unable to reach the rest. There are
three, and they are not the same problem.

| Break | Effect |
|---|---|
| Sensor to gateway | Affected sensors buffer their own readings and send them when the radio returns ([ADR-041](041-hybrid-transport.md)) |
| Estate to cloud | The estate carries on. Everything below is about this case |
| The estate machine itself | Reception stops entirely. Named as the largest open risk in [ADR-041](041-hybrid-transport.md), not solved here |

## Decision

While the estate is cut off, the estate's record is authoritative. On reconnection the records
merge, and anything that disagrees is flagged for a person rather than resolved automatically.

### What continues, and what does not

| Continues | Stops |
|---|---|
| All sensor readings, which stay on the estate | Anything requiring the cloud |
| Safety alarms, including containment ([ADR-043](043-welfare-loop.md)) | Assessments from models that run in the cloud |
| The vet's fixed limits and the equipment they control | Trends built from months of data |
| Equipment already running, since schedules and limits are local ([ADR-047](047-environment-and-weather.md)) | The weather forecast, which is an external service |
| Keepers acknowledging and closing alerts | Sending anything off the estate |
| Visitor counting and ticket validation ([ADR-045](045-presence-and-flow.md), [ADR-012](012-admissions-and-ticketing.md)) | Uploading the image files behind camera counts |
| Camera counts, computed on the estate ([ADR-046](046-count-reconciliation.md)) | |

Nothing in a keeper's normal day depends on the connection, which is what the topology in
[ADR-040](040-connectivity-topology.md) was for.

### Merging the records

Buffered readings are sent when the link returns. Most fill gaps and conflict with nothing.

Conflicts are possible only where the same event can be recorded in two places: once on the
estate, and once against the cloud copy while it is stale. Whether the cloud copy is writable
at all belongs to the seat that owns it, and this record assumes it is.

**These are not resolved automatically.** Three situations look identical in the data:

- The same feeding entered twice
- Two staff feeding the same enclosure by mistake
- Two genuine feedings at different times

Guessing either invents a feeding that never happened or hides one that did, and both corrupt
a welfare record. So both versions are kept, the record is marked unresolved, and a
reconciliation task goes to a keeper.

### Reconnecting without an alert storm

Queued readings are not replayed as alerts. The system evaluates the current situation and
handles the gap separately.

| Situation | Result |
|---|---|
| A limit was crossed and is still crossed | Normal alert, normal urgency |
| A limit was crossed and recovered during the outage | One line in a summary |
| Nothing was crossed | Nothing |

The keeper gets one summary of the outage plus normal alerts for anything still happening.
Most readings are quarter-hourly or slower ([ADR-042](042-telemetry-model.md)), so replaying
them would bury whatever still needs attention.

### Gaps stay visible

Every outage is recorded: when it started, when it ended, which enclosures were affected, and
which of the three breaks it was.

Missing readings must never resemble a quiet period. Anything reading this data later, person
or model, has to distinguish "we measured nothing unusual" from "we measured nothing". This
matters more once the data is training material ([ADR-047](047-environment-and-weather.md)),
because a model cannot ask why a week is empty.

## Consequences

| Decision | Cost |
|---|---|
| Estate record authoritative, conflicts go to a person | Somebody resolves them by hand, and until they do the record holds two versions |
| No alert replay, one summary instead | Something that went wrong and fixed itself during an outage interrupts nobody, and a repeating pattern could go unnoticed |
| Outages recorded and shown as gaps | Charts and reports have visible holes |
| Three breaks distinguished | More outage states to record and display than a single connected or disconnected flag |

## Assumptions

- The cloud copy can be written to, so double entry is possible. If it is read-only, the
  conflict handling above is unnecessary
- Reconciliation tasks are resolved within a working day

## Open questions

- How long the estate can run disconnected before local storage becomes a limit
- Whether a keeper should be told during an outage that the estate is cut off, or only
  afterwards in the summary
- What happens to a reconciliation task nobody answers

## Related

- **[ADR-040](040-connectivity-topology.md)** put the broker and buffering on the estate
- **[ADR-041](041-hybrid-transport.md)** reduced that to one machine and moved the LoRaWAN network server onto it, so sensor data stays readable during an outage
- **[ADR-042](042-telemetry-model.md)** defines which readings are buffered and which are guaranteed
- **[ADR-043](043-welfare-loop.md)** defines the alerts this suppresses and summarises
- **[ADR-047](047-environment-and-weather.md)** depends on gaps being distinguishable from quiet

---

<p align="center">❦</p>

<p align="right"><a href="#044-working-while-disconnected-and-putting-the-records-back-together">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="README.md">All ADRs</a> · <a href="../diagrams/README.md">All diagrams</a></p>
