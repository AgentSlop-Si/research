# F020: sparse even-digit induction with an odd terminal digit

23 October 2026 UTC. Original mathematical candidate for independent review. This packet does not accept or publish itself. No frozen accepted packet was modified, and no historical or author-supplied scientific program was run or imported.

## 1. Proposed unbounded theorem and credit boundary

Let p be an odd prime, t>=0, and

    e_0=r > e_1=k_1 > ... > e_t=k_t > e_(t+1)=j>=2,
    e_i-e_(i+1)>=2 for every i,
    c_a even, 2<=c_a<p; d odd, 1<=d<p; s>r,
    n=2p^r+sum_(a=1)^t c_a p^(k_a)+d p^j.

For t=0 the displayed exponent list means simply r>=j+2. The proposal is that for every characteristic-zero primitive p^s-th root q, the ORIGINAL polynomials

    P_0=1, P_1=X, P_(b+1)=X P_b-(1-q^b)P_(b-1),
    H_b(z)=sum_a [b choose a]_q z^a

are squarefree at b=n, and at every P_n root xi the ORIGINAL algebraic-square kernel is nonzero:

    sum_(a<n) P_a(xi)^2/w_a=P_n'(xi)P_(n-1)(xi)/w_(n-1),
    w_a=product_(v=1)^a(1-q^v).

All derivatives below are ordinary characteristic-zero derivatives, before reduction. No associated neighbor replaces P_(n-1), and no absolute-square kernel is substituted.

There is no upper bound on t: r grows with t. This is a genuine finite-length induction with a length-independent invariant, not a further fixed-digit slice. Its t=0 and t=1 parts retain their prior credit. The first new degree shape has t=2, with minimum n=14751 (p=3,j=2,k_2=4,k_1=6,r=8,c_1=c_2=2,d=1). No adjacent scales, j=1, odd middle digits, even terminal digits, other leading digits, or non-prime-power orders are claimed.

High-order deflation, fixed-degree and all successful residual certificates keep their existing credit. For n=2u+1 the high-order exclusion is phi(p^s)>C_u, with

    a_h=floor(u/h), b_h=((h+1)/2)a_h+floor(a_h/2),
    kappa=u+3floor(u^2/4)+2floor(u/4),
    C_u=u(u+1)(2u+1)/3-ceil(u/2)-kappa
        -sum_(odd 3<=h<=u) phi(h)b_h.

Thus incremental coverage, IF accepted, is only t>=2 in the displayed domain outside every earlier successful certificate, in particular with phi(p^s)<=C_u. This is not a Catalan bound. F020/F023 remain open as whole owners. No historical novelty, FFT, algorithmic speedup, bit-complexity or stability claim follows.

## 2. Precisely bound inherited inputs

The accepted two-middle report and independent review are copied and hash-bound in SOURCE_BINDINGS.json. Their original author report SHA-256 is 7608ae11d5157573b923a5b4ae122ed0448c7f9f4a3127556684c3807dc895b2. Selected underlying deep-cap bodies and original source bindings are also copied, not silently substituted by an archive. This is not a recursively complete source/archive audit.

Use t0=q-1, v(t0)=1 and E_p=v(p)=(p-1)p^(s-1). For nonzero legal indices let

    V(a)=p^ord_p(a), W(b)=sum_(a=1)^b V(a), W(0)=0.

At a level ell>=2 put

    beta_ell=p^floor(ell/2), D_ell=p^ell,
    rho_ell=beta_ell/2                              (ell even),
    rho_ell=(2p-1)p^(floor(ell/2)-1)/2              (ell odd),
    T_ell(b)=sum_(a=1)^b min(V(a),rho_ell), R_ell=W-T_ell.

The beta_ell disjoint closed disks have H-centers -q^a (0<=a<beta_ell); the corresponding X-centers are i(q^(a/2)-q^(-a/2)). Higher-level disks are strictly nested in their matching lower-level disks. The coordinates z=v0^2, X=v0+v0^(-1), v0 near i, are analytic isometries with unit derivatives. The finite Newton identities and ordinary off-root chain rule are

    H_b=sum_(h=b mod2) w_b N_h/[w_h Q_((b-h)/2)],
    H_b'=sum_(h+delta+2a=b,delta>=1)
          w_b z^(delta-1)N_h/[w_h Q_a(1-q^delta)],
    N_h=product_(v=0)^(h-1)(z+q^v),
    Q_a=product_(v=1)^a(1-q^(2v)),
    H_b'(v0^2)=v0^(b-2)[(b/2)P_b+(v0-v0^(-1))P_b'/2].   (2.1)

