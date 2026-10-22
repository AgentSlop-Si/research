# Independent bounded review: n = 2p^3 + p

21 October 2026 UTC. **ACCEPTED WITHIN THE EXACT STATED SCOPE.** Final byte bindings are recorded in VERDICT.json and SOURCE_AUDIT.json. This report does not accept a later revision, a transformed public package, or any external publication.

The accepted candidate manifest SHA-256 is 3b560b06a3c8c635c771adf31f05c70917fed370266e7c73d71d5b7005787d12. Its REPORT.md is 20,193 bytes, SHA-256 1f6ccc014b3eaf811af03a68968794b3e40e163dab2a8d40197cb9df9e10878a. All 30 listed files, the seal, the complete 32-file inventory, and all 17 exact documentary snapshots were independently checked. Original full general-author and accepting-review manifest entries were verified at their source locations; the partial snapshots are not passed off as complete packages.

The scope is every odd prime p, every integer s>3, and every characteristic-zero primitive p^s-th phase q, with n=2p^3+p. The original recurrence is P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1); H_n is the original Gaussian polynomial; derivatives are ordinary characteristic-zero derivatives; the kernel uses algebraic squares and the original w_j=product_(u=1)^j(1-q^u).

No producer or dependency program was executed. Only this reviewer's fresh programs were run. No source was modified and no external write was made. Pre-freeze mathematical discussion was substantive and is disclosed below; it is not misrepresented as a wholly blind review.

## 1. Prior scope and the failed short-tail extension

I first read the accepted complete short-tail map and its final accepting independent review. Their exact common rectangle is n=c p^r+d, r>=2, 1<=c<p, 0<=d<p. The current target has base-p digits 2010 and cannot be represented in that rectangle. Its d=p is not an allowed low digit.

I also read the retained historical first-two-digit theorem and its accepting review directly from the intact accepted comparison archive. They cover b<min(p^2,p^s), not two nonzero digits in arbitrary positions. The earlier p-block and third-block theorems have b<2p and b<3p, and the retained fourth-block/fixed small-p statements do not cover this target. Pure-power and single-leading-digit statements do not cover it either. Thus no theorem family from those audited sources is re-credited here. This is a bounded source-scope finding, not a global historical originality search.

The p-block coefficient lemma is inherited and independently rederived in the candidate. It is not new credit. The accepted adjacent-leading-digit report supplies unconditional full-disk coefficientwise facts for A=P_(2N), M=P_(2N-1), A', and M'; its separate criterion for degree 2N+1 is not imposed as a hypothesis on the new degree.

The old d<p argument genuinely fails: the residual tail Hermite polynomial at d=p is Z^p, the constant p!! is not a residue unit, and the full shallow residual is Z^(2N+p). There are no roots of value 1/2. Neither separable shallow Hensel lifting nor the old unit quotient V/T can be reused. The new proof resolves that failure with a different scale, not by ignoring it.

## 2. Normalization and inherited facts

Use t=q-1, v(t)=1, e=v(p)=(p-1)p^(s-1), N=p^3, beta=p, L=p^2, m=(p-1)/2, B=3(p-1)p^2/2, K=N+2B, E=N/2+2B, D=N+E-p. The correct old radius is rho=(2p-1)/2, not p/2 and not a radius obtained from beta=p^ceil(3/2). The added-tail scale is eta=(p+1)/2, and eta<rho for every odd prime including p=3.

The geometric centers are x_a=i(q^(a/2)-q^(-a/2)), 0<=a<p, with i^2=-1 and square roots near 1. Distinct centers have distance valuation 1. In the original H coordinate they are -q^a, under the branch v0 near i in H_b(v0^2)=v0^b P_b(v0+v0^(-1)). The coordinate maps are analytic isometries because p is odd.

The accepted general coefficientwise source gives on each D_a={v(X-x_a)>=rho}: weight(A)=K with residual a unit times Zbar^2+1; weight(M)=E and weight(A')=D, both with residual a nonzero scalar times Zbar; weight(M')>=E; Zbar=alpha_a Y^L. The A residual has degree 2L and nonzero constant. Consequently A has exactly 2L roots on each boundary and these p disks exhaust its degree. At every point satisfying the residual equation Zbar^2+1=0, including new roots, M and A' have exact values E and D. This is not a statement restricted to old roots.

All needed edges are nonzero: 2p^3+p<p^4<=p^s. Every valuation of an edge below the root order is exactly p^ord_p(j), and v(1-q^(2N))=N. No p>=5-only correction theorem is imported at p=3.

## 3. Exact shifted tail and its genuine ordinary derivative

