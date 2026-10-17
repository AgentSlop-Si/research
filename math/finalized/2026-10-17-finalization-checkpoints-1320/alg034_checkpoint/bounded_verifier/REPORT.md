# ALG-034: bounded raw-input, policy and payload binding contract

17 October 2026. Fresh standalone verification code; no production integration.

## Result

This packet advances the source-gap audit with an executable, bounded consistency verifier. It independently reads exact raw input, derives canonical state, recomputes the already accepted cyclotomic zero prepass and precision plan, and binds those results to one exact grid payload. It does not re-prove or claim new credit for the accepted numerical policy.

The fresh verifier passes 72 named controls and 300 exact-rational canonicalization/regridding cases. These are finite controls of the new checker, not execution of the accepted serial producer. All payloads used in this packet are explicitly synthetic. No historical producer, adapter, or archived module was imported or executed.

The strongest nonzero verdict is deliberately `BINDING_CONSISTENT_PRODUCER_UNVERIFIED`. Every verdict reports `authenticated_provenance=false`, `producer_execution_verified=false`, `numerical_error_certificate_verified=false`, `adapter_invoked=false`, and `downstream_integration_verified=false`. No receipt flag can change these results.

The ALG-034 owner remains TO RESEARCH, priority 48. The source-bound implementation gate remains open. No external write, release change, all-size adapter, speed claim, or downstream execution is part of this work.

## What is actually implemented

`binding_verifier.py` is freshly authored and uses only the Python standard library. It provides:

- `derive_policy(raw,state,t,q,p=None)`: full input/state checks and exact recomputation of the accepted policy. The caller may specify expected actual fractional precision p; otherwise the minimum accepted p is selected. The record cannot choose a different p behind the caller's back.
- `make_record(...)`: constructs a consistency record for a supplied payload. It is intentionally public and unauthenticated; anyone can construct one. Its existence is not evidence of producer execution.
- `verify(raw,state,t,q,record,p=None,expected_payload=None)`: checks the record against the caller's separately supplied context, then optionally compares the payload with a separately supplied exact-grid reference component by component.
- `strict_loads(text)`: bounded JSON intake rejecting duplicate keys, floats/nonfinite constants, huge decimal tokens, and invalid Unicode text. Direct API checks reject booleans in integer positions, coercible/custom numeric types, tuples in list positions, unexpected fields, and malformed nested structures.

The implementation is deliberately limited to N<=64, raw Cartesian numerator width<=1024, payload Cartesian numerator width<=8192, and supplied integer metadata and selected p width<=128. Its JSON intake limit is 4 MiB; canonical-object traversal has depth and node-count limits plus a conservative 4 MiB aggregate serialization budget, charged before encoding using worst-case Unicode escape sizes. These are new checker resource limits, not changes to the accepted theorem or adapter. A RESOURCE_LIMIT result says that this checker declined the input. It does not prove mathematical impossibility or actual failure of another implementation. No host runtime guarantee or machine-word complexity claim is made.

For a nonzero original input the checker constructs Phi_L by exact monic polynomial divisions, aggregates all phase exponents modulo L, reduces each block polynomial exactly, selects the original aggregated mass with the accepted tie break, and derives the accepted plan fields. It does not trust supplied remainders, masses, modulus, W, C, p, kappa, or radius. The entire proposed policy object must match fresh computation using canonical typed serialization. The odd-length parity term is retained, and Phi_12 is checked as X^4-X^2+1 in the controls.

The checker binds the canonical partition and cycle-to-frequency map to state. This verifies what order the payload is declared to have; it does not establish that an actual producer wrote its coordinates in that order.

## Three different meanings of identity

1. Exact original representation: the raw-input commitment hashes F and the complete ordered real/imaginary integer arrays. It identifies decoded exact data, not the original JSON document bytes. Whitespace, key order, and textual -0 versus 0 are intentionally irrelevant. If exact original transport bytes matter, a separate externally retained byte commitment is required.
2. Mathematical dyadic value: a vector m*2^scale is canonicalized by removing the common power of two from every nonzero integer component and adding it to the symbolic scale. A zero vector has scale zero. Coordinate order and length are retained. No huge power of two is materialized. Equivalent common-grid encodings have equal value commitments even when their original representation commitments differ.
3. Exact producer grid: the payload-grid commitment includes the complete integer arrays and kappa. The payload-value commitment applies the mathematical canonicalization above. An equivalent regridded payload is not accepted as the original p-grid output: kappa must be exactly W-F-p, and an external payload reference must match the grid arrays and exponent exactly.