A Newton product has coefficientwise weight >=T_ell(h) on every level-ell disk, in both q orientations on the same X-disks. W and R are base-p digit-linear, and W is superadditive with equality exactly for carry-free addition.

The accepted enlarged deep cap, used only in its proved range, says: on a full level-ell disk, if M=p^k and ell>=k+2, then for 0<=b<pM,

    R_ell(b)<=W(floor(b/2)), equality only b=0,1,
    P_b>=h_b:=W(b)-W(floor(b/2)),
    P_b'>=h_b-p (b odd), P_b'>=h_b-(p-1) (b even).        (2.2)

For even b, the weight-h_b initial is its nonzero constant P_b(0). These are full-disk coefficient bounds, not values at auxiliary roots.

All indices here are legal: by the geometric gap bound,

    n<[2+(p-1)/(p^2-1)]p^r=[2+1/(p+1)]p^r<p^(r+1)<=p^s.

Every recurrence edge and denominator appearing below is nonzero. We never require the total polynomial weight to be less than E_p.

## 3. The length-independent invariant

For 0<=i<=t let

    U_i=2p^r+sum_(a=1)^i c_a p^(k_a),
    m_i=n-U_i, D_i=p^(e_i), M_i=p^(e_(i+1)), L=p^j,
    G_i=W((m_i-1)/2), C_i=P_(U_i), B_i=P_(U_i-1),
    f_i=f_(m_i)^(U_i), g_i=g_(m_i)^(U_i).

Here f,g are the ACTUAL associated continuants defined by

    f_0^U=1,f_1^U=X,g_0^U=0,g_1^U=1,
    u_(b+1)^U=Xu_b^U-(1-q^(U+b))u_(b-1)^U,
    P_(U+m)=f_m^U P_U-(1-q^U)g_m^U P_(U-1).             (3.1)

The invariant, valid for every i regardless of the number of digits left, consists of:

A. The even prefix C_i has a complete uniform monic level-e_i cover, plus full-disk original core/neighbor derivative bounds and terminal residuals described in Section 4. Prefix simplicity is NOT an induction hypothesis.

B. On every full level-e_i disk, the remaining odd tail satisfies

    f_i>=G_i+L, f_i' exact G_i+L-p with constant initial,
    g_i exact G_i with constant initial,
    g_i'>=G_i-(p-1).                                    (3.2)

C. On every full level-e_(i+1) disk,

    g_i>=G_i+L-M_i,
    g_i'>=G_i+L-M_i-rho_(e_(i+1)).                       (3.3)

On its STRICT interior, f_i' has exact value G_i+L-p. Its full-disk derivative initial is the appropriate EVEN Hermite polynomial, not an assumed constant (Section 6).

D. Outside the prefix's complete cover, with tau the maximum center-distance valuation,

    C_i'/C_i>=-tau,
    B_i/C_i>=-D_i/2+rho_(e_i)-tau,
    B_i'/C_i>=-D_i/2-tau.                               (3.4)

These are coefficientwise estimates on the appropriate local disk around the outside point. The ratio argument needs only the complete monic cover, NOT simplicity.

The invariant is regenerated at i+1 simply by absorbing the next even digit into the prefix. The new prefix is again even with a nonzero terminal even digit; the new suffix retains every digit and carry property used below; the next gap is again >=2. Thus no numerical constant, missing case or extra hypothesis grows with the number of digits.

## 4. Arbitrary-prefix core cover and ordinary neighbor derivative

For any even U=QD<p^s, D=p^ell, with terminal digit e=Q mod p even and 2<=e<p, set J=T_ell(U), E=J-D/2 and Z=N_D/sqrt(w_D). On every full level-ell disk, the accepted arbitrary-prefix terminal cap gives

    C=P_U>=J, C'>=J+D/2-p, B=P_(U-1)>=E,
    C_initial proportional to Y^((U-eD)/beta_ell) M_e(Z),
    C'_initial and B_initial proportional to
          Y^((U-eD)/beta_ell) M_(e-1)(Z),               (4.1)

