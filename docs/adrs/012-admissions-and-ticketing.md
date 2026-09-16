# 012. Admissions and ticketing, with gates that work offline

**Go straight to:** [Home](../../README.md) · [ADRs](README.md) · [Diagrams](../diagrams/README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

## Status

Proposed

## Context

There is no ticketing or admission system today ([P8](../requirements.md#problems)). We need to sell tickets including
family passes ([R1](../requirements.md#requirements)) and validate admission at entry at scale ([R2](../requirements.md#requirements)), growing from 5,000 to
15,000 visitors a day over three years ([C8](../requirements.md#constraints), [C9](../requirements.md#constraints)).

The hard part is not selling. It is the gate.

Wifi coverage across the park is patchy ([C1](../requirements.md#constraints)), and the estate must keep operating while
disconnected from the cloud ([R15](../requirements.md#requirements)). A gate that cannot validate a pass without a network
call is a gate that forms a queue on the one Saturday the estate most needs to not have
a queue. Given [P4](../requirements.md#problems) and [R10](../requirements.md#requirements) — the estate's difficulty in attracting returning visitors —
an hour lost at the entrance is expensive well beyond that day's revenue.

Family passes are what make the data model non-trivial. A pass admits a defined party,
possibly on multiple days, possibly with different entitlements per member. Issuing,
amending and refunding one touches several entities at once, and getting it half-right
is worse than rejecting it.

Three alternatives were considered.

**A. Buy third-party ticketing software.** Genuinely attractive given [C13](../requirements.md#constraints) and [C14](../requirements.md#constraints): it is
a solved commercial problem and nobody on this team has to maintain it. Rejected on the
gate, not the sale. Off-the-shelf systems assume connectivity at the point of scan, and
the estate's constraint is precisely that connectivity is unreliable. We would still be
building the offline path, and we would be building it against someone else's data model.
Worth revisiting if a product with genuine offline validation is found.

**B. Online-only validation.** Gate scanners call the admissions service on every scan.
Simple, immediately consistent, no re-use window at all. Rejected by [C1](../requirements.md#constraints) and [R15](../requirements.md#requirements).

**C. Admissions as microservices.** Rejected in [010](010-architecture-style.md): it
converts the family-pass invariants into distributed transactions to buy elasticity we do
not need at roughly twenty admissions per second.

## Decision

**Admissions is a modular monolith over one relational database**, with enforced module
boundaries for catalogue, orders, passes, entitlements and refunds. Family-pass
invariants stay inside a single transaction.

**Passes are cryptographically signed tokens that a gate can verify with no network at
all.** A pass is issued as a signed payload — pass identifier, party size and composition,
validity window, entitlements — encoded as a QR code or written to NFC. The signature is
verified against a public key cached on the scanner. No lookup is required to establish
that a pass is authentic and unexpired.

**The scanner holds a cached revocation list** for passes refunded or reported lost,
refreshed opportunistically whenever it has connectivity. Revocation is the only case
requiring shared state, and it is small.

**Every scan is recorded locally and forwarded on the satellite broker's queue** per
[040](040-connectivity-topology.md) and [042](042-telemetry-model.md), carrying pass
identifier, gate, members admitted and timestamp. Reconciliation happens centrally when
the records arrive.

**We accept a bounded re-use window.** Between a pass being scanned at one gate and that
scan reaching the others, the same pass could in principle be presented again elsewhere.
We accept this deliberately. Detection is after the fact, by reconciliation, and repeat
offenders are handled as a commercial matter rather than an architectural one. The
alternative is gates that stop working, and the fraud exposure on a day ticket is a few
tens of pounds against a queue that costs far more.

Admission events are also the estate-wide ground truth against which zone counts are
reconciled, which is what makes the presence-sensing verification in C's range possible.

## Consequences

### Positive

- Gates work with no network, which is the only acceptable answer given [C1](../requirements.md#constraints).
- Family-pass correctness is enforced by a database transaction rather than by
  compensating logic.
- One deployable and one database is operable by a small staff ([C13](../requirements.md#constraints)).
- Admission events give the analytics layer a trustworthy denominator for every
  popularity and conversion measure ([R3](../requirements.md#requirements), [R4](../requirements.md#requirements)).
- There is no AI anywhere in this record, which is the correct answer for a payment and
  entitlement system and consistent with [011](011-ai-determinism-tiers.md).

### Negative

- A bounded window exists in which a pass could be re-used at a second gate.
- Key management becomes an operational responsibility. Rotating the signing key means
  redistributing the public key to every scanner, and a compromised private key means
  reissuing outstanding passes.
- Passes cannot be amended after issue without reissue, because the entitlement travels
  in the token rather than being looked up.
- Online sales stop if the monolith is down. Gate validation continues, so the estate
  stays open to those who already hold passes.
- We are building something we could have bought, and carrying the maintenance.

### Assumptions

- Gate scanners have local storage and can run signature verification, and are physically
  supervised during opening hours.
- The revocation list stays small enough to distribute to every scanner. This holds while
  refunds are a small fraction of sales.
- Payment is handled by an external provider. We store no card data.
- A short offline re-use window is commercially acceptable to the estate. This is a
  business decision and should be confirmed rather than assumed.

---

<p align="center">❦</p>

<p align="right"><a href="#012-admissions-and-ticketing-with-gates-that-work-offline">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="README.md">All ADRs</a> · <a href="../diagrams/README.md">All diagrams</a></p>
