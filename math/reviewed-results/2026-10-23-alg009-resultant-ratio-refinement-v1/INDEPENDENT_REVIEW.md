# Independent review: ALG-009 three-raw-ratio recovery

23 October 2026 UTC. ACCEPT the final scope-revised candidate at MANIFEST.json SHA-256 359b52031c4ce255b803de6d88fd9deb53e9a9beb9c34f321f8ae7f3063beb0e. Exact file bindings are supplied separately in VERDICT.json.

## Mathematical finding

The proposed mechanism correctly removes the specialized linear-gcd condition from the source-named nonzero-resultant recovery branch. It does not remove the nonzero-resultant requirement, the full raw-data certificate, the nonzero multiplier requirement, the one-or-two-defect admission, or the at-most-one-pole budget. The uniform proof is elementary and exact; finite controls supplement it rather than establish it by extrapolation. Both displayed strict-selector witnesses were already accepted by the older ratio branch, so no strict full-hybrid coverage expansion is established.

This is a strict recovery-family extension relative to the named Phase20 selector. It is not a claim that every previous hybrid detector fails on the witnesses, nor a historical-priority claim for ratio recovery or resultants. No historical or candidate program was executed or imported by this reviewer. Only the separately authored independent_controls.py was executed.

## Exact source and input model

The original Phase20 theorem was read in full, SHA-256 b49a3863273c2c80cb211e71711d0575cd3ac96bac32f4ac293f48a77b0f7ec9. The corrected source selector was read as inert text, SHA-256 09ef37694af956394b82f55bf366e121849cbaf7f4d89caff5527aad9a142ef4. Its immutable repository location is:

https://github.com/AgentSlop-Si/research/blob/1dadcbac912a22c88ad0950bc0488978b5bf919d/math/finalized/2026-10-16-source-repairs-0126/alg009_static/corrected/resultant_gate.py

The source explicitly computes a specialized polynomial gcd at each retained shift and skips it unless its coefficient-list length is two. The theorem explicitly calls degree-one gcd an algebraic nondegeneracy hypothesis and leaves higher-degree gcds outside its recovery guarantee. Thus this is a source-named live gate, not an unselected general observation attached retrospectively to another problem.

The reviewed comparison report, SHA-256 521efc5a7291d062862246ed16d5e4448e75a13ac32e810b10e9665051bfbedf, makes the complete input/interface contract explicit. The mathematical residual input is a supplied raw vector r in GF(p)^N, N >= 8, certified prime p > 55, and a supplied element omega of exact order N. Existence of that root implies p does not divide N. The prime-field/root resources are inputs, not free algorithms for finding fields, generators or extension representations.

The ratios use raw coefficients r_i. They do not use Fourier values. Eight direct dot products R_k = sum_j r_j omega^(kj), k=0,...,7, are separately paid. Only the first six enter the two Hankel cubics. Acquiring eight rather than six preserves the source probe interface and remains linear. No full Fourier vector is supplied to the recovery algorithm.

For the original input x, r = P x must first be formed and paid, with P = 7I + S + 2D^(-1). After all residual Fourier coordinates are reconstructed, y = L^(-1)R, L = 7I + 2S + D, is paid. The Green identity gives y = F x. This transfer requires separately valid Green setup and solvers; mere matrix nonsingularity is not enough for the historical diagonal-inversion constructor. The inherited zero-diagonal and additional fallback-root qualifications remain in force. The new raw-r core is not an execution of that historical wrapper.

## Universal coverage proof and edge cases

Write h_j = r_j - alpha r_(j-delta mod N), with alpha nonzero, 1 <= delta < N, and 1 <= |supp(h)| <= 2. The positive-sign Fourier convention gives Y_k = R_k(1-alpha w^k) = (Fh)_k at w=omega^delta. Therefore the two 3-by-3 Hankel determinants P_0 and P_1 vanish at the true alpha, including at resonant Fourier bins. They are padded cubics in alpha. Their fixed 6-by-6 Sylvester determinant T(w) has degree at most 45 in w: the coefficient degrees are at most six and nine, and every Sylvester term takes three coefficients from each cubic.

