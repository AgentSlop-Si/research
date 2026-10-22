# Odd middle digit: n = 2p^3 + cp

21 October 2026 UTC. Author candidate requiring separate independent verification. Original recurrence, characteristic-zero ordinary derivatives and original algebraic-square kernel throughout. No supplied source program was executed, no external state was changed, and this report does not accept itself.

## 1. Exact proposed theorem and disjoint root ledger

Let p be an odd prime, s>3, c odd with 1<=c<p, q any characteristic-zero primitive p^s-th root, and n=2p^3+cp. The c=1 case is accepted inherited mathematics; the added sector is precisely odd 3<=c<p. Keep

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_b(z)=sum_k [b choose k]_q z^k,
    w_j=product_(u=1)^j(1-q^u), w_0=1.

The candidate proves that P_n and H_n are squarefree and, at each P_n root xi,

    sum_(j=0)^(n-1) P_j(xi)^2/w_j != 0.

In an algebraic p-adic embedding put t=q-1, v(t)=1 and e=v(p)=(p-1)p^(s-1). Define

    N=p^3, L=p^2, m=(p-1)/2, h=(c-1)/2,
    B=3(p-1)p^2/2, K=N+2B, E=N/2+2B, D=N+E-p,
    W=h(2p-1), F=c(p-1/2), alpha=(2p-1)/(2p),
    rho=p-1/2, eta=(p+1)/2,
    x_a=i(q^(a/2)-q^(-a/2)), i^2=-1, 0<=a<p,

where the q square roots are near 1. W is a new scalar for this report, not the q-factorial valuation function, which is denoted Vfac below. The exhaustive disjoint root ledger is:

- 2L high roots on the boundary of each D_a={v(X-x_a)>=rho}, hence 2N in total. Their original derivative values are W+N+E-p/2 in D_0 and W+N+E-1 in every D_a with a!=0.
- One exact zero, simple and strictly inside D_0, with derivative value K+W+p-1. It is not a high boundary root.
- p-1 separated inner roots, one in each T_a={v(X-delta_a)>=rho}, 1<=a<p. Here delta_a is the t-scale root of the exact shifted cp-tail with delta_a/t reducing to ia. It satisfies v(delta_a-x_a)=eta<rho. These P_n roots have X-value 1 and derivative value 3N-p^2+W+p-1.
- (c-1)p outer roots of X-value alpha<1. Their c-1 nonzero coarse residue locations are the roots of He_c(Y^p), each containing p roots counted before simplicity is proved. Their ordinary derivative value is 2N alpha+F-1/2. No finer separation radius of those coarse classes is asserted.

The count is 2N+1+(p-1)+(c-1)p=n. T_a is disjoint from every D_b and from the other T disks. All outer roots are outside these disks. There are no roots of X-value 1/2 and no unexamined cluster. There is no exceptional (p,c) inside the stated scope.

The new sector is empty at p=3. The uniform proof includes c=1 there and reproduces the accepted degree-57 ledger, rather than claiming a new p=3 case. No arbitrary-middle-digit, arbitrary-degree, global F020/F023 closure, p=2, s<=3, composite-order, historical-novelty, cost or FFT assertion is made.

## 2. Bounded source audit and credit before new claims

The accepted complete short-tail map and accepting review cover n=b p^r+d, r>=2, 1<=b<p, 0<=d<p. The present n has base-p digits 20c0. Its position-one digit is not an allowed low tail d<p; it cannot be represented in that rectangle. The latest accepted middle-digit results cover c=1 and c=2 exactly. The historical first-two-digit theorem has degree below p^2, not two arbitrarily positioned occupied digits. Its p-block, third-block, fixed small-prime degree and fixed-order certificates do not encompass this symbolic family. Pure-power or conditional local/all-A statements likewise do not establish it.

This is a bounded audit of the retained accepted source chain, not an exhaustive literature search or priority claim. Original identities, the elementary p-block coefficient fact, general leading-two off-root disk bounds, and the c=1 eta-neighbor lemma remain inherited. The short whole-block Hermite mechanism is directly reconstructed below, without claiming it as historical novelty. The current advance is their uniform odd-c shifted-tail combination and the complete root/ordinary-derivative accounting.

