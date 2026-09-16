# 063. Estate operations copilot

**Go straight to:** [Home](../../README.md) · [ADRs](README.md) · [Diagrams](../diagrams/README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

## Status

Proposed.

## Context

The rest of this repository produces a great deal of data: telemetry
([042](042-telemetry-model.md)), welfare outcomes ([043](043-welfare-loop.md)), zone
counts ([045](045-presence-and-flow.md)), animal counts
([046](046-count-reconciliation.md)), conditions and weather
([047](047-environment-and-weather.md)), admissions
([012](012-admissions-and-ticketing.md)).

None of it helps if the only people who can query it are the people who built it, and
this is a family estate with a small operations staff and no technology function
([C13](../requirements.md#constraints)). A keeper who wants to know whether feeding has fallen off since the cold
snap is not going to write SQL.

The Countess asked to understand which parts of the estate are popular and to turn that
into staffing and investment decisions ([R3](../requirements.md#requirements), [R4](../requirements.md#requirements)). That is a question-asking
problem, and the barrier is the query language.

## Decision

**The copilot translates a question into a query, shows the query, and runs it
read-only.** It is Tier 3 because natural language in is generative by nature, but the
thing it produces is inspected before it is trusted, which is what makes Tier 3
acceptable here.

**The generated query is shown, always, not hidden behind the answer.** A person reading
"admissions where date between X and Y grouped by zone" can tell whether it answers what
they asked, even if they could not have written it. That is the verification mechanism,
and it costs nothing because it is the interface.

**Read-only, with no exceptions.** No writes, no schema changes, no deletes, enforced by
the credentials the copilot holds rather than by the prompt. A prompt is not a permission
boundary.

**Every answer carries its provenance**: which records it read, the time range, the row
count, and whether any of it arrived late after a partition
([044](044-disconnected-operation.md)). A number from a period the estate was
disconnected is a different number, and the person reading it should be told so rather
than left to find out.

**It sits in front of something that works without it.** The raw filter interface named
in [020](020-model-gateway.md) is a real screen people can use, not a theoretical
fallback. When the provider is unavailable or the cost ceiling is reached
([023](023-ai-cost-control.md)), the copilot degrades to that screen.

**Disposition is captured from behaviour, not a survey.** Whether the user ran the
generated query as offered or edited it first is the accuracy signal
[022](022-detecting-ai-misbehaviour.md) reads. Heavy editing is the model being wrong,
recorded for free at the moment it happens.

## Consequences

| Decision | Cost |
|---|---|
| Showing the query | Some users will not read it, and showing it is still the only thing that makes the output checkable |
| Read-only | Cannot be used to correct a bad record, which stays a separate job for whoever owns that data |
| Provenance on every answer | More to render, and it is what stops a partition-shaped hole being read as a real decline |
| Fallback screen must be real | Somebody has to build and maintain a filter interface that most people will rarely use |

### What this provides

- The estate's own data is answerable by the people who work there ([R3](../requirements.md#requirements), [R4](../requirements.md#requirements))
- Verification is the interface rather than an extra step, so it survives [C13](../requirements.md#constraints)
- A drift signal captured from normal use, with nobody asked to rate anything

## Alternatives rejected

| Option | Why not |
|---|---|
| A fixed dashboard instead | Answers the questions we thought of. The questions worth asking are the ones that come up on the day |
| Copilot executes without showing the query | Removes the only verification mechanism, in exchange for one fewer click |
| Write access for corrections | Puts a non-deterministic component in front of the records everything else depends on |
| Training a model on the estate's schema | No ML team ([C13](../requirements.md#constraints)), and schema-in-the-prompt is sufficient at this size |

## Assumptions

- The schema is small and stable enough to describe in a prompt. It grows with the
  estate, and if it outgrows that, this record needs revisiting
- Staff will read a query they did not write. Untested, and the edit rate will show it
  quickly
- Data sensitive enough to need per-user restriction does not exist here, because
  [045](045-presence-and-flow.md) means there are no visitor identities to protect

## Open questions

- Whether keepers and the Countess need different views, or one view is enough
- Whether a question the copilot cannot answer should be logged as a gap in the data
  model rather than discarded
- How far back the queryable history goes before it is archived

## Related

- **[011](011-ai-determinism-tiers.md)** sets the tier and demands this justification
- **[020](020-model-gateway.md)** provides the gateway and names the raw filter fallback
- **[021](021-evaluating-ai-before-release.md)** gates it before release
- **[022](022-detecting-ai-misbehaviour.md)** reads the edit rate as drift
- **[023](023-ai-cost-control.md)** sets its ceiling
- **[044](044-disconnected-operation.md)** is why answers carry partition provenance
- **[042](042-telemetry-model.md)**, **[045](045-presence-and-flow.md)**, **[046](046-count-reconciliation.md)**, **[047](047-environment-and-weather.md)** are what it reads
- Diagram: [03 AI capability map](../diagrams/03-ai-capability-map.md)

---

<p align="center">❦</p>

<p align="right"><a href="#063-estate-operations-copilot">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="README.md">All ADRs</a> · <a href="../diagrams/README.md">All diagrams</a></p>
