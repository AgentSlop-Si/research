# Independent audit of the characteristic-two reciprocal contraction

## Verdict

**Pass, with the stated stopping boundary preserved.** The reciprocal recurrence, ordinary-discriminant contraction, parity-resultant identity, cyclotomic nondivisibility equivalence, coefficient Frobenius identity, and diagonal monomial identity are correct under their stated characteristic-two and exact-order hypotheses. Fresh arithmetic reproduces both requested counterexamples exactly, including the one-bad/seven-good distinction at order 85. The report's candidate-field cost accounting is sound as a conservative bound and correctly excludes finding the field factor.

Nothing in this audit establishes the remaining assertion for every composite N congruent to 1 modulo 4. No target counterexample was found or sought by a new target-range census. The previously accepted characteristic-zero results and finite range are neither enlarged nor re-certified here. No novelty or literature-priority inference is made.

Audited input: `characteristic_two_chirp_guard_0320/RESEARCH_REPORT.md` and its sealed numeric evidence. The accepted classification was read only to check the exact diagonal product being reduced. No supplied or predecessor program was executed, imported, or compiled.

## 1. Reciprocal contraction: valid

All identities in this section take place over F₂[q]. Define a_j=1+q^j and S_n=xS_(n−1)+a_(n−1)S_(n−2). The Gaussian-binomial polynomial H_n satisfies the stated three-term recurrence: the minus sign in the characteristic-zero Rogers–Szegő recurrence becomes plus in characteristic two.

The substitution H_n(t²)=t^n S_n(t+t⁻¹) follows term by term: t(t+t⁻¹)=t²+1 and the second recurrence term contributes a_(n−1)t². The parity of the powers of x in S_n agrees with n, so S_(2r)=P_r(x²). Thus

H_(2r)(z)=z^r P_r(z+z⁻¹).

Eliminating S_(2r−3) explicitly gives

S_(2r)=(x²+a_(2r−1)+a_(2r−2))S_(2r−2)+a_(2r−2)a_(2r−3)S_(2r−4).

Indeed, substitute xS_(2r−3)=S_(2r−2)+a_(2r−3)S_(2r−4) in characteristic two. Since a_(2r−1)+a_(2r−2)=q^(2r−2)(1+q), this is exactly the report's recurrence, with P₀=1 and P₁=y+1+q. Evaluating the original S recurrence at x=0 gives P_r(0)=∏_(j=1)^r(1+q^(2j−1)). No specialization or squarefreeness assumption enters this derivation.

Fresh controls construct H independently by the two-term q-Pascal coefficient recursion, construct P by the proposed contracted recurrence, and compare the full Laurent inflation. All ten cases r=1,…,10 pass as polynomial identities over F₂[q], including their constant terms.

## 2. Ordinary discriminants and parity resultants: valid

This audit uses the ordinary formal derivative with respect to z or y throughout. No Jackson derivative, q-difference derivative, or q-discriminant is substituted.

For a monic P(y)=∏_(i=1)^r(y+u_i), the reciprocal inflation factors as ∏_i(z²+u_i z+1). In characteristic two:

- Disc(z²+u_i z+1)=u_i².
- Res(z²+u_i z+1,z²+u_j z+1)=(u_i+u_j)².

For the second statement, evaluation of the second quadratic at either root α of the first gives (u_i+u_j)α, and the two roots' product is 1. The discriminant-of-a-product formula therefore gives

Disc H_(2r)=P_r(0)²(Disc P_r)².

A proof via generic independent roots establishes a polynomial identity before specialization, so it remains valid for repeated roots and zero discriminants. There is no circular squarefreeness assumption.

Write P(y)=A(y²)+yB(y²). Its ordinary derivative is B(y²). If r=2s, A is monic of degree s and B has degree at most s−1. For nonzero B of degree b with leading coefficient β, evaluation at the roots of B gives

Res_y(B(y²),P(y))=β^(2s)∏_(B(t)=0) A(t)²=Res_t(B,A)².

Each root of B(y²) is counted twice in the algebraic closure. The signs disappear in characteristic two. If r=2s+1, B is monic of degree s and the same calculation applies, with A of degree at most s. Consequently

Disc P=Res(A,B)².

This argument also explains why drops in the nonmonic parity part cause no hidden leading-coefficient correction. If B=0 and deg P>0 is even, both the derivative resultant and the parity resultant vanish. The degree-one case gives 1. The relevant target has r≥2; statements at r=0 merely require the conventional discriminant/resultant values for constants and are not used in the reduction.

Combining the identities gives exactly

Disc H_(2r)=[∏_(j=1)^r(1+q^(2j−1))]² Res(A_r,B_r)^4.