where Z_initial=gamma Y^(D/beta_ell), gamma!=0, and

    M_e(Z)=e! sum_(a=0)^floor(e/2) Z^(e-2a)/(2^a a!(e-2a)!).

Each of the beta_ell disks contains exactly U/beta_ell roots counted with multiplicity, and there are no other roots. In particular this statement applies to EVERY U_i, including U_0=2p^r. At a disk boundary Y!=0, the two displayed residuals are coprime, since M_e=Z M_(e-1)+(e-1)M_(e-2) and e<p. At strict level-r interiors for U_0, C_0 is exact J=W(p^r), since M_2(0)=1 and no prefix factor Y occurs.

The additionally required full-disk bound

    B'>=E                                                     (4.2)

does not assume any special upper prefix. For clarity, the accepted two-middle Section 8 proof extends without changing a step: put F(x)=R_ell(U)-R_ell(U-x). An ordinary H_(U-1)' term has h+delta+2a=U-1, and (4.2) is equivalent to

    F(delta+1+2a)-W(a)-V(delta)>=D/2.                    (4.3)

The general block inequality depends only on superadditivity:

    F(lD+v+2uD+2w)-W(uD+w)
      >=lR(D)+D[W(l)-l]+D[W(u)-u]+F0(v+2w)-W(w),

where F0(epsilon D)=epsilon R(D), and for 0<z<D,
F0(epsilon D+z)=epsilon R(D)+D-rho_ell+R(z-1).
Write delta+1=lD+v. For v=0 subtract V(delta)=1; the block part is >=R(D)-1>=D/2. For v=1 one has l>=1; after subtracting D V(l) the block part is >=R(D)-D>0, while the proper block contributes >=D/2. For 2<=v<D, the proper block contributes >=D/2+W(v-1)/2, strictly unless v+2w is a multiple of D. Since W(y)/2-V(y)>=-1/2 and scores are half-integral, strictness suffices. In the multiple case the only negative remainders have y=v-1 equal to 1 or p; then v is even, v+2w=2D, and the exact small-block expression minus V(y) is D+W(v/2-1)-V(y)>=D-p>=D/2. This exhausts every carry and endpoint. The omitted block terms are nonnegative.

The P transfer of (4.1)'s ordinary core derivative is off-root: its extra term has weight >=J+ell E_p>J+D/2-p. For the neighbor derivative the extra term has weight >=E. Thus (4.2) is also an original P bound, not a derivative of a reduced polynomial.

Finally the accepted general outside-cover proof yields (3.4): the complete monic root count makes v(H_U)=v(N_U) outside the cover; capped intervals of 2a+1 center distances have sum <=tau+T_ell(2a). The global digit-linear bound

    W(x)/2-R_ell(x)<=D/2-rho_ell

then gives B/C>=-D/2+rho_ell-tau. Factorization gives C'/C>=-tau; coefficientwise ordinary Gauss differentiation gives B'/C>=-D/2-tau. Tied radii and multiple maximizing centers are included. These estimates are used only near X=0, where the coordinate isometries apply.

## 5. The sparse-suffix carry lemma and deep actual tails

Write an arbitrary remaining suffix as

    m=sum even c_a p^(k_a)+dL, u=(m-1)/2, G=W(u).

Every base-p digit of u is <=h=(p-1)/2. Its digits below j are all h, and its j-th digit is (d-1)/2<=h-1. Above j the nonzero digits are c_a/2<=h. Therefore

    W(m-1)=2G, W(m)=2G+L,
    u mod p^b < (p^b-1)/2 for EVERY b>j.                (5.1)

These facts, not a restriction on the number of middle digits, are the necessary invariant. Let M be the largest power in m, so m<pM, and use a full disk at a scale D>=p^2 M. The deep cap (2.2) immediately gives P_m>=G+L.

For an ordinary H_m' term, (2.2), superadditivity, and the elementary exact scores

    V(2a+1)-W(a)<=p, equality only a=(p^2-1)/2,
    V(a)-W(a)<=0

