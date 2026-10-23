# F020: arbitrary-length separated even-middle digits with bottom p

23 October 2026 UTC. New mathematical candidate, not independently accepted by this packet. No external writes, changes to accepted packets, or historical/author scientific-code execution. This work does not delay or replace the two already accepted F020 families.

## 1. Statement, genuinely new scope, and prior credit

Let p be an odd prime, t>=0 any finite integer, and

    e_0=r > e_1=k_1 > ... > e_t=k_t > e_(t+1)=1,
    e_i-e_(i+1)>=2 for every i,
    c_a even with 2<=c_a<p, d odd with 1<=d<p, s>r,
    n=2p^r+sum_(a=1)^t c_a p^(k_a)+dp.

For t=0 the gap condition means r>=3. For t>=1 the lowest middle exponent is at least three. For every characteristic-zero primitive p^s-th root q, the ORIGINAL polynomials

    P_0=1, P_1=X, P_(b+1)=X P_b-(1-q^b)P_(b-1),
    H_b(z)=sum_a [b choose a]_q z^a

are squarefree at b=n. At every original P_n root xi, the ORIGINAL algebraic-square kernel is nonzero:

    sum_(a<n) P_a(xi)^2/w_a=P_n'(xi)P_(n-1)(xi)/w_(n-1),
    w_a=product_(v=1)^a(1-q^v).

All derivatives are ordinary characteristic-zero derivatives before reduction. The neighbor is the original P_(n-1), not an associated polynomial; the squares are algebraic, not absolute.

The theorem has no fixed bound on the number t of even middle digits. The proof below regenerates the same invariant after absorbing any next middle digit, and has no constant depending on t. The t=0 family was already covered by the 2p^r+z, z<p^2 window. The t=1 family is precisely the independently accepted separated bottom-p theorem and retains that credit. Only t>=2 can receive incremental credit, after subtraction of EVERY prior successful high-order, fixed-degree, and residual certificate. The smallest new degree shape is n=4917 (p=3, r=7, k_1=5, k_2=3, c_1=c_2=2, d=1); this is a shape minimum, not a claim that every order at that degree is previously uncovered.

For n=2u+1, the accepted high-order subtraction remains phi(p^s)>C_u, where

    a_h=floor(u/h), b_h=((h+1)/2)a_h+floor(a_h/2),
    kappa=u+3floor(u^2/4)+2floor(u/4),
    C_u=u(u+1)(2u+1)/3-ceil(u/2)-kappa
        -sum_(odd 3<=h<=u) phi(h)b_h.

Thus incremental coverage also requires phi(p^s)<=C_u and failure of every other inherited successful certificate. The arbitrary-length j>=2 theorem retains its separate credit and is disjoint at the terminal exponent. The present extension does not close F020/F023; independent local/all-A and overlap obligations remain. No adjacent-gap, bottom-zero, odd-middle, even-terminal, different-leading-digit, general-polynomial, non-prime-power, novelty, FFT, stability, or runtime claim is made.

## 2. Source inputs and exact local geometry

SOURCE_BINDINGS.json copies and hashes the actual accepted sparse and bottom-p mathematical bodies and their independent acceptance records, plus selected underlying deep-cap, two-middle, first-two-digit, and deflation sources. This is a selected dependency binding, not a recursively complete archive audit. In particular, the sparse report SHA-256 is bda2193ca3b5e02479f20a61e21d803c965cf70d98dbb7f93400791cc36a014b; the accepted one-middle bottom-p report is 0ee61bbaeff0884c76638771e897f929b3998f13c36a969c7cb43c10bc648f6d. Their conclusions are used only within their accepted scope. The universal finite identities, arbitrary-prefix covers, and coefficient bounds have the explicit broader ranges stated below. The new many-digit carry/endpoint argument is proved, not imported from the one-middle conclusion.

Put t0=q-1, v(t0)=1, E_p=v(p)=(p-1)p^(s-1), and for legal positive indices

    V(a)=p^ord_p(a), W(b)=sum_(a=1)^b V(a), W(0)=0,
    N_b(z)=product_(a=0)^(b-1)(z+q^a),
    Q_b=product_(a=1)^b(1-q^(2a)).

W is base-p digit-linear and superadditive. Its carry defect in an addition is the sum of (p^a-p^(a-1)) over all carries across p^a, with multiplicities. All indices are legal because

    n<[2+(p-1)/(p^2-1)]p^r=[2+1/(p+1)]p^r<p^(r+1)<=p^s.

