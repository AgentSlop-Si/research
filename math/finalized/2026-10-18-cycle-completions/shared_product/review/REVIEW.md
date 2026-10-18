# Independent final review: canonical block-jump shared multiplication

Date: 18 October 2026.

## Verdict

**PASS.** The reviewed construction is an exact complete signed-binary multiplier on its recognized branch, with complete bit cost

O(N + r^12 + (K_A + K_B) r^4 + Q r^4 + K_A K_B r^2),

and consequently O(N + r^12 + K_A K_B r^4), where r = floor(log2 N), Q is the number of distinct commutative normalized-leaf product types, and K_A, K_B count all changes in the complete legal block lists, including transitions from and back to zero.

The fixed-budget test K_A K_B r^4 <= C N yields a complete O(N) accepted branch for every fixed positive C. The default front end uses C = 64 and the previously accepted complete dispatcher on rejection. Its arbitrary-input upper bound remains N exp(O(log N / log log N)), with the accepted root-wide bookkeeping erratum. No arbitrary-dense N log N bound or new-policy lower bound follows.

No production change or new erratum is required. The theorem inherits the already accepted native-plan facts and fallback proof; the reviewed fallback must continue to be interpreted with its existing required erratum. This review does not assert historical novelty for run differences or sparse convolution.

## Reviewed artifacts and provenance

- Candidate report: `../candidate/REPORT.md`, SHA-256 `79744e977c8953bc80d081f6b89d316357ff4c39e918314c9fa6c2e6f0416c9f`.
- Candidate source: `run_shared.py`, SHA-256 `b21a5c620e045f8cb7865763593b67137d38b320efbb085617417c5631e731f0`.
- Imported primitive/fallback source: `../candidate/dependencies/shared_adaptive_completion_20261017_2130/shared_dispatcher.py`, SHA-256 `a5c5e68fac2a43fa0847c15f2c09341c2da3f94013dc5a31ef6f797637fe4a06`.
- Accepted comparison review: `../candidate/dependencies/shared_adaptive_final_review_20261017_2147/REVIEW.md`, SHA-256 `b740dd0f3f61b1e34527a33f00fee5b293fe960ede8ee3fad41fbfc83051d692`.
- Required inherited erratum: `ERRATUM.md` in that accepted directory, SHA-256 `45f2f4506e5d81fa1c02d81ac8db779d88ee4292ad87aa1d680460b0ecbe368f`.

The accepted directory's nine manifest entries and its manifest seal were independently checked. The candidate enforces its primitive dependency hash before import. This review read the production source and accepted proof before authoring new controls. It imported no prior control program and did not modify the candidate or its dependency. Work and outputs remained local.

## 1. The nonlinear encoding issue is correctly resolved

Let c(a) be the canonical Newton digits of a legal block, W_h = binom(P+h-1,h), and f_c(x) = sum_h (-1)^h c_h binom(x,h). The accepted plan ensures f_c(-P) = sum_h c_h W_h = a.

Canonical encoding is not additive. The production code forms d_i = c(a_i) - c(a_(i-1)) entry by entry, rather than encoding the numerical difference. With the terminal change to zero included, this gives the exact polynomial identity

D_A(x,Y) = (1-Y) F_A(x,Y),

and the corresponding identity for B. This holds at every x and for each source packing base, not merely at the target -P. Thus the original source matrices are preserved.

Every nonzero jump is normalized by the sign of its first nonzero coefficient. This sign can oppose the sign of its decoded integer value. The code handles that correctly: normalized leaves may decode to negative integers, products and interpolation remain signed, and the separate event sign restores the original vector product. Fresh regressions at ranks 6, 10, 12, and 18 use the transition P-1 to P+1. Its vector difference is not the encoding of 2, and the normalized leaf decodes to -2 with a negative external sign.

The original canonical digits lie in [0,P), so jump digits lie in (-P,P). Degree remains at most r-1, and ordinary-node values retain O(r)-bit size. No assumption of nonnegative jump coefficients or node values is used.

## 2. Recognition, exact graph construction, and checks

`split_blocks` extracts the complete magnitude block list through one dense byte representation and bounded byte windows. `run_transitions` scans every block, includes a possible leading transition after a zero prefix, and appends the final transition back to zero. An internal zero run is represented by its actual changes. A nonzero finite list has at least two transitions.

Recognition counts both complete transition lists and evaluates the budget before canonical conversions or pair construction. The native plan has already been constructed at this point, so rejection costs O(N+r^12), not simply O(N) at every finite N. This is exactly the overhead paid in the report.

The graph canonically expands run values, differences adjacent vectors, sign-normalizes, and interns through exact deterministic sorting. It retains original positions and signs. Each of the M = K_A K_B term pairs generates one signed event. Commutative leaf-index pairs are sorted and interned; no hashing hypothesis, position-by-position reinterpolation, or root-size linear lookup is hidden here.

