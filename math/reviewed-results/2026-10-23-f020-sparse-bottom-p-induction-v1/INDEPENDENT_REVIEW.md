# Independent review: arbitrary separated even-middle digits, terminal p

23 October 2026. **SCOPED PASS. No mathematical repair requested.** The proof is a genuine all-finite-length extension, not a finite-slice or central-disk extrapolation.

## Exact accepted scope and dependency boundary

Bind the frozen report SHA-256 `3b5440a464304e0e08690363f9e1d76878975c7ea4159825cb78f6b398835970` and manifest `71a2d32fc860c7f8e236d831b72b7c8a66a637be78de163076fe8f817a3135e0` in `sparse_bottom_author`.

Accept, for every finite t>=0,

    n=2p^r + sum_(a=1)^t c_a p^(k_a) + dp,

where p is odd prime, c_a are even with 2<=c_a<p, d is odd with 1<=d<p, all consecutive exponents in r,k_1,...,k_t,1 differ by at least two, and s>r. The original P_n and H_n are squarefree at every characteristic-zero primitive p^s phase. At every original P_n root, its original ordinary derivative, original consecutive neighbor and original algebraic-square Christoffel-Darboux kernel are nonzero.

Incremental credit is **only t>=2 after subtraction of every previously successful high-order, fixed-degree and residual certificate**. The t=0 window and accepted t=1 bottom-p theorem retain their prior credit. The minimum new shape is 4917, not a certification that every phase order at that degree was previously unresolved. The exact inherited high-order C_u formula and exclusion test remain unchanged. The terminal-j>=2 family is distinct. No adjacent gap, terminal zero, odd middle digit, even terminal digit, altered leading digit, non-prime-power phase, owner closure, novelty, algorithmic complexity, FFT or stability conclusion is accepted.

The selected prior contracts were checked at their actual scope: arbitrary-even-prefix covers/bounds/outside ratios from the accepted sparse proof, the universal finite shifted identity and terminal-p deep cap/outer cap from the accepted bottom-p proof, and their independent reviews. Neither a one-middle squarefreeness conclusion nor a simple-prefix hypothesis is used as a substitute for the new many-digit lemmas.

## 1. Length-independent balance and legal indices

For every remaining suffix m, u=(m-1)/2 has all base-p digits at most h=(p-1)/2, units digit h, and p-digit (d-1)/2<h. This description includes every remaining even digit and is preserved by removing the largest one. Hence doubling u is carry-free, W(m-1)=2W(u), W(m)=2W(u)+p, and u mod p^b is at most (p^b-1)/2, strictly below it for b>1.

For x+(u-x)=u, if V(2x+1)=p^b with b>1, the residue x mod p^a=(p^a-1)/2 exceeds u mod p^a for every 2<=a<=b. The W carry defect is at least p^b-p. For b<=1 ordinary superadditivity suffices. This proves

    W(x)+W(u-x)+V(2x+1)<=G+p, G=W(u),

with no bound on the number of upper digits. The geometric digit bound gives n<[2+1/(p+1)]p^r<p^(r+1)<=p^s; all recurrence and factorial indices remain legal. Every prefix has V(U)=its terminal scale D, every remaining tail has indices of value at most its largest scale M, and D>=p^2 M.

## 2. The ordinary derivative endpoint, including the full lower equality set

On a full deep disk, the odd delta=2b+1 score is bounded by W(u-b)+V(2b+1). If b<h its value is at most G+1; if b>h the carry lemma and W(b)>=h+1 make it at most G+h. At b=h, subtracting the units half-digit is carry-free and the score is exactly G+h+1. Even delta has score at most G. Strictness of the deep Newton cap eliminates every nonzero Newton index at this maximum. Thus the unique least ordinary derivative term is Newton index zero, delta=p, and a=(m-p)/2, of weight G+h with nonzero constant initial.

For a full lower level-k disk, the half-W inequality gives score at most W(m-delta)/2+V(delta). If ord_p(delta)>=2, adding m-delta to delta-1 gives m-1 and forces carries across every level 2 through ord_p(delta). This uses the deficient p-digit of m-1, not a false deficiency at its units digit. Subtracting that defect improves the bound to the report's equation (5.5). Its bracket is p(3-p) at order two and decreases thereafter, strictly below the delta=p maximum. Order-zero indices are lower, and among order-one indices only delta=p can attain the maximum.

At delta=p, half-W equality forces the Newton index to be bM. Parity makes b even, with 0<=b<=c for m=cM+a0. Every listed term has

    a=(c-b)M/2+(a0-p)/2.

The full remaining a0 is retained. Its half after subtracting p has units digit zero and all other digits at most h, so the required addition and doubling are carry-free. Conversely the equality conditions leave no other term. This is the substantive all-length extension of the one-middle argument.

