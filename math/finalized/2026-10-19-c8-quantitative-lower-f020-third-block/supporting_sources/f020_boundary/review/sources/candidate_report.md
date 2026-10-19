# F020 boundary resolution: b = 2p

19 October 2026 UTC. Author-level mathematical result, submitted for independent review. No external write or historical-program execution.

## Result

Let p be any odd prime, s >= 2, q any primitive p^s-th root of unity, and

    P_0(X;q)=1, P_1(X;q)=X,
    P_(n+1)(X;q)=X P_n(X;q)−(1−q^n)P_(n−1)(X;q),
    H_n(z;q)=sum_(k=0)^n [n choose k]_q z^k.

Then P_(2p) and H_(2p) are squarefree in characteristic zero. In fact, P_(2p) is irreducible over Q_p(q). Thus the previously accepted range extends to

    0 <= b < p^s, b <= 2p

for every odd p and s >= 1; for s=1 this remains b<p.

The original b=2p inseparable residual is resolved explicitly. Write t=q−1, normalize v(t)=1, and set

    alpha=(2p−1)/(2p), h=(p−1)/2,
    c=(−1)^((p+1)/2), lambda=[X]P_p(X;q),
    C=−P_(2p)(0;q)=product_(j=1)^p (1−q^(2j−1)).

Choose kappa with kappa^2=C and any a satisfying

    a^p+lambda a=kappa.

Then v(a)=alpha. In a finite complete extension containing a and kappa, the following polynomial is integral and has the indicated reduction:

    P_(2p)(a+tZ;q)/(2 kappa t^p)  -->  Z^p+cZ.        (R)

The same formula holds with (a,kappa) replaced by (−a,−kappa). The residual derivative is c, a nonzero unit. Each center therefore supplies p distinct roots; the two sets are disjoint. Within either set every difference has valuation 1, and between the sets every difference has valuation alpha. There is no small-prime exception, including p=3,s=2.

The proof is uniform. Fresh exact checks below are transcription controls, not a prime census or the basis of the theorem. No assertion for b>2p or unrestricted F020 closure is made.

## 1. Accepted inputs and exact family

The accepted author packet `f020_two_digit_hensel_20261019_0124` and its independent review `f020_primepower_extension_review_20261019_0124` establish the following facts. Their exact reports, manifests, and review verdict are SHA-256 bound in SOURCE_BINDINGS.json. No old checker is executed here.

Let K=Q_p(q). Its valuation group, under v(t)=1, is Z, and

    v(p)=e=p^(s−1)(p−1).

Indeed Phi_(p^s)(1+T) is Eisenstein. For u_j=1−q^j,

    v(u_j)=1 if p does not divide j,
    v(u_p)=p, u_p/t^p --> −1.

Put A=P_p. The accepted p-block estimate is

    A(X)=X^p+lambda X+E(X),
    v(lambda)=p−1, lambda/t^(p−1) --> c,

where E is odd, has only exponents 3,5,...,p−2, and all its coefficients have valuation at least p−1. The set of exponents is empty for p=3, so E=0 there. These statements include all mixed-characteristic terms because e>p−1.

Let B=F_p be the continuant on vertices p+1,...,2p, whose internal edges are u_(p+1),...,u_(2p−1). Let G be the continuant on vertices p+2,...,2p, with internal edges u_(p+2),...,u_(2p−1), and let D=P_(p−1). Thus G and D each have degree p−1. The exact concatenation identity is

    P_(2p)=AB−u_p GD.                                  (1)

Set R=GD. No recurrence sign, normalization, block index, or family is changed.

For completeness, B−A is odd and each of its coefficients has valuation at least p: replacing an edge u_j by u_(p+j) changes it by −q^j(q^p−1), of valuation p, and the continuant is an integer polynomial in integral edge variables. A telescoping change of edge variables proves the coefficientwise bound. Both blocks are monic of degree p, so their difference has degree at most p−2.

Each coefficient of X^(2j) in G or D has valuation at least h−j: its matching expansion is a sum of products of h−j internal edges, all of valuation 1. Consequently

    v([X^(2j)]R) >= p−1−j, 0 <= j <= p−1.            (2)

Cancellation can only improve this lower bound. The constant of R is nonzero, and its valuation is p−1.

Since p is odd, the recurrence constant gives

    P_(2p)(0)=−product_(j=1)^p u_(2j−1),
    C=u_p R(0)=−P_(2p)(0), v(C)=2p−1.                (3)

All odd indices are below p^s, and exactly one, p, is divisible by p. This proves the valuation and nonvanishing in (3) for every s>=2.

The exact transformation to the actual Rogers–Szego polynomial is

    H_n(v^2;q)=v^n P_n(v+v^(−1);q).                    (4)