For every ell>=2 set beta_ell=p^floor(ell/2), D_ell=p^ell, and

    rho_ell=beta_ell/2                         if ell is even,
    rho_ell=(2p-1)p^(floor(ell/2)-1)/2         if ell is odd,
    T_ell(b)=sum_(a=1)^b min(V(a),rho_ell), R_ell=W-T_ell.

The beta_ell disjoint closed H-disks have centers -q^a, 0<=a<beta_ell. Their X-centers are i(q^(a/2)-q^(-a/2)). The maps z=v0^2 and X=v0+v0^-1, with v0 near i, are unit-derivative analytic isometries. Both q orientations use these same X-disks. Higher disks are strictly nested in matching lower disks.

Level one is separately defined as a SINGLE disk centered at z=-1 or X=0, with

    rho_1=1-1/(2p), beta_1=1,
    T_1(b)=rho_1 b, R_1(b)=W(b)-rho_1 b.

Every higher center has positive valuation at least one, so all higher disks lie strictly inside this outer disk. Section 8 reproves its arbitrary-prefix cap rather than extrapolating ell>=2 formulas.

The finite Newton identities and ordinary off-root chain rule are

    H_b=sum_(h=b mod 2) w_b N_h/[w_h Q_((b-h)/2)],
    H_b'=sum_(h+delta+2a=b,delta>=1)
       w_b z^(delta-1)N_h/[w_h Q_a(1-q^delta)],
    H_b'(v0^2)=v0^(b-2)[(b/2)P_b+(v0-v0^-1)P_b'/2].    (2.1)

A Newton product has coefficientwise weight at least T_ell(h) throughout every disk, not just at a central point.

The accepted deep cap, including its checked bottom-one extension, says that if M=p^k, ell>=k+2, and 0<=b<pM, then on EVERY full level-ell disk, in both orientations,

    R_ell(b)<=W(floor(b/2)), equality only b=0,1,
    P_b>=h_b:=W(b)-W(floor(b/2)),
    P_b'>=h_b-p for b odd,
    P_b'>=h_b-(p-1) for b even.                       (2.2)

An even P_b has its nonzero constant initial at h_b. For k=1, at ell=3 one has R_3(b)=floor(b/p)/2 for b<p^2; at ell>=4, R_ell(b)=0. This explicitly checks the extension and its strictness, not the false old delta=p^2 endpoint. On every full level-k disk with k>=2,

    R_k(b)<=W(b)/2 for b<pM,
    equality exactly b=aM.                           (2.3)

For k=1 and b<p^2 this follows directly from digit linearity: W(1)/2-R_1(1)>0 and W(p)/2-R_1(p)=0.

## 3. The length-independent invariant

For i=0,...,t set

    U_i=2p^r+sum_(a=1)^i c_a p^(k_a),
    m_i=n-U_i, D_i=p^(e_i), M_i=p^(e_(i+1)),
    u_i=(m_i-1)/2, G_i=W(u_i), h=(p-1)/2,
    C_i=P_(U_i), B_i=P_(U_i-1).

Define the ACTUAL shifted continuants by f_0^U=1, f_1^U=X, g_0^U=0, g_1^U=1, each with recurrence edge 1-q^(U+a). Then exactly

    P_(U+m)=f_m^U P_U-(1-q^U)g_m^U P_(U-1).          (3.1)

Abbreviate f_i=f_(m_i)^(U_i), g_i=g_(m_i)^(U_i). The invariant has four components:

A. Each even C_i has a complete monic cover at level e_i and the original core/neighbor bounds, residuals and outside ratios of Section 4. Prefix simplicity is NOT an assumption.

B. On EVERY full level-e_i disk,

    f_i>=G_i+p, f_i' exact G_i+h with constant initial,
    g_i exact G_i with constant initial, g_i'>=G_i.   (3.2)

C. On EVERY full level-e_(i+1) disk,

    g_i>=G_i+p-M_i,
    g_i'>=G_i+p-M_i-rho_(e_(i+1)).                   (3.3)

On its STRICT interior, f_i' is exact G_i+h. Its complete full-disk initial is an even Hermite polynomial, not an assumed constant on boundaries.

