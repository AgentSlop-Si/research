# A grouped-coherence refinement for the signed-bank continuation

Status: root derivation, 10 October 2026. Pending independent review of its use in the uniform bank construction. This file does not modify the original author addendum.

Let three orthonormal bases in C^N have cross-basis inner products of magnitude at most N^(-1/2). Select a, b, c vectors from these bases, respectively. For coefficient vectors u, v, w, the selected Gram quadratic form is bounded below by

    ||u||^2 + ||v||^2 + ||w||^2
    - 2 sqrt(ab/N)||u||||v||
    - 2 sqrt(ac/N)||u||||w||
    - 2 sqrt(bc/N)||v||||w||.

This follows by bounding each cross-Gram block by its Frobenius norm. Thus the selected vectors are independent whenever the real symmetric 3-by-3 matrix with diagonal 1 and off-diagonals -sqrt(ab/N), -sqrt(ac/N), -sqrt(bc/N) is positive definite. Empty groups may simply be removed.

In the derivative-annihilation argument of UNIFORM_SQRT_SAVING_ADDENDUM.md, the asserted group counts are

    a = 7d - 10, b = d - 1, c = 5d - 5.

They are bounded by 7d, d, 5d. Let Q be the nonnegative symmetric matrix with zero diagonal and off-diagonals sqrt(7), sqrt(35), sqrt(5), in that order. Its spectral radius is strictly below 8: the leading principal minors of 8I-Q are 8, 57, and 66, all positive, so Sylvester's criterion gives positive definiteness. For the last determinant,

    8^3 - 8(7+35+5) - 2 sqrt(7*35*5) = 512 - 376 - 70 = 66.

Entrywise comparison of nonnegative matrices gives the comparison matrix spectral radius at most d times the spectral radius of Q. Therefore sqrt(N) >= 8d already gives strict positive definiteness; a strict inequality is unnecessary.

Proposed application, subject to checking every other step of the original construction: choose d=floor(sqrt(N)/8), for odd N>=1025, so d>=4. This would give at most

    2N - 2 floor(sqrt(N)/8) + 2

permitted signed banks, or 2N - sqrt(N)/4 + O(1). The coordinate-functional exclusion has smaller group counts and is also covered by these upper bounds. The auxiliary envelope, nonwrapping, dimension, squarefree-pencil, root-incidence, descent, and exact reconstruction steps still require the independent uniform-theorem review. This is a bank-count claim only; it supplies no sub-N log N scalar Fourier algorithm or worldwide novelty claim.

No inherited program was executed for this derivation. The proof uses classical Gram-matrix and spectral-radius estimates.