The actual normalized w/Q block units are c!, b! and 2^v v!, since all block counts are below p. Their sum is exactly M_c(Z), times the stated nonzero suffix scalar w_(a0)/Q_((a0-p)/2). That scalar has not been replaced by a one-digit approximation. Since c is even and c<p, M_c(0)!=0. At the terminal lower scale the arbitrary-prefix level-one argument supplies M_(d-1), also with nonzero constant. Therefore derivative exactness holds on **strict** lower interiors, not indiscriminately on lower boundaries.

The off-root H/P chain term is higher: on full lower disks P_m has weight at least W(m)/2=G+p/2 and v(m)=E_p, giving E_p+G+p/2>G+h. On deep disks the stronger P_m>=G+p applies. This is ordinary characteristic-zero differentiation before reduction, not differentiation of a Hermite residual or a q-derivative.

## 3. Actual shifted g' and the four-parity lemma

The universal finite shifted identity in Section 6 is the same exact original-continuant identity already independently checked in the bottom-p review. Its cancellation of the (1-q^delta) denominator is algebraic, and the actual U+a and U+b denominators remain. Since V(U)=D>M, their weights are V(a),V(b), and the prefactor has weight W(m). The Chebyshev factor is integral and nonnegative near X=0. Thus the entire new obligation is the stated endpoint score inequality, not a transfer from an unshifted derivative.

Let x=floor((a-1)/2), y=floor((m-b)/2), z=u-y. I independently checked all four cases:

- Even a, odd b: absorb V(a) by W(x+1)<=W(z), then apply the odd-endpoint carry lemma at z.
- Both even: x+1<=z-1 absorbs both endpoint values inside W(z), leaving the stronger bound G.
- Both odd: z-x is a positive multiple of min(V(a),V(b)). The corresponding W interval absorbs the smaller endpoint value, and the carry lemma handles the other.
- Odd a, even b: when z-x>=B=V(b), the complementary interval absorbs B. Otherwise reflection about the multiple z gives W(z)-W(x)=B+W(z-x-1). Away from 2(z-x)-1=B the elementary score V(2v+1)-W(v)<=p suffices. In the exception with A=V(a)>B, each power C with B<C<=A has z mod C=(C+B)/2>u mod C, so z+y=u has carry defect at least A-B. The remaining score is at most G+B-W((B-1)/2)<=G+p.

The final residue comparison needs only u mod C<=(C-1)/2. It therefore covers B=1,C=p, where the units half-digit is full. No nonexistent strict deficit at that bottom level is assumed. The elementary endpoint bound holds at arbitrary order: its maximum p is attained at the minimal order-two endpoint, and order>=3 gives no larger score.

Together with W(m)=2G+p, this proves **actual shifted g'>=G on every full deep disk**, uniformly in phase and suffix length. The proof does not assume the false globally stronger separate core-neighbor derivatives found in the stopped adjacent route.

## 4. Deep g unit, actual shift errors and noncentral disks

For odd unshifted g connection indices, both P factors are even. The carry lemma bounds their score by G+p, and every weight-G contribution has a constant deep-disk initial. Even indices begin at G+p. The nonzero complete leading constant is fixed by g_m^0(0)=(-1)^u Q_u of weight G.

This is not central-to-noncentral extrapolation: the deep cap leaves only Newton index zero for each even factor, and the H/P unit factor has the same residue at all matching centers (q powers reduce to one and v0 reduces to i). Thus the normalized leading constant is the same one identified by evaluation at zero. No full-lower g-unit assertion is made.

The finite connections give eta_initial=1 and v(eta-1)>=D-M. Independently pricing each term gives the deep corrections Delta_f>=G+p+D-M, Delta_f'>=G+D-M and Delta_g>=G+p+D-2M. On full lower disks the half-W estimate instead gives Delta_f>=G+p/2+D-M and Delta_g>=G+p+D-2M; Gauss differentiation subtracts the lower radius sigma. The derivative correction exceeds G+h by D-M-sigma+1/2>0. All these margins follow from D>=p^2 M, sigma<M/p and p<=M and do not deteriorate with the number of digits.

The actual full-lower g bound is only G+p-M, with derivative at least G+p-M-sigma. Preserving this weaker bound is essential; one may not reuse the deep unit on those larger disks.

## 5. Arbitrary-prefix outer disk and core geometry

The level-one radius rho_1=1-1/(2p) is genuinely separate from the higher-scale formulas. Every q-center is strictly inside it, so each Newton product has initial (z+1)^v. For arbitrary b=Qp with nonzero terminal digit e, the quotient/remainder formulas for R_1(b)-R_1(b-x), together with W superadditivity, give the stated block inequality without restricting the upper prefix.

