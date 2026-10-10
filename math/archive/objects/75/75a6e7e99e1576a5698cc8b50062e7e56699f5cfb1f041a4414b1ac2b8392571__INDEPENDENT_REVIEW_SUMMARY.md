# Independent review: augmented lower-content extension

Status: exact certificates and the stated arithmetic consequences accepted; universal unramified support remains open. Date: 10 October 2026 UTC.

## Accepted finite certificates

The reconstructed constants are

- c_3^+ = 1
- c_7^+ = 7^2
- c_11^+ = 11^5
- c_15^+ = 3^12 · 5^9 = 1,037,970,703,125
- c_19^+ = 19^11 = 116,490,258,898,219

Every supplied coefficient field U, g, v, delta, Disc(U), Res(z^s+1,U), Gamma, Gamma Gamma^iota, and their augmented product agrees with the independently reconstructed value. The auxiliary reciprocal polynomial P was verified separately by expansion and was not used to compute the primary determinants. The coefficient gcds have explicit integer Bezout witnesses in the independent JSON files.

The exact definitions are

U = H_((s-1)/2)/(z+1), g = U(-1),
v = (q^2;q^2)_((s-3)/4) (q;q^2)_((s-1)/2),
Gamma = Disc_z(U) Res_z(z^s+1,U), delta = 2g-v,
c_s^+ = gcd of the canonical coefficients of Gamma Gamma^iota delta modulo Phi_s.

In particular, the resultant is included, the ordinary z derivative is used, and the product is reduced before taking the coefficient gcd. No algebraic norm is substituted.

## Independent construction

The primary verifier uses only Python's standard library. It reconstructs the Gaussian binomial coefficient [b choose k]_q by enumerating k-subsets I of {0,...,b-1} with weight q^(sum(I)-k(k-1)/2). It computes cyclotomic polynomials by exact recursive division of q^s-1, divides H by z+1, and works in the integral power basis of Z[q]/Phi_s.

For a monic U, Res(U,a) is the determinant of multiplication by a on the free quotient module R[z]/U. Direct degree-(b-1) multiplication matrices give the derivative resultant and the z^s+1 resultant. Determinants are computed by Faddeev-LeVerrier with checked exact integer divisions and a Cayley-Hamilton zero remainder. No reciprocal degree reduction enters this calculation. Only after reconstruction does the verifier read certificate JSON for comparison. None of the author's programs, checkers, modules or code were executed, imported, compiled or parsed.

Independent symbolic discriminant/resultant computations over Z[q], followed by cyclotomic reduction, also agree at the s=7 and s=11 calibration bases. Those auxiliary controls use SymPy 1.14.0.

## Theorem consequences and hypotheses

Apply the already accepted augmented lower-content criterion to the two new exact constants:

1. For every prime p congruent to 1 modulo 4 with p != 5, H_((15p-1)/2)(z;zeta_(15p)) is squarefree in characteristic zero, at every primitive root.
2. For every prime p congruent to 1 modulo 4, H_((19p-1)/2)(z;zeta_(19p)) is squarefree in characteristic zero, at every primitive root.

The exclusion p=5 for s=15 is mandatory: p divides s, the lower algebra modulo p is ramified, and the criterion's squarefree q^s-1 and p-unit Q_s arguments fail. Indeed Phi_15 mod 5 = Phi_3^4, and the augmented residue is zero. The new certificates neither prove nor disprove the target d=75. For s=19, p=19 cannot occur in the requested p congruent to 1 modulo 4 regime.

The criterion needs one same residue component with the augmented product nonzero. Since p does not divide s, O_s/pO_s is a product of fields; coefficient content not divisible by p gives exactly this existential statement. The inverse-pair Hermite argument then chooses a good inverse root, and the accepted characteristic-zero local formula and exact cyclotomic division supply the target-order nonvanishing. No upper bound on the local vanishing order relative to p-1 is assumed.

The new orders d=15p and d=19p are congruent to 3 modulo 4. Their residual half-order squarefreeness removes the remaining guard in the inherited all-local-index overlap expansion, using the accepted uniform resonance and disk theorems. The root -1 is still present, simple, and forbidden for the scalar-bank application. The m+1 legal-bank minimum remains unchanged. This is not an all-composite theorem or an FFT speed result.

