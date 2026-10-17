# Independent final-stage review: branch-preserving RS scaling obstruction

17 October 2026. Verdict: **SCOPED ACCEPT. No mandatory mathematical repair found.**

The accepted result rejects the precisely defined normalization-only candidate. It does not close FUS-06, Q20, NF-03, or the wider RS research program.

## 1. Frozen candidate and evidence

Reviewed candidate: `../candidate`.

All 13 members of its `MANIFEST.json` were checked against both byte counts and SHA-256 digests. The exact candidate proof hash is `afc7898a886ac1296351a8ef7c874259b655a0a287ef208df9888e9355a2b167`. The manifest hash and complete member binding are recorded in this review's `RESULTS.json` and `INPUT_BINDING.json`.

The proof, candidate metadata, README, source index, supplied controls, results and copied source/review texts were inspected as inert input. The copied compact-family acceptance supplies the finite legal grid, all-embedding root-radius upper bound 6, explicit finite preparation/precision contract and simultaneous evaluator. The copied previously accepted obstruction/review supplies the canonical-embedding lower bound rho >= sqrt(9/8) for even N >= 44 and |t| <= 1. This review checks the use and scope of those inherited results; it does not claim to have rerun their full preparation algorithms or independently re-certified all of their original proofs. Remote sources were not fetched again, and no external write was made. The candidate directory was not changed.

## 2. Exact physical bank and perturbation theorem

The signed-wrap convention, c_j=q^[j(j-1)/2], and canonical positive q match the accepted source. For even N, c_(j+N)=-c_j. The signed autocorrelation reduces to a geometric sum of q^(kj), proving the stated flat unitary H. Every branch is a rational function of the same unitary signed shift T. Thus all branches are diagonal in one orthonormal basis, which is the essential hypothesis behind the exact norm calculation.

The forward statement is correct for u >= 0:

sup_{|delta_l| <= u} ||H_delta-H||_2 = u chi.

At a spectral point attaining chi, choose each nonzero delta_l b_l to have the same phase. These are single branch scalars, not perturbations that vary independently with spectral position. Hence this is an admissible one-bank perturbation and attains the global norm bound. Zero-residue branches cause no difficulty.

For u chi < 1, all perturbed spectral eigenvalues have magnitude at least 1-u chi. The inverse difference equals |e|/|lambda+e| because |lambda|=1. Align e opposite lambda at a chi-maximizing spectral point to attain

sup_{|delta_l| <= u} ||H_delta^(-1)-H^(-1)||_2 = u chi/(1-u chi).

There is no hidden conflict between attaining the scalar extremum and keeping the other eigenvalues invertible: the uniform bound |e(tau)| <= u chi < 1 handles every spectral point simultaneously.

The domain restriction is essential. If u chi >= 1, the allowed ball contains a singular perturbation: use the same opposing phases with magnitude 1/chi. Even after excluding singular matrices, approaching that perturbation from within the subcritical ball makes the inverse-difference supremum infinite. The candidate does not assert its finite formula in this excluded domain.

Because the exact target and its inverse are unitary, these operator errors also equal the respective worst-case action errors normalized by the exact physical output norm (or input norm). This equivalence uses unitarity and should not be generalized to an arbitrary target without changing the normalization.

### Meaning of the inverse result

The inverse formula is specifically the sensitivity of **inverting the perturbed forward bank H_delta**. It is not a theorem that every implementation of the exact inverse H* incurs that same rational sensitivity. For example, directly applying adjointed perturbed branches gives H_delta*, whose difference from H* has norm u chi, rather than u chi/(1-u chi). The candidate defines H_delta^(-1) explicitly, so its mathematical statement is correct. Any abbreviated downstream description should retain this meaning. No general inverse executor or inverse production cost is certified here.

### Mathematical adversary versus implementable errors

The attainability claim permits independent arbitrary complex relative branch scalars. This is a legitimate, sharply declared mathematical perturbation model. It does not prove that a particular floating-point routine, a real-only coefficient format, correlated coefficient preparation, node perturbations, componentwise rounding, or a fixed deterministic implementation can generate the extremizer. The proof expressly disclaims that broader inference. The result establishes exactly the worst case allowed by this model, not an unavoidable error in every algorithm.

