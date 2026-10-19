# F020 third-block extension: all b < min(3p, p^s)

19 October 2026 UTC. New author-level theorem, submitted for independent review. Canonical owner F020; F023 remains its alias and priority 58 is unchanged. No external write or historical-program execution.

## Result and exact scope

Let p be any odd prime, s >= 1, q a primitive p^s-th root of unity, and

    P_0(X;q)=1, P_1(X;q)=X,
    P_(n+1)(X;q)=X P_n(X;q)−(1−q^n)P_(n−1)(X;q),
    H_n(z;q)=sum_(k=0)^n [n choose k]_q z^k.

Then the actual P_b and H_b are squarefree whenever

    0 <= b < min(3p, p^s).                              (T)

The genuinely new degrees are 2p < b < 3p for s>=2. The accepted b=2p result is used as an explicit local input, not asserted as a new discovery. The proof works uniformly at p=3, including the new degrees b=7,8 for every s>=2. At s=1 the range stays b<p. There is no assertion at b=3p or later.

More precisely, for s>=2 write b=2p+r with 0<=r<p, set

    t=q−1, v(t)=1, alpha=(2p−1)/(2p),
    epsilon=r mod 2, m=(r−epsilon)/2, h=(p−1)/2.

P_b has exactly:

- r−epsilon outer roots of valuation 1/2, with every pairwise distance of valuation 1/2;
- 2p inner roots of valuation alpha, in two p-root clusters, with within-cluster distances of valuation 1 and cross-cluster distances of valuation alpha;
- the additional simple root 0 if and only if epsilon=1.

Every outer root has distance of valuation 1/2 from every inner root and from 0. When present, 0 has distance of valuation alpha from every inner root. The monic degree-2p factor consisting of all inner roots is irreducible over K=Q_p(q). In particular, P_(2p+1)/X is irreducible over K. The full P_b need not be irreducible.

The complete distances give

    v(Disc_X P_(2p+r))
      =p(4p−3)+2pr+r(r−1)/2+epsilon(2p−2).             (D)

The original ordinary-square bilinear Christoffel–Darboux kernel is nonzero at every P_b root throughout (T). These conclusions remain author-level pending independent acceptance. F020 is still open beyond the displayed range; no unrestricted all-A closure is claimed.

## 1. Accepted inputs, normalization, and provenance

The accepted source chain is:

1. `f020_two_digit_hensel_20261019_0124`, independently accepted by `f020_primepower_extension_review_20261019_0124`, establishes the actual-family squarefreeness and bilinear guard for b<min(2p,p^s), the p-block coefficient theorem, and the outer residual recurrence.
2. `f020_boundary_hensel_resolution_20261019_0839`, independently accepted by `f020_boundary_resolution_review_20261019_0840`, establishes the b=2p boundary, its auxiliary centers and exact separating residual, irreducibility, distances, and discriminant.

The second review binds its acceptance to author report SHA-256

    6b27fcbdc7aae652afae91fa9e1a8baf84270ef57af75c44c5f35288541686da

and author manifest SHA-256

    eb31526958e004a90a531f7a857679faa9515fdb50146343fda23a50fbd9c9cb.

The present packet verifies those bindings and all entries of the two boundary manifests. Relevant source reports, verdicts, and manifests are bound in SOURCE_BINDINGS.json. Source bytes remain unchanged. The new contribution is a perturbation argument that transports the accepted separating residual through the entire following partial p-block. It does not rename the accepted boundary work or imply a historical literature-originality search.

Work in K=Q_p(q), with t=q−1 and v(t)=1. For s>=2,

    v(K^×)=Z, v(p)=e=p^(s−1)(p−1),
    u_j=1−q^j,
    v(u_j)=1 if p does not divide j,
    v(u_p)=v(u_(2p))=p.

The value-group assertion follows from the Eisenstein shifted cyclotomic polynomial. The last equality also follows from u_(2p)=u_p(1+q^p), whose second factor reduces to 2. All indices used below are strictly below p^s, since

    2p+r <= 3p−1 < p^2 <= p^s

