# Independent final review: certified bounded-support shared dispatcher

Date: 17 October 2026.

Reviewed report SHA-256: `a2dfcf8d367fa9a4cb5df0599af58c90ea73f384e7d58cc51b9c9b889fd8d707`.

Reviewed producer SHA-256: `a5c5e68fac2a43fa0847c15f2c09341c2da3f94013dc5a31ef6f797637fe4a06`.

## Verdict

**PASS WITH REQUIRED ERRATUM.** The signed-integer dispatcher, bounded-support representation, exactness/termination argument, complete recognized-branch O(n) result, and arbitrary-input n exp(O(log n / log log n)) upper bound are accepted with the accompanying hash-bound `ERRATUM.md`.

Two statements require explicit clarification: the unbounded hard-family cores do not always fit the fixed elementary base threshold, and root-wide diagnostic counters/log indices require root-size bookkeeping rather than child-local constant-time accounting. The erratum supplies the corrected arguments. Neither issue requires a source change or invalidates the main results.

No general N log N improvement, matching lower bound for the new policy, or sharing-resistant hard family is established. The finite factor 5.907067823613817 concerns the declared primitive-charge ledger only.

The reviewed production source was not modified. This review imports that candidate solely to exercise it against independently constructed controls. No historical program was imported or executed; historical files were read only for provenance and inherited mathematical definitions. No external write was performed.

## 1. Arbitrary signed input, recognition, shifts, and content

The public multiplier validates integer operands, handles zero before any plan construction, removes both signs, scans dense byte representations for exact binary valuations, and restores the sum of the valuations and the product sign. With a fixed base threshold at least eight, every non-base rank is valid for the native plan.

The plan implementation reproduces the retained native integer construction. Its lcm/CRT computations and generalized binomial products use the explicit arithmetic backend. In fresh controls, an independent direct-CRT formula, ordinary exact binomial coefficients, and independent signed-binomial node norms matched every plan field at ranks 2 through 40. The canonical weights are W_j = binom(P+j-1,j), and the retained coefficient vector evaluated at -P equals the input block.

Legal s-bit blocks have canonical nonnegative digits below P. For all but the top digit this follows from the exact integer successive-weight radix; for the top digit it follows from the beta capacity bound. Hence coefficients and ordinary row values have O(r) bits, using the inherited native point and row-norm bounds. No arbitrary real coefficients or supplied support oracle are admitted.

`split_blocks` uses one dense byte conversion and bounded windows. `compile_sparse` scans the actual complete block lists before checking the support limit. The recognition result therefore binds to arbitrary dense input, including distant low nonzero blocks and unequal operand lengths. The root rejects a fifth occupied block under the default support-four policy. It does not decide sparsity from only the first few observed terms.

Every occupied block is canonically expanded. The vector gcd is removed exactly, primitive coefficient vectors are interned by equality, and the gcd of the resulting contents on each side is extracted. These contents are factors of the formal block polynomials; they need not be maximal integer gcds. Their product is applied to small nodal coefficients before dense reconstruction. There is no large output multiplied by a supposedly free content factor.

Binary shift extraction normally leaves first occupied block position zero. The compiler's separate outer-shift representation is nevertheless valid and was independently exercised with nonzero shifts and unequal supports. The fixed threshold correction in the erratum is necessary: the new 2,049-bit-core control takes a shared call after shift extraction, not an elementary base call.

## 2. Shared DAG, memoization, certificates, and varying packing widths

The structural certificate has at most 2t primitive leaves and t^2 commutative product nodes for fixed support limit t. Each side records exact occupied positions, positive scales, and primitive leaf indices. Every term pair contributes an edge with its exact outer position and scale. Product-node lookup and scalar-product memoization use exact comparisons, not fingerprints. Equal-position edges for the same product node are combined by addition.

At each retained ordinary node x, each primitive leaf and each symbolic product node is evaluated once. The second cache reuses equal signed integer operand pairs, including coincidences at different x. Each cache miss uses `Elementary.mul`; a sorted signed pair is a valid commutative key. The number and bit size of keys are polynomial in r for fixed t, so bounded linear cache search is paid. The new repeated-leaf control combines nine edges into five distinct supported positions using one product node, with nonzero contents and outer shifts.

`check_structure` independently binds the representation to all actual input support and canonical digits, checks primitive leaf vectors, common contents, offsets, required term-pair edges, product-node validity and use, and all native-plan metadata. It does not invoke the compiler. It may tolerate representation redundancy that does not change the identity, such as an unused additional primitive leaf within its limit; canonical compression uniqueness is not required for soundness.

