# F020: an adjacent terminal-gap theorem and the remaining deeper boundary lemma

23 October 2026 UTC. Original candidate for independent review. This packet neither accepts nor publishes itself. No frozen accepted file was modified, and no historical or author-supplied scientific program was run or imported.

## 1. Exact result, novelty boundary, and open scope

The proposed new theorem is the following unbounded adjacent-scale family:

    p any odd prime; c even, 2<=c<p; d odd, 1<=d<p;
    r>=5, s>r; q any characteristic-zero primitive p^s-th root;
    n=2p^r+c p^3+d p^2.

Then the ORIGINAL recurrence polynomial P_n and Rogers–Szegő polynomial H_n are squarefree, and the ORIGINAL ordinary algebraic-square Christoffel–Darboux kernel is nonzero at every P_n root. Here

    P_0=1, P_1=X, P_(a+1)=X P_a-(1-q^a)P_(a-1),
    H_a(z)=sum_b [a choose b]_q z^b,
    w_a=product_(v=1)^a(1-q^v),
    sum_(a<n) P_a(xi)^2/w_a=P_n'(xi)P_(n-1)(xi)/w_(n-1).

Derivatives are ordinary characteristic-zero derivatives taken BEFORE reduction. The neighbor is the actual P_(n-1), never an associated-tail substitute. No absolute-square kernel is substituted.

This is not another separated-digit case: its two lower exponents differ by ONE. The family is unbounded in p,r,s and includes every legal c,d. Minimum n is 549 (p=3,r=5,c=2,d=1). It is NOT the full requested adjacent domain k>=3: the theorem here is k=3. Section 9 isolates the only remaining obstruction to the same argument for every k>=4, without calling that obstruction a multiple root.

Subtract every inherited high-order deflation, fixed-degree, and separately successful residual certificate before assigning incremental credit. In particular, for n=2u+1 the already-certified condition is phi(p^s)>C_u, where

    a_h=floor(u/h), b_h=((h+1)/2)a_h+floor(a_h/2),
    kappa=u+3floor(u^2/4)+2floor(u/4),
    C_u=u(u+1)(2u+1)/3-ceil(u/2)-kappa
        -sum_(odd 3<=h<=u) phi(h)b_h.

Thus incremental scope is only the displayed adjacent family outside EVERY earlier successful certificate, in particular phi(p^s)<=C_u. This is not a Catalan bound. Whole F020/F023 remain open. No historical priority, FFT, algorithmic speedup, bit-complexity, or numerical-stability claim follows.

## 2. Accepted dependencies and notation

The exact accepted sparse-induction report/review and the two-middle report/review and deep-cap bodies are bound in SOURCE_BINDINGS.json. They are read as mathematical sources, not executed programs. This is a selected mathematical dependency check, not a recursively complete archive audit.

Put t=q-1, v(t)=1 and E_p=v(p)=(p-1)p^(s-1). For legal nonzero indices set

    V(a)=p^ord_p(a), W(b)=sum_(a=1)^b V(a), W(0)=0,
    Q_b=product_(a=1)^b(1-q^(2a)), N_h(z)=product_(a=0)^(h-1)(z+q^a).

At level ell>=2 use beta_ell=p^floor(ell/2), D=p^ell and

    rho_ell=beta_ell/2                            (ell even),
    rho_ell=(2p-1)p^(floor(ell/2)-1)/2            (ell odd),
    T_ell(b)=sum_(a=1)^b min(V(a),rho_ell), R_ell=W-T_ell.

There are beta_ell disjoint disks, H-centered at -q^a, and the matching X-centered disks through X=v0+v0^-1, z=v0^2, v0 near i. These coordinates are analytic isometries with unit derivatives. Higher-level disks lie strictly inside lower-level disks, including a gap of ONE: rho_(ell+1)>rho_ell, and matching centers differ with value at least beta_ell>rho_ell. Both q orientations use the same X disks.