Padding is essential to the stated T. A true common finite alpha root makes the padded determinant zero even when degrees drop. Conversely, padded degree drops can introduce spurious roots; the new method never treats a resultant root as a certificate. It does not replace the padded resultant by a variable-size resultant or silently cancel alpha=0.

If r has at most two nonzero coordinates, its Fourier sequence is a sum of at most two geometric sequences. At alpha=0, both Hankel determinants then vanish for every w. Equivalently, both polynomials in GF(p)[w][alpha] have zero constant coefficient and hence the common factor alpha (with the zero-polynomial case included). The padded Sylvester determinant is identically zero. Thus T nonzero implies at least three nonzero raw coordinates; it is always possible to choose three distinct indices i_1,i_2,i_3 with r_i nonzero.

Fix those three indices once. For each retained shift delta, form q_i = r_(i+delta mod N)/r_i. Then

q_i - alpha = h_(i+delta mod N)/r_i.

Translation modulo N is injective on distinct selected indices, whether or not delta is coprime to N. At most two selected target coordinates can be in supp(h), so at least one of the three ratios equals the true alpha. This handles overlaps between anchors and defects, wraparound, short shift cycles and periodic shifts without an extra assumption. Every denominator was explicitly selected to be nonzero. A ratio with zero numerator may be zero and is safely rejected because the promised alpha is nonzero. Duplicate ratios may be retried; deduplication is unnecessary for the bound.

The true w is retained by the exact T scan. Nonzero T has at most 45 distinct field roots, and exact order N makes omega^delta distinct for delta=1,...,N-1. The field-polynomial root bound does not fail when N <= 45, and no discrete logarithm or polynomial-root oracle is needed. Up to three ratios per shift give at most 135 proposals. At least one is the true alpha for every promised admissible description. An earlier different accepted description is equally sound, because acceptance depends on a complete raw certificate rather than parameter uniqueness.

The method retains the N >= 8, p > 55 source domain. The three-ratio identity itself works more generally, but the finite GF(3) controls do not extend the complete interpolation theorem to characteristic three. The 46 nodes 0,...,45 are distinct under the retained field hypothesis. T identically zero remains an explicit decline, not a proof that no model exists. Zero defects also remain outside the admitted one-or-two-defect class.

## Pole budget and complete output

Let g = gcd(delta,N). The map k -> omega^(k delta) has image of order N/g, with g preimages per image point. For alpha nonzero, the denominator has Z=g zeros if alpha^(N/g)=1, and Z=0 otherwise. Therefore the allowed shift domain is not restricted to coprime shifts: noncoprime, nonresonant descriptions remain valid. Noncoprime resonant descriptions with g>1 are rejected rather than receiving an uncharged repair.

The new core counts actual zeros while scanning all N denominator entries for every proposal whose defect scan passed. This is O(N) per proposal and needs no gcd or field-power oracle. Accepted descriptions satisfy Z <= 1. Every nonpole R_k is obtained from the certified one/two-term H by direct geometric streams and division. Every admitted pole is obtained by an actual direct Fourier sum of raw r. No cancellation or removable rational continuation substitutes for its input-dependent value. The all-coordinate defect identity proves the entire output, including cases whose first eight probes are misleading.

## Complete all-path cost audit

The inspected new paid_executor.py uses the following schedule, distinct from the incomplete historical operation proxy:

1. Validate canonical input encoding and build the supplied-root table with N-1 products; verify exact order by testing the generated powers and the final Nth power. Input reads, allocation and indexing are O(N).
2. Form exactly eight direct Fourier samples. Its explicit stream routine uses 2N products and N additions per sample, including the final unused phase update. Thus these probes cost 16N products plus 8N additions, not a free spectral oracle.
3. Form the two padded cubics and evaluate the fixed 6-by-6 determinant at 46 nodes, then interpolate. Signs, coefficient arithmetic, scaling, determinant inversions, divisions and trimming tests are charged. The amount is independent of N, not zero. The theorem's degree proof supplies exactness; the new core need not inherit the old three redundant evaluation checks.
4. Scan the N-1 nontrivial subgroup nodes with a polynomial of degree at most 45. The literal zero-initialized Horner loop has at most 46 products and 46 additions per node. Root admission supplies both the node and its shift index.
5. Scan raw r for three nonzero anchors and invert only those three entries. There are at most 135 ratio products/proposals. Each attempted defect scan is charged, including an early rejection after the third defect. Every potentially accepted proposal scans all N entries. Each successful defect scan then incurs the complete O(N) denominator/pole scan, even if subsequently rejected for multiple poles.
6. For the first admitted certificate, evaluate every numerator through at most two geometric streams, perform every nonzero denominator inversion and product, write every output, and perform at most one complete direct pole sum. These are O(N) operations and O(N) field slots. No full-length FFT, polynomial factorization, generic field-root search or discrete logarithm is hidden.
7. On decline, the preceding work remains paid. The new executor's optional direct fallback costs O(N^2), not O(N log N). A separate admissible exact FFT fallback can recover the historical O(N log N) all-input bound only with its own additional roots, setup, operation charges and valid wrapper domain. Unsupported input domains are not silently covered.

All field arithmetic in the inspected core is routed through its Meter methods; exact tests are separately counted. The review accepts the all-path linear pre-fallback schedule and the stated field-operation model, not a hardware-time or bit-cost estimate. Runtime integer indexing, reads, writes and allocation remain O(N) for fixed constants in an O(log N)-bit index-word model, with field-element widths treated separately. Prime/root discovery and field representation construction are not performed. Supplied-root exact-order checking is performed and charged. The original literal implementation ledger remains an open, separate obligation.

The ledger's conservative bound of 500,000 + 804N + 138 field operations is valid for this new raw-r executor. Independently counting the fixed loops gives at most 205 operations per cubic, five power products, and at most 172 operations per padded determinant elimination, or at most 587 per resultant value. One direct Lagrange basis costs at most 4,369 operations. The total fixed algebra is therefore at most 46(587+4,369)=227,976, safely below 500,000. The linear coefficient is the sum 2+24+92+270+405+11=804, and the remaining constant counts three anchor inversions plus 135 proposal products. Zero tests and index/read/write costs remain separately explicit. The historical Green wrapper is not included in that raw-r scalar total.

## Independently verified strict witnesses

The author's N8 witness was checked by fresh algorithms: numerical 3-by-3 Hankel determinants followed by four-point interpolation in alpha, direct signed-permutation evaluation of the padded 6-by-6 determinant, an independent polynomial Euclidean algorithm, and direct DFTs. All 46 degree-bounding evaluations agree with the supplied resultant coefficient list. Its only nontrivial root-grid shifts are 1 and 7, and both specialized gcds are quadratic. T(2)=78. A supplied-root Green lift also has nonzero constructor diagonals and det(P)=det(L)=28 modulo 97.

The reviewer independently found and verified the preferable N16 witness, where eight probes are not the complete transform:

- p=97, N=16, supplied omega=8;
- r=(80,4,42,70,52,22,69,18,30,50,51,85,77,96,63,8);
- delta=1, alpha=34, h_0=2, h_2=3, every other h coordinate zero;
- T(2)=46; the only nontrivial subgroup resultant roots are delta=1 and 15;
- the respective monic gcd coefficient lists, in ascending powers, are (77,75,1) and (63,69,1).

The old linear-gcd selector therefore skips every subgroup candidate. The new raw ratios include alpha=34 and the full certificate succeeds with no poles. The complete residual output is

