# First intermediate digit: n = 2p^3 + p

21 October 2026 UTC. Author candidate for separate verification, not self-accepted. Original recurrence, characteristic-zero ordinary derivative and algebraic-square kernel throughout. No supplied research program was executed and no external state was changed.

## 1. Candidate theorem and disjoint all-root partition

Let p be any odd prime, s>3, q any characteristic-zero primitive p^s-th root, and n=2p^3+p. Define exactly

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_b(z)=sum_k [b choose k]_q z^k,
    w_j=product_(u=1)^j(1-q^u), w_0=1.

Then the candidate proves that P_n and H_n are squarefree and, at every P_n root xi,

    sum_(j=0)^(n-1) P_j(xi)^2/w_j != 0.

Choose an algebraic p-adic embedding, put t=q-1 and v(t)=1, and retain e=v(p)=(p-1)p^(s-1). Set

    N=p^3, L=p^2, m=(p-1)/2, B=3(p-1)p^2/2,
    K=N+2B, E=N/2+2B, D=N+E-p,
    rho=(2p-1)/2, eta=(p+1)/2,
    x_a=i(q^(a/2)-q^(-a/2)), 0<=a<p, i^2=-1,

where the square roots of q^a are the ones near 1. The disjoint partition of roots is:

1. Exactly 2L high roots in each old disk D_a={v(X-x_a)>=rho}, all on its boundary, giving 2N roots. The original derivative has value N+E-p/2 on D_0 and N+E-1 on D_a, a!=0.
2. One exact zero, strictly inside D_0, not among the boundary roots. It is simple with v(P_n'(0))=K+p-1.
3. Exactly p-1 further roots, one in each separate disk T_a={v(X-delta_a)>=rho}, 1<=a<p. Here delta_a is the unique root of the exact shifted tail continuant f_p with delta_a/t reducing to ia. These tail centers satisfy v(delta_a-x_a)=eta<rho. Every such P_n root has value 1 and derivative value 3N-p^2+p-1.

Thus 2N+1+(p-1)=n. No shallow root of value 1/2 remains. The central f_p zero is exactly 0 and is counted in item 2, not as an additional separated tail root. The T_a are disjoint from every D_b and from one another.

The family does not close F020/F023 globally, does not cover another intermediate digit, arbitrary degree, p=2, s<=3, composite orders, or complexity/FFT claims. No historical novelty is asserted. The exact result is submitted to a separate reviewer.

## 2. Audit of inherited scope, before new proof credit

The accepted complete short-tail map and its accepting independent review cover precisely n=c p^r+d, r>=2, 1<=c<p, 0<=d<p. The base-p digits of this target are 2010, with the digit 1 in position 1 and digit 2 in position 3. They cannot be represented in that rectangle. The earlier accepted general leading-digit, pure-power, leading-one low-tail, leading-two short-tail and later parity-sector theorems consequently do not already imply this symbolic family.

The intact accepted-history archive was also inspected at its historical theorem statements, rather than trusting names such as “two-digit.” Its complete first-two-digit residual theorem has b<p^2, not two arbitrarily positioned nonzero digits. Earlier p-block/third-block/fourth-block bounds and fixed p=3 degrees 9,10,11 do not contain 2p^3+p; fixed order-9/order-25 certificates do not apply to s>3. The pure-power distinguished-root and outer-root statements are restricted to n=p^r. The inherited local/all-A hypotheses and fixed-node guards are not unconditional squarefreeness for this target.

This is a bounded accepted-source scope audit, not an exhaustive external literature search or a priority certificate. The bound source identities and selected exact statement snapshots are recorded separately. The general leading-digit coefficientwise lemmas and old p-block coefficient fact remain inherited ingredients, not fresh theorem credit. No existing accepted statement has been relabeled as a new family.

## 3. Accepted full-disk inputs and legal specialization

Put A=P_(2N), M=P_(2N-1), a0=1-q^(2N). The accepted general adjacent-criterion author report Sections 2–5, independently reviewed, proves the following unconditional coefficientwise facts at c=2,r=3, including p=3:

- On every D_a, A has weight K and residual a nonzero scalar times Zbar^2+1, where Zbar=alpha_a Y^L, alpha_a!=0.
- M has weight E and residual a nonzero scalar times Zbar.
- The ORIGINAL ordinary A' has weight D and residual a nonzero scalar times Zbar.
- The ORIGINAL ordinary M' has weight at least E.
- The leading polynomial A has exactly 2L roots in each D_a, all on the boundary, and these exhaust degree 2N. A(0) has value K.

The last root count also follows directly from the first residual and degree exhaustion. At any point of the residual locus Zbar^2+1=0, M and A' have exact values E and D. These are off-old-root coefficientwise lemmas, so they are usable at new roots. They are not derivative claims inferred from differentiating the inseparable residual. Their exact accepting report and author/review manifest identities are retained in SOURCE_BINDINGS.json.

The growth bound is strict even at p=3:

    2p^3+p < p^4 <= p^s,
    p^4-(2p^3+p) = p[(p-2)p^2-1] > 0.

Every recurrence edge used, and every q-factorial denominator below, is therefore nonzero. For 1<=j<p^s, v(1-q^j)=p^ord_p(j); in particular v(a0)=N. Also e>p-1, including the least s=4.

We use the exact Newton expansion

    H_b(z)=sum_(0<=k<=b, k=b mod 2)
             w_b N_k(z)/(w_k Q_((b-k)/2)),
    N_k(z)=product_(j=0)^(k-1)(z+q^j),
    Q_j=product_(u=1)^j(1-q^(2u)),
    W(j)=v(w_j)=v(Q_j)=sum_(u=1)^j p^ord_p(u).

The identity is over Q(q), derived by the original generating functions; all denominators survive the stated specialization. The exact coordinate identity H_b(v0^2)=v0^b P_b(v0+v0^(-1)) is an analytic isometry near v0=i because p is odd. It carries H disks around -q^a to P disks around x_a and preserves coefficientwise Gauss lower bounds up to analytic unit factors.

## 4. Exact p-tail, ordinary derivative, and why the old unit lemma fails

Define b_j=1-q^(2N+j), 1<=j<=p-1, and the exact continuants

    f_0=1, f_1=X, f_(j+1)=X f_j-b_j f_(j-1),
    g_0=0, g_1=1, g_(j+1)=X g_j-b_j g_(j-1).

Induction in the original recurrence gives

    P_(2N+j)=f_j A-a0 g_j M.                              (4.1)

Write f=f_p and g=g_p. Parity makes f odd and g even. There is no division by a possibly vanishing tail in this identity.

Let c=(-1)^((p+1)/2). The elementary p-block coefficient fact is

    P_p=X^p+lambda X+sum_(odd k,3<=k<=p-2) e_k X^k,
    v(lambda)=p-1, lambda/t^(p-1) -> c,
    v(e_k)>=p-1.                                        (4.2)

For clarity, here is a fresh derivation of the inherited ingredient. In F_p[[t]],

    [p choose j]_(1+t) = (-1)^(j-1)t^(p-1)/j + O(t^p), 0<j<p.

It follows that H_p=1+z^p modulo (p,t^(p-1)). Substitution z=v0^2 and the exact H/P identity, followed by the injectivity of X->v0+v0^(-1) in Laurent polynomials, yields P_p=X^p modulo (p,t^(p-1)). The largest Laurent exponent proves injectivity without any division by p. Differentiating the original H_p before reduction gives H_p'(-1)/t^(p-1)->-1: the p-1 inner terms each contribute 1, while the leading p term is above this order. At X=0 the coordinate derivative factor is i^(p-1)=(-1)^m, giving c. Because e>p-1, all discarded p-divisible coefficients are genuinely higher in the original field. Thus (4.2) is mixed-characteristic, valid for every s>3 and phase.

Each shifted edge differs from the unshifted one by

    b_j-(1-q^j)=-q^j(q^(2N)-1), of value N.

In the path-matching formula, the coefficient of X^(p-2h) in f-P_p has value at least N+h-1 for 1<=h<=m: telescope products and retain at least h-1 other edges of value 1. The leading coefficient does not change. On every disk of X-Gauss weight >=1 this yields weight(f-P_p)>=N+m. Differentiating these integer-coefficient monomials first gives weight(f'-P_p')>=N+m-1. Consequently throughout v(X)>=1,

    v(f'(X))=p-1.                                      (4.3)

Indeed the lambda term is unique at that weight; pX^(p-1) and every higher odd coefficient are strictly higher. This is the original ordinary derivative.

For g, the unique maximal matching uses the even edges 2,4,...,p-1. It gives, on any X disk of weight x>=1,

    weight(g)=m, g/t^m -> (p-1)!! !=0,
    weight(g')>=m-1+x.                                 (4.4)

Every nonconstant term of g has strictly larger weight. The ordinary derivative bound follows term by term, keeping its integer factors.

The short-tail constant d!! is not a unit here: d=p divides p!!. At the former shallow scale tau^2=t, the full recurrence instead reduces to Z^(2N+p). To see this without importing a failed lemma, the reduced Hermite recurrence is M_(j+1)=Z M_j+j M_(j-1), M_p=Z^p and M_(ap+b)=Z^(ap)M_b for 0<=b<p. Hence no nonzero shallow residue exists. This proves absence of roots of value 1/2, but is not a simplicity argument at zero.

## 5. Tail roots, their displacement, and full high-disk values

At the X=tZ scale, (4.2) and the shifted-edge bounds give

    f(tZ)/t^p -> S(Z)=Z^p+cZ.

Since S'=c!=0, S has exactly p distinct roots. If i^2=-1 then i^(p-1)=(-1)^m=-c, so these roots are ia, a in F_p. Simple-root Hensel gives exactly one f root delta_a in each class delta_a/t->ia. These are all its p roots. Oddness and (4.3) show delta_0=0 exactly and simply.

For a!=0, evaluate the original H_p Newton expansion on the full H disk v(z+q^a)>=rho. The k=1 term has weight

    W(p)-W(1)-W(m)+v(z+1)
       =2p-1-1-m+1=(3p-1)/2=:F.

It has constant nonzero initial because v(z+1)=1. For odd 3<=k<p, even the weaker bound weight(N_k)>=k gives weight at least (3p+k-2)/2>F. The k=p term is N_p, whose weight is p-1+rho>F, since rho-eta=(p-2)/2>0. Thus the k=1 term is uniquely minimal, including p=3. Coordinate transfer and the shifted-edge bound prove

    weight_Da(f)=F, with constant nonzero initial, a!=0. (5.1)

In particular v(f(x_a))=F. The other p-1 f roots have distance value 1 from x_a because their t-scale residues differ. Monic factorization now gives

    v(delta_a-x_a)=F-(p-1)=eta.                         (5.2)

This proves displacement exactly, not an approximate Taylor inference. The noncentral tail roots are outside the old rho disks, not inside them.

On the central disk, (4.2) instead gives

    weight_D0(f/X)=p-1,
    (f/X)/t^(p-1) has constant nonzero initial.           (5.3)

There is no pole at X=0. On a noncentral old disk f is an analytic unit after scalar normalization; on the central old disk f/X, not f, is the unit.

## 6. The 2N high roots and the exact zero

On D_a, a!=0, the two terms in (4.1) have weights

    fA: K+F,
    a0 g M: >=N+m+E=K+N/2+m.

Their difference in weights is N/2+m-F=N/2-p>0. Thus the entire new P polynomial has the same degree-2L boundary residual as a unit times A. Newton/Weierstrass counting gives precisely 2L roots on the boundary, counted with multiplicity before the derivative calculation.

On D_0 divide the exact odd polynomial by X:

    P_n/X=(f/X)A-a0 g(M/X).

Polynomial division gives weight(M/X)>=E-rho. The correction exceeds the principal weight K+p-1 by at least

    N/2+m-rho-(p-1)=N/2-rho-m>0.

Thus the quotient has exactly 2L boundary roots and a nonzero constant residual. At zero this proves

    v((P_n/X)(0))=K+p-1,

so zero is simple and is not among those boundary roots. Nothing here differentiates an inseparable residual.

At every nonzero high root the residual equation is still Zbar^2+1=0. Therefore v(M)=E, v(A')=D, and v(M')>=E at all these new roots. Also f and g are nonzero there, so the exact root equation may be used as A=a0 g M/f.

Differentiate (4.1) in characteristic zero, without suppressing any terms:

    P_n'=f A'+f' A-a0 g'M-a0 g M'.                       (6.1)

At a noncentral high root the four values/bounds are respectively

    F+D=N+E+(p-1)/2,
    N+m+E+(p-1)-F=N+E-1,
    >=N+m+E,
    >=N+m+E.

The second is uniquely smallest. Hence v(P_n')=N+E-1.

At a central high root x=v(X)=rho and v(f)=rho+p-1. The corresponding values/bounds are

    rho+p-1+D=N+E+rho-1,
    N+m+E-rho=N+E-p/2,
    >=N+m+E-1+rho,
    >=N+m+E.

Again the second is uniquely smallest; the first gap is 2rho-m-1=3(p-1)/2>0, and the others have gaps 2rho-1 and rho. Thus v(P_n')=N+E-p/2. All 2N high roots and the exact zero are simple, uniformly at p=3 as well as larger primes.

## 7. Fresh eta-disk neighbor bound: the new carry lemma

It remains to find and certify p-1 further roots; the old shallow-root count cannot do this. We first prove a coefficientwise bound for M on every larger eta-disk v(X-x_a)>=eta:

    weight(M)>=E_eta:=3N-2p^2.                          (7.1)

In the H coordinate, N_k has weight at least

    T_eta(k)=k+(eta-1)floor(k/p),

because every complete p-block includes one factor within the eta cap and all other factors have value at least 1. Here eta<p, also at p=3. Set R_eta=W-T_eta. For b=2N-1, the k-th Newton term has weight at least W(b)-W((b-k)/2)-R_eta(k).

Write k=2l+1, 0<=l<N. Digit complementation gives exactly

    W((b-k)/2)=W(N-1-l)=W(N-1)-W(l).

Put l=a_0+a_1 p+a_2 p^2, 0<=a_j<p. Let eps_0,eps_1,eps_2 be the carries in doubling l and adding 1:

    eps_0=floor((2a_0+1)/p),
    eps_1=floor((2a_1+eps_0)/p),
    eps_2=floor((2a_2+eps_1)/p).

Using W(l)=a_0+(2p-1)a_1+(3p^2-2p)a_2 and

    R_eta(k)=m floor(k/p)+p(p-1)floor(k/p^2)
                                      +p^2(p-1)floor(k/p^3),

the exact score is

    J:=R_eta(2l+1)-W(l)
      =-a_0-p a_1-p a_2+m eps_0+p(p-1)eps_1+p^2(p-1)eps_2.

For fixed carries, J is maximized by the smallest admissible digits:

    a_0=m eps_0,
    a_1=(m+1-eps_0)eps_1,
    a_2=(m+1-eps_1)eps_2.

Every such triple is admissible for its carry pattern. These give the following maxima for (eps_0 eps_1 eps_2):

    000: 0                  100: 0
    010: p(m-1)             110: pm
    001: p^2(p-1)-p(m+1)    101: p^2(p-1)-p(m+1)
    011: p^2(p-1)-p         111: p^2(p-1).

Every maximum except 111 is strictly below p^2(p-1), for all m>=1. Equality in the full score requires a_0=a_1=a_2=m, hence k=N. Therefore

    W((b-k)/2)+R_eta(k)
        <=W(N-1)+p^2(p-1)=4(p-1)p^2,

while W(b)=7N-6p^2. This proves (7.1), with unique Newton equality index k=N. Only the lower bound is needed below. The coordinate unit multiplier preserves it in P. This is a new finite-carry proof, not a numerical prime extrapolation.

## 8. The separated p-1 tail roots and their ordinary derivatives

For each a!=0 consider T_a={v(X-delta_a)>=rho}. By (5.2), every point in T_a has distance value eta from x_a and value 1 from every other old center. The accepted monic factorization of A into its 2L roots in each D_b therefore proves coefficientwise

    weight_Ta(A)=J_A:=2L eta+2L(p-1)=3N-p^2,

and its normalized polynomial is an analytic unit with constant initial. All its root distances are fixed on this entire smaller disk. Since T_a is contained in the eta-disk about x_a, (7.1) applies to M there. By (4.4), g has weight m.

Consequently the restricted analytic quotient

    R=a0 g M/A

has weight at least

    V=N+m+E_eta-J_A=N-p^2+m.

The required strict inequality is

    V > p-1+rho,
    V-(p-1+rho)=p^3-p^2-(3p-2)/2>0.                    (8.1)

It holds already at p=3 (gap 29/2), and increases thereafter. No division by M or f was made on these disks.

Because f has exactly one root delta_a here and its other p-1 roots have distance value 1, monic factorization gives weight(f)=p-1+rho and a simple linear residual in the scaled coordinate X=delta_a+lambda Y, v(lambda)=rho. Equation (8.1) shows f-R has the same simple linear residual. Hensel/Weierstrass therefore yields exactly one root of P_n=A(f-R) in each T_a. It is not a high boundary root because T_a and all D_b are disjoint.

For the ORIGINAL ordinary derivative, differentiation of an integral restricted analytic expansion on this radius loses at most rho, as the integer coefficient multipliers have nonnegative valuation. Thus

    weight(R')>=V-rho>p-1,

whereas f' has exact value p-1 by (4.3). At the root, the A'*(f-R) term vanishes exactly. Hence

    v(P_n')=J_A+p-1=3N-p^2+p-1.

The p-1 tail roots are simple. Along with the 2N high roots and one exact zero, the count exhausts the monic degree n. This also rules out every unexamined root cluster.

## 9. Small p, all phases, H, and the original kernel

For p=3 the data are

    n=57, N=27, L=9, m=1, rho=5/2, eta=2,
    K=81, E=135/2.

There are 18 central high roots with derivative value 93, 36 noncentral high roots with value 187/2, one exact zero with value 83, and two separated tail roots with value 74. The total is 57. The eta lemma gives E_eta=63, J_A=72 and V=19. Every strict inequality above remains strict; no p>=5-only cancellation expansion or division by 3 is used. As a derived consistency check the sum of derivative valuations is 5271, but no extra discriminant theorem is needed for the claimed conclusion.

All proofs use the actual t=q-1, actual e=(p-1)p^(s-1), original integer recurrences, and mixed-characteristic coefficient bounds. The only residue-field p-block calculation was transferred at precision p-1<e. The shifts have actual valuation N at every s>3. The remaining Newton and derivative statements are exact accepted all-phase inputs or fresh exact valuation inequalities. Thus no finite-s or finite-phase sample substitutes for the universal quantifier.

Every P root reduces to zero, either from the complete partition or directly from P_n mod(t)=X^n. In particular no root equals +/-2. The branch v0 near i in H_n(v0^2)=v0^n P_n(v0+v0^(-1)) therefore gives a multiplicity-preserving bijection of all P and H roots. H_n(0)=1; all H roots reduce to -1. At a root, the exact ordinary derivative identity

    H_n'=v0^(n-2)[(n/2)P_n+(v0-v0^(-1))P_n'/2]

has zero prefactor term and a unit multiplier of P_n'. Hence H_n is squarefree with the same rootwise derivative valuations. Exact P zero maps to H root -1. No equality of normalized P/H units is claimed.

Finally consecutive original P polynomials have no common root: backward recurrence through nonzero edges would contradict P_0=1. The unchanged Christoffel-Darboux identity at a P_n root is

    sum_(j=0)^(n-1)P_j(xi)^2/w_j
      =P_n'(xi)P_(n-1)(xi)/w_(n-1).

Every factor on the right is nonzero. These are algebraic squares, not absolute-value squares; no positivity or interlacing is used. Injective algebraic p-adic embeddings, or equivalently conjugacy after the all-phase proof, transfer the conclusion to every characteristic-zero primitive phase.

## 10. Evidence and independent-review boundary

Fresh controls in this packet check the original exact transfer and differentiated transfer at finite-field primitive phases, the small-prime tail series and derivative, exact center evaluations, exhaustive digit/carry identities, unique Newton minima, all positive valuation gaps, disjoint counts, and negative controls against extending the old d<p lemma. They are reproducible falsification/transcription evidence, not the uniform proof.

Only new author controls were executed. Supplied source programs and accepted control suites were not run. Source documents were read and hashed; they were not changed. Selected exact documentary snapshots are not represented as complete copies of their original packages.

Pre-freeze discussion with the separate reviewer checked the intended central/noncentral split and derivative terms. The author independently derived the stronger eta-neighbor carry lemma in Section 7 and sent it before the reviewer offered a different weaker global bound. That alternative is not used. The author owns the proof and new controls; the separate review, not this report, decides acceptance of the final frozen bytes. No public artifact, repository, table, or permission state is changed here.

Finite-reduction caution: direct controls at p=3,s=4 in F_163 found gcd degree 2 at phase exponents 28 and 29, and p=3,s=5 found gcd degree 2 at exponent 142 in its selected field. These are retained bad reductions, not characteristic-zero multiple-root claims. The first author control draft incorrectly required every auxiliary finite-field reduction to be squarefree; that diagnostic assertion was removed, and the actual gcd outcomes are now recorded. Exact transfer identities continued to hold. This control correction changes no p-adic proof or theorem statement.
