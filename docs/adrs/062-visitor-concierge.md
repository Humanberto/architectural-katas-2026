# 062. Visitor concierge

## Status

Proposed — Context drafted by A, Decision belongs to D

## Context

Few visitors return, and the estate does not understand how to change that (P4, R10).
The mechanism is not mysterious: a visitor who had a well-paced day, saw the animals
being fed, and did not queue twice comes back. One who missed the feeding and queued
twice does not.

A conversational planner in a visitor app is a plausible answer, and it is one of only
two places in this system where the interface genuinely is open-ended natural language.
Under [011](011-ai-determinism-tiers.md) that makes it a Tier 3 capability, which means
choosing it requires justification in this record — what the Tier 1 version would have
been, and why a static map with opening times is insufficient.

The constraint that dominates the design is C1: wifi coverage across the park is patchy.
A concierge that needs connectivity to tell someone where the toilets are will be
useless in exactly the far paddocks where someone is most lost. R15 requires the estate
to keep operating while disconnected, and that applies to visitor-facing software too.

Questions D will want to settle:

- What is cached, and when? Caching the map, the content pack and the day's itinerary at
  gate entry — over the good connection at the gate — is the obvious move.
- What still works with no signal, and how is the absence shown? A spinner that never
  resolves is worse than a message saying live queue times are unavailable.
- What grounds the answers? Ride details, height restrictions, feeding times,
  accessibility routes, and live queue estimates from C's presence sensing.
- What happens when it does not know? "Ask a member of staff" is a correct answer and
  the system should prefer it to a plausible invention.
- How is it verified, given no external ground truth? A golden question set with
  human-graded reference answers, plus grounding checks, is the likely shape — coordinate
  with [021](021-evaluating-ai-before-release.md) rather than inventing a parallel scheme.
- What does it cost per thousand visitors, and what does it degrade to when the budget
  breaker trips? See [023](023-ai-cost-control.md).

Note that nothing here may take an action. Under 011 rule 2 a generative capability
advises; it does not book, buy, or admit.

Alternatives worth considering and rejecting explicitly: a native app rather than a
progressive web app; a purely server-rendered chat with no offline cache; and a static
map and timetable with no conversational element at all.

## Decision

_To be written by D._

## Consequences

_To be written by D._
