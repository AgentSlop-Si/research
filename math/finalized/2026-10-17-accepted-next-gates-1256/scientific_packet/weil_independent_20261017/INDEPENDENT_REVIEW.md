# Independent challenge: Q18 negative-chirp formula gate

Date: 17 October 2026 UTC.

## Verdict and exact reviewed object

**ACCEPT the domain-qualified mathematical proof and formula-only gate. Keep implementation acceptance OPEN.**

The reviewed `PROOF_AND_GATE.md` has SHA-256:

`ff0c10b49fc5509ff7e89ca538fe874be91e425bdaca182347887082552bd0b3`.

No algebraic defect was found in the negative-chirp kernel, exact support, signed core ratio, Weyl covariance, or exact additive shear law. The proof includes the identity scalar b=0 and does not use invertibility of b where it is unavailable. Its characteristic-zero cyclotomic arithmetic rationale is valid, and the distinction between actual checker assertions and matrix entries implied by a circulant reduction is sound.

A separately written finite-field checker passed **27,100,842 recorded equality/condition checks**, including 26,232,633 in the requested prime-power domain. The extra 868,209 belong to a clearly separated q=15 diagnostic and do not broaden the accepted theorem. Field-setup guards are not included in these counters.

This review did not execute or import the author's checker, any uploaded/historical module, the static candidate, or any historical/derivative tests. Only the reviewer's new `independent_finite_field_check.py` was executed. Report and result-file hashing is a byte-binding operation, not execution evidence for the author or candidate.

## 1. The index ring and coefficient field must remain distinct

The model is functions on the **cyclic ring R=Z/qZ**, with q=p^k, p odd prime, k>=1. The coefficient field K contains a root zeta of exact order q and has characteristic different from p. In particular:

- q=9,25,27 mean cyclic index rings Z/9Z, Z/25Z, Z/27Z.
- They do not mean finite-field index sets F_9, F_25, F_27 equipped with trace characters.
- A nontrivial additive trace character on F_(p^k) has order p, not p^k. Replacing the stated ring by that finite field would change the theorem and invalidate this exact-root interpretation.
- GF(19), GF(101), GF(109), GF(4), and GF(64) below are coefficient fields only. Their sizes are not the dimension of the indexed operator.
- Inverses of 2 and u inside exponents are taken in Z/qZ or Z/mZ. Scalar inverses of q and m are taken in K. Therefore coefficient characteristic 2 is allowed.

The author's report specifies the correct ring explicitly. No F_q trace-character claim is being accepted.

## 2. Independent algebraic checks

With F[x,y]=zeta^(xy) and C_s[x,x]=zeta^(s*x^2/2), Fourier orthogonality gives F^-1[x,y]=q^-1 zeta^(-xy). Therefore

    U_b[x,y] = q^-1 sum_z zeta^(-b*z^2/2 + (y-x)*z).

The sign follows independently from the stated displacement operator

    D(a,c) f(x) = zeta^(c*(x-a/2)) f(x-a).

Substitution yields C_s D(a,c)=D(a,c+sa) C_s and F D(a,c)=D(-c,a) F. Thus conjugation by F^-1 C_(-b) F gives (a,c) -> (a+bc,c). Positive chirp gives the opposite shear under these same conventions.

### Exact support and completed square

For b!=0 modulo q, use the canonical representative and write g=gcd(b,q), m=q/g, u=b/g. The residue of u modulo m is a unit. Shifting z by m multiplies the kernel summand by zeta^((y-x)*m). The quadratic changes vanish modulo q. If g does not divide y-x, this multiplier is not one, so the invariant sum is zero in the coefficient field.

When x=r+gX and y=r+gY, the summand has period m; its g repetitions cancel the factor g in q. Setting eta=zeta^g and Delta=Y-X gives

    U_b[x,y] = (1/m) sum_z eta^(-u*z^2/2 + Delta*z)
             = kappa_(-u,m) eta^(Delta^2/(2u)).

The square completion is valid because u and 2 are units modulo m. It never divides by the original nonunit b modulo q.

For any unit a modulo m, the invertible index substitution r=x-y, s=x+y proves

    G(a)G(-a) = sum_(r,s) eta^(a*r*s/2) = m,
    G(a) = sum_z eta^(a*z^2/2).

The inner sum vanishes for every r!=0, including nonunit r. Since m is nonzero in K, both Gauss factors are nonzero. This proves support exactness rather than only support containment. There are g dense m-by-m residue blocks, with exactly m nonzeros in every row and column.

Expanding Delta^2 produces the core eta^(-u^-1*X*Y) after nonzero row/column scalings. For local rows and columns 0,1, the ratio of diagonal products to off-diagonal products is eta^(-u^-1), which has exact order m. The corresponding positive-chirp ratio is its inverse. These two ratios are distinct because m>1 is odd and u is a unit. Their orders alone are identical and therefore insufficient to determine the sign.

### Weyl reduction and additive law

For S_b(t)=sum_z zeta^(-b*z^2/2+t*z), replacing z by w+c gives

    S_b(t+bc) = zeta^(c*t+b*c^2/2) S_b(t).

This shift uses no inverse of b. For t=y-x+a, multiplying by zeta^(c*(x-(a+bc)/2)) gives precisely the phase zeta^(c*(y+a/2)) on the other side of the matrix covariance identity. Thus the report's equation (7) really is sufficient for every a,x,y, rather than a restricted covariance condition. This includes b=0.

