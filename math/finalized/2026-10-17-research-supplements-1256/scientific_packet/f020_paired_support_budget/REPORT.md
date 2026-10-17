# F020: exact remaining characteristic-two gates

17 October 2026 UTC. Read-only source reconciliation and bounded analytical follow-through.

## Result

**The full paired-support gate remains OPEN58. Its endpoint-only subgate remains OPEN53.** The new accepted ordinary-discriminant results do not prove either characteristic-two assertion.

The exact unresolved object is the reciprocal common support of the actual Rogers–Szegő obstruction polynomial `Q_m=E_m R_m`, uniformly for every integer `m>=1`. The endpoint question uses only `E_m`. Their accepted reductions, source identities and completed endpoint lines are available; the blocker is a missing uniform nonvanishing argument, not missing source access.

This report adds two elementary, proved consequences of the inspected exact sources:

1. A paired-obstruction degree/order budget after the accepted deflation. This gives the correct necessary search conditions for an inverse pair and distinguishes them from the whole-cyclotomic cutoff.
2. Squarefreeness of the high-order part of the accepted affine endpoint obstruction, by an exact derivative identity.

These are search/verification corollaries. They neither establish a new actual-family support range nor change either status or priority. No new growing-index census, historical-program execution, external write, or historical-novelty claim is included. Fresh exact controls pass; the new corollaries have not received a separate independent review.

## 1. Definitions and exact statement of OPEN58

All polynomials in this section are over `F2`. Start from the actual integral Gaussian family reduced modulo two:

    H_(2m+1)(z;q) = (z+1) U_m(z;q),
    U_m(z;q) = z^m P_m(z+z^-1;q),
    P_0=1, P_1=X+q+q^2,
    P_j=(X+a_j)P_(j-1)+c_j P_(j-2),
    a_j=q^(2j-1)(1+q),
    c_j=(1+q^(2j-1))(1+q^(2j-2)), j>=2.

Use the unique even/odd spectral split

    P_m(X;q)=A_old(X^2;q)+X B_old(X^2;q),
    E_m=P_m(0;q),
    R_m=Res_Y(A_old(Y;q),B_old(Y;q)),
    Q_m=E_m R_m.

The accepted degree theorem is

    N_m=deg Q_m=m(m+1)(2m+1)/3,
    Q_m*=q^N_m Q_m(q^-1),
    L_(2m+1)=product_(j=0)^m (1+q^(2j+1)).

The exponent in the reversal is the actual degree of `Q_m`. The reversed polynomial itself has degree `N_m-ceil(m/2)` because `Q_m` has that nonzero q-content. Padding either reversal would change the problem.

**Full gate.** For every `m>=1`, prove

    (Q_m,Q_m*)=(1) in F2[q,1/L_(2m+1)].                 (G58)

Equivalent exact completion forms are:

- Polynomials `a_m,c_m` with `a_m Q_m+c_m Q_m*=L_(2m+1)^N_m`, uniformly in `m`.
- No `alpha` of exact odd order `d>2m+1` for which both `Q_m(alpha)` and `Q_m(alpha^-1)` vanish.
- Refutation by one actual-family common irreducible factor, with both divisibilities and an exact root order exceeding `2m+1` certified.

The roots of `L_(2m+1)` are exactly the nonzero parameters of odd order at most `2m+1`; repeated factors in `L` cause no support ambiguity. There is no lost q=0 component because `Q_m*(0)=1`.

The four channels are

    E(alpha)=E(alpha^-1)=0,
    E(alpha)=R(alpha^-1)=0,
    R(alpha)=E(alpha^-1)=0,
    R(alpha)=R(alpha^-1)=0.

Endpoint/collision and collision/endpoint are exchanged by inversion, but both orientations must be respected in a certificate. A self-reciprocal irreducible factor and a complete pair of distinct reciprocal irreducible factors both obstruct (G58). An isolated factor in a split inverse pair does not.

Why the endpoint belongs in `Q`: `Disc_X(P_m)=R_m^2`, while `z -> z+z^-1` is ramified at `z=1`, with trace value zero. Consequently `U_m` is squarefree exactly when `E_m R_m` is nonzero. The collision roots at the two parameter orientations may have different spectral coordinates.

