# Uniform exponent extension: n = 2p^r + cp

21 October 2026 UTC. Author candidate requiring separate independent verification. No source program was executed. No external, repository, or table state was changed. This candidate does not accept itself.

## 1. Statement, scope audit, and exact ledger

Let p be any odd prime, r>=3, s>r, 1<=c<p, and q any characteristic-zero primitive p^s-th root. Keep the ORIGINAL definitions

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_b(z)=sum_k [b choose k]_q z^k,
    w_j=product_(u=1)^j(1-q^u), w_0=1,
    n=2p^r+cp.

Then P_n and H_n are squarefree and, at every P_n root xi,

    sum_(j=0)^(n-1) P_j(xi)^2/w_j != 0.

This is a uniform exponent extension. The ENTIRE r=3 family is inherited from the accepted even/odd middle-digit source pair, including all c, and receives no new credit here. Relative to the inspected accepted source chain, the added sector is every r>=4 with 1<=c<p. The accepted one-leading-digit/short-tail map covers 2p^r+d only for d<p, not d=cp; the first-two-digit family has degree below p^2, not arbitrary occupied positions. Pure powers, leading digits, adjacent/low-tail results, bounded small-prime and fixed-order certificates, and conditional guards do not establish this extension. This is a bounded source audit, not an exhaustive literature or novelty claim.

In an algebraic p-adic embedding set t=q-1, v(t)=1, e=v(p)=(p-1)p^(s-1), and

    N=p^r, B=r(p-1)p^(r-1)/2, h0=floor(r/2),
    beta=p^h0, L=N/beta,
    rho=beta/2 if r is even,
    rho=p^(h0-1)(2p-1)/2 if r is odd,
    K=N+2B, E=N/2+2B, D=N+E-p,
    m=(p-1)/2, sigma=p-1/2, eta=(p+1)/2,
    alpha=1-1/(2p), F=c(p-1/2),
    x_a=i(q^(a/2)-q^(-a/2)), i^2=-1, 0<=a<beta,
    D_a={v(X-x_a)>=rho}.

Square roots of q^a are chosen near 1. Notice beta is p^floor(r/2), not p^ceil(r/2); rho depends on the parity of r, and sigma is a separate FIXED radius. We have eta<sigma<=rho, sigma<p, and p^(h0-1)<rho.

For EVEN c the disjoint exhaustive ledger is:

- Exactly 2L high boundary roots in each of the beta old disks D_a, totaling 2N; every original derivative has value D+F.
- Exactly cp outer roots of X-value alpha, p in each of the c distinct nonzero residue locations of He_c(Y^p). Their derivative value is 2N alpha+F-1/2.
- No exact zero: v(P_n(0))=K+F.

For ODD c put W=(c-1)(2p-1)/2. The disjoint exhaustive ledger is:

- Exactly 2L high boundary roots in every D_a, totaling 2N. For p not dividing a their original derivative value is W+N+E-1. For p dividing a (INCLUDING a=0), it is W+N+E+m-x, where x=p^ord_p(a) if a!=0, and x=rho if a=0.
- One exact simple zero, strictly inside D_0, with derivative value K+W+p-1. It is not a high boundary root.
- Exactly p-1 separated inner roots, one per disk T_u={v(X-delta_u)>=sigma}, 1<=u<p. Here delta_u is the t-scale root of the EXACT shifted cp-tail with delta_u/t reducing to iu. It satisfies v(delta_u-x_u)=eta. These roots have X-value 1 and derivative value 3N-N/p+W+p-1.
- Exactly (c-1)p outer roots of X-value alpha, p in each of the c-1 nonzero residue locations of He_c(Y^p), with derivative value 2N alpha+F-1/2.

Thus the counts are 2N+cp in the even case and 2N+1+(p-1)+(c-1)p in the odd case, both equal to n. For odd c, the p-indivisible high centers number beta-beta/p, the nonzero p-divisible centers number beta/p-1, and the central center is one. No equal-leading-derivative obstruction or exception in the parity of r remains. No general finer radius for the p-fold outer classes is claimed.

## 2. Provenance and inherited full-disk inputs

