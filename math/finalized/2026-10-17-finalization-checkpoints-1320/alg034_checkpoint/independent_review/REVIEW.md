# ALG-034 bounded consistency contract: independent challenge

17 October 2026.

## Verdict

**ACCEPT the scoped bounded consistency verifier, after two resource-handling repairs. No required repair remains in the reviewed snapshot.**

Reviewed `binding_verifier.py`: SHA-256 `aa6863c524d69a1433bb4298cdc63092a4e7dd869f857356689bc2cbc0612d27`, 15,485 bytes.

The artifact checks exact original data, the accepted policy, and proposed payload consistency within its stated local limits. It does **not** establish an authentic producer execution, numerical target/error correctness, adapter eligibility, or downstream integration. The implementation-evidence gate remains open. Preserve ALG-034 **TO RESEARCH, priority 48**; do not credit a new precision theorem or close the parent.

The final frozen source passes **95 independent named controls**. One named batch contains 92 independently recomputed exact-policy cases; another covers four admitted length/width boundaries. These are finite implementation controls, not a universal testing proof or a numerical producer run.

## Independent method and inspected material

I read the accepted source-gap audit and underlying all-length policy report as data, then read the newly written verifier in full. I independently authored `independent_oracle.py` and `challenge.py`. The oracle constructs cyclotomic polynomials by recursive proper-divisor division and independently reconstructs the exact block polynomials, remainders, masses, selected witness, width, precision plan and symbolic scales. It does not call the candidate's policy routines to obtain expected answers.

After source inspection, I imported only the newly authored bounded checker for adversarial tests. The final run used a byte-identical frozen copy. No historical producer, archived checker, adapter, downstream implementation, or the author's own `checks.py` was imported or executed by this review. No original research program was used as a numerical oracle. No external state was changed.

`STATIC_REVIEW.json` records imports, the invariant success return, and independent byte-length/SHA-256 checks of all six entries in the author's refreshed manifest. Author test results were read only as data and are not counted as independent tests.

## Exact dyadics, policy and grammar

The three identity meanings are correctly separated:

- The raw commitment preserves decoded F and every ordered integer numerator. W is computed on these submitted numerators before normalization.
- The value commitment removes exactly the minimum trailing-power-of-two valuation over all nonzero Cartesian components. Negative components divide exactly, zeros remain zero, and an all-zero vector has canonical scale zero. Both coordinate order and vector length remain present.
- The payload-grid commitment preserves the exact proposed numerators and kappa. Equal dyadic values do not permit a different original grid or a different producer grid to replace the caller's expected representation.

Integer JSON `-0` and `0` intentionally identify the same decoded integer. Floating signed zero is rejected with other floating-point input. The raw commitment is not a commitment to the original JSON byte stream; whitespace and key order are irrelevant. The report expressly states this boundary.

Independent controls cover negative common exponents, negative numerators, shared trailing powers, zero vectors at different F, maximum admitted numerator widths, unchanged value commitments after regridding, and rejection of that regridding against the original caller context.

The exact policy comparisons cover N=3 through 32 with several balanced partitions and coprime states, plus N=63 and 64 boundary cases. They agree on the full modulus, aggregated polynomials and remainders, A and its tie break, W, K, G, H, C, c, p_min, selected p, I, kappa, symbolic radius and separation exponent. The known even-length projected-zero case N=6 and the odd-parity nonzero case N=9 are distinguished. No new mathematical theorem is inferred from these controls.

Raw arrays and payloads reject incorrect lengths, tuples, list subclasses, bool-as-int, floats, strings, integer subclasses and overwidth values. State/domain and t/q/p conditions are enforced. Rehashed changes to all tested policy or plan fields reject against separately supplied caller context. Nested tuple or subclass substitutions, non-JSON objects, cyclic structures, self-asserted certification flags, duplicate JSON keys, malformed numbers, nonfinite constants and depth-limit violations do not obtain a successful record. The final JSON parser applies the same conservative tree/serialization budget as direct canonical intake.

EXACT_INPUT_ZERO, EXACT_PROJECTED_ZERO and ZERO_APPROXIMATION remain distinct. Exact zero branches cannot supply a producer payload or declare p. An all-zero approximation on a nonzero plan rejects. This review does not treat that rejection as proof that a nonzero arbitrary payload is correct.

## Hash scope and proof-status boundary

