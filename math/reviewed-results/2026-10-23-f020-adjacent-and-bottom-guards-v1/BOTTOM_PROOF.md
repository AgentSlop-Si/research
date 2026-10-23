# F020: the separated bottom-p digit guard

23 October 2026 UTC. Original candidate for independent review. No external writes, self-acceptance, historical-program execution, or all-degree claim.

## 1. Exact theorem and coverage subtraction

Let p be any odd prime, c even with 2<=c<p, d odd with 1<=d<p, k>=3, r>=k+2, and s>r. Put

    N=p^r, M=p^k, A=2N+cM, n=A+dp.

For every characteristic-zero primitive p^s-th root q, the ORIGINAL polynomials

    P_0=1, P_1=X, P_(b+1)=X P_b-(1-q^b)P_(b-1),
    H_b(z)=sum_a [b choose a]_q z^a

are squarefree at b=n. At every original P_n root xi the ORIGINAL ordinary algebraic-square kernel is nonzero:

    sum_(a<n) P_a(xi)^2/w_a=P_n'(xi)P_(n-1)(xi)/w_(n-1),
    w_a=product_(v=1)^a(1-q^v).

No associated polynomial replaces P_(n-1), no absolute squares replace algebraic squares, and all derivatives are ordinary characteristic-zero derivatives taken before reduction.

The minimum degree is 543 (p=3,c=2,d=1,k=3,r=5). The displayed shape has three nonzero base-p digits and bottom exponent exactly one. It is disjoint from the first-two-digit range, the fourth block, one-leading-plus-units, the 2p^r+t window with t<p^2, single-middle families, accepted separated j>=2 sparse families, and the submitted adjacent j=k-1>=2 family. No j=0, k=2, adjacent gap, odd c, even d, more middle digits, or other orders are asserted here.

Every separately successful high-order, fixed and residual certificate retains its prior credit. For n=2u+1 the accepted high-order subtraction is phi(p^s)>C_u, where

    a_h=floor(u/h), b_h=((h+1)/2)a_h+floor(a_h/2),
    kappa=u+3floor(u^2/4)+2floor(u/4),
    C_u=u(u+1)(2u+1)/3-ceil(u/2)-kappa
        -sum_(odd 3<=h<=u) phi(h)b_h.

Incremental coverage, if accepted, is only the displayed family outside EVERY earlier successful certificate, in particular phi(p^s)<=C_u. The high-order theorem and first-two-digit theorem are source-bound inputs, not reproved or relabeled new. This does not close F020/F023, discard independent local/all-A or overlap obligations, or establish historical novelty, FFT, complexity, or stability improvement.

## 2. Exact source inputs and notation

SOURCE_BINDINGS.json binds selected actual mathematical bodies and their acceptance/source bindings. In particular the frozen sparse report (SHA-256 bda2193ca3b5e02479f20a61e21d803c965cf70d98dbb7f93400791cc36a014b) and its independent review supply the arbitrary even-prefix cap, original neighbor derivative, outside-cover estimates, and genuine finite f/g connections. The deep-cap proof itself and the original deflation report with acceptance are retained. This is a selected source comparison, not a recursive archive audit.

Set t=q-1, v(t)=1, E_p=v(p)=(p-1)p^(s-1), and, for legal positive indices,

    V(a)=p^ord_p(a), W(b)=sum_(a=1)^b V(a), W(0)=0,
    Q_b=product_(a=1)^b(1-q^(2a)),
    N_b(z)=product_(a=0)^(b-1)(z+q^a).

W is base-p digit-linear and superadditive. Its exact carry defect is the sum of (p^h-p^(h-1)) times the carries across p^h. All indices below n are legal because

    n<[2+(p-1)/p^2+(p-1)/p^4]N<pN<=p^s.

For ell>=2 use the inherited disks with beta_ell=p^floor(ell/2), centers z=-q^a (0<=a<beta_ell), and

    rho_ell=beta_ell/2                         (ell even),
    rho_ell=(2p-1)p^(floor(ell/2)-1)/2         (ell odd).

Write T_ell(b)=sum_(a<=b) min(V(a),rho_ell), R_ell=W-T_ell. The corresponding X centers are i(q^(a/2)-q^(-a/2)). The maps z=v0^2, X=v0+v0^(-1), v0 near i, are unit-derivative analytic isometries. Both q orientations use the same X disks. Higher disks lie strictly inside their matching lower disks.

