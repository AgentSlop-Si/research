# Independent review: complementary RS endpoint certificate and exact-spectrum limit

13 October 2026 UTC.

## Verdict

**ACCEPT, at the stated restricted scope.** No mathematical correction is required to the candidate's all-parameter endpoint certificate, its balanced-order corollary, its complementary spectral-gcd constraint, or its synthetic nonimplication example.

The accepted claims are:

1. Over every characteristic-two field containing an element alpha of exact odd order d=2h+1>=3, and for every m,n>=0 with m+n=h-1, the explicitly displayed product-coefficient identity for E_m(alpha) and E_n*(alpha) holds and has a nonzero right side.
2. Consequently paired endpoint zeros are impossible for every m>=1 on the actual-family line ord(alpha)=4m+3.
3. The full length-h RS continuant has inverse-parameter reflection and the squarefree full d-th-root trace polynomial as its characteristic polynomial. The gcd of complementary prefix/suffix trace polynomials divides that polynomial.
4. The synthetic length-five chain has precisely the claimed full order-11 trace spectrum, nonzero edges and inverse-Frobenius reflection, while its complementary length-two blocks have distinct conjugate double roots. It disproves only the proposed implication from these structural premises to complementary-block squarefreeness.

**Not accepted as conclusions:** the general all-four-channel paired-support theorem, the general endpoint theorem off the balanced-order line, an actual RS paired counterexample, characteristic-zero transport, a new fixed-stage support census, a general FFT/runtime result, or historical novelty.

The original general paired-support gate remains OPEN at 58; the general endpoint gate remains OPEN at 53. The synthetic construction does not change either status.

The candidate's manifest SHA-256 is
4930b41793555c91bd9884a59f9c57a5c531bec9a9b1280f57ebd84448a523f0.
Its theorem file SHA-256 is
2c3fe11c5c1016924b89616940020b246b640d6c98b25da6648c4f70b071d93e.

## 1. Definitions and the endpoint recurrence

The normalization is the original Gaussian polynomial modulo two:
H_(2j+1)=(z+1)z^j P_j(z+z^-1), with P_0=1 and
P_1=X+q+q^2. The stated a_j=q^(2j-1)(1+q) and
c_j=(1+q^(2j-1))(1+q^(2j-2)) agree with the accepted three-term trace recurrence. Ordinary spectral derivatives, endpoint evaluation and parameter reversal remain distinct operations.

The endpoint recurrence can be re-established without assuming the new certificate. The Gaussian degree recurrence evaluated at z=1 gives
H_(2j)(1)=D_j=product_(r=1)^j(1+q^(2r-1)).
The odd value H_(2j-1)(1) is zero. Differentiating the same recurrence in z and evaluating at z=1 gives
E_j=D_j+(1+q^(2j))E_(j-1), E_0=1.
The equality E_j=H'_(2j+1)(1)=P_j(0) follows directly by differentiating the displayed factorization, since its only surviving derivative term at z=1 is the derivative of z+1.

This also proves the exact degree used for reversal. D_j has degree j^2, whereas the second summand has degree j(j+1), inductively, with leading coefficient one. Since j(j+1)>j^2 for j>=1, no leading cancellation occurs. Thus deg E_j=j(j+1), and E_j*=q^[j(j+1)]E_j(q^-1) is the actual-degree reversal. It is not permissible to reverse at the Gaussian degree or an inherited full-Q degree instead.

Unrolling the endpoint recurrence after division by C_j=product_(r=1)^j(1+q^(2r)) gives E_j=C_j S_j, where S_j=sum_(r=0)^j D_r/C_r. Every use of this quotient below is made only after verifying the denominators are units.

For the full unresolved problem, the candidate preserves Q_m=E_m R_m and reversal at N_m=m(m+1)(2m+1)/3. No endpoint-only result is substituted for this full obstruction. At m=1, R_1=1, E_1=q+q^2, E_1*=1+q and N_1=2, so the boundary is consistent with the original conventions.

## 2. All-parameter product certificate

Let alpha have exact order d=2h+1. The positive exponents in C_j and D_j for j<=h are strictly between 0 and d. Therefore every factor is nonzero, even when d is composite. This uses exact order, not merely alpha^d=1. The latter weaker condition would permit vanishing denominators.

The Gaussian product formula at degree d is legitimate term by term for interior coefficients: its denominator has exponents below d, and its numerator contains 1+alpha^d=0. Hence H_d=1+z^d. Its derivative at 1 is d=1 in characteristic two, so E_h=1 and S_h=1/C_h.

For each j between 0 and h, reversing the final j factors of s_h=D_h/C_h gives
s_(h-j)=s_h alpha^j s_j=s_h s_j(alpha^-1).
The exponent is +j. For one reversed factor the quotient is
(1+alpha^(1-2l))/(1+alpha^(-2l))
=alpha (1+alpha^(2l-1))/(1+alpha^(2l)).
The tail starts at m+1 and ends at h. Under k=h-j this becomes exactly j=0,...,h-m-1, so the complementary index is n=h-m-1, not h-m.