D. Outside the complete level-e_i cover, with tau the maximum center-distance valuation,

    C_i'/C_i>=-tau,
    B_i/C_i>=-D_i/2+rho_(e_i)-tau,
    B_i'/C_i>=-D_i/2-tau.                            (3.4)

Absorbing the next even digit regenerates exactly A-D: the new prefix remains even with a nonzero terminal even digit, the suffix retains all the half-digit properties proved next, and D_i>=p^2 M_i. No inequality deteriorates with length.

## 4. Arbitrary even prefixes: complete covers, not simplicity

These are the accepted sparse theorem's arbitrary-prefix inputs, valid independently of the number or arrangement of upper prefix digits. For U=QD<p^s, D=p^ell with ell>=2, terminal digit e=Q mod p even and 2<=e<p, set J=T_ell(U), E=J-D/2, C=P_U, B=P_(U-1). On every full disk,

    C>=J, C'>=J+D/2-p, B>=E, B'>=E.                 (4.1)

On a boundary Y!=0, after normalization, C has residual proportional to

    Y^((U-eD)/beta_ell) M_e(Z),

while B and the original ordinary C' have residuals proportional to the same Y-factor times M_(e-1)(Z), where

    M_e(Z)=e! sum_(a=0)^floor(e/2) Z^(e-2a)/(2^a a!(e-2a)!),
    Z_initial=gamma Y^(D/beta_ell), gamma!=0.

The Hermite recurrence makes M_e and M_(e-1) coprime for e<p. Each disk contains U/beta_ell roots counted with multiplicity, and the disks cover all U roots. At strict r interiors for the leading-two prefix U_0=2p^r, C_0 is exact J=W(p^r), because M_2(0)=1 and the Y-prefix factor is absent.

The ordinary B'>=E bound is important: it is the accepted arbitrary-prefix neighbor bound, not a bound for an associated neighbor or a simple prefix. In the Newton derivative expansion it is equivalent to

    F(delta+1+2a)-W(a)-V(delta)>=D/2,
    F(x)=R_ell(U)-R_ell(U-x).

Its accepted proof uses only the general block superadditivity inequality. The cases delta+1=lD+v, v=0,1, and 2<=v<D exhaust all indices; the only negative half-unit remainders in the proper-block case are v-1=1 or p, and the exact multiple-block expression there leaves D+W(v/2-1)-V(v-1)>=D-p>=D/2. The upper prefix is unrestricted. The ordinary off-root corrections are included in (4.1).

The complete monic cover, with multiplicities, gives all three outside ratios (3.4); it does not require a squarefree prefix. The proof retains tied nearest centers, the capped-interval bound, and W(x)/2-R_ell(x)<=D/2-rho_ell. The estimates are coefficientwise on the local outside disk and apply also to the new bottom annulus with tau<1. All coordinates there remain near X=0.

## 5. Many-digit carry lemma and the new ordinary endpoint

Take ANY remaining suffix

    m=sum remaining even c_a p^(k_a)+dp,
    u=(m-1)/2, G=W(u), h=(p-1)/2,

and let M be its largest power (M=p for the terminal suffix). Every digit of u is <=h. Its units digit is h, its p-digit is (d-1)/2<h, and every higher nonzero digit is c_a/2. No carry enters this description, regardless of the number of digits. Consequently

    W(m-1)=2G, W(m)=2G+p,
    u mod p^b <=(p^b-1)/2 for all b>=1,
    u mod p^b <(p^b-1)/2 for every b>1.              (5.1)

For every 0<=x<=u,

    W(x)+W(u-x)+V(2x+1)<=G+p.                        (5.2)

Indeed, if ord_p(2x+1)<=1, superadditivity suffices. If its order is b>1, then for every 2<=a<=b,

    x mod p^a=(p^a-1)/2>u mod p^a.

Thus the addition x+(u-x)=u carries across every such level, costing at least p^b-p. This argument retains the ENTIRE many-digit suffix; it does not replace it by the one-middle residue.

On a full deep disk, an odd derivative index delta=2b+1 in (2.1) has score at most W(u-b)+V(2b+1). For b<h it is at most G+1. For b>h, (5.2) makes it at most G+p-W(b)<=G+h. At b=h it is exactly G+p-h=G+h+1, since subtracting the units half-digit is carry-free. An even delta=2b has score at most W(u-b)+V(b)<=G. The deep cap is strict except at Newton indices 0 and 1; parity excludes 1 at the maximizing odd delta. Therefore the UNIQUE least derivative term is

    Newton index 0, delta=p, a=(m-p)/2,
    original P_m' exact G+h with nonzero constant initial.  (5.3)