The new outer scale is a SINGLE disk centered at z=-1 (equivalently X=0) with

    rho_1=(2p-1)/(2p)=1-1/(2p), beta_1=1,
    T_1(b)=rho_1 b, R_1(b)=W(b)-rho_1 b.

All k disks lie strictly inside it, since their centers have valuation >=1>rho_1. This definition is proved below at level one rather than inferred from a formula whose accepted range began at two.

The finite identities and off-root chain rule are

    H_b=sum_(h=b mod 2) w_b N_h/[w_h Q_((b-h)/2)],
    H_b'=sum_(h+delta+2a=b,delta>=1)
             w_b z^(delta-1)N_h/[w_h Q_a(1-q^delta)],
    H_b'(v0^2)=v0^(b-2)[(b/2)P_b+(v0-v0^-1)P_b'/2].   (2.1)

For a prefix U, define ACTUAL continuants f_0=1,f_1=X,g_0=0,g_1=1, each with shifted edge 1-q^(U+a). Then

    P_(U+m)=f_m^U P_U-(1-q^U)g_m^U P_(U-1).           (2.2)

No unshifted proxy is substituted.

## 3. Inherited full-disk inputs, only in their valid range

The accepted deep cap says, when D=p^ell, M0=p^a, ell>=a+2 and b<pM0,

    R_ell(b)<=W(floor(b/2)), equality only b=0,1,
    P_b>=h_b:=W(b)-W(floor(b/2)),
    P_b'>=h_b-p (b odd), P_b'>=h_b-(p-1) (b even).     (3.1)

Even P_b has its exact nonzero constant initial at h_b. The proof of this cap also covers a=1: its basis formula S(p^e)=(ell-e)(p-1)p^(e-1)/2 for e>=floor(ell/2), and S(p^e)=W(p^e)/2 below that, gives S(p^e)>p^e/2 for the relevant e<=1 whenever ell>=3; the endpoints 0,1 are unchanged. This checks the needed range extension of the input, not the false p^2 derivative endpoint at bottom one.

At a full level-k disk, for b<pM,

    R_k(b)<=W(b)/2, equality exactly b=eM.             (3.2)

At level one the same statement for b<p^2 follows directly from digit linearity: S_1(1)=(p-1)/(2p)>0 and S_1(p)=0.

For either even prefix U=2N (ell=r) or U=A (ell=k), put D=p^ell, J=T_ell(U), E=J-D/2, C=P_U, B=P_(U-1). The accepted arbitrary-prefix theorem gives a COMPLETE monic cover, U/beta_ell roots per disk counted with multiplicity, and

    C>=J, C'>=J+D/2-p, B>=E, B'>=E.                  (3.3)

At a disk boundary Y!=0 their residuals are, up to nonzero scalars and a common nonzero Y factor, M_e(Z) for C and M_(e-1)(Z) for B,C', where e is the terminal even digit (2 or c), Z_initial=gamma Y^(D/beta_ell), and

    M_e(Z)=e! sum_(a=0)^floor(e/2) Z^(e-2a)/(2^a a!(e-2a)!).

M_e and M_(e-1) are coprime for e<p by their three-term recurrence. At strict r interiors C=P_(2N) is exact J=W(N).

Outside that complete cover, with tau the maximal center-distance valuation,

    C'/C>=-tau,
    B/C>=-D/2+rho_ell-tau,
    B'/C>=-D/2-tau.                                  (3.4)

These are coefficientwise local bounds, including tied nearest centers. They use the cover with multiplicities, not prefix squarefreeness. All are inherited full-disk/actual-neighbor statements. There is no central-disk extrapolation.

## 4. The bottom-one carry invariant and the new derivative endpoint

Use either tail m=cM+dp after U=2N, or m=dp after U=A. Put

    u=(m-1)/2, G=W(u), h=(p-1)/2.

Every base-p digit of u is <=h, its units digit is h, and its p digit is (d-1)/2<h. Consequently

    W(m-1)=2G, W(m)=2G+p,
    u mod p^b < (p^b-1)/2 for EVERY b>1.              (4.1)

For 0<=x<=u the exact odd-index carry bound is

    W(x)+W(u-x)+V(2x+1)<=G+p.                         (4.2)

