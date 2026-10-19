# Independent review: F020 boundary resolution at b=2p

19 October 2026 UTC. Review of the author packet `f020_boundary_hensel_resolution_20261019_0839`, against the accepted `f020_two_digit_hensel_20261019_0124` baseline and `f020_primepower_extension_review_20261019_0124`. Exact final source bindings and the acceptance target are recorded in the accompanying JSON files. No external record is changed by this review.

## Verdict and exact scope

**ACCEPT within the written scope.** Acceptance binds to author report SHA-256 `6b27fcbdc7aae652afae91fa9e1a8baf84270ef57af75c44c5f35288541686da` and author manifest SHA-256 `eb31526958e004a90a531f7a857679faa9515fdb50146343fda23a50fbd9c9cb`, also recorded in `VERDICT.json`. No mathematical blocker was found. The two logically separate conclusions both hold:

1. For every odd prime p and s>=2, the actual monic continuant P_(2p)(X;q), q primitive of order p^s, is irreducible over K=Q_p(q), hence squarefree in characteristic zero. The irreducibility already follows from the accepted boundary slope together with the base-field value group.
2. For the explicitly constructed auxiliary center a and kappa, the integral translated residual is exactly Z^p+cZ. It separates both p-root clusters and gives all pairwise valuations and v(Disc P_(2p))=p(4p−3).

The actual Rogers–Szego H_(2p) is squarefree and the original ordinary-square bilinear Christoffel–Darboux kernel is nonzero at every P_(2p) root. Combined with the accepted strict b<2p theorem, the supported range is 0<=b<p^s with b<=2p; for s=1 it remains b<p. There is no assertion for b>2p, no unrestricted all-A or ordinary-guard closure, and no claim of historical originality. F020 remains open; F023 remains its alias and priority 58 is unchanged.

The independent fresh program passed **195 exact assertions**. These are finite transcription controls, not a proof by census. No author or historical program was imported or executed.

## 1. Base field, constants, and the irreducibility shortcut

Let t=q−1. The shifted cyclotomic polynomial Phi_(p^s)(1+T) is Eisenstein over Z_p: it is monic, reduces to T^e modulo p, and has constant p, with e=p^(s−1)(p−1). Therefore K is totally ramified of degree e, t is a uniformizer, and under v(t)=1 one has v(K^×)=Z and v(p)=e. The integral value group is essential to the irreducibility argument; it is asserted only for K, not for the later auxiliary extensions.

The exact recurrence gives

    P_(2p)(0)=−product_(j=1)^p u_(2j−1),  u_j=1−q^j.

Exactly one of the p odd indices is divisible by p, namely p itself; every index is strictly below p^s. Thus this constant is nonzero, and its valuation is p+(p−1)=2p−1. The accepted normalized boundary polynomial

    P_(2p)(t^alpha Y)/t^(2p−1), alpha=(2p−1)/(2p),

is monic and integral after adjoining the indicated fractional power, and its reduction is Y^(2p)−1. Its constant is a unit. Every scaled root is integral, because the polynomial is monic, and the product of the roots is a unit. Hence every scaled root has valuation zero. All original roots, counted with multiplicity, have valuation alpha and are nonzero.

If P_(2p) had a monic proper K-factor of degree m, its nonzero constant would be a signed product of m original roots, so would have valuation m alpha in Z. Because gcd(2p−1,2p)=1, this forces 2p|m, impossible for 0<m<2p. Any factorization over K can be made monic, so every proper factor is excluded. Irreducibility in characteristic zero implies separability. The same irreducibility also holds over the embedded number field Q(q), though the author's stated K conclusion already suffices.

This argument does not treat an inseparable reduction as a repeated characteristic-zero root. It explains precisely why the accepted slope was stronger than its previous residual-Hensel discussion made explicit.

## 2. Exact blocks and the coefficient estimates

Use the accepted family, without a sign or normalization change:

    P_0=1, P_1=X, P_(n+1)=X P_n−u_n P_(n−1).

Let A=P_p, let B be the shifted p-vertex block with internal edges p+1 through 2p−1, and let G be the (p−1)-vertex block with internal edges p+2 through 2p−1. Put D=P_(p−1), R=GD, and C=u_p R(0). The exact joining identity is

    P_(2p)=AB−u_p R, C=−P_(2p)(0).

The indexing and sign were independently reconstructed. The constants of G and D together contain precisely the odd-index edges other than p. Their individual signs (−1)^((p−1)/2) multiply to +1. This agrees with the constant-product formula above.

Write lambda=[X]A, h=(p−1)/2, c=(−1)^((p+1)/2), and

    g(X)=X^p+lambda X, A=g+E.