for every odd p and s>=2. Thus no required edge or norm factor vanishes. The inequality also explains why no extra qualification on r is hidden when p=3,s=2.

Put A=P_p, lambda=[X]A, and c=(−1)^((p+1)/2). The accepted p-block estimate says

    A(X)=X^p+lambda X+E(X),
    v(lambda)=p−1, lambda/t^(p−1) -> c,

where E is odd, uses only powers 3,5,...,p−2, and all its coefficients have valuation at least p−1. E is identically zero at p=3.

Define the accepted boundary constant and centers by

    C=−P_(2p)(0)=product_(j=1)^p u_(2j−1),
    kappa^2=C, a^p+lambda a=kappa.

Every such a has v(a)=alpha, and v(kappa)=p−1/2. In a finite complete extension containing these quantities, put

    L=v(2 kappa t^p)=2p−1/2,
    S(Z)=Z^p+cZ.

The exact accepted boundary statement is coefficientwise integrality and reduction

    P_(2p)(a+tZ)/(2 kappa t^p) -> S(Z).                (1)

The same statement holds at (−a,−kappa). The derivative S'=c is a unit. We use (1) as proved and independently accepted; we do not infer simplicity from an inseparable first residual.

## 2. A coefficientwise bound on the preceding polynomial

For a polynomial in Z, write its valuation for the minimum of its coefficient valuations. The convention for zero is +infinity. Since v(a)=alpha<1, substitution X=a+tZ sends every monomial X^j to a polynomial of coefficientwise valuation at least j alpha. Multiplication and addition obey the usual lower bounds in this coefficientwise valuation.

A continuant with n vertices and all internal edges of valuation 1 has X^(n−2k) coefficient of valuation at least k. This follows directly from its path-matching expansion: each summand has exactly k edges. At any scale with alpha>1/2, this gives

    n=2j:   v(Q(a+tZ)) >= j,
    n=2j+1: v(Q(a+tZ)) >= j+alpha.                    (2)

No claim about the absence of cancellation is needed for these lower bounds.

We need the following new estimate:

    v(P_(2p−1)(a+tZ)) >= h+p alpha.                   (3)

To prove it, split after vertex p. Let U be the (p−1)-vertex block on vertices p+1,...,2p−1, V the (p−2)-vertex block on vertices p+2,...,2p−1, and D=P_(p−1). The exact concatenation formula is

    P_(2p−1)=U A−u_p V D.                            (4)

All edges internal to U,V,D have valuation 1. Thus (2) gives

    v(U(a+tZ))>=h,
    v(V(a+tZ))>=h−1+alpha,
    v(D(a+tZ))>=h.

The p-block theorem and alpha<1 give v(A(a+tZ))>=p alpha. Indeed the X^p term has this lower bound, while every lower odd monomial has valuation at least p−1+j alpha, strictly greater than p alpha for j>=1. The joining term in (4) has lower bound

    p+(h−1+alpha)+h
      =h+p alpha+(h−1/2+alpha).

The equality follows by substituting p alpha=p−1/2. The extra gap h−1/2+alpha is strictly positive, including p=3, where it equals 4/3. Both terms of (4) therefore satisfy (3). This proves a statement about every Z coefficient, not merely the value at Z=0.

## 3. Exact tail block and its leading factor

For 0<=r<p, let F_r be the r-vertex block immediately after vertex 2p, with internal edges

    u_(2p+1),...,u_(2p+r−1).

For r>=1 let G_(r−1) be the final (r−1)-vertex block, with internal edges

    u_(2p+2),...,u_(2p+r−1).

Use F_0=1 and G_0=1. The exact identity is

    P_(2p+r)=F_r P_(2p)−u_(2p) G_(r−1)P_(2p−1).     (5)

At r=0 the joining term is absent. At r=1, (5) is the defining recurrence; induction in r or the matching expansion proves the formula for all r. Thus there is no boundary-index or normalization change.