Fresh controls evaluate Sylvester determinants by newly authored fraction-free elimination over F₂[q], not by applying the identity being checked. All six cases r=1,…,6 pass for both discriminant identities. Additional degenerate parity cases, including zero derivative and drops in A or B, pass. The exact factorization R₃=(q+1)^6(q²+q+1)(q⁵+q⁴+q³+q+1) is also reproduced.

## 3. Exact-order and cyclotomic implications: valid

For N=4r+1 and q of exact order N in a characteristic-two field, every exponent 2j−1 appearing in P_r(0) lies between 1 and 2r−1, hence strictly below N. Thus the product is nonzero. The discriminant identities then imply

H_(2r) squarefree ⇔ P_r squarefree ⇔ R_r(q)≠0.

This equivalence uses exact order, not merely q^N=1. It requires a field (or the appropriate passage to fields) for the usual discriminant criterion. Compositeness is unnecessary for the algebraic equivalence; it only specifies the unresolved family.

For odd N, x^N−1 has derivative x^(N−1), so is squarefree over F₂. The reduced cyclotomic factors appearing in its product decomposition are therefore squarefree and pairwise coprime. Every root of the reduction of Φ_N has exact order N: otherwise it would also be a root of x^d−1 for a proper divisor d and hence of a different cyclotomic factor. This proves both the squarefreeness of Φ_N modulo 2 and its coprimality with P_r(0).

Writing Φ_N as a product of distinct irreducibles now gives

Φ_N divides Disc H_(2r) ⇔ Φ_N divides Disc P_r ⇔ Φ_N divides R_r.

Taking negations produces exactly the report's stated nondivisibility equivalence. The reason powers may be removed here is the squarefreeness of Φ_N. This does not say gcd(Φ_N,R_r)=1. Nondivisibility by the whole Φ_N means that at least one irreducible factor is good; it does not mean every factor is good.

The unchanged residual problem is to prove Φ_(4r+1) does not divide R_r for every composite 4r+1, or to give an exact target counterexample. None of the identities forces that conclusion. In particular, computing in the full quotient by Φ_N does not permit arbitrary division, because this quotient can have zero divisors.

## 4. Frobenius coefficients and diagonal: valid

Take an odd N=2m+1≥3, exact-order q in a characteristic-two field, F_k=∏_(j=1)^k(1+q^j), and c_k=[m choose k]_q. All factors used have exponents below N and are nonzero. Squaring the Gaussian product and using 2m≡−1 modulo N produces the scalar q^(−Σ_(j=0)^(k−1)(2j+1))=q^(−k²). The remaining numerator is the odd-indexed product up to 2k−1, and the denominator is the even-indexed product. The latter is F_k², so

c_k²=q^(−k²)F_(2k)/F_k⁴.

The full product ∏_(j=1)^(N−1)(1+q^j)=1 follows by evaluating (X^N−1)/(X−1) at X=1 in characteristic two. Pairing j with N−j then gives F_m²=q^M, where M=m(m+1)/2. With h=(N+1)/2, the square of q^(hM) is q^M. Frobenius is injective in a field, hence F_m=q^(hM).

The accepted diagonal product reduces in characteristic two to δ=q^(−M)F_m. Therefore δ²=q^(−M) and, since 8M=N²−1, δ^16=q. Already δ=q^((h−1)M) is a power of q. Because gcd(16,N)=1, this proves δ=q^(16⁻¹ mod N).

The identity is an algebraic identity for this diagonal product. It does not assert that a legal minimal-node bank exists at every N, and it supplies no ordinary-derivative or squarefreeness conclusion. N≥3 is the nontrivial intended setting of the accepted chirp problem; the report's phrase “any odd number” should be read with this setting, rather than using an inverse modulo 1.

Fresh controls check every coefficient at N=9 and N=21, and separately at all eight primitive order-85 factors. The full-product, half-product, δ², δ^16, and modular-exponent formulas all pass. These controls deliberately perform no squarefreeness test of the half-degree targets.

## 5. Exact counterexamples independently reconstructed

Binary polynomial integers use bit j for q^j; outer polynomial lists are in ascending z-degree. The fresh code enumerates trial factors to establish each small modulus's irreducibility, then checks q^N=1 and q^(N/p)≠1 for each prime divisor p of N. Gaussian coefficients come from a newly authored q-Pascal recursion. Ordinary derivative gcds come from Euclid with independently verified Bézout identities; the full Bézout coefficients and divisibility quotients are saved in the results.

### H₆ at order 31

The modulus 0x3b is q⁵+q⁴+q³+q+1. The independently computed ascending coefficient list is

