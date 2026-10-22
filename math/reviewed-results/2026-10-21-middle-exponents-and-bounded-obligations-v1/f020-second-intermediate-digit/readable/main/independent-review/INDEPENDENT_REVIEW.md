# Independent bounded review: n = 2p^3 + 2p

21 October 2026 UTC. ACCEPTED WITHIN THE EXACT STATED SCOPE. The frozen author manifest is SHA-256 ebff60ce117ad3f9f7830e1053b1edf02f0e6733cf9571ca80e4b6d25544e05e. The author REPORT.md is 22,231 bytes, SHA-256 3e7694e17870344c43e7e9702212ad7a89f86dce57704cca663fe4d353a2f5da. All 40 manifest-listed files and the exact 42-file inventory including manifest/seal pass. This report accepts only these exact author bytes, not later revisions, transformed public artifacts, or external publication.

The scope is every odd prime p, every integer s>3, and every characteristic-zero primitive p^s-th root q, at degree n=2p^3+2p. The unchanged definitions are P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1), the Gaussian polynomial H_n, ordinary characteristic-zero derivatives, and the algebraic-square Christoffel-Darboux kernel with w_j=product_(u=1)^j(1-q^u).

No candidate or dependency program was executed. I independently wrote and ran the controls in this review directory. Sources and the candidate were read, not changed. No external write was made. The author shared the intended architecture before the final freeze; I independently reconstructed its decisive estimates and later read the whole report. This is disclosed rather than represented as a wholly blind review. No mathematical repair was required.

## 1. Bounded scope and the historical-byte discrepancy

The accepted short-tail map and its accepting review cover n=c p^r+d with r>=2, 1<=c<p, and 0<=d<p. The target's digits are 2020, so it is outside that rectangle. The accepted first intermediate-digit result is specifically 2010, not an arbitrary intermediate digit theorem. The historical first-two-digit range means b<min(p^2,p^s), and the smaller p-block/fixed-degree ranges, pure powers and independent local hypotheses do not imply the present symbolic family. These conclusions are a bounded source audit, not a historical priority search.

The p-block coefficient lemma, general leading-digit disk coefficients, and short b=2p separation are inherited mathematical ingredients. The last has a genuine documentary mismatch: the retained archive REPORT.md is SHA-256 00a4ad13b0726205f3dd6515a4f4c6e9687622c738efdb3df39360b6bcf593db, while its original review and verdict cite report 6b27fcbdc7aae652afae91fa9e1a8baf84270ef57af75c44c5f35288541686da. These hashes differ. Original author-byte acceptance is not extended to the retained snapshot, and the original complete short-boundary package is not asserted recovered. I independently verified this discrepancy and the archived snapshot identity. The needed short residual is proved directly in the current report and reconstructed below. Mathematical credit remains inherited despite that reconstruction.

The current result is the bounded combination and perturbation at 2020. It does not close F020/F023, establish other middle digits or arbitrary degree, cover p=2 or s<=3, settle composite orders, assert historical novelty, or yield an FFT/cost claim.

## 2. Original definitions and accepted off-root coefficients

Put N=p^3, L=p^2, m=(p-1)/2, B=3(p-1)p^2/2, K=N+2B, E=N/2+2B, D=N+E-p, rho=p-1/2 and alpha=1-1/(2p). Use t=q-1, v(t)=1, e=(p-1)p^(s-1), and x_a=i(q^(a/2)-q^(-a/2)), 0<=a<p, with the roots of q^a near one.

On every D_a={v(X-x_a)>=rho}, the accepted general leading-digit proof supplies coefficientwise weights K,E,D,>=E for A=P_(2N), M=P_(2N-1), A' and M'. The respective initial polynomials for A,M,A' are nonzero scalar multiples of Zbar^2+1,Zbar,Zbar, where Zbar=gamma_a Y^L. These are full-disk statements, not estimates restricted to old A roots. At any new root with Zbar^2+1=0, M and A' therefore have exact values E,D. No residue-field differentiation is substituted for A' or M'.

A has exactly 2L boundary roots in each D_a, exhausting its degree 2N. Its constant has value K. The centers have mutual distance value one, and rho>1. The strict inequality 2p^3+2p<p^4<=p^s holds even at p=3, so every used recurrence edge and q-factorial denominator is nonzero and v(1-q^j)=p^ord_p(j) throughout the required indices.

## 3. Exact tail and high-scale bounds

With b_j=1-q^(2N+j), define f_j,g_j from the original recurrence and initial values (1,X) and (0,1), respectively. For f=f_(2p), g=g_(2p), a0=1-q^(2N), the exact identity is

    F=P_n=f A-a0 g M.

Splitting the tail at its middle edge b_p gives f=UV-b_p E0E1 and g=R0V-b_p T0E1, with the p-blocks, even endpoint-deleted blocks, and odd double-endpoint-deleted block indexed exactly as in the candidate. I reconstructed those path decompositions; in particular g starts at tail vertex two, not at vertex one.