The accepted p-block theorem gives v(lambda)=p−1, lambda/t^(p−1) reducing to c, and every coefficient of E of valuation at least p−1. Parity leaves only odd powers 3 through p−2; E=0 when p=3. The coefficientwise comparison B−A has valuation at least p because each replacement edge differs by −q^j(q^p−1), of valuation p. The difference is odd and has no constant or leading term.

Every edge internal to G and D has valuation 1. A matching term contributing X^(2j) in a (p−1)-vertex block has exactly h−j edges, so its coefficient has valuation at least h−j. Multiplication gives

    v([X^(2j)]R)>=p−1−j, 0<=j<=p−1.

This bound requires no noncancellation hypothesis. The constant is a single matching in each even block, so v(R(0))=p−1 exactly. These estimates justify all later coefficientwise integrality claims.

## 3. Every auxiliary center exists and has the claimed valuation

Choose kappa with kappa^2=C. It is nonzero and has v(kappa)=p−1/2. Any root a of

    a^p+lambda a=kappa

exists in a finite algebraic extension of K, which is complete. The Newton polygon has endpoints (0,p−1/2),(p,0); the middle point (1,p−1) lies above their segment by (p−1)/(2p)>0. Thus every root a has valuation alpha, not merely some specially chosen root.

The same fact follows by comparing the three possible valuations p beta, p−1+beta, p−1/2 when beta=v(a): unless beta=alpha, one term is uniquely smallest. No target P_(2p) root was used to define a. In fact, the auxiliary trinomial itself is separable, since at any such a its derivative p a^(p−1)+lambda has valuation p−1, the lambda term being uniquely smallest. This additional observation is not needed for choosing a.

Because p is odd, −a is a center for −kappa. Their distance has valuation v(2a)=alpha<1, so the radius-v>=1 discs about them are disjoint. The extended value group may be fractional; this presents no issue for Hensel lifting and is not used in the K-irreducibility argument.

## 4. Independent derivation of the entire translated residual

Here is a coefficientwise derivation independent of the author's difference decomposition. Set

    L=v(2 kappa t^p)=2p−1/2.

After X=a+tZ, every monomial X^j has coefficients of valuation at least j alpha, because alpha<1. Thus

    v(E(a+tZ))>=p−1+3alpha>p,
    v((B−A)(a+tZ))>=p+alpha>p.

The first expression is infinite for p=3. Also g(a+tZ) has coefficientwise valuation at least p alpha=p−1/2. The nonconstant joining term has

    v(u_p(R(a+tZ)−R(0)))
      >=min_(j>=1)(2p−1−j+2j alpha)
      =2p−1/p>L.

The decisive gap is 1/2−1/p=(p−2)/(2p)>0. It is 1/6 at the smallest prime p=3.

Expanding A=g+E and B=A+(B−A) now proves

    P_(2p)(a+tZ)=g(a+tZ)^2−C+error,
    v(error)>L.

Indeed, the product 2gE has gap at least 3alpha−1>0 above L; E^2 has valuation >2p>L; (B−A)(g+E) has gap at least alpha>0; and the joining difference has the strict gap just computed. All are statements about every Z coefficient, so normalization cannot hide a nonintegral higher coefficient.

The defining center equation gives

    g(a+tZ)−kappa=t^p Z^p+lambda tZ
       +sum_(j=1)^(p−1) binom(p,j)a^(p−j)t^j Z^j.

Each mixed coefficient has valuation at least e+(p−j)alpha+j>p. Its least possible excess is e−(p−1)/(2p)>0. The linear term divided by t^p reduces to cZ. Therefore

    (g(a+tZ)−kappa)/t^p -> Z^p+cZ.

Factoring g(a+tZ)^2−kappa^2, the linear increment gives 2 kappa t^p times this residual, while its square has valuation >=2p>L. The previously bounded error vanishes as well. Consequently the actual normalized polynomial is integral and

    P_(2p)(a+tZ)/(2 kappa t^p) -> Z^p+cZ.

This establishes the displayed residual, including its zero constant, leading coefficient, linear coefficient and suppression of every omitted term. It works for every odd p and all s>=2. At s=2 the least ramification is e=p(p−1); the mixed-characteristic estimates still hold. At p=3,s=2, alpha=5/6, L=11/2 and e=6, with E absent and the strict joining gap intact. There is no analogue of the earlier b=4 scale-overlap exception here.

## 5. Lifting, complete root count, and distances

The residual derivative is c, a unit, so Z^p+cZ has p simple roots after a finite residue-field extension. If i^2=−1, its roots are exactly i F_p: i^(p−1)=(−1)^h=−c, and all p such values are distinct. Simple-root Hensel lifting applies to the integral normalized polynomial even though its characteristic-zero degree is 2p and its reduced degree is p. Monicity of the normalized polynomial is unnecessary for this local lifting statement.

