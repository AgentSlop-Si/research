# Block-coherence refinement: a uniform constant-eight bound

10 October 2026. Separate author refinement, pending independent review. Neither WHOLE_LEFT_RANK_ENVELOPE.md nor UNIFORM_SQRT_SAVING_ADDENDUM.md is modified. This note replaces only the conservative scalar coherence estimate in the latter proof; the explicit recurrence, row-compatibility and legal-bank constructions are unchanged.

## Statement

For every odd N≥1025, let

d=floor(sqrt(N)/8), m=N−d.

The negative Fourier matrix has a representation over a splitting field of K=Q(q) by at most

2N−2 floor(sqrt(N)/8)+2

permitted banks, with orientation multiplicities (m,1,1,m), the same m distinct nonzero roots in both same-sign groups, cross-sign singleton nodes 1, and beta=1 everywhere. The defining polynomial can be chosen in K[t], and the splitting field degree is at most m!.

Thus this refined bound is 2N−(1/4)sqrt(N)+O(1). It remains a bank-count statement, with leading coefficient 2, and makes no K-only or scalar FFT runtime claim.

## 1. An exact three-block independence estimate

Use the three orthonormal bases in Section 3 of UNIFORM_SQRT_SAVING_ADDENDUM.md. Select a chirp-Fourier atoms, b ordinary Fourier atoms, and c coordinate atoms. Inside each group the Gram block is an identity matrix. Each cross-block entry has magnitude 1/sqrt(N), so its operator norm is at most its Frobenius norm: sqrt(ab/N), sqrt(ac/N), or sqrt(bc/N).

For coefficient vectors in the three groups with norms x,y,z≥0, the Gram quadratic form is bounded below by

x²+y²+z²−2sqrt(ab/N)xy−2sqrt(ac/N)xz−2sqrt(bc/N)yz.

If a≤7d, b≤d, c≤5d and N≥64d², this is bounded below, for the nonnegative triple (x,y,z), by the quadratic form of I−Q/8, where

Q = ((0,sqrt(7),sqrt(35)),
     (sqrt(7),0,sqrt(5)),
     (sqrt(35),sqrt(5),0)).

The real symmetric matrix 8I−Q is positive definite by its exact leading principal minors:

8, 64−7=57, 512−8(7+35+5)−2sqrt(7·35·5)=66.

Thus I−Q/8 is positive definite, and all selected atoms are linearly independent. This argument remains strict at N=64d². It does not replace same-basis zeros by the worst-case cross-basis bound, and it uses no numerical eigenvalue approximation.

## 2. Exact atom counts

In the derivative-functional argument of the constant-thirteen proof, the step-two operator has degree r=2(d−1). The exact conservative atom counts after applying it are

a=(E_max+1)+(O_max+1)+2r=7d−10,
b=d−1,
c=d+2r−1=5d−5.

These satisfy the sufficient bounds in Section 1. The two chirp frequency blocks remain disjoint modulo N: one ends at E_max+r≤(7d−11)/2, and the second starts at e=(N+1)/2 and ends before N because O_max+r≤(7d−12)/2. The inequality N≥7d is more than sufficient.

For the coordinate-functional argument, the counts are smaller: a=3d−6, b=d−1, c=d. They also obey a≤7d, b≤d, c≤5d. Thus the block estimate proves both exclusions used in the uniform proof.

## 3. All remaining numerical hypotheses

For odd N≥1025, d=floor(sqrt(N)/8)≥4 and N≥64d². In particular:

- N≥7d, so the chirp frequency blocks do not overlap or wrap;
- m=N−d≥4(d−1), so the derivative-annihilation interval is nonempty;
- m+1≥3(d−1), so the final ordinary constant-coefficient recurrence propagates its initial zero block;
- dim W≥N−5d+12≥(N+1)/2, so the prescribed-root incidence argument applies;
- m≥(N−1)/2, as required for the original positive-half row interpolation.

All inequalities follow directly from 64d² for d≥4. At the first admissible order N=1025,d=4, the shifted chirp ranges are 0,…,8 and 513,…,521. The three derivative groups have sizes 18,3,15, respectively, and the exact block estimate applies.

## 4. Completion of the theorem

Use the block estimate in place of scalar strict diagonal dominance in Sections 4 and 5 of UNIFORM_SQRT_SAVING_ADDENDUM.md. The arguments then exclude every coordinate functional and every derivative evaluation functional from the recurrence row space under the new N,d choice.

Sections 6–8 of that proof require only those exclusions and the numerical hypotheses checked above. They yield a monic degree-m polynomial in the K-affine kernel with nonzero constant, no repeated roots, and full axis rank. In particular the squarefree argument is not a parameter count, and the prescribed-root incidence argument simultaneously secures the axis guard.

The exact physical row assignments and original raw-weight/resolvent formulas in the companion rank-envelope note then give 2m+2 legal banks. The same finite grid construction with Nd+2m choices per affine free coordinate remains valid. This establishes the refined statement if the underlying uniform proof and this block estimate pass independent review.
