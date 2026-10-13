# Independent review: nine N11/F23 signed-bank obstructions

Review date: 13 October 2026. **Verdict: ACCEPT, within the declared all-F23 scope.**

The nine displayed monic quintics, rank-five certificates, field-root evaluations, and all-subset obstruction are correct. No mathematical or arithmetic repair is required. Combining these nine exclusions with the prior 211 nonsingular gates gives the claimed one-sided six-node lower bound for every primitive eleventh root in F23 and every nonzero base-field singleton node. Reflection gives a fourteen-bank lower bound only for the architecture with one effective cross-sign node in each orientation. This is not an attainment or unrestricted optimum result.

## 1. Exact reviewed source and source chain

The reviewed candidate is `Signed_Bank_Nine_F23_Obstructions_Candidate_2026-10-13.zip`, 1,490,227 bytes, SHA-256:

`841e5170f693db12053e23a081bd5394b4de2da072c9f05a3019eb234096a805`.

This review includes those exact bytes as `CANDIDATE_SOURCE.zip`. Its 19 archive members match the live candidate directory byte for byte. Every one of the 18 entries in its inner manifest was checked for both length and SHA-256. The candidate report has SHA-256 `df2125a018f94e7ef4b542c6dbe5a8043a9cc7e37d812dbb8fc9af0a24c33735`; its frozen contract has SHA-256 `76b80776c4862390dbb63ffab5892ea3456fa8493346575dff1ca79dad6240f2`.

The inherited report, 220-case matrix file, and manifest were independently compared with the corresponding members of `Last165_Independent_Review_v2_Q08_REPAIR_and_Bounded_ACCEPT_2026-10-13.zip`, SHA-256 `613cb7d508d86c0c60cec07a2daa35aa5298f588fd30628dd70f887b2b5032bb`. All three are exactly equal. The prior report's SHA-256 is `b0b1b234f9c55112ea323816f23f2ce0c430fdbb4715b1eb79af1a7e3813c303`; the prior matrix-file SHA-256 is `9d929d034e8d8ad7f6e8014a342e5635e73137e769e908b28e94e198b4a8652b`.

`SOURCE_VERIFICATION.json` and `ARCHIVE_CHAIN_VERIFICATION.json` give the complete receipts. The three human-readable text copies in this review are exact extracted bytes, not rewritten source editions. The archived declaration is evidence of the frozen contract; an actual before-computation timestamp is not independently established by the mathematical check and is not needed for the result.

## 2. Independence and fresh work

No candidate or historical scientific program was executed, imported, compiled, or evaluated. Reading a program member for its byte hash did not execute it. Only the newly written `independent_check.py`, Python standard library only, performs scientific calculations for this review. All fresh scientific results are completed and saved before candidate numerical JSON or CSV is opened for comparison.

The fresh route is deliberately different in key steps:

1. It constructs coefficients by right-multiplication in the noncommutative algebra, rather than enumerating binary words or using a copied Gaussian table.
2. It independently rebuilds **all 220 gates**, not only the nine candidate cases, and evaluates every 6-by-6 determinant by the full 720-term Leibniz formula.
3. It finds each monic quintic from signed 5-by-5 cofactors of the first five rows. Modular row reduction is a crosscheck, not the source of the quintic.
4. It constructs every five-node polynomial by Vieta's elementary-symmetric formula, rather than iteratively multiplying its linear factors.
5. It verifies the literal original resolvent grammar using direct 11-by-11 matrix inversion for 160 legal bank controls, including alpha=0 and beta=0 cases.

Exact workloads: 1,210 direct target-coefficient checks; 4,840 reflection identities; 1,760 two-sided inverse checks; 19,360 literal bank coefficient checks; 220 fresh gates and determinants; nine cofactor kernel certificates; 207 root evaluations; and 237,006 pair/subset tests. These counts measure this finite checker, not the cost of evaluating a legal bank representation.

## 3. Derivation from the original legal bank