W is always calculated on the supplied original integer arrays, before mathematical-value canonicalization. This avoids silently changing the accepted raw-width and precision contract when removing common trailing powers of two.

All hashes use SHA-256 with an explicit versioned prefix, a field-specific domain label, and deterministic typed JSON. Policy commitments include original-input, dyadic-value and canonical-state commitments. The outer binding commitment covers the full recomputed policy, payload and subordinate commitments. There is no ambiguous byte concatenation of variable-length fields.

For exact equality, the checker compares typed canonical content and, for the external payload reference, the actual arrays and scale. Digests support compact identity/corruption detection under the usual SHA-256 collision-resistance assumption. The digest is not used as a substitute for recomputing policy or comparing a supplied exact payload reference.

## Trust boundary: what hashes cannot establish

The caller supplies raw input, state, t, q, expected p, and optional expected payload separately from the record. Their provenance is outside this API. If an attacker can replace both the context and the record, they can construct a consistent replacement. A self-contained record is not authentication.

Likewise, an attacker may replace a proposed payload and recompute every digest. Such a record can pass this checker while having no demonstrated relationship to the mathematical target. The controls intentionally exercise exactly this case. The verdict still explicitly refuses producer/numerical acceptance. Supplying an independently retained exact output as `expected_payload` rejects that forged payload, but the checker cannot authenticate where the reference came from.

Even a verified digital signature would establish only an authorized party's attestation to bytes unless its signing authority and execution semantics were separately established. This packet implements no signature, key infrastructure, producer source-pin attestation, or execution monitor. A hash of source code would identify the source bytes but would not prove that those bytes ran, at the declared p, on the declared input.

## Zero branches and bounded adapter boundary

- EXACT_INPUT_ZERO follows a full scan of the original numerator arrays; W=0 is recorded as an input fact. No relative normalization or producer precision is declared.
- EXACT_PROJECTED_ZERO follows the exact recomputed cyclotomic prepass for nonzero original input. It remains distinct from original zero. This interface returns its own zero-policy record with no producer/adapter payload.
- An all-zero proposed payload on a NONZERO_PLAN branch is rejected as ZERO_APPROXIMATION, because it contradicts a genuine accepted one-shot run. It is never relabeled as either exact zero branch.

The accepted adapter has no projected-zero status. This checker never invokes it or forges its original-zero flag.

The accepted sufficient check p+I<=65536 is recorded truthfully. A control uses expected p=70000 with an actual one-bit synthetic payload to show that failure of this sufficient check is not proof of actual overwidth. That example is a data-binding control, not evidence that the payload is a genuine producer output or an eligible adapter input. The new checker's lower local payload cap does not relax or replace any existing adapter cap.

## Evidence obligations after this packet

| Obligation | What this checker establishes | What remains necessary |
| --- | --- | --- |
| Raw input and W | Exact built-in grammar, full arrays, actual W, original-zero state, original and value identities | Authenticate/fix the caller's original source and prevent substituted context across the actual run |
| Canonical state | N,B,a,beta/gcd, balanced partition, parity, intended frequency map | Establish that the producer uses those exact values/indexes |
| Zero policy and plan | Fresh exact prepass and accepted-plan recomputation, including selected actual p and symbolic scales | Review this implementation's correctness and cumulative cost for the intended deployment |
| Producer implementation | Nothing beyond the intended plan/interface | Pin actual entrypoint and dependencies; establish implementation-to-theorem correspondence or verify a separately proved, paid semantic execution trace |
| Roots and inverse square root | No enclosure is accepted or inferred | Actual intended-embedding root enclosures and inverse-square-root enclosure at actual p; an approximate root equation or source digest is insufficient |
| Fixed-point stages | No stage is evaluated | Lossless normalized loading; declared tie rule; rounded products/half-sum; exact additions, partial sums and accumulators; compression, boundary, coefficient factors, seeds, recurrence, normalization, complete gauge scan and output permutation |
| Payload | Exact kappa and declared radius; complete content binding; optional exact equality to external output | Establish that the returned payload was actually produced by the specified arithmetic on the same input/state/p. An untrusted matching digest or reference alone cannot do this |
| Range and cost | Checker limits and finite control counts only | Actual intermediate ranges/widths; all reached producer, root, prepass, planning, checking, copying, normalization and output work paid cumulatively |
| Adapter | No call and no eligibility claim | Actual legacy grammar/metadata caps, dyadic length 4<=N<=4096, actual Cartesian numerator width<=65536, correct zero status and normalization/tolerance allowance |
| Downstream | No call or instance | Actual source-class, sparse eligibility, window, schedule, tolerance and cumulative costs; second ideal target remains R P x/alpha |
| Different backend | No alternative backend | Backend-specific seed, coefficient, recurrence-residual and stability evidence, including roots/padding/rounding/range and all costs |

