# 10. Evaluation and drift loop

How a model or prompt version earns its way to production, and how we know if it stops
deserving to stay there. Behind [021](../adrs/021-evaluating-ai-before-release.md) and
[022](../adrs/022-detecting-ai-misbehaviour.md).

```mermaid
flowchart TB
  golden[(Golden set: representative, edge, known-bad)]
  gate[021 release gate: grounding + grading + audit]
  canary[Canary: 10% traffic, min 48h / 200 interactions]
  production[Production: 100% traffic]

  disposition[(Disposition log: right / wrong / unclear)]
  groundtruth[(Independent ground truth: ledger, admissions, inspection)]
  person([Person acting on the output])

  monitor[022 drift monitor: rolling 14-day rate vs gate baseline]
  digest[Weekly digest]
  revert[Auto-revert to last known-good]
  opslead([Operations lead])

  golden --> gate
  gate -- fail --> golden
  gate -- pass --> canary
  canary -- breach --> revert
  canary -- clean --> production

  production --> disposition
  production --> groundtruth
  person --> disposition

  disposition --> monitor
  groundtruth --> monitor

  monitor -- Tier 1/2: alert only --> digest
  monitor -- Tier 3: breach --> revert
  monitor --> digest
  digest --> opslead
  revert -.-> canary
  monitor -. audit sample .-> golden

  classDef t1 fill:#EAF3DE,stroke:#639922,color:#173404
  classDef t2 fill:#FAEEDA,stroke:#BA7517,color:#412402
  classDef t3 fill:#EEEDFE,stroke:#7F77DD,color:#26215C
  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef cloud fill:#E6F1FB,stroke:#378ADD,color:#042C53
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528
  classDef ext fill:#FCEBEB,stroke:#E24B4A,color:#501313

  class golden,disposition,groundtruth store
  class gate,canary,production,monitor,digest,revert cloud
  class person,opslead human
```

## Reading it

- The top half is **before release** (021): nothing reaches even a canary slice without
  passing the golden set.
- The bottom half is **after release** (022): the disposition log and the ground-truth
  comparison are the same two signals whether the capability is a day old or a year old
  — there is no separate "monitoring" system to build.
- The loop closes twice: a **breach** reverts to the last known-good version (dashed,
  back toward canary/gateway), and an **audit finding** adds a case to the golden set
  (dashed, back to the top), so the gate gets stricter over time instead of staying
  static.
- Tier 1/2 and Tier 3 diverge only at the monitor: Tier 1/2 always has a person or a
  ledger downstream already, so a breach alerts; Tier 3 has no such backstop, so a
  breach reverts automatically and then alerts.

## Open questions

- Whether 14 days and 10 percentage points (022) are the right sensitivity once real
  disposition data exists, or whether they need tuning per capability rather than one
  shared threshold.
