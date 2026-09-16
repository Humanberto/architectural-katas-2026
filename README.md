# Architectural Katas 2026: Von Digitalis Estates

**Team 1-800-GOT-KATA** — O'Reilly Architectural Katas 2026: AI-Assisted Software Architecture

## Team

| Name | GitHub |
|------|--------|
| Roberto | [@Humanberto](https://github.com/Humanberto) |
| Sergey Buylov |  [@sgblv](https://github.com/sgblv) |
| Swati Dhami | _add handle_ |
| Kelly Colht | [@kellycolht](https://github.com/kellycolht) |

## The problem

The newly appointed 72nd Countess Von Digitalis needs a modern architecture to make the family estates profitable: ticketing (including family passes), understanding which parts of the park are popular, monitoring the health of 200+ exotic animals across 55 enclosures (including piranha population counts), and growing visitors from 5,000/day to 15,000/day within three years. Wifi is patchy, cloud is allowed, and there is budget for MQTT-capable devices across the park. The brief asks for a strong focus on how AI solves these problems.

Full brief: [`docs/kata-brief.pdf`](docs/kata-brief.pdf)

## Deliverables

**Start here: [`docs/overview.md`](docs/overview.md)** — the whole proposal in two pages.

| Deliverable | Where |
|-------------|-------|
| Overview: short narrative of how the team used AI to solve the Countess's problems | [`docs/overview.md`](docs/overview.md) |
| Diagrams: comprehensive and targeted views for each use of AI | [`docs/diagrams/`](docs/diagrams/README.md) |
| ADRs for AI-related decisions, with trade-off analysis | [`docs/adrs/`](docs/adrs/README.md) |
| (optional) Pertinent implementation details | [`docs/implementation.md`](docs/implementation.md) |
| (semi-finalists) Five-minute video | link to be added |

## Supporting documents

| Document | What it is |
|----------|------------|
| [Architectural characteristics](docs/architecture-characteristics.md) | What we optimised for, in order, and what we deliberately gave up |
| [Problems, requirements and constraints](docs/requirements.md) | Everything the brief tells us, with an identifier so records can cite it |
| [Roles and working agreement](docs/roles.md) | How the four of us divided the work |

## Evaluation criteria

- Innovative use of AI in the solution(s)
- Suitability of the solution given the constraints
- Appropriate levels of detail
- Dealing with uncertainty in the world of AI technology (model/provider changes, pricing, shutdown)
- Architectural characteristics of the additions match the existing architecture
- Validation and verification of AI results (non-deterministic behavior, misbehavior in production)

## Key dates

| Milestone | Deadline |
|-----------|----------|
| Team registration form | Wed Sept 2, 12pm ET |
| **Solution due in this repo** | **Wed Sept 16, 11:59pm ET** |
| Semifinalists announced | Mon Oct 5 |
| Semifinalist video due | Mon Oct 12, 11:59pm ET |
| Winners announced | Wed Oct 21 |

## Working in this repo

See [`CONTRIBUTING.md`](CONTRIBUTING.md). New teammate? Start with [`ONBOARDING.md`](ONBOARDING.md).

## Inspiration

- [The Katalog](https://github.com/thekatalog) — past kata submissions
- [Architectural Katas](https://www.architecturalkatas.com/)