For the theorem set

    j=2, k=3, L=p^2, M=p^3, N=p^r, A=2N+cM,
    a0=dL, m=cM+dL, G0=W((dL-1)/2), G=W((m-1)/2),
    sigma0=rho_2=p/2, sigma=rho_3=(2p-1)/2.

The proof of the new cap below is also valid for j=k-1>=2, L=p^j,M=pL. Let

    lambda=L/(2p).

Legality is explicit: n<2N+pM<3N<=pN<=p^s, with strict n<pN also at p=3, because pM<=N/p. Therefore all recurrence edges and every finite-connection denominator used below are nonzero. No total weight is assumed below E_p.

We use the exact finite Newton identities and paid off-root chain rule from the accepted sources:

    H_b=sum_(h=b mod2) w_b N_h/[w_h Q_((b-h)/2)],
    H_b'=sum_(h+delta+2a=b,delta>=1)
       w_b z^(delta-1)N_h/[w_h Q_a(1-q^delta)],
    H_b'(v0^2)=v0^(b-2)[(b/2)P_b+(v0-v0^-1)P_b'/2].       (2.1)

Original associated continuants F=f_(dL)^A and H=g_(dL)^A satisfy

    P_n=FC-b_A HB, C=P_A, B=P_(A-1), b_A=1-q^A, v(b_A)=M.  (2.2)

The two finite connections are exactly those in accepted two-middle (2.4). In particular for U=0,

    g_m^0=w_m sum_(ell=1)^m (-1)^(ell-1)q^(ell(ell-1)/2)
      P_(m-ell)(q)P_(ell-1)(q^-1)
      /[w_(m-ell)w_(ell-1)(1-q^ell)].                   (2.3)

We do not transplant the separated deep-cap estimate onto an adjacent disk.

## 3. Replacement adjacent cap, including its actual residual

For a general adjacent pair k=j+1>=3 and every 0<=h<M=p^(j+1),

    R_k(h)-W(floor(h/2))<=lambda=L/(2p),
    equality holds EXACTLY at h=L.                     (3.1)

Proof. Let S(h)=W(h)/2-R_k(h), digit-linear. Every digit-basis weight below k is positive. If a>=floor(k/2),

    S(p^a)=(k-a)(p-1)p^(a-1)/2;

below that range S(p^a)=W(p^a)/2. If h>=2 has highest digit index a and h=2u+epsilon, the exact floor formula gives

    W(h)-2W(u)<=p^a.

If a<floor(k/2), R_k(h)=0 and there is no positive defect. Otherwise

    R_k(h)-W(u)<=p^a/2-S(h)<=p^(a-1)/2<=lambda.

The first two inequalities can attain lambda only if a=j, the leading digit is 1, and every lower digit is zero, because all lower S-basis weights are strictly positive. Thus h=L is the unique candidate, and direct substitution gives equality. The cases h=0,1 have defect zero. This proves (3.1), including p=3 and both scale parities.

For the odd tail a0=dL, carry-free halves give W(a0)=2G0+L. Apply (3.1) to its Newton series and then superadditivity:

    weight(P_(dL))>=G0+L-lambda.                        (3.2)

There is EXACTLY ONE equality term, namely

    h=L, a=(d-1)L/2,
    H_(dL),initial = initial of w_(dL) N_L/[w_L Q_((d-1)L/2)]. (3.3)

The required addition W((L-1)/2)+W((d-1)L/2)=G0 is carry-free. On a level-k disk N_L has initial gamma_a Y^(L/beta_k) at its exact weight T_k(L), with gamma_a nonzero. This follows by counting the complete L/beta_k matching residue classes; every nonmatching factor has its fixed nonzero unit. Thus (3.3), with the exact scalar as written, retains every primitive phase. It is nonzero at EVERY k-boundary Y!=0, independently of the core residual. There is no guessed sum of unit coefficients.

For k=3 the residual is a nonzero scalar times Y^p, and

    weight(F)=G0+p^2-p/2 on each k boundary.            (3.4)

This is the actual adjacent residual replacing the false G0+L bound. It must NOT be formally differentiated after reduction: Y^p has zero residual derivative, while the ordinary derivative has the nonzero initial proved next.