[1, q², q²+q, q⁴+q³+q², q²+q, q², 1].

The ordinary derivative is q²+(q⁴+q³+q²)z²+q²z⁴. Its monic gcd with H₆ is

G=z⁴+(q²+q+1)z²+1.

Both exact factorizations are verified:

H₆=G(z²+q²z+1),
G=(z²+(q⁴+q³+q+1)z+1)².

Thus exact odd order greater than 2n+1 does not guarantee ordinary squarefreeness, even when all 1+q^j for 1≤j≤n are nonzero. This is not the target at order 31: its half-degree would be 15, and 31 is not 1 modulo 4.

### H₅₂ at order 85

Independently enumerating every monic degree-eight binary polynomial, retaining irreducible moduli whose residue q has order 85, gives exactly

0x13f, 0x177, 0x17b, 0x18b, 0x1a3, 0x1bd, 0x1dd, 0x1f9.

Their product is independently compared with Φ₈₅ constructed by monic exact divisions from x^d+1, and matches. The ordinary derivative gcd degrees, in that order, are

0, 4, 0, 0, 0, 0, 0, 0.

At 0x177=q⁸+q⁶+q⁵+q⁴+q²+q+1, the exact monic gcd is z⁴+(q³+q)z²+1. Every one of the 53 H₅₂ coefficients, every derivative coefficient, and every gcd coefficient matches the sealed evidence. Hence the report's one-bad/seven-good claim is exact, not an artifact of unchecked modulus irreducibility or root order.

This is an unrestricted-degree obstruction, not a target obstruction. The half-degree target at order 85 is H₄₂. The additional H₁₀/order15 control also reproduces the reported gcd z⁴+(q²+q+1)z²+1, but has no bearing on the target family.

## 6. Cost and representation audit

For odd N, the Frobenius orbit of a primitive Nth root has length d=ord_N(2), so every irreducible factor of reduced Φ_N has degree d. This can be as large as φ(N). With a supplied irreducible modulus, d-bit polynomial-basis field elements support classical O(d²) multiplication and Euclidean inversion, and O(d) addition.

Constructing P_r by the scalar three-term recurrence requires O(r²) extension-field operations. A classical polynomial gcd of P_r and its ordinary derivative also costs O(r²) such operations. Therefore the stated O(N²d²) conservative bit bound and O(Nd) polynomial-storage bound for one supplied candidate factor are valid. They are not optimality claims, and they do not include obtaining that factor.

A conservative O(d³) bit irreducibility check is available by repeated Frobenius squaring and binary-polynomial gcds. Given the prime factorization of N, exact-order checks use O(ω(N) log N) field multiplications, hence an additional O(ω(N)d² log N) classical bit bound. Obtaining or certifying the prime factorization must be charged separately. Our very small-field control program instead uses exhaustive trial factors and exponentiation-based inversion for simplicity; it is a correctness control, not the implementation establishing the report's asymptotic bounds.

Factoring Φ_N, constructing a suitable field, or searching for a primitive root is additional work. The report correctly discloses this. Enumerating all 2^d monic degree-d binary polynomials is a legitimate exponential fallback, with its testing costs added; it is not a polynomial-time root-construction theorem. In a worst case, all primitive factors may have to be tested to show that this characteristic-two sufficient route fails at a specified N.

The factorization-free resultant route is also valid if the resultant is computed over F₂[q] before reduction, or by a division-free determinant method in the quotient. The report does not give an uncharged unit-cost algorithm over a quotient with zero divisors. A specified-N decision procedure is not a uniform nonvanishing proof.

## 7. Reproduction and preservation

Run only the fresh audit code:

    python fresh_controls.py

This uses Python's standard library only and writes FRESH_CONTROL_RESULTS.json beside the script. Its supplied CONTROL_RESULTS.json input is data used for final comparison; no supplied code is loaded. FRESH_CONTROL_RUN.log records the successful execution. The independently authored preservation helper may be run with `before` and `after` arguments, although the included original before snapshot should be retained as the audit record.

At the start of this audit, all 16 entries of the current package's manifest and all five predecessor manifests verified. All 61 inherited protected hashes matched their present files. The audit's before/after set covers 79 files, including all current-package files and the inherited inputs. INPUT_HASHES_BEFORE.json, INPUT_HASHES_AFTER.json, INPUT_SEAL_VERIFICATION.json, and PRESERVATION.json provide the exact records. Hashing a supplied program or a pre-existing compiled artifact as uninterpreted bytes does not execute it.

No accepted input was edited. The final audit seal covers this report, fresh code, controls, and preservation evidence.
