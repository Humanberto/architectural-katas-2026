# 020. Model gateway and provider abstraction

## Status

Proposed — Context drafted by A, Decision belongs to B

## Context

The brief requires that we survive a model or provider changing, repricing, or shutting
down (R14), and tells us that models and providers change fast, including pricing and
availability (C11). This is a family estate with a small operations staff and no
in-house ML team (C13), and no budget beyond the funded MQTT hardware baseline (C14).

The problem is coupling. If business logic calls a vendor SDK directly, then a provider
change is a code change in every place that calls it, a price rise is discovered on the
invoice, and a shutdown is an outage. None of those are recoverable in a week by a team
this size.

[011](011-ai-determinism-tiers.md) limits our exposure by keeping most capabilities in
Tier 1 and Tier 2, which run on the estate and depend on no provider at all. This record
covers what to do about the remainder, where an external model genuinely is the right
answer.

Three scenarios need answering distinctly, and the brief names all three:

- A better model appears. How do we adopt it without rewriting anything?
- A provider raises prices. How do we find out quickly, and what happens then?
- A provider shuts down. What still works?

Questions B will want to settle:

- What is the unit of abstraction — a capability name such as "answer visitor question",
  or a thinner wrapper over a chat completion?
- Where do prompts and model choices live, and are they versioned artefacts subject to
  the same release process as code?
- Is there a self-hosted fallback per capability, and do we know what quality it gives
  us, or are we guessing?
- How is a candidate model evaluated against the incumbent — offline against a fixed
  set, shadowed against live traffic, or both?
- Who can switch the active model, and is that a deployment or a configuration change?

Alternatives worth considering and rejecting explicitly: calling vendor SDKs directly
and accepting the coupling; adopting a third-party gateway or router product; and
committing to a single provider deliberately in exchange for simplicity.

## Decision

_To be written by B._

## Consequences

_To be written by B._
