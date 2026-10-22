# Second intermediate digit: n = 2p^3 + 2p

21 October 2026 UTC. Author candidate for a separate independent review. This report does not accept itself, change a table or repository, claim historical originality, or close F020/F023. No supplied research program was executed.

## 1. Exact theorem candidate and disjoint root ledger

Let p be any odd prime, s>3, q any characteristic-zero primitive p^s-th root, and n=2p^3+2p. Keep the original definitions

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_b(z)=sum_k [b choose k]_q z^k,
    w_j=product_(u=1)^j(1-q^u), w_0=1.

The candidate proves that P_n and H_n are squarefree, and that at every P_n root xi,

    sum_(j=0)^(n-1) P_j(xi)^2/w_j != 0.

These are algebraic squares, not absolute-value squares. Work in an algebraic p-adic embedding with t=q-1, v(t)=1, e=v(p)=(p-1)p^(s-1), and put

    N=p^3, L=p^2, m=(p-1)/2,
    B=3(p-1)p^2/2, K=N+2B, E=N/2+2B, D=N+E-p,
    rho=(2p-1)/2, alpha=(2p-1)/(2p),
    x_a=i(q^(a/2)-q^(-a/2)), i^2=-1, 0<=a<p,

with the square roots of q^a near 1. The complete disjoint root ledger is:

1. Exactly 2L roots on the boundary of each D_a={v(X-x_a)>=rho}, a=0,...,p-1. These 2N roots have original ordinary derivative value

       v(P_n')=N+E+p-1.

2. Exactly p roots in each of the two disks B_+={v(X-a)>=1} and B_-={v(X+a)>=1}, with a defined explicitly in Section 6. Their common X-value is alpha<1, their within-disk pairwise differences have value 1, and their cross-disk differences have value alpha. These 2p roots have original ordinary derivative value

       v(P_n')=2N alpha+2p-3/2.

3. There is no zero root. In particular the central high disk has only its 2L boundary roots, not an additional zero. More exactly,

       v(P_n(0))=K+2p-1.

All p old disks are disjoint. Both B disks are disjoint from every old disk and from each other. The counts add to 2N+2p=n. No root of X-value 1/2 or unexamined root cluster remains.

At p=3, n=60: there are 18 high boundary roots in each of three disks, all with derivative value 193/2, and six added roots in two three-root disks at X-value 5/6, all with derivative value 99/2. There is no zero. The sum of derivative valuations is 5508; this is only a consistency corollary, not an additional global theorem.

## 2. Scope audit and inherited credit

The accepted complete short-tail assembly and its accepting review cover exactly n=c p^r+d with r>=2, 1<=c<p, 0<=d<p. The target has base-p digits 2020. Its intermediate digit 2 is not an allowed low digit; 2p is not d<p. It is not a pure power or a single-leading-digit degree. The latest accepted intermediate theorem is only n=2p^3+p (digits 2010), not arbitrary intermediate digits.

The retained complete first-two-digit theorem means b<p^2, not arbitrary two occupied base-p positions. The retained p-block, third-block, fourth-block, fixed p=3 degrees, fixed order-9/order-25 statements, and pure-power/local guards do not already imply the target. This is a bounded audit of the retained accepted source chain, not a global literature or originality search. No existing accepted family is relabeled as new.

The following ingredients remain inherited mathematics: the original identities; the elementary p-block coefficient lemma; the general leading-digit full-disk coefficientwise lemmas; and the b=2p separating-residual construction. The current work is their bounded perturbative combination at n=2p^3+2p. For the b=2p residual, Section 6 supplies a full direct argument rather than resting on unresolved original-byte provenance.

### Documentary distinction

The latest accepted 2010 author manifest is SHA-256 3b560b06a3c8c635c771adf31f05c70917fed370266e7c73d71d5b7005787d12. Its accepting review manifest is 6ce8b81464ad0be29fcbf504ad302f7d07a2ad5f25111922a7484ce8879e9fc6. Both identities were freshly checked. A fresh read-only source audit also verifies all listed entries of those two complete manifests and of the original general-author and accepting-review manifests, plus all 17 original-location bindings inherited from the 2010 source packet.

The accepted-history comparison archive has SHA-256 c86929554da6cba650c0eb13ede9384e1515cfd220522983e0031e39331aa5fe. Its retained b=2p REPORT.md snapshot has SHA-256 00a4ad13b0726205f3dd6515a4f4c6e9687622c738efdb3df39360b6bcf593db, whereas its historical review cites original author report 6b27fcbdc7aae652afae91fa9e1a8baf84270ef57af75c44c5f35288541686da. These are not identical bytes. This report does not assert that the original b=2p author bytes or original complete package were recovered or verified, nor automatically extend historical byte acceptance to the retained snapshot. Actual retained bytes, the citation, and this limitation are recorded separately. The needed short proof is reconstructed below, while its historical mathematical credit stays inherited.

## 3. Inherited high-disk inputs and legal specialization

Set A=P_(2N), M=P_(2N-1), and a0=1-q^(2N). The accepted general adjacent-criterion report, Sections 2-5, and its accepting review give the following unconditional coefficientwise statements at c=2,r=3, including p=3:

- On each D_a, A has weight K and residual a nonzero scalar times Zbar^2+1, where Zbar=gamma_a Y^L, gamma_a!=0.
- M has weight E and residual a nonzero scalar times Zbar.
- The ORIGINAL ordinary A' has weight D and residual a nonzero scalar times Zbar.
- The ORIGINAL ordinary M' has weight at least E.
- A has exactly 2L boundary roots per D_a, exhausting degree 2N, and v(A(0))=K.

At every point on the residual equation Zbar^2+1=0, therefore, M and A' have exact values E and D. These are full-disk coefficientwise facts, applicable at new roots, not statements available only at old A roots. They are not obtained by differentiating an inseparable residual.

The current packet preserves the exact documentary author and accepting-review snapshots and their original-location bindings from the accepted 2010 packet. Their roles and individual hashes appear in SOURCE_BINDINGS.json. Selected snapshots are not represented as complete copies of their original packages.

The strict degree bound is

    2p^3+2p < p^4 <= p^s,
    p^4-(2p^3+2p)=p[(p-2)p^2-2]>0,

including p=3. Every recurrence edge and q-factorial used is nonzero. For 1<=j<p^s,

    v(1-q^j)=p^ord_p(j).

In particular v(a0)=N and v(1-q^(2N+p))=p. All actual ordinary derivatives are taken in characteristic zero before reducing.

## 4. Exact double-block tail and the correct high-scale bounds

For 1<=j<=2p-1 write b_j=1-q^(2N+j). Define f_0=1, f_1=X, g_0=0, g_1=1, and

    f_(j+1)=X f_j-b_j f_(j-1),
    g_(j+1)=X g_j-b_j g_(j-1).

Put f=f_(2p), g=g_(2p). Induction in the ORIGINAL recurrence gives the polynomial identity

    P_n=f A-a0 g M.                                      (4.1)

Here f is the continuant on tail vertices 1,...,2p and g is that on vertices 2,...,2p. No division by g or M is made.

We record bounds for any disk on which the coefficientwise weight of X is x>=1. For an even (p-1)-vertex block with only valuation-one internal edges, the X^(2j) coefficient has value at least m-j. Its constant is a unique perfect matching, hence has value exactly m and nonzero normalized residue. Therefore its weight is m with constant initial, and its ordinary derivative has weight at least m-1+x. An odd (p-2)-vertex block similarly has weight at least m-1+x and ordinary derivative weight at least m-1.

The inherited p-block fact is

    P_p=X^p+lambda X+sum_(odd j,3<=j<=p-2) e_j X^j,
    v(lambda)=p-1, lambda/t^(p-1) -> c=(-1)^((p+1)/2),
    v(e_j)>=p-1.                                       (4.2)

It is a mixed-characteristic coefficient statement. For orientation, its derivation uses [p choose j]_(1+t)=(-1)^(j-1)t^(p-1)/j+O(t^p) modulo p, the exact H/P Laurent identity, and the ORIGINAL H_p'(-1), not a derivative of a Frobenius residual. The working precision p-1 is below e. A full such derivation is retained in the accepted 2010 source.

If a p-block's edges are shifted by an exponent u with v(1-q^u)>=p, its coefficient of X^(p-2h) differs from that of P_p by value at least p+h-1. This follows by telescoping each h-edge matching, with one changed edge of value at least p and h-1 other edges of value 1. At weight x>=1, the block consequently has weight at least p-1+x, and its original derivative has exact value p-1 with constant initial c after normalization. The derivative bound includes the factor p in the leading term: e+(p-1)x>p-1.

Split the tail into its two p-vertex blocks U and V. Let E0 be U with last vertex removed, E1 be V with first vertex removed, R0 be U with first vertex removed, and T0 be U with both endpoints removed. Their edges have exactly the types just discussed. U is shifted from P_p by 2N (edge difference value N); V is shifted by 2N+p (edge difference value p). The exact joining identities are

    f=U V-b_p E0 E1,
    g=R0 V-b_p T0 E1.                                  (4.3)

Since v(b_p)=p and E0,E1 have constant normalized units, the second term in f has weight p+2m=2p-1. The first has weight at least 2p-2+2x>=2p. Hence

    weight(f)=2p-1, with constant nonzero initial,
    weight(f')>=2p-2+x.                                (4.4)

The derivative bound follows by differentiating both exact products in (4.3) and retaining the integer factors.

For g, the first product has weight at least m+p-1+x, and the joining term has weight at least p+2m-1+x, higher by m. For g', the term R0 V' has exact weight m+p-1 and constant initial. The term R0' V is higher by at least 2x-1, while the differentiated joining terms are higher by at least m. Therefore

    weight(g)>=m+p-1+x,
    weight(g')=m+p-1, with constant nonzero initial.    (4.5)

These comparisons are strict also when p=3 and m=1. No presumed residue unit d!! at d=2p was used.

Indeed the old d<p lemma does not extend here: the old shallow Hermite recurrence gives the tail residual Z^(2p), and (2p-1)!! contains p. The new constant scale is 2p-1, not the short-tail scale p. The failure of the old reduction is a method obstruction, not a characteristic-zero repeated-root claim.

## 5. All 2N high roots, their ordinary derivatives, and no zero

On D_a, let x=1 for a!=0 and x=rho for a=0. By (4.4), f A has weight K+2p-1 and its residual is a constant unit times that of A. The correction a0 g M has weight at least N+m+p-1+x+E. Its gap above the principal term is

    N/2+m-p+x > 0.                                    (5.1)

This is strict for every odd p; its minimum occurs at x=1. Hence P_n has the same nonzero-constant, degree-2L boundary residual as A on each old disk. Newton/Weierstrass counting gives exactly 2L boundary roots in each D_a, counted with multiplicity before simplicity is proved.

At each such new root, M and A' have values E,D and M' has value at least E. Since f is nonzero, use (4.1) only as A=a0 gM/f. Differentiate in the original variable:

    P_n'=f A'+f' A-a0 g'M-a0 gM'.                     (5.2)

The first term has exact value

    2p-1+D=N+E+p-1.                                  (5.3)

The other three terms have respective lower bounds

    N+E+m+p-2+2x,
    N+E+m+p-1,
    N+E+m+p-1+x.

Their gaps above (5.3) are m-1+2x, m, and m+x, all strictly positive. Thus f A' is uniquely minimal, giving the stated ordinary derivative value at every high root. In particular no cancellation class remains. The root equation does not require g!=0; if g vanishes the f'A term only becomes still smaller in magnitude.

Both g and M are odd. Consequently P_n(0)=f(0)A(0), with value 2p-1+K, and is nonzero. Equivalently the central normalized residual has a nonzero constant. No exact zero or extra central interior root is counted.

## 6. Reconstructed inherited b=2p separating residual

This section directly reconstructs the known short argument, avoiding any assertion that transformed historical bytes inherit the original review's hash acceptance. It is not new mathematical credit.

For the UNSHIFTED recurrence let T=P_(2p), U0=P_p, V0 the p-vertex block on p+1,...,2p, and R the product of the two (p-1)-vertex endpoint blocks. Then

    T=U0 V0-u_p R, u_p=1-q^p.

Write h(X)=X^p+lambda X with lambda as in (4.2), and U0=h+J. Then J is odd, has degrees 3,...,p-2, and coefficients of value at least p-1. At p=3 it is identically zero. The odd polynomial Delta=V0-U0 has degree <=p-2 and coefficients of value at least p, by the edge shift. The X^(2j) coefficient of R has value at least p-1-j. Its constant is nonzero with value p-1.

Define

    C=-T(0)=u_p R(0)=product_(j=1)^p(1-q^(2j-1)),
    kappa^2=C, h(a)=a^p+lambda a=kappa,
    ell=2p-1/2.

Here v(C)=2p-1 and v(kappa)=p-1/2. Every solution a has v(a)=alpha: the Newton polygon has endpoints (0,p-1/2),(p,0), and the middle point (1,p-1) strictly above the segment. Choose one a in a finite complete extension. The negative center -a corresponds to -kappa. Their distance has value alpha<1, so their radius-one disks are disjoint.

On X=a+tZ, coefficientwise,

    weight(h)=p alpha=p-1/2,
    weight(J)>=p-1+3alpha>p,
    weight(Delta)>=p+alpha>p.

Expanding T-h^2+C, the terms 2hJ, J^2 and Delta(h+J) have weight strictly above ell. For the joining difference,

    weight(u_p(R(X)-R(0)))
        >=min_(j>=1)(2p-1-j+2j alpha)
        =2p-1/p > ell.

The last strict gap is 1/2-1/p>0, including 1/6 at p=3. These are coefficientwise bounds, not merely point evaluations.

The exact binomial expansion gives

    h(a+tZ)-kappa=t^p Z^p+lambda tZ
       +sum_(j=1)^(p-1) binom(p,j) a^(p-j)t^j Z^j.

Every mixed term has weight at least e+(p-j)alpha+j>p. Hence (h(a+tZ)-kappa)/t^p reduces to S(Z)=Z^p+cZ. Its square has weight at least 2p>ell. It follows that

    T(a+tZ)/(2 kappa t^p) -> S(Z)=Z^p+cZ.              (6.1)

The same formula holds at (-a,-kappa). All normalized coefficients are integral. The p roots of S are the distinct residues i r, r in F_p, because i^(p-1)=-c. This explains the two p-root disks and the separating scale, but we will apply it to the full perturbed polynomial in Section 7.

We also verify the ORIGINAL ordinary derivative independently. At every x of value alpha,

    U0(x)/x^p -> 1, V0(x)/x^p -> 1,
    U0'(x)/t^(p-1) -> c, V0'(x)/t^(p-1) -> c.

The leading derivative p x^(p-1) includes e, and every higher odd lower term is strictly above p-1. Delta' has coefficient values at least p. The joining derivative u_p R' has value at least 2p-2+alpha, strictly above 2p-3/2 by alpha-1/2>0. Therefore

    T'(x)/(2c t^(p-1)x^p) -> 1,
    v(T'(x))=2p-3/2.                                 (6.2)

This is ordinary characteristic-zero differentiation before reduction, not an attempt to differentiate the inseparable first residual Z^(2p)-1.

## 7. Perturbation by the large leading block and all added roots

Work on either B disk from Section 6. It has X-Gauss weight alpha, and every old A root has X-value at least 1. Thus its distance from every point of this disk has value alpha. Monic factorization of A proves

    weight(A)=2N alpha,

with constant nonzero normalized initial on the entire disk. In particular A has no zero here and its reciprocal is a restricted analytic unit after scalar normalization.

An elementary bound suffices for M and g. Every edge of either continuant has value at least 1. A matching contributing degree d-2h therefore has weight at least h+(d-2h)alpha. Since alpha>1/2, the minimum for an odd degree d is attained at h=(d-1)/2. Hence

    weight(M)>=N-1+alpha,
    weight(g)>=p-1+alpha.                             (7.1)

No old high-disk M estimate is illegally extended to a larger disk. The bounds (7.1) are new direct matching estimates at the actual alpha scale.

Set Rbig=a0 gM/A, an analytic function on this disk. By (7.1),

    weight(Rbig)>=V=N+(p-1+alpha)+(N-1+alpha)-2N alpha
                       =p^2+p-1/p.

The strict comparison needed is

    V-ell=p^2-p+1/2-1/p>0.                            (7.2)

For the shifted f versus unshifted T=P_(2p), every edge difference has value N. In an h-edge matching, telescope one changed edge and h-1 unchanged factors, each of value at least 1. For 1<=h<=p, the difference coefficient at X^(2p-2h) has value at least N+h-1. At X-weight alpha this gives

    weight(f-T)>=N+p-1>ell,
    N+p-1-ell=N-p-1/2>0.                              (7.3)

Thus F/A=f-Rbig has exactly the same normalized residual (6.1) as T. Simple-root Hensel lifting gives p distinct roots in B_+ and p in B_-, each reducing to a different root of S in its scaled coordinate. Both disks are disjoint from every old disk, since alpha<1. Distinct residues give within-disk difference value 1; opposite disks give distance alpha. These roots all have X-value alpha.

For the original ordinary derivative, differentiating a restricted analytic expansion on a radius-one disk loses at most 1 in weight: integer coefficient multipliers have nonnegative valuation. Consequently

    weight(Rbig')>=V-1>ell-1,
    weight((f-T)')>=N+p-2>ell-1.

The ORIGINAL T' has exact value ell-1=2p-3/2 by (6.2), at every point in these disks. Hence f'-Rbig' has that same exact value. At a root, the term A'(f-Rbig) vanishes EXACTLY, so

    P_n'=A(f'-Rbig'),
    v(P_n')=2N alpha+2p-3/2.                          (7.4)

Every added root is simple. The disjoint count 2N+2p equals the monic degree n, so these and the already certified high roots exhaust the polynomial. No extra root or zero is left to inspect.

## 8. p=3, phases, H, and the original kernel

At p=3,

    N=27, L=9, m=1, rho=5/2, alpha=5/6,
    K=81, E=135/2, D=183/2,
    ell=11/2, V=35/3, V-ell=37/6.

The least high-root correction gap is N/2+m-p+1=25/2. The three ordinary-derivative gaps are at least 2,1,2. The shifted-tail gap N-p-1/2 is 47/2. In the reconstructed separating residual the joining error gap remains 1/6. Thus every comparison is strict at the boundary p=3, s=4, without dividing by 3 or importing a p>=5-only lemma. There are 54 high roots with derivative 193/2, six added roots with derivative 99/2, and P_60(0) has value 86.

All arguments use the actual t=q-1 and e=(p-1)p^(s-1), actual integer recurrence coefficients, legal nonzero-edge specialization, and full coefficientwise inequalities. The p-block fact is an accepted mixed-characteristic input, not merely a formal mod-p assertion. The p=3 finite controls are not a substitute for the universal argument. Thus every s>3 and every characteristic-zero primitive phase is covered by the proof.

All P roots have positive value, so none equals +/-2. The unchanged exact identity is

    H_n(v0^2)=v0^n P_n(v0+v0^(-1)).

The analytic branch near v0=i provides an isometry between the full P-root neighborhood and the H-root neighborhood at -1, since p is odd. The n P roots correspond bijectively, preserving multiplicity, to all n H roots; H_n(0)=1. At a root the exact original derivative identity is

    H_n'=v0^(n-2)[(n/2)P_n+(v0-v0^(-1))P_n'/2].

Its P_n term vanishes and the remaining multiplier is a unit. Therefore H_n is squarefree with the same rootwise derivative valuations. This does not assert equality of normalized units in P and H.

Consecutive original P polynomials have no common root: backward propagation through the nonzero recurrence edges would contradict P_0=1. At every P_n root xi, the original Christoffel-Darboux identity gives

    sum_(j=0)^(n-1) P_j(xi)^2/w_j
       =P_n'(xi)P_(n-1)(xi)/w_(n-1) != 0.

No Hermitian positivity, complex interlacing, or altered kernel is used. Injective algebraic p-adic embeddings transfer nonvanishing to the original characteristic-zero phases. There is no p=2, s<=3, arbitrary intermediate digit, odd-composite, arbitrary-degree, global F020/F023, FFT-speed, or historical-novelty claim.

## 9. Fresh controls, corrections, and independent-review boundary

Fresh check_controls.py implements narrow polynomial arithmetic from scratch. It does not import or execute any supplied source checker. The completed normal and optimized runs each pass 5,210 explicit checks and produce byte-identical JSON. They include:

- Original p-block and 2p-block series, both exact joining identities, ordinary derivatives, high-scale constant initial and derivative units, first alpha residual, full translated residual error before imposing the auxiliary center relation, and negative shallow controls for p=3,5,7,11,13,17,19. All tested t-precision thresholds are below the actual least e for s=4; the universal mixed-characteristic statements remain proved in the report.
- Exact rational positive-gap, count, derivative, zero, and endpoint ledgers at all 45 odd primes through 199.
- Original full recurrence, transfer and differentiated transfer, and H/P identity at all 54 primitive 81st phases in F_163, plus three primitive phases each for orders 243 and 625. The algebraic-square CD polynomial identity is checked at all 54 order-81 phases.

One bad finite reduction is retained: p=3,s=4, modulus 163, primitive base q=4, phase exponent 70 has gcd degree 2 at n=60. The other 53 order-81 phases and all six other fixtures have gcd degree zero. This is a negative control against promoting arbitrary finite-characteristic bad reduction to a characteristic-zero exception. Every tested exact identity holds at that bad reduction as well.

Two pre-freeze diagnostic corrections are transparent. First, an initial documentary assertion expected the historical b=2p original report hash, but detected the retained transformed snapshot mismatch. The script now preserves the actual bytes and limitation, and Section 6 proves the needed fact directly. Second, an early handwritten simplification of V was lower by 1; the rational control rejected equality. The corrected exact V is p^2+p-1/p, making the strict gap stronger. Neither correction required changing the theorem or relying on an unsupported hypothesis. No failed control is hidden as a passing run.

The author communicated the intended proof architecture to the separate reviewer before final freeze. The reviewer owns independent acceptance or rejection of the final bytes. This report, source binding, and its finite tests are a candidate, not independent certification. No public artifact, permission, table, or repository was changed.