The off-root chain correction has higher weight (already P_m>=G+p), so this is not differentiation of a residual polynomial.

On the full lower disk at M=p^k, the half-W cap gives the score bound

    R_k(b)+W(a)+V(delta)
       <=W(m-delta)/2+V(delta)
       <=G+V(delta)-W(delta-1)/2.                     (5.4)

For ord_p(delta)=0 the right increment is <=1. For order one it is <=h+1, uniquely at delta=p. For order b>=2, adding m-delta and delta-1 to obtain m-1 forces carries at every level 2,...,b: delta-1 has all bottom b digits p-1, while m-1 has its p-digit strictly deficient. Since W(delta-1)>=W(p^b-1)=b(p-1)p^(b-1), the improved score is

    <=G+[p+p^b-b(p-1)p^(b-1)]/2 <G+h+1.             (5.5)

The bracket is p(3-p) at b=2 and decreases thereafter. Thus the new endpoint delta=p is length-independent on full lower disks too.

If m=cM+a0 begins with an even digit, where a0 is the ENTIRE positive remaining lower suffix, the complete equality set is

    delta=p, Newton index bM for b=0,2,...,c,
    a=(c-b)M/2+(a0-p)/2.                             (5.6)

Necessity follows from the half-W equality set, the unique delta endpoint, parity, and m<pM. Conversely every listed addition and doubling is carry-free: (a0-p)/2 has digits (d-1)/2 at p, zero at units, and all higher digits at most h. This is the step that a one-middle citation alone would NOT justify.

Put A0=(a0-p)/2, omega^2=w_M, Z=N_M/omega. The actual factor units are

    w_m/(w_M^c w_(a0))->c!,
    w_(bM)/w_M^b->b!,
    Q_(vM+A0)/(Q_A0 w_M^v)->2^v v!.

After normalizing by w_(a0) omega^c/[Q_A0(1-q^p)], of weight G+h, ALL equality terms in (5.6) sum to M_c(Z). The lower suffix is kept in its exact scalar w_(a0)/Q_A0. Because c is even and <p, M_c(0)!=0. For terminal m=dp, Section 8 supplies instead M_(d-1)(Z), again with a nonzero constant, at the SAME weight G+h. Thus P_m' is exact G+h on every STRICT lower interior, not necessarily on a boundary. The off-root correction is at least E_p+G+p/2>G+h.

## 6. Actual shifted g': all four parities for arbitrary suffixes

The accepted universal finite identity, valid for every legal U,m, is

    (g_m^U)'=C_m^U sum_(1<=a<b<=m)
      (-1)^(a-1) q^(a(a-1)/2)
      P_(m-b)(q) P_(a-1)(q^-1) U_(b-a-1)(X/2)
      /[w_(m-b) w_(a-1) (1-q^(U+a))(1-q^(U+b))],      (6.1)

where C_m^U=product_(a=1)^m(1-q^(U+a)), and U_j(X/2) is the monic Chebyshev recurrence 1,X,X^2-1,... . This is the ACTUAL shifted ordinary derivative. It follows by differentiating the finite inverse-generating-series connection; the key exact cancellation is

    [1/(1-q^(U+a))-q^delta/(1-q^(U+a+delta))]/(1-q^delta)
      =1/[(1-q^(U+a))(1-q^(U+a+delta))].

No stopped adjacent-route estimate is imported. All endpoints and the off-root ordinary derivative are present. Since V(U)=D>M>=V(a),V(b), the shifted denominator values are exactly V(a),V(b), and v(C_m^U)=W(m). The Chebyshev factor has integral coefficients and nonnegative weight near X=0.

By the full deep cap it remains to prove, for

    x=floor((a-1)/2), y=floor((m-b)/2), z=u-y,

that

    W(x)+W(y)+V(a)+V(b)<=G+p.                        (6.2)

Here 0<=x<z<=u, with z>=x+2 in the even-even case. The proof uses only (5.1)-(5.2), so it applies to arbitrarily many remaining digits:

1. a even, b odd: a=2x+2, b=2z+1. Since x+1<=z, W(x)+V(a)=W(x+1)<=W(z); apply (5.2) at z.