## 4. Ordinary short-tail derivative, actual g-unit, and a new g' bound

The accepted terminal-level cap applies to the unshifted dL tail on FULL j disks. It gives ordinary derivative initial M_(d-1)(gamma Y^(L/beta_j)) at weight G0+L-p. Its constant is nonzero because d-1 is even and <p. Since a full k disk lies in a STRICT j interior,

    P_(dL)' has exact constant initial at G0+L-p there. (4.1)

The off-root term in (2.1) has weight at least j E_p+G0+L/2>G0+L-p, and is therefore paid, not discarded by a root assumption.

The unshifted g_(dL)^0 on a full j disk has weight >=G0, and its residual has nonzero constant on each strict j interior. Here is the retained endpoint mechanism, also proved in accepted two-middle Section 9. The half-W Newton bound and (2.3) make the term score at most G0+L; equality requires ell=bL. At Y=0 only odd b can contribute a constant: the two polynomial indices are then even, and their h=0 terms give the same constant, up to their explicitly retained nonzero coordinate units, on every disk. Even b terms have positive Y degree. The entire constant sum is certified by the exact recurrence value

    g_(dL)^0(0)=(-1)^((dL-1)/2) Q_((dL-1)/2), of value G0.

Thus g_(dL)^0 is a unit of exact value G0 on every full k disk. This argument does not need a gap of two.

The genuinely new ordinary-derivative bound on FULL k disks is

    (g_(dL)^0)'>=G0.                                   (4.2)

Proof by the full differentiated finite connection, before reduction. In a term where the first polynomial factor is differentiated through its H-derivative part, put

    h+delta+2a=dL-ell, t+2b=ell-1.

The other differentiated factor is identical after interchanging roles. The possible score is

    R_k(h)+R_k(t)+W(a)+W(b)+V(delta)+V(ell).

Every h,t<dL<M. Their S values are nonnegative half-integers, positive unless the index is zero. Superadditivity gives

    score <= G0-W(delta)/2-S(h)-S(t)+V(delta)+V(ell).

Now W(delta)/2-V(delta)>=-1/2, and its negative cases are ONLY delta=1,p. These are odd; then h+t is odd, so at least one of h,t is positive and S(h)+S(t)>=1/2. For even delta the elementary difference is nonnegative. In both cases score<=G0+V(ell)<=G0+L. Since W(dL)=2G0+L, the asserted derivative lower bound follows termwise.

The off-root P term from each factor's chain rule also has weight >=G0: its integer coefficient has nonnegative value, and the undifferentiated product estimate just used already gives that bound. The q^-1 orientation has exactly the same weights on the same disks. Hence (4.2) is an original ordinary P derivative estimate, not formal differentiation of a constant residual.

For the actual shift U=A, V(A)=M and every nonzero tail index has V<=L. The exact connections give eta=C_(dL)^A/w_(dL) with eta-1>=M-L and

    F=eta P_(dL)+Delta_F, H=eta g_(dL)^0+Delta_H,
    Delta_F>=G0+M-L/2, Delta_F'>=G0+M-L/2-sigma0,
    Delta_H>=G0+M-L, Delta_H'>=G0+M-L-sigma0.           (4.3)

These are full-j bounds and hence hold on full k disks. They follow respectively from the exact extra f ratio of value M-V(a) and reciprocal difference of value M-2V(ell), not an unshifted proxy. Since M=pL, p>=3 and sigma0<L/2, all errors are strictly above the retained weights. Thus for EVERY adjacent j>=2:

    F>=G0+L-lambda, exact on every k boundary;
    F' exact G0+L-p with constant initial;
    H exact G0; H'>=G0                                  (4.4)

on the full k disks. This replaces, rather than assumes, the old separated deep invariant.

## 5. All k=3 core boundaries, including coincident residual classes

The accepted arbitrary-prefix terminal cap for the EVEN core A gives, on every full k disk,

    J=T_k(A), E=J-M/2,
    C>=J, C'>=J+M/2-p, B>=E, B'>=E,
    C_initial proportional to Y^(2N/beta_k) M_c(Z),
    B_initial proportional to Y^(2N/beta_k) M_(c-1)(Z),
    Z_initial=gamma_a Y^(M/beta_k), gamma_a!=0.         (5.1)