Work over F23, N=11, with q of exact order eleven. Set S e_t=e_(t+1) and T e_t=q^t e_t, so TS=qST. For a sign pair (epsilon,delta), put U=S^epsilon, V=T^delta, and z=q^(epsilon delta). Then VU=zUV.

In the ordered monomial basis U^r V^ell, right-multiplication by U+V gives the coefficient recurrence

    D(r,ell) = z^ell D(r-1,ell) + D(r,ell-1),
    D(0,0)=1,

with absent indices zero. The Gaussian product formula, or this recursion with the root-of-unity identity, gives D(r,11-r)=0 for 1<=r<=10 and endpoint coefficients one. The fresh checker verifies this degree-eleven identity for every tested q and orientation. Therefore, for every original branch

    X_j = alpha S^epsilon + beta q^(epsilon delta j) T^delta,

we have X_j^11=(alpha^11+beta^11)I. If Delta=1-alpha^11-beta^11 is nonzero, telescoping proves on both sides that

    (I-X_j)^(-1) = (I+X_j+...+X_j^10)/Delta.

Thus the original bank, with its original factor 1/11, has coefficient at W_(a,b)=S^a T^b

    alpha^r G_(epsilon,delta)(a,b)
      * beta^ell/(11 Delta) * sum_j w_j q^(epsilon delta j ell),

where r=[epsilon a]_11, ell=[delta b]_11, and G is D(r,ell) for r+ell<=10 and zero otherwise. The formula includes beta=0 and alpha=0 with the usual zeroth-power convention. In particular it uses no inverse beta and no forbidden change of grammar. Different legal beta values only change sector amplitudes; they cannot change the common-alpha moment necessity.

Direct coefficient extraction from F[k,t]=q^(-kt) gives

    (1/11) sum_t q^(-bt) F[t+a,t]
      = (1/11) sum_t q^(-t^2-(a+b)t)
      = C q^(3(a+b)^2),

where C=(1/11)sum_t q^(-t^2) is nonzero and 4*3=1 modulo eleven. This is a coefficient normalization only; no map is applied to the target or generators. All 121 coefficients were directly checked for each of the ten primitive q values.

## 4. Forced moments and all effective-node guards

Assume exactly one effective minus-plus alpha node y. At (a,b)=(11-b,b) for b=1,2, only minus-plus has support. Its normalized target coefficient is one. Its normalized sector amplitude is therefore

    T_b = 1/[y^b G_-+(11-b,b)].

The source denominators are nonzero. A zero singleton alpha cannot represent the target at (10,1); likewise a singleton realized entirely with beta=0 cannot do so. If multiple original banks share the same effective alpha, their amplitudes add sector by sector and the same equation holds. No assumption of equal beta is used.

For b<=a<=10-b, both negative-delta orientations vanish. G_++ is nonzero. Hence any representation must satisfy

    v_b(a) = [q^(3(a+b)^2)-T_b y^(11-a)G_-+(a,b)]/G_++(a,b)
           = sum_x A_(b,x) x^a.

There are nine consecutive moments for b=1 and seven for b=2. The first sequence gives four length-six windows and the second gives two. These are exactly the six rows of M. The fresh computation checked the support and denominator conditions at every primitive q and every nonzero y.

Repeated ordinary plus-plus nodes merge by addition of amplitudes. They do not create derivative atoms. A zero plus-plus node contributes zero on these strictly positive-exponent windows, so may be discarded from this necessary-condition argument. This does not discard its possible contribution to the untested axis; no sufficiency claim is being made.

