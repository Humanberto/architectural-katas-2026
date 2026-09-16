# 062. Visitor concierge

**Go straight to:** [Home](../../README.md) · [ADRs](README.md) · [Diagrams](../diagrams/README.md) · [Implementation](../implementation.md) · [Requirements](../requirements.md) · [Characteristics](../architecture-characteristics.md) · [Brief](../kata-brief.pdf)

## Status

Proposed.

## Context

The animal collection was previously private and is being opened to the public
([P7](../requirements.md#problems)), so there is no existing public-facing operation to inherit
([P10](../requirements.md#problems)). Five thousand visitors a day, rising towards fifteen thousand
([C8](../requirements.md#constraints)), will arrive with questions, on an estate whose staff is small and has no
technology function ([C13](../requirements.md#constraints)).

A generative assistant is the obvious answer and also the one that needs the most
justification, because [011](011-ai-determinism-tiers.md) requires an argument before
anything reaches Tier 3.

The argument is that visitor questions are open-ended in a way a menu cannot cover. A
person asking whether the reptile house is worth visiting with a nervous six-year-old is
not selecting from a list. That is what generative text is genuinely good at.

There is one category where it is not good enough, and the collection makes it sharp:
some of these animals are poisonous ([C6](../requirements.md#constraints)).

## Decision

**The concierge is Tier 3, and it advises only.** It answers questions and points at
things. It does not take bookings, change tickets, open anything, or tell anyone what is
safe.

**Safety questions are refused and handed to a person.** Anything touching proximity,
handling, allergy, venom, or what to do if something happens is answered with where to
find a keeper, not with an answer. This is enforced as a refusal case in
[021](021-evaluating-ai-before-release.md)'s golden set, so a release that starts
answering them fails its gate rather than reaching a visitor.

**Every factual claim is grounded or it is not said.** Opening times, prices, feeding
times, height restrictions and directions must trace to an approved source document the
gateway retrieved for that call, per [021](021-evaluating-ai-before-release.md)'s
grounding check. An answer with an untraceable fact fails automatically, which needs no
judgement call and therefore survives [C13](../requirements.md#constraints).

**It runs through the gateway, like everything else in Tier 3.** Model choice, prompt
version, fallbacks and the call log are [020](020-model-gateway.md)'s. The cost ceiling
and the degradation ladder are [023](023-ai-cost-control.md)'s. This record adds no
infrastructure of its own.

**When the link to the cloud is down, the concierge degrades rather than disappears.**
The static FAQ tree named in [020](020-model-gateway.md) runs on the estate and depends
on no provider, which is the same guarantee [044](044-disconnected-operation.md) gives
everything else on site. A visitor gets a worse answer, never an error page.

**It never sees who is asking.** No account, no history, no profile. Partly because
[045](045-presence-and-flow.md) makes identity impossible by construction, and partly
because a visitor asking a question in a park should not be creating a record.

## Consequences

| Decision | Cost |
|---|---|
| Refusing safety questions | The most urgent questions get the least helpful answer. Correct, and it must be designed to hand off well rather than just decline |
| Grounding required for every fact | Somebody has to write and maintain the source documents, and an ungrounded question gets no answer at all |
| No memory of the visitor | Each question starts cold, so follow-ups are weaker than they could be |
| Static fallback offline | Two versions of the answers to keep in step, and the fallback will be stale unless somebody owns it |

### What this provides

- An answer to questions a menu cannot anticipate, at a volume no small staff could cover
- A hard, checkable answer to "did it make that up", independent of how fluent it reads
- No new failure mode when the network drops, and no provider dependency at the bottom
  of the stack

## Alternatives rejected

| Option | Why not |
|---|---|
| A scripted FAQ chatbot only | Handles the questions we anticipated, which are the ones a printed sign already answers |
| Letting it answer safety questions with a strong disclaimer | A confident wrong answer about a venomous animal is the failure this whole repository is built to avoid. A disclaimer is not a control |
| Letting it take bookings and amend tickets | Puts a non-deterministic component in front of money and admission, which [012](012-admissions-and-ticketing.md) and [013](013-pass-lifecycle.md) deliberately keep deterministic |
| Personalising answers from visitor history | Requires an identity the architecture does not have, and should not acquire for this |

## Assumptions

- Visitor questions repeat enough that caching carries most of the traffic. This is our
  assumption rather than the brief's, and [023](023-ai-cost-control.md)'s cost per
  thousand visitors will confirm or kill it within weeks
- Somebody at the estate owns the source documents the answers are grounded in. Without
  an owner the grounding check passes against stale facts, which is worse than failing

## Open questions

- Where the concierge lives — a page on a phone, a screen at the entrance, or both — and
  whether the offline fallback differs between them
- Which languages, and whether grounding sources must exist in each
- Whether a refused safety question should also alert a keeper that somebody asked

## Related

- **[011](011-ai-determinism-tiers.md)** requires the justification this record gives
- **[020](020-model-gateway.md)** provides the gateway, the fallbacks and the call log
- **[021](021-evaluating-ai-before-release.md)** holds the golden set, the refusal cases and the grounding check
- **[022](022-detecting-ai-misbehaviour.md)** watches it after release
- **[023](023-ai-cost-control.md)** sets the ceiling and the degradation ladder
- **[044](044-disconnected-operation.md)** is why the static fallback exists
- **[045](045-presence-and-flow.md)** is why there is no visitor to personalise for
- Diagram: [08 Concierge offline behaviour](../diagrams/08-concierge-offline.md)
- Diagram: [03 AI capability map](../diagrams/03-ai-capability-map.md)

---

<p align="center">❦</p>

<p align="right"><a href="#062-visitor-concierge">↑ Back to top</a> · <a href="../../README.md">Home</a> · <a href="README.md">All ADRs</a> · <a href="../diagrams/README.md">All diagrams</a></p>
