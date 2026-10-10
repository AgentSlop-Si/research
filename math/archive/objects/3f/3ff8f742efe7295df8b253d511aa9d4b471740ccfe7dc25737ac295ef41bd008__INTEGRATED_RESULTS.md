# Fourier research checkpoint 25: review and content extensions

LOCAL CHECKPOINT 25 CANDIDATE. The source-review snapshot is frozen at 785 accepted reads. Its predecessor is saved Library version 24 with 491 reads; the Library save receipt, not this local package, determines the actual saved version.

## Conclusion and coverage

The research has gained exact, scoped algebraic results and sharper tests for proposed algorithms. It has not produced an exact arbitrary-input Fourier transform using o(N log N) fully charged work. Comprehensive source, dependency, proof and priority review remains unfinished.

The frozen inventory has 906 observed source identities, 1,686 distinct program-source hashes and one separate build-metadata hash. The present static-reading ledger is 184 frozen-inventory reads plus 601 subsequent reads, totaling 785; 901 program hashes remain open. The six new reviews contribute 33 phase26/sparse, 45 fusion/phase, 46 interface/certificate, 45 routed-factor, 45 green-geometry and 80 orbit-geometry reads. All 294 exact hashes are disjoint from the previous 491-read snapshot and have complete source snapshots and line-referenced reviews. Static inspection, source execution, mathematical proof acceptance and dependency closure remain separate evidence levels.

The private inventory's last verified update is 491 reads and 1,195 open hashes, with its saved-master reference updated to version 24. The 785 local total is a later snapshot; this staging task made no spreadsheet or Library change.

## A general sparse-inverse representation theorem

The accepted audit proves that a Fourier matrix over any field containing a primitive Nth root, represented as a sum of r≥1 independently endpoint-monomial-routed inverse branches, must satisfy

N ≤ r(r+1)^r,

provided each inverted matrix is nonsingular and has at most two nonzero entries in each column. No row-degree restriction is imposed. Endpoint permutations and weights may differ between branches, and endpoint weights may be zero. In particular, two such branches cannot represent Fourier for N≥19, including composite lengths in the stated field model.

The proof identifies inverse-row restrictions with a direct sum of one-dimensional component nullspaces after deleting column-labeled graph edges. Any k selected output rows therefore partition each branch's columns into at most k rank-one classes. Refining r partitions and using k=r+1 consecutive Fourier rows gives the bound by a Vandermonde minor. An additional summand with at most δ nonzeros in each row changes the necessary bound to N≤δ(r+1)+r(r+1)^r.

The older two-cycle cut theorem remains preserved as an accepted historical special case, including its coherent-unitary scope. For Fourier representation, its earlier thresholds are superseded by the broader independently routed column-two theorem. The two author-proposal directories are historical drafts; the accepted audit and extension are authoritative. This is a restricted matrix representation result, not a general arithmetic or runtime lower bound, and no global novelty claim follows.

Primary evidence: routed_branch_independent_audit_0439/SEALED_PROOF.md and EXTENSION_AUDIT.md. The separate stronger logarithmic pseudoforest proposal dated 0452 belongs to the next checkpoint and is not accepted evidence in this one.

The inherited FFT_SEPARATION_RANK_THEORY theorem and green-geometry claim C04 already give a stronger Omega(log N) branch bound over the complex numbers for independently routed constant-separation-rank branches. Concatenating bare cycle-block orders preserves separation rank at most one, even with arbitrarily many cycles. Their retained rectangle size m=floor(N/2^r) gives m²≤Nr. The new projective bound is weaker asymptotically on this subclass. Its expanded structural scope is arbitrary attached-tree/high-degree column-two support and arbitrary-field finite bounds; independent routing and unrestricted bare cycle count are not new coverage.

The inherited theorem also already gives the fixed-branch asymptotic operator-error gap: error²≥max(0,m/N−r/m), hence liminf error≥2^(−r/2). The final priority review proves a separate tiny positive finite-N spectral/Frobenius gap for the enlarged column-two class. It is not a positive accuracy barrier uniform in N, an exclusion of practical approximate algorithms, or the first approximation result for bare-cycle branches. Classical gain-graph contraction and Vandermonde full-spark facts remain explicit antecedents; public-literature priority of the precise combination is unresolved.

Final priority reconciliation: routed_branch_priority_0441/SOURCE_LEDGER_AND_CLAIM_COMPARISON.md and FINITE_N_APPROXIMATION_COROLLARY.md. Its preceding seal is preserved as history.

## Five overlap families now have independently accepted proofs

