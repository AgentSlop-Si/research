# Independent acceptance review: global C8 rank-zero minimum

20 October 2026 UTC.

## Verdict

ACCEPT the exact global optimum in the original unrestricted complex-monomial, real-core, rank-zero, external-operator-norm model:

    delta_(8,0) = (1/2) sqrt(1 + sqrt(sqrt(2)-1)).

The accepted scope includes arbitrary nonperiodic phases. It does not classify every minimizer, assert that every minimizer is four-periodic, or settle any positive correction rank. No owner record or external service was changed by this review.

## Exact reviewed source

Candidate: candidate/PROOF.md
SHA-256: 776acb79b13199fe5b52c5e352c89135b93ff8100848cbc78598969a53fd7936
Bytes: 12732.

Separate independently derived analytic proof: PROOF.md in this review directory.
SHA-256: 773e372f70ff1494310d0e8daa3c07aaf69473364f8e595fd7d734a9ac76a191
Bytes: 10375.

The independent proof uses a complete compact-maximizer/KKT boundary analysis for the scalar inequality. The candidate uses a different, simpler opposite-pair balancing proof. Both have been checked independently. Source hashes also bind the previously accepted exact witness and its review.

## Principal challenges and resolutions

1. Original-model equivalence is exact. Real monomial magnitudes and permutations are absorbed into the unrestricted real core; no nonunitary residual norm is substituted. The transformation from W=(PFQ)^T(PFQ) to F A F B is unitary similarity, and every diagonal unitary A,B has legal diagonal-unitary square roots.

2. The all-phase periodicization is valid. C=FAF commutes with the half-shift for every A, not just a periodic A. Averaging B with its shifted conjugate gives E=DT. For normal unitary Z=CD and an eigenvector x, x*Z=lambda x*, so x*Herm(ZT)x=Re(lambda)x*Tx. This forces Re(lambda)>=c when c>0 and 0<=T<=I. No commutation of Z,T is assumed. Cyclic unitary similarity allows the second diagonal factor to be normalized in the same manner without changing the first.

3. All four sectors are retained. A fresh full eight-by-eight calculation verifies every sector entry, normalized Fourier factor, trace, determinant, and off-sector zero. The determinant product has the essential minus sign. Actual principal eigenphase midpoints give a signed sum equal to pi/2 modulo pi; the absolute-sum lower bound pi/2 is therefore branch-safe.

4. The trace matrix is a genuine contraction. Its Hadamard factors have unit row and unit column Euclidean norms in the appropriate orientation, so Cauchy-Schwarz applies to arbitrary test vectors. No unproved spectral surrogate is used.

5. The candidate's pair-balancing inequality is correct. Interior contractions can be moved to the norm-one boundary by increasing both off-diagonals. The boundary determinant gives the required quadratic root restriction q<=q_max; its other root is strictly above one. The cosine of the two-arcsine sum is strictly decreasing in q, and both compared angles lie in [0,pi]. The balanced matrix is a legal contraction, the lower-entry threshold is preserved, and the second pair balancing plus convex endpoint maximization yields the sharp four-angle inequality.

6. The independent KKT proof covers every face. Compactness, positivity, strict convexity, and the one-free-singular-direction perturbation handle no active entry constraints. Smoothness follows from f_d<0 in the exactly-one-active case; the stationary factor has a strictly positive first factor, forcing symmetry, where the explicit derivative contradicts maximality. Adjacent and opposite pairs cover all cases with two or more active lower bounds. For the needed fixed threshold m, the adjacent-case range restriction is rigorously satisfied.

7. The fixed-threshold use is important and correct. Even if a hypothetical better point has cos(theta) larger than the independent lemma's stated parameter range, apply that lemma with the fixed m=(1-sqrt(sqrt(2)-1))/2. The contradiction is between 4 theta-pi/2 and 4 theta*-pi/2. No extension of the independent lemma beyond its proved range is required.

8. The exact attaining phases remain legal. Fresh controls verify their actual square roots and all four block traces and determinants. Together with the radical/angle identity this reproduces the endpoint and its full spectral branches in the same external norm.

## Computation and integrity

The newly written check_exact.py passes 375 exact assertions in 2.100272498006234 seconds of reported checker runtime. It checks the unrestricted shift identity, generic full sector decomposition, determinant-center sign, both scalar-proof algebraic identities, threshold radicals, actual P and Q phase squares, witness traces/determinants, and a genuinely noncommuting normal-factor control. A destructive control rejects the wrong determinant product sign.

No numerical optimization was run for this independent review. No historical or candidate checker was imported or executed. The candidate's numerical-search provenance is not independently measured here and is not a premise of acceptance.

Checker development had two resolved implementation errors: an incorrect sign when subtracting a polynomial identity in the checker, and an ordinary Python integer needing sympification. Neither changed the mathematical proof, witness, or frozen candidate. A prior 355-check algebra-only run passed before witness controls were added; the final 375-check run completed successfully. No pending calculation remains in this independent review.