Fresh read-only controls verify all listed bytes of six complete source manifests: c=1 author/review, c=2 author/review, and general leading-digit author/review. Their pinned hashes are recorded in SOURCE_AUDIT.json. The c=1 author/review manifests are 3b560b06a3c8c635c771adf31f05c70917fed370266e7c73d71d5b7005787d12 and 6ce8b81464ad0be29fcbf504ad302f7d07a2ad5f25111922a7484ce8879e9fc6. The c=2 author/review manifests are ebff60ce117ad3f9f7830e1053b1edf02f0e6733cf9571ca80e4b6d25544e05e and 1fd4b414f987ad2244420386d82cfa4a847551eb74f4014bd86056f456712cc6. All 17 original-location bindings inherited from c=1 and the accepted-history archive were also verified. Selected documentary snapshots are not represented as complete copied packages.

The historical b=2p mismatch is preserved: retained report SHA-256 00a4ad13b0726205f3dd6515a4f4c6e9687622c738efdb3df39360b6bcf593db differs from the original author hash 6b27fcbdc7aae652afae91fa9e1a8baf84270ef57af75c44c5f35288541686da cited by its historical review. Those original author bytes and their complete package are not claimed recovered or accepted. No mathematical step below depends on transferring byte acceptance to that changed snapshot.

The concurrent even-middle candidate was read to understand its boundary, but is not an accepted dependency. All whole-block facts used here are proved below. In particular, a first-deleted continuant is never silently substituted for the last-deleted one; the even sector's possible first-deleted cancellation is not imported as either a unit claim or an obstruction for the odd sector.

## 3. Legal specialization and precisely inherited disk inputs

Set A=P_(2N), M=P_(2N-1), a0=1-q^(2N). The accepted general full-disk statements give, on every D_a, coefficientwise weights K,E,D,>=E for A,M,A',M' respectively. Their initial polynomials for A,M,A' are nonzero scalar multiples of Zbar^2+1,Zbar,Zbar, where Zbar=gamma_a Y^L with gamma_a!=0. Thus at any point of the residual locus Zbar^2+1=0, M and the ORIGINAL ordinary A' have exact values E,D. These are off-old-root coefficientwise bounds, valid at new roots, not just values at roots of A. The accepted theorem also gives exactly 2L boundary roots of A per D_a, exhausting degree 2N, and v(A(0))=K.

The accepted c=1 report Section 7 and its independent review give the additional coefficientwise estimate on each larger eta disk about x_a:

    weight(M)>=E_eta:=3N-2p^2.                         (3.1)

For auditability, its finite-carry proof uses the exact H Newton expansion and Vfac(j)=sum_(u=1)^j p^ord_p(u). For b=2N-1 and k=2l+1, writing l=a0+a1p+a2p^2, the score R_eta(2l+1)-Vfac(l) equals

    -a0-p a1-p a2+m eps0+p(p-1)eps1+p^2(p-1)eps2,

where the eps are the carries in doubling l and adding one. Its unique maximum is p^2(p-1), attained at a0=a1=a2=m, so k=N. This gives (3.1). The proof and accepted source are retained; no old rho-disk M bound is simply extended to eta or alpha.

The strict degree bound holds even at p=3:

    n<=2p^3+p(p-1)<p^4<=p^s,
    p^4-[2p^3+p(p-1)]=p[(p-2)p^2-p+1]>0.

Every recurrence edge and q-factorial denominator used is nonzero. For 1<=j<p^s, v(1-q^j)=p^ord_p(j); in particular v(a0)=N. Also e>(p-1)p and every small precision used below is below e where reduction modulo p is invoked.

The unchanged exact Newton identity is

    H_b(z)=sum_(k=b mod 2) w_b N_k(z)/(w_k Q_((b-k)/2)),
    N_k(z)=product_(j=0)^(k-1)(z+q^j),
    Q_j=product_(u=1)^j(1-q^(2u)),
    v(Q_j)=v(w_j)=Vfac(j).

The exact identity H_b(v0^2)=v0^b P_b(v0+v0^(-1)) is a local analytic isometry near v0=i because p is odd. It carries H disks about -q^a to the P disks about x_a and preserves coefficientwise lower bounds up to analytic units.

## 4. Exact tail and odd matching units at the t scale

For 1<=j<cp set b_j=1-q^(2N+j). Define f_0=1,f_1=X,g_0=0,g_1=1, with both sequences satisfying the original tail recurrence using b_j. Put f=f_(cp),g=g_(cp). Exact induction gives

    P_n=f A-a0 g M.                                    (4.1)