The default checker performs a separate full input scan and reconstructs expected transitions and coefficient-vector differences. It checks all terms against exact canonical vectors, verifies leaf use, reconstructs every required pair event, rejects missing or redundant product types, checks native leaf/product evaluations, and verifies actual source maxima and widths from separately evaluated original run values. Direct decoded-leaf products used by the checker have O(s)-bit operands and use the explicit elementary backend. They do not invoke an original-input or packed-child multiplication oracle.

The checker validates the graph and its evaluated targets. The two-prefix reconstruction and final carrying are established by the source-level proof and independent tests; the production checker is not advertised here as a separate verifier of an externally supplied final output integer.

## 3. Source rows and reconstruction are exact

At each retained node, prefix sums of the jump values equal the original run values. `source_rows` updates the running value at every transition and checks the final zero tail. It considers actual values only where the run occupies an input position. Leading zero runs do not affect the maximum; zero-valued internal runs are harmless. The separately recomputed checker maxima agree.

For A_x, B_x and L = max(L_A,L_B), the positive-row width is exactly

w_x = 8 ceil(bit_length(2 L A_x B_x)/8).

It is strictly large enough even on an exact power-of-two boundary. A zero row product receives width zero. Since the jump identity holds as a polynomial in Y, substitution of a different source base 2^w_x at each node is legitimate. The algorithm need not materialize the packed child integers.

Every distinct product of two degree-(r-1) leaf polynomials has degree at most 2r-2. Its evaluations at the retained 2r-1 consecutive nodes are interpolated exactly once. An event at i+j therefore contributes the signed numerical product of the original block changes at i and j.

If e_k is the sum of all events at k, then two inclusive prefix sums recover the ordinary convolution of the original nonnegative blocks, because

D_A(-P,Y) D_B(-P,Y) = (1-Y)^2 F_A(-P,Y) F_B(-P,Y).

The code visits indices through L_A+L_B. It stores coefficients through L_A+L_B-2, checks both following coefficients are zero, and checks the first prefix also ends at zero. These are the correct terminal conditions. All stored coefficients must be nonnegative.

The inherited assembly routine performs ordinary base-2^s carrying and writes each output block by a bounded byte window. Adjacent non-byte-aligned windows share only the appropriate boundary byte. It does not repeatedly shift the entire output or a shrinking per-byte reservoir. Restoring the sign yields the exact signed integer product. Zero and fixed-width elementary cases are handled separately.

## 4. Complete bit-cost audit

The accepted native facts give s = Theta(r^2), log P = Theta(r), O(r)-bit digits and node matrix entries, and O(r^2)-bit interpolation weights. The one-time fresh-plan construction costs O(r^12).

### Canonical conversion

Before division by W_h, the remaining value is below W_(h+1), including the top digit because the legal capacity is at most W_r. The successive-weight ratio is at most P. The quotient is therefore less than P, and the dividend/divisor bit-length difference is O(r), even though the integers themselves have O(r^2) bits. The explicit long-division routine costs O(r^3) per weight and O(r^4) per run value. Repeated conversion in the checker only changes the constant.

### Leaf and product work

There are at most K = K_A+K_B distinct leaves. Evaluating one leaf at O(r) nodes requires O(r^2) elementary products of O(r)-bit operands and hence O(r^4) work. Source-row prefix values remain O(r) bits.

A product has O(r) pointwise multiplications of O(r)-bit node values. Its finite-difference table has O(r^2) entries. Repeated differences increase bit size by at most O(r), so entries remain O(r) bits. Multiplying O(r) such values by O(r^2)-bit interpolation weights costs O(r^4). The checker separately decodes each leaf in O(r^4) and directly multiplies each pair of O(r^2)-bit targets in O(r^4). Thus all evaluation, interpolation, and verification work is O((K+Q)r^4).

### Comparisons, records, and event accumulation

A full leaf vector contains O(r^2) bits. Sorting K leaves costs O(K log(K+1) r^2) = O(Kr^3), since K = O(N). Pair and event records consist only of O(r)-bit indices, positions, and signs. Sorting M records costs O(M log(M+1) r) = O(Mr^2). Exact comparisons and record movement are covered. Rebuilding these records in the checker changes only constants.

Each event target has magnitude below 2^(2s). The sum at a position, its first prefix, and its second prefix have respective conservative bounds M 2^(2s), M 2^(2s), and (L_A+L_B+1)M 2^(2s). Since M = O(N^2), they all have O(r^2) bits. The stronger exact final convolution bound is min(L_A,L_B)2^(2s). Event accumulation therefore costs O(Mr^2).

### Full scans, carrying, and output

Splitting, run recognition, repeated dense input binding, and complete output reconstruction scan O(L_A+L_B) blocks, each of O(r^2) bits. This is O(N), including zero gaps and unequal lengths. The prefix scans and carrying use O(r^2)-bit state per position. Block-offset multiplication uses O(r)-bit metadata and costs O(r^2) per block, also O(N). Input/output sign and dense integer conversions are included.