## 3. Compensated bases and radial normalization

For any invertible S, exact preparation S^(-1)x and decoding S make the transformed perturbed sum exactly H_delta. Its inverse decodes to H_delta^(-1) by the same conjugacy identity. This invariance is valid even for nonunitary, nondiagonal or poorly conditioned S, under the same scalar branch perturbations and exact transformations.

It does not identify arbitrary transformed-coordinate entrywise errors with the same physical perturbation set. It also does not assert that forming S, applying it, inverting it, or representing its entries is free. The candidate uses the arbitrary-S statement as an algebraic invariant, not a new complexity guarantee. Compensated scalar factorization is covered only for a relative error on the resulting branch coefficient, as stated.

The scalar radial identities are correct. With a_l=alpha_l/r and T_r=rT, every I-a_l T_r equals I-alpha_l T, and the wrap identity becomes T_r^N=-r^N I. The numerator factor remains 1+a_l^N r^N=1+alpha_l^N. Using 1+a_l^N alone or retaining the old generator would change the bank. The original physical resonances and physical resolvent norms therefore stay unchanged.

Since spectral radius is similarity invariant, every alpha_l S^(-1)TS has spectral radius |alpha_l|. No induced operator norm can make a branch with |alpha_l|>1 into a Neumann contraction. This conclusion concerns the original first-order branch architecture. Reciprocal branches, recombination and new pencils lie outside it.

## 4. Flat-unitary diagonal bound and physical errors

For diagonal D, an entry joining a minimum-magnitude diagonal position to a maximum-magnitude position has modulus kappa_D/sqrt(N) in D^(-1)HD. The same assertion holds in D^(-1)H*D, its exact inverse, because both H and H* are flat. Operator norms dominate entries, so multiplying yields

kappa_2(D^(-1)HD) >= kappa_D^2/N.

This proof works for arbitrary complex diagonal phases and unequal magnitudes. It makes no claim that the target's physical condition number has changed; H itself still has condition number one. The trivial lower bound one can be added when the displayed expression is smaller, as the candidate notes.

The exact physical decoding amplification u kappa_D is also valid in both directions under the stated **relative scaled-output norm contract**. Choose the exact physical output to be a unit coordinate at a minimum-|D| position; unitarity provides an input of norm one. Choose the scaled output error along a maximum-|D| position with magnitude u/min|D|. This satisfies the scaled relative bound and decodes to a physical error of magnitude u kappa_D. Replacing H by H* gives the inverse-direction construction. This can be verified with explicit inputs x=H*e_i and x=He_i, respectively.

Absolute and relative contracts must remain distinct. For an absolute scaled error ||delta z|| <= eta, the worst absolute decoded error is eta ||D||_2. It is not automatically eta kappa_D. Obtaining a relative error also requires the physical input/output norm. The candidate's equation (11) uses a relative scaled-output contract and is correct in that form.

Likewise, a componentwise or weighted-norm guarantee may avoid this unstructured worst case. The theorem does not forbid such an implementation; it requires that its additional error structure be proved rather than inferred from a favorable displayed matrix.

## 5. Uniform exponential consequence and the explicit r=8 family

For D_r=diag(1,r,...,r^(N-1)), the ordinary links are 1/r and the signed wrap is -r^(N-1). Consequently kappa_D=r^(N-1). Both the transformed-target condition bound r^[2(N-1)]/N and the exact decoding factor r^(N-1) follow with the stated exponents.

If r >= rho and even N >= 44 in the retained compact family, rho >= sqrt(9/8) gives the uniform lower bound (9/8)^(N-1)/N. The canonical embedding and |t| <= 1 hypotheses are preserved. The result is not extrapolated from the observed numerical chi values, and no exponential lower bound on chi is claimed.