For every prime p congruent to 3 modulo 4 and d in {3, 7, 11, 15, 19}, the half-degree Rogers–Szegő polynomial H_((dp−1)/2)(z; ζ_dp) is squarefree in characteristic zero. The uniform argument requires p not dividing d. Separate, independently rechecked old certificates at N=9, 45, 49, 121, 361 supply precisely the excluded cases for these five families.

The local overlap polynomial is J_(A+1)(y; τ)=y He_A(y)−Aτ He_(A−1)(y). The proof keeps the residual discriminant, residual-cluster resultant and overlap discriminant nonzero. At half degree, the inverse-root parameters satisfy 1/τ+1/τ*=1. The characteristic-p paired-good argument and exact cyclotomic division over the integers provide one good residue factor; goodness in every component is unnecessary.

The independently reconstructed paired contents are 1, 7², 11⁵, 3¹²5⁹ and 19¹¹ for the five bases. In the previously accepted common-cycle scalar-resolvent model with one free diagonal and its legal-node guards, these orders have minimum bank size (dp−1)/2. This remains a restricted-model corollary, not unrestricted inverse-bank optimality or a faster transform.

Primary package evidence: overlap_cluster_extension_0406/RESEARCH_REPORT.md and overlap_cluster_independent_audit_0410/INDEPENDENT_AUDIT.md.

## Exact content valuation and three more fixed-base families

For positive s congruent to 1 modulo 4, prime p congruent to 1 modulo 4, c_s nonzero and p not dividing s c_s, the accepted theorem proves

c_(sp) nonzero and v_p(c_(sp)) = floor(3s(p−1)/8).

In particular, v_ell(c_ell)=floor(3(ell−1)/8) for every prime ell congruent to 1 modulo 4. The proof establishes the integral local product order before upper-root specialization. Its rational-content conclusion uses the minimum valuation over all primes above p, divided by the ramification index and rounded down. A value at one good prime alone would not supply the required global lower bound.

The independent audit reproduces c_17=17⁶, c_21=3¹¹7⁹ and c_25=5¹⁷, including the full coefficient arrays. Thus H_((dp−1)/2) is squarefree for d=17, 21, 25 and every odd prime p not dividing d. These corollaries exclude N=289, 63, 147 and 125 respectively; the new package supplies none of those excluded orders. The scalar-bank corollary also retains the inherited congruence and model requirements.

For d=4r+1≥5, reciprocal contraction reduces the unramified content question to a rank-r multiplication determinant. For p not dividing d, p divides c_d exactly when that determinant element vanishes modulo p, meaning it vanishes in every residue component. No proof that all c_d have prime support only inside d is supplied. General higher ramification and arbitrary-composite squarefreeness remain outside these results.

Primary package evidence: ramified_content_extension_0404/RESEARCH_REPORT.md and content_extension_independent_audit_0420/INDEPENDENT_AUDIT.md. The audit's two scope clarifications, d≥5 for the reduced determinant and an explicit choice of good upper prime, are retained here.

## Content primitivity is still unresolved

The accepted follow-on argument identifies the Galois-orbit ideal of a nonzero cyclotomic integer with its coefficient-content ideal after inverting d, with an explicit integral trace certificate for d times the content. This makes the proposed full-orbit certificate equivalent to the missing primitivity assertion; it does not prove that assertion.

At the actual base d=17 and prime 2, a bad residue factor persists under all powers-of-two conjugates, including complex conjugation, while a conjugate outside that subgroup removes this local obstruction. One good factor remains, so this is not a counterexample to the content-primitivity claim. A separate synthetic perturbation preserves four exact special values while forcing a double root modulo an unramified odd prime. It proves that those special values alone are insufficient; it is not the actual Gaussian polynomial.

Primary evidence: content_primitivity_research_0431/RESEARCH_REPORT.md. This package has parent argument review and scoped fresh controls, not a second complete independent implementation audit. No new full-content base or uniform all-composite theorem is asserted.

## The normalized route is sound, but the available construction is still N log N

Independent review accepts the normalized packet recurrence, orthonormal antichain, O(NL) interconversion with a specified partial Fourier transform, charged mask preparation and integer-triangular chirp reduction. Here n=log₂N and L=Theta(n/log n). It also accepts the O(L) constructive modulation cover and the simultaneous-unitary entropy bound in their stated models.

One marker interval strengthens the ordinary packet-graph obstruction to at least N(n−2b−1) non-input scalar nodes. This applies to that recurrence graph. The separate entropy bound requires simultaneous two-register unitary realization; the earlier unnormalized determinant argument does not apply to the normalized interface. None is a universal Fourier-circuit lower bound.

