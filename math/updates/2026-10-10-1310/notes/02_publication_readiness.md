# Publication readiness of the newly accepted results

10 October 2026. Bounded assessment of the 12:20, 12:40 and frozen 13:00 supplements.

## Recommendation

The N5 exact minimum and the real-versus-complex unitary Green boundary are the leading **new manuscript-development packages** in this comparison. The projected Fourier comparator and sharp inverse-neighborhood theorem are the next pair. This is an editorial ordering of the next useful work, not an impact score, novelty certification, journal recommendation, or global ranking of the research collection. Ties reflect different strengths rather than an unsupported fine ordering.

Correctness below means independent mathematical acceptance at the recorded scope, not external peer review. Breadth means the quantified class actually proved. Novelty evidence means the specific primary-source comparison available. Readiness asks whether a coherent standalone manuscript exists and what still blocks a defensible submission. These dimensions must not be collapsed into one rating.

## Existing manuscripts remain the publication baseline

- **[Fourier rectangle rank and dyadic endpoint minimax](../../../drafts/endpoint_rank/manuscript.md).** A self-contained, independently accepted draft already combines the finite-abelian autocorrelation-deficit rank and singular-value bounds with the exact cyclic dyadic independent-order minimax N/4+1. Its [prior-art comparison](../../../comparisons/endpoint_prior_art_20261010/ENDPOINT_PRIOR_ART_ADDENDUM.md) identifies substantial antecedents, including the prior N=8 lower bound and standard quasiseparable terminology. The final Delvaux–Van Barel 2008 full-article comparison is already complete, as recorded under Q05 in [the accepted register](../../../catalogue/STATUS_REGISTER.json). A separate 2007 article, LAA 426, 349–367 (DOI 10.1016/j.laa.2007.05.009), was compared through the TW477 author report; its final-journal verification remains open. Next gate: finish that distinct DV2007 verification and sharpen the exact theorem-difference statement, rather than replace the draft with a newer specialist note.
- **[Local Rogers–Szegő discriminants and composite squarefreeness](../../../drafts/discriminant/manuscript.md).** A self-contained, independently accepted draft already supplies local cluster/discriminant formulas and five fixed-base infinite families, with s in {3,7,11,15,19}, prime p congruent to 1 modulo 4 and p not dividing s. Next gate: obtain and compare the Zhedanov 1997 mathematical body and the missing Lubinsky–Saff reference page, as recorded in the [bounded comparison](../../../comparisons/zhedanov_priority_1119/COMPARISON.md). The gap is priority evidence, not a newly reported failure of its accepted proofs.

Their accepted source hashes are preserved in [the manuscript review record](../../../MANUSCRIPT_REVIEW_STATUS.json). The present assessment establishes no reason to displace either draft. Other historical candidates are outside this bounded comparison; omission does not withdraw them.

## Ranked development groups

### First group

**N5 exact five-bank minimum.**

