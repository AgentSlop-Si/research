# Fresh whole-proof review: the remaining central family

20 October 2026 UTC. Verdict: **ACCEPTED WITHIN THE EXACT STATED SCOPE**.

This is a new whole-argument review of the frozen author candidate, not an adoption of the simultaneous exploratory auditor's findings. No mathematical correction, missing lemma, essential repair, or author-text revision was supplied by this reviewer. Acceptance binds the exact author manifest and report identified below.

## Accepted scope and frozen identity

For every odd prime p, every integer s>2, and every characteristic-zero primitive p^s-th root q, retain the original recurrence P_(j+1)=X P_j-(1-q^j)P_(j-1), P_0=1, P_1=X, the original Gaussian Rogers–Szegő polynomial H, and ordinary characteristic-zero derivatives. Normalize v(q-1)=1 and put W=3p²-2p, d=p(p-1)/2.

The new central result proves that all 2p previously unresolved nonzero central roots of P_(2p²+1) are simple. Their original root-derivative valuations are:

- W+d+1=(7p²-5p+2)/2 when p>=5. In the author's U coordinate, the normalized ordinary derivative has residue 1/8.
- 76/3 when p=3, with v(U+1)=4/3 and v(f_U)=13/3.

Together with the accepted partial theorem's exact zero-root and noncentral-root results, this proves squarefreeness of both original P_(2p²+1) and H_(2p²+1), and nonvanishing of the original algebraic-square Christoffel–Darboux kernel at every P root. This accepts the adjacent leading-two r=2 completion only. It does not assert arbitrary degrees or digits, odd-composite orders, global F020/F023 closure, novelty, or any FFT or complexity improvement. It does not assert a constant ordinary derivative valuation across the entire degree family.

Frozen candidate identifiers:

- MANIFEST.json: 072e4134daea3f759d79550c891027abb0410ed38aac6826635fee085f730147.
- REPORT.md, 18,236 bytes: 192f8509aebe5c3dd23060faae8702789fa59e6aa09f19d26a5be8757cc75aed.
- THREE_CERTIFICATE.json: d85d43bbebb9c0353daef5c0256d96e2c7705a7b968dd4d83e17acedacc1232e.

Every one of the ten candidate manifest entries and all six exact dependency bindings was checked. Both accepted dependency manifests were checked against their files. The prior partial report and independent review were also checked byte-for-byte against the public adjacent-degree archive, SHA-256 3cf2c2567755df12b394c8c28feb0faa54ed304d1f46cd070ceec3bb344ee600; all 43 public manifest entries were verified. Historical private source locators are not publication links and are not needed to identify the scientific bytes.

## 1. Imported assertions and original normalization

I read the actual accepted partial report and review, plus its accepted leading-two source. The imported ingredients are the exact ordinary Newton identities, the original H/P change of variable, the complete disk count before simplicity, the central residual (U+1)^p, the coefficientwise ordinary derivative bound of weight d, and the exact neighbor value E and derivative lower bound E.

The quotient F=P_(2p²+1)/X is a polynomial and is even. Substitution X²=t^p U therefore gives f in the original cyclotomic coefficient field, without requiring a square-root extension for its coefficients. The accepted F' residual gives the stated f_U residual after ordinary differentiation and exact scaling; it is not obtained by differentiating the inseparable residue polynomial.

All recurrence edges and Newton denominators used in the proof are nonzero: 2p²+1<p³<=p^s. The endpoint edge has value v(1-q^(2p²))=p², not 2p². The normalization e=v(p)=(p-1)p^(s-1) is retained throughout.

## 2. All central competing coefficients and gaps

On the central boundary, z+q^j has value p/2 for j divisible by p, including j=0, and value 1 otherwise. Thus the exact central Newton-product value is

T_c(m)=m+(p/2-1)ceil(m/p).

For m=c p²+a p+b, direct substitution in the floor formula for W(m) gives

2 Delta_c(m)=a(p-1)+b+(p-2)1_(b>0).

This establishes the stated zero set {0,p²,2p²} and the positive gap (p-1)/2 uniformly. It also checks the endpoints and both partial p-block cases; no assumption from a finite range is needed.

For the neighbor, superadditivity leaves this gap in every term except k=p². At that odd admissible pivot the remaining bracket is exactly zero. Consequently its relative error is at least (p-1)/2.

For the ordinary derivative double sum, I independently checked the reduction to

p+W(j-1)/2-p^ord_p(j)+Delta_c(m).