show that the unique least term is h=0,delta=p^2,a=u-(p^2-1)/2. It exists and attains equality because j>=2 and u's bottom two digits are both h: subtraction of (p^2-1)/2 is carry-free, and W(u)=W(u-(p^2-1)/2)+p^2-p. Its scalar is nonzero and has value G+L-p. The extra term in (2.1) has weight >=G+L, so this is the original ordinary P_m' constant initial off roots.

For the actual first-deleted tail use the exact finite connection

    g_m^U=C_m^U sum_(ell=1)^m (-1)^(ell-1)q^(ell(ell-1)/2)
       P_(m-ell)(q)P_(ell-1)(q^-1)
       /[w_(m-ell)w_(ell-1)(1-q^(U+ell))],
    C_m^U=product_(a=1)^m(1-q^(U+a)).                   (5.2)

First set U=0. For odd ell=2x+1, both polynomial factors are even; the relevant score is

    W(u-x)+W(x)+V(2x+1)<=G+L.                         (5.3)

If b=ord_p(ell)<=j, superadditivity and V(ell)<=L suffice. If b>j, then for EVERY j<a<=b,

    x mod p^a=(p^a-1)/2 > u mod p^a.

Adding x and u-x to obtain u forces a carry at every such level. Thus the W defect is at least sum_(a=j+1)^b(p^a-p^(a-1))=p^b-L, proving (5.3). This is the new arbitrary-digit carry argument; it retains all intermediate nonzero even digits instead of replacing their residues by a constant.

For even ell=2x the floor-index score is

    W(u-x)+W(x-1)+V(ell)=W(u-x)+W(x)<=G.

Hence these terms start at weight G+L. Every possible weight-G term is odd-ell and has constant initial by (2.2). The full sum of these constants is nonzero, certified by the EXACT recurrence value

    g_m^0(0)=(-1)^u Q_u, v(g_m^0(0))=G.

Thus g_m^0 has exact constant value G on each full deep disk. Odd-ell products lose at most p-1 under ordinary differentiation. Even-ell products lose at most p but start at G+L. Consequently (g_m^0)'>=G-(p-1).

No full-lower-disk g-unit statement follows or is used. The accepted exact negative control m=171 at p=3 already disproves that statement on the larger k disk (weight 273, versus deep G=303).

## 6. Full lower disks: complete ordinary derivative initial

On level-k disks, M=p^k the largest power in m, digit linearity gives

    R_k(h)<=W(h)/2 for h<pM,
    equality exactly when h=bM.                        (6.1)

For every ordinary H_m' term h+delta+2a=m,

    R_k(h)+W(a)+V(delta)
      <=W(m-delta)/2+V(delta)
      <=G+V(delta)-W(delta-1)/2<=G+p.                  (6.2)

The final maximum is unique at delta=p^2. It is crucial that the second step is superadditivity, not a false endpoint-reflection identity.

If m=cM+a0 with c even and lower suffix a0>0 odd, equality in ALL steps occurs exactly at

    delta=p^2, h=bM for b=0,2,...,c,
    a=(c-b)M/2+(a0-p^2)/2.                            (6.3)

The arbitrary lower suffix causes no missing carry: u0=(a0-1)/2 has bottom j half-digits and all other digits <=h, so subtracting (p^2-1)/2 and doubling the result are carry-free. Conversely (6.1), the unique delta maximum, and parity force precisely (6.3).

Put A0=(a0-p^2)/2, omega^2=w_M and Z=N_M/omega. The normalization

    S0=w_(a0) omega^c/[Q_A0(1-q^(p^2))]

has value G+L-p. ALL equality terms sum, using actual factor units,

    w_m/(w_M^c w_(a0))->c!,
    w_(bM)/w_M^b->b!,
    Q_(vM+A0)/(Q_A0 w_M^v)->2^v v!,
    H_m'/S0 -> M_c(Z).                               (6.4)

Every factorial is a nonzero residue since c<p. In the terminal case m=dL (M=L), the already proved terminal-cap equality set instead gives the full derivative initial M_(d-1)(Z) at the SAME weight G+L-p. Both residual indices c and d-1 are even and <p, hence their constants

    M_(2v)(0)=(2v)!/(2^v v!)

