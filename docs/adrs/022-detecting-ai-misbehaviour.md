# 022. Detecting AI misbehaviour in production

## Status

Proposed — Context drafted by A, Decision belongs to B

## Context

The brief asks specifically for detection of AI misbehaviour once in production (R13),
not merely testing before release. This is the harder half. A model that passed its gate
in September can degrade in November without anything visibly breaking — no exception,
no error rate, just worse answers.

Three things can drift underneath us. The inputs change: a new species arrives, a ride
reopens, a heatwave falls outside anything in the training data. The model changes: a
provider updates it, or we switch it under [020](020-model-gateway.md). Or the world
changes and the model is now answering a question nobody is asking.

Two features of this system help, and B should exploit both.

The first is that a human already acts on most AI output. [043](043-welfare-loop.md)
establishes that a keeper closes every welfare alert with an outcome — real, not real,
or unclear. That disposition is a free, continuous accuracy measurement, because closing
the alert has to happen anyway. The same pattern is available wherever a person acts on
a model's suggestion.

The second is that several capabilities have an independent physical ground truth that
keeps reporting forever: admission totals from [012](012-admissions-and-ticketing.md)
against zone counts, a stock ledger against a population estimate, an inspection against
a condition advisory. Divergence between the two is a detector that needs no labels.

Questions B will want to settle:

- What is measured, at what cadence, and where does it surface? A metric nobody looks at
  is not detection.
- What are the thresholds, and what does breaching one actually do — alert someone, or
  automatically revert?
- Is rollback a configuration change at the gateway or a deployment? How long does it
  take?
- Does a new model go out to everything at once, or to a slice first?
- Who is on the receiving end of a drift alert, given C13 means there is nobody whose
  job this is?

There is a trap worth naming. It is easy to design monitoring that requires an ML
engineer to interpret. This estate does not have one and will not hire one, so any
signal that cannot be acted on by a generalist is decoration.

Alternatives worth considering and rejecting explicitly: periodic manual review rather
than continuous monitoring; relying on user complaints as the detection mechanism; and
full observability tooling that the estate cannot operate.

## Decision

_To be written by B._

## Consequences

_To be written by B._