If ord_p(2x+1)<=1 this is superadditivity. Otherwise x mod p^a=(p^a-1)/2 exceeds u mod p^a for every 2<=a<=ord_p(2x+1), forcing W carry defect at least V(2x+1)-p. This is the accepted sparse carry argument, whose validity does not require two bottom half-digits.

On a full deep disk, an odd derivative index delta=2b+1 in (2.1) has score at most W(u-b)+V(2b+1). If b<h, it is <=G+1. If b>h, (4.2) makes it <=G+p-W(b)<=G+h. At b=h it equals G+p-h=G+h+1, since subtracting h from u is carry-free. Even delta=2b has score <=W(u-b)+V(b)<=G. Strictness in (3.1) forces the Newton index to be zero at equality. Therefore the UNIQUE least term is

    Newton index 0, delta=p, a=(m-p)/2,
    P_m' exact G+h, with a nonzero constant initial.   (4.3)

The old delta=p^2 endpoint is not retained. The chain-rule extra term has weight >=G+p, strictly greater than G+h; thus this is an original ordinary derivative statement off roots.

On full level-k disks, (3.2) bounds the score of a derivative term by

    W(m-delta)/2+V(delta)
       <=G+V(delta)-W(delta-1)/2.                      (4.4)

If ord_p(delta)=0 this is <=G+1. If ord_p(delta)=1 it is <=G+h+1, uniquely at delta=p. If b=ord_p(delta)>=2, every level 2,...,b carries when adding m-delta and delta-1 to obtain m-1, because delta-1 has all those lower digits p-1 while m-1 does not. The improved bound is

    G+[p+p^b-b(p-1)p^(b-1)]/2 < G+h+1.                (4.5)

The bracket is already p(3-p) at b=2 and decreases thereafter for p>=3. Thus delta=p is again the only possible equality endpoint. For m=cM+dp the COMPLETE equality set is

    delta=p, Newton index bM (b=0,2,...,c),
    a=(c-b)M/2+(d-1)p/2.                              (4.6)

All additions/doublings are carry-free, and (3.2) proves that there are no others. Put a0=(d-1)p/2, omega^2=w_M, Z=N_M/omega. Actual factor units give

    w_m/(w_M^c w_(dp))->c!,
    w_(bM)/w_M^b->b!,
    Q_(vM+a0)/(Q_a0 w_M^v)->2^v v!.

After normalizing by w_(dp) omega^c/[Q_a0(1-q^p)], of weight G+h, ALL equality terms sum to M_c(Z). Its constant is nonzero because c is even and <p. Hence P_m' is exact G+h on EVERY strict k interior, but not automatically on its boundary. The off-root correction has weight >=E_p+G+p/2>G+h.

The analogous terminal statement for m=dp at the new level-one disk is proved in Section 7: the full derivative initial is M_(d-1)(Z), also with nonzero constant. Thus it too is exact G+h on the strict lower interior.

## 5. A new full-deep-disk bound for the ACTUAL shifted g derivative

The previously available g' bound G-(p-1) is insufficient here. We use an exact ordinary derivative cancellation, not an estimate at a central point.

Let C_m^U=product_(a=1)^m(1-q^(U+a)) and let U_j(X/2) denote Chebyshev's monic recurrence U_0=1,U_1=X,U_(j+1)=XU_j-U_(j-1). Finite generating-series inversion and differentiation give exactly

    (g_m^U)' = C_m^U sum_(a>=1,b>a,b<=m)
      (-1)^(a-1) q^(a(a-1)/2)
      P_(m-b)(q)P_(a-1)(q^-1) U_(b-a-1)(X/2)
      /[w_(m-b)w_(a-1)(1-q^(U+a))(1-q^(U+b))].        (5.1)

For clarity, if A_j=P_j(q)/w_j and B_j=(-1)^j q^(j(j-1)/2)P_j(q^-1)/w_j, their truncated generating series satisfy AB=1 and A_X=A L, B_X=-B L, where L_delta=U_(delta-1)/(1-q^delta). Differentiating the exact g connection cancels the denominator because

    [1/(1-q^(U+a))-q^delta/(1-q^(U+a+delta))]/(1-q^delta)
      =1/[(1-q^(U+a))(1-q^(U+a+delta))].

