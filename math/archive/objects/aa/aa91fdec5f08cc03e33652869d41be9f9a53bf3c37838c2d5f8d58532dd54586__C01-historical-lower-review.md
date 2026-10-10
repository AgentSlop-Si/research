# Independent audit: all-order N5 chirp-B exclusion

## Accepted result

Let zeta be any primitive complex fifth root, F5 the unnormalized positive-exponent Fourier matrix, A=diag(zeta^(3j²)), and B=(F5^{-1}+A)^{-1}. **B cannot be the sum of two weighted Hamiltonian-cycle Green resolvents with arbitrary diagonal endpoints on the fixed five coordinates.** All 24² ordered structural-cycle pairs are covered, including zero edges and singular endpoint masks, with each Green denominator invertible.

This is an exact computer-assisted finite-size representation exclusion. It strengthens the previously accepted one-order-pair N5 obstruction to every Hamiltonian order pair. It is not an asymptotic FFT lower bound, does not cover unmatched endpoint permutations, and does not address more summands or products. The separate N3 positive construction remains valid.

## Source and independent method

Constructor report: `N5_EXHAUSTIVE_DIAGONAL_ENDPOINT_EXCLUSION.md`, SHA-256 bd82b37ed61bbeaa992bf3665b0b18484dd1480b36506a2ec51348a707463271. The supplied manifest was checked by reading and hashing files; none of the constructor programs was imported or executed. Source report and certificate data are preserved inert under `source/`.

Our checker independently creates every Hamiltonian permutation from traversals beginning at zero, recomputes the target by direct finite-field inversion, derives every eligible row-pair equation, constructs its own projective forests and polynomial domains, enumerates all branches, derives all column directions, and generates its own nonzero maximal augmented minors. A second own script compares every supplied branch and every supplied determinant against fresh exact arithmetic. This does not rely on reported summary counts as evidence.

## 1. Target and arithmetic guards

For N5, G=1+2(zeta²+zeta³), c=5G. Integer polynomial reduction modulo 1+zeta+zeta²+zeta³+zeta⁴ independently gives G²=5 and c²=125. Consequently 1+c is nonzero in characteristic zero. The target entry formula

B_ij = [zeta^(ij) − G zeta^(−3(i+j)²) + c zeta^(−3i²) delta_ij]/(1+c)

has good reduction at p=241,zeta=91: exact order five, G=103,c=33,denominator34. Our direct inverse and this formula agree in all 25 entries with the stated target matrix. The scalar 5 is also a unit at this prime.

The extension E=F241(theta), theta²=7, is a field because 7^120=−1. Every polynomial of degree at most two over F241 splits there. Our root routine handles a base-field square discriminant, a nonsquare as a square times 7, repeated roots, linear polynomials, constant polynomials and the separate projective point at infinity. No rejection is based merely on absence of F241-rational roots.

## 2. Complete projective row enumeration

For a fixed pair pi,tau, write row direction u_i=(a_i,b_i) at columns i,pi(i), and column direction v_j=(c_j,d_j) at rows j,tau^{-1}(j). Outside j∈{i,pi(i),tau(i)}, the necessary equation is

u_i^T [[B_i,j, B_i,tau^{-1}(j)], [B_pi(i),j, B_pi(i),tau^{-1}(j)]] v_j = 0.

Eliminating a shared nonzero v_j from rows i,k gives a bilinear form u_i^T C u_k=0. Our independently derived coefficient convention satisfies det C=det M_i,j * det M_k,j. Across all 576 pairs, all 4,320 eligible transition forms are nonsingular. Thus every such equation is a genuine invertible projective transition, with no discarded singular strata.

A spanning forest transports each row direction from a component root. Every remaining internal equation becomes a homogeneous binary quadratic in that root. Our exact affine polynomial gcd plus separate infinity check yields:

- 384 order pairs with an empty projective row domain over the algebraic closure;
- 72 surviving pairs with one component and two directions;
- 120 surviving pairs with two components, each having two directions.

No unrestricted component occurs. All surviving finite roots are simple. Therefore the complete branch count is 72*2+120*4=624. Each empty component has an independently rebuilt certificate of at most three homogeneous quadratics: 382 pairs use two and two pairs use three. To see completeness of such a witness, start with one nonzero quadratic, enumerate its at most two projective roots, and add an equation that rejects each root. The saved witness data verify every case.

These finite quadratic domains include infinity and zero base coordinates. All branch tuples are computed afresh, and their normalized sets match the supplied certificate sets exactly.

## 3. Columns and closed scale minors

For each row branch, the joint off-support constraints on each column are a matrix with two columns. Every one of the 3,120 such matrices has rank exactly one, so its projective nullspace has exactly one point. There is no omitted rank-zero column continuum. Direct multiplication verifies the complete off-support system for the resulting U,V.

Let K=UBV. A genuine invertible-branch representation forces

