# Roles and working agreement

**Go straight to:** [Home](../README.md) · [ADRs](adrs/README.md) · [Diagrams](diagrams/README.md) · [Implementation](implementation.md) · [Requirements](requirements.md) · [Characteristics](architecture-characteristics.md) · [Brief](kata-brief.pdf)

Team of four. A working document for the team, not a submission artefact — but it lives in the repo so
everyone is reading the same version.

## The four seats

| | Seat | Owns | ADR range |
| --- | --- | --- | --- |
| **A** | Lead and integrator | The characteristics ranking, the comprehensive view, everything the Countess sees first, admissions and ticketing | 010–019 |
| **B** | AI platform and assurance | Model gateway, evaluation, cost control, authority boundaries | 020–039 |
| **C** | Edge and animals | Connectivity, welfare, the physical estate | 040–059 |
| **D** | Visitors, rides and money | Rides, pricing, concierge, copilot, retention | 060–079 |

Beyond ADRs: A owns `docs/architecture-characteristics.md`, the root `README.md`, the ADR
index, and the key, context and container diagrams. B owns the evaluation and cost
sections of `docs/implementation.md` plus the gateway and evaluation-loop diagrams. C and
D own the diagrams for their own capabilities.

Four people cannot cleanly cover five roles, so something doubles up. We have put
communication with the lead rather than making it a fifth seat or leaving it vacant. With
a team this small the largest risk is incoherence, and the person reading everyone else's
work is already doing the integration — so they may as well own the artefacts where
incoherence shows.

## ADR numbering

ADRs live in `docs/adrs/NNN-kebab-title.md` on the scheme already in the repo. Ranges are
reserved per seat so four people numbering independently do not collide. 040, 042 and 043
are already taken.

A writes few ADRs by design. The lead seat is integration, so the decisions that belong to
it are the cross-cutting ones nobody else can own, plus the one part of the system with no
model in it:

- **010 — architecture style.** The edge-first data plane with a conventional transactional
  core, and why the estate is the source of truth until reconciliation.
- **011 — AI determinism tiers.** Prefer classical, then perceptual, then generative;
  reaching for a language model is the exception that needs justifying. This exists as a
  decision rather than a preference so it can be pointed at, not argued each time.
- **012 — admissions and ticketing.** The transactional core: tickets, family passes,
  entitlements, and gate validation that works when the network does not.

Admissions sits with A rather than D despite being revenue, because it is the piece 010
lands on and the only part of the system with no AI in it. D keeps every AI capability,
which is where the interesting decisions are.

## How we split, and why

**By decision, not by artefact.** Whoever makes a decision writes its ADR and draws its
diagram. We are deliberately not appointing a "diagrams person": that role becomes a
bottleneck transcribing decisions they were not in the room for, and the pictures drift
from the text within days.

The one exception is the comprehensive container diagram, which A draws alone. Four people
designing one picture by consensus produces a worse picture than one person drawing it and
three people attacking it.

## Writing for a seat that has not started

Anyone may write the Context section of an ADR in another seat's range — the problem, the
constraints, the numbers, the alternatives worth considering — and must leave Status as
Proposed and Decision empty. Context is research and it is a gift to whoever picks it up.
Decision is authorship and it belongs to the seat.

## Sequencing

**B front-loads Wednesday to Friday.** C and D reference the model gateway and the
authority taxonomy in nearly every AI ADR they write, so they are blocked until B's gateway
and authority records exist in draft in the 020–039 range. B should get those to "good
enough to build on" fast and refine later, rather than perfecting them in isolation.

**A starts the comprehensive diagram on Friday 11 September**, before C and D have
finished. It is the artefact that surfaces unresolved decisions, which is the point of
drawing it early. Expect it to be wrong twice.

**Everything is blocked on the characteristics ranking**, which is why that is the first
hour of the alignment meeting and involves everyone.

## Two sync points

Not standups. Two meetings that matter.

- **Alignment, whole team, one sitting.** Agree the ranking of architectural
  characteristics and the determinism-tier discipline. Every later disagreement traces back
  to this, and settling it once saves the week.
- **Monday 14 September, cold read.** Everyone reads a slice they did not write and says
  what they did not understand. Whatever was missed is a communication defect, not the
  reader's fault. This is also the team deadline — the 15th and 16th are integration and
  buffer.

## What we are defending

Two ideas; everything else is negotiable.

1. **The characteristics ranking.** It is what lets us say no later.
2. **The determinism-tier discipline** — prefer classical and perceptual models over
   generative ones, and justify every exception. Most teams will over-index on "innovative
   use of AI" and under-serve the three meta-criteria: dealing with AI uncertainty,
   matching architectural characteristics, and verifying non-deterministic results. That
   gap is our opening.

## Notes per seat

- **B** holds three of the six evaluation criteria. If anything needs reinforcing at the cold
  read, this is the highest-value place to put it.
- **C** is furthest ahead — 040, 042 and 043 are written. C also holds the strongest
  verification story, where a model's estimate is reconciled against an independent
  physical record. Worth writing so the Countess cannot miss it.
- **D** has the widest span, and the two generative capabilities are the easiest to
  over-claim. Keep the authority boundaries tight.
- **A** owns the artefacts that fail silently. Nobody chases anyone for a README.

## Conventions

- Branch per ADR: `adr/NNN-topic`, matching the existing branches.
- The ADR index in `docs/adrs/README.md` is A's. Add your file, and let A add the index row
  — it is the file most likely to conflict otherwise.
- Every ADR needs at least two rejected alternatives and why they lost. An ADR that only
  states a decision scores nothing on the criterion it exists to satisfy.

---

<p align="center">❦</p>

<p align="right"><a href="#roles-and-working-agreement">↑ Back to top</a> · <a href="../README.md">Home</a> · <a href="adrs/README.md">All ADRs</a> · <a href="diagrams/README.md">All diagrams</a></p>