2. Both even: a=2x+2, b=2z, x+1<=z-1. The two endpoint values are absorbed as W(x)+V(a)+V(b)<=W(z-1)+V(z)=W(z). Superadditivity gives the stronger total <=G.

3. Both odd: a=2x+1, b=2z+1. The positive interval length r0=z-x is divisible by min(V(a),V(b)). If V(a)<=V(b), W(z)-W(x)>=r0 absorbs V(a), then (5.2) applies at z. Otherwise W(u-x)-W(y)>=r0 absorbs V(b), and (5.2) applies at x.

4. a odd, b even: write a=2x+1, b=2z, r0=z-x and B0=V(z)=V(b). If r0>=B0, the interval W(u-x)-W(y) absorbs B0 and (5.2) applies at x. If r0<B0, reflection about the multiple z gives exactly

       W(z)-W(x)=B0+W(r0-1).

   Unless 2r0-1=B0, one has V(a)=V(2r0-1), so superadditivity and V(2v+1)-W(v)<=p prove (6.2). In the exception r0=(B0+1)/2, put A0=V(a). If A0<=B0 the same elementary score suffices. If A0>B0, then at every p-power C with B0<C<=A0,

       z mod C=(C+B0)/2>(C-1)/2>=u mod C.

   Thus z+y=u carries at every such level, costing at least A0-B0. The remaining score is at most

       G+B0-W((B0-1)/2)<=G+p.

   Notice the weak final inequality in the residue comparison. It also covers B0=1,C=p, where u's units residue is exactly (p-1)/2; no false strict-deficit assumption at that lowest level is needed.

For completeness the elementary score has no hidden digit-length restriction. If V(2v+1)=p^b, then v>=(p^b-1)/2 and W((p^b-1)/2)=b(p-1)p^(b-1)/2. Hence its maximum is p, at b=2 and the minimal such v; the b=0,1 cases are smaller and b>=3 is nonpositive for p>=3.

Equation (6.2) with W(m)=2G+p proves

    (g_m^U)'>=G                                      (6.3)

on EVERY full deep disk, uniformly in all phases and suffix lengths. This bound is proved for the actual shifted g', not transferred from an unshifted proxy.

## 7. Actual tails and all shift errors paid

The exact finite f and g connections are

    f_m^U=C_m^U sum_(a=0)^m [(1-q^U)/(1-q^(U+a))]
      (-1)^a q^(a(a+1)/2)P_(m-a)(q)P_a(q^-1)/[w_(m-a)w_a],
    g_m^U=C_m^U sum_(a=1)^m (-1)^(a-1)q^(a(a-1)/2)
      P_(m-a)(q)P_(a-1)(q^-1)/[w_(m-a)w_(a-1)(1-q^(U+a))].

The a=0 f ratio is 1. Set eta=C_m^U/w_m. Since V(U)=D and every tail index has value at most M,

    eta_initial=1, v(eta-1)>=D-M.

The f correction gains D-V(a); the g reciprocal correction gains D-2V(a). No interior endpoint is omitted.

For unshifted g_m^0 on a full deep disk, (5.2) bounds odd connection indices by G+p; their factors are both even, hence all possible weight-G contributions have constant initials. Even connection indices have score at most G and begin at weight G+p. Their entire weight-G constant sum is nonzero by the exact recurrence value

    g_m^0(0)=(-1)^u Q_u, v(Q_u)=G.

Thus g_m^0 is exact G with constant initial. The shifted correction is at least G+p+D-2M>G. Likewise the deep f correction is at least G+p+D-M; its ordinary derivative is at least G+D-M>G+h by the coarse loss p in (2.2). Section 5's constant ordinary endpoint survives. Section 6 proves the stronger actual g' bound independently. This establishes (3.2).

On full lower disks, the half-W cap applied to the actual g connection and superadditivity give

    g_m^U>=G+p-M,
    (g_m^U)'>=G+p-M-sigma, sigma=rho_lower.           (7.1)

The latter is ordinary coefficientwise Gauss differentiation. Only this weak bound is used; there is no full-lower g-unit assertion.

For f=eta P_m+Delta_f and g=eta g_m^0+Delta_g, the full-lower errors obey

    Delta_f>=G+p/2+D-M,
    Delta_f'>=G+p/2+D-M-sigma,
    Delta_g>=G+p+D-2M.