It is the accepted normalization and also follows directly from the two recurrences.

## 2. A short irreducibility proof already implicit in the boundary

The accepted boundary establishes that all 2p roots of P_(2p), counted with multiplicity in an algebraic closure of K, have valuation alpha=(2p−1)/(2p). This already forces irreducibility over K.

Indeed, if a monic proper factor over K had degree m with 0<m<2p, its nonzero constant term would be a product of m such roots and would have valuation m alpha. Every nonzero element of K has integral valuation. Since gcd(2p−1,2p)=1, integrality of m alpha requires 2p to divide m, a contradiction. A monic polynomial over a field may be factored into monic factors, so this excludes every proper factor. Characteristic zero is perfect, hence P_(2p) is separable.

Thus inseparability of the first residual never implied a characteristic-zero obstruction. The next sections nevertheless derive the requested explicit separating residual and all root distances, without using irreducibility or assuming that any original root is simple.

## 3. The ramified auxiliary center

Choose kappa with kappa^2=C in a finite extension of K. Then

    v(kappa)=p−1/2.

Choose any root a of the auxiliary degree-p trinomial

    f(X)=X^p+lambda X−kappa.

Such a root exists in a finite algebraic extension. Its valuation is alpha. One way to see this is that the Newton polygon has a single segment from (0,p−1/2) to (p,0): the intermediate point (1,p−1) is strictly above the line, by (p−1)/(2p)>0. Equivalently, if beta=v(a) differs from alpha, either p beta or p−1/2 is uniquely smallest among p beta, p−1+beta, and p−1/2, which is impossible in f(a)=0. The term lambda a lies strictly above a^p and kappa at beta=alpha.

The construction uses no root of P_(2p). It is genuinely an auxiliary center. The negative center −a solves X^p+lambda X=−kappa, since p is odd. Their difference has valuation alpha<1.

Set

    L=v(kappa)+p=2p−1/2.

At a, the omitted block terms satisfy

    v(E(a)) >= p−1+3 alpha > p,
    v((B−A)(a)) >= p+alpha > p.                         (5)

For E=0 the first bound means infinite valuation. Hence

    A(a)=kappa+epsilon_A, B(a)=kappa+epsilon_B,
    v(epsilon_A),v(epsilon_B)>p.

Using (2) and 2alpha−1>0 gives

    v(u_p(R(a)−R(0)))
       >= 2p−2+2alpha = 2p−1/p > L.                  (6)

The last strict inequality is (p−2)/(2p)>0, including p=3. Equations (1), (3), (5), and (6) now imply

    v(P_(2p)(a))>L.                                   (7)

Thus the center is accurate enough for the separating scale t; it is not claimed to be an exact original root.

## 4. Polynomial difference estimates at scale t

All valuations of polynomials in Z below are coefficientwise. Write

    Delta_A(Z)=A(a+tZ)−A(a),
    Delta_B(Z)=B(a+tZ)−B(a).

Then

    Delta_A/t^p --> Z^p+cZ,
    Delta_B/t^p --> Z^p+cZ.                            (8)

Here are the complete estimates. The leading monomial contributes

    (a+tZ)^p−a^p=t^p Z^p
       +sum_(k=1)^(p−1) binom(p,k)a^(p−k)t^k Z^k.

Each mixed coefficient has valuation at least e+(p−k)alpha+k>p; the minimum over k is at k=1, and its excess over p is e−(p−1)/(2p)>0. The linear coefficient contributes lambda t Z, whose quotient by t^p reduces to cZ. For every monomial of E with odd exponent j>=3, the lowest possible difference weight is

    p−1+(j−1)alpha+1=p+(j−1)alpha>p.

This is attained in the lower bound at k=1 because alpha<1. Finally each monomial of B−A has coefficient valuation at least p and positive odd exponent j, so its difference has valuation at least p+(j−1)alpha+1>p. These estimates prove both integrality and the exact residues in (8).

For the joining term, (2) likewise gives

    v(u_p(R(a+tZ)−R(a))) >= 2p−1+alpha > L.           (9)

Indeed for j>=1 the X^(2j) coefficient contributes at least p+(p−1−j)+(2j−1)alpha+1, minimized at j=1 since 2alpha−1>0. Terms k>1 have still higher weight because alpha<1. No constant term contributes to the difference.

## 5. The next residual and all 2p roots

Expand the exact identity (1) at the auxiliary center:

    P_(2p)(a+tZ)=P_(2p)(a)
        +A(a) Delta_B+B(a) Delta_A+Delta_A Delta_B
        −u_p(R(a+tZ)−R(a)).                            (10)

