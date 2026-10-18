# Independent final review: target-explicit dense dispatch

18 October 2026 UTC.

## Decision and scope

**PASS for the final repaired, frozen candidate.** No remaining blocking defect was found within the stated scope. The mathematical, implementation, binding, and accounting review accepts this narrow gate: a source-bound, target-explicit, certified direct unitary DFT; a separate exact normalized singleton second-transform reversal; and an honest complete dense fallback/mixed-dispatch cost contract.

This is not a fast Fourier algorithm, a same-source sparse/outer composition, a general-block implementation, or closure of ALG-034. No rounded-serial equivalence, historical execution attestation, or novelty result is inferred. The runtime is bounded by its explicit finite Limits. The unrestricted construction and cost theorem are mathematical statements, not an executable all-length performance guarantee.

## 1. What was inspected and independently executed

The complete production file, report, source bindings, author control source/results, repairs, status, seal, and manifest were inspected. The nine retained dependency documents were checked for the target/domain qualifications actually used. Their local SHA-256, length, and Git blob SHA are independently recomputed. No inherited implementation or predecessor test suite was run. The author's fresh scientific driver was read but not imported or executed by this review.

The review imports only the new production module from a byte-identical frozen snapshot. Its independent controls are authored after inspection. The exact target oracle uses pi = 8 atan(1/3) + 4 atan(1/7), direct separate even/odd rational power sums, and integer-bisection reciprocal-square-root bounds. This differs from both the production Machin formula and the author's oracle identity. All error comparisons are rational inequalities; floating tolerances are absent.

All 20 candidate manifest entries and nine source-document Git blobs verified before the final run and remained unchanged afterward. Process timing is an observation, not performance evidence.

## 2. Target distinction and original-source binding

For a supplied original x = c 2^-F, the inherited singleton supplier gives f = U_N x / alpha, with alpha = 2^(h-F). Its recovery target is U_N f = R_N x / alpha. The outer stage instead requires the separately bound centered transform of an original u and conditionally targets U_N u. The candidate correctly refuses to identify these targets from a label or digest.

FIRST_DFT evaluates U_N x for the exact supplied original. SINGLETON_SECOND_NORMALIZED requires B_A=N and materializes R_N x / alpha exactly, with denominator exponent h. Its alpha metadata is not a claim to have materialized a scale-backed result. The independent N=4 delta_1 control separates these targets by exact squared distance 2. General B_A is rejected, and no callback, recovered support claim, or alleged centering certificate can select a fast path.

Every dense coordinate is visited; immutable nonzero tuples, N, F, and representation kind retain an equivalent exact original with implicit zero coordinates. Sparse input is a supplied exact representation, not purported acquisition of an unknown dense input. Complete replay binds the result to the original, target, representation, scale, precision, dispatch, and receipt. Caller mutation cannot alter the retained immutable source. This remains caller-relative mathematical binding under trusted Python/standard-library semantics, not external authenticity.

## 3. Coefficient and numerical proof

The Machin alternating intervals, outward dyadic reduction, signed residue angle reduction, exact Taylor recurrence and remainder, and reciprocal-square-root enclosure are valid. For a real angle, the integral Taylor remainder of exp(ix) is bounded by |x|^(K+1)/(K+1)!; no missing exponential growth factor is required. The exact endpoint-distance squared test certifies a complex coefficient radius, rather than merely two unrelated Cartesian tolerances. The stated constants are loose enough for every uncapped prescribed precision.

The exact energy normalization gives 1/2 < ||c/2^h||_2 <= 1 for nonzero input. Coefficient error contributes at most N 2^-q ||u||_2, and one final Cartesian rounding contributes at most sqrt(N) 2^-b. With q=b=r+ceil(log2 N)+4, the stated 3/16 relative error bound follows. Zero is exact and does not satisfy a strict positive relative inequality; the repaired report now says so. N=1 is an exact copy.

All complex products and accumulations are integer-exact. Each Cartesian prefix obeys the proved W+g+m+4 signed allocation even when a later cancellation leaves a very small final sum. The new 1024-bit cancellation control reconstructs every prefix independently and records the gap between its largest intermediate width and its final zero-frequency width. Signed ties-to-even rounding and exact scale-back are consistent with the theorem.

A huge positive F remains an encoded denominator exponent. A sufficiently negative F produces real shifted numerators, and that work/storage is charged. Both the general direct-transform and N=1 physical-shift endpoints are checked. Oversized physical expansion rejects before Fourier setup or full output allocation. Normalized reversal legitimately keeps a huge negative F only in alpha metadata.

## 4. Dispatch and complexity

The structural test M=nextpow2(4N), t=32D log2(M)+4, t<M is evaluated before coefficient setup. For fixed D, the explicit finite exception bound N<4096D^2 is sound. Absorbing this region into O_D(N) additionally assumes the report's fixed family of precision, width, scale, and parameter encoding bounds. It is neither uniform in D nor applicable to arbitrary missing-provider fallbacks. Independent allocation-free plans force structural fallback at lengths through 2^126 by varying D.

At N=2^28, the actual original support distinguishes the historical recovery domain from its failure, but even an eligible original does not bind a same-target sparse provider. The implementation reports this explicitly and routes all supported FIRST_DFT work to direct evaluation.

Writing L=2+r+ceil(log2(N+1))+W+bit_length(F)+bit_length(D), with J the actual physical shift, the conservative production bound

    O((Ns + N(L+J+1)) (L^2+J)^3)