Consequently
S_h=S_m+s_h S_n(alpha^-1).
Furthermore C_n(alpha^-1)=alpha^[-n(n+1)]C_n(alpha), so
S_n(alpha^-1)=E_n*(alpha)/C_n(alpha).
Substitution and multiplication by C_h C_m C_n yield exactly
C_h C_n E_m(alpha)+D_h C_m E_n*(alpha)=C_m C_n.
Every factor cleared is already nonzero. The coefficients on the two endpoint terms, the reciprocal exponent, the tail index, and the right-side constant are all correct.

This is a proof for arbitrary indices and exact odd order, independent of finite controls. It is an explicit unit certificate, rather than a norm reformulation of an unknown gcd. Dividing by C_m C_n gives a conventional right-side-one certificate; the independent result file records these normalized coefficients in each control.

For h=2m+1, both endpoint indices are m and division by C_m gives
C_(2m+1) E_m+D_(2m+1) E_m*=C_m.
Thus paired endpoint vanishing is excluded at exact order 4m+3 for every m>=1. The equivalent congruence modulo Phi_(4m+3) reduced modulo two is valid: odd-order root polynomials are separable in characteristic two, and the reduced cyclotomic factors have precisely their exact-order roots. Composite d creates no exception.

At self-reciprocal Frobenius orbits, E_m's coefficients are in F2, so one endpoint zero would carry to its inverse and contradict the certificate. This one-sided conclusion is limited to those orbits. Off the balanced line, the certificate relates different endpoint degrees and supplies no induction to an arbitrary inverse pair of the same degree.

### Boundaries checked

- m=1, d=7: E_1=q+q^2 and E_1*=1+q have the asserted normalization and certificate.
- d=3, h=1, m=n=0: C_1+D_1=alpha^2+alpha=1, exactly the empty-prefix certificate.
- m=0 or n=0: the empty endpoint is 1; the formula still holds. The corresponding cut omits its absent edge term. It does not demand a defined c_1 or divide by it.

The computational boundary controls use only the already selected index family and its required empty-block cuts, not a new support census.

## 3. Full-chain reflection and spectral gcd

The diagonal reflection index is h+1-j. Substitution of d=2h+1 gives
alpha^[2(h+1-j)-1](1+alpha)
=alpha^(-2j)(1+alpha)=a_j(alpha^-1).
For edges the correct index is h+2-j; its exponents reduce to 2-2j and 3-2j, which agree with the two factors of c_j(alpha^-1), in the opposite order. Thus both displayed reflections are correct.

Reversal transposes the roles of the two off-diagonals. Characteristic polynomials depend on their products, so reversed trailing principal blocks have characteristic polynomial P_k(X;alpha^-1). A diagonal similarity can restore upper entries to 1 because every edge product is nonzero. This is not a diagonal-affine Hermitian gauge of the actual prefix matrix and does not contradict the earlier gauge obstruction.

The polynomial defined by
z^h CYC_d(z+z^-1)=(1+z^d)/(1+z)
is exactly P_h at alpha. It has constant coefficient 1. Its roots are alpha^j+alpha^-j for j=1,...,h. If u+u^-1=v+v^-1 then (u+v)(uv+1)=0; the chosen indices contain neither repetitions nor two representatives of an inverse pair. Consequently these h roots are distinct and nonzero. No positivity, analytic conjugation, or assumption on eigenvectors is needed.

Naming clarification: when d is composite, CYC_d includes the traces of all nontrivial d-th roots, including lower-order roots. It is the full d-th-root trace polynomial, not just the primitive cyclotomic trace factor. The candidate's explicit definition and calculations are correct; its use of the word "cyclotomic" must not be read as a primitive-only assertion.

Cutting at vertex m+1 gives the three matching possibilities: the vertex is unmatched, matched left, or matched right. They yield
CYC_d=(X+a_(m+1))P_m P_n^inv
       +c_(m+1)P_(m-1)P_n^inv
       +c_(m+2)P_m P_(n-1)^inv.
Here m+n=h-1, and absent boundary terms are omitted. Both edge indices and the inverse suffix normalization are correct.

Every term is divisible by gcd(P_m,P_n^inv), hence that gcd divides the squarefree CYC_d. This is a multiplicity statement about the gcd, not an assertion that either factor is squarefree. It excludes a common endpoint because CYC_d(0)=1, and excludes both polynomials having multiplicity at least two at the same spectral coordinate. Equivalently, gcd(P_m,P_m',P_n^inv,(P_n^inv)')=1.

It does not exclude a repeated root of one polynomial at x and of the other at a different y. In particular, Frobenius transporting a repeated root need not fix it. The candidate retains this distinction and makes the fixed-root corollary conditional on an appropriate field action and a fixed coordinate.

## 4. Independent synthetic-example reconstruction

Over F4 with w^2+w+1=0, the five-vertex matrix has diagonal
(0,0,1,0,0), upper edges (1,1,1,1), and lower edges
(w^2,w^2,w,w). Coefficientwise squaring reverses both diagonal and edge-product sequences. All edges are nonzero.