All these internal edges have valuation 1. Their leading coefficients agree with the classical residual recurrence

    h_0(Y)=1, h_1(Y)=Y,
    h_(n+1)(Y)=Yh_n(Y)+n h_(n−1)(Y)

over the residue field of characteristic p, since u_(2p+j)/t reduces to −j. Consequently, with epsilon and m as in the theorem, put

    d_r=(2m−1)!! if epsilon=0,
    d_r=(2m+1)!! if epsilon=1,
    sigma_r=d_r t^m a^epsilon.                        (6)

The convention (−1)!!=1 covers r=0. All d_r are p-units because r<p. The matching coefficients give, coefficientwise in Z,

    F_r(a+tZ)/sigma_r -> 1.                          (7)

For completeness, F_(2m) has constant coefficient t^m times a unit reducing to (2m−1)!!, and its X^(2j) coefficient has valuation at least m−j. At alpha>1/2 every j>=1 term has strictly higher weight. For F_(2m+1), its linear coefficient divided by t^m reduces to (2m+1)!!, and each X^(2j+1) term for j>=1 has strictly greater weight than m+alpha. Finally (a+tZ)/a reduces to 1 because 1−alpha>0. These observations prove the full coefficientwise assertion (7), including the odd-r normalization by a.

The only needed bounds on G are

    r=2m>=2:   v(G_(r−1)(a+tZ))>=m−1+alpha,
    r=2m+1:    v(G_(r−1)(a+tZ))>=m.                  (8)

They follow from (2) and include G_0=1 when r=1.

## 4. The separating residual survives the entire partial block

Divide (5), after X=a+tZ, by

    N_r=2 kappa t^p sigma_r,
    v(N_r)=L+m+epsilon alpha.                         (9)

By (1) and (7), the product F_r P_(2p) is integral after this division and reduces exactly to S(Z).

For r>0 the joining term vanishes in the residue. In detail, combine v(u_(2p))=p with (3) and (8). For even r=2m>=2 its coefficientwise valuation is at least

    p+(m−1+alpha)+(h+p alpha)
      =L+m+(h−1+alpha).

Its strict excess above v(N_r) is

    Delta_even=h−1+alpha=(p−3)/2+alpha>0.             (10)

For odd r=2m+1 the lower bound is

    p+m+h+p alpha=L+m+h,

whose excess is

    Delta_odd=h−alpha=(p−3)/2+1/(2p)>0.              (11)

The smallest possible gap is 1/6, at p=3 in the odd case. Thus there is no lost equality case at the smallest prime. At r=0, F_0=sigma_0=1 and the joining term is absent, recovering exactly (1).

We have proved the new explicit residual

    P_(2p+r)(a+tZ)/(2 kappa t^p d_r t^m a^epsilon)
       -> Z^p+cZ.                                   (12)

Every coefficient is integral; the normalized constant is zero in the residue; the derivative of the residual is c. Replacing (a,kappa) by (−a,−kappa), including that replacement inside sigma_r, gives the same residual. This is a transport of the accepted auxiliary centers: it does not choose a root of the target polynomial or assume target simplicity.

## 5. All roots, the odd-r zero, and exact distances

After a finite residue-field extension, S(Z)=Z^p+cZ has p distinct roots. If i^2=−1 in that field, those roots are i F_p because i^(p−1)=−c. Simple-root Hensel lifting applied to (12) yields p distinct target roots of form

    a+t z_j,

with pairwise distinct z_j residues. The negative center gives p further roots. Their two discs are disjoint, since v(2a)=alpha<1. This establishes exactly 2p distinct constructed inner roots, each of valuation alpha. Within a disc the difference valuations are 1; between discs they are alpha.

For the remaining roots, choose a square root tau of t. The actual recurrence gives the integral outer scaling

    P_b(tau Y)/tau^b -> h_b(Y).