are nonzero. Therefore P_m' is exact G+L-p on every STRICT lower-disk interior, but not in general on its boundary.

For the off-root transfer, P_m>=W(m)/2=G+L/2 and v(m)=j E_p, so the discarded term has weight >=j E_p+G+L/2>G+L-p. Thus (6.4) is genuinely an ordinary P derivative initial.

For g_m^0 on full lower disks, apply (6.1) to both factors of (5.2). Superadditivity gives W(m-ell)+W(ell-1)<=W(m-1)=2G, and V(ell)<=M. Consequently

    g_m^0>=G+L-M,
    (g_m^0)'>=G+L-M-rho_k.                            (6.5)

The derivative is an ordinary coefficientwise Gauss bound. We do not assume g_m^0 is a unit, and we do not divide by it.

## 7. Actual prefix shifts, with errors paid

For any prefix U_i, V(U_i)=D_i, while every nonzero tail index has V(a)<=M_i<D_i. Therefore v(1-q^(U_i+a))=V(a), and

    eta=C_m^U/w_m, v(eta-1)>=D-M.

Use the genuine f connection, as well as (5.2):

    f_m^U=C_m^U sum_(a=0)^m [(1-q^U)/(1-q^(U+a))]
       (-1)^a q^(a(a+1)/2) P_(m-a)(q)P_a(q^-1)
       /[w_(m-a)w_a],                                (7.1)

with the a=0 ratio equal to 1. Write f=eta P_m+Delta_f and g=eta g_m^0+Delta_g. The f correction has the exact extra value D-V(a); the reciprocal difference in g has value D-2V(ell). No internal tail endpoint is omitted.

On full lower disks, (6.1) and superadditivity give

    Delta_f>=G+L/2+D-M,
    Delta_f'>=G+L/2+D-M-rho_k,
    Delta_g>=G+L+D-2M,
    Delta_g'>=G+L+D-2M-rho_k.                         (7.2)

On full upper disks the deep estimates improve these to

    Delta_f>=G+L+D-M,
    Delta_f'>=G+L+D-M-p,
    Delta_g>=G+L+D-2M,
    Delta_g'>=G+L+D-2M-p.                             (7.3)

The bounds follow termwise in both orientations from the original finite connections; no inverse-parameter sign guess is needed because only error lower bounds are used. Here D>=p^2 M, L<=M and rho_k<M/p, so all error gaps above the retained derivative or constant initials are strictly positive. In particular D-M-L/2-rho_k+p>0, and L+D-2M-1>0. The unit eta has initial 1 and is independent of X. This proves every part of (3.2)-(3.3) for the ACTUAL shifted continuants, uniformly in prefix length and coefficients.

## 8. Every core-scale boundary and the deepest interior

Fix i and abbreviate J=T_(e_i)(U_i), D=D_i, G=G_i, C=C_i, B=B_i, f=f_i, g=g_i and b=1-q^(U_i), v(b)=D. At a P_n root,

    fC=bgB,
    P_n'=f'C+fC'-bg'B-bgB'.                          (8.1)

On a level-e_i boundary Y!=0. If the core residual M_e(Z) vanishes, its original neighbor is exact J-D/2 by coprimeness; g is exact G. Thus f,C are nonzero. Put delta=v(f)-G>=L and gamma=v(C)-J>=0. The root identity gives delta+gamma=D/2. The f'C term is exact G+L-p+v(C), while the lower gaps of the three competing terms are

    2delta-L, delta-L+1, delta-L+p.                   (8.2)

All are positive, including coincident prefix/tail residual classes. The neighbor derivative bound (4.2) is indispensable for the last gap.

If the core residual does not vanish, C is exact J; direct comparison gives gaps

    D/2, D/2-L+1, D/2-L+p,                            (8.3)

again strictly positive since L<=M<=D/p^2. This branch also includes f=B=0, without division by either.

For strict interiors of the deepest level r, choose i=0. The leading-two core C_0 is exact W(p^r), and (8.3) applies unchanged. Thus every core-scale boundary and every deepest strict-interior root is simple.

## 9. Every adjacent-scale annulus

