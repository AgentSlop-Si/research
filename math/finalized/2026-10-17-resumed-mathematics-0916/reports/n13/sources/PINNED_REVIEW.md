# Independent review: exact pinned-cross N13 field criterion

Date: 14 October 2026 UTC. Verdict: **ACCEPT_SCOPE_LIMITED**.

## Accepted conclusion

Fix N=13, q=16, characteristic 53, the original negative unnormalized Fourier target, and the original signed-resolvent-bank grammar with exactly one effective alpha node in each cross orientation. Assume both cross nodes are pinned to y=z=1.

Any sixteen-physical-bank representation over a field K has same-sign annihilators H_plus and H_minus, and each is one of H_15 or H_37 below. This conclusion allows arbitrary legal beta parameters and arbitrary support nodes in K; **Frobenius stability is a conclusion, not an assumption**.

- H_15 has irreducible factor degrees 1,1,5, so its roots require a copy of F_(53^5) in K.
- H_37 has irreducible factor degrees 1,1,2,3, so its roots require a copy of F_(53^6) in K.

The sufficiency direction is also independently checked in Section 6. Therefore, writing B_1 for the pinned-cross minimum,

    B_1(K)=16 if and only if K contains F_(53^5) or F_(53^6).

In particular, B_1(F_(53^d))=16 if and only if 5 divides d or 6 divides d. No such sixteen-bank representation exists for d=1,2,3,4. The new degree-six attainment is an algebraic original-bank existence proof, not a new literal inverse-matrix certificate in an explicit degree-six coordinate encoding.

The conclusion does not exclude sixteen banks at d=2,3,4 when y or z is allowed to vary away from 1. It does not establish an exact seventeen/eighteen minimum there. With the already accepted eighteen-bank witness, the pinned subproblem has minimum between seventeen and eighteen for these three degrees. The unrestricted free-singleton problem also has exact minimum sixteen whenever K contains F_(53^5) or F_(53^6), since a pinned construction is permitted there and the inherited lower bound is universal. Necessity of this field condition in the unrestricted model remains unproved.

## 1. Dependence on the accepted universal lower bound

The accepted source `sources/PRIOR_LOWER_REVIEW.md` proves, for every characteristic-53 field and every legal beta, that each same-sign orientation requires at least seven distinct nonzero effective alpha nodes and each cross orientation requires a nonzero node. This review reads and binds that accepted theorem rather than claiming to reconstruct its large polynomial minors anew.

At a total of sixteen physical banks, all inequalities are equalities. There are exactly seven banks at distinct nonzero alpha values in (++), one nonzero-alpha bank in (-,+), one in (+,-), and seven at distinct nonzero alpha values in (--). No additional zero-alpha, repeated, ineffective, or cancellation-only physical bank is available. Thus each same-sign support has a monic degree-seven annihilator with distinct nonzero roots in K.

## 2. Arbitrary legal beta can be normalized without changing any bank

For one original bank let epsilon, delta be its signs, alpha its node, beta any legal parameter, and Delta=1-alpha^13-beta^13 nonzero. Write

    r=[epsilon*a]_13, ell=[delta*b]_13,
    gamma=(1/13) sum_t 16^(-t^2)=7,
    A_b=beta^ell/(13 Delta gamma) sum_j w_j 16^(epsilon*b*j).

Its normalized Weyl coefficient is alpha^r G_(epsilon,delta)(a,b) A_b. No division by beta occurs, so this includes beta=0 with the ordinary polynomial convention beta^0=1.

When alpha is nonzero, choose beta'=1 and Delta'=-alpha^13, which is nonzero. Set

    w'_j=Delta' gamma sum_(b=0)^12 A_b 16^(-epsilon*b*j).