In characteristic p, h_p=Y^p and the recurrence implies h_(p+j)=Y^p h_j for every j>=0. Hence

    h_(2p+r)=Y^(2p) h_r.                              (13)

For r<p, h_r is squarefree: h_r'=r h_(r−1), and the recurrence with nonzero coefficients 1,...,r−1 excludes common roots of consecutive h's. For r=0, h_0=1 and there are no outer roots. The root 0 occurs in h_r exactly when r is odd, and is then simple, as its linear coefficient is r!!, a p-unit.

The r−epsilon nonzero roots of h_r in (13) are simple, so they lift to r−epsilon distinct roots of valuation 1/2. Distinct residual values give every outer-pair difference valuation 1/2. Their valuations distinguish them from all inner roots and from 0.

When epsilon=1, parity of the exact recurrence makes P_b odd, so 0 is an exact root. It is distinct from every inner and outer root already constructed. We now have

    (r−epsilon)+2p+epsilon=b

mutually distinct roots of a monic degree-b polynomial. This exhausts its degree and proves that every one, including 0, is simple. In particular, we never assume simplicity of the odd-r zero from parity alone. When epsilon=0 the same count without 0 already exhausts the degree, excluding any zero root.

The distances between roots of differing valuations are the smaller valuation. Thus outer-to-inner and outer-to-zero distances have valuation 1/2, while zero-to-inner distances have valuation alpha. This proves the complete root description and squarefreeness of P_b for the new block.

The p=3 cases are especially explicit. Here alpha=5/6 and L=11/2. The r=0 case is the accepted b=6 theorem. At r=1, b=7, the dividing factor has valuation 19/3 and the joining term has valuation at least 13/2, leaving the strict gap 1/6; the seven roots are the six inner roots and the simple root 0. At r=2, b=8, the dividing factor has valuation 13/2 and the joining lower bound is 22/3, leaving gap 5/6; the eight roots are the six inner roots and two outer roots. This covers s=2 as well as every larger s.

## 6. Inner irreducibility and discriminant

The valuation on the algebraic closure of a complete discretely valued field is invariant under its K-automorphisms. The set of all 2p inner roots is therefore Galois-stable. Its monic root polynomial I_r(X) lies in K[X]. It has degree 2p, nonzero constant term, and all its roots have valuation alpha. If a monic K-factor had degree j with 0<j<2p, its constant term would have valuation j alpha. This must be an integer because v(K^×)=Z. But gcd(2p−1,2p)=1 forces 2p to divide j, a contradiction. Thus I_r is irreducible.

The same Galois-stability argument gives

    P_(2p+r)=X^epsilon I_r O_r

with O_r monic of degree r−epsilon and all its roots outer. This proves P_(2p+1)/X irreducible, while making no unsupported irreducibility claim for the full polynomial in later degrees.

Put n=r−epsilon. The discriminant is the product of squared pairwise differences. The inner roots contribute the accepted value p(4p−3), since their complete distances are preserved. Outer pairs contribute n(n−1)/2, and outer-to-inner or outer-to-zero pairs contribute n(2p+epsilon). If 0 is present, its pairs with the inner roots contribute 4p alpha=4p−2. Therefore

    v(Disc P_b)
      =p(4p−3)+n(n−1)/2+n(2p+epsilon)
           +epsilon(4p−2),

which simplifies exactly to (D). As another expression of the same distance calculation, the derivative valuations are

    inner root:  2p−3/2+m+epsilon alpha,
    outer root:  (b−1)/2,
    root 0:      2p−1+m, if epsilon=1.

Summing them over all roots gives (D) again. At p=3 the values for b=6,7,8 are respectively 27,37,40. These are t-normalized p-adic valuations, not ordinary p-adic valuations with v(p)=1.

## 7. Actual Rogers–Szego polynomial and the original kernel

Use the exact accepted identity

    H_b(v^2;q)=v^b P_b(v+v^(−1);q).                   (14)