Choosing r=8 with the accepted least legal compact-grid parameter is fully specified. It neither assumes that t=1/(2N) is always legal nor that t=1 is always legal. The inherited upper radius 6 gives |alpha_l/8| <= 3/4 at every coefficient-field embedding covered by the source. Dividing nodes by a rational number introduces no additional algebraic field extension. Distinctness, nonzero nodes, the original alpha_l^N != -1 guard and possible zero residues are retained. In normalized-generator coordinates the forbidden relation is a_l^N != -8^(-N), equivalently 1+a_l^N 8^N != 0; the physical guard has not disappeared.

The exact powers are kappa_D=2^[3(N-1)] and the condition lower numerator 2^[6(N-1)]. Under the unstructured relative scaled-output contract, guaranteeing physical relative error 2^(-p) requires scaled error at most 2^[-p-3(N-1)]. This is a sharp additional accuracy requirement for that contract. It is not a universal bit-complexity lower bound. Exact binary exponent adjustment still needs sufficient exponent range and does not remove decoding sensitivity, overflow or underflow concerns.

## 6. Preparation, precision, all-output costs, and remaining scope

The ledger correctly retains the accepted 2^[O(p+N^3)] general certified preparation cost rather than replacing it with the O(N) cost of applying the normalization. The current packet does not run that exhaustive preparation. It retains the paid O(N^log_2 3) rational-operation simultaneous forward-bank evaluator and its separate finite-bit contract; a rational-operation count is not a fixed-word runtime benchmark. All N input/output diagonal scalings are counted, and an explicitly dense transformed matrix is not treated as a free data structure.

The exact forward coefficient requirement u chi <= epsilon and inverse-bank requirement u chi <= epsilon/(1+epsilon) are correct. Node errors, branch-solve errors, endpoints and summation errors remain separate obligations. The moment-transform propagation identity E(WVE)^(-1)W delta c=V^(-1)delta c is valid for invertible W,E. It does not turn a worst-case right-side assertion into a lower bound for the one fixed chirp right side.

For arbitrary similarities, preparation and physical transformations may themselves be expensive or unstable. Since no algorithmic benefit is claimed for arbitrary S, the invariant does not silently certify those costs. The detailed explicit execution/range conclusions concern the geometric diagonal construction.

The rejection is therefore exact and narrow: radial normalization or a compensated invertible change of coordinates, by itself, does not improve the declared physical relative-branch sensitivity; geometric state scaling also incurs the proved range/condition penalty. It does not exclude new pencils, genuinely recombined branches, structured preparation, correlated error cancellation, weighted error contracts, practical implementations, or other polynomial bases that change the architecture. It does not establish global owner closure, h-pole optimality, a universal t choice, Q08 stability, practical FFT superiority, or historical priority.

## 7. Fresh independent controls

`independent_controls.py` was newly written for this review. No candidate or historical executable was run or imported. Only installed general-purpose exact/numerical libraries were used.

Completed controls:

1. All 13 frozen manifest members verified.
2. One exact Gaussian-rational commuting normal bank with varying branch signs and a zero branch verifies attainable forward/inverse extrema, two nondiagonal nonunitary compensated similarities, the singular boundary and four near-boundary blowup cases.
3. Three independent rational flat-unitary examples with complex/unequal diagonal scalings verify exact extremizing errors in both physical directions, the distinct absolute-error factor and the extremal entries supporting the condition bound. Numerical singular values are sanity checks only.
4. Nine exact signed-shift/radial/resolvent cases cover N=4,6,10 and real/complex poles inside and outside the unit disk. Forgotten generator compensation is rejected.
5. Exact symbolic threshold arithmetic and dyadic precision/range checks at N=4,44,128,1024 supplement the analytical derivation.

Two initial harness-only assertion issues were repaired before the recorded successful run: ordinary Python integer division had produced floats in one exact comparison, and one complex-polynomial identity needed symbolic expansion before equality comparison. Neither was a candidate failure. The final script and final log are included so the completed run is reproducible. Finite controls support but do not replace the all-N proofs.

## 8. Disposition

**Accept the precisely stated normalization-only candidate as negatively resolved.** No mandatory proof correction is required before recording this bounded result. Retain the inverse-bank semantics, the adversarial-error model and all explicit exclusions when summarizing it. Keep the broader FUS-06/Q20/NF-03 obligations open.
