# Independent review: uniform square-root bank saving, constant 13

Review date: 10 October 2026. Verdict: PASS. This is a separate receipt from the finite-order lifts and rank envelope; it does not retroactively merge their claims.

## Accepted theorem

For every odd N≥1297, put d=floor((sqrt(N)+16)/13) and m=N−d. The Fourier matrix has a representation in the original signed-bank grammar by at most

2N−2floor((sqrt(N)+16)/13)+2

banks over a finite algebraic extension of K=Q(q), with degree at most m!. The orientations have counts (m,1,1,m); β=1 throughout; both cross-sign nodes are 1; and the same m distinct nonzero roots of a polynomial in K[t] serve both same-sign orientations.

This is a uniform 2N−(2/13)sqrt(N)+O(1) upper bound. Its leading coefficient is still 2. It is not a K-only count, an approximately 8N/5 theorem, an unrestricted minimum, an efficient coefficient-construction result, or an FFT-complexity bound. Historical novelty is not cleared by this review.

## 1. Numerical range and envelope

The previously reviewed whole-left recurrence matrix has rank at most 4d−11. Its coefficient kernel W therefore has dimension w≥N−5d+12. The chosen integer d satisfies d≥4 and 13d−17<sqrt(N). Because d≥4 gives 13d−17>8d, these conditions imply N>64d² and, in particular, all of

N≥7d, m≥4(d−1), m+1≥3(d−1), w≥(N+1)/2.

No borderline odd order is omitted: at N=1297, d=4.

After multiplying column k by the nonzero D(q^k), every recurrence row extends to an N-periodic sequence

B(k)=C_kE(q^k)+C_kρ^kO(q^k)+R(q^k),
C_k=q^(hk²), ρ=q^e,

where h=4^−1 and e=2^−1 modulo N. The degree bounds are E_max=d−3+floor((d−1)/2), O_max=d−3+floor((d−2)/2), and deg R≤d−2. The uniform proof conservatively discards the divisibility restrictions from the sharper envelope. This only enlarges its allowed row space and is safe for the exclusions.

## 2. Coherence argument checked independently

The coordinate, normalized Fourier, and normalized chirp-Fourier systems are three orthonormal bases of C^N. Their cross-basis inner products all have modulus 1/sqrt(N), including for composite odd N. An elementary proof of the only nontrivial Gauss norm squares the sum and substitutes u=r−s: the inner sum over s vanishes unless 2hu=0 modulo N. Because 2h is a unit and N is odd, only u=0 remains, giving squared norm N.

For any s selected distinct atoms, the Gram diagonal is 1 and the absolute off-diagonal row sum is at most (s−1)/sqrt(N). Strict inequality below 1 proves positive definiteness and linear independence. No probabilistic incoherence, prime-order restriction, or generic-matrix claim is being used.

If a coordinate functional δ_j lay in the recurrence row space over C, its scaled envelope would have at most d coordinate-support positions in the full N-periodic extension. The envelope contains at most 4d−7 Fourier/chirp atoms, so it would yield a dependence on at most 5d−7 atoms, contrary to 5d−8<sqrt(N). This excludes every δ_j, in particular the leading and constant coefficient functionals and derivative evaluation at zero.

For nonzero x, assume derivative evaluation (k x^(k−1)) lies in that same complex row space. On k=0,…,m the envelope would equal k x^(k−1)D(q^k). The operator

L_x=∏_(j=0)^(d−2)(E_2−x²q^(2j))²

annihilates that exponential-polynomial sequence. Its degree in the step-two shift E_2 is r=2(d−1). Hence L_xB vanishes for 0≤k≤m−2r; these shifts never leave the originally matched range.

The identities for one shift are

E(z)↦qzE(q²z)−λE(z),
O(z)↦q²zO(q²z)−λO(z),
R(z)↦R(q²z)−λR(z).

They follow directly from C_(k+2)=q^(k+1)C_k and ρ²=q. The first two degrees increase by one at every step for a nonzero polynomial, because the new leading term cannot cancel with the lower-degree second summand. The ordinary degree does not increase.

After r steps the chirp frequencies occupy 0,…,E_max+r and e,…,e+O_max+r. They are disjoint and do not wrap modulo N: E_max+r≤(7d−11)/2<e, and O_max+r≤(7d−12)/2<N−e, under N≥7d. Thus coefficients from the two chirp pieces cannot cancel by modular aliasing.

There are at most 7d−10 chirp atoms, d−1 Fourier atoms, and d+2r−1=5d−5 coordinate atoms. Their sum is 13d−16. The condition 13d−17<sqrt(N) forces every coefficient in this purported dependence to vanish. In particular both transformed chirp polynomials are zero, and the leading-term observation forces the original E=O=0.

What remains is R(q^k)=k x^(k−1)D(q^k) on m+1 consecutive values. Their difference has a monic forward recurrence of order at most 3(d−1): the Fourier roots q^j have multiplicity one and the xq^j roots multiplicity two. Coinciding roots only decrease the order. The initial zero block is long enough to propagate to all k≥0. Comparing k=0 and k=N then gives

