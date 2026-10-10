# Characteristic-two chirp guard: exact contraction and stopping boundary

## Result

This investigation does **not** prove or refute the sufficient uniform assertion

    Φ_N(q) ∤ Disc_z H_((N−1)/2)(z;q) in F₂[q]

for every composite N ≡ 1 (mod 4). The accepted characteristic-zero classification and its finite range through 1001 remain unchanged.

There are two proved uniform algebraic reductions and two useful obstruction examples:

1. An exact characteristic-two reciprocal contraction cuts the polynomial degree from (N−1)/2 to (N−1)/4. It factors the ordinary discriminant into an explicitly nonzero product and the fourth power of a smaller resultant.
2. At primitive odd order N, an exact Frobenius identity describes the squares of every half-degree Gaussian coefficient. The forced diagonal also reduces to the monomial q^(16^−1 mod N).
3. Even degree and an odd root order larger than twice that degree do not guarantee squarefreeness: H₆ fails at an explicitly specified primitive root of order 31.
4. Even the congruence and compositeness of the root order are insufficient without the special degree: H₅₂ fails at one prime above 2 of order 85, while the other seven primes give squarefree reductions. This is not the target H₄₂.

The first two are identities with proofs, not extrapolations from finite tests. The remaining nonvanishing problem is stated explicitly below. No literature-priority claim is made.

## 1. Definitions

Work first over F₂[q]. Let

    H_n(z;q) = Σ_(k=0)^n [n choose k]_q z^k.

The q-Pascal recurrence gives

    H₀=1,  H₁=z+1,
    H_n=(z+1)H_(n−1)+(1+q^(n−1))zH_(n−2).

All discriminants and derivatives in this report are ordinary ones. No q-difference discriminant is used.

Put a_j=1+q^j and introduce

    S₀=1,  S₁=x,
    S_n=xS_(n−1)+a_(n−1)S_(n−2).

In the Laurent extension z=t², direct substitution in the recurrences proves

    H_n(t²;q)=t^n S_n(t+t^−1;q).

S_(2r) has only even powers of x. Define P_r by S_(2r)(x;q)=P_r(x²;q).

## 2. Uniform reciprocal contraction lemma

For every r≥0, in F₂[q,z,z^−1],

    H_(2r)(z;q)=z^r P_r(z+z^−1;q),                         (1)

where

    P₀=1,
    P₁=y+1+q,
    P_r=(y+q^(2r−2)(1+q))P_(r−1)
        +(1+q^(2r−2))(1+q^(2r−3))P_(r−2),  r≥2.          (2)

Moreover,

    P_r(0;q)=∏_(j=1)^r (1+q^(2j−1)),                     (3)

and

    Disc_z H_(2r)=P_r(0;q)² (Disc_y P_r)².                (4)

### Proof of (1)–(3)

Eliminating the odd-indexed S polynomials gives

    S_(2r)=(x²+a_(2r−1)+a_(2r−2))S_(2r−2)
           +a_(2r−2)a_(2r−3)S_(2r−4).

Here a_(2r−1)+a_(2r−2)=q^(2r−2)(1+q), which gives (2). The Laurent substitution gives (1), since (t+t^−1)²=z+z^−1. Finally the original S recurrence at x=0 gives (3).

### Proof of the ordinary discriminant identity (4)

In a splitting algebra, write P_r(y)=∏_i(y+u_i). Then

    H_(2r)(z)=∏_i(z²+u_i z+1).

In characteristic 2, the discriminant of z²+u_i z+1 is u_i². For i≠j, subtracting the two monic quadratics gives (u_i+u_j)z, and therefore their resultant is (u_i+u_j)². The discriminant-of-a-product identity now yields

    Disc H_(2r)=∏_i u_i² ∏_(i<j)(u_i+u_j)^4
               =P_r(0)²(Disc P_r)².

This is a polynomial identity and remains valid when roots repeat. The proof does not assume the desired squarefreeness.

### A second Frobenius contraction

Write the even and odd parts of P_r as

    P_r(y;q)=A_r(y²;q)+y B_r(y²;q),
    R_r(q)=Res_t(A_r(t;q),B_r(t;q)).

The characteristic-two parity-resultant identity is

    Disc_y P_r=R_r(q)².

For example, when r=2s, A_r is monic of degree s and P_r'=B_r(y²). Pairing the two equal square-root factors above each root of B_r, or applying the product formula for resultants, gives Res(P_r,P_r')=Res(A_r,B_r)². When r is odd, B_r is monic and the same calculation applies. The degree-one case has R₁=1. These identities are valid over the coefficient polynomial ring, including specializations where the other parity part drops in degree.

