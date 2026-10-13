# Next bounded gate: ordinary residual squarefreeness at b=27

12 October 2026. This is a proposed next-cycle proof/counterexample check. Nothing in the new overlap certificate establishes this guard.

## Exact target

For every primitive odd-order root q with d>27 in characteristic zero, prove or find a genuine counterexample to

Disc_z U(z;q) !=0, where H_27(z;q)=(z+1)U(z;q).

Write U(z;q)=z^13 P_13(z+z^(-1);q). The exact monic recurrence is

P_0=1, P_1=t+q+q^2,
P_j=(t+q^(2j-1)+q^(2j))P_(j-1)-(1-q^(2j-1))(1-q^(2j-2))P_(j-2), j>=2.

The accepted identity is

Disc_z U=P_13(2)P_13(-2)(Disc_t P_13)^2.

The general derivative-nonzero theorem already gives P_13(-2)=(-1)^13 H'_27(-1;q)!=0. It is not the pending factor. The remaining guard is C_13(q)=P_13(2)Disc_t P_13 !=0 at primitive odd d>27.

## Why the large-order range is already closed

The accepted ordinary-squarefreeness theorem is general for every odd b>=3 and odd d>=4b^2. It compares the scaled Rogers–Szegő tridiagonal to the real probabilists' Hermite Jacobi matrix, uses a proved minimum Hermite zero gap, and tracks algebraic multiplicity by disjoint resolvent contours. Its explicit inequality is

b^4-(b-1)(b-2)^2(b+1/2)=(9b^3-11b^2+4)/2>0.

At b=27 the hypothesis is d>=2916; since d is odd, the first relevant order is2917. Thus only the 1,444 odd orders29,31,...,2915 remain for ordinary residual squarefreeness unless a finite polynomial certificate proves all odd d at once. The separate endpoint theorem d>6(b-1)=156 alone cannot close Disc P_13.

Source: math/reviewed_rounds/2026-10-12-reviewed-research/rs-ordinary-squarefree.md, sections1–4, at pinned commit95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d. This is an inherited general proof, not a finite large-d scan.

## First and preferred finite certificate

Work exactly over F_2[q], without computing the potentially expensive integer discriminant first.

1. Construct P_13 independently from the finite Euler product for H_27, removal of the q^(j(j-1)/2) shifts, division by z+1, and the reciprocal trace basis. Use the displayed recurrence as a second coefficientwise control.
2. Split P_13(t)=A(t^2)+tB(t^2). Here B is monic of degree6, and A has degree at most6. In characteristic2,
   Disc_t P_13=Res_y(A,B)^2.
   A division-free12x12 Sylvester determinant by subset recurrence has exactly4096 subset states. It is a finite bounded calculation, not an unbounded search.
3. Form F_13=P_13(0)Res_y(A,B)^2. Confirm F_13 is nonzero and construct F_13^* using its ACTUAL degree after reduction. Compute G_13=gcd(F_13,F_13^*) with exact bit-polynomial arithmetic. Record full coefficient bitmasks and Bezout identities.
4. Test the complete low-order-factor certificate. Let L(q)=product_(j odd,1<=j<=27)(q^j-1). Repeatedly divide the current G by gcd(G,L), until the gcd is1. If the final remainder is1, every root of G has odd order at most27, with all multiplicities accounted for. This bypasses full high-degree factorization and is sufficient.
5. The accepted reciprocal-cyclotomic criterion then excludes Phi_d|C_13 for every odd d>27. It completes the b27 ordinary residual guard, and only together with a separately reviewed b27 overlap result completes all b27 local-discriminant simplicity guards.

Why step4 proves the needed assertion: each polynomial q^j-1 is separable for odd j in characteristic2 and its roots have order dividing j<=27. Iterated gcd stripping removes exactly the factors with those orders, regardless of their multiplicities in G. If all factors are removed, no order>27 root remains. If not, that is merely failure of this sufficient certificate.

## Controlled fallback and counterexample discipline

If a nontrivial remainder survives, do not assume a characteristic-zero repeated root. The earlier m12 order17 factor already disproved the stronger order<=m heuristic while leaving b25 valid. For m13 a factor of order17,19,21,23,25 or27 would also be harmless; step4 removes it.

A bounded fallback is to test exact divisibility by Phi_d mod2 for the 1,444 remaining odd orders29..2915. A nonzero remainder excludes the characteristic-zero cyclotomic divisor at that d. If divisibility does occur, record the exact d and isolate it for characteristic-zero computation of gcd_t(P_13,P'_13) and P_13(2) in Q[q]/Phi_d. A modular vanishing alone is not a counterexample. Do not turn this into an unbounded factor-order scan.

## Stopping condition

The next cycle ends with exactly one of:

- A complete verified F13/G13 and low-order-divisibility certificate, independently reconstructed with negative controls, proving all odd d>27; or
- A completed bounded d29..2915 modular screen plus a precise finite list of unresolved exact cyclotomic cases, with at least one smallest survivor's characteristic-zero gcd/endpoint check; or
- A genuine characteristic-zero repeated-root/endpoint counterexample with exact arithmetic witness; or
- A concrete implementation/resource/provenance blocker, preserving the intermediate exact polynomials and identifying the next operation required.

Stop escalation if the fixed12x12 exact determinant or gcd cannot be completed in the agreed cycle resources. Do not keep enlarging the degree, prime list or order range. A failed sufficient test is not proof of nonsimplicity. No overlap result, finite numerical root plot, q-discriminant product, or conjectured general bound is allowed to retire this guard.