0=R(1)=N x^(N−1)D(1),

which is impossible. Therefore no derivative evaluation functional at any finite complex point lies in the recurrence row space.

## 3. Squarefree polynomials: the pencil step has no hidden one-dimensional case

Let H be the common divisor of W after extension to C. A repeated root of H would make derivative evaluation vanish on W, contrary to the preceding exclusion. The constant-coefficient exclusion gives H(0)≠0. The leading-coefficient exclusion ensures W contains a degree-m member.

Dividing W by H preserves its dimension, which is at least (N+1)/2≥649. Thus the residual polynomial space cannot be one-dimensional. Choose a degree-m member and a second quotient avoiding all roots of its quotient, possible because the residual space has no common root and C is infinite. The two quotients are coprime and have a nonconstant rational ratio. Only finitely many pencil parameters give multiple roots, meet the finitely many roots of H, or annihilate the leading/constant coefficient. Hence W has a nonempty projective open subset of degree-m squarefree polynomials with nonzero constant.

This is a characteristic-zero finite-exception argument, not an unsupported genericity assertion.

## 4. Simultaneous axis guard: incidence argument checked adversarially

Put r_0=(N−1)/2. Since w−1≥r_0, let U be the open set of ordered, distinct, nonzero r_0-tuples Y for which evaluations on W are independent. The incidence variety over U, with projective fibers of polynomials in W vanishing on Y, is a projective bundle of fiber dimension w−r_0−1≥0. U is a nonempty open subset of an irreducible tuple space, so the incidence variety is irreducible.

Nonemptiness is not merely inferred from dimension. Start with one squarefree degree-m g∈W with nonzero constant. Evaluating W at all m roots of g has kernel precisely the span of g: any degree-at-most-m polynomial vanishing at all those distinct roots is a scalar multiple. Therefore the rank is w−1 and r_0 roots can be selected with independent evaluations. This constructs a point of the incidence variety at which the good-polynomial condition holds.

The N-column root-axis determinant using these r_0 nodes in both orientations and the singleton is a nonzero polynomial in Y. At y_i=q^i it is exactly the full Fourier determinant with permuted columns, for every odd N. Although that specialization need not itself be in U, its nonzero locus intersects U because both are nonempty opens of the same irreducible tuple space. Pulling back gives a nonempty open subset of the incidence bundle.

The good-polynomial open set and the axis-open set therefore intersect in that irreducible bundle. This establishes simultaneous guards; no inference that arbitrary prescribed roots preserve squarefreeness is required.

To transfer this to the monic kernel over K, convert the full root-axis matrix to the polynomial moment-axis matrix by invertible block Vandermonde maps. Full rank implies at least one moment-axis minor, a polynomial in the monic coefficients over K, is nonzero at the obtained complex point. The constant/discriminant/minor product is therefore a nonzero polynomial on the monic affine kernel, which itself is a nonempty K-affine space. Because K is infinite, the good open locus has a K-valued point. Only the polynomial is descended; its roots may still require a splitting field.

## 5. Constructive grid and final bank realization

A coefficient of t^a modulo monic g has total degree at most a−m+1 when a≥m, proved by induction by multiplying once by t and reducing its top term. In the axis matrix a≤N−1, so every remainder coefficient has degree at most d. An N-minor has degree at most Nd.

The discriminant has total degree 2m−2 in the general coefficients, and specializing the leading coefficient to 1 cannot increase it. Thus the product of one nonzero axis minor, c_0, and the discriminant has degree at most Nd+2m−1. An affine parametrization of the monic kernel preserves that bound. A Cartesian grid with Nd+2m distinct rational integers per free coordinate must contain a nonzero evaluation. Testing the full axis rank avoids needing to identify the nonzero minor beforehand.

This is a finite, generally enormous recipe. The previously reviewed interpolation/reflection/raw-weight proof then realizes every physical row with 2m+2 legal banks over the splitting field. The coefficient construction is not claimed efficient, and its potentially large algebraic extension cannot be suppressed from the statement.

## 6. Independent controls and frozen binding

fresh_uniform_inequality_check.py independently verifies exact integer versions of all numerical inequalities, frequency-range separation, and atom counts for every odd N from 1297 through 100001 (49,353 orders). This is supporting boundary/control evidence; the general algebraic inequalities above prove the all-order range. At N=1297 the shifted chirp ranges are 0,…,8 and 649,…,657; the group counts are 18,3,15, totaling 36, and 35²<1297.

The verdict applies to the complete frozen UNIFORM_SQRT_SAVING_ADDENDUM.md with SHA-256 9404352b64e3569f5cde5ae83e665b16bc03c2a9d0caa977f0c42d1ccbcd9ebb. Its source snapshot and this review are bound by UNIFORM_SQRT_REVIEW_RECEIPT.json. Any later coherence-constant refinement is a separate theorem and separate receipt.