Between adjacent levels e_i>e_(i+1), let a root be in a strict lower-disk interior but outside all CLOSED upper disks. Put rho=rho_(e_i), sigma=rho_(e_(i+1)) and let tau be its maximum upper-center distance valuation. Nesting gives

    sigma<tau<rho.

The full-lower estimates and exact strict-interior derivative give

    g>=G+L-M, g'>=G+L-M-sigma, f' exact G+L-p.

The complete prefix cover gives (3.4); C is an analytic unit in the relevant local disk. From f=bgB/C,

    v(f)>=G+L-M+D/2+rho-tau.

Divide (8.1) ONLY by C. The f' term is exact, and the three other lower gaps are

    D/2-M+p+rho-2tau,
    D/2-M+p+rho-tau-sigma,
    D/2-M+p-tau.                                    (9.1)

All are positive because M<=D/p^2, rho<D/p, and p>=3 imply M+rho<D/2. This proof covers every annulus independently of the number of nonzero prefix or suffix digits. It neither requires prefix simplicity nor assumes g nonzero at arbitrary points.

## 10. Complete root ledger and conclusion of the induction

Apply the accepted arbitrary-prefix terminal cap at the OUTERMOST level j directly to n, with terminal odd digit d. Each of the beta_j disks has n/beta_j roots counted with multiplicity, and these exhaust degree n. On their boundaries, the complete root/ordinary-derivative residuals M_d and M_(d-1) are coprime after removal of the nonzero Y factor. Thus exactly (d-1)L outer-boundary roots are simple. No count at a deeper scale is inferred from a coincident residual factor.

Every remaining root is in a strict outer j interior. The disjoint exhaustive partition is:

1. For each i=0,...,t: the strict level-e_(i+1) interiors outside the closed level-e_i cover (all annuli).
2. For each i=0,...,t: the boundaries of the level-e_i disks.
3. The strict interiors of the level-r disks.

Disjoint nesting makes this a finite exhaustive partition for every t. Sections 8-9 settle every class. This proves P_n squarefree without assuming any unproved even-prefix squarefreeness theorem. This is the induction: each added even digit inserts one boundary stratum and one annulus, governed by exactly the same invariant, while the terminal outer count and deepest interior stay valid.

Consecutive ORIGINAL P_n,P_(n-1) are coprime because every recurrence edge below n is nonzero; a common zero would propagate to P_0=1. Hence the original ordinary algebraic-square CD identity proves kernel nonvanishing at every root. Modulo the maximal ideal P_n=X^n, so its roots reduce to zero and are not +/-2. H_n(0)=1, and the unit local coordinate changes in (2.1) transfer multiplicity and original derivative nonvanishing to H_n. An algebraic p-adic embedding (or Galois conjugacy) gives every characteristic-zero primitive phase.

## 11. Controls, review boundary and costs

The uniform argument is Sections 3-10. Fresh controls.py checks the new sparse digit/carry invariant, derivative equality sets and scalar factorial units, full/deep g score bounds, arbitrary-prefix neighbor derivative scores, and shift/dominance margins. It neither executes nor imports any prior scientific program. Its output is only a falsification/transcription control, never a substitute for the unbounded proof. Source-bound inherited negative controls remain warnings, not new independent numerical evidence.

Normal and optimized outputs are byte-identical and pass 3,393,468 explicit checks. The growing-length controls include 0, 1, 2, 3, 6 and 12 even middle digits. An exact out-of-scope negative control has p=3, m=819, ell=243: the deep g score is 1824, above G+L=1662. This rejects dropping the even-digit invariant; it does not disprove squarefreeness outside the theorem. Counts and hashes are recorded separately. No cyclotomic root census or arbitrary-degree computational proof is asserted. A valuation sieve through b uses O(b) arithmetic and storage; naive recurrence coefficients use O(n^2) coefficient-field operations and O(n) live coefficients. Those bounds do not price coefficient representation, bit growth, precision, factorization or roots, and no algorithmic improvement is claimed.

Scientific acceptance must be independently bound to final bytes. Publication, table credit and any scope aggregation belong only to the designated parent/publisher after that review. Until then this is an unaccepted unbounded induction candidate, not accepted new coverage.