Divide by 2 kappa t^p. The constant term vanishes in the residue by (7). Since A(a)/kappa and B(a)/kappa both reduce to 1, the two middle linear differences give Z^p+cZ by (8). Their product has valuation at least 2p>L, and (9) removes the joining difference. This proves (R), with every coefficient integral after division.

The residual derivative is c, nonzero in characteristic p, so all its p roots are simple. It splits over a finite residue-field extension. More explicitly, if i^2=−1 in that residue field, its roots are i r for r in F_p, because

    i^(p−1)=(−1)^h=−c.

They are all distinct, including r=0. The ordinary simple-root Hensel lemma gives p distinct roots of P_(2p) of the form

    a+t z_r, z_r reducing to i r.

Repeat at −a with denominator −2 kappa t^p. The same residual gives p roots in the other ball. Because v(2a)=alpha<1, the balls a+t O and −a+t O are disjoint. Their total contains 2p distinct roots, the entire degree. No assumption about original-root simplicity was used in this construction.

For two roots from the same center, their distinct z residues give difference valuation exactly 1. For roots from opposite centers, the difference is 2a plus a term of valuation at least 1, hence its valuation is exactly alpha. Every root itself has valuation alpha. Parity P_(2p)(−X)=P_(2p)(X) pairs the two clusters by negation.

## 6. Derivative and discriminant checks

There is also a direct uniform derivative proof. At any x with v(x)=alpha,

    A(x)/x^p --> 1, B(x)/x^p --> 1,
    A'(x)/t^(p−1) --> c, B'(x)/t^(p−1) --> c.

The leading derivative p x^(p−1) has valuation e+(p−1)alpha>p−1, and the higher odd lower terms have valuation greater than p−1. The derivative of B−A has coefficientwise valuation at least p. From (2),

    v(u_p R'(x)) >= 2p−2+alpha.

This is strictly above (p−1)+p alpha=2p−3/2, with difference (p−1)/(2p). Therefore

    P'_(2p)(x)/(2c t^(p−1)x^p) --> 1,
    v(P'_(2p)(x))=2p−3/2.                             (11)

In particular the derivative is nonzero at every root. This provides a separate verification of the separating mechanism.

The exact pairwise distances above or (11) yield the discriminant valuation

    v(Disc_X P_(2p))=p(4p−3).                           (12)

Indeed the product of the 2p derivative values has this valuation. Alternatively there are p(p−1) same-cluster unordered pairs and p^2 cross-cluster pairs, and the discriminant is their squared difference product. Equation (12) is a corollary within b=2p, not a statement about later blocks.

## 7. Actual H polynomial and bilinear kernel

Each u_j has positive valuation, so P_(2p)(X) reduces to X^(2p). Since p is odd, P_(2p)(2) and P_(2p)(−2) are nonzero. Also H_(2p)(0)=1.

At any root z of H_(2p), choose nonzero v with v^2=z. In (4), the map v to v^2 is unramified in characteristic zero; the map v to v+v^(−1) is unramified away from v=1,−1, whose X values 2,−2 are already excluded. The factor v^(2p) is a unit. Consequently root multiplicities are preserved locally, and squarefreeness of P_(2p) proves squarefreeness of the actual H_(2p).

Since 2p<p^s for every odd p,s>=2, all recurrence norm factors 1−q^j with j<=2p−1 are nonzero. Consecutive P's have no common root by the recurrence. The accepted Christoffel–Darboux identity then implies that the actual bilinear kernel

    sum_(k=0)^(2p−1) P_k(xi)^2 /
                    product_(j=1)^k(1−q^j)

is nonzero at every root xi of P_(2p). These are ordinary squares, and no positive-metric argument is used. Nonzero discriminants are algebraic statements, so the p-adic embedding proves the result at every primitive complex embedding.

Combined with the accepted b<min(2p,p^s) theorem, this supplies both squarefreeness and the corresponding kernel guard through b=2p whenever b<p^s. The existing local all-A theorem may be composed only where its other accepted guard applies. F020 remains open beyond the stated range; F023 remains its alias and priority 58 is unchanged. No canonical or repository record is changed by this packet.

## 8. Verification and provenance

`check_boundary.py` is newly authored in this directory. It constructs the actual recurrence from scratch with sparse exact arithmetic, checks the auxiliary approximation, shifted residual, derivative valuation, block indices, and transformation to H, and includes p=3 controls. The primary infinite-family justification is Sections 1–7, not these finite checks.

All 74 fresh exact assertions passed. The script does not execute or import any historical checker. Accepted input files are read only for source binding. RUN_LOG.md records execution and any implementation correction. CHECKS.json stores the fresh exact results. MANIFEST.json binds the frozen deliverable. Independent review is required for acceptance; neither this author report nor its finite checks claim independent certification.