The derivative error exceeds G+h by D-M-sigma+1/2>0. All remaining errors are strictly above retained initials, since D>=p^2 M, sigma<M/p (also sigma=rho_1<1=M/p at bottom), and p<=M. The off-root corrections in Section 5 remain paid. Thus the strict-lower derivative exactness holds for the ACTUAL f, completing (3.3).

## 8. Arbitrary-prefix level-one cap, explicitly retained

This proof applies to ANY b=Qp<p^s with terminal digit e=Q mod p nonzero, not just one-middle degrees. Write b0=b-ep, rho=rho_1, R=R_1 and F(x)=R(b)-R(b-x). Every q-center is at valuation at least one from -1, so N_v has exact initial (z+1)^v on the whole outer disk and exact weight rho v.

For 0<=v,w<p, the general block inequality is

    F(lp+v+2up+2w)-W(up+w)
      >=lR(p)+p[W(l)-l]+p[W(u)-u]+F0(v+2w)-W(w),   (8.1)

where R(p)=p-1/2 and

    F0(epsilon p)=epsilon R(p),
    F0(epsilon p+t)=epsilon R(p)+p-rho+R(t-1), 0<t<p.

It follows directly from W superadditivity and quotient division: for x=alpha p+t,

    F(alpha p)>=pW(alpha)-alpha/2,
    F(alpha p+t)>=pW(alpha+1)-alpha/2-1+t/(2p), t>0.

For root terms take l=v=0. If w>0, writing 2w=epsilon p+t (necessarily t>0) leaves the strictly positive remainder

    F0(2w)-W(w)=epsilon(p-1)/2+p-1-t(p-1)/(2p)>0.

Equality therefore requires w=0, u<p, and no terminal carry, precisely a=up, 0<=2u<=e. The complete root initial at weight rho b is a nonzero scalar times

    Y^b0 M_e(Z), Z_initial=gamma Y^p, gamma!=0.       (8.2)

It has full degree b with unit leading coefficient, so all b roots, counted with multiplicity, lie in this single closed disk.

For ordinary derivative terms, write delta=lp+v. If v>0, the explicit small-block expression F0(v+2w)-W(w)>=p/2; V(delta)=1, so the result is strictly greater than -1/2. If v=0, l>=1, the l-dependent part after subtracting V(delta)=pV(l) is

    pW(l-1)-l/2,

which equals -1/2 only at l=1 and is larger for l>=2. Equality also requires w=0, u<p and no terminal carry. Thus the ENTIRE derivative equality set is

    delta=p, a=up, Newton index b0+(e-1-2u)p,
    0<=2u<=e-1.                                    (8.3)

Actual block factorial units sum all these terms to a nonzero scalar times

    Y^b0 M_(e-1)(Z)                                 (8.4)

at weight rho b-1/2. The off-root H/P correction is at least E_p+rho b, strictly higher. Thus (8.4) is the ORIGINAL ordinary derivative initial even though the reduced map Y->Y^p is inseparable.

For b=n and e=d odd, M_d and M_(d-1) are coprime, M_d has a simple zero at Z=0, and its d-1 nonzero roots give exactly (d-1)p outer-boundary roots counted before simplicity. The ordinary derivative is nonzero at every such root, so they are simple. Every remaining root is in the strict outer interior. For b=dp, rho dp-1/2=G+h and M_(d-1)(0)!=0, which supplies the terminal strict-lower assertion used above. Nothing in this argument restricts Q or the number of its upper digits.

## 9. Every core-scale boundary and the deepest interiors

Fix any i. Abbreviate U,m,D,M,G,C,B,f,g,J,E as above and b_U=1-q^U. At an actual original P_n root,

    fC=b_U gB,
    P_n'=f'C+fC'-b_U g'B-b_U gB'.                    (9.1)

On a level-e_i boundary where M_e(Z)=0, the original neighbor B is exact E by coprimeness, and g is exact G. Therefore f,C are nonzero. Put delta=v(f)-G>=p and gamma=v(C)-J>=0. The root equation gives delta+gamma=D/2. The leading term f'C is exact G+h+v(C); the other terms have respective lower gaps

    2delta-p-h, delta-h, delta-h.                   (9.2)

All are at least h+1>0. This handles every coincident residual class without inventing a separated root count.

