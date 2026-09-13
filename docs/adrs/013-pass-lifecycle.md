# 013. Pass lifecycle: amendment, revocation, and key rotation

## Status

Proposed

## Context

[012](012-admissions-and-ticketing.md) decided that a pass is a cryptographically signed
token, verifiable at a gate with no network at all, and that scanners hold a cached
revocation list. It then listed three things it did not resolve, and this record resolves
them.

- Passes cannot be amended after issue, because the entitlement travels in the token.
- Key rotation is "an operational responsibility", with a compromised key implying reissue
  of every outstanding pass.
- The revocation list stays distributable only "while refunds are a small fraction of
  sales" — an assumption with nothing holding it up.

All three are lifecycle problems. A pass is a bearer token: once issued it is outside our
control until somebody presents it at a gate, and everything that happens to it in between
— a family adds a child, a card is refunded, a phone is lost, a signing key leaks, the
season ends — has to be handled without assuming the gate can ask anyone anything.

The commercial frame from 012 has not changed. Given the estate's difficulty attracting
returning visitors (P4, R10), a queue at the entrance costs far more than the fraud it
prevents. Every decision below resolves in favour of admitting the visitor.

### Sizing the problem

At the three-year target of 15,000 visitors a day (C8, C9) and an assumed average party of
2.5, the estate issues roughly 6,000 passes a day. These are the numbers the rest of this
record argues against.

| Quantity | Figure | Basis |
|---|---|---|
| Passes issued per day at target | ~6,000 | 15,000 visitors (C8) ÷ 2.5 per party |
| Revocation rate | 3% of sales | Assumed. Refunds, reported losses, fraud |
| Revocations per day | ~180 | 6,000 × 3% |
| Revoked passes valid on any one day | ~1,300 | 180/day across a 7-day multi-day window |
| Outstanding annual passes revoked | ~60 | Assumed 2,000 annual passes at 3% |

### Three alternatives were considered

**A. Allowlist distribution.** Push every pass valid today to every scanner and deny
anything absent from it. Genuinely attractive: it is positive verification rather than
negative, it needs no signature scheme at all, and a forged token cannot pass because it is
not on the list. Rejected on size and on timing. The list is ~6,000 entries a day rather
than ~1,300, and worse, it churns — every same-day walk-up sale invalidates it, and that
visitor is denied at the gate until their purchase propagates to the scanner they happen to
walk up to. The deny list is small precisely because revocations are rare; an allowlist is
large precisely because sales are not, and it fails in the direction that turns customers
away.

**B. Short-lived tokens refreshed by the visitor's phone.** The airline boarding-pass
pattern. A token valid for minutes makes revocation almost unnecessary, because anything
revoked expires before it matters. Rejected because it relocates the connectivity
dependency onto the one component we do not control. A family arriving at a rural estate
with patchy coverage (C1) and a flat battery cannot refresh, and the failure lands at the
gate anyway — but now we cannot fix it. It also excludes printed passes, which a family
estate selling to families needs.

**C. Server-side pass state with an offline cache.** Scanners query the admissions service
and fall back to a local cache when it is unreachable. Rejected because the cache *is* the
offline path: we would build both, and the online path would mask defects in the offline
one until the day connectivity failed and the untested path carried the whole gate. 012
rejected online-only validation on the same ground.

## Decision

The states and transitions below are drawn in
[09 Pass lifecycle](../diagrams/09-pass-lifecycle.md).

### Re-entry is allowed, so a pass has no consumed state

A day pass admits its party for the day, including re-entry. There is no "spent" or
"consumed" state to track.

This is a business rule bought deliberately for an architectural simplification, and it is
the largest one available here. Consumption is the one piece of pass state that changes at
the gate rather than at purchase, which makes it the one piece that cannot be established
offline. Removing it means the deny list is the *only* shared state a scanner needs, and
everything else in the token is fixed at issue.