covers input recognition, normalization, coefficient construction, index work, products, all prefix updates, output expansion, and bookkeeping. The pi series and Taylor intermediates have O(L^2) width, and O(NL) coefficient records give the explicit O(NL^7) setup bound. No coefficient table is treated as an oracle. Worst-case s=N gives the honest quadratic direct-transform term. Peak production data O(N(L+J)+L^2), with external retention/export/review artifacts separate, is a safe bound.

The reversal branch pays input acquisition/normalization plus every N output, and the stated O((N+sL)L^3) conservative bound is valid. Replay, comparison, and each export have separate receipts. Receipt counter widths are included in the global envelope. The final repair also preserves a completed replay receipt when comparison rejects, so a failed comparison cannot erase already incurred work.

The future mixed-branch contract correctly adds all actually reached stages and all aborted prefixes. Deterministic dense fallback on explicit rejection cannot worsen an already established sparse joint success/accuracy bound; it does not make undetected bad sparse answers deterministic. Independent tape, fixed-source guarantees, and paid amplification remain prerequisites, not results of this reference.

## 5. Review findings and required repairs

The initial inspected candidate was not accepted unchanged. Review found and reproduced:

1. set(raw) traversed an arbitrarily large malformed dictionary before the length guard while returning a constant grammar-rejection receipt. The repair checks exact dictionary type and length before key traversal, and rejects non-built-in key types.
2. Ordinary dataclass equality allowed a Result subclass or an integer subclass inside a result to return True from a supplied __eq__ method. Wrong numerical answers then verified successfully. The repair uses expected-shape recursive comparison with exact types and bounded length/width guards, and charges visited nodes/scalars.
3. The strict comparator could exceed its event cap after a successful replay, returning only the comparison prefix and dropping the replay receipt. The repair retains prior stage receipts and requires summing them with the current prefix. Exact Result/Source instances missing fields are covered by typed grammar rejection with the same retained replay.
4. Pre-limit abs() on enormous negative metadata/components copied unbounded raw integers before rejecting them. Direct exact-int bit_length reads avoid the copies, and computed width metadata is charged before the width-based rejection.

The zero-input strict inequality and literal claim that every zero pair was copied were corrected in prose. These repairs do not change the Fourier target or introduce a sparse bridge.

## 6. Stopping point

The frozen repaired package, all manifest/source bindings, the complete new independent batch, and the unchanged post-test hashes have now been verified. This gate closes the bounded dense-reference/dispatch obligation only. The next substantive research obligation is a genuine same-source, same-target sparse branch with the correct general/centered source, recovery/amplification guarantees, and full all-tape costs. No external write was performed by this review.

## 7. Final frozen evidence

Accepted candidate manifest SHA-256:

    ce811d4cf810e73c0c5c53e100484ff472bf38fd0d370d8b45e0b59334b67fe0

Accepted production SHA-256:

    45dfd1f87e6a5abc25ea3cb7f15b2b55e0fa2c6604beb052d3970e4d6ee07f31

The final independent batch completed:

- 18 primary direct-DFT runs and 239 fully checked output rows. Seventeen runs use guaranteed independent rational target intervals; the N=128, r=128 endpoint uses the exact two-mode Fourier identity for x_j=1+i(-1)^j and a 240-bit bisection enclosure of 1/sqrt(2). Every one of its 128 rows is checked, including both active modes and all zero modes. All primary checks meet the stronger stated 3/16 norm bound.
- Six exact reversal runs, including target separation, and 175 checked output rows.
- Three separate coefficient tables, 22 coefficients, each independently checked against the complex 2^-q radius. A further nine-coefficient table supports the independently reconstructed cancellation-prefix control; its work has a separate receipt.
- Ten allocation-free plans, including variable-D lengths through 2^126 and historical-domain support counts 0, 1, 16, and 17 at N=2^28. None admits a same-target sparse branch.
- Eight complete three-coordinate semantic replays: one valid and seven altered-source/scale/representation/target/output/equality-hook cases.
- Seventeen paid source/resource rejections, including a 20,000-key dictionary and one-million-bit negative metadata/components.
- Five comparison rejections that preserve their completed replay: four event caps and one missing-field Result. Each failed cap control explicitly sums the completed replay and terminal comparison-prefix work/storage, with original production separate.
- In total, 36 complete FIRST_DFT executions wrote 275 rows in this final batch, including replay/source-setup work. Together with reversal, 450 output rows were materialized. Rejected numerical prefixes and extra coefficient preparation remain separately recorded.

The 1024-bit cancellation control independently reconstructed 18 prefixes. The maximum magnitude width was 1062 bits, below the 1071-bit signed allocation; the zero-frequency final magnitude used only 38 bits. This explicitly checks a large prefix followed by cancellation.

The complete N=128 endpoint performed 16,384 exact complex prefix updates. Its guaranteed squared error divided by the stronger theorem budget is at most 2^(-18).

CONTROL_RESULTS.json, independent_controls.py, INTEGRITY.json, and the frozen candidate_snapshot contain the reproducible evidence. An initial reviewer harness expected a cap-40 comparison rejection, but the valid comparison has only 35 scalar records. That test expectation was corrected to caps 12/16/24/32 and the entire final batch rerun. The failed harness log is retained transparently; no production change was needed for it.

**Stopping condition met:** the repaired target-explicit dense reference and qualified complete fallback accounting are accepted. The missing sparse/centered/general-block composition remains open.