The accepted r=3 author manifests are 6645bc9ce05b89a9b7276404d60d3024c8b4b261c4afb16470dbb64c2951e82d (even) and 4d0463cbbd22a5a527cd21794dc07a9071809fa5316d9b9d8b2f07a0c9930e15 (odd). Their accepting review manifests are 2dcac0183e6606661e345064b109530b9bc064b238b1059ea967c2e73c12b172 and ef2ecc602790a592a398296453c1a47520619b4aababca8d0819a17d4591b186. The combined accepted public archive has SHA-256 5e1a38d57dd21b1f04e24f48794b3afb099d3b115a7ee2b7052b88028ef2b3ae, and its detached packaging-audit archive has SHA-256 4265751372800018ada1e9e5ebabe3a722262212d1cb31a8e50a043efebd108d. Packaging acceptance supplies no additional theorem credit.

Fresh read-only source checks bind those exact source packages, the accepted general adjacent-criterion source pair, the inspected complete-map scope, and relevant documentary snapshots. Selected snapshots are not represented as complete copied packages. No supplied research/checking program is run.

The historical b=2p discrepancy remains unresolved: the retained report is 00a4ad13b0726205f3dd6515a4f4c6e9687622c738efdb3df39360b6bcf593db, whereas its historical review cites original author report 6b27fcbdc7aae652afae91fa9e1a8baf84270ef57af75c44c5f35288541686da. Those different bytes are not identified, recovered, or newly accepted here. The needed short whole-block argument is reconstructed below from the original recurrence.

Let A=P_(2N), M=P_(2N-1), a0=1-q^(2N). The accepted general leading-two full-disk statements, genuinely valid for all r rather than extrapolated from r=3, give on each D_a coefficientwise Gauss weights

    A: K,  M: E,  A': D,  M': >=E.

The first three initial polynomials are nonzero scalar multiples of Zbar^2+1, Zbar, Zbar, with Zbar=gamma_a Y^L and gamma_a!=0. On the residual locus Zbar^2+1=0 the M and ORIGINAL ordinary A' values are exactly E,D. These are off-old-root statements, so they apply to the new roots below. The inherited result gives precisely 2L boundary roots of A per D_a and v(A(0))=K. All A roots have positive X-value at least 1. Mutual center distance is

    v(x_a-x_b)=p^ord_p(a-b)<rho, a!=b.

No r=3 geometry is retained as an all-r assumption.

Legal specialization holds because

    n<=2p^r+p(p-1)<p^(r+1)<=p^s

for every p>=3,r>=3: the difference is (p-2)p^r-p(p-1)>0. Every used edge and q-factorial is nonzero, and v(1-q^j)=p^ord_p(j) for 1<=j<p^s. In particular v(a0)=N.

## 3. Exact shifted tails and their uniform short-block bounds

Put b_j=1-q^(2N+j), 1<=j<cp. Define f_0=1,f_1=X,g_0=0,g_1=1, applying the same continuant recurrence with edges b_j; set f=f_(cp),g=g_(cp). Exact induction gives

    P_n=f A-a0 g M.                                      (3.1)

Here g is the FIRST-vertex-deleted tail, not the last-deleted neighbor P_(cp-1). Its parity is opposite to f.

For the unshifted p-block, the elementary inherited coefficient identity is

    P_p=X^p+lambda X+J,
    v(lambda)=p-1, lambda/t^(p-1)->epsilon=(-1)^((p+1)/2),
    J odd of degrees 3,...,p-2, with coefficient values >=p-1. (3.2)

It follows by the original Gaussian-binomial/Laurent identity at precision below e and by ordinary differentiation before reduction. Each full p-block in f is shifted by 2N+ip, 0<=i<c. Changed edges have value >=p (N for i=0); telescoping a k-edge matching gives changed coefficient value >=p+k-1. Thus, for every full shifted block U,

    U(tY)/t^p -> S(Y)=Y^p+epsilon Y,
    weight_alpha(U)>=p alpha, initial Y^p,
    U'(r0 Y)/t^(p-1)->epsilon, v(r0)=alpha.             (3.3)

The ORIGINAL leading derivative term pX^(p-1) has value e+(p-1)alpha>p-1. Differentiated nonlinear terms and shifted errors are higher as well. It is not legitimate to differentiate Y^p after reduction in lieu of this calculation.

An endpoint-deleted p-block has p-1 vertices, weight m at every X-weight x>1/2, and normalized constant d=(p-2)!! or u=2^m m!, according to the deleted endpoint. Both are nonzero modulo p and du=-1. Its X^(2j) coefficient has value >=m-j and its derivative weight is >=m-1+x. A doubly endpoint-deleted block has weight >=m-1+x and derivative weight >=m-1. These are direct matching bounds; each even constant has a unique perfect matching. Joining edge ip has value p and residue -i after division by t^p.