Consequently the full exact factorization is

    Disc_z H_(2r)(z;q)
       = [∏_(j=1)^r(1+q^(2j−1))]² R_r(q)^4.             (5)

## 3. Exact remaining target

Now let N=4r+1 be odd, and let q have exact order N in characteristic 2. Every exponent 2j−1 in (3) is strictly between 0 and N, so P_r(0;q)≠0. Thus

    H_(2r) is squarefree ⇔ P_r is squarefree ⇔ R_r(q)≠0.  (6)

Because Φ_N is squarefree modulo 2 and is coprime to the product in (3), (5) also proves the polynomial-ring equivalence

    Φ_N ∤ Disc H_(2r) ⇔ Φ_N ∤ Disc P_r ⇔ Φ_N ∤ R_r.       (7)

In particular, the requested sufficient route is **exactly** the following smaller resultant problem:

    For every composite N=4r+1, show Φ_(4r+1) ∤ R_r
    in F₂[q], with P_r, A_r and B_r defined above.

One good irreducible factor remains sufficient. No argument here proves that this residual resultant is a unit, that every factor is good, or that a good factor always exists. The contraction removes the already-understood z=1 obstruction but does not remove the genuine ordinary-derivative obstruction.

For illustration, the recurrence gives the exact small residual factorization

    R₃(q)=(q+1)^6(q²+q+1)(q⁵+q⁴+q³+q+1).              (8)

The last factor is not supplied by the nonzero product in (3). Its root-of-unity specialization causes the first obstruction below.

## 4. Half-degree q-Pascal/Frobenius identities

Let N=2m+1 be any odd number, q have exact order N in a characteristic-two field, and define

    F_k=∏_(j=1)^k(1+q^j),  F₀=1,
    c_k=[m choose k]_q.

Every F_k used below is nonzero. For 0≤k≤m one has

    c_k² = q^(−k²) F_(2k) / F_k^4.                      (9)

### Proof

Square the Gaussian product formula and use 2m≡−1 (mod N):

    c_k²
     = ∏_(j=0)^(k−1) (1+q^(2m−2j))
       / ∏_(j=1)^k(1+q^(2j))
     = q^(−k²) ∏_(j=0)^(k−1)(1+q^(2j+1))
       / ∏_(j=1)^k(1+q^(2j)).

The last ratio equals F_(2k)/F_k^4, since the even-indexed product is F_k². This proves (9).

There is also a closed Frobenius reduction of the forced diagonal. Put M=m(m+1)/2 and h=(N+1)/2. Since

    ∏_(j=1)^(N−1)(1+q^j)=1

and pairing j with N−j gives q^(−M)F_m²=1, injectivity of Frobenius gives

    F_m=q^(hM).

The characteristic-two reduction of the accepted diagonal is therefore

    δ=q^(−M)F_m,
    δ²=q^(−M),
    δ^16=q,
    δ=q^(16^−1 mod N).                                 (10)

For the middle equality, 8M=4m(m+1)=N²−1≡−1 (mod N); the last equality follows because δ is already a power of q and 16 is invertible modulo N.

Identities (9) and (10) are uniform at every primitive odd order. They simplify coefficients and the diagonal, but no valid implication from either identity to R_r(q)≠0 was obtained. In particular, squaring a Gaussian coefficient is not an ordinary derivative identity.

## 5. Exact obstructions to stronger shortcuts

### 5.1 A root order much larger than the degree is insufficient

Let

    K=F₂[q]/(q⁵+q⁴+q³+q+1).

The modulus is irreducible; q has order 31. The freshly computed polynomial is

    H₆(z;q)=1+q²z+(q²+q)z²+(q⁴+q³+q²)z³
             +(q²+q)z⁴+q²z⁵+z⁶.

Set

    G(z)=z⁴+(q²+q+1)z²+1.