If M_e(Z) is nonzero, C is exact J. The direct bounds (3.2),(4.1) put all three competing terms at least D/2-h>0 above f'C. This also covers f=B=0, without dividing by either. On the strict deepest r interiors the leading-two C_0 is exact J, so the same argument applies. No squarefree even-prefix theorem is invoked.

## 10. Every adjacent-scale annulus, including the bottom one

A root in a strict level-e_(i+1) interior but outside the closed level-e_i cover has

    sigma<tau<rho,
    sigma=rho_(e_(i+1)), rho=rho_(e_i).

The full-lower bounds and strict-interior derivative give g>=G+p-M, g'>=G+p-M-sigma, and f' exact G+h. The complete monic core cover makes C an analytic unit; (3.4) and f=b_U gB/C give

    v(f)>=G+p-M+D/2+rho-tau.

Divide (9.1) ONLY by C. Relative to its exact f' term, the three competitor lower gaps are

    D/2-M+h+1+rho-2tau,
    D/2-M+h+1+rho-tau-sigma,
    D/2-M+h+1-tau.                                  (10.1)

They are all positive, since M<=D/p^2, rho<D/p, and p>=3 imply M+rho<D/2. This applies equally to the bottom annulus, including tau<1. It retains tied nearest centers and does not divide by g or presume g is a unit on a full lower disk. No constant depends on the number of intervening strata.

## 11. Exhaustive root partition and genuine finite-length induction

Section 8 counts ALL n roots in the outer closed disk and settles every outer-boundary root. Every remaining root lies in exactly one of these disjoint classes:

1. For each i=0,...,t, a strict level-e_(i+1) interior outside the closed level-e_i cover.
2. For each i=0,...,t, a level-e_i disk boundary.
3. A strict level-r disk interior.

Strict nesting and complete covers make this partition exhaustive for every finite t. Sections 9-10 settle every class. Absorbing the next even digit inserts exactly one core boundary stratum and one annulus, governed by the same invariant A-D; Section 5 retains every lower digit, Section 6 handles every endpoint parity, and Section 8 is valid for the entire upper prefix. This is the asserted arbitrary-length induction, not finite-slice evidence or a one-middle extrapolation. Therefore P_n is squarefree.

All recurrence edges below n are nonzero. A common zero of original P_n and original P_(n-1) would propagate to P_0=1, so the original ordinary CD identity proves the claimed kernel nonvanishing. Modulo the maximal ideal P_n=X^n; its roots reduce to zero and are not +/-2. Also H_n(0)=1 and H_n(v0^2)=v0^n P_n(v0+v0^-1). The unit coordinate derivatives transfer multiplicity to H_n. Algebraic p-adic embedding and Galois conjugacy give every characteristic-zero primitive p^s phase, not merely one convenient phase or central disk.

## 12. Fresh controls, negative scope guards, and acceptance boundary

Fresh controls.py contains no imports or executions of accepted-packet or historical scientific programs. It checks exact carry scores for genuine suffixes with two, three, and four middle digits, all four endpoint parities, the large-endpoint exception, deep and full-lower delta=p equality sets, arbitrary-prefix level-one root/ordinary-derivative equality sets, actual shifted g' identities at rational q, and all displayed shift/boundary/annulus margins through thirty middle digits.

All endpoint pairs in large fixtures are covered by an exact running-maximum separation of the a-score and b-score, separately for each parity. Five smaller fixtures are also fully enumerated without that reduction. Derivative maxima are exactly enumerated by fixing the Newton index and p-adic order of delta: the least delta of the required parity strictly dominates every larger delta of the same order, since its W(a) is greater. Three unpruned derivative enumerations check this reduction. These are exact finite transcription/falsification controls, not the uniform proof.

Normal and optimized executions agree byte-for-byte. The final CONTROL.json records 671,247 explicit checks and the fixtures, including 90 new exact-rational shifted-derivative identities and 16,324 exceptional endpoint pairs. The explicit out-of-scope odd-middle suffix m=3^5+3^3+3=273 at p=3, x=121 has carry score 679>G+p=463. This rejects extending the invariant to odd middle digits, not squarefreeness of that polynomial. The old bottom-one delta=p^2 mechanism is rejected independently by P_3'=3X^2+3t0+t0^2, whose constant valuation is 2 at the legal phases rather than the old predicted 1.

The argument, not the numerical checks, establishes the unbounded candidate. Independent review bound to the final bytes is still required before scientific acceptance, table credit, or publication. Previously accepted work remains intact and can proceed independently.