Let a0=1-q^(2N), b_j=1-q^(2N+j), and define exact continuants f_j,g_j by the original three-term recurrence, starting (f_0,f_1)=(1,X) and (g_0,g_1)=(0,1). With f=f_p and g=g_p,

    P_n=f A-a0 g M.

The old p-block calculation gives P_p=X^p+lambda X+sum e_k X^k, where v(lambda)=p-1, lambda/t^(p-1) has residue c=(-1)^((p+1)/2), and every other lower coefficient has value at least p-1. I checked the Gaussian coefficient derivation and its sign: normalized H_p'(-1) has residue -1, the P/H multiplier at X=0 is i^(p-1), and therefore the normalized P_p'(0) residue is -i^(p-1)=c. The integer Laurent substitution is injective, so this is coefficientwise in X. The precision p-1 is below the actual e for every s>3.

Each shifted edge differs from the unshifted edge by a term of value N. A matching term with h edges shows that the coefficient of X^(p-2h) in f-P_p has value at least N+h-1. On any X disk of Gauss weight at least 1, the whole difference has weight at least N+m and its original derivative at least N+m-1. Thus f' has exact value p-1 throughout v(X)>=1. All other terms of P_p' have strictly greater value, including the leading pX^(p-1). This derivative is taken in characteristic zero first.