Then exact field arithmetic gives

    H₆(z;q)=G(z)(z²+q²z+1),
    gcd(H₆,H₆')=G.

Indeed G=(z²+(q⁴+q³+q+1)z+1)². This refutes a purported theorem that even H_n must be squarefree merely because q has odd order greater than n, or even greater than 2n+1. All the factors 1+q^j with 1≤j≤6 are nonzero here.

It does not contradict the target: the target half-degree for order 31 is 15, and 31 is not 1 modulo 4.

### 5.2 Composite order 1 modulo 4 is also insufficient at unrestricted degree

Let

    K=F₂[q]/(q⁸+q⁶+q⁵+q⁴+q²+q+1).

The modulus is irreducible and q has exact order 85. Here

    gcd(H₅₂(z;q),H₅₂'(z;q))=z⁴+(q³+q)z²+1.              (11)

The full H₅₂ coefficient list is stored in CONTROL_RESULTS.json. There are eight irreducible degree-eight factors of Φ₈₅ over F₂. The controls verify that their product is Φ₈₅, verify irreducibility and exact root order for each, and compute the H₅₂ derivative gcds. Exactly the factor displayed above is bad; the other seven gcds have degree zero.

Thus the characteristic-two behavior can depend on the prime above 2, even with composite N≡1 (mod 4). This concretely distinguishes “one good factor” from “all factors good.” It is **not** a failure of the requested sufficient condition: the target at N=85 is H₄₂, not H₅₂, and H₅₂ itself still has seven good factors.

A smaller additional control records H₁₀ at primitive order 15, with modulus q⁴+q³+1 and gcd z⁴+(q²+q+1)z²+1. It serves only as another exact non-target obstruction.

## 6. Honest representation and algorithm costs

The identities above are not a claim that a primitive root in a field is supplied for free.

For an odd N, every irreducible factor of Φ_N over F₂ has degree

    d=ord_N(2),

because the Frobenius orbit of a primitive root has that size. Given one such factor f, represent the field F₂[q]/(f) using d bits per element. Classical multiplication and polynomial extended-Euclid inversion cost O(d²) bit operations; addition costs O(d). The order d can be as large as φ(N), so treating extension operations as unit-cost prime-field operations would be incorrect.

With q and f supplied:

- Precompute the powers of q and construct P_r by (2): O(r²) field operations.
- Compute gcd(P_r,P_r'): O(r²) field operations with classical polynomial arithmetic.
- Thus one candidate-factor test costs O(N²) extension-field operations, or the conservative O(N²d²) classical bit bound, with O(Nd) bits of polynomial storage. These are sufficient bounds, not optimal ones.
- An irreducibility check for f can use successive Frobenius squaring and gcd tests, with a conservative O(d³) bit bound under the same arithmetic conventions. Exact order N is checked using q^N=1 and q^(N/p)≠1 for every prime p|N. The prime factorization of N must be supplied or computed and its cost charged.

Finding f is an additional task. Factoring Φ_N, constructing the field and finding a primitive Nth root are not included in the candidate-test cost. A completely explicit, inefficient alternative is to enumerate the 2^d monic degree-d binary polynomials, test irreducibility, and test whether the residue of q has exact order N. The resulting exponential search bound is real and is not hidden inside the O(N²) count. To establish existence for an arbitrary N by exhaustive candidate tests, all primitive factors may need inspection before concluding failure of this sufficient route.

There is also a factorization-free decision procedure for the statement in (7): construct Φ_N, compute the polynomial resultant R_r over F₂[q], and reduce it modulo Φ_N. This avoids pretending that division in the quotient F₂[q]/(Φ_N) is always legal; that quotient usually has zero divisors. A division-free determinant algorithm for the Sylvester matrix is an alternative over this quotient. These procedures decide a specified N. They do not prove nonvanishing uniformly and supply no uniform guarantee of finding a good factor.

The characteristic-zero implication remains one-way: one good reduction proves characteristic-zero squarefreeness. Failure at every characteristic-two factor would refute this sufficient route at that N, but would not itself be a characteristic-zero counterexample.

## 7. Controls, source preservation and scope

Only freshly authored code was executed. No supplied or predecessor constructor, verifier or audit implementation was executed or imported. The current package's exploratory programs may import its own newly authored arithmetic controls; these are not predecessor code.

independent_controls.py verifies:

- The indeterminate-q contraction and constant-product identities through H₂₀.
- The ordinary discriminant contraction through H₁₂.
- The explicit field counterexamples above, including modulus irreducibility and exact order.
- All eight order-85 factors for the non-target polynomial H₅₂.
- The half-degree coefficient-Frobenius and diagonal-monomial identities at N=9,21,85. These last controls deliberately perform no squarefreeness test.

Exploratory logs also record small fixed-degree symbolic discriminant factorizations and non-target degrees below several small orders. The half-degree targets were excluded from the non-target gcd explorations. There was no repeat of the accepted 250 finite certificates, no expanded target range claim, and no inference of a uniform theorem from these controls.

Both immediate input manifests were verified before research. Sixty-one distinct protected input/predecessor paths were hashed at the beginning and completion, including paths named by the input snapshots. PRESERVATION.json records their exact agreement. The new output manifest seals this report, fresh programs, results and provenance.

## Stopping boundary

The uniform work achieved here is the proved factorization (5), the exact equivalence (7), and the primitive-root Frobenius identities (9)–(10). The missing step is nondivisibility of the explicitly defined residual resultant R_r by Φ_(4r+1) for every composite 4r+1, or an exact target counterexample to that assertion. Neither has been established in this bounded research pass.