## Reciprocal-polynomial identities

For s=4r+3, write U(z)=z^r P(z+z^-1). If S_s(t) is determined by S_s(z+z^-1)=z^s+z^-s and C_s is the monic degree-(s-1)/2 polynomial with

z^s+1=(z+1)z^((s-1)/2) C_s(z+z^-1),

then

Disc(U)=P(2)P(-2) Disc(P)^2,
Res(z^s+1,U)=Res(P,S_s+2)=(-1)^r P(-2) Res(P,C_s)^2.

These identities are correct. Pair the roots of U via z^2-t_i z+1; its discriminant is t_i^2-4, and the resultant between two such quadratics is (t_i-t_j)^2. This gives the discriminant formula. Evaluating z^s+1 at each reciprocal pair gives S_s(t_i)+2. Finally S_s+2=(t+2)C_s^2 and Res(P,t+2)=(-1)^r P(-2), giving the resultant formula. The formulas remain polynomial identities under specialization. They are an exact computational reduction, not a proof of uniform content support.

## Adversarial controls

### Reduced coordinates cannot be omitted

Using the canonical input factors but taking content before the final cyclotomic reduction produces

- s=11: 11^4 before reduction, 11^5 after reduction
- s=15: 3^12 · 5^8 before reduction, 3^12 · 5^9 after reduction
- s=19: 19^10 before reduction, 19^11 after reduction

Thus a verifier taking ordinary polynomial-product content would return wrong constants.

### The exceptional parameter is real and must be excluded componentwise

At s=7, p=13, Phi_7 factors as

(q^2+3q+1)(q^2+5q+1)(q^2+6q+1).

Gamma Gamma^iota is coprime to Phi_7, whereas the delta gcd is q^2+6q+1. The latter component has tau=tau'=2, and J(y;2)=y^7+12y^5+9y^3 in F_13[y] has a root of multiplicity exactly three at zero. Its derivative gcd is y^2. Norm(delta)=1183 is divisible by 13, although c_7^+=49 is not; the other components suffice.

### A resonance obstruction to an all-component/norm-unit strategy

At s=63 and p=5, let

f=q^6+q^4+3q^3+q^2+1,
h=q^6+q^5+2q^4+2q^2+q+1.

Both are irreducible factors of Phi_63 modulo 5, and their roots have exact order 63. The independent controls explicitly check q^(5^6)=q and that the gcds with q^25-q and q^125-q have degree zero. They also check q^63=1, q^21 != 1, and q^9 != 1. These are the complete degree-six irreducibility and order-63 tests. An independent elementary-symmetric generating-product construction of H_31, followed by direct degree-30 U Euclidean gcds in F_(5^6), gives:

- At the f component, delta is nonzero and gcd(U,U') has degree zero, but gcd(U,z^63+1) has degree two. The same is true at the inverse root.
- At the h component, delta is nonzero and all four residual gcds, at the root and its inverse, have degree zero.

All supplied degree-30 U and inverse-U coefficient arrays, delta values, and monic resonance gcds for both components match the independent reconstruction. This proves an unramified bad resonance component exists. Therefore it is false that every unramified component must be good, and a norm-unit requirement would be unnecessarily strong. The good component also proves 5 does not divide c_63^+. This is not a counterexample to characteristic-zero half-order simplicity or to the existential augmented-content criterion.

## Boundary of acceptance

The review accepts the exact fixed constants, their two infinite-family consequences, the reciprocal identities, and the two-component s=63,p=5 obstruction control. It does not establish that all prime divisors of c_s^+ divide s for arbitrary s, repeated-prime target orders, worldwide priority, a universal all-composite result, or an FFT runtime improvement. Higher-base exact certificates are fixed constants entering an all-p theorem, not a target-order census.

The author also reports a 43-pair exploratory modular survey. That survey was not independently rerun, and is not a premise of any accepted theorem here. The review independently reconstructs the five exact fixed-base certificates and the decisive two s=63,p=5 components.
