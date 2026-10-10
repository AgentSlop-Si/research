# Independent review: projective Fourier gauge rigidity

## Verdict

Accept Theorems I–IV for fixed complex stages A,B (and N≥2 for the two-column statements), with the stated nonzero constraints and finite-field qualification. They provide a complete linear feasibility test and a useful synthesis objective. They do not construct Fourier factors, exclude all Green parameters, or give a general FFT lower bound.

The exact archive is FFT_PROJECTIVE_GAUGE_RIGIDITY_2026-10-10.zip, Library [private-id], SHA-256 5eac4f25f89289545280f3d6575a1096cf443a52e3237111f66cecc909c92e76. All 16 members were read completely, including all five Python programs as inert text. CRC and all 15 internal manifest entries pass. Source output logs are preserved, not treated as independently rerun experiments. The historical 21-archive catalogue was read but not recursively reindexed or proof-audited here; its coverage claims are not silently adopted.

## Independent mathematical audit

Let C_j=A diag(B e_j), z_i=omega^i, K_j=C_(j+1)-diag(z)C_j, and T stack all K_j. Then T d=0 says that every row of A diag(d)B is a scalar multiple of the corresponding Fourier row. The last cyclic constraint is consistent because omega^N=1. A valid factorization requires all d_i and (C_0 d)_i nonzero; setting L_ii=1/(C_0d)_i then gives equality. Each forbidden zero is a linear hyperplane in ker T. Over an infinite field these finitely many proper hyperplanes cannot cover ker T; a functional is nonzero on ker T exactly when appending it increases the row rank. This proves both necessity and sufficiency, including singular A,B without silently dividing by them. If the test passes, the resultant full Fourier factorization in turn forces A,B invertible.

Replacing T by K_0 proves precisely the first-two-column version. Later columns are independent obligations. For corank one, any nonzero adjugate column spans the kernel. For higher corank, the moment-curve vector sum t^(j-1)v_j in a kernel basis avoids all forbidden zeros for some choice among 2N(r−1)+1 distinct t-values. Over GF(q), q>2N suffices by the hyperplane union bound; a small field may fail despite every individual rank augmentation succeeding. This field-size qualification is essential.

The projective gap proof is correct. For u=C_0d, v=C_1d and s_i=|u_i|²+|v_i|²>0, minimizing over one complex row scale gives |v_i−z_i u_i|²/s_i. If s_i=0, the actual row error is 2, while that row contributes zero to the weaker numerator bound. Nonsingularity of K implies positivity of Q=C_0* C_0+C_1* C_1: a Q-null vector would annihilate both C_j and hence K. Since s_i≤d*Qd, the sum of row residuals is at least ||Kd||²/(d*Qd). Two-column Frobenius norm is at most sqrt(2) times full spectral norm, proving gamma/sqrt(2). Allowing zero output scales only weakens the minimization, so the inequality remains valid for invertible L. For the normalized target the factor is gamma/sqrt(2N).

The row minimizer and Wirtinger gradient are correct. An independent quotient-rule form is

G = K*(r/s) − C_0*(u |r|²/s²) − C_1*(v |r|²/s²),

where r=v−diag(z)u and operations inside parentheses are coordinatewise. This equals the source's envelope form. The derivative along h is 2 Re(G* h); omitting this factor two would be a convention error, but the source does not omit it. The objective is defined only where every s_i>0. When the optimal row scale is zero, it yields an infimum over invertible output scales, not a attained minimum in that domain. These distinctions are already present in the source.

## Fresh computational evidence

Only reviewer-authored check_projective_independent.py was executed.

- Exact rational arithmetic verifies the two nonzero-weight two-cycle inverses and (3/8)(G_++G_-)=I. Thus the four-branch A=B=I witness has gamma=1. The actual best diagonal spectral error is exactly 1: any diagonal approximation leaves an off-diagonal entry of magnitude one, and diag(1,−1) attains error one.
- The saved 8×8 reference pencil has determinant 55687 modulo 65537. Its Green parameters are not included in this archive, so this check verifies the matrix certificate only. Four-Green origin and the characteristic-zero lift remain inherited provenance, not a newly reconstructed claim.
- For each of the four N4/GF(17) corner cases, all 16^4 nonzero middle gauges were examined independently for both first-two and all-column feasibility. All eight rank-augmentation outcomes, forced-zero coordinates, forced-zero seed rows and saved ranks agree. The corrupted third-column example passes the two-column gate and fails full equality.
- One hundred independently generated dense complex controls at N3,5,8,16,32 agree between quotient and envelope gradients, pass central finite differences, obey scale invariance, and satisfy the projective spectral bound. These are numerical controls, not interval certificates for the source's decimal gamma values or a replay of its seeded four-Green samples.

Static program review found the forward cyclic recurrence and adjoint permutation/weight reversal consistent with the stated Green matrix. Each uses O(N) work per supplied branch. Two forward and two adjoint stage calls suffice for a loss/gradient evaluation once b0,b1, parameters and permutations are supplied. Parameter construction, root generation, conditioning and numerical convergence are separate obligations. The explicit all-column stack has N³ scalar entries; synthesis/elimination is not an O(N) application algorithm.

## Constructive consequences and novelty boundary

1. Eliminate the output diagonal analytically in candidate fitting. This removes N artificial optimization variables without pretending to solve the outer parameter search.
2. Reject a singular-pencil candidate if a middle coordinate or a seed row is forced zero. Determinant zero alone is an unsafe positive gate.
3. On a feasible corank-one branch, substitute one kernel/cofactor vector into every remaining K_j d=0. This reduces symbolic variables while retaining all exceptional higher-corank and denominator branches separately.
4. Use the full stack for exact certification of a discovered candidate; use the two-column objective only to search. A positive numerical fit must still survive every Fourier column, nonzero normalization and exact arithmetic.

The inherited determinant obstruction, Fourier covariance and cocycle methods are not new here. Rank-nullity, hyperplane avoidance, generalized singular values, least squares and adjugates are classical. The combination is useful within the inspected project; global novelty was not established, and no literature-priority claim is accepted.
