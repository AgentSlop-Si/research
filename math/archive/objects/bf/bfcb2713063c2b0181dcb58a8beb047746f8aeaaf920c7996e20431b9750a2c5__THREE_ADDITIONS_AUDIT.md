# Independent audit of the three additions received at 15:19 UTC

9 October 2026. This supplement advances and corrects the prior Fourier research record; it does not replace its historical sources. The 349-item Library snapshot, 528 canonical text contents, and 14:50 additions retain their own dated inventories.

## Result in brief

The additions strengthen the exact feasibility formulation, improve the approximate decoder's structure and memory, and sharpen a restricted unitary-stage obstruction. They do not establish a new exact arbitrary-input sub-N-log-N Fourier algorithm. The approximate guarantees, finite-field polynomial checks, pair-unitary lower bounds, and unrestricted complex arithmetic goal must remain distinct.

All original archives were materialized as data, safely inspected, and retained unchanged. No uploaded Python program was executed or imported. Every executable check in the audit directories was newly authored independently.

## 1. Algebraic inverse and Fourier-support gate

The preceding two-stage F8 chart used 30 equations in 26 variables, of degree up to 28, to eliminate the second separated-generator stage. The new inverse chart and Fourier support reduction give materially smaller formulations on their own regular loci:

- Inverse-stage chart: 30 quartics in 26 variables, 1,268 exported terms.
- Fourier-support reduction: 25 sextics in 21 variables, 1,749 exported terms.
- Complete separated-generator lift: 176 quadratics in 184 variables, 800 exported terms.

The independent checker reconstructs and compares every exported coefficient, not merely the equation counts. The removed Fourier-support constraints cancel symbolically. The complete lift includes zero-anchor cases within the stated globally separated-generator stage model, while the smaller systems require their explicit regular-patch inequalities.

Important retained caveats:

- The old chart normalizes diag(A), while the inverse chart normalizes diag(A^-1); their regular loci differ. For N=8, A=(7/6)I-(1/6)J has diagonal one and nonzero anchors, but A^-1=(6/7)I-(6/7)J has diagonal zero. Therefore the degree-28 to degree-4 change is not an unconditional equivalence on every old-patch point.

- Inverting a separated stage preserves quasiseparable cut ranks but can leave the globally separated chart when corner anchors vanish.
- A singular all-ones inverse candidate satisfies the unsaturated quartics and is not an actual Fourier factorization.
- A polynomial solution on the regular patch, or a certified exclusion together with exceptional-patch coverage, has not been found.
- Finite-field polynomial equality checks validate the exports. They are not by themselves a characteristic-zero feasibility or impossibility certificate.

The independent extension factors the two inverse-corner cofactors into an endpoint anchor and six local gaps. This converts the previous verbal inverse-anchor requirement into explicit saturation factors without a dense adjugate expansion. See `inverse_audit/` for the formulas, proof, exact coefficient comparisons, and exhaustive/sampled controls. On the required t!=0 locus, 11 equations also have removable t factors. Their primitive equivalent list has four cubics, six quartics, one quintic and fourteen sextics. The entire all-other-coordinates-equal-one beta-line remains a singular false-positive family before saturation. An unoptimized degree-59 product of nonzero factors yields a degree-60 reciprocal equation, so headline degree six excludes saturation. The formulation is now more precise; the exact feasibility question remains open.

## 2. Streaming-majority v8

The supplied v8 adds a unit-modulus gauge transformation that changes each two-cycle recurrence into a prefix sum. A balanced scan has linear work and logarithmic accumulation depth. This repairs the serial accumulation path length; it does not alone bound errors in roots, summaries, FFTs, seeds, range handling, or cell classification.

The three-shift grid lemma is sound in exact arithmetic. If a strict majority of real observations lies within tau of a target, grids of width 7 tau with offsets 0, 7 tau/3, 14 tau/3 have at least two safe grids. Each safe grid's majority-cell center is within 5 tau/2. The median of the three Boyer–Moore candidate centers retains that bound.

Using the previously verified per-output covariance and independent rows gives the supplied complex-output radius 5 g sqrt(M/N)||x||2 and failure bound 2N exp(-R D(1/2 || 1/g^2)), for the stated dyadic factorization and g>sqrt(2).

There is a computational-model qualification: constant-time exact cell quantization/floor is an additional primitive. Showing that cell IDs fit in O(log N) bits does not implement that primitive in an arithmetic-and-comparison model. The prior five-counter comparison-only selector remains an alternative if such a primitive is not allowed. Both are approximate estimators; neither computes arbitrary Fourier outputs exactly.

