# 10. Evaluation and drift loop

**Go straight to:** [Home](../../README.md) · [ADRs](../adrs/README.md) · [Diagrams](README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

How a model or prompt version earns its way to production, and how we know if it stops
deserving to stay there. Behind [021](../adrs/021-evaluating-ai-before-release.md) and
[022](../adrs/022-detecting-ai-misbehaviour.md).

```mermaid
flowchart TB
  candidate{{A new model or a new prompt<br/>both count as a release}}

  golden[(Golden set<br/>representative, edge, must-refuse)]
  gate[021 release gate<br/>runs in CI, blocks the merge]
  canary[Canary<br/>10% of traffic, 48 hours or 200 calls]
  production[Full release<br/>all traffic]

  person([Whoever acted on the output<br/>keeper, inspector, ops user])
  disposition[(Disposition log<br/>right, wrong, or unclear)]
  groundtruth[(Physical ground truth<br/>keeper count, gate admissions, inspection)]

  monitor[022 drift monitor<br/>14-day rate vs the rate at release]
  revert[Revert<br/>last known-good version, minutes]
  digest[Weekly digest<br/>seven lines, one recipient]
  opslead([Operations lead])

  candidate --> gate
  golden -- every case, every time --> gate
  gate -- fail: it does not ship --> candidate
  gate -- pass --> canary
  canary -- breach on the 10% slice --> revert
  canary -- clean --> production

  production --> disposition
  production --> groundtruth
  person -- costs nothing, they were closing it anyway --> disposition

  disposition -- did it turn out to be right --> monitor
  groundtruth -- does the model still agree with the world --> monitor

  monitor -- Tier 1 and 2: a person is already downstream --> digest
  monitor -- Tier 3: nothing is downstream, so revert first --> revert
  monitor -. an audit finding becomes a new case .-> golden
  digest --> opslead
  revert -. previous version resumes .-> production

  classDef t1 fill:#EAF3DE,stroke:#639922,color:#173404
  classDef t2 fill:#FAEEDA,stroke:#BA7517,color:#412402
  classDef t3 fill:#EEEDFE,stroke:#7F77DD,color:#26215C
  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef cloud fill:#E6F1FB,stroke:#378ADD,color:#042C53
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528
  classDef ext fill:#FCEBEB,stroke:#E24B4A,color:#501313

  class candidate t3
  class golden,disposition,groundtruth store
  class gate,canary,production,monitor,digest,revert cloud
  class person,opslead human
```

## Reading it

- Read it top to bottom once and the shape is: **nothing ships unproven, nothing stays
  unwatched.** The top half is [021](../adrs/021-evaluating-ai-before-release.md), the bottom half is [022](../adrs/022-detecting-ai-misbehaviour.md), and they share the
  golden set, so the same evidence works before and after release.
- A prompt edit enters at the same top box as a new model. That is the point of the
  label: wording is how grounding and refusal behaviour break, so it gets the full gate.
- The two pink stores are the whole detection strategy. Neither costs anything to
  produce: the **disposition** is a keeper closing an alert they had to close anyway,
  and the **ground truth** is a count somebody was already taking. No labelling project,
  no data team.
- The two arrows out of the monitor are the one place tiers behave differently, and the
  edge labels say why rather than just what. Tier 1 and 2 always have a person or a
  physical count standing behind them ([043](../adrs/043-welfare-loop.md), [045](../adrs/045-presence-and-flow.md), [046](../adrs/046-count-reconciliation.md)), so an alert is enough.
  Tier 3 has nothing behind it, so the gateway reverts first and tells someone after.
- The loop closes twice. A breach puts the last known-good version back. An audit
  finding becomes a new golden-set case, so the gate gets stricter over time instead of
  aging into a formality.

## Open questions

- Whether 14 days and 10 percentage points ([022](../adrs/022-detecting-ai-misbehaviour.md)) are the right sensitivity once real
  disposition data exists, or whether they need tuning per capability rather than one
  shared threshold.

---

<p align="center">❦</p>

<p align="right"><a href="#10-evaluation-and-drift-loop">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="../adrs/README.md">All ADRs</a> · <a href="README.md">All diagrams</a></p>