The polynomial f is odd of degree cp; g is its FIRST-vertex-deleted, even, degree-(cp-1) continuant. It is not P_(cp-1), which in the unshifted model deletes the other endpoint.

The inherited elementary p-block coefficient fact is

    P_p=X^p+lambda X+J,
    v(lambda)=p-1, lambda/t^(p-1)->epsilon=(-1)^((p+1)/2),
    J odd, degrees 3,...,p-2, coefficient values >=p-1. (4.2)

Its mixed-characteristic derivation uses [p choose j]_(1+t)=(-1)^(j-1)t^(p-1)/j+O(t^p) modulo p, the exact H/P Laurent identity and the ORIGINAL H_p'(-1). Precision p-1 is below e. It is not differentiation of a Frobenius residual in place of the ordinary derivative.

Split f into c consecutive p-vertex blocks, indexed 0,...,c-1. Each full block is shifted from P_p by 2N+ip. The changed edge has value at least p, and telescoping a matching with k edges bounds its changed coefficient at degree p-2k by p+k-1. At X=tY all these errors have weight >p. Consequently each intact block U satisfies

    U(tY)/t^p -> S(Y)=Y^p+epsilon Y.                  (4.3)

At X-weight alpha its residual at weight p alpha is Y^p. The ORIGINAL U' normalized by t^(p-1) has constant residual epsilon there: pX^(p-1) has value e+(p-1)alpha>p-1, all higher odd lower terms and all shifted differences have strictly greater derivative value. These statements also cover the first block, whose shift has value N rather than merely p.

A p-block losing its last or first vertex is an even (p-1)-vertex block. Its X^(2j) coefficient has value at least m-j, and its unique constant matching has normalized residue d=(p-2)!! or u=2^m m!, respectively. Both are nonzero modulo p, and du=(p-1)!=-1. At every X-weight beta>1/2 its weight is m with constant initial; its derivative has weight at least m-1+beta. A block losing both endpoints has p-2 vertices, weight at least m-1+beta, and derivative weight at least m-1. These follow directly termwise from matchings and parity.

The joining edge after p-block i, 1<=i<c, has value p and residue b_(ip)/t^p -> -i. Expand the full continuant according to which joining edges are selected. For a selected subset J, let j=|J| and let a be the number of adjacent selected-edge pairs. There are a twice-incident blocks, 2j-2a once-incident blocks, and c-2j+a intact blocks. At X=tY its term has weight at least

    cp-j+a(m+1).

The number of runs j-a is at most h=floor(c/2). Its excess above cp-h=W+p is at least am. Equality thus requires a=0,j=h. Summing precisely these maximum nonadjacent matchings gives the coefficient of Z in the probabilists' Hermite polynomial He_c(Z), defined by He_0=1,He_1=Z,He_(j+1)=Z He_j-j He_(j-1):

    C:=He_c'(0)=(-1)^h c!! !=0 modulo p,
    f(tY)/t^(W+p) -> C S(Y).                         (4.4)

For g the first block is shortened. Let z=1 if the first joining edge is selected and 0 otherwise; let a again count twice-incident complete blocks. Direct classification gives lower weight

    m+(c-1)p-j+(a+z)(m+1).

Runs not meeting the shortened first block satisfy j-a-z<=h. The excess above W+m is at least (a+z)m. Equality requires a=z=0,j=h, and the UNIQUE matching is {2,4,...,c-1}. Therefore

    g(tY)/t^(W+m) -> G:=u*(-1)^h*2^h*h! !=0.          (4.5)

No cancellation set for this residual remains: all factors are nonzero because c<p. This is the exact odd-c answer, rather than an assumed unit based on the even case. The c=p boundary would kill C and is excluded, not silently included.