This proves (5.1) with every endpoint and ordinary off-root term present. It is also recorded, without a squarefreeness conclusion, in the separately stopped adjacent-boundary identity packet. No unresolved bound from that route is imported.

Here V(U)=D exceeds every endpoint valuation, so the shifted denominators have values V(a),V(b), and v(C_m^U)=W(m). Chebyshev coefficients are integers, and X reduces to zero, so their weights are >=0. By (3.1), it remains to prove the following exact endpoint inequality, with

    x=floor((a-1)/2), z=u-floor((m-b)/2), y=u-z:

    W(x)+W(y)+V(a)+V(b)<=G+p.                         (5.2)

We give all four parity cases; 0<=x<z<=u except that the harmless even-even endpoint convention gives z>=x+2.

1. a even, b odd: a=2x+2, b=2z+1. Then W(x)+V(a)=W(x+1)<=W(z), so (4.2) at z proves (5.2).

2. a even, b even: a=2x+2, b=2z. Since x+1<=z-1,

       W(x)+V(a)+V(b)<=W(z-1)+V(z)=W(z).

   Superadditivity proves the stronger bound <=G.

3. a odd, b odd: a=2x+1, b=2z+1. Let r0=z-x. Since both endpoints are divisible by min(V(a),V(b)), r0 is a positive multiple of that minimum. If V(a)<=V(b), the interval W(z)-W(x)>=r0 absorbs V(a), and (4.2) at z applies. Otherwise the equal-length interval W(u-x)-W(y) absorbs V(b), and (4.2) at x applies.

4. a odd, b even: a=2x+1, b=2z, r0=z-x, B0=V(z)=V(b). If r0>=B0, W(u-x)-W(y)>=r0 absorbs V(b), and (4.2) at x applies. If 1<=r0<B0, exact reflection about the multiple z gives

       W(z)-W(x)=B0+W(r0-1).

   Unless 2r0-1=B0, V(a)=V(2r0-1), so superadditivity and the inherited elementary score V(2v+1)-W(v)<=p prove (5.2). In the remaining case r0=(B0+1)/2, put V(a)=A0. If A0<=B0 the same bound suffices. If A0>B0, at every p-power C strictly above B0 through A0,

       z mod C=(C+B0)/2 > (C-1)/2 > u mod C.

   Adding z and y to obtain u therefore has carry defect >=A0-B0. Thus

       W(x)+W(y)+A0+B0 <=G+B0-W((B0-1)/2)<=G+p,

   by the same elementary score. This exhausts the exceptional large endpoint rather than silently bounding it by B0.

Equation (5.2), W(m)=2G+p, and (5.1) prove uniformly on EVERY full deep disk

    (g_m^U)' >= G.                                    (5.3)

This is a genuine shifted, phase-uniform bound. It does not assert that g' is a unit or that a residual derivative computes the ordinary derivative.

## 6. Tail values and paid shift errors

The inherited exact finite connections are

    f_m^U=C_m^U sum_(a=0)^m [(1-q^U)/(1-q^(U+a))]
      (-1)^a q^(a(a+1)/2)P_(m-a)(q)P_a(q^-1)/[w_(m-a)w_a],
    g_m^U=C_m^U sum_(a=1)^m (-1)^(a-1)q^(a(a-1)/2)
      P_(m-a)(q)P_(a-1)(q^-1)/[w_(m-a)w_(a-1)(1-q^(U+a))].

The a=0 f ratio is 1. Set eta=C_m^U/w_m; eta has initial 1 and v(eta-1)>=D-M0, where M0 is the largest power in the tail (M or p). The f correction has extra value D-V(a); the reciprocal correction in g has value D-2V(a).

On full deep disks, (3.1) and (4.2) imply

    f_m^U>=G+p,
    f_m^U{}' exact G+h with constant initial,
    g_m^U exact G with constant initial,
    g_m^U{}'>=G.                                     (6.1)

For g with U=0, odd connection indices have score <=G+p by (4.2); even indices have score <=G. All weight-G terms therefore use even P factors and are constant. Their sum is nonzero by the exact recurrence value g_m^0(0)=(-1)^u Q_u. The shifted g correction is >=G+p+D-2M0>G. The deep f correction is >=G+p+D-M0, and its derivative is >=G+D-M0>G+h, using only the coarse ordinary loss p from (3.1). Thus the retained derivative initial is unaffected. Equation (5.3) supplies the sharper actual g derivative, independently of an error estimate.

