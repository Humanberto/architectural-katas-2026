# Contributing

Simple rules so four people can work in parallel without stepping on each other. Seats
and ownership are in [docs/roles.md](docs/roles.md).

## Branches

- `main` is always the submittable version. Do not commit directly to it.
- One branch per ADR, named for its number: `adr/061-pricing`, matching the branches
  already in flight.
- Diagrams and docs: `diagram/ride-condition`, `docs/overview`.

## Getting your work in

Open a pull request if you want a second pair of eyes. If you do not, tell A and they
will merge it.

We are not requiring peer review before merge. With four people and one week, waiting
for a reviewer costs more than it catches, and A reads everything anyway. Reviewing
after the fact is fine and normal here — say so in the pull request or in chat.

## Writing ADRs

- Take the next free number **in your seat's range**. Ranges are listed in
  [docs/adrs/README.md](docs/adrs/README.md). Do not take the next number in overall
  sequence — someone else has that range.
- Copy `docs/adrs/000-template.md`, or copy a written ADR you like the shape of. 040 and
  042 are the house style; 043 is looser and also fine. Substance matters more than
  format.
- Cite requirement identifiers inline from [docs/requirements.md](docs/requirements.md),
  like `patchy wifi (C1)`. This is the cheapest way to keep four documents consistent.
- Add your file. Leave the index row in `docs/adrs/README.md` to A — that file conflicts
  if several of us edit it.

Some ADRs already exist with a Context section written and the Decision left blank.
Those are yours to finish, and you may rewrite the Context if you disagree with the
framing. They exist so starting is cheap, not to settle anything.

## What makes an ADR done

- At least two rejected alternatives, and why each lost. The Countess is paying for
  judgement, not conclusions, and an ADR that only states a decision shows none.
- Numbers where numbers exist — thresholds, volumes, costs, limits.
- Status moves from Proposed to Accepted at the cold read on Monday 14 September.

## Diagrams

- Diagrams are Mermaid inside Markdown, in `docs/diagrams/`. GitHub renders them, so the
  source and the picture are the same file and cannot drift apart. No exported `.png` to
  keep in sync.
- Use the shared key in [docs/diagrams/README.md](docs/diagrams/README.md). Paste the
  `classDef` lines verbatim. If you need a shape or colour that is not in the key, add it
  to the key first.
- Keep them simple: boxes, arrows, words. Fewer than about 25 nodes.
- Reference every diagram from an ADR or `docs/overview.md`. Only what is linked gets
  read.

## Dates

| When | What |
|---|---|
| Friday 11 September | A drafts the container view, incomplete on purpose |
| Monday 14 September | Cold read, and the team deadline. Everything merged |
| Tuesday 15 September | A integrates — overview, README, consistency |
| Wednesday 16 September | Submit in the morning. The rest of the day is contingency |

## Before we submit

- `README.md` links to every deliverable and nothing is orphaned.
- Every diagram has a key and is referenced from somewhere.
- Every ADR is Accepted, or explicitly marked as a decision we did not reach.