The exhaustive cases are: j prime to p, j divisible exactly once by p, j=p², and j=2p². Their first-part lower bounds are respectively p-1, (p-1)/2, 0, and 3p²/2-p. When j=p², parity excludes m=0 and the only zero-slack admissible m is p². This proves the unique pivot (k,m)=(2p²,p²) and the required gap for every other ordinary derivative term.

For H_(2p²), each intermediate even k differs from the odd p². The p²-floor contribution to W(2p²)-2W(a)-W(k) is at least p²-p; every other floor contribution is nonnegative. Adding the central slack gives excess at least (p²-1)/2. Hence the two-term polynomial approximation used in the root-location argument is justified. These are uniform arguments over every index, not interpolation from the enumerated controls.

## 3. Grouped products and the root-location estimate

The characteristic-p grouped-product lemma is valid. In the q-binomial coefficient for 1<=k<p, the numerator has one factor of h-order p and k-1 factors of order 1; its denominator has k factors of order 1. The resulting order is p-1. The final product coefficient differs from its h=0 value only in order at least p. This proves the claimed divisibility for all coefficients, rather than incorrectly estimating each individual factor.

For the p-factor blocks of N_(2p²), h=q^p-1 has order p. The normalized errors are at least p(p-2)/2 for the divisible block and p(p-2) otherwise. Both are strictly greater than p for p>=5. Replacing the second p² block after taking p-th powers introduces still larger error. Every main product has total value W, so the absolute error is strictly above W+p.

For the constant Newton term, the odd-index partition covers exactly the required odd indices. Its p-divisible block is the exact Frobenius identity stated in the report; the other blocks have the same sufficient gap. This gives the sign -t^(p²)D_0^(2p).

I independently checked both linear normalized product coefficients in (4.4): the leading units are -1 and the two sums are 1/2 modulo p. The replacement R/R_0 has error of value p/2-1>1. Also z+1 has value p/2>1. Using (z+1)²=zX² gives cancellation through relative order 1 in N_p²-t^pD_0². Its p-th power, and every discarded Newton term, have value strictly above W+p.

The transfer back to characteristic zero is valid and explicitly ramification-dependent: for p>=5, e>W+p. The evaluated even original polynomial is an integer polynomial in t. A coefficient divisible by p cannot contribute below that cutoff, while the characteristic-p computation annihilates all unit-coefficient terms through the cutoff. Thus its actual value is strictly above W+p. The quotient perturbation has exact value W+d with d>p, so v(f(-1))>p follows.

Finally, the inference to every central root is sound. After U=-1+V, the coefficients are integral, a_p is a unit, and 1<=j<p have v(a_j)>=d because those ordinary differentiation factors j are p-adic units. For 0<v(V)<=1 the p-th term is uniquely smallest: the constant is above p, the lower positive degrees are at least d>p, and every higher degree gains strictly larger V-weight. Hence all central roots satisfy v(V)>1. No stronger unproved constant-coefficient formula is required.

## 4. First correction and ordinary derivative for p>=5

The neighbor and ordinary derivative nonpivot gaps are at least 2 for p>=5, sufficient to discard them through relative order 1. The M' term has additional value at least p/2>1. The H/P prefactor term has weight at least 2e+W>D+1, so the conversion is valid off the H_(2p²) root set as required.

I derived the pivot ratio directly from the two Newton coefficients and the ordinary coordinate derivative. It is exactly the displayed main factor

X² [2z^(p²)/(z-1)] Q_A/(1-q^(p²)).

In particular the powers of z, the sign, the endpoint edge, and the factor 2 are correct. The coordinate factor is 1 with error above 1, and (1-q^(p²))/(-t^(p²)) also has error above 1 with the actual ramification.

For Q_A, separating divisible and nondivisible indices gives normalized leading unit -1 and first coefficient

sum_(p does not divide j) (2j-1)/2=(p²-1)/8=-1/8 modulo p.

Divisible-index and mixed-characteristic errors are above 1, so no omitted term affects this coefficient. The ratio is U(1-t/8+error above 1). At U=-1+V with v(V)>1, adding the exact quotient term gives t/8 with all other terms above 1.

The remaining scalar K has value d and residue -epsilon U^((p-3)/2), which equals 1 at U=-1. Thus f_U/t^(d+1) has residue +1/8, not -1/8. The retained M' error remains strictly larger. This proves a nonzero original ordinary derivative for every central root without differentiating a characteristic-p residual.

## 5. The fixed p=3 certificate and every s>=3