K_ij=V_ij x_i + U_ij y_j.

The augmented matrix has 25 rows, ten coefficient columns and the final K column. All 624 branches have coefficient rank ten and augmented rank eleven. Our own elimination generates 624 independent 11-row nonzero-minor certificates. Every one of the constructor's separate 624 supplied determinants is also recomputed exactly and agrees, including the example 221+173theta.

There are 240 branches with a zero row base, 240 with a zero column base, and 144 with neither. **None was excluded by a base-coordinate, invertibility or cycle-denominator guard.** Every rejection is a nonzero closed polynomial minor. This distinction is indispensable for the complex lift.

## 4. Multihomogeneity and endpoint boundaries

For independent row and column projective rescalings lambda_i and mu_j,

U'=D_lambda U, V'=V D_mu, K'=D_lambda K D_mu.

Each equation row (i,j) of the augmented matrix gains lambda_i mu_j; its x_i coefficient column loses lambda_i and its y_j column loses mu_j. Hence an 11-column maximal minor using equation rows R transforms by

product_i lambda_i^(n_i−1) * product_j mu_j^(m_j−1).

If a selected row set misses an i or a j, the corresponding full coefficient column is zero and the minor is identically zero. Otherwise every exponent is nonnegative. A nonzero minor is therefore genuinely multihomogeneous, of total row-direction degree six and column-direction degree six. Our checker verifies the degrees and a nontrivial exact projective gauge identity for every independently generated minor; the supplied degrees agree too.

The joint off-support bilinears and all maximal augmented minors thus define a closed necessary set S_B in (P1)^10. The finite computation proves S_B has no point over the algebraic closure of F241. It is sufficient to evaluate one nonzero minor per enumerated point; this is not claiming that the selected finite list alone defines the complete universal necessary system.

If a forward representation had singular diagonal endpoints, replace each zero endpoint by epsilon and keep its legal Green denominators and weights unchanged. Both branches become invertible over C(epsilon). Their sum tends to B. Normalize each inverse row pair and each inverse column pair by its lowest epsilon valuation, so the limiting pairs remain projectively nonzero. The off-support equations and all homogeneous minors specialize to zero. Consequently the singular-endpoint representation would still give a point of S_B. Scale variables may have poles and base coordinates may vanish; neither is required to survive. Zero edges involve no division and are included. Only singular Green denominators remain outside the original grammar.

## 5. Proper specialization to characteristic zero

Let R be the localization of Z[zeta5] at (241,zeta5−91). The target denominator 1+c is a unit. The polynomial necessary equations define a closed subscheme of the projective R-scheme (P1_R)^10, hence a proper R-scheme. A complex point would make the generic fiber nonempty; finite type also permits passage to a finite algebraic coefficient extension if desired. The image of a proper morphism is closed. Containing the generic point of this integral local base would force it to contain the closed point, giving a geometric special-fiber point. That contradicts the exhaustive algebraic-closure enumeration.

This use of properness is legitimate: it is the emptiness of a **closed projective necessary system** that is lifted. No affine inconsistency after a potentially vanishing normalization, and no open Green guard, is promoted to characteristic zero. The argument is independent of the embedding of Q(zeta5), so all primitive complex fifth roots are covered.

The requisite facts were checked against the primary Stacks statements: [projective morphisms are proper, Tag 01WC](https://stacks.math.columbia.edu/tag/01WC), and [the valuative criterion, Tag 0BX5](https://stacks.math.columbia.edu/tag/0BX5). The concrete polynomial degrees and all finite emptiness claims were independently verified here.

## 6. Positive controls and replay

Twelve independently constructed N5 two-Green targets pass the same necessary equations. Eight have singular endpoint masks and all retain structural zero-edge cases. Their normalized limiting direction tuples give augmented rank at most ten. The actual N3 chirp-B construction is independently rebuilt at w=15,t=207,kappa=2 over F241; its augmented matrix has rank six, and all 36 maximal 7-by-7 minors vanish. These controls test necessity and boundary handling rather than asserting complexity improvements.

`independent_checks.py` is self-contained standard-library code. It writes its own complete 576-pair and 624-branch certificates. `compare_source_certificates.py` imports only this own module and reads source JSON as inert data. Isolated replay of the first program reproduces the exact complete results JSON. The comparison separately reproduces all supplied branch sets, 624 determinant values and multidegrees, 384 short row-rejection witnesses, and the exact cyclotomic guard. All passed.

## Final scope

Accepted: the specified forced chirp B at N5 is outside every sum of two Hamiltonian Green branches with arbitrary diagonal endpoint masks, legal denominators and zero edges, on the fixed coordinate set. This leaves unmatched endpoint permutations, other targets, larger sizes, more branches and product architectures open. Any proposed extension to infinitely many sizes needs a separate restriction and arithmetic argument.