The lifts have form a+t z_r, with z_r reducing to i r. Distinct residues imply same-cluster differences of valuation exactly 1. Repeating at (−a,−kappa) gives p further roots; the two discs are disjoint because their centers have distance valuation alpha<1. Cross-cluster differences have valuation alpha. Thus these are exactly 2p distinct roots and exhaust the degree, without presupposing original-root simplicity.

Every original root has valuation alpha, consistently with the first slope. Evenness pairs the two clusters by negation. There are p(p−1) same-cluster unordered pairs and p^2 cross-cluster pairs. The discriminant, a product of squared differences, therefore has valuation

    2p(p−1)+2p^2 alpha=p(4p−3).

The author's independent derivative calculation is also correct. For any x with v(x)=alpha, A(x)/x^p and B(x)/x^p reduce to 1, while A'(x)/t^(p−1) and B'(x)/t^(p−1) reduce to c. The joining derivative has valuation at least 2p−2+alpha, strictly above 2p−3/2 by (p−1)/(2p). Hence

    P'_(2p)(x)/(2c t^(p−1)x^p) -> 1,
    v(P'_(2p)(x))=2p−3/2.

At all 2p roots this independently gives the same discriminant valuation. Both supplementary conclusions are confined to b=2p.

## 6. Correspondence to the original H polynomial and kernel

The exact identity is the baseline one:

    H_b(v^2;q)=v^b P_b(v+v^(−1);q).

Since all u_j have positive valuation, P_b(X) reduces to X^b. For odd p, P_b(2) and P_b(−2) are units, so these critical X values are excluded. H_b(0)=1. At an H root choose nonzero v with v^2=z. In characteristic zero, v->v^2 is unramified there; v->v+v^(−1) is unramified unless v=+/-1, precisely the excluded X=+/-2 cases. The factor v^b is a local unit. Thus root multiplicities are preserved and the proved P_(2p) squarefreeness transfers to the actual H_(2p), without claiming irreducibility of H.

Put w_k=product_(j=1)^k u_j. Since 2p<p^s, every needed w_k is nonzero. Consecutive P's are coprime: a common root propagates down their recurrence through nonzero u_j to P_0=1. The exact diagonal Christoffel–Darboux formula at a P_b root xi is

    sum_(k=0)^(b−1) P_k(xi)^2/w_k
      =P_b'(xi)P_(b−1)(xi)/w_(b−1).

The independently checked sign and normalization agree with the original bilinear kernel. Both numerator factors are nonzero, so this is the required guard. It concerns ordinary squares, not absolute-value squares or a positive Hermitian norm.

Finally, a nonzero discriminant in the chosen p-adic embedding is algebraic nonvanishing. The embedding is injective, and Galois conjugacy transfers this to every primitive complex embedding. No p-adic valuation is interpreted as complex positivity.

## 7. Exact independent controls and source handling

`independent_controls.py` was written fresh for this review. Its recurrence and sparse polynomial arithmetic do not import any prior checker. For p=3,5,7,11,13 it reconstructs the actual P blocks and checks the exact joining identity, parity, lambda residue, coefficient bounds, constant sign and valuation, first residual, center slope, irreducibility denominator, all error gaps, whole translated residual, derivative residual, simple residual and root-spacing discriminant expression. It also checks shifted cyclotomic Eisenstein conditions at s=2 and s=3, the actual H/P identity through b=10, and the exact unnormalized diagonal CD identity through b=8.

The translated control is especially direct. It forms the integer polynomial

    P_(2p)(A+TZ;1+T)
      −(g(A)^2−C)−2g(A)T^p(Z^p+cZ)

before any auxiliary relation is imposed. Each remaining monomial has weight strictly greater than L under weight(A)=alpha, weight(T)=1 and integer coefficient weight=e*v_p(coefficient), using the least allowed e=p(p−1). Substituting g(a)=kappa and kappa^2=C gives exactly the desired normalized residue. Thus these controls do not silently discard p-multiples or a constant-center error. In the five tested primes the minimum error weight is 2p; this finite observation is not promoted to a stronger uniform claim.

The first fresh run passed 190 assertions. Five derivative-residual controls were then added, and the final run passed all 195, with no failed assertion. Every p=3 test and the least ramification s=2 are included. The controls test formulas; the unlimited result rests on Sections 1–6 and the source-bound accepted coefficient theorem.

The accepted source reports and candidate files are read-only inputs. Source bytes and frozen manifest entries are independently hash-checked. There is no author-checker replay, historical-code execution, remote-source read, external write, or implied literature originality search in this review.

## Terminal decision

Accept the b=2p boundary as a uniform extension of the previously accepted result, including irreducibility of P_(2p) over Q_p(q), the explicit simple residual, exact within/cross-cluster distances, discriminant valuation, actual H squarefreeness and the bilinear kernel guard. Any use of the existing local all-A result remains restricted to degrees where its other guard is already accepted. Later blocks and unrestricted F020 closure remain open.
