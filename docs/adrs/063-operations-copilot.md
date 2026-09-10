# 063. Estate operations copilot

## Status

Proposed — Context drafted by A, Decision belongs to D

## Context

The estate has no visibility into which areas are popular, so investment and staff
deployment are guesswork (P2), and the brief asks us not merely to measure popularity
but to turn that measurement into decisions (R4).

Once C's presence sensing and A's admissions system are running, the data exists. The
gap is that the Countess and a very small management team (C13) will not learn a
business intelligence tool, and nobody here will build and maintain thirty dashboards
for questions that change weekly.

This is the second of only two places where the interface genuinely is open-ended
natural language, making it Tier 3 under [011](011-ai-determinism-tiers.md) and
requiring justification in this record.

The interesting design problem is verification. Unlike the piranha count, there is no
physical ground truth to reconcile against — a wrong answer to "which enclosure costs
most per visitor who stops to look at it" looks exactly like a right one. A plausible
fabrication here does real damage, because someone will act on it.

Questions D will want to settle:

- Does the model query raw tables, or a governed semantic layer of defined metrics?
  The latter is more work up front and far more defensible.
- Is the connection read-only, and enforced how?
- Is the generated query shown to the user alongside the answer? Making the working
  visible turns the human into the verification step, which may be the only verification
  available.
- What happens when the question cannot be answered reliably? An explicit refusal is
  better than a confident guess, and the system should be built to prefer it.
- What does the regression suite look like — question and known-answer pairs, presumably,
  coordinated with [021](021-evaluating-ai-before-release.md).
- Who is allowed to ask? Some of this data is commercially sensitive and some concerns
  staff.

Alternatives worth considering and rejecting explicitly: text-to-SQL directly over raw
tables; a conventional BI dashboard; and a fixed set of pre-built reports with no
natural-language layer.

## Decision

_To be written by D._

## Consequences

_To be written by D._
