# 044. Working while disconnected, and putting the records back together

## Status

Proposed

## The decision

While the estate is cut off, the estate's own record is the real one. When the connection returns we merge, and anything that disagrees is flagged for a person rather than resolved automatically.

## Why we need to decide this

Wifi across the park is patchy ([C1](https://github.com/Humanberto/architectural-katas-2026/blob/main/docs/requirements.md#:~:text=Source-,C1,-Wifi%20coverage%20across)) and the route from the estate to the cloud is ours to design ([C2](https://github.com/Humanberto/architectural-katas-2026/blob/main/docs/requirements.md#:~:text=stated-,C2,-Cloud%20is%20permitted)). The system has to keep working while cut off ([R15](https://github.com/Humanberto/architectural-katas-2026/blob/main/docs/requirements.md#:~:text=R15,from%20the%20cloud)).

A **partition** is when part of the system cannot talk to the rest. During one, two copies of the truth exist. This record covers what still works while that lasts, and what happens to both copies afterwards.

## What still works while cut off

| Keeps working | Stops working |
|---|---|
| All sensor readings, because they stay on the estate | Anything that needs the cloud |
| Safety alarms, including containment | Long-range trends built from months of data |
| The vet's fixed limits and the equipment they control | Assessments from any model that runs in the cloud |
| Keepers acknowledging and closing alerts | Reporting for the Countess |
| Scheduled rounds, feeding and maintenance | Sending anything off the estate |

Nothing a keeper does on a normal day depends on the connection. That is the point of the topology in ADR-040.

## Putting the records back together

Readings buffered on the estate are sent up when the link returns. Most of them simply fill in gaps and nothing conflicts.

Conflicts happen where a person could have written a record in two places. A keeper logs a feeding on the estate while someone in the office logs one from the cloud copy, which is now stale.

**We do not resolve those automatically.** The system cannot tell the difference between three things that look identical in the data:

- The same feeding entered twice
- Two staff both feeding the same enclosure by mistake
- Two genuine feedings at different times of day

Guessing wrong means either inventing a feeding that never happened or hiding one that did. Both are bad in a welfare record.

So the estate's version is kept, the office version is kept beside it, and a reconciliation task goes to a keeper to say which it was. Until someone answers, both versions are visible and the record is marked unresolved.

## Coming back online without an alert storm

When six hours of readings arrive at once, we do not replay the alerts that would have fired.

Instead the system looks at the situation **now**, and handles the gap separately.

| Situation | What happens |
|---|---|
| A limit was crossed and it is still wrong now | A normal alert, at normal urgency |
| A limit was crossed and it recovered during the outage | One line in a summary, no interruption |
| Nothing was crossed | Nothing |

The keeper gets one summary of what happened while the estate was cut off, and normal alerts for anything still happening. Most readings here are quarter-hourly or slower and are not urgent on their own, so replaying them would bury the one thing that still needs attention.

## Gaps are visible

Every outage is recorded, with when it started, when it ended, and which enclosures were affected.

Missing readings must never look like a quiet period where nothing happened. Anything reading this data later, a person or a model, has to be able to tell the difference between "we measured nothing unusual" and "we measured nothing."

## What we chose, and what it cost us

| We chose | Instead of | What it costs us |
|---|---|---|
| The estate's record is kept, and conflicts go to a person | Letting the newest record win automatically | Somebody has to resolve conflicts by hand, and until they do the record has two versions in it |
| No alert replay. One summary instead | Firing every alert that was missed | If something went wrong and fixed itself during the outage, nobody is interrupted about it, and a repeating pattern could go unnoticed |
| Outages are recorded and shown as gaps | Letting missing readings blend into normal quiet | Charts and reports have visible holes, which looks worse but is honest |

## What this gives us

- A keeper's normal day does not depend on the internet.
- No welfare record is ever silently overwritten or invented.
- The first thing a keeper sees after an outage is what still needs doing, not a backlog.
- Nobody can mistake missing data for good news.

## Assumptions

- Office staff can record events that keepers also record, so double entry is possible.
- Someone resolves reconciliation tasks within a working day.

## Related

- **[ADR-040](https://github.com/Humanberto/architectural-katas-2026/blob/main/docs/adrs/040-connectivity-topology.md)** put the broker and buffering on the estate, which is what makes this possible
- **[ADR-042](https://github.com/Humanberto/architectural-katas-2026/blob/main/docs/adrs/042-telemetry-model.md)** defines which readings are buffered and which are guaranteed
- **[ADR-043](https://github.com/Humanberto/architectural-katas-2026/blob/main/docs/adrs/043-welfare-loop.md)** defines the alerts this suppresses and summarises