On full lower disks, (3.2), superadditivity, and V(a)<=M0 give

    g_m^U>=G+p-M0,
    g_m^U{}'>=G+p-M0-rho_lower.                       (6.2)

The derivative is the ordinary coefficientwise Gauss bound. The full-lower shift errors are

    Delta_f>=G+p/2+D-M0,
    Delta_f'>=G+p/2+D-M0-rho_lower,
    Delta_g>=G+p+D-2M0.

They are strictly above all retained initials because D>=p^2 M0, rho_lower<M0/p (also rho_1<p/p), and p<=M0. In particular D-M0-rho_lower+1/2>0. Therefore the strict-lower-interior derivative in Section 4 or 7 remains exact G+h for the ACTUAL f. No full-lower g-unit assertion or division by g is used.

## 7. The new arbitrary-prefix outer level-one cap

We prove the outer count directly, not by importing a first-two-digit theorem for the large degree n. Put B=p, rho=rho_1, and consider b=Qp with terminal digit e=Q mod p nonzero. For the application b=n, e=d is odd; b=dp supplies the terminal tail derivative. Write b0=b-ep and R=R_1. Since every q-center is at distance >=1 from -1, every N_v has exact initial (z+1)^v on the radius-rho disk. Thus its weight is v rho, not merely a central value.

The general block identity, inherited algebraically from W superadditivity, is

    F(lp+v+2up+2w)-W(up+w)
      >= lR(p)+p[W(l)-l]+p[W(u)-u]+F0(v+2w)-W(w),   (7.1)

where F(x)=R(b)-R(b-x), 0<=v,w<p, R(p)=(2p-1)/2, and

    F0(epsilon p)=epsilon R(p),
    F0(epsilon p+t)=epsilon R(p)+p-rho+R(t-1), 0<t<p.

Here R(t-1)=(t-1)/(2p), so every small-block inequality can be checked explicitly, without assuming ell>=2.

For the root expansion take l=v=0. If w>0, write 2w=epsilon p+t, 0<t<p; then

    F0(2w)-W(w)
      =epsilon(p-1)/2+p-1-t(p-1)/(2p)>0.

Hence equality requires w=0. The block terms and the terminal-digit carry condition then force precisely a=up with 0<=2u<=e. The root initial is a nonzero scalar times

    Y^b0 M_e(Z), Z_initial=gamma Y^p, gamma!=0,         (7.2)

at weight T_1(b)=rho b. Its degree is b and leading coefficient is a unit. Thus the SINGLE closed disk contains all b roots counted with multiplicity.

For the ordinary derivative, write delta=lp+v. If v>0, the explicit F0 formula gives F0(v+2w)-W(w)>=p/2, while V(delta)=1, so this case is strictly above -1/2. If v=0, l>=1, and the l-dependent part after subtracting V(delta)=p V(l) is

    lR(p)+p[W(l)-l]-pV(l)=pW(l-1)-l/2.

It equals -1/2 exactly at l=1 and is strictly larger for l>=2. Equality also forces w=0, u<p and no terminal carry, precisely

    delta=p, a=up, Newton index b0+(e-1-2u)p,
    0<=2u<=e-1.                                     (7.3)

The same actual block factorial units sum ALL equality terms to a nonzero scalar times

    Y^b0 M_(e-1)(Z),                                 (7.4)

at weight T_1(b)-1/2. For example a common normalization before the Y factor is w_b/[w_b0 omega^(e-1)(1-q^p)], omega^2=w_p; its weight plus rho b0 is rho b-1/2. The root normalization uses omega^e instead. All factorials are units because e<p. The off-root chain term has weight >=E_p+T_1(b)>T_1(b)-1/2, so (7.4) is also the ORIGINAL ordinary P derivative initial.

For b=n and e=d, M_d has a simple zero at Z=0 and d-1 nonzero simple zeros, since d<p and the Hermite recurrence gives coprimeness with M_(d-1). On the disk boundary Y!=0, (7.2) and (7.4) cannot vanish together. Exactly (d-1)p outer-boundary roots, counted before simplicity, are therefore simple. All remaining roots are in the strict outer interior. For b=dp, T_1(dp)-1/2=G+h and M_(d-1)(0)!=0; this proves the terminal derivative assertion used in Sections 4 and 6, including p=3,d=1.

