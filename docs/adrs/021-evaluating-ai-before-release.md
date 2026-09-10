# 021. Evaluating AI before release

## Status

Proposed — Context drafted by A, Decision belongs to B

## Context

The brief asks us to validate and verify AI results (R13). Verifying deterministic
software is routine; the difficulty is that generative behaviour is non-deterministic
(C12), so "run it twice and compare" does not establish correctness.

[011](011-ai-determinism-tiers.md) splits our capabilities into three tiers, and each
tier admits a different kind of evidence:

- Tier 1, classical and reproducible. A held-out set and an accuracy threshold. This is
  ordinary testing and needs little invention.
- Tier 2, perceptual. Non-deterministic in value, bounded in shape, and — critically —
  usually has an independent physical ground truth available: a stock ledger, a turnstile
  count, an inspection, a vet's score.
- Tier 3, generative. Non-deterministic in both value and shape, and frequently with no
  external ground truth at all.

This record covers what has to be true before an AI capability is allowed to ship.
[022](022-detecting-ai-misbehaviour.md) covers what happens after it has shipped.

Questions B will want to settle:

- What does a golden set look like per tier, who builds it, and how large does it need
  to be to mean anything?
- What is the numeric gate for each capability, and who sets it? A threshold nobody
  agreed is a threshold nobody enforces.
- For Tier 3, is a model grading another model's output acceptable evidence, and if so
  what fraction gets human-audited?
- Is a prompt change a release? If prompts are versioned artefacts, does changing one
  re-run the gate?
- What is the minimum bar for a capability with no available ground truth — and is
  "cannot be evaluated" grounds for not shipping it?

Note the constraint that shapes all of this: there is no ML team here (C13). Whatever is
designed has to be runnable by a generalist, in CI, without interpretation.

Alternatives worth considering and rejecting explicitly: manual spot-checking before
release; relying on provider-published benchmarks; and shipping without a gate and
relying entirely on production monitoring.

## Decision

_To be written by B._

## Consequences

_To be written by B._