Its complete cover and the original neighbor derivative bound are accepted general-prefix results, not assumptions of core simplicity. M_c and M_(c-1) are coprime because c<p. Off-root chain terms in (5.1) are paid in the source proofs, including B'.

At any original P_n root on a k boundary,

    FC=b_A HB,
    P_n'=F'C+FC'-b_A H'B-b_A HB'.                     (5.2)

If M_c(Z)=0, then B has exact E. Both H and F are nonzero by (4.4), so C is nonzero too. Put delta=v(F)-G0 and gamma=v(C)-J. The actual boundary residual gives delta=L-lambda, and the root equation gives delta+gamma=M/2. The F'C term is exact. The three other terms lie above it by at least

    2delta-L=L-2lambda,
    delta-L+p=p-lambda,
    delta-L+p=p-lambda.                              (5.3)

For j=2, lambda=p/2, these are respectively p^2-p,p/2,p/2, all STRICTLY positive, including p=3. No residual coincidence is discarded: even on M_c(Z)=0 the tail residual (3.3) is nonzero at Y!=0, and no division by a potentially zero residual is taken.

If M_c(Z)!=0, C is exact J, and the direct three gaps are

    M/2-lambda, M/2-L+p, M/2-L+p,                    (5.4)

again strictly positive. This branch does not divide by B and includes B=0. Thus every k=3 boundary root is simple.

## 6. Strict k interiors: what survives unchanged and why

Use the leading-two prefix 2N and the full suffix m=cM+dL, whose half-digits are all <=(p-1)/2. Its strict carry deficit above j is unchanged by adjacency:

    W(m-1)=2G, W(m)=2G+L,
    ((m-1)/2) mod p^b < (p^b-1)/2 for every b>j.

Therefore the accepted sparse-suffix carry argument applies on the full r disks, because r>=k+2 still makes every m-index lie in the PROVED deep-cap range. It gives genuine shifted-tail bounds

    f>=G+L, f' exact G+L-p, g exact G, g'>=G-(p-1).

On full k disks the accepted half-W argument uses only the balanced half-digits, not a k-j gap. Its complete ordinary f' equality set is delta=p^2, h=bM for b=0,2,...,c, and a=(c-b)M/2+(dL-p^2)/2. Its full initial is M_c(Z); hence f' is exact G+L-p on STRICT k interiors. The weak bounds remain g>=G+L-M and g'>=G+L-M-sigma. Outer shift errors are paid because N>=p^2 M. The same off-root correction bound j E_p+G+L/2>G+L-p holds.

Consequently the accepted leading-two r-boundary and deepest-interior comparisons go through: their gaps use N/2-L, which remains positive for L=M/p and N>=p^2M. In the k/r annulus the three gaps are

    N/2-M+p+rho_r-2tau,
    N/2-M+p+rho_r-tau-sigma,
    N/2-M+p-tau.

They are positive because M+rho_r<N/2, independently of L. Only the leading-two core is divided out; no g-unit assertion on full k disks is introduced. This proves every strict-k-interior root simple for the proposed adjacent family.

## 7. The j/k annulus also survives adjacency

On full j disks the actual small tail has H>=G0, H'>=G0-sigma0 by ordinary Gauss differentiation, and F' is exact G0+L-p on strict interiors. The errors (4.3) remain strictly higher with M=pL. For the even core A, the accepted outside-cover ratios give

    C'/C>=-tau,
    B/C>=-M/2+sigma-tau,
    B'/C>=-M/2-tau,
    sigma0<tau<sigma.

At a root, divide (5.2) ONLY by C. The three gaps over F' are

    M/2-L+p+sigma-2tau,
    M/2-L+p+sigma-tau-sigma0,
    M/2-L+p-tau.