The independent precision audit in `v8_audit/` supplies a complete specified row implementation with deterministic error at most 800 sqrt(NM) log2(N) u ||x||2 when 8u log2(N)<=0.01. It charges certified roots at guard precision, normalization, norm-envelope preparation, exact modular indices, valid numerical range and exact represented-grid classification. Choosing u<=theta g/[800 N log2(N)] and inflating a common certified grid radius preserves the approximate error exponents with explicit larger constants. O(log N)-bit mantissas suffice in the stated bounded-input regimes; arbitrary input bits and full bit costs remain charged. This theorem must not be attributed to the original source's conditional scan statement or to its mixed-precision NumPy tests.

## 3. Phase16 entropy and Green Givens compiler

For the model of in-place two-coordinate unitary gates, each gate raises matrix entropy by at most two bits. The known argument is attributed to Nir Ailon. The project-specific Phase15 factorization saturates the bound gate by gate and has component entropies

- base bank: N log2 B;
- normalized residual fold: N-B;
- orbit bank: B+N(log2 L-1).

Their sum is N log2 N. This independently corroborates the preceding Phase15 audit rather than reopening a path to savings by reordering these same pair-unitary gates.

The path Cayley compiler gives at most 2N-3 pair gates plus scalar phases. Together with the Haar involution compiler, one full Haar–Green stage uses at most (11N/2)-8 pair gates. Therefore a product of t such stages, their inverses, permutations and unit phases that is exactly normalized Fourier obeys

t >= N log2 N/(11N-16).

This improves the earlier compiler's additive constant and permits size-dependent real strengths. It is not a lower bound for unrestricted arithmetic or nonunitary shared-work algorithms, and does not claim linear-time preparation of all Givens parameters.

The independent checker includes zero and signed couplings, large couplings, complex Hermitian path edges and on-site diagonals. A generic extension of the fixed nearest-column pivot rule fails on a degenerate rank-one unitary. Adaptive prefix pivoting repairs that case without increasing the gate count; the irreducible path theorem is unaffected. The exact example and repair are in `phase16_audit/`.

The independent extension makes the restriction robust to fixed approximation error for an exactly unitary stage product. If its operator-norm error is <=epsilon, or its Frobenius error is <=epsilon sqrt(N), a continuity bound for column probability entropy gives the corresponding explicit stage bound. For every fixed epsilon<1, it is still Omega(log N). Zero-initialized extra registers do not evade the pair-unitary gate count. These statements do not transfer to the nonlinear randomized chirp estimator. Free complex phases matter: original stages have determinant one, whereas the normalized Fourier determinant is +/-i for powers of two N>=4; without these phases exact equality is already obstructed.

## 4. A useful corollary for the proposed fusion

Noncommuting Green resolvents escape a common-base rational-function description, but they do not automatically escape aligned cut-rank constraints. A sum of r common-order tridiagonal inverses, even with independently chosen diagonal masks, has aligned cut rank at most r. Products of such sums obey the additive expanded-expression budget. The inverse cut-rank identity holds even when principal blocks are singular.

In standard Fourier ordering a balanced cut is a full-rank Vandermonde block, requiring budget at least floor(N/2). With arbitrary endpoint permutations the uniform lower bound is ceil(floor(N^2/4)/N). See `fusion_audit/ALIGNED_RESOLVENT_GATE.md`.

This is a specialization of the earlier quasiseparable inverse/subadditivity facts, not a newly discovered general lower bound. Independently reordered paths and shared-state computations outside this representation require fresh analysis. Passing a rank test never establishes the full Fourier coefficient identities.

## 5. Provenance and reproduction

The three source archives contain 477 recursive file occurrences and 298 unique byte contents. Relative to the baseline canonical texts and 14:50 source-member inventory, 58 unique contents are new: 22 in the inverse gate, 9 in v8, and 27 in Phase16. These figures include programs, logs, manifests and archive wrappers; they are not counts of independently proved theorems.

All 633 embedded SHA-256 manifest entries passed. `SOURCE_ARCHIVES.json` retains exact Library/file identities, versions, names, timestamps, sizes and hashes. `SOURCE_MEMBER_INVENTORY.json` retains recursive archive chains. `PRIOR_HASH_REFERENCE.json` binds the inventories used for deduplication. `audit_provenance.py` reruns these checks entirely locally.

Exact symbolic identities, finite exact controls, numerical stress checks, proved statements, source-only claims and open feasibility tasks are distinguished in each branch report. The top-level verification file records only the independently authored scripts actually run in the portable layout.
