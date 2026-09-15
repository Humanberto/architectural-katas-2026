# 021. Evaluating AI before release

## Status

Accepted

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

**No capability, and no new model or prompt version of an existing capability, may
become active in [020](020-model-gateway.md)'s gateway without passing a release gate
appropriate to its tier.** The gate runs in CI, produces a pass/fail with no
interpretation required, and blocks the merge or the config change if it fails — this
is the only design that survives C13, because anything requiring judgement to read has
no one here to read it.

**Tier 1 gate.** A held-out test set and a numeric accuracy threshold. The number
belongs to the capability's owning ADR (043 for welfare, 060/061/064 for D's range);
this record's contribution is that the threshold must be a number checked in CI, not a
number in a document nobody re-runs.

**Tier 2 gate.** A golden set of at least 100 labelled examples reconciled against the
capability's named independent physical ground truth — a stock ledger for the piranha
count, gate admissions for zone counting, an inspection outcome for ride condition. Pass
criterion is a mean-absolute-error bound set by the owning ADR. The gate re-runs on
every model change and on every material sensor or firmware change, because either can
move the error without moving the code.

**Tier 3 gate — this is the one B owns most directly, because concierge and copilot have
no natural held-out set.**

1. A golden set of at least 50 scenarios per capability, written by a person, split into
   three kinds: representative questions (the forty-or-so things visitors actually ask),
   edge cases, and known-bad prompts the capability must refuse or must not answer from
   invented facts.
2. A grounding check runs on every golden-set answer and every production answer alike:
   any factual claim (price, opening time, safety rule) must be traceable to an approved
   source document the gateway retrieved for that call. An answer with an untraceable
   factual claim fails automatically, with no judgement call involved — this is a
   programmatic check, not a reviewer's opinion.
3. A model grading another model's output is acceptable as a first pass, because it is
   cheap and catches the obvious failures, but it is not sufficient evidence on its own.
   A human audits 100% of golden-set answers before a capability's first release, and a
   sampled 20% of the golden set on every release after three consecutive releases with
   no audit failure. A failure found in the sample resets the audit rate to 100% for the
   next release.
4. **A prompt change is a release.** It re-runs the full gate, with no smaller check for
   "just wording." Wording is the mechanism by which grounding and refusal behaviour
   break.
5. A capability with no available ground truth and no retrievable grounding source is
   not eligible to ship — "cannot be evaluated" is grounds for not shipping it, not
   grounds for shipping it with a lighter check. Both of B's Tier 3 capabilities have a
   grounding source (the estate's own FAQ and pricing data, the operations data the
   copilot queries), so neither is expected to hit this case; if a future generative
   capability has neither, it belongs in Tier 2 or does not ship.

Two alternatives were rejected beyond manual spot-checking, which the context already
raises as insufficient for the reason ordinary testing usually is: it does not run
automatically, so it does not run reliably.

**A. Relying on provider-published benchmarks.** Rejected because a benchmark measures
the model in general, on someone else's questions; it says nothing about whether our
grounding sources are wired up correctly or whether our specific prompt causes
hallucination on our specific edge cases. It is evidence about the model, not evidence
about the capability.

**B. Shipping without a gate and relying entirely on production monitoring.** Rejected
because it conflates this record with [022](022-detecting-ai-misbehaviour.md), and
production monitoring is necessarily reactive — the first evidence of a bad release
would be a visitor receiving a wrong answer, which is exactly what R13 asks us to catch
before it reaches them, not after.

## Consequences

### Positive

- The gate is mechanical and generalist-operable, which C13 requires: pass or fail, no
  ML expertise needed to read the result.
- Grounding checks give the concierge a hard, checkable answer to "did it make something
  up," independent of how fluent the answer reads.
- Treating a prompt edit as a full release closes the most common way evaluation gates
  get quietly bypassed in practice.
- The audit-rate ramp (100% → 20% after three clean releases) gives a stable capability
  a lighter ongoing cost without ever removing human oversight entirely.

### Negative

- Building and maintaining three golden sets (welfare, population/condition, two Tier 3
  capabilities) is real ongoing work for a four-person team; it is front-loaded exactly
  when the team is also building the capabilities themselves.
- The 100-example minimum for Tier 2 and 50-scenario minimum for Tier 3 are our numbers,
  not the brief's — chosen as the smallest set we believe says something, and worth
  revisiting once real question logs exist.
- A capability that fails 5 and cannot get a grounding source built in time does not
  ship at all; this is a real product cost, not a hypothetical one, if the copilot's
  query layer turns out to be harder to ground than expected.

### Assumptions

- Someone on the team writes the first golden set by hand; there is no existing question
  log to mine it from, because the estate has no digital operation today (P8, P7).
- The model-grading-a-model step is cheap enough to run on every release without
  becoming a cost problem in its own right; if it is not, [023](023-ai-cost-control.md)
  should account for it explicitly.

## Related

- Diagram: [10 — Evaluation and drift loop](../diagrams/10-evaluation-loop.md)
- Implementation: [Evaluation](../implementation.md#evaluation-b)
- [020](020-model-gateway.md) is what this gate promotes a version into
- [022](022-detecting-ai-misbehaviour.md) covers the same capability after release
