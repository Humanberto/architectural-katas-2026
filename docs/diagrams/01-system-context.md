# 01. System context

Who uses the Von Digitalis systems, and what we depend on outside them. Shapes and
colours are defined in the [key](README.md#the-key).

```mermaid
flowchart TB
  visitor([Visitor])
  keeper([Keeper])
  vet([Vet])
  engineer([Maintenance engineer])
  manager([Countess and managers])
  gate([Gate staff])

  platform[Von Digitalis platform]

  payment[[Payment provider]]
  weather[[Weather service]]
  models[[Model providers]]

  visitor -->|Buys passes, plans the day| platform
  gate -->|Scans passes| platform
  keeper -->|Records feeds, closes alerts| platform
  vet -->|Sets safe ranges per species| platform
  engineer -->|Closes condition advisories| platform
  manager -->|Asks questions, sets prices| platform

  platform -->|Takes payment| payment
  platform -->|Reads forecast| weather
  platform -->|Calls generative capabilities| models

  classDef t1 fill:#EAF3DE,stroke:#639922,color:#173404
  classDef t2 fill:#FAEEDA,stroke:#BA7517,color:#412402
  classDef t3 fill:#EEEDFE,stroke:#7F77DD,color:#26215C
  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef cloud fill:#E6F1FB,stroke:#378ADD,color:#042C53
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528
  classDef ext fill:#FCEBEB,stroke:#E24B4A,color:#501313

  class visitor,keeper,vet,engineer,manager,gate human
  class platform cloud
  class payment,weather,models ext
```

## Notes

Six kinds of person, three external dependencies. Only one of those dependencies —
model providers — is volatile (C11), and only two capabilities use it, which is the
argument made in [011](../adrs/011-ai-determinism-tiers.md).

The vet appears as an actor rather than a role inside the estate because
[043](../adrs/043-welfare-loop.md) makes them the authority on what "unwell" means, and
there is no vet on staff by default.

## Questions we would settle with the Countess

- Are gate staff a distinct actor, or just keepers on a different shift?
- Does a schools or groups booking channel need to appear separately?
- Should the statutory ride inspector appear? They are an authority the system defers to
  but never talks to.