`check_execution` takes the actual block lists and separately recomputes full canonical polynomials and direct sparse row convolutions. It does not rely on DAG evaluation or cache outputs. It verifies the row positions and values, actual maxima-derived bounds, strict source-rule widths, every convolution coefficient, and all reconstructed output coefficients. Together the two checkers prove the input-bound DAG identity and its executed products. The memo hit/miss fields are diagnostic telemetry, not a separately certified transcript of every cache operation; their correctness is established by source inspection and fresh executions rather than by the arithmetic checker.

For a node with actual row maxima A and B, each convolution coefficient has absolute value at most L A B, where L is the maximum original block-list length. The recorded positive-row width is exactly

w = 8 ceil(bit_length(2 L A B) / 8),

so Q = 2^w is strictly greater than 2 L A B, including exact power-of-two boundaries. A zero row product is recorded with width zero. The DAG identity is an identity of polynomials in the outer variable Y, so substituting a different legal Q at every node is valid. Equal widths across nodes are unnecessary.

Each supported outer-column polynomial has degree at most 2r-2. Its 2r-1 consecutive values determine it uniquely; the signed finite-difference interpolation routine evaluates it exactly at -P. The reconstructed coefficients are precisely the convolution of the nonnegative original binary blocks. Binary carrying, zero-gap traversal, byte serialization, shifts, and sign restoration yield the requested signed product.

## 3. Dense fallback and termination

When recognition fails, the code pads only the shorter block list, canonically converts all blocks, evaluates ordinary signed rows, and derives widths from their actual maxima. The separate positive/negative byte streams produce exactly the signed packed integers. Since each input coefficient is smaller than Q/2 and each product coefficient is bounded strictly below Q/2, the balanced unpacking is unique. The final borrow check correctly distinguishes negative from nonnegative packed products.

The fresh signed-stream controls include negative packed products, nonzero leading negative coefficients, mixed signs, unequal length situations through padding, and exact boundary widths. Independent direct convolutions agree with unpacking in all cases. Large coefficient carries and non-byte-aligned output widths were also checked directly against a sum-of-shifts oracle.

Before recursion the code measures every actual packed child. If any child is not strictly narrower than the current reduced parent, the parent returns the explicit elementary product. Otherwise all recursive widths strictly decrease. Removing binary shifts can only decrease them further. Strong induction on width proves termination and exactness; neither the proof nor the guard assumes that an allocated width equals the actual bit length.

The cap bounds apply to the actual implementation because every canonical digit is below P, the row maxima are bounded by the native row-norm cap, byte-rounded actual widths are at most their corresponding cap widths, and signed packed magnitudes are below Q^L. Thus each actual child is bounded by its retained cap. For sufficiently large reduced widths all caps contract, so the guard affects only a finite induction base. Very small configured thresholds can make this finite base expensive; one fresh 180-bit-input control produced 74,344 calls and still terminated exactly. The theorem's constants include such policy-dependent finite behavior.

## 4. Complete recognized-branch bit cost

Let n be the original width, n0 the reduced width, and r = floor(log2 n0). The inherited elementary native facts give s = Theta(r^2), log P = Theta(r), O(r)-bit canonical digits and nodal values, and O(r^2)-bit interpolation weights and reconstructed columns.

For fixed t, the number of encoded occupied blocks, leaves, product nodes, edges and supported output columns is bounded independently of n. The O(r) ordinary nodes introduce only polynomially many small arithmetic operations. Native plan construction, explicit long division, gcd/content operations, exact interning, all memo comparisons, both checkers, interpolation, and trace construction fit the deliberately loose O_t(r^12) bound. The bound includes the elementary bit cost of metadata and the polynomial-size trace; it is not a claim that every such event appears individually in the primitive-charge diagnostic.

One detail deserving explicit accounting is `check_execution`'s repeated support scans. It traverses each entire block list at all O(r) nodes. There are O(n0/s) block positions and each index costs at most O(r) bits to manipulate. These zero/support traversal costs are therefore O((n0/s) r^2) = O(n0), not an overlooked extra logarithmic factor. Only the fixed number of occupied blocks incur canonical arithmetic at each node.

Recognition and splitting use dense scans and bounded windows. Carrying visits all output positions, including absent ones. Each output block is written once using a bounded byte window; the implementation does not repeatedly shift a shrinking s-bit reservoir byte by byte. Index multiplication by s has only O(r)-bit metadata and also fits the stated bound. Digests, sign handling, extracted shifts and final dense output cost O(n). If n0 is bounded while n grows through a large shift, all core work is bounded and the dense restoration remains O(n).