All u_j have positive valuation, so P_b reduces to X^b. Since p is odd, P_b(2) and P_b(−2) are units. Also H_b(0)=1. At an H_b root choose nonzero v with v^2=z. In characteristic zero the map v->v^2 is unramified there, while v->v+v^(−1) is unramified except at v=±1, whose X-values ±2 were excluded. The prefactor v^b is a local unit. Thus (14) preserves root multiplicity locally, and P_b squarefreeness proves squarefreeness of the actual H_b.

For b>=1 put w_k=product_(j=1)^k(1−q^j), with w_0=1. All required w_k are nonzero because b<p^s. Consecutive P's are coprime: a common root propagates downward through the recurrence and nonzero u_j to P_0=1. At any P_b root xi the accepted exact diagonal identity is

    sum_(k=0)^(b−1) P_k(xi)^2/w_k
       =P_b'(xi)P_(b−1)(xi)/w_(b−1).

Both numerator factors are now nonzero, proving the stated bilinear nonisotropy. The squares are ordinary algebraic squares, not absolute-value squares; no positive-metric or Hermitian argument is used. At b=0 there are no roots and the guard is vacuous.

Nonzero discriminants and the kernel assertions are algebraic. The p-adic embedding is injective and primitive-root embeddings are Galois conjugate, so they hold at every primitive complex embedding. No valuation inequality is interpreted as complex positivity.

Combining this new block with the accepted b<2p theorem proves (T). The existing local all-A theorem can be composed only where its other independently accepted guard also applies. No canonical status or repository record is changed here.

## 8. Fresh exact controls and stopping scope

`check_third_block.py` was authored anew for this packet. It imports no previous checker. For p=3,5,7,11,13 and every 0<=r<p, it constructs the actual integer recurrence and both blocks with their exact edge indices. It checks the exact joining identities, the preceding-polynomial valuation bound, the entire tail leading residual, the entire joining-term strict inequality, the outer residual, residual squarefreeness and parity, full root counts, the discriminant/derivative formulas, and the inner irreducibility denominator.

Weight controls use exact integer coefficients after q=1+T, including e*v_p(coefficient) with the least allowed ramification e=p(p−1). Translation is retained through T^(4p); omitted terms have weight at least 4p+1, strictly above every threshold tested. Replacing X by a+tZ cannot lower the tested X-weight because v(t)>v(a). Thus the error tests apply coefficientwise to the translated polynomials, rather than only to values at a center. The infinite-family proof is Sections 2–7; these finitely many controls check its formulas and indexing.

As additional exact nonvanishing controls, the script constructs a primitive p^2-th root in a finite field and checks the actual P_b and actual Gaussian H_b against their derivatives for every degree of the new block. The successful pairs (field prime, root) are (19,4), (101,16), (197,16), (727,64), and (677,16), in increasing p order. There were no bad-reduction retries. These witnesses are supplemental finite checks, not a replacement for the uniform proof and not a claim of unrestricted root-order certification.

`check_discriminants.py` additionally computes the actual symbolic discriminants of P_6,P_7,P_8, reduces each modulo Phi_(3^s) for s=2,3, and calculates its exact valuation in the uniformizer basis. The remainder has degree less than e, so its coefficient weights are distinct modulo e and the unique minimum is the exact valuation. These six controls independently recover 27,37,40 without assuming the root-distance formula.

All 543 exact controls passed: 537 assertions in the block checker and six actual discriminant valuations. Both programs passed on their first runs. Source acceptance bindings and frozen manifest entries are checked separately in INPUT_VERIFICATION.json. RUN_LOG.md records execution and provenance; MANIFEST.json freezes the deliverable. No historical checker, browser, external service, or repository write was used. No independent-acceptance or historical-originality claim is made by this author packet.

The stopping scope is precise: the full next partial block 2p<=b<3p is resolved, and the supported combined range becomes b<min(3p,p^s), subject to independent review. At r=p the p-unit d_r used in (6) is unavailable; neither the proof nor its displayed residual is asserted at that next boundary. F020 and unrestricted ordinary-guard closure remain open.