Differentiate the ORIGINAL polynomial after making the exact scaled substitution. Namely, t^(-(W+p-1))f'(tY) is the formal derivative in Y of the integral polynomial t^(-(W+p))f(tY). Its reduction is C epsilon, since the coefficient p of Y^(p-1) vanishes only AFTER ordinary differentiation. Thus throughout any disk of X-Gauss weight x>=1,

    weight(f')=W+p-1, constant nonzero initial,
    weight(f/X)=W+p-1, constant nonzero initial if x>1,
    weight(g)=W+m, constant nonzero initial,
    weight(g')>=W+m-1+x.                             (4.6)

For the f/X statement at x>1, (4.4)'s X^(p-1) term becomes strictly higher; at x=1 its residual need not be constant. For g, every nonconstant coefficient at the t scale is strictly above W+m by (4.5), hence at least one whole valuation step above it: the coefficients lie in the cyclotomic field with uniformizer t. Even parity then gives coefficient value at least W+m-d+1 for each even d>=2, so its differentiated monomial at x>=1 has value at least W+m-d+1+(d-1)x>=W+m-1+x. This retains the integer derivative multipliers and proves the g' bound. The old d<p double-factorial unit rule is not used at d=cp.

## 5. Outer tail residual and original derivative, reconstructed

Choose r with r^(2p)=t^(2p-1), so v(r)=alpha. First take the unshifted T=P_(cp). In the same joining expansion the term with j chosen joins and a adjacent pairs has alpha weight at least

    F+a delta, where delta=(p^2-1)/(2p)>0.

For a=0, the normalized term is product_(i in J)(-i) Y^(p(c-2j)). Indeed the recurrence sign makes the joining edge contribute i, while each pair of one-endpoint-deleted block residues contributes du=-1. All a>0 terms are higher. The matching formula gives

    T(rY)/r^(cp) -> He_c(Y^p).                       (5.1)

Here He_c has a simple zero at 0 and c-1 other simple nonzero zeros. To justify simplicity, He_c'=c He_(c-1); a common zero of consecutive Hermite polynomials propagates down the recurrence through nonzero coefficients j<c<p to contradict He_0=1. Since c is odd, its linear coefficient C is nonzero and its zero at 0 is simple.

Reduce the ORIGINAL T' separately, using the scale t^(p-1)r^((c-1)p) of value F-1/2. In each exact selected-join term, differentiation of an intact block, a one-endpoint-deleted block, or a twice-endpoint-deleted block has respective weight at least

    F+a delta-1/2,  F+a delta-1+alpha,  F+a delta-alpha.

For a>=1 these all exceed F-1/2; the smallest third-type excess is delta-alpha+1/2=m>0. For a=0, the endpoint-derivative excess alpha-1/2 is positive. Only derivatives hitting intact blocks of nonadjacent matchings survive, with residue epsilon from (4.3). Therefore

    T'(rY)/(t^(p-1)r^((c-1)p)) -> epsilon He_c'(Y^p). (5.2)

The derivative on the right is in the Hermite variable, THEN evaluated at Y^p. It is not d/dY[He_c(Y^p)], which would give zero and lose the actual ordinary derivative.

Every shifted edge of f differs from that of T by value N. Telescoping a k-edge matching gives coefficient-difference value at least N+k-1. Since cp is odd and alpha>1/2, minimizing over k<= (cp-1)/2 gives

    weight_alpha(f-T)>=Q:=N+(cp-3)/2+alpha,
    weight_alpha(f'-T')>=Q-alpha.                    (5.3)

The exact gaps are

    Q-F=N-c(p-1)/2-1/2-1/(2p)>0,
    Q-alpha-(F-1/2)=N-c(p-1)/2-1>0.                 (5.4)

Thus f has the same alpha residual (5.1), and its ORIGINAL derivative has residual (5.2). This is a precision comparison, not an equality of roots.

Newton/Weierstrass counting applied to (5.1) gives precisely (c-1)p roots of f with value alpha, p in each nonzero coarse class counted with multiplicity. Separately (4.4) gives precisely p roots with v(X)>=1, each a simple lift delta_a of ia, a in F_p, because S has exactly these p simple zeros. All cp roots have now been accounted for. Oddness makes delta_0=0 exactly; (4.6) makes it simple. No attempt is made to use simple-root Hensel on the repeated alpha residual.

## 6. Noncentral tail displacement from an exact Newton minimum

We require f on the OLD high disks, where the t-scale residue in (4.4) vanishes. This is not a substitution of a zero residue into a false unit estimate.

For the unshifted T=P_(cp), let j0=(cp-1)/2=hp+m. On an H disk v(z+q^a)>=rho, a!=0, the k=1 Newton term has weight

    Vfac(cp)-Vfac(j0)=W+(3p-1)/2=:W+F1,             (6.1)

and constant nonzero initial, since v(z+1)=1. To bound every other odd k, write k=2l+1, l>=1. Since cp<p^2,

    Vfac(k)=k+(p-1)floor(k/p),
    weight(N_k)>=k+(rho-1)floor(k/p).

Hence Vfac(k)-weight(N_k)<=floor(k/p)/2. Also Vfac(j0-l)<=Vfac(j0)-l. The Newton score for k is therefore at most

    Vfac(j0)-l+floor((2l+1)/p)/2 < Vfac(j0),

because floor((2l+1)/p)/2<l for every p>=3,l>=1. Thus k=1 is uniquely minimal on the WHOLE disk, not only at its center. The analytic H/P coordinate transfer yields the same coefficientwise constant unit for T.

At X-weight >=1 the shifted difference f-T has weight at least N+(cp-1)/2. Its excess above W+F1 is

    N-(h+1)p+h>0.

Consequently on every noncentral D_a,

    weight(f)=W+F1 with constant nonzero initial.     (6.2)

To find displacement exactly, factor the monic f using the complete tail root ledger of Section 5. At x_a the (c-1)p outer roots each have distance value alpha, total W. The p-1 inner roots with other t residues each have distance value one. The remaining distance is therefore

    v(delta_a-x_a)=(W+F1)-W-(p-1)=eta.               (6.3)

This is exact monic factorization, not an approximate Taylor inference. Since eta<rho, the nonzero inner tail centers lie OUTSIDE their corresponding old D_a. On D_0, (4.6) instead gives f/X weight W+p-1 with constant initial. The exact zero is not a separated T_a.

## 7. All high roots and the exact zero

On D_a with a!=0, the two terms of (4.1) have weights

    fA: K+W+F1,
    a0 g M: N+W+m+E.

The latter exceeds the former by N/2+m-F1=N/2-p>0. Thus P_n has the same degree-2L boundary residual as a scalar unit times A, giving exactly 2L boundary roots per such disk before simplicity is proved.

On D_0, divide the exact odd polynomial by X:

    P_n/X=(f/X)A-a0 g(M/X).

The quotient M/X has weight at least E-rho. The correction exceeds the principal weight K+W+p-1 by at least

    N/2+m-rho-(p-1)=N/2-rho-m>0.

The normalized quotient consequently has the old degree-2L boundary residual and a nonzero constant. It has exactly 2L boundary roots, no strict-interior roots, and

    v(P_n'(0))=v((P_n/X)(0))=K+W+p-1.               (7.1)

Zero is therefore simple, strictly interior, and counted separately.

At every nonzero high root, the residual locus remains Zbar^2+1=0, so v(M)=E,v(A')=D,v(M')>=E. Both f and g are nonzero there. Use the exact root equation A=a0 gM/f, and differentiate the ORIGINAL polynomial:

    P_n'=f A'+f' A-a0 g'M-a0 gM'.                   (7.2)

For a noncentral high root the four values/bounds are

    W+F1+D = W+N+E+m,
    N+W+m+E+(p-1)-F1 = W+N+E-1,
    >=W+N+E+m,
    >=W+N+E+m.

The second term is uniquely minimal. Therefore v(P_n')=W+N+E-1.

For a central high root v(X)=rho and v(f)=W+p-1+rho. The corresponding four values/bounds are

    W+N+E+rho-1,
    W+N+E+m-rho = W+N+E-p/2,
    >=W+N+E+m-1+rho,
    >=W+N+E+m.

Again the second is uniquely minimal. Its gaps to the other three are 3(p-1)/2, 2rho-1 and rho, all strictly positive. These comparisons cover every c in scope and every primitive phase. No equal-leading-term cancellation remains.

## 8. The separated p-1 inner roots

For a!=0 take T_a={v(X-delta_a)>=rho}. By (6.3) every point has distance eta from x_a and distance one from every other old center. Since all old A roots are on the corresponding rho boundaries, monic factorization gives on this ENTIRE smaller disk

    weight(A)=J_A:=2L eta+2L(p-1)=3N-p^2,

with constant nonzero normalized initial. Its reciprocal is thus an analytic unit after scalar normalization. Equation (3.1) applies since T_a is contained in the eta disk about x_a. Equation (4.5) gives g weight W+m. Therefore the analytic function R=a0gM/A satisfies

    weight(R)>=W+V0, where V0=N-p^2+m.               (8.1)

The other cp-1 roots of f have fixed distances from this disk: the outer roots contribute W, and the other p-1 inner roots contribute p-1. Monic factorization therefore gives f weight W+p-1+rho, with simple linear residual in X=delta_a+lambda0 Y, v(lambda0)=rho. The strict perturbation gap is

    V0-(p-1+rho)=p^3-p^2-(3p-2)/2>0.                (8.2)

Thus f-R has the same simple linear residual and exactly one root in T_a. This is a root of P_n=A(f-R), disjoint from the high roots and the exact zero.

Differentiate the ORIGINAL restricted analytic expansion. On a radius-rho disk differentiation loses at most rho in weight, because integer coefficient multipliers have nonnegative valuation. Consequently

    weight(R')>=W+V0-rho>W+p-1,

while f' has exact value W+p-1 by (4.6). At a root the term A'(f-R) vanishes exactly, so

    v(P_n')=J_A+W+p-1=3N-p^2+W+p-1.                (8.3)

All p-1 separated inner roots are simple. This argument does not divide by a possibly vanishing f or M, and it treats the exact central f zero separately rather than inventing an extra separated root.

## 9. All outer P_n roots and their original derivatives

At alpha scale every root of A has value at least one. Monic factorization gives weight(A)=2N alpha and residual Y^(2N) after scaling by r^(2N). An elementary matching bound suffices for the other two continuants: all edges have value at least one, so an h-edge term in degree d has weight at least h+(d-2h)alpha. Minimizing over h gives

    weight_alpha(g)>=(cp-1)/2,
    weight_alpha(M)>=N-1+alpha.                     (9.1)

These are direct bounds at the actual alpha scale, not extensions of the high-disk bounds. Hence the correction a0gM lies above the principal A f weight 2N alpha+F by

    Delta=p^2-c(p-1)/2-1/2-1/(2p)>0.                (9.2)

The full monic polynomial therefore has integral alpha reduction

    P_n(rY)/r^n -> Y^(2N) He_c(Y^p).                (9.3)

Each of the c-1 nonzero simple Hermite locations has multiplicity p in this residual. Newton/Weierstrass counting supplies exactly (c-1)p roots of X-value alpha, p per such coarse class, counted with multiplicity. The zero residue has multiplicity 2N+p and is accounted for by Sections 7-8, not miscounted as an additional alpha-valued cluster.

For every outer root xi, A(xi) has exact value 2N alpha and is nonzero. Locally define R=a0gM/A. The matching bounds and ordinary derivative term bounds give

    v(R(xi))>=V:=p^2+(cp-3)/2+alpha,
    v(R'(xi))>=V-alpha.                             (9.4)

To justify the second bound without claiming a global reciprocal on the whole alpha disk, differentiate the quotient explicitly: the numerator terms a0g'MA,a0gM'A,-a0gMA' are divided by A^2. Each polynomial derivative loses at most alpha from its coefficientwise alpha bound, including A'>=2N alpha-alpha. Evaluating at xi yields (9.4). A does have zeros in the full alpha disk, so no analytic inverse there is asserted.

At xi the residue y=xi/r obeys He_c(y^p)=0 and y!=0; by Hermite coprimeness He_c'(y^p)!=0. The ORIGINAL T' thus has exact value F-1/2 by (5.2). The two error gaps are

    V-alpha-(F-1/2)=p^2-c(p-1)/2-1>0,
    Q-alpha-(F-1/2)=N-c(p-1)/2-1>0.                 (9.5)

Both follow already from c<=p-1. Thus f'-R' has exact value F-1/2. At a root, exact differentiation of P_n=A(f-R) kills A'(f-R), giving

    v(P_n')=2N alpha+F-1/2.                         (9.6)

Every outer root is simple. Together with the 2N high roots, one zero and p-1 inner roots, their disjoint count exhausts degree n. The absence of every further cluster follows from degree exhaustion, not from an unexamined shallow residual.

## 10. Endpoints, cancellations, every phase, H and original kernel

There are no theorem exceptions in the stated odd-c range. The t-scale f coefficient C=(-1)^h c!! is nonzero, and the first-deleted g constant G=u*(-1)^h2^h h! comes from one unique matching. The outer polynomial has distinct Hermite zeros because c<p. The noncentral old-disk minimum is uniquely k=1. The central quotient constant and every original high-derivative comparison are strict. These mechanisms explicitly resolve each possible leading cancellation rather than extrapolating from a finite grid.

At p=3 the only permitted odd c is inherited c=1, with W=0,n=57. The proof gives 18 central high roots with derivative 93; 36 noncentral high roots with derivative 187/2; one zero with derivative 83; two separated roots with derivative 74; and zero outer roots. The eta gap (8.2) is 29/2. All displayed inequalities remain strict, and the outer proof is simply vacuous. No new p=3 case, division by 3, or p>=5-only cancellation formula is claimed.

The first new case is p=5,c=3: W=9,n=265. It has 50 central high roots with derivative 494, 200 noncentral high roots with derivative 991/2, one zero with derivative 438, four separated inner roots with derivative 363, and ten outer roots with derivative 238. These sum to 265. The c=p-2 endpoint is included for every p>=5. The formal extension c=p would make C vanish and is outside the theorem, not evidence of a characteristic-zero multiple root.

Every argument uses actual t=q-1, actual e=(p-1)p^(s-1), original integer recurrence coefficients, legal nonzero-edge specialization, and coefficientwise bounds. The residue p-block step is transferred below e, the shifts have their actual valuations, and all derivative factors are retained before reduction. Therefore every s>3 and every characteristic-zero primitive phase is covered. Finite formal or finite-field tests are only falsification/transcription controls, never the universal proof.

Every P root has positive value and therefore is not +/-2. In

    H_n(v0^2)=v0^n P_n(v0+v0^(-1)),

the branch near v0=i has unit coordinate derivatives because p is odd. It gives a multiplicity-preserving bijection of all P_n roots with all H_n roots near -1; H_n(0)=1. At a root the exact ORIGINAL derivative identity is

    H_n'=v0^(n-2)[(n/2)P_n+(v0-v0^(-1))P_n'/2].

The P_n term vanishes, and the remaining multiplier is a unit. Thus H_n is squarefree with the same rootwise derivative valuations. Exact P zero maps to H root -1; no equality of normalized P/H units is asserted.

Consecutive original P polynomials have no common root: backward propagation through the nonzero recurrence edges would contradict P_0=1. At each root xi of P_n, the unchanged Christoffel-Darboux identity gives

    sum_(j=0)^(n-1) P_j(xi)^2/w_j
      =P_n'(xi)P_(n-1)(xi)/w_(n-1) != 0.

These are algebraic squares, not absolute-value squares. No positivity, Hermitian reformulation or complex interlacing is used. Injective algebraic p-adic embeddings transfer nonvanishing to every original characteristic-zero primitive phase.

## 11. Evidence and independent-review boundary

Fresh author controls reconstruct the original small-prime recurrence as a truncated polynomial in t and X, its actual ordinary derivative, alpha and t residuals, and the first-deleted tail rather than its endpoint-swapped substitute. They test every joining subset in the stated small-prime range, exact noncentral Newton scores, root counts and rational strict gaps, including c=1,p=3 and the first new cases. Additional modular fixtures check original transfer, differentiated transfer, H/P and algebraic-square CD identities without requiring good reduction. They are narrow reproducible evidence, not substitutes for the uniform proof.

Only fresh author programs in this packet are executed. Source manifests and documents are read and hashed, not their supplied programs. The same control runs are made normally and under Python optimization with explicit failure checks rather than removable assert statements. The final source/control totals and actual tested ranges are reported in the machine-readable outputs and run log.

Before freeze, the author and independent reviewer discussed the intended odd matching units, two-scale ledger and noncentral Newton score. The author derived the score inequality and sent the architecture before seeing the reviewer's same independently supplied score argument. This overlap is disclosed: the author does not claim a blind development process, and the separate reviewer still decides acceptance of the final frozen bytes. No public projection, repository/table write, permission change or global closure is made by this candidate.

Completed fresh normal and optimized runs each pass 80,668 explicit checks with byte-identical JSON. They include 11 original-tail formal-series cases at p=3,5,7,11 (including inherited c=1), 567 odd-(p,c) rational ledgers through p=101, 9,412 noncentral Newton indices through p=31, 15,795 eta-score indices through p=19, every joining subset in those series cases, and 270 exact identity checks across 18 finite phase/degree fixtures and three evaluation points each. The read-only source runs each pass 186 explicit checks with byte-identical output.

Two pre-freeze diagnostic/transcription issues were corrected without changing a theorem or bound. An early control erroneously demanded g' be strictly above W+m at x=1 although the proved and needed bound was only >=W+m; the corrected control tests exactly that lower bound. The first typed p=5,c=3 numerical example had wrong high derivative arithmetic; the exact rational ledger gives 494 and 991/2, now displayed. Neither a failed required comparison nor a bad reduction was removed to obtain acceptance.