If at most five effective plus-plus nodes exist, their distinct nonzero set X has at most five members. Under the candidate's contract X is contained in F23*. Extend it to a five-element set X' inside the 22-element set F23*. Then

    g(t) = product_(x in X') (t-x)

is monic of degree five, squarefree, has nonzero constant term, and splits over F23. For each selected window,

    sum_(k=0)^5 g_k v_b(a+k)
      = sum_x A_(b,x) x^a g(x) = 0.

Consequently M(g_0,...,g_5)^t=0. This padding by *distinct nonzero field elements* is the correct necessary splitting guard for fewer nodes. Padding by powers of t would not justify a squarefree test and is not used here. The proof needs only necessity; the complex-field sufficiency theorem in the older common-node source is not imported as a finite-field sufficiency claim.

## 5. Nine exact kernel and splitting certificates

The ten primitive q values, independently enumerated from x^11=1 and x!=1 in F23, are 2,3,4,6,8,9,12,13,16,18. Of their 220 pairs with y in F23*, precisely the following nine matrices are singular. Each has rank exactly five.

Coefficient vectors are ascending, so the last coordinate is the coefficient of t^5. The minor is the determinant on the first five rows and columns.

| q | y | Unique monic kernel coefficients | Distinct nonzero roots in F23 | gcd(g,g') | Minor |
|---|---|---|---|---|---|
| 3 | 4 | (13,3,1,22,12,1) | 3,22 | 1 | 8 |
| 4 | 10 | (15,12,6,14,6,1) | 22 | t+1 | 5 |
| 9 | 14 | (2,17,11,13,6,1) | 6,11 | 1 | 13 |
| 12 | 7 | (2,5,7,22,10,1) | 20 | 1 | 17 |
| 13 | 4 | (6,4,18,1,8,1) | none | 1 | 3 |
| 13 | 15 | (14,1,14,17,12,1) | 3,21 | 1 | 8 |
| 16 | 11 | (5,15,22,10,10,1) | none | 1 | 17 |
| 18 | 2 | (21,19,1,20,19,1) | 5 | 1 | 18 |
| 18 | 10 | (22,12,0,4,19,1) | 2 | 1 | 15 |

For an explicit elimination-free construction, let A be the first five rows of M and let v_j=(-1)^j det(A with column j removed), j=0,...,5. Laplace expansion gives A v=0. The independently computed sixth row also has zero dot product with v. Since v_5 is nonzero, normalize by v_5 to obtain the table. The nonzero first-five minor proves rank at least five; the nonzero full kernel vector proves rank at most five. Thus rank is exactly five and the entire kernel is one-dimensional. A monic degree-five vector in that kernel is unique.

The full row-reduced matrix is independently checked to be five identity columns, last column (-g_0,...,-g_4,0)^t, and a zero sixth row. The fresh file contains all cofactor vectors, minors, original moments, matrices, root evaluations, derivative gcds, and exact factor data.

None of these unique monic polynomials has five distinct nonzero F23 roots. The padded-node necessity therefore contradicts all nine possible at-most-five-node representations. At (q,y)=(4,10), the exact factorization is

    (t+1)^2 (t^3+4t^2+5t+15).

That polynomial also fails squarefreeness; the other eight are squarefree but do not split over F23. This report does not promote the eight nonsplitting observations to nonexistence over a splitting field, or add a separate extension-field theorem for the repeated-root case.

## 6. Exhaustive second certificate and controls

Independently of the cofactor quintics, the checker enumerates all C(22,5)=26,334 five-element subsets X of F23*. It obtains each monic coefficient using Vieta's formula

    g_k = (-1)^(5-k) sum_(Y subset X, |Y|=5-k) product_(x in Y) x,

then directly evaluates all six original recurrence rows for each of the nine pairs. These are 237,006 pair/subset tests. No test is accepted. The successive survivor counts after one through six equations are:

| Pair | Successive survivors |
|---|---|
| (3,4) | 1144,45,3,0,0,0 |
| (4,10) | 1127,58,2,2,0,0 |
| (9,14) | 1148,55,1,0,0,0 |
| (12,7) | 1141,42,2,0,0,0 |
| (13,4) | 1138,47,0,0,0,0 |
| (13,15) | 1163,39,1,0,0,0 |
| (16,11) | 1153,55,2,0,0,0 |
| (18,2) | 1090,46,1,0,0,0 |
| (18,10) | 1126,58,2,0,0,0 |

The independently generated CSV records every subset, all six coefficients, and all 54 recurrence residuals. Every parsed cell agrees with the candidate's complete compressed CSV, including all failed rows. The check is an exhaustive base-field obstruction, not a search over extension-valued nodes.

Four fresh synthetic controls test a valid rank-five five-node family, a three-node family, repeated nodes, and a zero node. Every case has a padded distinct-nonzero annihilator with all six residuals zero. The supplied synthetic controls also pass direct independent evaluation. The literal bank controls use (alpha,beta)=(0,5),(5,0),(1,1),(2,5) for every primitive q and all four orientations. Their Delta values are respectively 2,2,22,1. All are legal. For every branch, both inverse products are identity. All direct bank Weyl coefficients agree with the formula above, including the 1/11 normalization.

## 7. Combination with the prior 211 and the exact fourteen-bank scope

The prior 211 nonsingular gates are preserved under their original stronger hypotheses: q and the singleton node y are the tested base-field values, while same-sign nodes, sector amplitudes, and legal beta parameters may lie in an extension. An invertible matrix over F23 remains invertible over every extension; multiplying a degree-at-most-five annihilator by a suitable power of t supplies a nonzero length-six vector, which cannot lie in its kernel. Unlike the new splitting argument, that older argument does not need a squarefree padded polynomial. This review freshly recomputes and agrees with all 211 determinants but does not replace their extension-node scope with the narrower successor contract.

For the nine singular pairs, the new argument requires all relevant plus-plus nodes to be in F23, as supplied by the frozen all-parameter-F23 contract. Taking the union of the prior 211 cases and these nine proves:

**For N=11, every primitive eleventh root q in F23 and every nonzero y in F23, a legal representation with all original bank parameters in F23 and exactly one effective minus-plus node y requires at least six effective plus-plus nodes. Negative-delta orientations are unrestricted in number.**

Under simultaneous reflection (a,b,epsilon,delta) to (-a,-b,-epsilon,-delta), the local indices r,ell and epsilon*delta are preserved, and q^(3(a+b)^2) is unchanged. It exchanges ++ with -- and -+ with +-. No pre/post map or one-coordinate reflection is added. Thus exactly one effective plus-minus node forces at least six effective minus-minus nodes in the same base-field contract.

If both cross-sign orientations have exactly one effective node, the disjoint orientation groups need at least 6+1+1+6=14 effective nodes, hence at least fourteen actual banks. Multiple banks sharing a node can only increase the actual bank count. This does not assume that either singleton equals one, that the same-sign node sets coincide, or that the negative-delta bank count was bounded in the one-sided argument.

**Unchanged boundaries:** no fourteen-bank attainment in F23; no lower bound for different cross-sign allocations; no unrestricted fourteen-bank optimum; no new characteristic-zero theorem; no exclusion for extension-valued singleton nodes; no universal extension-node claim for these nine; no field descent; and no arithmetic-speed claim. The older q=2 sextic family and its base-field nonsplitting result are not rerun or strengthened here. Its different six-node family is not used to infer the five-node result. The historical characteristic-zero fourteen-bank construction is not a base-field attainment certificate.

## 8. Replay and deliverables

Run `python independent_check.py` from this folder. It reads `CANDIDATE_SOURCE.zip` only as inert source bytes after completing all new scientific computations. An alternative output directory may be selected with `--out`. No network, package installation, candidate script execution, or historical script execution is required.

The packet contains the exact candidate archive; this review; the fresh checker; fresh all-220 gates; full nine-case cofactor, root and factor certificates; the exhaustive subset CSV; fresh legal-bank and padding controls; source-chain receipts; and deterministic replay verification. `MANIFEST.json` binds the final packet members and the external seal binds the archive as a whole.

No Sheet, GitHub, or other external-service write was made, and no historical or candidate source file was changed. The stopping condition is met: the nine proposed additional obstructions and their union with the prior census are independently verified within the precise stated scope.
