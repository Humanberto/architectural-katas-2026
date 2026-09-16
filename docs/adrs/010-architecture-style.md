# 010. Edge-first data plane with a conventional transactional core

**Go straight to:** [Home](../../README.md) · [ADRs](README.md) · [Diagrams](../diagrams/README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

## Status

Proposed

## Context

The brief contains two problems of genuinely different shape, and the most consequential
early decision is to stop treating them as one.

The first is sensing and analysis. Measuring area popularity (R3), monitoring animal
health (R5), tracking feeding (R6), counting piranhas (R7) and moving all of it to the
cloud (R11) are a continuous stream of small observations from hardware scattered across
an estate with patchy wifi (C1) over a path we have to design rather than assume (C2).
The system must keep working while disconnected (R15).

The second is transactions. Selling tickets and family passes (R1) and validating
admission at entry (R2) is a small, strongly-consistent, money-handling problem with
invariants that span entities.

These pull in opposite directions. The first wants asynchronous messaging, local
autonomy and eventual consistency. The second wants a single database and a transaction.
Forcing one style onto both produces either a telemetry pipeline burdened with
transactional guarantees it does not need, or a ticketing system with eventual
consistency it cannot tolerate.

The scale numbers argue for restraint in both. Fifteen thousand visitors a day (C8) is
roughly one admission per second averaged, perhaps twenty per second at gate opening.
Telemetry runs under twenty messages per second estate-wide. Neither is a scale problem.

The operational constraint is the binding one. This is a family estate with a small
operations staff and no in-house ML team (C13), and no budget beyond the funded MQTT
hardware baseline (C14). Every additional moving part is a part nobody is paid to watch.

Three alternatives were considered.

**A. One event-driven system for everything.** Ticketing, passes and payment as services
communicating over the same backbone. Rejected: it converts a database transaction into
a distributed one, and buys elasticity we demonstrably do not need at twenty admissions
per second. The failure mode — a family pass half-issued — is exactly the failure mode
the estate cannot afford.

**B. One conventional cloud application for everything, with sensors calling in.**
Simple, familiar, one thing to operate. Rejected outright by C1 and R15: it stops
entirely when the link drops, which is a normal condition here rather than an outage.

**C. Fine-grained microservices throughout.** Rejected: it is the shape a team of four
with no platform engineer is least able to operate, and there is no scaling or
independent-deployment pressure to justify it.

## Decision

Two styles, chosen per problem, with exactly one new operational paradigm introduced.

**The data plane is edge-first and event-driven.** Sensors publish over MQTT to satellite
brokers that run local inference and buffer with prioritised store-and-forward, as set
out in [040](040-connectivity-topology.md) and [042](042-telemetry-model.md). The estate
is the source of truth until reconciliation; the cloud is where data eventually arrives
and is aggregated. Anything time-critical to safety or welfare is decided on the estate,
because that is the only place it can be decided reliably.

**The transactional core is a modular monolith over one relational database.** Admissions,
passes, entitlements and commerce live in one deployable with enforced module boundaries,
as set out in [012](012-admissions-and-ticketing.md). Invariants stay inside a
transaction.

The two meet at the event backbone and nowhere else. The transactional core publishes
facts, such as an admission, and consumes aggregates, such as an occupancy estimate. It
never queries an edge device and no edge device queries it.

The rule this gives us: if a decision must survive a network partition, it belongs on the
estate. If it must be atomic, it belongs in the monolith. If it is neither, it belongs in
the cloud analytics layer, where it is cheapest.

## Consequences

### Positive

- The patchy-wifi constraint is answered structurally rather than mitigated. Disconnection
  is a designed-for state, not a degraded one.
- One team of four can operate this. There is one event backbone, one database, one
  deployable for transactions, and a known set of edge devices.
- The architectural characteristics of each half match its problem, which is what lets us
  add AI capabilities later without them inheriting guarantees they do not need.
- Scaling from 5,000 to 15,000 visitors (C8, C9) requires no structural change. It is a
  larger database instance and more gate hardware.

### Negative

- Two styles means two mental models, two deployment paths and two sets of failure modes.
  Anyone joining has to learn where the seam is.
- The monolith is a single point of failure for admission sales. Gate validation survives
  it — see [012](012-admissions-and-ticketing.md) — but online purchase does not.
- Reconciliation logic is real work. Data arriving late, out of order, or twice is normal,
  and every consumer must tolerate it.
- If visitor volume ever exceeded this design by an order of magnitude, the monolith would
  need decomposing. We are accepting a rewrite we do not expect to need.

### Assumptions

- Twenty admissions per second at peak is a fair estimate of the gate-opening surge at
  15,000 visitors a day.
- The estate can host modest compute at the satellite brokers, per the funded MQTT
  hardware baseline (C3, C14).
- No regulatory requirement forces ticketing data to remain on the estate.

---

<p align="center">❦</p>

<p align="right"><a href="#010-edge-first-data-plane-with-a-conventional-transactional-core">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="README.md">All ADRs</a> · <a href="../diagrams/README.md">All diagrams</a></p>
