# 060. Ride condition monitoring

## Status

Proposed — Context drafted by A, Decision belongs to D

## Context

There are forty rides (C4). They are 18th-century and historically important, so
physical modification is limited (C7). They have only just passed inspection after the
asbestos, broken glass and garden gnomes were removed.

Two things follow. An unplanned closure costs revenue the estate cannot spare (P1, P5).
A failure in front of visitors would end the business. The rides are also the reason
many visitors come, so their availability bears directly on growth (R8) and returning
visitors (R10).

There is a hard boundary to draw here, and drawing it is the substance of this record.
[011](011-ai-determinism-tiers.md) rule 2 states that no generative output may actuate
anything, extending the principle in [043](043-welfare-loop.md) that fixed rules written
by a human may act while anything a model infers may only advise. Ride safety is the
sharpest test of that rule. Statutory inspection is a legal regime, not a technical one,
and nothing we build can substitute for it.

That leaves a real and useful job: catching degradation between inspections, and telling
maintenance where to look first.

Questions D will want to settle:

- What is actually sensed, given C7 limits what can be attached to a protected structure?
  Vibration and acoustic monitoring of drive assemblies and bearings is the obvious
  candidate, but the mounting constraint is real.
- Is a per-ride baseline learned during known-good operation, and how long is that
  learning period before the ride is in service?
- What are the severity bands, and what does each one oblige someone to do?
- Where does the boundary sit exactly — may the system recommend a closure, or only
  report a condition? Who holds the decision?
- How is the model verified? Every advisory closed out by an engineer with a finding
  gives live precision, and inspection outcomes are an independent ground truth.
- Which tier is this under 011, and does it need a model at all, or would a threshold on
  a vibration signature do?

The conservative answer is likely the right one here, and worth arguing for explicitly
rather than apologising for. A judge will respect a clearly drawn authority boundary more
than an ambitious claim about AI-managed safety.

Alternatives worth considering and rejecting explicitly: AI-gated ride opening;
scheduled maintenance only, with no sensing; and manual inspection frequency increased
instead of instrumentation.

## Decision

_To be written by D._

## Consequences

_To be written by D._