For root terms, a nonzero remainder a mod p gives a strictly positive small-block remainder. Equality is exactly a=up with 0<=2u<=e. For derivative terms a nonzero delta mod p is strictly above the minimum; if delta=lp the l-dependent expression pW(l-1)-l/2 is -1/2 only at l=1. The full equality set is therefore delta=p, a=up, and Newton index b0+(e-1-2u)p. Summing the genuine block units yields Y^b0 M_e and Y^b0 M_(e-1), respectively, not a differentiated inseparable residual. The chain correction is strictly higher.

The root initial has full degree b and unit leading coefficient, giving a complete monic cover. For b=n and odd e=d, the (d-1)p outer-boundary roots are simple because M_d and M_(d-1) are coprime. All other roots lie in the strict outer interior. For b=dp the derivative weight is exactly G+h with nonzero strict-interior constant. No one-middle restriction enters this argument.

Every even prefix uses the accepted arbitrary-prefix full-disk bounds C>=J, C'>=J+D/2-p, B>=J-D/2 and **ordinary original B'>=J-D/2**, plus its M_e/M_(e-1) boundary residuals and complete cover with multiplicities. These inputs do not assert prefix simplicity. Outside the cover, the monic product and coefficientwise analytic bounds give the three quoted ratios. Tied nearest centers are retained, and the outside argument remains in the near-X=0 region, including tau<1 in the bottom annulus.

## 6. Strict derivative domination and exhaustive finite-length induction

On a core boundary where M_e vanishes, B and deep g are units at their exact weights. The root equation forces f and C nonzero. Writing delta=v(f)-G>=p and gamma=v(C)-J gives delta+gamma=D/2. The exact f'C term has strictly lower valuation than the other three derivative terms, with gaps 2delta-p-h, delta-h, delta-h, each at least h+1.

Where M_e is nonzero, C is exact J and direct bounds leave gaps at least D/2-h. This argument does not divide by f or B and includes their simultaneous zero. In strict deepest r interiors, the leading-two core has constant nonzero residual and the same direct comparison applies.

In every annulus, C alone is an analytic unit. Using the weak full-lower g bounds, strict-lower f' exactness and the three outside ratios gives the displayed gaps

    D/2-M+h+1+rho-2tau,
    D/2-M+h+1+rho-tau-sigma,
    D/2-M+h+1-tau.

They are positive throughout sigma<tau<rho because M+rho<D/2. No division by g or lower-disk unit assertion is hidden here.

Strictly nested level disks partition all remaining outer-interior roots into exactly one boundary or annulus at a listed scale, or a strict deepest r interior. Adding a middle digit inserts one boundary and one annulus; the balanced suffix and unrestricted even-prefix contracts regenerate the same bounds. Thus the argument covers every finite number of digits, rather than merely the checked lengths.

Every recurrence edge below n is nonzero, so common roots of P_n and original P_(n-1) would propagate to P_0=1. The original ordinary algebraic-square CD identity then gives kernel nonvanishing. Monic reduction P_n=X^n places its roots near zero, away from +/-2; the unit H/P coordinates preserve multiplicity. H_n(0)=1 and the original identity cover all H roots. Algebraic p-adic embedding and Galois conjugacy transfer the result to every characteristic-zero primitive p^s phase.

## 7. Independent controls, pins and limits

`fresh_controls.py` is newly written reviewer code using only standard-library exact integer/rational arithmetic. It imports or runs no author or historical program. It checks seven genuine multi-middle suffixes, from 543 through 398,577, including two through five middle digits and p=3,5,7. Every endpoint pair is covered by an exact separated prefix maximum, independently explained in the code; all 147,153 pairs for the two-middle m=543 fixture are additionally checked unpruned. The compressed derivative maximization keeps every Newton index and the smallest delta of each allowed parity and p-adic order; larger deltas in the same class strictly reduce W(a). Unpruned full derivative loops cross-check that reduction at m=543.

Normal and Python -O runs are byte-identical: **1,696,089 active checks**. Coverage includes the complete lower and deep ordinary derivative equality sets, exact leading factorial units retaining the entire suffix, 117,393 exceptional endpoint carries, their bottom B=1 cases, arbitrary-prefix outer root/derivative equality sets including degree 4917, all-length boundary/annulus/shift margins through thirty middle digits, and the explicit odd-middle countercontrol. The universal shifted identity's earlier independent rational controls are retained as a dependency and are not falsely claimed as newly rerun here. No finite controls are used as a proof of the unbounded theorem.

All 40 frozen manifest members and 33 selected source copies were independently hash/length checked, including byte equality to their source paths. This is a selected source-contract review, not a broad repository or recursive historical audit.

**Disposition:** accept the exact unbounded separated-even-middle terminal-p theorem with incremental t>=2 credit only and all inherited exclusions. Preserve both prior accepted families and every explicit remaining F020/F023 obligation.
