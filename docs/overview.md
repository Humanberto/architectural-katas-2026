# Overview

## The problem in one paragraph

The Von Digitalis estates are unprofitable, the garden gnome business is gone, and visitor
numbers must roughly triple within three years or the carnivorous plants are sold (P1, P5,
C8). The Countess needs four things: a way to sell and check tickets, an understanding of
which parts of the estate people actually visit, confidence that 200-odd exotic animals
across 55 enclosures are well, and more visitors who come back (R1, R3, R5, R10). She has
patchy wifi, Victorian conduit, one internal IT person, and a budget that covers MQTT
hardware and not much else (C1, C13, C14).

## Our approach

**We treat the estate as the source of truth, and the cloud as somewhere data eventually
arrives.** That single choice shapes everything else. Sensors report over LoRaWAN to
satellite brokers spread across the park; cameras and controlled equipment use wifi; all of
it converges on one machine on the estate that runs the broker and the estate server
([040](adrs/040-connectivity-topology.md), [041](adrs/041-hybrid-transport.md),
[042](adrs/042-telemetry-model.md)). When the uplink drops — which is a normal Tuesday, not
an outage — the estate keeps recording, keeps alarming, and keeps the vet's limits running.
On reconnection the records merge, and anything that disagrees goes to a person rather than
being resolved quietly ([044](adrs/044-disconnected-operation.md)).

**Admission is the one part with no AI in it, and it works with no network at all.** Passes
are signed tokens a gate can verify against a locally cached key, with a small deny list for
refunds and losses. A scan changes no state, so re-entry is free and there is nothing for a
gate to look up. We accept a short window in which a pass could be presented twice, because
the alternative is gates that stop working on the one Saturday the estate cannot afford a
queue ([012](adrs/012-admissions-and-ticketing.md),
[013](adrs/013-pass-lifecycle.md)).

**Everything else is conventional on purpose.** There is one event backbone, one relational
database, one deployable for transactions. Fifteen thousand visitors a day is about one
admission per second. This is a small system, and designing it as a large one would be the
surest way to build something the estate cannot operate
([010](adrs/010-architecture-style.md)).

The full picture is in the [container view](diagrams/02-container-view.md). What we chose to
optimise for, and what we deliberately gave up, is in
[architectural characteristics](architecture-characteristics.md).

## Where AI is used

Most of the Countess's problems are measurement and forecasting problems. Is this reading
abnormal for this species at this time of year. How many fish are there. How busy will
Saturday be. Which enclosure does nobody stop at. Those are statistics questions, and a
language model would answer them more slowly, less reproducibly and less accurately than a
well-chosen classical one.

So we sorted every use of AI into three tiers and committed to using the lowest one that
works ([011](adrs/011-ai-determinism-tiers.md)). Reaching for a language model is the
exception that needs justifying in its own record; choosing a classical model needs no
justification at all. The result is that most of the AI here runs on the estate, costs
nothing per call, and keeps working when the network does not.

- **Welfare.** A vet sets the safe range for each species. Fixed limits may switch equipment
  on by themselves; anything a model infers may only raise an alert for a keeper. Feed
  weights, enclosure conditions and equipment state are recorded on one clock so the
  question "do animals behave differently on busy days" becomes answerable later
  ([043](adrs/043-welfare-loop.md), [047](adrs/047-environment-and-weather.md)).
- **Counting the piranhas.** A camera publishes a count, its confidence and its model
  version. A keeper, during a round they already do, types in what they saw. The keeper's
  number is the record; the camera's is an estimate. When they disagree we investigate, and
  we do not assume which is wrong ([046](adrs/046-count-reconciliation.md)).
- **Where people go.** Counters that are physically incapable of identifying anyone — beam
  break, thermal, time of flight — report integers over LoRaWAN. Daily ticket validations
  calibrate them. Route and dwell are published as inferences and drawn as inferences
  ([045](adrs/045-presence-and-flow.md), [diagram 06](diagrams/06-presence-and-flow.md)).
- **Visitors and revenue.** Demand forecasting, ride condition monitoring, a concierge that
  caches its content at the gate, an operations copilot, and retention modelling (060 to
  064).

The [AI capability map](diagrams/03-ai-capability-map.md) shows all of it at once, by tier
and by what each is allowed to do.

## How we deal with AI uncertainty

Models and providers change fast, and the estate cannot absorb a surprise (C11, C14). Our
main defence is structural rather than clever: only two capabilities use a hosted language
model at all. Everything else runs on hardware already paid for. A provider tripling its
price or shutting down costs the Countess two features — not her revenue, and not her
animals.

For the two that remain, business logic asks for a capability by name rather than naming a
vendor, so adopting a better model is an evaluation exercise and not a rewrite, and every
capability declares what it costs and what it degrades to when that ceiling is reached
(020, 023).

## How we validate that the AI works

Wherever an independent physical record exists, we reconcile against it and publish the
disagreement rather than hiding it.

| The model says | Checked against |
|---|---|
| How many piranhas | A keeper's typed count from a round they already do |
| How many people passed a point | Daily ticket validations at the gate |
| This animal may be unwell | The keeper's disposition when they close the alert |
| This ride needs attention | The engineer's finding, and the statutory inspection |

Three of those cost nothing extra, because the human was going to act on the output anyway.
Closing an alert has to happen; recording whether it was real is one extra tap, and it is
the only honest evidence we will ever have of what a sick animal looks like on this estate.

Nothing non-deterministic holds authority over safety or money. No model opens a ride, moves
money, or overrules a person.

## What we have not settled

- The hardware rollout across 55 enclosures and 40 rides is the largest capital number in
  this proposal and we have not costed it. It is the item most likely to change the phasing.
- The nine capabilities are not all first-season work. Admission, presence and welfare come
  first, and they contain no generative AI at all — so the estate's revenue and its animals
  do not depend on any external provider from day one.
- Several assumptions are marked as derived rather than stated in
  [requirements](requirements.md). They are listed there rather than buried.