The maximal matching of g uses the even edges, so g has weight m and nonzero constant initial (p-1)!!. Its derivative satisfies weight(g')>=m-1+x when the X weight is x>=1. No cancellation in g is needed for this bound.

At X=tZ, f/t^p reduces to Z^p+cZ. Its p simple roots are ia, a in F_p. Hence f has precisely one root delta_a in each of those residue classes; delta_0 is exactly zero. At a noncentral old disk the k=1 term of the original Newton expansion of H_p is uniquely minimal, of value F=(3p-1)/2. Every k>=3 term is higher, and the k=p term has value p-1+rho>F. This works at p=3 without an omitted term. Consequently f has constant nonzero initial of value F on D_a, a!=0. Monic factorization then yields

    v(delta_a-x_a)=F-(p-1)=eta, a!=0.

Thus all noncentral added-tail centers are outside the old rho disks. Centrally f/X, not f, is a unit after scaling by t^(p-1). The exact zero does not separate away from the central disk.

## 4. High-root count, zero, and all competing derivative terms

On a noncentral old disk, fA has weight K+F; a0 gM has weight at least K+N/2+m. The correction gap is N/2-p>0. Hence the P_n residual is a unit times the old A residual, with exactly 2L boundary roots counted with multiplicity.

On the central disk, divide the exact odd polynomial by X:

    P_n/X=(f/X)A-a0 g(M/X).

The first term has weight K+p-1. Since weight(M/X)>=E-rho, the second is higher by at least N/2-rho-m>0. The quotient therefore has exactly 2L boundary roots and a nonzero constant residual. At zero,

    v(P_n'(0))=K+p-1.

This proves one simple exact zero strictly inside D_0, in addition to its 2L boundary roots, and does not double-count it.

At any nonzero high root, use the exact root equation A=a0 gM/f in the fully differentiated original identity

    P_n'=f A'+f' A-a0 g'M-a0 gM'.

The f'A term is uniquely minimal. On a noncentral disk its value is N+E-1, and each of the other three terms is higher by at least eta. On the central boundary its value is N+E-p/2; the three other gaps are respectively 3m, 4m, and rho. They are all strictly positive even at p=3. This establishes every high root as simple. In particular, no derivative cancellation class remains to be lifted.

These are rootwise values obtained from the original root equation. The proof does not assert the same derivative valuation throughout an old disk and does not differentiate Zbar^2+1 as a substitute.

## 5. Independent check of the new eta-disk carry bound

The substantive new estimate needed outside the old disks is

    weight(M)>=E_eta=3N-2p^2

on every eta disk around an old center. I reconstructed this proof directly rather than accepting a finite prime pattern.

Each Newton product has weight at least T_eta(k)=k+m floor(k/p). Write k=2l+1, 0<=l<N, l=a_0+a_1p+a_2p^2. Digit complementation gives W(N-1-l)=W(N-1)-W(l). For carries eps_0,eps_1,eps_2 in doubling l and adding 1, the exact score is

    R_eta(2l+1)-W(l)
      =-a_0-p a_1-p a_2+m eps_0
         +p(p-1)eps_1+p^2(p-1)eps_2.

For fixed carries, choose the smallest admissible digits. The eight maxima are 0, 0, p(m-1), pm, p^2(p-1)-p(m+1), the same value again, p^2(p-1)-p, and p^2(p-1), with the last attained only for carry pattern 111 and digits a_0=a_1=a_2=m. Thus the score is at most p^2(p-1), with unique equality k=N. Subtracting from the exact factorial weights gives E_eta.

This also exposes why the original high-disk M estimate cannot simply be asserted on a larger disk: a separate cap and carry analysis is needed. The author supplies it. Only the lower bound is required for the subsequent perturbation proof, so no unproved unit assertion about M at a tail root is used.

## 6. Exhaustion by the separated tail disks

For each a!=0 take T_a={v(X-delta_a)>=rho}. Since v(delta_a-x_a)=eta<rho, it is disjoint from D_a and from every other old disk. It is also disjoint from T_b for b!=a.

All accepted A roots have fixed distances on T_a: 2L have distance valuation eta, and 2L(p-1) have distance valuation 1. Hence A has weight J_A=3N-p^2 and constant unit initial there. With R=a0 gM/A, the new eta bound gives weight(R)>=V=N-p^2+m. The strict gap is

    V-(p-1+rho)=p^3-p^2-(3p-2)/2>0.

Monic factorization of f gives one linear residual on T_a at weight p-1+rho. Therefore f-R, and hence P_n=A(f-R), has exactly one root there. Differentiating a normalized restricted analytic expansion loses at most rho, so weight(R')>=V-rho>p-1. At the root, the A'(f-R) term vanishes exactly, yielding

    v(P_n')=J_A+p-1=3N-p^2+p-1.

There are exactly p-1 such simple roots. Combined with 2p^2 central high boundary roots, 2p^2(p-1) noncentral high boundary roots, and one exact zero, their disjoint total is 2p^3+p. This degree exhaustion rules out any omitted cluster. No blanket assertion that all p added roots separate is used.

## 7. Small p and original H/kernel conclusions

For p=3 the proof gives n=57, rho=5/2, eta=2, K=81 and E=135/2. There are 18 central high roots of derivative value 93, 36 noncentral high roots of derivative value 187/2, one zero of derivative value 83, and two separated tail roots of derivative value 74. Their sum of counts is 57 and the derivative-value sum is 5271. The eta estimate is E_eta=63, J_A=72, V=19, with perturbation gap 29/2. All inequalities remain strict.

Every original P root reduces to zero and is therefore different from +/-2. The analytic branch near i gives a multiplicity-preserving correspondence with all H roots, which reduce to -1. At a root, the original H derivative identity has a vanishing P prefactor term and a unit multiple of P'. It preserves derivative valuations, not necessarily normalized units. P zero corresponds to H root -1; H_n(0)=1.

Consecutive P polynomials cannot share a root because every recurrence edge is nonzero, and backward recurrence would contradict P_0=1. At a P_n root the unchanged identity is

    sum_(j=0)^(n-1) P_j(xi)^2/w_j
      =P_n'(xi)P_(n-1)(xi)/w_(n-1).

All factors on the right are nonzero. This is the algebraic-square kernel, not a positive/Hermitian kernel. The argument uses actual t, actual e, legal integer specialization and the accepted all-phase coefficients; it is uniform over s>3 and every primitive phase, not inferred from sample phases.

## 8. Fresh controls, independence, and consumption limit

The fresh reviewer controls check 200 carry-pattern maxima through p=101, 82,142 exact odd Newton indices through p=31, 50 complete high-root derivative-gap rows, complete count and zero diagnostics, and direct p-block/center/shallow recurrences at p=3,5,7,11,13. They use explicit failures rather than Python assert, and normal and optimized runs are compared byte for byte.

Original P/H finite-field controls cover 54 primitive 81st phases modulo 163 and three phases each for orders 243, 625 and 2401. At n=57, modulus 163, q=4, phases q^28 and q^29 have repeated reductions of gcd degree two; the other 52 phases are simple. The original algebraic-square kernel identity is checked directly for all 54 phases. The two bad reductions are retained as negative controls against treating arbitrary finite-characteristic reductions as characteristic-zero exceptions. At least one nonzero specialization certifies each fixed characteristic-zero cyclotomic fixture by irreducibility/conjugacy, but none of these finite controls substitutes for the all-p, all-s proof.

I independently developed the high-root derivative comparison and a different weaker global M bound during the pre-freeze exchange. The author had already derived and communicated the stronger eta-disk lemma before that alternative was supplied, and did not use the alternative. The accepted report retains its own complete eight-carry proof. No mathematical repair was required. This review transparently records the exchanged mathematics rather than claiming there was no interaction.

The acceptance is only for the frozen original statement, proof, and source bindings. It does not close F020/F023, settle another intermediate digit or arbitrary degree, claim historical novelty or faster FFT complexity, approve a future public projection, or establish any table/repository mutation. The existing accepted families remain credited to their original sources.