Character orthogonality gives

    (1/(13 Delta' gamma)) sum_j w'_j 16^(epsilon*b*j)=A_b.

Every Weyl coefficient, hence the entire individual bank matrix, is unchanged. The orientation, alpha node, effective amplitude vector, and number of physical banks are unchanged. This normalization therefore applies to every bank of a putative sixteen-bank representation. It is not asserted for alpha=0, where beta'=1 would be singular; equality in the inherited lower bound has already excluded that case.

The obstruction below can also be derived directly with the original normalized amplitudes, so its validity does not depend on adopting beta'=1 in advance.

## 3. Independent reconstruction of the annihilator family

The new checker derives ordered Gaussian coefficients by the finite product

    G_(epsilon,delta)(a,b)
      = product_(i=1)^r (1-omega^(ell+i))/(1-omega^i),
    omega=16^(epsilon*delta),

when r+ell<13, and zero otherwise. All denominator factors are nonzero because 16 has exact order thirteen. This uses a different construction from the candidate's additive recurrence. Direct extraction independently verifies all 169 target Weyl coefficients gamma*16^(10(a+b)^2).

For b=1,...,6, the row a=13-b forces the (-,+) amplitude, since it is the sole supported orientation and y=1. The positive same-sign moments on a=b,...,12-b are

    M_b(a) = [16^(10(a+b)^2)
              - G_-+(a,b)/G_-+(13-b,b)] / G_++(a,b).

Their lengths are 11,9,7,5,3,1. A degree-seven support annihilator gives four recurrence equations from b=1 and two from b=2. The complete six-by-eight row matrix, in ascending annihilator-coefficient order, is

    29 46 40 18 29 26 34 29
    46 40 18 29 26 34 29 28
    40 18 29 26 34 29 28  8
    18 29 26 34 29 28  8 47
    36 50 17 47 18  9  7  7
    50 17 47 18  9  7  7  5

The determinant of the first six columns is 26 in F53, hence remains nonzero in every characteristic-53 extension. Fixing the coefficient of t^6 to lambda and the leading coefficient to one gives, over every such K, exactly

    H_lambda(t)=t^7+lambda t^6+(50+22lambda)t^5
      +(48+15lambda)t^4+(27+10lambda)t^3
      +(19+11lambda)t^2+(50+25lambda)t+(16+31lambda).

At this point lambda may be any element of K. Enumerating only the 53 prime-field values would not yet prove the desired obstruction.

## 4. Sector three forces descent by a formal identity

Let C be the normalized (+,-) cross-bank amplitude in sector b=3. At a=10, only (-,+) is supported, so its amplitude is 49=-4. For a=1,...,9 the (--) block vanishes. The original sector equations therefore give (++), unscaled power moments

    M_1=-2C-8,   M_2=9C-9,
    (M_3,...,M_9)=(-4,1,4,9,6,0,-6).

The checker independently reconstructs every G coefficient and target used in these nine equations. The (++ ) denominators for a=1,...,9 are, respectively, 23,16,44,37,36,52,9,45,4; all are nonzero constants. Thus no lambda-dependent division is hidden here.

Because H_lambda annihilates the seven actual support nodes, the two moment recurrences starting at a=1 and a=2 are

    (4lambda-6) C + 22lambda+15 = 0,
    (14lambda-15) C - 8lambda-21 = 0.

Let A1=4lambda-6, B1=22lambda+15, A2=14lambda-15, and B2=-8lambda-21. Multiply the first equation by A2 and the second by A1, then subtract. This gives the coefficientwise polynomial identity

    A2 B1 - A1 B2
      = 22lambda^2+22lambda+20
      = 22(lambda-15)(lambda-37).

This elimination involves no division by A1 or A2 and is valid at every lambda in every characteristic-53 field. Since K is a field and 22 is nonzero, lambda is 15 or 37. There are no lost exceptional cases. In addition, 14A1-4A2=29 is a nonzero constant, so these two C coefficients cannot vanish simultaneously. At lambda=15 they are 1 and 36; at lambda=37 they are 36 and 26.

Simultaneous reflection (a,b,epsilon,delta) to (-a,-b,-epsilon,-delta) preserves every G coefficient and the target and swaps the same-sign supports and cross nodes. All 676 G identities and all target reflection identities are checked independently. Because y=z=1, the same descent applies to the (--) support, using the reflected sector b=10.

The earlier finite full-sector census is not used to justify this universal descent. The formal quadratic identity is the step that removes the earlier Frobenius-stability restriction.

## 5. Exact factor profiles and finite-field exclusion

All fifty-three prime-field H_lambda polynomials were rebuilt and checked from scratch, then compared with the old JSON as inert data. Fifty-one pass nonzero-constant and squarefree guards: lambda=20 has constant term zero, and lambda=38 has derivative gcd t+44. For every guarded polynomial the checker iterates Frobenius modulo H and records gcd(H,t^(53^d)-t) for d=1,...,7. The degree of this gcd is the sum of degrees of the irreducible factors whose degrees divide d; recursive subtraction gives the exact count in each degree. All fifty-one full profiles match the source census.

Only two profiles matter after descent:

    H_15=(t-22)(t-36)
      (t^5+20t^4+6t^3+45t^2+49t+34).

The quintic factor is irreducible. Its exact factor degrees are 1,1,5.

    H_37=(t-17)(t-48)
      (t^2+38t+12)(t^3+11t^2+47t+41).

The displayed quadratic and cubic are irreducible. Its exact factor degrees are 1,1,2,3, not 1+6 or a single irreducible sextic.

Both factorizations are multiplied out exactly in the fresh checker, with their irreducible-degree claims certified by the Frobenius gcd profile. For an additional direct check, neither H_15 nor H_37 divides t^(53^d)-t for d=2,3,4; the modular remainders are independently evaluated and found unequal to t.

An irreducible degree-r polynomial over F53 splits in F_(53^d) exactly when r divides d. Thus H_15 splits exactly when 5 divides d; H_37 splits exactly when both 2 and 3 divide d, equivalently 6 divides d. A sixteen-bank support must contain every root of its monic degree-seven annihilator, so this proves the stated necessary field condition and the degree-2/3/4 exclusion.

## 6. Independent complete-sector sufficiency check

For each of the four ordered pairs (15,15), (15,37), (37,15), and (37,37), the fresh checker reconstructs all thirteen full 13-by-16 sector systems. It computes t^r modulo H by successive multiplication by t and reduction of its single degree-seven term, independently of the candidate's repeated monomial polynomial-division implementation. Gaussian elimination solves each system, then direct multiplication checks every row. All fifty-two systems pass, comprising 676 full row identities. Their ranks are 13,9,11,12,13,13,13,13,13,13,12,11,9 in sector order for each pair. Every actual coefficient vector is retained in `INDEPENDENT_ARITHMETIC.json`.

Here is the exact passage from these prime-field linear systems to legal original banks. If x_1,...,x_7 are the distinct roots of H in its splitting field, put V(k,i)=x_i^k. Evaluation gives

    [x_i^r]_(r,i) = R_H V,

where R_H(r,k) is the coefficient of t^k in t^r modulo H. The Vandermonde determinant is a product of nonzero root differences, so V is invertible. For each same-sign block and each sector, convert the solved quotient coefficient vector c into actual root amplitudes A=V^(-1)c. The two cross amplitudes are retained directly. Row multiplication by G commutes with this column change. Thus all thirteen sector identities hold at the actual support roots.

For every one of the sixteen banks choose beta=1 and the inverse-character raw weights from Section 2. All roots and both cross nodes are nonzero, so every Delta=-alpha^13 is nonzero. The inherited original-bank expansion, with the original factor 1/13, now identifies these amplitudes with exactly those legal physical-bank matrices. The 169 Weyl-coefficient identities imply the original negative unnormalized Fourier matrix identity because the S^a T^b form a basis when q has exact order thirteen and 13 is invertible.

Effectiveness requires a small grammar check before invoking the lower bound. The rebuilt solutions have (-,+) amplitude 49 in sector three and (+,-) amplitude 49 in sector ten, so both cross banks are effective. If a same-sign bank were ineffective, deleting it would leave a representation with at most fifteen physical banks and exactly one effective node in each cross orientation, contradicting the inherited lower bound. Hence all sixteen banks are effective and the allocation is exactly (7,1,1,7).

Taking the pair (15,15) proves existence over F_(53^5), and taking (37,37) proves existence over F_(53^6). Scalar extension preserves the full identities and nonzero denominators. Together with the necessity proof and the universal lower bound, this proves the stated iff over every characteristic-53 field. The mixed pairs require the degree-thirty compositum, as expected, but are not needed for the iff.

No trace-valued or quotient-algebra bank has been substituted into the grammar. Quotient matrices are only coordinate devices in the proof. This task did not construct an explicit degree-six modulus, list degree-six raw weights in coordinates, or record 208 degree-six branch inverses. Those additional artifacts are unnecessary for the exact algebraic existence proof and are not claimed as completed.

## 7. Fixed-support descent clarification

The candidate's separate fixed-support criterion is correct. Given a sixteen-bank representation over E and a subfield F of characteristic 53, retaining the identical raw certificate requires every alpha, beta, and raw weight to belong to F. If beta normalization and re-solving weights are allowed while retaining all orientation/alpha pairs, existence over F is equivalent to all those alpha nodes lying in F. In that case the complete sector matrices have F coefficients; consistency over E implies consistency over F by unchanged matrix and augmented ranks. Recover raw weights by Section 2. Isolated cross-sector rows force effective cross banks before the lower-bound argument forces all same-sign banks effective.

Having annihilator coefficients in F only asserts an invariant unordered support and does not place the individual alpha roots in F. The support polynomials must split in F. A total matrix in F, or a Frobenius-orbit sum in F, likewise does not make its individual extension-valued alpha nodes legal parameters over F. No orbit compression into a new trace primitive is allowed.

## 8. Reproducibility and boundary

Only the newly written `independent_check.py` was executed. No supplied or historical program was executed, imported, compiled, or evaluated. Supplied code was read as inert text; supplied JSON was parsed only as data. The checker independently reconstructs the arithmetic before comparison. No external write was made.

`INDEPENDENT_ARITHMETIC.json` contains the source hashes, complete forced-window matrix, affine annihilator coefficients, original sector-three rows, formal elimination coefficients, all fifty-three guard records, all fifty-one factor profiles with Frobenius gcd receipts, and all fifty-two complete sector solutions. `REPLAY.json` records an isolated cold replay using only the fresh checker and frozen inert inputs. The final candidate report, checker, result, and source-binding file are frozen and bound in `CANDIDATE_BINDING.json`; acceptance attaches to those exact bytes. This review establishes the pinned-cross iff and the accompanying fixed-support descent clarification. The previous quintic literal witness and its review remain separate attainment evidence; the new degree-six statement is proved by the algebraic construction above.