- **Correctness:** accepted matching bounds: the four-orientation support gate and four-bank exclusion, plus five explicit legal banks over Q(q), prove the minimum is five in characteristic zero. The construction's generic lemma fixes beta=1 and retains its nonzero, distinctness and nonsingularity hypotheses. [Construction and scope](../../2026-10-10-1220/notes/05_n5_five_bank_construction.md), [lower bound](../../2026-10-10-1220/notes/06_four_bank_lower_bound.md).
- **Breadth:** an exact small-size optimum in a specified additive magnetic-bank grammar. It closes a genuine boundary case and complements the odd-size four-bank classification; it is not an all-size optimum or an evaluation-cost result.
- **Novelty evidence:** the bank algebra has close precedents. [Ouvry–Wagner–Wu, Section 2](https://arxiv.org/html/1606.03273) contains a cyclic matrix and determinant whose directed specialization gives the same branch denominator. The [bounded comparison](../../2026-10-10-1220/notes/04_signed_bank_prior_art.md) separates this classical mechanism from the model-specific classification and explicitly does not clear the five-bank realization's priority.
- **Readiness and next gate:** coherent short-paper material, preferably packaged with the full four-bank classification and its stated computational N7 qualification. Write one self-contained synthesis/minimality manuscript; perform a narrowly matched comparison under equivalent quantum-torus and restricted-resolvent terminology. Further bank minima are not required to state the accepted N5 theorem honestly.

**Unitary real-collinear exclusion with its complex counter-scope.**

- **Correctness:** accepted for every N>=4 and any finite number of legal unitary Hamiltonian-cycle resolvents with coefficients on one real line in C, including invertible monomial Fourier equivalence. Actual real N2/N3 witnesses make the lower endpoint sharp. Separately, a fixed legal cycle's finite phase orbit spans all constant-diagonal matrices over C; a column gauge puts every Fourier matrix in that space. [Exclusion](../../2026-10-10-1300/notes/02_unitary_exclusion.md), [complete construction proof](../../2026-10-10-1300/notes/05_phase_averaging_proof.md).
- **Breadth:** all sizes and unrestricted finite term count, but essential single-cycle, unitary and real-collinear restrictions. The complex construction displays at most 3^(N-1) terms and supplies no fast evaluator. This is a different model from magnetic banks.
- **Novelty evidence:** Cayley and finite-character mechanisms are classical. [Rajchel–Gasiorowski–Zyczkowski, Appendix C](https://arxiv.org/html/1804.10715) already uses Haagerup invariants to exclude robust matrices equivalent to odd Fourier matrices. Its fixed paired phase -1 differs from the general paired phase in this theorem; the inspected comparison does not establish historical priority for that extension or the Green application.
- **Readiness and next gate:** a coherent short boundary-classification note. Combine exclusion, small witnesses and complex span in one statement; finish the targeted equivalence comparison with robust/skew-Hermitian Hadamard results and diagonal-conjugacy orbit spans. Do not present the complex result as supporting a broader impossibility claim.

### Second group

**Additive-quotient projected Fourier comparator.**

- **Correctness:** independently accepted for N=2^t and 1<=C<=t, computing all entries of F_N P_C x in O(N+(t-C+1)C2^C), including coefficient preparation and readout, with a supplied primitive 2^C-th root in characteristic other than two. [Algorithm](../../2026-10-10-1240/notes/06_projected_comparator.txt), [final proof receipt](../../2026-10-10-1240/notes/07_projected_comparator_review.txt).
- **Breadth:** arbitrary dense inputs, all dyadic sizes and admissible cutoffs, restricted output rank 2^C+(t-C)2^(C-1). C=t recovers an O(N log N) full DFT; C<t has a nontrivial kernel and no uniform nontrivial relative-accuracy guarantee.
- **Novelty evidence:** [Tóth–Haukkanen, Proposition 2](https://arxiv.org/html/1009.5281) already treats DFT invariance and Ramanujan-sum formulas for gcd-even functions, directly relevant at C=1. The precise higher-cutoff algorithm and root contract remain comparison targets; the packet records an unresolved full-text comparison with Tolimieri's 1986 multiplicative-character decomposition.
- **Readiness and next gate:** enough proved material for a specialized algorithm note, separate from the submitted direct-character evaluator. Finish the fixed-output comparison with classical pruned/quotient and multiplicative-character transforms; then present one complete cost model and algorithm. Numerical stability and benchmarks are additional gates only if practical speed or floating-point claims are sought.

**Sharp inverse-neighborhood approximation.**

- **Correctness:** accepted for every complex unitary U. For t=|I|, m=|J|, 0<=r<t and d=t-r, the inverse-block constraint rank(M^-1[I,J-complement])<=r is feasible exactly when d<=m. Its spectral-norm distance infimum from U is sqrt(1-sigma_d(U[J,I])^2); it is attained exactly when sigma_d>0. [Complete sharpness and boundaries](../../2026-10-10-1240/notes/05_inverse_refinement_review.md).
- **Breadth:** an all-unitary exact optimum for one allowed neighborhood. It does not prove sharpness for global uniform row sparsity or prescribed exact support unions. The separate 4sr/N scalar corollary requires s>=1 and r>=1; r=0 has its own branch.
- **Novelty evidence:** [Lang, Theorem II.1 and equation III.2](https://arxiv.org/html/0812.0172) places inverse-submatrix nullity and spectral low-rank approximation together. These directly yield the lower bound. The precise invertible attaining construction and unattained zero-singular-value boundary are the remaining comparison targets, not evidence of a new nullity principle.
- **Readiness and next gate:** complete theorem-and-sharpness material, but a substantial classical reduction limits the current novelty case. Check exact inverse-pattern distance/completion formulations; package as a short matrix-approximation note or a structural-paper section according to that result.

### Third group

**Schur completion and interface refinements.**

- **Correctness and breadth:** accepted over every field for totally nonsingular targets: minimum strict-upper completion rank floor(N/2), with an invertible triangular residual. Accepted additions include the singular-branch-pivot forward-rank bound, a shared-zero-rectangle bound stronger than LIS, and an exact reordered complex F4 example with interface dimension one. [Complete proofs](../../2026-10-10-1300/notes/06_schur_completion_proofs.md).
- **Novelty evidence:** [Woerdeman, Theorem 2.2](https://arxiv.org/html/math/0608130) already gives the triangular partial-matrix minimum-rank formula. The invertible residual and exact architecture-specific application need their own comparison. Composite Fourier is not automatically totally nonsingular, and prime size does not imply finite-field full spark.
- **Readiness and next gate:** supporting material for a structured-matrix/interface manuscript. Isolate the increment beyond classical completion and nullity before treating this as a standalone paper. Preserve the F4 counterexample and field qualifiers; do not count inherited treewidth and denominator-support theorems again.

**Selected-pair target-only obstruction.**

- **Correctness and breadth:** accepted division-free necessary condition over arbitrary fields, with exact Fourier exclusions at N=4,16,64,256 for pinned six-term baselines and their explicitly specified characteristic-zero lifts. Only the chosen input/output pair changes; coefficients and topology stay fixed. [Proof](../../2026-10-10-1220/notes/01_selected_pair_obstruction.md).
- **Novelty evidence:** the actual elimination uses the classical linear resultant and monomial vector (1,x,y,xy); [Drton–Sturmfels–Sullivant, Theorem 19 and Examples 20–21](https://arxiv.org/html/math/0509390) give this algebraic lineage. Rank at most three is a relaxation, not a sufficient reachability criterion.
- **Readiness and next gate:** a useful specialized certificate/methods section. Explain the reusable Green-family application and compare equivalent bilinear compatibility formulations; a stronger standalone claim needs additional generality or a compelling application, rather than more pinned instances alone.

### Fourth group

**Even-chart rank.** Correctness is accepted uniformly for even N over fields with an exact-order N-th root and the nonzero chart guards: rank N for N=2 modulo 4 and N-1 for N=0 modulo 4. [Proof](../../2026-10-10-1220/notes/02_even_chart_rank.md). Its concise argument is Gauss-sum parity followed by a nonzero last-antidiagonal rank calculation. No separate exact-match priority comparison is recorded. Treat it as a corollary in the chart/bank paper; its next gate is precise attribution and integration. This is separable-representation rank, not arithmetic complexity.

## Construction still open

**Necklace source.** The least-period trace formula, O(N2^c) short-horizon evaluator, guarded sparse Hessian/Gram representation and bounded-locality obstruction are accepted auxiliary mathematics. The source does not construct a uniformly generated inexpensive P with P^T H P=F_N. Q31 therefore remains constructively open. [Accepted scope and missing construction](../../2026-10-10-1300/notes/01_necklace_transport.md).

Classical orbit enumeration and Hessian-vector differentiation remain attributed to their predecessors in that note. A Fourier-algorithm paper cannot pass its next gate without the uniform transport, exact Fourier identity and fully charged preparation/application/transpose costs. Alternatively, an auxiliary trace/locality note needs its own narrow literature comparison. Dense full-rank carriers and small fitted examples do not close either gate. For the canonical trace carrier, characteristic dividing the horizon annihilates the Hessian.

## Evidence boundary

The [12:20](../../2026-10-10-1220/PROOF_STATUS.json), [12:40](../../2026-10-10-1240/PROOF_STATUS.json) and [13:00](../../2026-10-10-1300/PROOF_STATUS.json) records supply the acceptance scopes. This pass reviewed the scientific text, compared the primary passages linked above, and used recorded exact certificates without executing source programs. It does not certify new mathematics, a complete literature search, or the implementation of every submitted program. None of these packages establishes a new unrestricted Fourier speedup or circuit lower bound.