### Root-wide diagnostic state

The imported `Elementary` ledger is fresh when the native plan is constructed, before root-size stream charges. The inherited O(r^12) setup accounting therefore remains applicable. Subsequently all totals and record indices have O(r)-bit width: the branch has polynomial-in-N total work and records. Apart from already-paid sorting comparisons/movement, there are O((K+Q)r^2 + M + L_A+L_B) primitive or administrative events. Charging O(r) for counter/reference/index handling contributes O((K+Q)r^3+Mr+(L_A+L_B)r), within the stated terms. Elementary arithmetic loop costs are already covered by their bit bounds. Product logs are appended, not searched. Dense byte copies are charged by copied length rather than triggering a root-wide counter update for every copied bit.

Combining the terms proves the displayed refined bound. Since nonzero finite lists have K_A,K_B >= 2, K_A+K_B <= K_A K_B; also Q <= K_A K_B. This yields the uniform O(N+r^12+K_A K_B r^4) bound. Under the fixed linear budget, r^12 = o(N), so the complete recognized branch is O(N), with constants permitted to depend on the fixed base threshold, verification policy, and budget factor.

## 5. Comparison with the accepted bounded-support result

On the same native blocking, t_A and t_B occupied blocks imply K_A <= 2t_A and K_B <= 2t_B. Thus fixed occupied support is included, and the new criterion additionally allows growing support and growing transition counts. For the old dispatcher after binary-valuation removal, inclusion remains asymptotic: a fixed number of occupied old blocks occupies a fixed number of bit intervals, and the accepted two-sided s = Theta(log^2 N) bounds ensure each such interval intersects only O(1) blocks of the new root plan. Arbitrary binary shifts do not alter this conclusion.

Conversely, a nonzero legal block repeated throughout an arbitrarily long list has K_A = 2 and unbounded occupied support. Choosing odd repeated values avoids binary shift extraction. Such inputs eventually fail the old fixed-support recognizer while satisfying the new fixed-budget test. This is a strict extension of the stated recognized input class. It is not proof that the old dispatcher's runtime is superlinear on those families.

A rejected new branch adds only O(N+r^12) work and invokes the exact hash-pinned dispatcher. The accepted arbitrary-input bound dominates that overhead. Its root-wide bookkeeping erratum remains part of the inherited claim; the extension does not revert to child-local constant-time metadata assumptions.

## 6. Fresh controls

`independent_review_controls.py` was newly written after source inspection. It uses a separately reconstructed direct-CRT native point, exact generalized-binomial rows, direct canonical expansions, direct polynomial convolution, and native integer arithmetic only as test oracles.

The successful run passed:

- 33 complete independent native plans, ranks 2 through 34, including nodes, rows, and interpolation weights.
- 2,001 canonical boundary/random-block cases and 45,177 explicit short-quotient checks.
- 58 complete signed products, including zeros, both signs, the fixed base threshold, random dense inputs, maximum carry chains, non-byte-aligned serialization, zero gaps, leading shifts, partial top blocks, large imbalance, repeated values, and opposite normalization/decoded signs.
- 261 original-source-node identities, with independent actual maxima, strict widths, complete jump rows, terminal checks, and packed-source identities.
- 262 direct convolution comparisons, spanning original signed node rows and ordinary nonnegative block coefficients.
- 22 corrupt-certificate rejections, including changed dense input, header, leaf, term, event, product, target, nodal value, source maximum, source width, and source bound.
- Exact default-budget acceptance for 12 events and rejection for 16 events at rank 12. A sentinel established that the rejected case never called graph construction.
- The complete pinned fallback after an explicit zero-budget rejection.

The largest fresh dense-run example has 2,098,875 input bits, rank 21, block width 965, and complete occupied supports (2,175, 2,174). Its jump counts are (10,11), with 110 events and 110 shared products. It passes the default factor-64 budget and returns the correct negative product. The largest elementary multiplication operand is 1,850 bits and the largest prefix intermediate is 1,940 bits. No packed child is multiplied.

The first review-harness attempt mistakenly expected a rank-10, 12-event input to satisfy the fixed factor-64 budget. The actual predicate correctly rejected it. That test expectation was corrected to a six-event rank-10 case, and the full suite was rerun successfully. The initial log is retained as `HARNESS_THRESHOLD_CORRECTION.log`; no production bug or change resulted.

These finite tests corroborate exactness and implementation correspondence. They are not measurements of asymptotic speedup. The primitive ledger is diagnostic, not an end-to-end instruction counter; the complete bit bound rests on the accounting above.

## Final scope

The canonical block-jump theorem, full signed multiplication implementation, dense recognizer, default checks, carry/output handling, and inherited fallback are accepted on the stated parameter scope. The arbitrary-dense shared-representation question remains open.
