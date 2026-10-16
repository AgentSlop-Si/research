# Independent N13 free-cross rank review

16 October 2026 UTC. **Verdict: ACCEPT within the bounded scope below.**

The six forced degree-seven recurrence equations have coefficient rank six for every cross-node value over every characteristic-53 field. The advertised degree-37 exceptional determinant is irreducible, and the second determinant removes its rank-drop locus. The denominator-free affine parameterization is correct. No sixteen-bank existence or exclusion theorem follows from these facts alone.

## 1. Exact reviewed object and inherited scope

The reviewed coefficient matrix is the 6-by-8 E7 in `sources/RANK_DATA.json`, and the completed exact certificate is `sources/CANDIDATE_CERTIFICATE.json`, SHA-256 `d94b73bb0938c9367d686f8e70526315c142efa925954aec0e4fa8e856e5838d`. The independent checker compares both against newly reconstructed data. The completed report is frozen as `sources/CANDIDATE_REPORT.md`; its mathematical claims and the bounded findings in `sources/PROPOSED_EXISTING_CELL_PREFIXES.json` are also accepted. The proposed text correctly preserves the open parent problem and makes no larger exclusion or attainment claim. This audit does not authorize an external write or independently verify spreadsheet row mappings.

The accepted original-bank grammar fixes N=13, q=16 and characteristic 53, with independently free nonzero singleton cross nodes y,z. The arbitrary-beta expansion and forced-window necessity are inherited from `sources/PRIOR_LOWER_REVIEW.md`; their original-bank proofs are not replaced by this audit. The pinned-descent report and accepted rescaling-covariance review were read to delimit the unresolved problem. In particular no reduction of arbitrary y,z to one is assumed.

Only the newly written `check_independent.py` was executed. Candidate programs were inspected as inert text; no candidate or historical scientific program was executed, imported, compiled, or evaluated. Candidate JSON files were read only as data. There were no external writes, no support search, and no extension-element census. This is an informed independent reconstruction rather than a blinded audit.

## 2. Independent reconstruction

The checker verifies that 53 is prime and q=16 has exact order 13. In the Weyl algebra VU=omega UV, right multiplication gives

    D(r,l)=omega^l D(r-1,l)+D(r,l-1),  D(0,0)=1.

This differs from the candidate's closed Gaussian-binomial product. It reconstructs G for all four orientations from D at the signed residues, using zero when their sum is at least thirteen.

For b<=a<=12-b it then rebuilds the accepted forced moment polynomial

    v_b(a;y) = [q^(10(a+b)^2)
                - y^(13-a-b) G_-+(a,b)/G_-+(13-b,b)] / G_++(a,b).

The row labels (b,a) are (1,1),(1,2),(1,3),(1,4),(2,2),(2,3). Row (b,a) contains v_b(a+k;y), k=0,...,7. All 48 polynomial entries agree with both candidate datasets. Write E7=[A|B], so the seven nonleading coefficients h of a monic support candidate obey Ah=-B.

For D_j=det(A with column j deleted), j=0,...,6, independent formal Leibniz-term degree bounds are 34,35,36,37,38,39,40. Every bound is below 53. Determinants are computed numerically by scalar Gaussian elimination at all 53 field values, then interpolated using bound+1 distinct values. The remaining evaluations are checked. This establishes exact polynomial identities, not merely equality as functions on the prime field. It is independent of the candidate's polynomial permutation expansion.

All seven recovered minors agree coefficientwise. Their degrees are

    32, 33, 34, 35, 36, 37, 37.

D0 has leading coefficient 24; D6 has leading coefficient 48. Every Cramer determinant used below is independently reconstructed by the same degree-bounded interpolation route.

## 3. Uniform rank theorem and chart domain

Fresh polynomial Euclidean arithmetic produces U,V with

    U D0 + V D6 = 1,
    degree(U)=36, degree(V)=31.

This is checked by polynomial multiplication and coefficientwise equality. Consequently D0 and D6 cannot vanish simultaneously in any characteristic-53 field. A has exactly six rows, so rank A(y)=6 for every y in every such field, including y=0. The physical grammar still requires nonzero cross nodes.

Let f=48^(-1)D6 be monic of degree 37. Independent modular powering verifies

    Y^(53^37) = Y mod f,
    gcd(Y^53-Y,f)=1.

Because 37 is prime, these are the complete prime-degree irreducibility criteria. The checker additionally verifies the candidate's explicit irreducibility Bezout multipliers. Thus D6 is irreducible of degree 37.

A root of D6 lies in F_(53^d) exactly when 37 divides d. Therefore, when 37 does not divide d, deleting column 6 is invertible for every y in F_(53^d), and h6=lambda is a valid affine chart for every cross-node value. This includes d=2,3,4. When 37 divides d, that chart has genuine exceptional values, but A retains rank six there. Reduction modulo f checks D6=0 and U D0=1, explicitly confirming the alternate pivot on the exceptional locus. A singular chart is not a rank drop.

## 4. Denominator-free global affine family

Put C_j=(-1)^j D_j. The checker verifies the exact polynomial identity AC=0 and the primitive-coordinate identity

    U C0 + V C6 = 1.

For j=0 and 6, let W_j be the Cramer numerator vector with component j zero and with the other six components solving against -B. Independently reconstructed determinants verify

    A W_j = -D_j B.

Define H=U W_0+V W_6. Exact coefficient arithmetic then verifies AH=-B. The polynomial particular vector H has component degrees 63,64,65,66,67,68,68. Its full coefficients, and those of C,U,V, are recorded in `CHECK_RESULT.json`.

For every fixed y in any characteristic-53 field K, every solution is uniquely

    h=H(y)+tau C(y),  tau in K.

Indeed rank six makes the kernel one-dimensional, and the primitive-coordinate identity ensures C(y) is nonzero. The inverse parameter is polynomial as well:

    tau=U(y)(h0-H0(y))+V(y)(h6-H6(y)).

Thus this is a genuine global denominator-free affine family for the forced recurrence equations. At y=1, converting its parameter to h6=lambda reproduces every one of the 53 accepted prime-field pinned affine support polynomials. This checks normalization but does not re-prove their full-sector classification.

## 5. Controls, replay, and boundary

Independent one-coefficient corruptions of the kernel, particular solution, Bezout multiplier, and D6 are all rejected by their corresponding exact identities or a fresh scalar determinant. All 53 base-field specializations retain rank six. The proof over arbitrary extensions is the polynomial Bezout identity, not this finite sanity check.

A cold replay runs only the newly authored checker plus the frozen inert sources in a new directory. Its `CHECK_RESULT.json` is byte-identical; `REPLAY_VERIFICATION.json` records the comparison. `MANIFEST.json` binds the reviewed sources, new checker, report, and deterministic result. A separate archive seal binds the whole packet.

This closes the rank-drop prerequisite for the forced E7 system. An arbitrary member of the affine family need not split into seven distinct nonzero field roots, and passing these forced windows need not satisfy all thirteen original Weyl-sector systems. Both same-sign supports, the independent cross node z, full-sector compatibility, and original-bank realization still matter. No exclusion of sixteen banks with free y,z over degrees 2,3,4; no new minimal extension degree; no unrestricted bank minimum; and no arithmetic-speed claim is accepted here.