A semantic trace verifier would have to check the mathematical relationships between successive states and intended-root enclosures, not just hash the trace. A proof of such a verifier's soundness and its resource ledger are separate deliverables. A trusted execution wrapper alternatively needs a reviewed correspondence from the actual implementation to the accepted serial arithmetic and an unbroken, independently retained input/output binding. Neither alternative is supplied here.

## Controls and reproduction

Run `python checks.py` from this directory. It imports only the new sibling verifier and Python standard-library modules. `CHECK_RESULTS.json` records each named control, and `SYNTHETIC_EXAMPLE.json` contains a complete public-safe worked record with an explicit synthetic-payload warning.

Controls cover wrong raw coordinates/exponent, wrong state/frequency cycle, wrong t/q/p, insufficient p, rehashed wrong plan fields/prepass, stale or incorrect digests, wrong output scale, complete payload substitution, self-asserted certification flags, equivalent dyadic regridding, all three zero distinctions, odd parity, non-binomial modulus, near-kernel inputs, failed sufficient width bound with small actual payload, malformed types/lengths, duplicate JSON keys, nonfinite numbers, lone surrogates, nested tuple substitutions, and cyclic objects. The 300 random canonicalization cases are checked using independent `Fraction` arithmetic.

## Source basis

- [Accepted all-length policy](https://github.com/AgentSlop-Si/research/blob/acd8db5e6ad4660fb63ce1f2c63ee45577d454f0/math/finalized/2026-10-16-research-finalization-1458/all_length_policy/REPORT.md), SHA-256 7153cde50511545ea2b63b3ab7a67efc0b7222ba0b96c1ef76d1612635564062.
- [Independent acceptance](https://github.com/AgentSlop-Si/research/blob/acd8db5e6ad4660fb63ce1f2c63ee45577d454f0/math/finalized/2026-10-16-research-finalization-1458/independent_review/ALG034_REVIEW.md).
- [Accepted serial precision archive](https://github.com/AgentSlop-Si/research/blob/35d9dcdc3f3869de75b33b2b09705222e8d09e8d/math/reviewed_rounds/2026-10-13-reviewed-1354/archives/ALG034_Fixed_Point_Precision_Contract_Independent_Review_2026-10-13.zip), archive SHA-256 6381acc0cf5bf6aff7af69b645f77462026fa92949d7d685abaf0c5f523fc4b2; accepted report SHA-256 8dcc83d64316a136cb482fd04cff81ebaf7bf2351ab61fec1f02d8eadaf81cf8.
- [Accepted bounded adapter archive](https://github.com/AgentSlop-Si/research/blob/35d9dcdc3f3869de75b33b2b09705222e8d09e8d/math/reviewed_rounds/2026-10-13-reviewed-1625/archives/ALG034_Q16_Bounded_Paid_Source_Adapter_Independent_Acceptance_2026-10-13.zip), SHA-256 1ea2f4ce8db36d0f7e13141e8c1e679cf02e552f2054afe84a0dbda738ea5797.

The immediately preceding source-gap audit and its independent review were read as data. They identified the normalized-input-only reference producer and the payload-only bounded adapter. This packet does not claim no newer implementation exists elsewhere. Source reports were consulted as text; no historical source program was executed. Full source preimages and private audit directories are intentionally not included.
