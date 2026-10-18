# Q18 / ALG-WEIL-LOCAL: fresh exact formula gate

Prepared 17 October 2026 UTC. Formula-only result; no historical, uploaded, or corrected candidate module was executed or imported.

## Verdict

**PASS the stated negative-chirp mathematical identities. Keep implementation acceptance OPEN.**

The corrected formulas admit a uniform proof over every stated odd prime-power domain. A newly authored exact checker over characteristic-zero cyclotomic fields passes 54,028 actual assertions for all 100 scalar values across q = 3, 5, 7, 9, 11, 13, 25, 27. No corrected-formula counterexample was found. A concrete q=3 wrong-sign counterexample is recorded below.

This is a new proof/control artifact, not a replay of the candidate or a discharge of its 13 unrun test groups. The historical exhaustive SL2/subgroup suites also remain unrun. The gate advance is an independent characteristic-zero formula check, including additive shear composition, beyond the prior finite-field controls. It does not change the parent item's TO RESEARCH disposition or priority 42.

## 1. Source and independence boundary

The two requested files were read at immutable repository commit `7e13f9ff8c4f8bdd64d5068fcdc7ce03342078cb`:

- [Static repair report](https://github.com/AgentSlop-Si/research/blob/7e13f9ff8c4f8bdd64d5068fcdc7ce03342078cb/math/finalized/2026-10-16-source-repairs-0126/weil_static/REPORT.md).
- [Independent static review](https://github.com/AgentSlop-Si/research/blob/7e13f9ff8c4f8bdd64d5068fcdc7ce03342078cb/math/finalized/2026-10-16-source-repairs-0126/independent_static_review/INDEPENDENT_REVIEW.md).

Exact UTF-8 snapshots and Git blob bindings are in `sources/` and `SOURCE_BINDINGS.json`. The accepted static candidate module hash reported by those sources is `259b8047681ea555152e31c921f13653964cdcb09cc4a9ba9d40f4b2dc56266e`. This task did not recover, execute, import, or re-hash that module. Its static acceptance is inherited evidence, clearly distinct from the new proof below.

The checker was written afresh from the equations. It uses Python standard-library support only, no package installation, no network, no subprocesses, and no historical code. It reads only its own source to bind its hash and writes its results locally. Repository source snapshots are inert text. No external write was performed.

## 2. Domain and conventions

Let p be an odd prime, k >= 1, q = p^k, and K a field of characteristic different from p containing a root zeta of exact order q. Residue arithmetic is in R = Z/qZ. Fractions appearing in exponents, such as 1/2, are inverses in R, or in the expressly reduced ring Z/mZ. Scalars 1/q and 1/m are inverses in K. These two uses of inverse must not be conflated; the proof does not require characteristic(K) != 2.

On functions R -> K define

    F[x,y] = zeta^(xy),
    C_s[x,x] = zeta^(s x^2/2),
    D(a,c)f(x) = zeta^(c(x-a/2)) f(x-a).

The unnormalized Fourier inverse is F^-1[x,y] = q^-1 zeta^(-xy). Indeed, the sum of zeta^(tz) over z in R is q for t=0 and zero otherwise. The latter follows from the geometric-series identity and the exact order of zeta, including when t is a nonunit.

The corrected upper-shear operator is

    U_b = F^-1 C_(-b) F,
    U_b[x,y] = q^-1 sum_(z mod q) zeta^(-b z^2/2 + (y-x)z).       (1)

Values of b are interpreted modulo q. For b=0, (1) is the identity matrix.

## 3. Why the label has this sign

Direct substitution into the displacement definition gives

    C_s D(a,c) = D(a,c+sa) C_s,
    F D(a,c) = D(-c,a) F.

Thus C_s acts on the displacement column (a,c) by L(s)=[[1,0],[s,1]], and F by W=[[0,-1],[1,0]]. Ordinary 2-by-2 matrix multiplication gives

    W^-1 L(-b) W = [[1,b],[0,1]].

Consequently the corrected operator has precisely the covariance

    U_b D(a,c) = D(a+bc,c) U_b.                                 (2)

With C_b in place of C_(-b), the action would be (a-bc,c), the opposite shear. This label determination uses displacement covariance, rather than an ambiguous comparison of supports or orders. No claim about a globally normalized representation of all group elements is needed.

## 4. Support and completed square

Assume b != 0 in R. Use its representative 1 <= b < q and put

    g = gcd(b,q) = p^v,  m = q/g,  u = b/g mod m,  eta = zeta^g.

Then u is a unit modulo m and eta has exact order m. Set d=y-x. Translation z -> z+m in (1) multiplies its summand by zeta^(dm), because all other changes in its exponent are divisible by q. If g does not divide d, this multiplier is different from one, and the invariant sum must be zero in the field K.

If g divides d, write x=r+gX and y=r+gY with a common r in {0,...,g-1}. The summand has period m. Collapsing its g repetitions gives

    U_b[x,y] = m^-1 sum_(z mod m) eta^(-u z^2/2 + (Y-X)z).

Writing Delta=Y-X and shifting z by Delta/u yields

    -u z^2/2 + Delta z
       = -u (z-Delta/u)^2/2 + Delta^2/(2u)  mod m.

Therefore

    U_b[x,y] = kappa_(-u,m) eta^( (Y-X)^2/(2u) ),               (3)
    kappa_(-u,m) = m^-1 sum_(z mod m) eta^(-u z^2/2).

Both signs are fixed: the Gauss parameter is -u and the completed-square exponent is positive. The coordinates X=floor(x/g), Y=floor(y/g) are valid after, and only after, the same-residue support condition is established.

## 5. The support is exact, and the core has the claimed signed order

For a unit a modulo m define G(a)=sum_z eta^(a z^2/2). Since 2 is invertible in Z/mZ, the change of variables r=x-y, s=x+y is bijective. Hence

    G(a)G(-a)
       = sum_(x,y) eta^(a(x^2-y^2)/2)
       = sum_(r,s) eta^(a r s/2)
       = m.                                                    (4)

Orthogonality applies to the inner s-sum for every r != 0; a unit a cannot make ar/2 zero. The right side m is nonzero in K. Therefore both Gauss factors, and hence kappa_(-u,m), are nonzero. Every position admitted by g | (y-x) is nonzero, while every other position vanishes. Each row and column has exactly m nonzeros, and there are g residue blocks of size m.

Expanding (Y-X)^2 in (3) factors each block into nonzero diagonal chirps, the scalar kappa, and the core

    K[X,Y] = eta^(-u^-1 X Y).

The core is the positive Fourier matrix of order m with its column coordinate permuted by Y -> -u^-1 Y. In the local 0,1 row/column square, the cross ratio is

    U[0,0] U[1,1] / (U[0,1] U[1,0]) = eta^(-u^-1).            (5)

Its order is exactly m because -u^-1 is a unit modulo m. The sign in (5), unlike just its order, distinguishes the two shear conventions. These statements certify support and the stated block core, not a complete lower-parabolic double-coset classification or a lower bound for arbitrary evaluators.

## 6. Additive and inverse normalization are fixed within this subgroup

The exact Fourier inverse and C_(-b) C_(-c)=C_(-(b+c)) give

    U_b U_c = U_(b+c),   U_0=I,   U_b^-1=U_(-b).                (6)

Thus no extra projective scalar is present on this upper-shear subgroup. This does not certify the global normalization of all Weil operators or every mixed-word relation.

For an independent kernel form, put S_b(t)=sum_z zeta^(-b z^2/2+tz), so U_b[x,y]=S_b(y-x)/q. Expanding the convolution and using orthogonality proves

    sum_t S_b(t) S_c(d-t) = q S_(b+c)(d).

The checker tests this denominator-cleared identity by polynomial multiplication, separately from its dense Fourier conjugation controls.

Similarly, translating the Gauss-sum variable gives

    S_b(t+bc) = zeta^(ct+bc^2/2) S_b(t).                        (7)

Equation (7) is equivalent to all entries of (2): (U_b D)[x,y] uses S_b(y-x+a) times zeta^(c(y+a/2)), while (D' U_b)[x,y] uses S_b(y-x+a+bc) times zeta^(c(x-(a+bc)/2)). Setting t=y-x+a makes the two expressions equal by (7). Accordingly, the checker exhausts (b,c,t) and does not inflate its assertion count by enumerating the redundant x,a coordinates.

## 7. Explicit wrong-sign control

Take q=3, b=1 in Q(zeta), with zeta^2+zeta+1=0. Since 1/2=2 modulo 3,

    U_1[0,0] = (1+2 zeta)/3,
    (F^-1 C_1 F)[0,0] = (1+2 zeta^2)/3 = (-1-2 zeta)/3.

The difference is (2+4 zeta)/3 != 0. The correct cross ratio is zeta^2 and the positive-chirp cross ratio is zeta. Both have order three. This concretely explains why the earlier support/order-only tests could miss the labelling error. It is a counterexample to using the positive chirp for the fixed U(+1) convention, not a counterexample to (1)-(7).

## 8. Fresh exact checker and measured coverage

The file `check_cyclotomic_upper_shear.py` works in the integer quotient Z[X]/Phi_(p^k)(X), embedded in Q(zeta_q); all displayed matrix denominators are cleared before comparison. Here

    Phi_(p^k)(X) = 1 + X^(q/p) + ... + X^((p-1)q/p).

This is the cyclotomic minimal polynomial: after X -> X+1, all nonleading coefficients are divisible by p, and the constant term is p, so Eisenstein applies. Thus equality of reduced coefficient tuples is exact characteristic-zero equality; no floating tolerance or finite-field collision is used. The helper independently checks root multiplication and exact root order.

Executed command:

    python check_cyclotomic_upper_shear.py

The run passed with source SHA-256 `eb244b44de35e7855f5c9c30aa05f1749bea37ebd45052ac122237eb9afeb27c`. Machine-readable counts are in `EXACT_CHECK_RESULTS.json`; `RUN.log` records the summary.

- q = 3, 5, 7, 9, 11, 13, 25, 27: every b modulo q, totaling 100 scalar cases, including eight identities and 92 nonzero b.
- 1,808 direct circulant kernel numerators. They determine 40,060 matrix entries, but the latter number is explicitly implied coverage, not 40,060 separately evaluated direct matrix entries.
- 1,708 completed-square equalities and 1,708 exact support comparisons for nonzero b; 92 Gauss products, 92 Gauss nonvanishing tests, 92 signed cross ratios, and 92 exact residual-order tests (each with divisibility and strict-order assertions).
- 40,060 actual reduced Weyl equalities, covering every b,c,t for the listed q and hence all corresponding displacement entries by the reduction in section 6.
- 6,004 actual additive-convolution equalities: every b,c,d at q=3,5,7,9; for q=11,13,25,27, every b,d with c in {0,1,-b}, deduplicated.
- At q=3,5,7,9 only, 164 dense Fourier-inverse entry checks and 1,224 dense Fourier-conjugation entry checks, using explicit matrix entries and exact polynomial products.
- 500 noncanonical-integer-b equalities across five representative integers for each q.
- All 92 distinct nonzero-b positive-chirp controls were rejected as different operators.
- Total actual assertions: 54,028, including arithmetic controls and row-count/identity checks.

The list deliberately overlaps earlier finite-field controls but differs in arithmetic model and additionally tests additive composition. It adds q=11,13 and does not include q=49, which the prior review did cover. Neither its smaller finite domain nor its larger integer assertions can be presented as a full implementation replay. The uniform conclusions rest on the proof, not extrapolation from the finite list.

## 9. Gate disposition and next executable obligation

Accept only: an independently derived, domain-qualified negative-chirp identity, exact support and signed core, Weyl label, additive normalization on the upper-shear subgroup, and the stated fresh characteristic-zero controls.

Do not accept from this packet:

1. Any execution acceptance for the candidate hash or the 13 derivative tests. None were run. Formula equality does not establish a program's dispatch, parameter handling, implementation branches, or emitted records.
2. Any historical exhaustive SL2/subgroup, double-coset-refinement, valuation-count, operation-ledger, or predecessor-hash test replay. Static retention reported by the prior review is not execution evidence.
3. Recovery or replay of the original earlier bounded API/review bytes. The static report records a readable sanitized publication derivative, which remains distinct from the unrecovered original byte identities.
4. Malformed-input validation, p=2, global representation normalization, higher-dimensional congruence diagonalization, numerical production, preparation/bit costs, practical speed, novelty, or a faster general FFT.

The next implementation-level gate is an authorized run of the exact pinned corrected package and all 13 test groups, recording package/module hashes, actual commands, exit status, complete new logs and per-test results, without reusing the preserved historical output. If the historical exhaustive obligation is pursued, its exact source, sign convention, expected verdicts and scope must be separately pinned and run. The permission and execution boundary of this task forbids those runs; this report makes no request or presumption that they occurred.

Recommended record wording:

> The negative-chirp source repair remains statically accepted. A fresh characteristic-zero cyclotomic formula checker passes 54,028 assertions on all 100 b values for q=3,5,7,9,11,13,25,27, with a uniform proof of the corrected kernel, exact support, signed core, Weyl covariance and additive shear normalization. Candidate tests and historical exhaustive suites remain unrun; implementation acceptance and broader scope remain open.