The domain-separated SHA-256 commitments cover the intended exact decoded objects. Independent reconstruction of policy, grid, canonical-value and outer-record commitments reproduces an accepted record. Corrupt subordinate commitments and binding commitments reject. Canonical policy content is compared with a freshly recomputed policy rather than accepted from the digest alone. Hash-based compact identities retain the usual collision-resistance assumption.

The central adversarial controls deliberately succeed at **consistency only**:

1. Replace the complete payload by arbitrary nonzero integer arrays of the right scale, then recompute every commitment. Without an independently supplied reference, the record is consistent. Its producer, provenance and numerical correctness flags remain false.
2. Supply the original external grid reference against that replacement. It rejects with `PAYLOAD_REFERENCE_MISMATCH`.
3. Replace both raw input and payload, recompute the policy and commitments, and provide the substituted payload itself as the external reference. The result is still only consistency, even though exact-reference equality is true. Against the original caller context, the changed-input record rejects.

Static inspection strengthens these finite examples: the unmodified `verify` function has one successful return, with literal status `BINDING_CONSISTENT_PRODUCER_UNVERIFIED` and five literal false fields: authenticated provenance, producer execution, numerical error certification, adapter invocation and downstream integration. No record-supplied flag chooses those values. Consequently, no ordinary accepted record in this implementation can promote itself to proven execution through modified inputs, rehashed data or self-asserted flags.

This is an invariant of the reviewed checker, not authentication of its caller or a claim against a caller that replaces/monkeypatches the checker itself. An untrusted matching reference proves only equality to that reference. Source hashes, policy hashes and signatures without separately established execution semantics do not bridge the missing mathematical input-to-output relationship.

## Repairs found and rechecked

1. **Default precision metadata cap.** Initially, N=B=3, a=1, beta=0, raw real=[1,0,0], imag=[0,0,0], F=-(2^128-1), t=2^128-1 and q=2 produced a 129-bit default p that could pass consistency, while explicitly supplying the identical p rejected under the 128-bit cap. The final source validates selected p after default selection. The independent regression now rejects uniformly.
2. **Aggregate serialization budget.** Initially, per-string and node caps did not bound aggregate serialized size; repeated strings could force a very large temporary serialization before mismatch rejection. I identified the large-instance risk statically, without running a denial-of-service stress case. The final source conservatively charges total integer, string and container serialization size before encoding, including worst-case Unicode escapes. A small, safe over-budget regression now rejects. Depth, node and JSON intake caps remain in force.

These repairs concern the newly written checker's intake behavior. Neither changes the accepted precision policy, and neither exposed a route to a positive producer/numerical verdict. The original deep-JSON test expectation was also corrected to distinguish parsing from complete canonical intake; the final implementation now applies both stages inside `strict_loads`.

## Retained conditions and disposition

The final report preserves the stronger remaining obligations: an authenticated/fixed caller context, a pinned actual entrypoint and dependencies, implementation-to-theorem correspondence or a sound paid semantic execution verifier, intended-root and inverse-square-root enclosures, genuine serial arithmetic and rounding, actual output equality and order, intermediate range bounds, and cumulative resource accounting.

Local checker caps (N<=64, raw width<=1024, payload width<=8192, selected p and supplied integer metadata<=128 bits, and conservative serialization/tree limits) do not extend or alter the legacy adapter. Failure of p+I<=65536 remains failure of a sufficient width certificate, not proof of actual overwidth. Actual adapter grammar, dyadic length 4<=N<=4096, actual width<=65536, normalization/tolerance and downstream restrictions remain separate. The second ideal target remains R P x/alpha.

Recommended disposition: **COMPLETE_SCOPED_BOUNDED_INPUT_POLICY_PAYLOAD_CONSISTENCY_VERIFIER**. Retain **BLOCKED_ON_BOUND_IMPLEMENTATION_EVIDENCE**, ALG-034 TO RESEARCH / 48, and all full-owner conditions. This reviewed contract is a concrete consistency interface for future genuine producer evidence; it is not that producer evidence.

## Reproduction

Run `python challenge.py /path/to/reviewed/binding_verifier.py` with the exact reviewed source hash above. Only the newly authored checker is imported; `independent_oracle.py` supplies the separate arithmetic expectations. `CHECK_RESULTS.json` records all 95 named outcomes, and `STATIC_REVIEW.json` binds the reviewed source and companion artifacts. Private frozen copies and interpreter caches are excluded from the public manifest.
