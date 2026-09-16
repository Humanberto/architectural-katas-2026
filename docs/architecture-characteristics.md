# Architectural characteristics

What we are optimising for, in order, and what we are deliberately giving up. Every ADR
in this repository should be traceable to something on this page. If a decision
contradicts this document, one of the two is wrong and we should say which.

Identifiers in brackets come from [requirements](requirements.md).

## How we chose

We did not start from a quality-attribute checklist. We started from the failure modes
that would actually hurt the Countess, and worked back.

| If this fails | What it costs her | So we need |
|---|---|---|
| Gate entry on a busy Saturday | Queues, refunds, reviews, no return visits (P4, R10) | Admission that works with no network at all |
| A sick animal is spotted late | Vet bills, a death, licence risk on a venomous collection (P3, C6) | High integrity and an auditable welfare record |
| Footfall data is patchy | Staff in the wrong places; the central question stays unanswered (P2, R4) | Eventual completeness over real-time precision |
| Ticketing during a holiday peak | Lost revenue at the one moment revenue exists (P1, C8) | Elasticity on the sales path specifically |
| A model provider triples its price | An unbudgeted cost the estate cannot absorb (C11, C14) | Replaceability of every model |
| An AI feature quietly degrades | Wrong staffing, missed welfare signals, nobody notices (C12, R13) | Observability of non-deterministic behaviour |

## The ranking

Ranked deliberately. Everything cannot be first, and the ranking is what lets us say no
later without relitigating.

**1. Resilience under intermittent connectivity.** Wifi is patchy (C1), the estate-to-cloud
path is ours to design (C2), and the system must keep working while disconnected (R15).
The estate is the source of truth until reconciliation, not the cloud. This is the
characteristic that most shapes the topology, and it is why
[040](adrs/040-connectivity-topology.md) and
[012](adrs/012-admissions-and-ticketing.md) look the way they do.

**2. Data integrity, for welfare and for money.** Welfare records and financial
transactions are auditable and not silently rewritten. No AI output overwrites a
recorded fact; it is stored alongside as an opinion with its model version and
confidence. A licensed collection of venomous animals (C6, C10) is a regulated context
even where the brief does not say so.

**3. Replaceability of AI components.** Assume every model we choose is wrong within a
year (C11, R14). Models sit behind an internal contract and are never called directly
from business logic. This is what makes a price rise or a shutdown an operational event
instead of a rewrite.

**4. Cost efficiency.** The estate is unprofitable and must become profitable or be sold
up (P1, P5). The only funded baseline is MQTT hardware (C3, C14). Cost per capability is
an architectural constraint here, not a finance review — and a capability whose cost
scales with visitors gets more expensive precisely as the estate succeeds (C8).

**5. Observability of non-deterministic behaviour.** Generative behaviour is
non-deterministic (C12) and the brief asks us to detect misbehaviour in production
(R13). If we cannot tell that a capability has drifted, we do not deploy that capability.

**6. Elasticity, scoped.** Fifteen thousand visitors a day (C8) over three years (C9) is
roughly one admission per second, perhaps twenty per second at gate opening. Only the
public sales and visitor-facing paths need to scale sharply. The back office does not.

## What we are deliberately not optimising for

Naming these is what stops the design sprawling, and it is half the value of this page.

- **Sub-second real time.** Nothing here needs it. Welfare alerting within a minute is
  fine; footfall aggregation within fifteen minutes is fine. Refusing a real-time
  requirement we do not have buys enormous simplicity.
- **Extreme scale.** This is a small system. Designing it as a large one is the most
  likely way to fail the suitability criterion.
- **Multi-region resilience.** One cloud region plus genuinely capable edge is right for
  a single physical estate.
- **Fine-grained microservices.** There is no independent-deployment or scaling pressure,
  and there is no platform team (C13). See [010](adrs/010-architecture-style.md).

## The operational constraint behind all of it

This is a family estate, not a technology company, with a small operations staff and no
in-house ML team (C13). Every additional moving part is a part nobody is paid to watch.
Where two designs are close, we take the one that is easier to operate on a normal
Tuesday, and we say so in the ADR.

## Where each characteristic is realised

Linked numbers are records in this repository. Plain numbers are decisions we have
identified but not yet written up.

| Characteristic | Realised by |
|---|---|
| Resilience under intermittent connectivity | Satellite brokers with prioritised local buffering ([040](adrs/040-connectivity-topology.md), [042](adrs/042-telemetry-model.md)); offline-verifiable passes ([012](adrs/012-admissions-and-ticketing.md)); content cached at the gate so the visitor app works with no signal (062); reconciliation after a partition (044) |
| Data integrity, welfare and money | Vet-set thresholds with AI advising only ([043](adrs/043-welfare-loop.md)); statutory inspection as the sole safety authority for rides (060); admission events as the estate-wide ground truth ([012](adrs/012-admissions-and-ticketing.md)) |
| Replaceability of AI | Capability-based model gateway (020) |
| Cost efficiency | Lowest tier that works ([011](adrs/011-ai-determinism-tiers.md)); per-capability ceilings and graceful degradation (023) |
| Observability of non-determinism | Evaluation before release (021) and drift detection with rollback (022); the generated query shown beside the answer (063); population estimate reconciled against a keeper stock ledger (046) |
| Scoped elasticity | Single transactional core with an elastic public path ([010](adrs/010-architecture-style.md), [012](adrs/012-admissions-and-ticketing.md)); demand forecast driving capacity release and rostering (061) |

Two gaps are worth stating plainly. Replaceability of AI rests on a single record, 020,
which is not yet written. And most of what backs observability is still to be written —
which is the hardest of these characteristics to evidence, and the one where a proposal
is most easily taken on trust when it should not be.

## The one rule that follows from all of this

Use the lowest determinism tier that solves the problem, and justify any use of a
generative model in its own record. Most of this estate's problems are measurement and
forecasting problems, and treating them as such is cheaper, more verifiable, and works
when the network does not. This is stated properly in
[011](adrs/011-ai-determinism-tiers.md).