At X-Gauss weight x>=1, every even (p-1)-vertex endpoint block has weight m and a constant nonzero initial; its derivative has weight >=m-1+x. The odd (p-2)-vertex block has weight >=m-1+x and derivative weight >=m-1. These follow from the number of matched edges, with a unique perfect matching for the even constant.

The inherited original p-block coefficients are X^p+lambda X+J with v(lambda)=p-1, lambda/t^(p-1) reducing to c=(-1)^((p+1)/2), and odd J of degrees at least three with coefficients of value >=p-1. The leading ordinary derivative retains its multiplier p and thus has value e+(p-1)x>p-1. A block shifted by 2N or 2N+p changes each internal edge by a term of value at least p. Telescoping the h-edge products gives coefficientwise error >=p+h-1, so those shifted p-block derivatives still have the constant initial c of value p-1.

Since v(b_p)=p, the joining product in f has weight 2p-1, strictly below UV. Differentiating both exact products proves

    weight(f)=2p-1 with constant initial; weight(f')>=2p-2+x.
    weight(g)>=m+p-1+x; weight(g')=m+p-1 with constant initial.

For g', the term R0 V' is uniquely minimal: R0'V is higher by at least 2x-1 and both differentiated joining terms by at least m. All these gaps are positive at p=3. The old d<p unit-tail argument would be invalid because (2p-1)!! is divisible by p; the displayed 2p-1 scale, rather than p, resolves that failure.

## 4. High roots, every derivative term, and no zero

On a noncentral old disk x=1, and centrally x=rho. The correction a0gM is strictly above fA by N/2+m-p+x>0. Thus the whole polynomial has the same nonzero-constant, degree-2L boundary residual as A in each disk. It has exactly 2L roots there counted with multiplicity before derivative evaluation.

At such a root f is a nonzero unit after scalar normalization, and the root equation A=a0gM/f is legal whether or not g vanishes. Differentiating the original identity gives four terms:

    F'=f A'+f' A-a0 g'M-a0 gM'.

Their values/bounds are

    N+E+p-1,
    >=N+E+m+p-2+2x,
    N+E+m+p-1,
    >=N+E+m+p-1+x.

The last three exceed the first by at least m-1+2x, m and m+x. Hence the first is uniquely minimal, proving all 2N high roots simple with value v(F')=N+E+p-1. This conclusion does not differentiate the Frobenius disk residual.

Both g and M are odd. Thus F(0)=f(0)A(0) has exact value K+2p-1 and is nonzero. There is no zero root, no additional central interior root, and no parity-based carry-over of the preceding 2010 zero.

## 5. Independent reconstruction of the short separating residual

For the unshifted T=P_(2p), use T=U0V0-u_p R. Set h=X^p+lambda X, U0=h+J and V0-U0=Delta. The coefficients of J have value >=p-1 and odd degree >=3; Delta has odd degree at most p-2 and coefficient values >=p. For R, the coefficient of X^(2j) has value >=p-1-j. Its constant is a nonzero product of valuation-one edges.

Set C=-T(0)=u_p R(0), choose kappa^2=C and h(a)=kappa. Then v(C)=2p-1, v(kappa)=p-1/2, and the auxiliary trinomial Newton polygon gives v(a)=alpha. This center is not assumed to be an original T root. Its negative is the corresponding center for -kappa; their distance has value alpha<1.

On X=a+tZ, the respective weights of h,J,Delta are p-1/2, >=p-1+3alpha>p and >=p+alpha>p. Therefore 2hJ,J^2 and Delta(h+J) lie strictly above ell=2p-1/2. The joining error satisfies

    weight(u_p(R(X)-R(0)))>=2p-1/p>ell,

whose sharp stated gap is 1/2-1/p, still 1/6 at p=3. This verifies every coefficient, not merely the value at the center.

The binomial expansion of h(a+tZ)-kappa, divided by t^p, reduces to S(Z)=Z^p+cZ. Every mixed binomial coefficient has valuation at least e, and its monomial weight e+(p-j)alpha+j is strictly above p. Squaring the increment has value >=2p>ell. Hence

    T(a+tZ)/(2 kappa t^p) reduces to S(Z).

The same holds at (-a,-kappa). S has the p distinct roots i F_p and derivative c. The ordinary derivative is separately checked: U0,V0 have initial x^p at v(x)=alpha, while U0',V0' have initial c t^(p-1). The joining derivative is bounded below by 2p-2+alpha, greater than 2p-3/2 by alpha-1/2. Thus

    T'(x)/(2c t^(p-1)x^p) reduces to one,
    v(T'(x))=2p-3/2.

This proof needs no historical original-byte acceptance and is valid at the smallest prime. It remains inherited mathematics, not newly credited short-boundary theory.

## 6. Perturbation on the two outer disks

Every A root has X-value at least one. On either B disk v(X-a)>=1 or v(X+a)>=1, A has weight 2N alpha and a constant unit initial by its monic factorization. It is therefore invertible analytically there. A fresh direct matching bound, not an extension of the high-disk estimate for M, gives

    weight(M)>=N-1+alpha; weight(g)>=p-1+alpha.

Indeed an odd degree-d matching has weight at least h+(d-2h)alpha, minimized at the maximal h because alpha>1/2. Consequently

    Rbig=a0gM/A has weight >=V=p^2+p-1/p.

The exact gap V-ell=p^2-p+1/2-1/p is positive. For the shift f-T, an h-edge matching changes by at least N+h-1. Minimizing its weighted terms yields weight(f-T)>=N+p-1>ell. Therefore F/A=f-Rbig has the same S residual as T in each B disk.

Simple-root Hensel gives p distinct roots in each disk. Distinct S residues yield within-disk difference value one; across disks the difference has value alpha. All these roots have X-value alpha<1 and are disjoint from every old disk. Combined with 2N high roots, their count is the full degree 2N+2p. This establishes exact, not merely lower, disk counts and rules out any unexamined cluster.

Ordinary differentiation of a restricted analytic expansion on radius one loses at most one in coefficientwise value. Thus Rbig' has value >=V-1>ell-1 and (f-T)' has value >=N+p-2>ell-1. The actual T' has exact value ell-1. At an F root, A'(f-Rbig) vanishes exactly, so

    F'=A(f'-Rbig'), v(F')=2N alpha+2p-3/2.

Every outer root is simple. No division by f or M occurs on these disks.

## 7. p=3, every phase, H and the original kernel

For p=3, N=27, K=81, E=135/2, D=183/2, rho=5/2, alpha=5/6, ell=11/2 and V=35/3. There are 54 high roots, 18 in each old disk, with derivative 193/2, and six outer roots in two three-root disks with derivative 99/2. F(0) has value 86. The derivative-value sum is 5508. The outer perturbation gap is 37/6; the short joining gap is 1/6. All strict comparisons survive p=3,s=4.

The proof uses actual mixed-characteristic t and e, integer recurrences and legal specializations throughout. All primitive characteristic-zero phases satisfy those hypotheses. Finite controls do not replace this quantifier.

All P roots have positive value, so none is +/-2. The exact identity H_n(v0^2)=v0^n P_n(v0+v0^(-1)) gives a multiplicity-preserving correspondence on the analytic branch near v0=i, whose two coordinate derivatives are units because p is odd. It accounts for all n H roots, with H_n(0)=1. At roots the original H derivative identity has its P term zero and a unit multiplier of P'. Thus original H is squarefree with the same rootwise derivative valuations.

Consecutive original P polynomials are coprime by backwards recurrence through the nonzero edges. The unchanged diagonal CD identity at a root xi is

    sum_(j=0)^(n-1) P_j(xi)^2/w_j=P_n'(xi)P_(n-1)(xi)/w_(n-1).

All factors on the right are nonzero. These are algebraic squares, never absolute-value squares; there is no appeal to positivity or interlacing. Injective p-adic embeddings transfer the algebraic nonvanishing to every characteristic-zero primitive phase.

## 8. Independent controls and consumption boundary

The reviewer program reconstructs the unshifted p and 2p blocks from the exact original integer q recurrence, converts them to integer t polynomials, and retains mixed-characteristic coefficient factors through e v_p(coefficient). It verifies the entire translated auxiliary polynomial residual before imposing h(a)=kappa, not merely selected coefficients or an already-reduced derivative. It tests p=3,5,7,11,13, separately checks original ordinary derivative and high-tail/neighbor bounds, and checks exact rational ledgers at every odd prime through 103.

Independent finite-field fixtures use all 54 primitive order-81 phases modulo 487 and six order-243 phases modulo 1459. They verify the original transfer, all four differentiated transfer terms, the full polynomial CD identity and original H/P normalization. Their reductions happen to be squarefree; this is not required universally. The author's different modulo-163 fixture at exponent 70 has gcd degree two, correctly retained as bad reduction rather than a characteristic-zero counterexample.

The reviewer mathematical program passes 940 explicit checks. Normal and optimized reviewer runs are byte-identical and use explicit failures, not removable Python assertions. Separate source controls pass 86 checks covering frozen byte identities, exact inventory, all 27 retained documentary snapshots, all 17 inherited original bindings, and the full 2010 author/review and general author/review manifests (30, 8, 13 and 19 entries respectively). Five in-memory negative inventory mutations are rejected. Source normal and optimized outputs are byte-identical too. No supplied code is run. Exact counts, hashes and verdict are recorded in the machine-readable companions.

Acceptance is confined to the pinned candidate and its original stated theorem. A future public projection, repository operation, table annotation or broader theorem requires its own review and authorization. No acceptance of the unrecovered historical b=2p author bytes is implied.