Source: [exact reciprocal descent, Sections 1–5 and 7](https://github.com/AgentSlop-Si/research/blob/a462b0f54fc0e05da1fe689b7d1de665bd147944/math/finalized/2026-10-16-finalization-round/reports/f020/sources/RECIPROCAL_DESCENT.md).

## 2. The accepted smaller certificate, and what is still missing

Set

    v=ceil(m/2), d0=N_m-v, epsilon=d0 mod 2,
    V=(q+1)^epsilon q^-v Q_m, 2s=d0+epsilon,
    T=q+q^-1,
    q^-s V=A_m(T)+q B_m(T).

Here `A_m` is monic of degree `s`; either `B_m=0` or `deg B_m<=s-2`. These parameter coefficients are different from `A_old,B_old`, the spectral split. Define

    J_(2r+1)(T)=q^-r(1+q+...+q^(2r)),
    Dcal_m(T)=T product_(r=1)^m J_(2r+1)(T).

The accepted exact equivalence is

    (G58) iff (A_m,B_m)=(1) in F2[T,1/Dcal_m].

Thus the missing statement can be written

    gcd(A_m,B_m) divides Dcal_m^s,

or `a_m A_m+c_m B_m=Dcal_m^s`. The exponent `s-2` is available when `B_m` is nonzero, but does not cover the `m=1, B_m=0` boundary. At that boundary `A_1=T`, `Q_1=q(q+1)` and all support is allowed.

The unramified lift of a trace factor `h(T)` of degree `r` is `q^r h(q+q^-1)`. It is either one self-reciprocal irreducible of degree `2r`, or two distinct reciprocal irreducibles of degree `r` each. The `T=0/q=1` branch has its separate accepted multiplicity correction and is inverted in the desired statement.

**Nothing in free quadratic descent, the degree gap, or a vanishing quadratic norm proves the missing gcd support assertion.** The all-m coefficient-pair construction is already complete and should not be counted again as progress toward its conclusion.

## 3. Exact statement of OPEN53 and accepted coverage

The endpoint recurrence and actual reversal are

    E_0=1,
    D_j(q)=product_(r=1)^j(1+q^(2r-1)),
    C_j(q)=product_(r=1)^j(1+q^(2r)),
    E_j=D_j+(1+q^(2j))E_(j-1),
    deg E_j=j(j+1),
    E_j*=q^[j(j+1)]E_j(q^-1).

The endpoint gate is

    (E_m,E_m*)=(1) in F2[q,1/L_(2m+1)] for every m>=1. (G53)

It is precisely the first of the four channels, not another name for (G58).

Accepted endpoint exclusion covers all `m>=1` on the exact-order lines

    d=4m+3,
    d=2m+3, 2m+5, 2m+7.

Composite orders and every primitive Frobenius component are included. The accepted results are stronger than a test at a selected embedding, but do not cover arbitrary `d>2m+1`.

The mechanism is the complementary identity at exact odd order `d=2h+1`, with `m+n=h-1`:

    C_h C_n E_m+D_h C_m E_n*=C_m C_n.

All products are units at that parameter. Further, `D_h^8=alpha` and `C_h^8=alpha^-1`. Put

    F_n=E_n^8+q C_n^8,
    G_n=q(E_n*)^8+C_n^8.

Then at `alpha` the exact cleared transport is

    C_m^8 F_n=alpha^2 C_n^8(E_m*)^8,
    alpha C_m^8 G_n=C_n^8 E_m^8.

Hence (G53) is equivalent to

    support(gcd(F_n,G_n)) subset support(L_(2n+1))
    for every n>=0.                                      (AE)

This is an already accepted equivalence, not an easier theorem that has been proved. Its safe polynomial certificate has right side `L_(2n+1)^[8n(n+1)+1]`. The three accepted cases `n=0,1,2` produce the three off-line families. A complementary index smaller than `m` prescribes a nonzero affine endpoint value; it does not produce a smaller paired-zero instance, so it cannot support the tempting induction.

Sources: [complementary theorem](https://github.com/AgentSlop-Si/research/blob/a462b0f54fc0e05da1fe689b7d1de665bd147944/math/finalized/2026-10-16-finalization-round/reports/f020/sources/COMPLEMENTARY_THEOREM.md), [affine transport](https://github.com/AgentSlop-Si/research/blob/a462b0f54fc0e05da1fe689b7d1de665bd147944/math/finalized/2026-10-16-finalization-round/reports/f020/sources/ENDPOINT_TRANSPORT.md), and [independent endpoint acceptance](https://github.com/AgentSlop-Si/research/blob/a462b0f54fc0e05da1fe689b7d1de665bd147944/math/finalized/2026-10-16-finalization-round/reports/f020/sources/ENDPOINT_REVIEW.md).

## 4. Dependencies and separation from the new characteristic-zero results

The proof dependencies are:

1. Actual Gaussian family and the displayed trace recurrence.
2. Spectral split/resultant identity, exact q-content, and actual reversal degree.
3. Low-order localization and both inverse-orbit types.
4. Faithfully flat quadratic coefficient descent, including the ramified boundary.
5. For the endpoint route, the exact product-unit guards and complementary affine transport.

The accepted ramified and low-order deflations are useful extra arithmetic, not missing premises of (G58). They remove known low-order factors and give a whole-cyclotomic degree filter. They have not supplied a high-order inverse-pair exclusion.

The separate 17 October accepted packet establishes ordinary-discriminant valuations at odd primes, odd prime powers in the residual range `b<p`, and the original all-odd-order/all-odd-residual all-A overlap simplicity statement. Its bounded successor fills the static residual range at root orders 9 and 25 and derives the corresponding all-A local consequences. Those results remain accepted at their own scopes. **Do not reopen the now-completed all-odd overlap problem merely because older source reports call it a separate open guard.**

Those characteristic-zero statements do not imply (G53) or (G58). Conversely a modular paired counterexample would not automatically disprove ordinary characteristic-zero squarefreeness. The logical sufficient implication runs in the other direction:

    characteristic-zero residual discriminant vanishes at primitive order d
      => Phi_d divides the integral discriminant polynomial
      => reduced Phi_d divides Q_m
      => a high-order reciprocal common factor exists modulo two.

The middle step uses `Disc(U_m) mod 2=E_m^2 R_m^4` and separability of the reduced odd-order cyclotomic polynomial. A proper reciprocal subset can vanish without the whole reduced `Phi_d` dividing `Q_m`. Modular vanishing also need not lift to characteristic zero.

The bounded residual report and its independent review are bound in `LOCAL_INPUT_BINDINGS.json`. The broader ordinary-discriminant acceptance was also read at its exact scientific scope. This reconciliation does not redo those independent proofs or claim a general characteristic-zero composite-order static theorem.

## 5. Bounded analytical corollary: the correct paired search budget

This section is an elementary consequence of the accepted deflation and inverse-orbit classification. It is not a new uniform support theorem.

### 5.1 Full obstruction

Retain the accepted definitions

    N=m(m+1)(2m+1)/3, v=ceil(m/2),
    kappa=m+3 floor(m^2/4)+2 floor(m/4),
    e_d=((d+1)/2) floor(m/d)+floor(floor(m/d)/2),
    Delta_m=sum_(odd 3<=d<=m) phi(d)e_d,
    Cfull_m=N-v-kappa-Delta_m.

The nonzero integral quotient

    Qhat_m=Q_m/[q^v(q+1)^kappa product_(odd 3<=d<=m) Phi_bar_d^e_d]

has degree `Cfull_m`. Every removed factor has zero parameter or exact order at most `m`, so it is a unit at every candidate order `d>2m+1`.

Suppose a high-order paired obstruction exists and let `h(T)` be the irreducible polynomial of the trace `alpha+alpha^-1`, of degree `r`. Both inverse parameter components occur in `Q_m`, so the entire degree-`2r` lift `q^r h(q+q^-1)` divides `Qhat_m`. Therefore

    1<=r<=floor(Cfull_m/2).                              (B1)

The exact order must additionally satisfy one of:

- Split inverse pair: `ord_d(2)=r`, `-1` is not in the subgroup generated by 2 modulo d, and `d | 2^r-1`.
- Self-reciprocal component: `ord_d(2)=2r`, `2^r=-1 mod d`, and `d | 2^r+1`.

**Proof.** In the split case the root and its trace generate the same finite field `F_(2^r)`; its nonzero multiplicative group has order `2^r-1`. In the self-reciprocal case the root field is the quadratic extension of the trace field, and inversion is its nontrivial involution, so `alpha^(2^r)=alpha^-1`. Exact minimal degrees give the displayed multiplicative-order conditions. The degree inequality follows from the full lift divisibility, not from counting a single one-sided factor. QED.

In particular any paired counterexample has

    2m+1<d<=2^floor(Cfull_m/2)+1.                        (B2)

The order divisibilities in (B1) are more useful than the coarse upper bound (B2). They are necessary conditions only; they do not supply any actual common factor. The exact orbit conditions cannot be replaced by an assumption that inversion is always Frobenius.

The published cutoff `d<=Cfull_m^2` belongs to the different question of **whole** `Phi_bar_d` divisibility, where `phi(d)<=Cfull_m` is necessary. It does not provide a justified paired-support cutoff. A complete small negative control to the inference from residual degree alone is

    f=q^9+q^4+1,
    f*=q^9+q^5+1,
    V=f f*.

The polynomial `f` is irreducible with exact root order 511, and `f!=f*`. Thus `V` is reciprocal of degree 18 and has a paired order-511 zero, even though `511>18^2`. Fresh checks certify irreducibility by the degree-nine Rabin test and order by `511=7*73`, testing both proper prime-divisor powers. **This is a synthetic logical control, not an actual Rogers–Szegő counterexample; its degree 18 is not asserted to be an actual `Cfull_m` instance.** It disproves the proposed inference from residual degree alone. It does not disprove a separately established actual-family order bound, but no such `Cfull_m^2` paired-support bound is supplied by the inspected sources.

### 5.2 Endpoint-only budget

The accepted endpoint valuations give the genuine quotient

    Ehat_m=E_m/[q^(m mod 2)(q+1)^m
               product_(odd 3<=d<=m) Phi_bar_d^floor(m/d)].

Its degree is

    Bend_m=m^2-(m mod 2)
           -sum_(odd 3<=d<=m) phi(d)floor(m/d).            (B3)

The same full-lift argument proves that any high-order paired endpoint zero has `r<=floor(Bend_m/2)` and the same split/self-reciprocal order conditions. This is an endpoint-specific necessary search budget for (G53), often smaller than the full budget; the budgets agree at m=1 and m=2. Divisors of `2^r-1` or `2^r+1` are only a candidate superset until the exact trace-degree and orbit conditions are checked.

At the already studied controls `m=1,2,3,4,12`, the full budgets are `0,4,13,36,1006`, while endpoint budgets are `0,4,6,14,106`. These are degree calculations only, not new support certifications.

The known `m=2` example checks the essential qualifier: `E_2=(q+1)^2(q^4+q^3+1)` has a one-sided order-15 endpoint zero; its reciprocal endpoint has the other degree-four factor. Their high factors are coprime. The paired degree budget is four, whereas a whole distinct inverse pair would require eight. The budget does not incorrectly prohibit that known one-sided zero.

Sources: [accepted ramified deflation](https://github.com/AgentSlop-Si/research/blob/22e4fbdff0dd655d4cac7408964142fd2476686d/math/finalized/2026-10-16-mathematical-development-1221/f020/REPORT.md), [accepted low-order deflation](https://github.com/AgentSlop-Si/research/blob/a462b0f54fc0e05da1fe689b7d1de665bd147944/math/finalized/2026-10-16-research-finalization-1722/f020/REPORT.md), and the reciprocal-descent source in Section 1.

## 6. Bounded analytical corollary: affine high-order roots are simple

For the exact endpoint pair in Section 3, direct differentiation over `F2` gives

    F_n'=C_n^8,
    G_n'=(E_n*)^8,
    G_n=q^[8n(n+1)+1] F_n(q^-1).                        (B4)

The derivative identities follow because every eighth power has zero derivative. The reversal identity uses `deg E_n=deg C_n=n(n+1)` and reciprocity of `C_n`.

If `alpha` has exact odd order `d>2n+1`, then `C_n(alpha)!=0`: all its exponents lie between 2 and `2n`, and none is divisible by `d`. Thus every such root of `F_n` is simple. At a common root, `G_n=0` also gives `(E_n*)^8=alpha^-1 C_n^8!=0`, so it is a simple root of both members.

Consequently the high-order part of `gcd(F_n,G_n)` is squarefree. A putative affine endpoint counterexample needs a simple common irreducible factor, not a hidden multiplicity argument. This does not make its support empty. In particular it does not justify propagating the three accepted `n=0,1,2` certificates to all n.

Fresh controls reconstruct only those existing three symbolic cases and check both derivatives and the exact reversal, without executing any supplied code. The proof, not the controls, supplies the all-n derivative statement.

## 7. Smallest decisive next step, and how to stop safely

### A. Smallest uniform theorem target

The smallest existing gate whose proof would make a genuine structural advance is (G53), equivalently the already accepted all-n assertion (AE). A useful next lemma must provide a **uniform actual-family reason** why the high-order simple common factors of `F_n,G_n` are absent, or an all-m endpoint Bezout certificate. Re-deriving (AE), extending its three small cases one index at a time, or asserting an induction from complementary affine values does not supply that reason.

An endpoint proof closes only endpoint/endpoint. To close (G58), one still needs an actual-RS-specific invariant controlling inverse endpoint/collision and collision/collision failures, including different collision coordinates. No such invariant is established in the inspected source or this report.

### B. Smallest decisive counterexample certificate

A factor-first search is the appropriate conditional alternative to a new proof idea. Do not enumerate all orders up to the unrelated `Cfull_m^2` bound. For a specifically justified actual index or analytically proposed factor:

1. Reconstruct the actual recurrence independently. Compute the appropriate common gcd, either `gcd(Q_m,Q_m*)`, the accepted coefficient gcd `gcd(A_m,B_m)`, or the endpoint-only pair.
2. Saturate by the allowed low-order support. If it becomes 1, this is only a bounded checked case, not all-m completion.
3. For a surviving trace irreducible `h` of exact degree r, verify the full degree-`2r` lift and its split/self-reciprocal type. Apply (B1) or (B3) as necessary checks, not acceptance by themselves.
4. Certify an exact odd order d: prove `alpha^d=1` and `alpha^(d/p)!=1` for every prime p dividing d, in a verified irreducible quotient field. Require `d>2m+1`.
5. Verify both parameter orientations with an independent Gaussian reconstruction and label the actual endpoint/collision channels. For a collision give an exact spectral gcd/root certificate; allow different coordinates at inverse parameters.
6. Bind the factor, source normalization, exact divisions, order proof and independent readback. One successful actual-family witness refutes the relevant universal gate. An isolated one-sided factor does not.

There is currently no analytically proposed surviving actual-family factor in this packet. Accordingly no new index or larger census is selected. The correct stopping condition here is the exact remaining mathematical statement plus the admissible witness contract and proved search guards.

### C. Routes already known not to complete the gate

- The actual `m=2`, order-15 one-sided endpoint failure is not paired.
- The actual `m=12`, order-31775 one-sided ordinary collision leaves the inverse parameter good. It refutes one-sided kernel noncancellation, not (G58).
- The actual order-1285 arbitrary-spectral-coordinate q-shift witness has nonzero distinguished endpoints and does not refute (G53).
- A self-reciprocal collision at order 17 for `m=12` is inside the allowed range `17<=25`.
- Exact full-chain reflection, unit edges and simple full spectrum cannot exclude different repeated-root coordinates. The accepted synthetic length-five model already disproves that structural implication.
- A norm zero is not a common coefficient factor. A full-cyclotomic nondivisibility result does not exclude a proper reciprocal subset.

The witness provenance and exact scope are recorded in the [collision-kernel source](https://github.com/AgentSlop-Si/research/blob/a462b0f54fc0e05da1fe689b7d1de665bd147944/math/finalized/2026-10-16-finalization-round/reports/f020/sources/COLLISION_KERNEL.md) and the accepted endpoint/complementary sources above. These inherited witnesses were read as evidence; their historical programs were not run.

## 8. Deliverable and evidence limits

`SOURCE_BINDINGS.json` binds the immutable mathematical source bodies. `LOCAL_INPUT_BINDINGS.json` binds only the bounded residual scientific report and review. `CONTROLS.json` is generated by the freshly written standard-library checker `check_gate_corollaries.py`. `SUMMARY.json` states exactly what is proved and what remains open.

The source reconstruction and logical separation are complete for this task. The elementary corollaries are author-proved and fresh-control checked, not independently accepted or historically novel. No actual-family paired counterexample or full-gate proof was found. No source program was executed and no canonical record or external file was changed.