For k=3 all exceed M/2-L+p-sigma=p^2(p-2)/2+1/2>0. This proves the entire annulus, including tied nearest centers already retained by the ratio lemma. In fact the same positivity holds at every adjacent k>=3 since rho_k<L/2 and M=pL.

## 8. Root ledger, original neighbor, kernel, and phase scope

The accepted terminal-j cap applied directly to n counts every root with multiplicity in its complete j cover. On j boundaries, M_d and M_(d-1) are coprime away from Y=0, giving exactly (d-1)L simple boundary roots. No allocation among deeper coincident residual classes is inferred.

The remaining roots lie in exactly one of: the j/k annulus; a k boundary; a strict k interior. Sections 5–7 settle each class for k=3. The strict k interiors have the accepted complete partition into the r cover and its outside. This is an exhaustive ledger, not a finite root census.

Consecutive original P_n and P_(n-1) are coprime because their legal recurrence edges are nonzero; a common root would propagate to P_0=1. Therefore the unchanged original ordinary CD identity gives nonzero algebraic-square kernel at every root. Modulo the maximal ideal P_n=X^n; its roots reduce to zero and are not +/-2. H_n(0)=1, and the exact identity H_n(v0^2)=v0^n P_n(v0+v0^-1) with unit coordinate derivatives transfers multiplicity. An algebraic p-adic embedding, or Galois conjugacy, supplies EVERY characteristic-zero primitive phase.

## 9. Exact remaining lemma for adjacent k>=4

The replacement invariant (4.4), strict-k proof, j/k annulus, outer ledger, and the C-unit boundary branch all remain valid for general j=k-1>=2. The sole unsettled location class is a k boundary with M_c(Z)=0. There

    delta=L-lambda, gamma=M/2-L+lambda,
    v(F'C)=G0+J+M/2+lambda-p,
    v(FC')-v(F'C)>=L-2lambda>0.

Let the ACTUAL two remaining derivative terms be combined as

    K=b_A (H'B+HB').

A precise sufficient remaining local lemma is: at every original P_n root in this location class, either

    v(K)>G0+J+M/2+lambda-p,

or v(K) is strictly smaller than that displayed value; or, at equality, its leading term does not cancel the leading term of F'C. A more permissive but still precise sufficient local lemma is

    v(F'C-K)<G0+J+M/2+lambda-p+(L-2lambda).

The right side is the proven lower bound for v(FC'), so this strict inequality proves that adding FC' cannot cancel the nonzero initial. Mere nonvanishing of F'C-K without this valuation control would not suffice.

All ordinary chain-rule terms must be included in this K. The proven separate bounds give only v(K)>=G0+J+M/2, which is insufficient once lambda>p (every j>=3). In particular transplanting B'>=E, H'>=G into a false positive-margin argument fails by the explicit deficit lambda-p.

This is a cancellation problem of ACTUAL residuals at an actual root equation, not a proof of a characteristic-zero collision. It may be resolved by sharper core/neighbor residuals, by a combined derivative identity, or by an exact obstruction. None is claimed here. The k=3 theorem succeeds because p-lambda=p/2>0, not because the old deep cap miraculously survived.

## 10. Controls and acceptance boundary

Fresh controls are independently authored for this candidate and import no prior scientific program. They check the exact adjacent-cap equality, short-tail Newton equality, ordinary g' convolution score and its parity compensation, actual central-disk residuals, paid shift errors and both boundary margin branches. Normal and optimized outputs are byte-identical and pass 1,968,130 explicit checks; hashes are recorded separately. Finite controls are transcription/falsification evidence, never the uniform proof, which is Sections 2–8.

Exploratory formal-t recurrence outputs are explicitly limited to the small weights below v(p) of the selected legal s; they are not a general characteristic-zero multiple-root or squarefreeness test. The actual phase-uniform theorem is proved with finite identities over the characteristic-zero valuation field, not inferred from these reductions.

No fixed-N census, historical-code execution, algorithmic improvement, or exact coefficient bit-cost claim is made. Scientific acceptance requires an independent review bound to final bytes. Publication and table credit belong only to the designated publisher after that review; accepted separated packets remain untouched.