## 8. Every higher boundary and deepest interior

Use either core/tail split (U,m)=(A,dp) at level k or (2N,cM+dp) at level r. Let b_U=1-q^U, v(b_U)=D. At an actual P_n root,

    fC=b_U gB,
    P_n'=f'C+fC'-b_U g'B-b_U gB'.                     (8.1)

On a core boundary with M_e(Z)=0, the original B is exact E by residual coprimeness, and g is exact G. Hence f,C are nonzero. Put delta=v(f)-G>=p, gamma=v(C)-J>=0. The root identity gives delta+gamma=D/2. The f'C term has EXACT value G+h+v(C). From (3.3),(5.3),(6.1), its three competing terms have lower gaps

    2delta-p-h, delta-h, delta-h.                     (8.2)

Each is >=h+1>0. This settles coincident residual classes without separating nonexistent root counts.

If M_e does not vanish, C is exact J. Direct comparison gives all three lower gaps >=D/2-h>0. This branch includes f=B=0, with no division by them. On strict deepest r interiors the leading-two core is exact J, so the same comparison applies.

## 9. Both annuli, including the new bottom annulus

A root in a strict lower-disk interior but outside the closed upper cover has

    sigma<tau<rho,

where rho is the upper radius and sigma is the lower radius (rho_k or rho_1). The complete monic cover makes C an analytic unit there. Equations (3.4),(6.2), the exact strict-lower f' value, and the root equation give

    v(f)>=G+p-M0+D/2+rho-tau.

Divide (8.1) ONLY by C. Relative to f', exact at G+h, the three competitors have lower gaps

    D/2-M0+h+1+rho-2tau,
    D/2-M0+h+1+rho-tau-sigma,
    D/2-M0+h+1-tau.                                  (9.1)

They are all positive because M0<=D/p^2, rho<D/p, and p>=3 imply M0+rho<D/2. This includes the entire annulus from the singleton level-one disk to the k cover, even where tau<1. All coordinates remain near X=0 and are unit-derivative isometries; no argument assumes a central disk or a g unit.

## 10. Exhaustive ledger and original kernel

Section 7 first counts all n roots in the outer closed disk and settles its (d-1)p boundary roots. Every remaining root lies in exactly one of the following disjoint sets:

1. Strict level-one interior outside the closed k cover.
2. The k boundaries.
3. Strict k interiors outside the closed r cover.
4. The r boundaries.
5. The strict r interiors.

Strict nesting and the complete covers make this list exhaustive, including all coincident residual classes. Sections 8-9 settle every set, so P_n is squarefree.

All recurrence edges below n are nonzero. A common zero of ORIGINAL P_n and P_(n-1) would propagate down to P_0=1. Therefore the original ordinary CD identity displayed in Section 1 proves kernel nonvanishing. Modulo the maximal ideal P_n=X^n; its roots reduce to zero and are not +/-2. H_n(0)=1, and H_n(v0^2)=v0^n P_n(v0+v0^-1) with unit coordinate derivatives transfers all multiplicities. Algebraic p-adic embedding/Galois conjugacy supplies every characteristic-zero primitive phase.

## 11. Controls and limits

Fresh controls.py checks only transcription and falsification targets: bottom carry scores, the unique delta=p lower/deep derivative endpoint and all equality indices, the four-parity endpoint inequality including its large-endpoint exception, level-one root/derivative equality sets for arbitrary upper prefixes, actual shifted derivative identity at exact rational q, shift margins, and complete scope legality. Normal and optimized runs pass 942,039 explicit checks with byte-identical output, including 36 exact-rational actual shifted derivative identities. No historical program is executed/imported, no root census substitutes for the uniform argument, and no accepted packet is modified.

The old bottom-one delta=p^2 derivative claim is explicitly rejected by the exact p=3,m=3 control: P_3'=3X^2-(2-q-q^2), whose constant coefficient has t-adic value 2 for legal s>=6, whereas the old G+p-p prediction would be 1. This is a failure of the old derivative bound, not squarefreeness. The positive replacement is delta=p, with G+h=2.

Scientific acceptance, table credit, and any publication require a separate reviewer bound to these final bytes. The present artifact is only a candidate theorem with its precise exclusions.
