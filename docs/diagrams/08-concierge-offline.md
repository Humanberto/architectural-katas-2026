# 08. Concierge offline behaviour

**Go straight to:** [Home](../../README.md) · [ADRs](../adrs/README.md) · [Diagrams](README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

What a visitor's question reaches when the uplink is up, and what it reaches when there is no
signal at all. Decided in [062](../adrs/062-visitor-concierge.md), routed by
[020](../adrs/020-model-gateway.md).

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 75, 'curve': 'basis', 'padding': 12}}}%%
flowchart LR

  visitor([Visitor])

  subgraph onsite["On the estate — works with no signal"]
    surface[Concierge surface]
    cache[(Cached answers)]
    sources[(Approved source documents)]
    faq[Static FAQ tree<br/>Tier 1, no provider]
    keeper([Keeper])
  end

  gw[Model Gateway<br/>the only holder of a provider key]

  subgraph prov["External provider — needs the uplink"]
    cheap{{Cheaper hosted model}}
    full{{Hosted model<br/>Tier 3, generative}}
  end

  visitor -->|Asks a question| surface
  surface -->|Step 1, cache hit| cache
  surface -->|Safety question, refused| keeper
  surface -->|Step 4, ceiling or no signal| faq
  cache -->|Answer, no call made| visitor
  faq -->|Worse answer, never an error| visitor
  keeper -->|Answers it in person| visitor

  surface -.->|Step 2, by capability name| gw
  sources -.->|Grounding, retrieved per call| gw
  gw -.->|Cheap model first| cheap
  gw -.->|Step 3, escalate under the ceiling| full
  gw -.->|Grounded answer| surface

  classDef t1 fill:#EAF3DE,stroke:#639922,color:#173404
  classDef t2 fill:#FAEEDA,stroke:#BA7517,color:#412402
  classDef t3 fill:#EEEDFE,stroke:#7F77DD,color:#26215C
  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef cloud fill:#E6F1FB,stroke:#378ADD,color:#042C53
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528
  classDef ext fill:#FCEBEB,stroke:#E24B4A,color:#501313

  class surface edge
  class faq t1
  class cache,sources store
  class visitor,keeper human
  class gw cloud
  class cheap,full t3
```

### Key

```mermaid
flowchart LR
  k1[Runs on the estate] ~~~ k2[Deterministic, reproducible] ~~~ k3{{Generative model}} ~~~ k4([A person]) ~~~ k5[(Data store)] ~~~ k6[Runs in the cloud]

  classDef t1 fill:#EAF3DE,stroke:#639922,color:#173404
  classDef t3 fill:#EEEDFE,stroke:#7F77DD,color:#26215C
  classDef edge fill:#E1F5EE,stroke:#1D9E75,color:#04342C
  classDef cloud fill:#E6F1FB,stroke:#378ADD,color:#042C53
  classDef human fill:#F1EFE8,stroke:#888780,color:#2C2C2A
  classDef store fill:#FBEAF0,stroke:#D4537E,color:#4B1528

  class k1 edge
  class k2 t1
  class k3 t3
  class k4 human
  class k5 store
  class k6 cloud
```

| Arrow | Meaning |
|---|---|
| Solid | Always works, connection or not |
| Dotted | Only while the link to the cloud is up |

Green is Tier 1 and purple is Tier 3, from [011](../adrs/011-ai-determinism-tiers.md). Full team
key in [README](README.md).

### Reading it

**Everything inside the estate group answers without a provider.** The cache, the approved source
documents and the static FAQ tree sit on the estate, which is the guarantee
[044](../adrs/044-disconnected-operation.md) gives everything else on site. A visitor gets a
worse answer, never an error page ([062](../adrs/062-visitor-concierge.md)).

**The dotted arrows are the whole of the cloud dependency.** The surface asks for a capability by
name rather than naming a vendor, and the gateway is the only thing holding a provider key, so a
provider change is a configuration row ([020](../adrs/020-model-gateway.md)).

**The numbered steps are the degradation ladder.** A cache hit answers with no call at all; a
miss goes to the cheaper model; an answer that is not confident or not grounded escalates to the
full model only while the capability is under its cost ceiling; at the ceiling the request drops
to the FAQ tree, which depends on no provider ([implementation](../implementation.md),
[020](../adrs/020-model-gateway.md)).

**The refusal path never reaches a model.** Anything touching proximity,
handling, allergy or venom is refused and handed to a keeper, enforced as a refusal case in
[021](../adrs/021-evaluating-ai-before-release.md)'s golden set. Every remaining factual claim
must trace to a source document the gateway retrieved for that call, or it is not said
([062](../adrs/062-visitor-concierge.md)).

---

<p align="center">❦</p>

<p align="right"><a href="#08-concierge-offline-behaviour">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="../adrs/README.md">All ADRs</a> · <a href="README.md">All diagrams</a></p>