The complete recognized branch is consequently O(n + r^12) = O(n), with constants dependent on fixed policy parameters. This includes recognition, both certificate checks, all primitive bit work, and dense output. It does not hold uniformly when t grows with n, or when the diagnostic forced-dense option is selected.

## 5. General upper bound and all bookkeeping

Ignoring only the extra root-wide diagnostic integer/index overhead for the moment, local conversion, maps, streams, interpolation, reconstruction and administrative-event counts admit O(n (log n)^12). The production source has no uncharged large-input multiplication: its host multiplication expressions are signs, fixed constants, allocation sizes, indices, or diagnostic cost formulas. Those metadata products are elementary polynomial-logarithmic work. Arithmetic-data products use the explicit signed shift-and-add routine, and all arithmetic-data divisions use binary long division.

The inherited cap volume is at most (v_plus + o(1)) n with v_plus = 9.0889395816..., and each cap child has size Theta(n/log n). The source definitions and accepted cap derivation are consistent with this implementation. The comparison function Phi_b(n) = n exp(b log n/log log n) therefore has eventual ratio at most exp(-b)(v_plus + o(1)); any fixed b greater than log(v_plus) supplies an induction margin. Local polynomial-logarithmic work is negligible relative to that margin. Reduction to smaller core widths and linear shift restoration are paid.

The erratum explicitly completes the treatment of root-wide counters, append-only product/certificate lists, and cached-plan lookups. Their metadata can depend on root width N rather than current child width. First use an exponent b0 strictly between log(v_plus) and b to bound arithmetic/event volume. All resulting counts and indices have O(log N) bits, and even conservative root-wide metadata handling contributes only a polynomial-logarithmic factor. This is absorbed into Phi_b/Phi_b0. Thus the report's stronger statement, O(Phi_b(N)) for every fixed b > log(v_plus), remains valid for the complete implementation rather than just an idealized local ledger.

The base threshold, support limit, verification policy and chosen exponent margin are fixed. Their constants and the finite cap-contraction/guard range are included in the induction base. No claim is made uniformly as these parameters grow with n. On this precise scope, the arbitrary-input bound is n exp(O(log n/log log n)); there is no matching new-policy lower bound and no free fast multiplication oracle.

## 6. Fresh independent evidence

The controls were written after reading the complete producer. They use independently constructed input families, direct CRT, standard exact binomial identities, direct polynomial evaluation and convolution, and native endpoint arithmetic solely as independent test oracles. They do not rerun or import the producer's control programs.

The main run passed:

- All 12 candidate manifest entries.
- 39 independently reconstructed native plans, ranks 2 through 40.
- 2,791 legal canonical boundary/block tests.
- 180 signed packed-convolution tests, including 87 negative products.
- 320 strict byte-width boundary tests.
- 72 carrying/stream round trips with non-byte-aligned widths and long carries.
- 50 complete signed products, including randomized low-threshold recursion, dense inputs, extreme imbalance, large shifts, maximum legal blocks, support overflow, and the finite comparison.
- 142 independently evaluated shared rows and six direct original-block convolutions.
- Ten fresh structural and four fresh execution-certificate mutation rejections.
- All 33 source packed-child product identities for the distinct-odd witness.

A second run verified the historical archive, five pinned source members and both accepted mathematical documents without executing their programs. It also passed the 2,049-bit-core threshold regression, bringing complete products to 51.

The independently reconstructed 131,352-bit odd witness has 33 distinct child pairs, exactly 16 odd pairs, and actual child width 6,380 bits. The shared computation uses one dispatcher call; the largest elementary operand is 1,254 bits. Every symbolic row product substituted at its actual source packing base agrees with the independently materialized child product. This is genuine sharing on distinct inputs, not duplicate-call caching or root binary shift removal.

The fresh 16,490-bit diagnostic comparison exactly reproduces:

- Shared primitive charge: 376,741,957; one dispatcher call.
- Forced-dense primitive charge: 2,225,440,292; 522 dispatcher calls.
- Dense/shared ratio: 5.907067823613817.

This ratio is neither wall-clock speedup nor a count of all interpreter actions. The asymptotic verdict rests on the complete proof and required clarifications, not on these finite measurements.

## Final scope

With `ERRATUM.md` attached, this closes the bounded-support dispatcher implementation and its stated proof obligations. It establishes an actual legal input recognizer, common shift/content handling, generic shared products, exact input-bound certificates, variable-width packing correctness, memoized elementary evaluation, exact fallback, termination, and fully accounted bounds. It does not settle a larger arbitrary-dense shared representation or a sharing-resistant lower-bound family.
