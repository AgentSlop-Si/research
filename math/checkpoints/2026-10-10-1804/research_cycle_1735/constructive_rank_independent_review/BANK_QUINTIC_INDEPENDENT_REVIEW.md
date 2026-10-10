# Independent review: order-eleven fixed-singleton bank obstruction

Review date: 10 October 2026. Verdict: PASS for the restricted common-annihilator obstruction below. This is separate from the accepted all-odd-order base-field upper bound 2N−4. It neither improves that upper bound nor proves an unrestricted bank-rank lower bound.

## Statement and necessary architecture

Use the accepted four signed bank orientations, and the normalized Fourier Weyl coefficient f(a,b)=q^(h(a+b)²), where N=11, q is primitive of order 11 and h=4^−1 modulo 11=3. Assume exactly one −+ bank and one +− bank, each with α=1. Their sector amplitudes may be arbitrary. The ++ and −− groups may have arbitrary legal nodes, weights, and characteristic-zero coefficient-field extensions.

Then at least six ++ banks and at least six −− banks are necessary. Thus this fixed-singleton architecture requires at least fourteen banks in total. If the previously accepted fourteen-bank splitting-field witness belongs to this same architecture, it attains this restricted lower bound. This review does not claim that fourteen is necessary when cross-sign counts or nodes change. It does not settle fourteen-bank attainment over K=Q(q).

## Forced central moments

For orientation (ε,δ), let r=[εa]_N, ℓ=[δb]_N, and let G_(ε,δ)(a,b) be the Gaussian binomial [r+ℓ choose ℓ]_(q^(εδ)) when r+ℓ≤N−1, and zero otherwise.

For b=1,2, the coordinate a=N−b is supported exclusively by −+. Its α=1 forces normalized sector amplitude

T_b=1/G_-+(N−b,b).

For b≤a≤N−b−1, neither +− nor −− contributes. Hence the ++ nodes x_i must represent the common-node moment sequences

v_b(a)=[f(a,b)−T_b G_-+(a,b)]/G_++(a,b)
      =Σ_i A_(b,i) x_i^a.

All displayed Gaussian denominators are nonzero at a primitive eleventh root. The coefficients A_(b,i) can vary with b, but the nodes cannot. Any ≤5-node representation therefore has a nonzero common annihilator g of degree at most five. Padding its coefficient vector to length six if necessary, each six-term Hankel window of v_b annihilates that same vector.

There are four such windows from the nine terms of v_1 and two from the seven terms of v_2. The resulting 6×6 coefficient matrix must be singular if such a representation exists. Repeated or zero nodes do not avoid this necessary condition; their root product is still an annihilator of degree at most the bank count. Arbitrary β parameters are absorbed into sector amplitudes where they contribute and do not change this central-node condition.

## Independent good-reduction certificate

Work modulo 23 and specialize q↦2. This is a valid primitive eleventh root because 2^11=1 modulo 23 and 2≠1. The integer cyclotomic ring therefore maps to F_23. Every denominator used below reduces to a nonzero element, so the moment matrix has good reduction.

A fresh Pascal-recurrence implementation of the Gaussian binomials gives

v_1(1),…,v_1(9) = (16,19,9,0,11,15,12,22,17),
v_2(2),…,v_2(8) = (9,11,11,20,12,15,19)

in F_23. The six Hankel rows are

(16,19,9,0,11,15),
(19,9,0,11,15,12),
(9,0,11,15,12,22),
(0,11,15,12,22,17),
(9,11,11,20,12,15),
(11,11,20,12,15,19).

Their determinant is 4 modulo 23. In particular it is nonzero. If the characteristic-zero determinant were zero, its good reduction would also be zero. Thus the determinant is nonzero in K and remains nonzero in every characteristic-zero extension of K. There is no nonzero common coefficient vector of length six, ruling out all degree-at-most-five common annihilators, not only monic or depressed quintics.

The same argument reflected by (a,b)↦(−a,−b), with ++ and −− exchanged, forces at least six −− banks when the +− singleton also has α=1. The ++ obstruction itself is independent of the number of −− banks because those banks vanish on the central coordinates used in the proof.

## Controls and limits

fresh_bank_quintic_check.py was written independently for this review. It imports only Python standard-library modules, constructs Gaussian binomials by Pascal recurrence, and computes the determinant with fresh modular Gaussian elimination. It imports or runs no author/predecessor program. FRESH_BANK_QUINTIC_RESULT.json records the matrix, moment sequences, all required denominator residues, and determinant.

This justified good-reduction certificate is a characteristic-zero nonexistence proof for the stated architecture. It is stronger than parameter counting and is not a numerical fit. It supplies no obstruction for changing cross-sign singleton nodes, adding cross-sign banks, or abandoning the common-node architecture. No growing-order rank law is accepted solely from the author's finite-field rank table. Any such law still requires a separate symbolic argument or explicitly delimited finite-order certificates.