The selected frequency set has a small header mask and is a union of equal contiguous blocks. A fully charged blocked Cooley–Tukey construction using only the supplied roots still computes Q complete length-B input transforms first, costing N log B=Theta(N log N). Pruning its short outer stage does not remove that cost. Exact Hankel, modulation-orbit and binary-digit unfolding ranks also reject narrowly specified short-recurrence or tiny-state compression shortcuts. They do not rule out different general circuits.

The missing result is still a faster exact selected-convolution algorithm with all preparation, constants, routing and output costs paid. Early-time outputs, causal recovery, full-transform recovery and finite-precision/bit costs remain additional obligations.

Primary package evidence: normalized_frontier_independent_audit_0422/INDEPENDENT_NORMALIZED_FRONTIER_AUDIT.md and selected_convolution_construction_0421/SELECTED_CONVOLUTION_CONSTRUCTION.md. The latter is an accepted scoped construction analysis with its own exact controls, not a separately completed independent audit of every new rank argument.

## Priority is narrower after exact antecedent comparisons

The overlap polynomial is a standard gap-two Hermite combination and, by parity, a quasi-Laguerre pullback. Its standalone ordinary discriminant follows from established quasi-orthogonal formulas. The characteristic-p Wronskian identity is an exact hook-partition specialization of existing pseudo-Wronskian equivalence and congruence results. Cyclotomic ramification and the final content floor conversion are established ingredients.

The strongest surviving candidate contribution is the explicit shared-root local coefficient at a fixed nontrivial odd root of unity, its full ordinary-discriminant coefficient and its arithmetic applications. The inspected primary sources did not establish an exact antecedent for that combination. This is a bounded literature result, not certification of originality. Complete legitimate comparisons with Lubinsky–Saff (1987) and Zhedanov (1997) remain outstanding. No public posting, submission or outreach was performed.

Primary package evidence: overlap_valuation_priority_0421/DECISION_MEMO.md, PRIMARY_REDUCTIONS.md and CLAIM_SCOPE.md. The accepted scoped_mathematical_note_0432 package supplies a private manuscript outline, theorem dependency map, publication gate and one-page significance brief; this editorial synthesis adds no independent theorem certification.

## Source-review findings that change how evidence should be used

- The preserved exact N=3 offset counterexample rejects the generic executed offset-planner certificate. It does not reject direct coordinate-median theory or establish a saved Bessel output violation. The saved nontrivial Bessel certificate remains unsupported for the actual dispatcher settings.
- Six of fifteen saved v14 binary64 benchmark rows fail their stated stability threshold. Algebraic exactness is a separate claim. A saved experiment JSON also omits an unconditional section of current source; co-sealing source and output does not establish execution attribution.
- Direct-script test-runner placement can omit later test classes, but the examined discovery/module run logs include their full groups. Those stored runs should not be called truncated.
- A complex sparse-phase prototype can fail open on NaN by static branch analysis. No supplied source was run to establish that diagnosis, and the scoped finite-field algorithm is separate.
- The finite F8 contraction certificates are positive existence evidence for a fixed three-stage quasiseparable factorization. They are different from the adjacent-anchor inverse-sum exclusion, whose simpler explanation remains the classical cut-rank proof. Stored rational inequalities were checked; the interface review did not recompute the matrix residual or inverse Jacobian.
- Structured-shear shortcuts retain fixed-order, clean-pilot and sparse-innovation hypotheses. Work counters, public certificates and finite-field checks are not universal runtime or complex-field proof certificates.

The next three reviews additionally identify underweighted scan-order capacity outside the sampled r=1 regime, checkers that can omit required witness lists, incomplete operation ledgers and a replay wrapper that pre-copies expected outputs. The green-geometry review verifies scoped graph-cut and rank results while exposing a missing inverse-nonsingularity guard in a polynomial residual checker. These are specific evidence and API limits, not blanket invalidation of the source mathematics.

Primary package evidence: phase26_sparse_source_review_0406/CLAIM_DISPOSITION.md, fusion_phase_source_review_0408/REVIEW_REPORT.md, interface_certificate_source_review_0418/REVIEW_REPORT.md, routed_factor_source_review_0432/REVIEW.md, green_geometry_source_review_0430/PROOF_AND_SCOPE.md and orbit_geometry_source_review_0436/REPORT.md.

## Preservation and remaining scope

All inherited master bytes were checked before staging. New accepted packages are detached byte-for-byte copies with verified original seals; historical absolute paths are preserved as provenance and mapped to retained local evidence by PROVENANCE_CHECKS.json. This staging pass runs only freshly authored metadata/packaging helpers, never supplied source, historical audit programs or inherited integration scripts. A source seal attests bytes, not correctness or a rerun.

Missing historical versions, unresolved execution attribution and unreviewed dependencies remain explicit. The entire research review is not complete, and the upload-resume completion notice must not be issued.