For a selected joining subset J let j=|J| and a be the number of adjacent pairs. Its t-scale weight is at least

    cp-j+a(m+1),

because there are a doubly cut, 2j-2a singly cut, and c-2j+a intact blocks. The number of joining runs is j-a<=floor(c/2). Consequently:

EVEN c: with F=cp-c/2, the unique least matching is the perfect matching {1,3,...,c-1}, with residue He_c(0)=(-1)^(c/2)(c-1)!! !=0. Therefore for every X-weight x>=1,

    weight(f)=F, constant nonzero initial,
    weight(f')>=F-2+x,
    weight(g)>=F-m-1+x, weight(g')>=F-m-1.             (3.4)

For the last two bounds, the shortened first block gives subset weight >=m+(c-1)p-j+(a+z)(m+1), where z records its incident joining edge and a counts doubly cut COMPLETE blocks; j-a-z<=c/2-1. This yields t-weight >=F-m, then odd parity gives (3.4). No unit is asserted for even-c g. Its possible leading residual involves the sum of products (-i) over maximum nonadjacent subsets of {2,...,c-1}; this vanishes, for example, at (p,c)=(5,4),(11,6). Such cancellation only improves the bounds.

ODD c: set h=(c-1)/2 and W=h(2p-1). Maximum nonadjacent joinings give

    f(tY)/t^(W+p)->C S(Y), C=He_c'(0)=(-1)^h c!! !=0,
    g(tY)/t^(W+m)->G=u*(-1)^h*2^h*h! !=0.             (3.5)

For g the unique least matching is {2,4,...,c-1}, with the first joining edge absent. This proves its unit rather than exchanging endpoints. Ordinary differentiation of the exact scaled integral polynomial, followed by reduction, gives throughout x>=1

    weight(f')=W+p-1, constant nonzero initial,
    weight(g)=W+m, constant nonzero initial,
    weight(g')>=W+m-1+x.                              (3.6)

Also f/X has weight W+p-1 with constant nonzero initial at every x>1. For g', its nonconstant t-scale coefficients are strictly higher than W+m and belong to the cyclotomic field with integer t-values; even parity then gives the stated bound. The derivative multipliers are not discarded before reduction.

## 4. Alpha residuals and all-r error bounds

Let T=P_(cp), and choose r0 with r0^(2p)=t^(2p-1). At X=r0Y every selected-joining subset has weight >=F+a delta, delta=(p^2-1)/(2p)>0. When a=0 its initial is product_(i in J)(-i) times Y^(p(c-2j)); the endpoint pairs contribute du=-1. Summing the matching expansion gives

    T(r0Y)/r0^(cp)->He_c(Y^p),
    T'(r0Y)/(t^(p-1)r0^((c-1)p))->epsilon He_c'(Y^p). (4.1)

For the second identity differentiate each original exact summand. Hitting an intact, singly cut, or doubly cut block has weight respectively >=F+a delta-1/2, F+a delta-1+alpha, or F+a delta-alpha. Every term with a>0 lies strictly above F-1/2, since even the smallest third-type gap is delta-alpha+1/2=m>0. At a=0 only intact-block derivatives survive. The derivative of He_c is in its OWN variable and is then evaluated at Y^p, not the zero derivative of the Frobenius composition.

He_c'=c He_(c-1), and consecutive Hermite polynomials are coprime modulo p by downward recurrence since c<p. Thus He_c has c distinct roots, all nonzero for even c, and exactly one zero for odd c.

Every edge of f differs from T by value N. Telescoping a k-edge matching gives difference coefficient value >=N+k-1. Minimizing at alpha>1/2 proves

    weight_alpha(f-T)>=Q,
    weight_alpha(f'-T')>=Q-alpha,
    Q=N+cp/2-1                           (c even),
    Q=N+(cp-3)/2+alpha                    (c odd).     (4.2)

Here Q>F and Q-alpha>F-1/2. Their derivative gaps are N-c(p-1)/2-3/2+1/(2p) in the even case and N-c(p-1)/2-1 in the odd case, both positive already for N>=p^3,c<=p-1. Therefore f has both residuals (4.1).

In particular, for odd c, its (c-1)p outer roots and p simple t-scale roots exhaust its degree. The latter are delta_u, 0<=u<p, with delta_u/t reducing to iu; S has precisely these simple roots. Oddness gives delta_0=0 exactly. The nonzero alpha classes are counted with multiplicity before simplicity is proved, not simple-root-Hensel lifted from He_c(Y^p).

## 5. A fixed-radius noncentral tail unit and displacement

For odd c only, put F1=(3p-1)/2. On the fixed disk v(X-x_u)>=sigma, 1<=u<p, the unshifted T=P_(cp) has coefficientwise weight W+F1 and constant nonzero initial. Here is a direct original-Newton proof. Write Vfac(j)=sum_(i=1)^j p^ord_p(i), j0=(cp-1)/2. The exact identity is

    H_b(z)=sum_(k=b mod 2) w_b N_k(z)/(w_k Q_((b-k)/2)),
    N_k(z)=product_(j=0)^(k-1)(z+q^j),
    Q_j=product_(u=1)^j(1-q^(2u)), v(Q_j)=Vfac(j).     (5.1)

The k=1 term has weight Vfac(cp)-Vfac(j0)=W+F1 and constant initial because v(z+1)=1. For k=2l+1, l>=1, use cp<p^2 and

    Vfac(k)=k+(p-1)floor(k/p),
    weight(N_k)>=k+(sigma-1)floor(k/p).

Its subtracted score is at most Vfac(j0)-l+floor((2l+1)/p)/2, strictly below Vfac(j0). Thus k=1 is uniquely minimal on the whole disk. The H/P coordinate map near i is an analytic isometry and preserves the lower bound and normalized constant unit.

At X-weight 1 the shifted difference f-T has weight >=N+(cp-1)/2. Its gap above W+F1 is N-(h+1)p+h>0. Hence f has that same fixed-disk unit. Using its complete monic factorization, the (c-1)p outer distances at x_u contribute W and the other p-1 t-roots contribute p-1. The one remaining distance is exactly

    v(delta_u-x_u)=W+F1-W-(p-1)=eta.                 (5.2)

For ANY old center a with p not dividing a, write u=a mod p, 1<=u<p. Its difference from x_u has value >=p>sigma (or it is identical). Since rho>=sigma, D_a lies in that fixed sigma disk. Thus on every such old disk

    weight(f)=W+F1, constant nonzero initial.         (5.3)

This is a geometric inclusion, not a substitution of the vanishing t-residue into a false unit estimate. At the remaining old centers p|a, x=v(X)>1 on a noncentral disk and x=rho on the central boundary; the linear f/X unit from (3.6) applies.

## 6. The genuinely all-r eta-neighbor carry lemma

On every H disk v(z+q^u)>=eta, and hence the corresponding P disk, we prove

    weight(M)>=E_eta=3N-N/p-p^2.                     (6.1)

This is NOT obtained by replacing p^3 by N in the old r=3 estimate. Let b=2N-1, k=2l+1, 0<=l<N. Since 1<eta<p, the consecutive-product lower bound is

    T_eta(k)=k+(eta-1)floor(k/p), R_eta(k)=Vfac(k)-T_eta(k).

The subtracted Newton score is R_eta(2l+1)+Vfac(N-1-l). Digit reflection gives Vfac(N-1-l)=Vfac(N-1)-Vfac(l). Write l=sum_(j=0)^(r-1) a_j p^j; let eps_j be the carries in 2l+1, with incoming eps_(-1)=1. Direct substitution of Vfac(p^j)=p^j+j(p-1)p^(j-1) gives the exact score difference

    R_eta(2l+1)-Vfac(l)
      =-a_0-p a_1-p a_2
       +sum_(j=3)^(r-1) p^(j-1)[(j-2)p-(j-1)] a_j
       +m eps_0+sum_(j=1)^(r-1)(p-1)p^j eps_j.        (6.2)

Every high-digit coefficient j>=3 and every high carry coefficient is strictly positive. Replacing each high digit by p-1 maximizes it and forces its carry to one regardless of incoming carry. Thus every maximum has a_j=p-1 for j>=3, and the high contribution is independent of the low incoming choice.

For fixed low carry pattern (eps_0,eps_1,eps_2), the negative low-digit coefficients force the least feasible digits:

    a_0=m eps_0,
    a_1=(m+1-eps_0) eps_1,
    a_2=(m+1-eps_1) eps_2.

Their low score is

    p[(m-1+eps_0)eps_1
      +(p(p-1)-m-1+eps_1)eps_2].                     (6.3)

Its unique maximum is p^2(p-1), attained at all three carries equal to one, hence a_0=a_1=a_2=m. To see uniqueness directly, eps_2=0 gives at most pm; with eps_2=1 the positive gain forces eps_1=1 and then eps_0=1. The strict inequalities hold also at p=3.

Therefore the unique full score maximizer is

    l*=N-(p^3+1)/2, k*=2N-p^3.                       (6.4)

At r=3 this is k*=N; at every r>3 it is NOT N. Put j*=(p^3-1)/2 and B3=3(p-1)p^2/2. Reflection of the edge valuations gives

    Vfac(2N-1)-Vfac(k*)=Vfac(p^3)-p^3=2B3,
    Vfac(j*)=B3,
    T_eta(k*)=(2N-p^3)(3p-1)/(2p).

Subtracting the maximal score gives B3+T_eta(k*)=3N-N/p-p^2, proving (6.1). This is a coefficientwise lower bound; no uncancelled equality for M is claimed or needed. The unique maximum is a statement about the exact lower-bound score, not an assertion that its analytic residual cannot cancel.

The carry proof is valid for all r and uses no finite-grid inference. It is the main place a blind r=3 substitution would give a wrong extremizer and an unjustified sharp bound.

## 7. High roots and zero for even c

On D_a take x=p^ord_p(a) for a!=0 and x=rho for a=0 in the Gauss bounds. The principal fA has weight F+K. The correction a0gM has lower weight N+F-m-1+x+E and exceeds the principal by N/2-m-1+x>0. Thus P_n has the same degree-2L boundary residual as a scalar unit times A in every old disk. It has exactly 2L boundary roots there and no strict-interior root, counted with multiplicity before simplicity.

At each such new root v(M)=E, v(A')=D. Since f is a unit, use A=a0gM/f and differentiate (3.1) in characteristic zero:

    P_n'=f A'+f' A-a0g'M-a0gM'.                     (7.1)

The first term has exact value F+D. The other three terms have lower values N+E+F-m-3+2x, N+E+F-m-1, and N+E+F-m-1+x. Their gaps are m-2+2x, m, m+x, all strictly positive for x>=1,m>=1. Therefore every high derivative has exact value D+F, including every p-divisible center introduced when beta>p. Possible g cancellation only helps.

Both g and M are odd, so P_n(0)=f(0)A(0) exactly, with finite value F+K. There is no zero or missing central root.

## 8. High roots and exact zero for odd c

At p-indivisible old centers, (5.3) gives principal fA weight K+W+F1 and correction weight N+W+m+E. The gap N/2+m-F1=N/2-p is positive. At a nonzero p-divisible center, f has weight W+p-1+x, so the correction gap is N/2-m-x>0. This holds since x<rho and N/2>rho+m for all r>=3. The latter inequality follows already from rho<N/p and N(1/2-1/p)>m; the first inequality holds from the displayed parity formulas for r>=3.

On D_0 divide the exact odd polynomial by X:

    P_n/X=(f/X)A-a0 g(M/X).

The correction has lower weight N+W+m+E-rho, exceeding K+W+p-1 by N/2-m-rho>0. Therefore P_n/X has the old degree-2L boundary residual with nonzero constant. Each old disk has exactly 2L high boundary roots. The central quotient has no strict-interior root, and

    v(P_n'(0))=K+W+p-1.                              (8.1)

Zero is simple and counted separately.

At a high root, f and g are nonzero and the root equation permits the same differentiation (7.1). For p not dividing a the four term values/bounds are

    W+N+E+m,
    W+N+E-1,
    >=W+N+E+m,
    >=W+N+E+m.

Thus f'A is uniquely minimal with value W+N+E-1. For p dividing a, including the central boundary, put x as in the ledger. The four term values/bounds are

    W+N+E+x-1,
    W+N+E+m-x,
    >=W+N+E+m-1+x,
    >=W+N+E+m.

Now the second is uniquely minimal: the other gaps are 2x-m-1, 2x-1, x. They are positive because x>=p at every noncentral p-divisible center, and x=rho>=sigma at the central one. No parity-r tie occurs. In particular, it would be WRONG to assign the r=3 noncentral value to every a!=0 when r>=4.

## 9. The p-1 separated inner roots for every r

For odd c and 1<=u<p, use T_u={v(X-delta_u)>=sigma}. For any old center a with a mod p=u, (5.2) and v(x_a-x_u)>=p imply v(delta_u-x_a)=eta. All its A roots are still closer to that center than eta, since rho>eta. There are beta/p such centers and hence 2N/p A roots in this residue class. All other A roots are at distance value 1 from T_u. Monic factorization therefore gives on the WHOLE T_u

    weight(A)=J_A=(2N/p)eta+2N(1-1/p)=3N-N/p,

with constant nonzero initial, so its normalized reciprocal is analytic. The eta-neighbor lemma (6.1) applies because T_u lies in the eta disk about x_u. Together with (3.6), the analytic correction R=a0gM/A has

    weight(R)>=W+N+m-p^2.                            (9.1)

Monic factorization of f, using the exact tail root ledger, gives weight W+p-1+sigma and simple linear residual on T_u. The strict gap is

    N+m-p^2-(p-1+sigma)=N-p^2-(3p-2)/2>0.            (9.2)

Thus f-R has that same simple linear residual and exactly one root in T_u. Because A is a unit there, it is a root of P_n. Differentiation of an integral analytic expansion on a radius-sigma disk loses at most sigma in weight. Thus R' is strictly above W+p-1, while f' has exactly that value by (3.6). At a root, differentiating A(f-R) cancels the A'(f-R) term EXACTLY. Hence

    v(P_n')=J_A+W+p-1=3N-N/p+W+p-1.                 (9.3)

All p-1 inner roots are simple. Their disks are disjoint from each other (different t residues), from every old D_a (distance eta or 1 is smaller than both radii), from zero (X-value 1), and from the outer roots (alpha<1). This proof deliberately retains fixed sigma; the high radius rho can grow without weakening its inner estimates.

## 10. Outer roots and original ordinary derivatives

At alpha scale all A roots have value >=1>alpha, so A has weight 2N alpha with initial Y^(2N). Direct matching bounds, since every edge has value >=1, give

    weight_alpha(M)>=N-1+alpha,
    weight_alpha(g)>=cp/2-1+alpha      (c even),
    weight_alpha(g)>=(cp-1)/2          (c odd).

Consequently the correction a0gM lies above A f by the positive gap

    N/p-c(p-1)/2-1/p                  (c even),
    N/p-c(p-1)/2-1/2-1/(2p)           (c odd).

These follow from N/p>=p^2 and c<=p-1. Therefore

    P_n(r0Y)/r0^n -> Y^(2N) He_c(Y^p).               (10.1)

Newton/Weierstrass counting gives p roots in each nonzero Hermite residue class, counted with multiplicity. There are c such classes if c is even and c-1 if odd. No simple-root Hensel assertion is made for the repeated residual. All remaining roots have already been counted in the disjoint high/zero/inner ledger, exhausting the degree.

At an outer root xi, A(xi) is nonzero with exact value 2N alpha. Locally let R=a0gM/A. The displayed matching bounds imply

    v(R)>=V, v(R')>=V-alpha,
    V=N/p+cp/2-1/p                     (c even),
    V=N/p+(cp-3)/2+alpha               (c odd).        (10.2)

For the derivative, explicitly differentiate the quotient, applying the alpha derivative-loss bound separately to g,M,A. This is valid at xi; A is not claimed invertible on the entire alpha disk containing its own roots.

At xi, He_c'( (xi/r0)^p ) is nonzero, so T' has exact value F-1/2 by (4.1). The two perturbations f'-T' and R' lie strictly higher. The latter gap is

    V-alpha-(F-1/2)
      =N/p-c(p-1)/2-1/2-1/(2p)         (c even),
      =N/p-c(p-1)/2-1                   (c odd),

and the former was checked in Section 4. At a root P_n=A(f-R), the term A'(f-R) vanishes exactly, giving

    v(P_n')=2N alpha+F-1/2.

Every outer root is simple. No shallow X-value 1/2 cluster or unexamined zero residue remains, by disjoint degree exhaustion.

## 11. Boundary examples, phases, H, and the original square kernel

At r=3, beta=p,L=p^2,rho=sigma. There are no nonzero p-divisible old centers. All displayed ledgers specialize to the accepted r=3 results, with central odd value W+N+E-p/2 and inner value 3N-p^2+W+p-1. This entire specialization is inherited.

The smallest genuinely new exponent is p=3,r=4. Here N=81,beta=9,L=9,rho=9/2,B=108,K=297,E=513/2,D=669/2. For c=1, n=165: the 108 roots over p-indivisible centers have derivative 673/2; the 36 roots over a=3,6 have derivative 671/2; the 18 central high roots have derivative 334; the exact zero has derivative 299; and the two separated inner roots have derivative 218. There are no outer roots. These counts sum to 165. The eta score maximizer is k*=135, NOT 81; E_eta=207 and J_A=216.

For p=3,r=4,c=2, n=168: 162 high roots have derivative 679/2, six outer roots have derivative 279/2, and the constant value is 302. The high disks are nine disks of 18 roots, not three disks of 54 roots. These are exact rational substitutions, not finite-case substitutes for the proof.

Every argument uses actual mixed-characteristic t and e, integer recurrences, legal specialization, coefficientwise estimates and ordinary derivatives before reduction. The elementary small p-block precision is below e; the remaining statements use exact valuations and matching or Newton identities. Thus every s>r and every characteristic-zero primitive phase is covered, not only tested phases.

All P_n roots have positive value and cannot be +/-2. The exact identities

    H_n(v0^2)=v0^n P_n(v0+v0^(-1)),
    H_n'=v0^(n-2)[(n/2)P_n+(v0-v0^(-1))P_n'/2]

give a multiplicity-preserving correspondence on the branch near v0=i; both coordinate derivatives are units for odd p, and H_n(0)=1. At a root the P_n term vanishes exactly, so H_n has the same ordinary root-derivative valuations. This does not identify normalized P and H units.

Consecutive original P polynomials are coprime: a common root propagates backwards through nonzero recurrence edges to P_0=1. The original Christoffel-Darboux identity at a P_n root xi is

    sum_(j=0)^(n-1)P_j(xi)^2/w_j
      =P_n'(xi)P_(n-1)(xi)/w_(n-1) !=0.

The squares are algebraic squares, not absolute-value squares. No positivity, interlacing, altered kernel or Hermitian argument is used. An injective algebraic p-adic embedding transfers nonvanishing to the original characteristic-zero phase; equivalently Galois conjugacy covers all primitive phases.

## 12. Evidence boundary and independent review

Fresh author controls separately test exact carry identities and extrema, parity-r geometry/counts, every strict rational perturbation/derivative gap, both t/alpha residuals from original short-tail recurrence, ordinary derivatives, first-deleted endpoints, and original transfer/H/P/CD identities in finite phase fixtures. They include all r=3 endpoints and genuinely new even/odd exponents. They are finite falsification/transcription controls, not the uniform theorem or an inference from good finite reduction to characteristic-zero simplicity. No supplied research program is executed.

The author and independent reviewer exchanged the proposed all-r carry formula, extremizer, center split and fixed-radius inner geometry before freeze. The reviewer independently obtained the same bounded Newton-score pattern and related geometric formulas. This is disclosed pre-freeze coordination, not a claim of blind discovery. The final frozen bytes require a separate accepting review; this candidate cannot accept itself.

Excluded: r<3, c>=p, arbitrary middle digits or arbitrary degrees, p=2, s<=r, composite phase orders, global F020/F023 closure, historical novelty/priority, FFT/cost claims, a general finer outer splitting radius, universal good finite reduction, recovery of historical b=2p bytes, and any public/repository/table change. No finite sequence of favorable examples is represented as universal proof.

Completed fresh normal and optimized runs have byte-identical outputs: 516,492 mathematical/transcription checks, including 115,292 exact Newton digit-score indices in 18 (p,r) cases, 20,412 rational (p,r,c) ledgers for primes p<=101 and 3<=r<=20, and 37 original shifted-tail series cases. The series cases use p=3,r=3,4,5; p=5,r=3,4,5; p=7,r=3,4 with every allowed c, plus seven p=11,r=4 stress cases including first-deleted cancellation. The independent original-identity program passes 810 explicit checks across 45 legal finite phase/degree fixtures, at three points each. Fresh source runs pass 647 checks covering six complete original manifests with 48,21,47,13,13,19 entries, 39 selected snapshots, 17 original-location bindings and both pinned r=3 archives. No source program was executed in any run.