Expanding the convolution of two kernels and summing the intermediate coordinate forces the two Fourier indices equal. The surviving term is the kernel with coefficient b+c. Equivalently, exact conjugation cancels F F^-1. Both arguments give

    U_b U_c = U_(b+c), U_0=I, U_b^-1=U_(-b),

with no projective scalar on this subgroup. This does not settle a global Weil representation normalization.

### Domain boundaries

The proof correctly requires odd p and k>=1. The p=2 case is not covered because the exponent-ring inverse of 2 is unavailable. A nonprimitive root or noninvertible q is excluded. The gcd-based one-dimensional argument also works at arbitrary odd moduli when q is invertible and a primitive q-th root exists, but that observation is not used to enlarge the prime-power claim or certify any historical implementation.

## 3. Independent arithmetic controls

The new checker separates residue exponents from coefficient operations. It imports only Python standard-library facilities; it does not import any research file, contact a network, run a subprocess, or install anything. Its three binary-extension coefficient fields are checked as actual fields by verifying an inverse for every nonzero residue of each polynomial quotient before use.

Cases within the requested domain:

- q=3 in GF(7): 513 recorded checks
- q=5 in GF(11): 4,749
- q=7 in GF(29): 22,513
- q=9 in GF(19): 73,965
- q=25 in GF(101): 10,580,269
- q=27 in GF(109): 15,453,633
- q=3 in GF(4), modulus X^2+X+1: 513
- q=7 in GF(8), modulus X^3+X+1: 22,513
- q=9 in GF(64), modulus X^6+X+1: 73,965

These are 95 scalar-b cases, including nine identity cases and every scalar in each listed coefficient-field case. The q=15/GF(31) diagnostic adds 15 scalar cases and 868,209 checks, explicitly flagged outside the requested prime-power scope.

Across all ten cases, the recorded checks include:

- 41,006 separately evaluated Fourier-conjugation matrix entries
- 25,029,230 full entrywise Weyl covariance comparisons, exhausting b,a,c,x,y
- 41,006 additive-convolution comparisons, exhausting b,c,d; circulant translation then supplies all x,y entries
- 991,402 Fourier-label and 991,402 chirp-label covariance comparisons
- 1,772 exact support and 1,772 completed-square comparisons
- 100 nonzero Gauss-product tests and 100 nonvanishing tests
- 100 exact signed ratios and residual-order tests
- 100 opposite-chirp operator rejections and 100 distinct signed-ratio rejections
- 660 noncanonical integer-b comparisons

All b+c=0, b=0, c=0 and nonunit-b cases are included in the relevant exhaustive loops. Identity checks use all circulant differences, not only a single diagonal entry.

### Characteristic-2 negative-control nuance

The report's explicit q=3 counterexample is stated over Q(zeta), where the two diagonal entries are different. It is correct in that domain. A diagonal-only negative control would not work universally: over GF(4), with zeta^2+zeta+1=0, the two q=3 diagonal entries are both 1. The full kernels are

    U_1 first row:     (1, zeta^2, zeta^2),
    U_(-1) first row:  (1, zeta,   zeta).

The off-diagonal entries and signed ratios still distinguish them. The independent controls therefore reject the full wrong-chirp operator and verify the signed ratio, rather than relying on diagonal separation. This is a boundary caution, not a defect in the author's explicitly characteristic-zero example.

## 4. Report coverage and cyclotomic claims

The listed q values in the author's characteristic-zero report sum to 100. Their squares sum to 1,808 and their cubes to 40,060. Thus its distinction between 1,808 directly formed circulant kernel numerators and 40,060 implied matrix entries is arithmetically consistent. Its reduced Weyl count is also 40,060, with the sufficiency proved above.

The reported convolution domain gives 1,224 checks for all b,c,d at q=3,5,7,9, plus 4,780 for every b,d and deduplicated c in {0,1,-b} at q=11,13,25,27, totaling 6,004. The report does not claim all b,c pairs at the latter moduli. The 54,028 aggregate equals the sum of the result JSON's group counters.

The prime-power polynomial Phi_(p^k)(X)=sum_(j=0)^(p-1) X^(j*p^(k-1)) is the required cyclotomic polynomial. After X -> X+1 its reduction modulo p is the leading monomial and its constant term is p, so Eisenstein establishes the stated characteristic-zero field model. This validates the mathematical arithmetic rationale. This review has not independently executed the author's checker or audited every line of its implementation; its execution counts are bound reported evidence, supplemented by the separate controls above.

## 5. Reproduction and retained gates

Reviewer command executed successfully with exit status 0:

    python independent_finite_field_check.py

Files in this review packet:

- `independent_finite_field_check.py`: newly authored checker
- `EXACT_FINITE_FIELD_RESULTS.json`: exact field definitions, primitive-root encodings, case counts and source hash
- `RUN.log`: successful run output
- `REVIEW_BINDINGS.json`: reviewed report/result/source identities and reviewer artifact identities
- `MANIFEST.sha256`: review packet file bindings

The author's reported accepted static-candidate hash remains inherited source-report evidence only. This reviewer did not recover or re-hash that implementation. No conclusion here upgrades candidate execution, dispatch correctness, malformed-input behavior, the 13 derivative tests, original exhaustive SL2/subgroup suites, prior bounded-API byte recovery, global representation normalization, higher-dimensional results, operation/preparation/bit costs, numerical stability, practical speed, or novelty.

The parent item remains TO RESEARCH, priority 42, with implementation acceptance open. No external write, upload, or publication was performed by this review.