This part was checked by an independent construction, not merely by rerunning the author's E/O recurrence. I reconstructed the original P_19 using the path-matching formula: sum over all 6,765 nonadjacent edge subsets of {1,...,18}, with each subset contributing the appropriate X power times product(q^i-1). I then substituted q=1+t and X²=t³(V-1) by integer binomial expansion. All ten resulting integer V-coefficient polynomials agree exactly with THREE_CERTIFICATE.json.

The four first p-unit monomials are exactly (degree, residue)=(25,1),(28,2),(24,2),(21,1). The divisibility C_j by t^(9+2j) follows independently from the number of recurrence edges in a term of X²-degree l: at least 9-l edge factors plus the substituted t^(3l), with l>=j.

For j=0,1,2,3, every coefficient divisible by 3 therefore has weight at least 18+9+2j, respectively 27,29,31,33. These are strictly larger than the indicated unit degrees 25,28,24,21. Higher unit monomials also have larger weights. The unique minimum cannot cancel after evaluation in any cyclotomic field with e>=18. This proves the four valuations for every s>=3, including minimal ramification s=3. It is a fixed-degree symbolic certificate plus a uniform inequality, not extrapolation from several cyclotomic examples.

The resulting coefficient valuations (4,7,3,0), integrality of all higher coefficients, and residue V³ force v(V)=4/3. The coefficient field has integer valuation group, so the nonleading residue-zero coefficient a_4 has value at least 1. The complete ordinary derivative comparison is then 7, 13/3, e+8/3, at least 5, and at least 16/3 for subsequent terms. The unique minimum is 2a_2V. The factor 3 in the cubic derivative is retained and is essential to this argument. Thus v(f_U)=13/3 uniformly.

## 6. Original roots, H transfer, and kernel

At a nonzero root, exact ordinary differentiation gives P'=X F'=2U t^W f_U. Since 2 and U are units, this yields precisely the stated original P-derivative valuations. The accepted count includes all 2p central roots with multiplicity before simplicity, so no root or repeated residual location is omitted.

The original H/P coordinate derivatives are units at corresponding roots, and the derivative of the prefactor vanishes there by the root equation. Thus simplicity and the original derivative valuations transfer. The exact zero root and all noncentral roots are supplied by the already accepted partial theorem.

All recurrence edges below n are nonzero; backward recurrence makes P_n and P_(n-1) coprime. The original algebraic-square CD identity therefore has a nonzero right-hand side at every root now that the last central derivatives have been proved nonzero. No positivity, complex absolute-value square, Jackson derivative, or interlacing argument is involved. Algebraic nonvanishing transfers between primitive characteristic-zero embeddings.

## 7. Replays, adversarial controls, and independence

The following are auxiliary controls, except for the fixed P_19 symbolic certificate described above:

- Cold replay of the untouched author checker produced byte-identical CONTROL_RESULTS.json and THREE_CERTIFICATE.json.
- Independent direct-sum Newton-weight enumeration covers p=3,5,7,11,13,17,19. It uses explicit cumulative p-power valuations and central counts instead of the author's floor-formula implementation, and verifies all competing terms and unique pivots.
- Direct multiplication of grouped products checks the claimed h-divisibility in p=3,5,7,11.
- A separate exact cyclotomic recurrence and explicit binomial q=1+t transform reconstructs every centered coefficient, not only a truncated jet, for (p,s)=(3,3),(3,4),(3,5),(5,3),(5,4),(7,3). The ordinary Newton and derivative comparisons confirm the reported values in all six fields, retaining e and the residue p/t^e=-1.
- An adversarial derivative mutant dropping the ordinary integer differentiation factors produces the wrong p=3 minimum 8/3 instead of 13/3 and is rejected.
- The p=3 nonpivot gap is exactly 1, rejecting an attempted extension of the p>=5 first-order gap argument to p=3. The independently reconstructed p>=5 first coefficient also rejects a reversed 1/8 sign.

These tests do not establish an unlimited family by themselves. The acceptance is based on the uniform mathematical checks in Sections 1–6 and the exact fixed-polynomial certificate with its all-e>=18 dominance argument.

The reviewer did not participate in the prior simultaneous exploratory audit and did not supply an essential proof ingredient or repair. The author's disclosed exploratory overlap remains disclosed; it is not used as an acceptance credential. No candidate proof bytes were changed. No further fresh reviewer is required on account of a reviewer-created proof contribution. Any future mathematical modification must be frozen and reviewed as new bytes.