It also largely dissolves the bounded re-use window that 012 accepted as a negative. What
remains is not sequential re-use but concurrent use — two different parties presenting the
same pass at two gates at once — which is bounded by the party size carried in the token
and by gates being physically supervised during opening hours (012's own assumption).

### The deny list is scoped to passes valid today

A scanner holds revoked passes whose validity window includes the current date, not every
pass ever revoked. The list self-prunes at midnight.

| Approach | Entries | Size at 17 bytes/entry | Growth |
|---|---|---|---|
| Valid-today, as decided | ~1,300 | ~22 KB | Bounded, self-pruning |
| All-time, over the C9 horizon | ~197,000 | ~3.4 MB | Unbounded, no pruning point |

Twenty-two kilobytes refreshes over patchy wifi (C1) in a single request. This turns 012's
assumption into a property of the design: the list is small because of how it is scoped,
not because we are hoping refunds stay rare. Even a tenfold rise in the revocation rate
leaves it under a quarter of a megabyte.

Revoked annual passes are the one entry class that persists, staying on the list for the
remainder of their window — roughly 60 entries, which does not move the total.

Scanners refresh every 60 seconds when connected, and opportunistically otherwise.

### The deny list carries two classes, not one

| Class | Cause | Gate behaviour |
|---|---|---|
| `revoked` | Refund, reported loss, downgrade amendment, suspected fraud | Deny. Refer to the gate desk. |
| `superseded` | Upgrade amendment — the party or entitlement grew | **Admit at the entitlement in the presented token.** Flag for reconciliation. |

The distinction exists for one scenario, which is common and otherwise handled badly. A
family amends a booking to add a child, pays for it, and arrives holding a screenshot of
the original QR code. Under a single deny class they are turned away at the gate for a
change they paid us to make.

Admitting them at the *old* entitlement is never worse for the estate than what they have
already bought, and it is strictly better than a queue and an argument. The gate desk
resolves the difference; the reconciliation flag means nobody has to notice it manually.

Downgrades are the mirror case and must be hard revocations. A family that dropped a member
and took a partial refund would otherwise present the superseded token and be admitted for
five having paid for four.

### Amendment is revoke-and-reissue in one transaction

There is no in-place edit of an issued pass. An amendment revokes the old pass identifier,
issues a new signed token, and writes both the deny-list entry and the new pass in a single
database transaction. This is precisely the invariant 012's modular monolith exists to make
cheap, and it is why amendment does not need compensating logic.

### Signing keys are identified in the token, and rotation is routine

Each token header carries a key identifier. A scanner trusts a **set** of public keys, not
one.

- Rotation is annual and scheduled. New passes are signed with the new key immediately.
- The previous public key stays trusted until the longest-lived pass signed with it expires
  — thirteen months for an annual pass.
- A scanner therefore holds at most three public keys, at 32 bytes each.

This removes 012's rotation problem entirely. There is no flag day, no redistribution race,
and no reissue of outstanding passes for a routine rotation. Ed25519 gives a 64-byte
signature and a 32-byte public key, keeping the whole pass payload near 200 bytes — small
enough for a mid-range QR symbol at medium error correction, and verifiable on scanner
hardware in well under a millisecond.

Compromise remains the expensive case. A leaked private key means dropping that key
identifier from the trusted set and reissuing every pass signed with it. We have made
rotation routine; we have not made compromise cheap, and we are not claiming to.

### Gates are wired. Offline is the degraded mode, not the resting state

C1 says wifi coverage *across the park* is patchy, and it is — 55 enclosures and 40 rides
(C4, C5) are spread across an estate where running cable to every point is exactly the
impractical thing that made MQTT the answer in [040](040-connectivity-topology.md).

Gates are not that. They are a small number of fixed buildings on the perimeter, and they
are the single highest-value place on the estate to buy reliable connectivity. Wiring them
properly is conventional capital work against a handful of known locations.

So the normal case is a deny list seconds old, and 012's offline gate is what happens when
that fails. This does not weaken 012 — its requirement stands in full, and the offline path
is built, tested and used. It changes only what we call normal, and therefore how stale we
should expect the deny list to be when it matters.

This is a spend beyond the MQTT-capable baseline, which C14 requires us to argue for rather
than assume. The argument is above; the cost is in the Negative section.

### Staleness never stops the gate

| Deny list age | Behaviour |
|---|---|
| Under 4 hours | Normal operation |
| Over 4 hours | Continue admitting. Mark every admission `unverified-revocation`. Alert operations. |

There is no threshold at which a scanner stops admitting visitors. The exposure of
honouring a revoked day pass is tens of pounds; the exposure of a stopped gate on a
Saturday is the queue 012 was written to prevent. Reconciliation catches what the gate let
through, and repeat offenders stay a commercial matter rather than an architectural one.

### Scan and lifecycle events

Every scan is already forwarded on the satellite broker's queue per
[040](040-connectivity-topology.md) and [042](042-telemetry-model.md). Lifecycle
transitions — issue, amend, revoke, supersede — originate in the admissions monolith and
are not gate events. They reach the deny list by the refresh path above, and reach
analytics through the estate API path that 042 reserves for transactional systems.

## Out of scope

- Payment authorisation and card handling. External provider, per 012. We store no card
  data.
- Pricing, discounting and the purchase funnel. Seat D's range.
- Reconciliation of admission events into popularity and conversion measures (R3, R4).
  012 establishes admission events as the denominator; the analysis is elsewhere.
- Key custody mechanics — HSM versus software keystore — which is an implementation choice,
  not an architectural one.
- Visitor identity and personal data retention. Nothing here requires a pass to name anyone.

## Consequences

### Positive

- The deny list is the only shared state a gate needs, and it is ~22 KB. Everything else a
  scanner must know is in the token or in its trusted key set.
- Routine key rotation costs nothing operationally, which matters given a small operations
  staff (C13).
- A customer who paid for an upgrade is never turned away at the gate for holding the old
  token.
- The revocation-list size argument now survives growth to 15,000 visitors a day (C8) by
  construction rather than by assumption.
- Amendment correctness is a single database transaction, consistent with 010 and 012.
- Still no AI anywhere in this record, which remains the correct answer for entitlements
  and consistent with [011](011-ai-determinism-tiers.md).

### Negative

- Wiring the gates is capital spend outside the funded baseline (C3, C14). It is a handful
  of fixed locations rather than park-wide coverage, but nobody has itemised it and the
  estate has to agree to it.
- Two deny-list classes is more logic on cheap scanner hardware than one, and the
  `superseded` path is the one least likely to be exercised in testing.
- An upgrade admitted at the old entitlement creates manual work at the gate desk. We have
  moved a bad experience rather than removed it.
- Re-entry is asserted as a business rule. If the estate wants single-entry day passes,
  consumption state returns and most of this record's simplification goes with it.
- Key compromise still requires reissuing every outstanding pass signed with that key.
- Multi-day and annual passes keep entries on the deny list for the length of their window,
  so the list's floor rises as the estate sells more of them.
- A pass presented between revocation and the next scanner refresh is admitted. Under
  wired gates that window is seconds; under the degraded path it is up to the staleness
  threshold.

### Assumptions

- Average party size is 2.5 and the revocation rate is around 3% of sales. Both are
  estimates, and both should be replaced with the estate's own figures once it has any.
  The size conclusion tolerates an order of magnitude of error in either.
- Gates are a small enough number of fixed perimeter buildings that wiring them is
  conventional work. The gate count is not in the brief and needs confirming.
- Re-entry on a day pass is commercially acceptable. This is the estate's decision, not
  ours, and the architecture changes materially if the answer is no.
- Scanner hardware can hold a few hundred kilobytes, run Ed25519 verification, and is
  physically supervised during opening hours — carried forward from 012.
- Annual passes exist as a product. If they do not, the persistent tail of the deny list
  disappears and every number here improves.