(41,0,22,23,10,94,75,18,14,0,67,75,18,40,51,53).

This witness also belongs to the original supplied-root Green input model. The exact input is

x=(19,18,6,6,4,12,34,88,66,12,33,35,75,56,64,6).

Independently solving the two finite linear systems verifies P x=r and L^(-1)R=F x, with full output

(49,84,28,19,86,60,86,94,68,39,7,60,65,74,0,67).

All P and L constructor diagonals are nonzero and both determinants are 71 modulo 97. This is a theorem-level supplied-root witness. No compatibility with the historical default generator is assumed, and no historical constructor or full hybrid was run.

Separate exhaustive GF(3) ratio-only controls covered 2,992 raw vectors with at least three nonzeros, 2,360 qualifying descriptions and 29,344 choices of three anchors, including 664 noncoprime descriptions and 5,328 anchor sets containing a zero ratio. All coverage and exact failure-identity checks passed. Another 296 controls verified the sparse-input alpha-zero/padded-resultant mechanism. The small-field checks test the ratio lemma, not the p>55 complete algorithm. These finite controls do not substitute for the universal proof above.

## Targeted comparison with the existing hybrid

The original Phase20 archive was independently hash-checked at c20b633a0e8a7be1ee81ab65765a15e3fb77a39d3315c7139cef5d88aa1333c3. Its nested Phase19 archive is ab110c544f28b8c2d6e750ffcd07776a036de2f8c5ed8ff0dd805b5eccfbdd55. Relevant extracted sources are retained as inert text evidence with exact hashes in sources/FRONTIER_SOURCE_BINDING.json. This targeted check did not execute any archived source.

Phase19 Theorem A guarantees coprime one-defect recovery on nowhere-zero data. Its Theorem B guarantees bounded-defect recovery under a nowhere-zero/coprime-shift, wrap-class-separation contract. The implementation proposes shifts through adjacent-ratio counts, then obtains alpha by a five-edge raw-ratio majority for K=2. Raw-ratio recovery at a proposed shift is thus an existing project ingredient, not novel here. Theorem C covers sparse circular inverses C(S)r=e_0, which force every Fourier coordinate to be nonzero. These are different promised families, not a theorem that T nonzero alone implies their hypotheses. The alternate blind_sparse_rational implementation also explicitly requires a specialized degree-one gcd. The hybrid source runs the ratio route, then sparse inverse, then the linear-gcd resultant gate.

The N16 witness has adjacent-ratio class sizes 14,1,1; the N8 witness has sizes 6,1,1. In each case subset-count u=1 proposes delta=1 and the first five edges have a strict majority equal to the generating alpha. The original full raw certificate therefore passes. Both witnesses are already accepted by the old Phase19 ratio branch, before the resultant gate is called. The independent controls verify these counts and majorities directly without executing the old program.

No inspected predecessor theorem states the new complete nonzero-T/one-or-two-defect/at-most-one-pole guarantee. The contribution is a simpler integration/coverage theorem for the named resultant branch, using three nonzero-anchor proposals and fully charged certification/output. Absence of an identical predecessor theorem is not proof that the union of all old branches has smaller coverage. A strict full-hybrid extension, net runtime improvement on these witnesses, and historical novelty are expressly unestablished. Final PROOF Section 8, README and SCIENTIFIC_RESULT.json now state this limitation; the earlier freeze is not the accepted version.

## Scope retained

Accept only the source-relative selector recovery extension and its conditional linear exact-field schedule at the exact final pins. No strict full-hybrid coverage increase, zero-resultant completeness, unrestricted sparse-rational interpolator, complete original-implementation execution, literal historical ledger, whole-owner closure, historical novelty, numerical stability, bit complexity, hardware speedup or generic FFT improvement follows. The two reviewed primary-source comparison outcomes remain qualified nonmatches for the complete fixed-grid raw-data recovery contract; this review makes no new global literature-priority claim.
