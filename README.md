# Von Digitalis Estates

**Team 1-800-GOT-KATA** · O'Reilly Architectural Katas 2026: AI-Assisted Software Architecture

The 72nd Countess Von Digitalis has inherited estates that lose money. This is the
architecture we built for her, and the order in which it was decided.

**This repository is meant to be read in sequence.** Each chapter ends with the question the
next one answers, and every page returns you here.

**[Begin →](#1--a-countess-inherits-a-problem)**

| Name | GitHub | Owns |
|---|---|---|
| Kelly Colht | [@kellycolht](https://github.com/kellycolht) | The shape of the system, and holding it together |
| Swati Dhami | [@sdhami4](https://github.com/sdhami4) | Running AI safely and affordably |
| Roberto | [@Humanberto](https://github.com/Humanberto) | The estate itself: network, animals, visitors on the ground |
| Sergey Buylov | [@sgblv](https://github.com/sgblv) | Rides, pricing, and turning it into money |

<p align="center">❦</p>

## The chapters

| | Chapter | What is in it |
|---|---|---|
| 1 | [A Countess inherits a problem](#1--a-countess-inherits-a-problem) | The brief, and what she asked for |
| 2 | [Why it is harder than it sounds](#2--why-it-is-harder-than-it-sounds) | Patchy wifi, an unreliable cloud, nobody to run it |
| 3 | [Deciding the shape first](#3--deciding-the-shape-first) | Architecture style, AI determinism tiers, ticketing |
| 4 | [An estate that cannot hear itself](#4--an-estate-that-cannot-hear-itself) | Network topology, LoRaWAN, the telemetry model |
| 5 | [Now it can hear. What may it do?](#5--now-it-can-hear-what-may-it-do) | The welfare loop and the authority boundary |
| 6 | [Take the connection away](#6--take-the-connection-away) | Disconnected operation and reconciliation |
| 7 | [Counting what cannot be seen](#7--counting-what-cannot-be-seen) | Piranha population, checked against a keeper |
| 8 | [Counting people without knowing them](#8--counting-people-without-knowing-them) | Visitor presence and flow, without identifying anyone |
| 9 | [All of this leaves a record](#9--all-of-this-leaves-a-record) | Conditions, weather, equipment state, training data |
| 10 | [Who watches the models?](#10--who-watches-the-models) | Gateway, evaluation gates, drift detection, cost |
| 11 | [Turning it into money](#11--turning-it-into-money) | Rides, pricing, concierge, copilot, retention |
| 12 | [Standing back](#12--standing-back) | The decision map and the overview |

**Go straight to:** [Overview](docs/overview.md) · [Architectural characteristics](docs/architecture-characteristics.md) · [ADRs](docs/adrs/README.md) ·
[Diagrams](docs/diagrams/README.md) · [Implementation](docs/implementation.md) ·
[Requirements](docs/requirements.md) · [Brief](docs/kata-brief.pdf)

<p align="center">❦</p>

## 1 · A Countess inherits a problem

After a bizarre gardening accident, the 204th in line becomes the 72nd Countess Von Digitalis.
The estates are large, sprawling, and in need of help to make them profitable. The family's
previous business of making unfortunately highly explosive garden gnomes is no longer viable.

What remains is an extensive, historically important collection of 18th-century amusement park
rides, recently passed safety inspection after the asbestos, broken glass and garden gnomes
were removed. And a previously private exotic and poisonous animal collection, a mix of aquatic
and land-based animals, which is also going to be opened to the public.

Five thousand visitors come each day. Fifteen thousand are hoped for within three years, or the
family may be forced to sell the carnivorous plant collection.

The Countess asked for six things: sell tickets including family passes, understand how popular
different parts of the park are, monitor animal health and how much and how well they are
eating, check piranha population levels, grow visitor numbers, and make the estates more
profitable. The brief asked for a seventh: place the focus on how AI could solve these
problems, and prove the results can be trusted.

Every problem, requirement and constraint has an identifier, and every decision record cites
them inline. They live in [requirements.md](docs/requirements.md).

<p align="right"><a href="#von-digitalis-estates">↑ Back to top</a></p>

<p align="center">❦</p>

## 2 · Why it is harder than it sounds

Three facts make this a different problem from the one it resembles.

**The estate cannot reliably talk to itself.** Wifi coverage on the park is patchy. Not slow in
places: absent in places. Any design assuming a network reaches all 55 enclosures has already
failed.

**The cloud is allowed, but the road to it is ours to build.** The brief says cloud services may
be used, and that we need some way of getting information from the estate to the cloud. Which
means it can be assumed to break, and the estate has to carry on while it does. Animals do not
wait for an uplink.

**There is nobody here to run this.** A family estate, not a technology company: a small
operations staff and no in-house ML team. Anything requiring a specialist to operate, or to
interpret, will not be operated or interpreted.

Around those sit the rest: 40 rides that are historically important and cannot be freely
modified, over 200 animals across 55 displays and enclosures with several poisonous and
hazardous to enter, a budget for MQTT-capable hardware devices installed throughout the park
and silence beyond it, and AI providers that change their models and their prices without
asking.

Those three facts explain nearly every decision that follows. When a choice below looks
conservative, it is usually one of them.

<p align="right"><a href="#von-digitalis-estates">↑ Back to top</a></p>

<p align="center">❦</p>

## 3 · Deciding the shape first

Before anything could be built, two questions had to be settled: where does the truth live, and
how much of this should be AI at all?

| Read | What it settles |
|---|---|
| [010 Architecture style](docs/adrs/010-architecture-style.md) | An edge-first data plane with a conventional transactional core. The estate holds the truth until reconciliation |
| [011 AI determinism tiers](docs/adrs/011-ai-determinism-tiers.md) | Prefer classical, then perceptual, then generative. Reaching for a language model is the exception that has to be argued |
| [012 Admissions and ticketing](docs/adrs/012-admissions-and-ticketing.md) | Tickets, family passes and gates that work when the network does not |
| [01 System context](docs/diagrams/01-system-context.md) · [02 Container view](docs/diagrams/02-container-view.md) | The system, and everything it depends on |

The second of those is the most consequential decision in the repository, and the least
dramatic. It is why this submission is not a pile of language models. Most capabilities here are
deterministic, run on the estate, and depend on no provider at all, which quietly answers most
of the cost, reliability and uncertainty questions before they are asked.

Admissions sits here rather than with the commercial work because it is the one part of the
system with no AI in it whatsoever, and because everything else needs a reliable count of who
came through the gate.

So the shape is decided. None of it matters if a reading cannot get out of an enclosure.

<p align="right"><a href="#von-digitalis-estates">↑ Back to top</a></p>

<p align="center">❦</p>

## 4 · An estate that cannot hear itself

Patchy wifi is the first real obstacle, and this is where we changed our minds in public rather
than quietly.

The original answer scattered small brokers around the park so every sensor had one within
range. It worked, and it spent hardware to solve a problem the radio could solve better. When a
teammate pointed that out, we did not rewrite history. We wrote a second record saying what
changed and why.

| Read | What it settles |
|---|---|
| [040 Tiered topology](docs/adrs/040-connectivity-topology.md) | What runs on the estate, what runs in the cloud, and the rule that decides |
| [041 Hybrid transport](docs/adrs/041-hybrid-transport.md) | Sensors move to LoRaWAN. Amends 040 |
| [042 Telemetry model](docs/adrs/042-telemetry-model.md) | The topic tree, four enclosure archetypes, and which streams are guaranteed |
| [04 Edge connectivity](docs/diagrams/04-edge-connectivity.md) | All of it, drawn |

The effect of LoRaWAN is not really the radio. It is that **the coverage problem moves**: 55
enclosures no longer need a network, only two gateways do, and gateways can be placed where
power already exists. Cameras and equipment stay on wifi, because a LoRaWAN message cannot carry
an image and cannot deliver a command promptly.

Readings are now arriving. Which raises a much harder question than how they got here.

<p align="right"><a href="#von-digitalis-estates">↑ Back to top</a></p>

<p align="center">❦</p>

## 5 · Now it can hear. What may it do?

This is the decision the whole submission turns on.

**Fixed rules written by a vet may switch equipment on by themselves. Anything a model works out
may only be a suggestion to a person.**

| Read | What it settles |
|---|---|
| [043 Welfare loop](docs/adrs/043-welfare-loop.md) | The authority boundary, and how we know when we get it wrong |
| [05 Welfare monitoring](docs/diagrams/05-welfare-monitoring.md) | The boundary, drawn |

We keep that rule even where the model is better at spotting problems than the limit is. If a
pump runs because oxygen fell below a number a vet wrote down, that can be explained to anyone,
afterwards, exactly. If it runs because a model decided something, explaining it needs someone
who understands the model, and the estate does not employ that person.

Two ideas inside this record are worth more than the rule itself.

**The animals are sensors.** A fish that stops coming up to feed may be reporting the water
before the oxygen probe has drifted enough to notice. One observation answers two questions: is
the animal unwell, or is the enclosure wrong?

**Every alert a keeper closes is a free label.** Closing it has to happen anyway, and recording
whether the problem was real turns routine work into permanent evidence. That pattern is
generalised across the whole system in chapter 10.

All of which assumed the estate was connected. It will not always be.

<p align="right"><a href="#von-digitalis-estates">↑ Back to top</a></p>

<p align="center">❦</p>

## 6 · Take the connection away

| Read | What it settles |
|---|---|
| [044 Disconnected operation](docs/adrs/044-disconnected-operation.md) | Three kinds of break, what survives each, and how records merge afterwards |

Not one outage but three, and they behave differently: a sensor losing its gateway, the estate
losing the cloud, and the estate machine itself failing. Only the middle one is survivable by
design, and the record says so plainly rather than implying all three are handled.

While cut off, the estate's own record is the true one. When the link returns, anything that
disagrees goes to a person, because the system cannot tell the difference between the same
feeding entered twice and two genuine feedings, and guessing wrong either invents a meal or
hides one.

One detail from here matters more than it looks: **outages are recorded as gaps.** Missing
readings must never resemble a quiet period, because a model reading this data in two years
cannot ask why a week is empty.

<p align="right"><a href="#von-digitalis-estates">↑ Back to top</a></p>

<p align="center">❦</p>

## 7 · Counting what cannot be seen

The Countess needs to check population levels in the jumping piranha collection. Nobody knows
the number, the water is murky, and the fish jump.

| Read | What it settles |
|---|---|
| [046 Count reconciliation](docs/adrs/046-count-reconciliation.md) | The keeper's count is the record. The camera is an estimate checked against it |

The obvious approach is a submerged camera, which would photograph sediment. The next obvious
approach is photographing the keeper's ledger and reading the handwriting with a model, which
would be worse: a misread digit and a missing animal become identical in the data, and the check
would be a model checking a model.

So a keeper types a number, and that number is the record. The camera watches the surface, where
fish come to feed, and counts what it can see. The two are compared as a ratio rather than a
difference, because the surface count is always a fraction of the truth and it is the change in
that fraction which means something.

And because the brief tells us the piranhas jump, we count the jumps too. A jump is a surface
disturbance. It requires no visibility through the water at all.

That is one counting problem. The other one involves people, and is more delicate.

<p align="right"><a href="#von-digitalis-estates">↑ Back to top</a></p>

<p align="center">❦</p>

## 8 · Counting people without knowing them

The Countess has no real idea what parts of the estates are most popular, which makes it
difficult to know where to invest and deploy staff.

| Read | What it settles |
|---|---|
| [045 Presence and flow](docs/adrs/045-presence-and-flow.md) | Count with equipment that cannot identify anyone |
| [06 Presence and flow](docs/diagrams/06-presence-and-flow.md) | Counting and calibration, drawn |

The conventional answers are cameras that detect people and sensors that count phones. Both
produce a record of where individuals went, at a family attraction whose animal collection has
never been open to the public before.

So the decision is made in the hardware rather than in a policy. Beam-break, thermal and
time-of-flight counters produce a number and nothing else: no image, no device address, nothing
that can be linked to a person afterwards. Asked later for records of individual movement, the
estate has none, and that answer does not depend on anyone following a process correctly.

The counters undercount groups walking abreast, which matters because family passes make groups
common, so ticket validation at the gate calibrates them daily. The same pattern as the
piranhas: a frequent cheap estimate, corrected by a scarcer reliable fact.

By now the estate is producing a great deal of data. It is worth asking what it is for.

<p align="right"><a href="#von-digitalis-estates">↑ Back to top</a></p>

<p align="center">❦</p>

## 9 · All of this leaves a record

| Read | What it settles |
|---|---|
| [047 Recording conditions](docs/adrs/047-environment-and-weather.md) | Weather, forecast, conditions, equipment state, feeding, behaviour and visitors, on one clock, kept the same way for years |

Nobody on this team is building the models that will eventually read this. That is rather the
point: the job is to make sure that when somebody does, the data is worth training on. Data not
recorded in September cannot be recovered in March.

Which is why equipment reports its own state rather than only receiving instructions. A record
showing the temperature falling, without recording that the mister actually ran, teaches a
future model that enclosures cool themselves.

It also answers the question every monitoring system fails on: what happens on day one, when
nothing is known about any individual animal? The estate has over 200 animals, so an
individual's expected range starts as its cohort's and becomes its own as evidence accumulates.
A constraint turned into an asset.

Weather sits here too, because the same heat that empties the midway changes how animals behave,
and a forecast is the only stream that lets anyone act before a problem rather than after it.

<p align="right"><a href="#von-digitalis-estates">↑ Back to top</a></p>

<p align="center">❦</p>

## 10 · Who watches the models?

Models drift. One that passed every test in September can be quietly worse in November, with no
error, no exception, and nothing broken. The brief asks for this specifically.

| Read | What it settles |
|---|---|
| [020 Model gateway](docs/adrs/020-model-gateway.md) | Every generative capability calls one internal gateway. No business code holds a vendor key |
| [021 Evaluating before release](docs/adrs/021-evaluating-ai-before-release.md) | A CI gate per tier, with grounding checks and a human audit that relaxes only after three clean releases |
| [022 Detecting misbehaviour](docs/adrs/022-detecting-ai-misbehaviour.md) | A rolling fourteen-day disposition rate against the release baseline, and automatic rollback for generative capabilities |
| [023 Cost control](docs/adrs/023-ai-cost-control.md) | Cost per thousand visitors, a declared ceiling per capability, and a ladder that degrades rather than switches off |
| [10 Model gateway](docs/diagrams/10-model-gateway.md) · [11 Evaluation and drift loop](docs/diagrams/11-evaluation-loop.md) | Both, drawn |
| [Implementation](docs/implementation.md) | Golden set format, the CI gate, the cost formula, the degradation ladder as code |
| [03 AI capability map](docs/diagrams/03-ai-capability-map.md) | Every capability, its tier and its authority |

Here is where the earlier chapters pay off. **Every model in this system is checked by something
that is not a model.** The camera's fish count against the keeper's typed number. The visitor
movement inference against the gate count. The welfare model against what a keeper found when
they walked out to look. The keeper's disposition from chapter 5 is generalised into the primary
drift signal for every capability in the estate.

None of those checks were built for this purpose. They are the ordinary business of running an
estate, which is what makes them affordable to run forever.

Every fallback bottoms out somewhere that depends on no provider at all: a static FAQ tree, a
raw filter interface, a vet's fixed limit. A provider disappearing degrades the estate to a
state it already had, rather than to nothing.

Cost gets the same treatment. Measured per thousand visitors rather than per month, because a
capability that is affordable at 5,000 visitors a day and ruinous at 15,000 has failed at
exactly the moment the estate succeeds.

<p align="right"><a href="#von-digitalis-estates">↑ Back to top</a></p>

<p align="center">❦</p>

## 11 · Turning it into money

Everything so far measures the estate. None of it pays for the estate.

| Read | What it settles |
|---|---|
| [060 to 064](docs/adrs/README.md) | Ride condition, demand and pricing, visitor concierge, operations copilot, retention |

The rides are 18th-century and historically important, so their condition is inferred rather
than instrumented invasively. The rest turns measurements from the earlier chapters into
decisions the Countess can act on: what to charge, where to deploy staff, what to tell a visitor
standing in front of an empty enclosure, and how to get them to come back.

<p align="right"><a href="#von-digitalis-estates">↑ Back to top</a></p>

<p align="center">❦</p>

## 12 · Standing back

| Read | What it settles |
|---|---|
| [00 Decision map](docs/diagrams/00-decision-map.md) | Every record, every dependency, and the four chains that run through them |
| [Overview](docs/overview.md) | The short narrative of how the team used AI to solve the Countess's problems |

Three ideas recur often enough to be the architecture rather than features of it. Models advise
and people decide. Every model is checked by something that is not a model. And the evidence for
both is produced by work somebody was doing anyway.

<p align="right"><a href="#von-digitalis-estates">↑ Back to top</a></p>

<p align="center">❦</p>

## Where each requirement is answered

| Criterion | Chapters |
|---|---|
| Innovative use of AI in solutions | [7](#7--counting-what-cannot-be-seen), [8](#8--counting-people-without-knowing-them), [9](#9--all-of-this-leaves-a-record) |
| Suitability of the solution given the constraints | [2](#2--why-it-is-harder-than-it-sounds), [4](#4--an-estate-that-cannot-hear-itself), [10](#10--who-watches-the-models) |
| Appropriate levels of detail | Every record carries trade-offs, assumptions and open questions. [Implementation](docs/implementation.md) goes to code level |
| Dealing with uncertainty in AI technology | [3](#3--deciding-the-shape-first), [5](#5--now-it-can-hear-what-may-it-do), [10](#10--who-watches-the-models) |
| Architectural characteristics match the existing architecture | [4](#4--an-estate-that-cannot-hear-itself), [6](#6--take-the-connection-away) |
| Validation and verification of AI results | [7](#7--counting-what-cannot-be-seen), [10](#10--who-watches-the-models) |

## Deliverables

| Deliverable | Where |
|---|---|
| Overview | [docs/overview.md](docs/overview.md) |
| Diagrams | [docs/diagrams/](docs/diagrams/README.md) |
| ADRs with trade-off analysis | [docs/adrs/](docs/adrs/README.md) |
| Implementation details | [docs/implementation.md](docs/implementation.md) |
| Five-minute video (semi-finalists) | link to be added |

## Key dates

| Milestone | Deadline |
|---|---|
| **Solution due in this repo** | **Wed 16 Sept, 11:59pm ET** |
| Semifinalists announced | Mon 5 Oct |
| Semifinalist video due | Mon 12 Oct, 11:59pm ET |
| Winners announced | Wed 21 Oct |

## Working in this repo

[CONTRIBUTING.md](CONTRIBUTING.md) · New teammate? [ONBOARDING.md](ONBOARDING.md) ·
Full brief: [docs/kata-brief.pdf](docs/kata-brief.pdf)

<p align="right"><a href="#von-digitalis-estates">↑ Back to top</a></p>