A separate dense symbolic characteristic-determinant calculation, reduced modulo two and w^2+w+1, gives
L=X^2+w^2=(X+w)^2,
R=X^2+w=(X+w^2)^2,
and full characteristic polynomial
X^5+X^4+X^2+X+1=CYC_11.
The repeated roots w and w^2 differ and are swapped by Frobenius. The two block polynomials are coprime and have nonzero endpoints. The full polynomial's derivative is X^4+1, whose only root in characteristic two is 1, while CYC_11(1)=1. Therefore the full polynomial is squarefree. Also CYC_11(w)=CYC_11(w^2)=1, emphasizing that the repeated block roots are not full-chain spectral roots.

The independent field construction certifies t^10+t^3+1 irreducible and verifies that t has exact order 1023. With the same binary polynomial-residue convention as the candidate,
alpha=t^93=0x2c9 has order 11,
omega=t^341=0xed has order 3,
and sigma(u)=u^32 sends alpha to alpha^-1 and omega to omega^2.
The five trace roots are
0x302, 0x356, 0x13b, 0x262, 0x30c.
They are distinct, fixed by sigma, and their monic product is exactly CYC_11. Thus the example genuinely fits the common field F1024 and its F32 trace subfield, not just an abstract F4 calculation.

This is not J_5(alpha) of the actual RS family: its first diagonal is 0, whereas a_1(alpha)=alpha(1+alpha) is nonzero at exact order 11. The correct rejected implication is solely that reflected nonzero-edge chains with this full spectrum must have a squarefree complementary block. No actual-family bad factor has been found.

## 5. Comparison with the inspected earlier results

- The earlier endpoint-fusion and endpoint-specific packets already establish the endpoint recurrence, actual reversal, q^2-shift identities and guarded Hankel/Hasse reductions. They leave the uniform endpoint certificate open and do not contain this high-order complementary prefix result.
- The b31 all-A overlap report, section 5, already uses complementary-prefix reflection and its characteristic-zero conjugate form. The mechanism is not new. The present packet supplies a direct characteristic-two derivation with every denominator checked and obtains the balanced exact-order line. It does not import that report's positivity, annulus estimate or characteristic-zero theorem.
- The uniform reciprocal-descent packet identifies an equivalent coefficient-pair obstruction for the entire Q_m, with exact multiplicities and ramified correction. The new identity is genuinely a restricted nonvanishing theorem, not another equivalent expression of the general unknown. It does not alter any full-Q multiplicity convention or remove any unresolved channel.
- The collision-kernel packet proves consecutive coprimality and an exact kernel identity, then exhibits an actual one-sided high-order collision. The present full-chain fusion supplies a different complementary-parameter restriction, but its synthetic example confirms that separate collisions remain possible under those structural conditions.
- The Frobenius/Hermitian packet already warns that collision roots can move under Frobenius, disallows the naive diagonal-affine Hermitian gauge, and gives a smaller nonsimple synthetic model. The present five-vertex example adds exact full trace spectrum and reversal premises to the nonimplication test. It neither rebrands those older facts as new nor refutes every possible Hermitian method.

The candidate is appropriately classified as a bounded packet-level interface plus a scoped obstruction. Historical priority has not been investigated. The classical recurrence attribution was cross-checked against Vinroot's primary-source paper, equation (1.1), available at https://www.math.wm.edu/~vinroot/RogersSzego_1.pdf. An initial direct fetch failed, but the indexed primary-source PDF returned its definition and recurrence. That source is used only for classical provenance; the mathematical acceptance above uses the explicit proof and independent reconstruction.

## 6. Replay, independence and limitations

The submitted archive has exactly the 32 manifest-bound payload files plus FILE_MANIFEST.json and SEAL.json. The pinned manifest and every payload size/hash pass. Seventeen inert source snapshots pass; the five cited predecessor review manifests independently pass all 165 bound entries. This verifies local source bytes, not new remote repository provenance or reruns of historical scientific suites.

Two new clean-directory replays each:
1. Extract and verify the pinned candidate archive, including payload closure.
2. Run both producer checkers and recover the exact saved RESULTS.json and ORTHOGONAL_SYNTHETIC.json hashes.
3. Run the reviewer's independent program in a separate directory and recover its own deterministic result file byte for byte.
4. Compare the independently calculated product certificates, endpoints, full trace polynomials and synthetic field data against the producer results only after calculation.

The new implementation imports no producer/predecessor program. It uses sparse sets of exponents for F2 arithmetic, the opposite q-Pascal orientation, and symmetric Laurent trace folding rather than the producer's triangular binomial extraction. SymPy supplies integer cyclotomic polynomials, a dense synthetic determinant and a separate irreducibility check. It covers the candidate's five declared identity controls and three required boundary cuts. The all-m conclusions rest on the proof, not on these finite cases.

All 24 producer corruption controls replay. Seven additional review controls reject a lower-order parameter mislabeled as exact order, q=1 denominator inversion, an off-by-one complementary index, both adjacent incorrect reciprocal weights, replacing the inverse endpoint with the forward endpoint, and an unchanged characteristic-two identity transported modulo three. They are named guard tests, not exhaustive adversarial coverage.

No files outside this review artifact were changed. No external writes, repository mutations, child tasks, finite-stage expansion or quantitative-priority promotion were performed.
