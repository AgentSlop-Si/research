# F020: the next boundary b = 3p

19 October 2026 UTC. Author-level proof candidate awaiting independent review. Owner F020, alias F023, priority 58 unchanged. No external write, canonical status change, performance claim, or historical-originality claim.

## Result and stopping scope

Let p be an odd prime, let q be a primitive p^s-th root of unity, and assume 3p < p^s. Define the actual recurrence and Gaussian polynomial by

    P_0(X;q)=1, P_1(X;q)=X,
    P_(n+1)(X;q)=X P_n(X;q)-(1-q^n)P_(n-1)(X;q),
    H_n(z;q)=sum_(k=0)^n [n choose k]_q z^k.

Then P_(3p) and H_(3p) are squarefree in characteristic zero. At every root xi of P_(3p), the original ordinary-square bilinear kernel

    sum_(k=0)^(3p-1) P_k(xi;q)^2 / product_(j=1)^k(1-q^j)

is nonzero. Empty products equal 1. These are algebraic squares, not absolute-value squares.

The boundary condition means s>=2 for p>=5 and s>=3 for p=3. In particular the proof does not treat b=9 as a below-order degree when q has order 9.

For p>=5 there is also an explicit local description. Put K=Q_p(q), t=q-1, v(t)=1, and alpha=(2p-1)/(2p). The roots are:

- 2p roots of valuation alpha, whose monic degree-2p factor is irreducible over K;
- p-1 roots of valuation 1;
- the simple root 0.

The p roots in the last two items have pairwise differences of valuation 1. Every root xi, including 0, satisfies

    v(P'_(3p)(xi))=3p-2,
    v(Disc_X P_(3p))=3p(3p-2).

No p=3 version of that local description or discriminant-valuation formula is asserted. At p=3 a separate exact degree-nine cyclotomic certificate proves squarefreeness uniformly for every s>=3.

Composed with the previously accepted b<min(3p,p^s) result, the supported range becomes 0<=b<p^s and b<=3p. The only new degree in this packet is b=3p. No statement for b>3p, general odd-composite root orders, unrestricted F020/all-A closure, cost improvement, or optimal algorithm follows.

## 1. Source-bound question and classical inputs

A fresh read of AgentSlop-Si/research's open-record index returned Git blob 9c88b352a77a46061b45aeb614a66a8cce28625c. Its F020 record explicitly identifies the unproved b=3p boundary and warns that the third-block tail unit fails there. That warning is respected: the accepted r<p tail argument is not continued through r=p. This packet instead splits the path into three whole p-vertex blocks.

The accepted third-block report is SHA-256 2eac2d7ee2c9685aa1413482fde7b3d061d9fb35d522da4aa872df61db7fb925. Its independent review accepts precisely b<min(3p,p^s). The earlier accepted p-block coefficient theorem is the only family-specific estimate needed for the p>=5 proof below. Source texts and acceptance records are frozen and hashed in SOURCE_BINDINGS.json. No prior checker was imported or executed.

These are the classical continuous q-Hermite polynomials in monic variable X: P_n(X;q)=C_n(X/2|q). Their recurrence, finite Fourier expansion, and root-of-unity terminal identities are described by Atakishiyeva, Atakishiyev and Koornwinder, Section 2, [arXiv:0811.4100](https://arxiv.org/pdf/0811.4100). The transformation to H_n, continuant matching identity, and Christoffel-Darboux identity are established tools. The root-order terminal identity is not used to infer lower-degree simplicity.

Simple-residual Hensel lifting is classical; a version for integral, not necessarily monic, polynomials over complete nonarchimedean fields is in Keith Conrad's [Hensel notes, Theorems 9.1-9.2](https://kconrad.math.uconn.edu/blurbs/gradnumthy/hensel.pdf). The integral-value-group irreducibility implication is the elementary primitive Newton-side argument, within standard Newton-polygon theory; see Guardia, Montes and Nart, [Section 1.4](https://arxiv.org/pdf/0807.2620). The discriminant product formula is standard. No claim that these tools or polynomial families are new is made. The cited sources were opened for these tool attributions; this is not a fresh exhaustive priority search for the b=3p statement.

## 2. Valuation facts and whole-block notation

For the rest of Sections 2-6 assume p>=5 and s>=2. Let u_j=1-q^j and h=(p-1)/2. The shifted cyclotomic polynomial Phi_(p^s)(1+T) is Eisenstein, so

    v(K^times)=Z, v(p)=e=p^(s-1)(p-1).

All edges used have indices j<=3p-1<p^s. If p does not divide j then v(u_j)=1 and u_j/t reduces to -j. At the two joining edges,

    v(u_p)=v(u_(2p))=p,
    u_p/t^p -> -1, u_(2p)/t^p -> -2.

The accepted p-block coefficient theorem says

    A_0=P_p=X^p+lambda X+E(X),
    v(lambda)=p-1, lambda/t^(p-1) -> c=(-1)^((p+1)/2),

where E uses only odd exponents 3,...,p-2 and each coefficient has valuation at least p-1.

Let A_k be the p-vertex continuant on vertices kp+1,...,(k+1)p, for k=0,1,2. A path on vertices a,...,b has internal edges u_a,...,u_(b-1). Let L_k be A_k with its last vertex removed and R_k be A_k with its first vertex removed. Finally let M be the middle (p-2)-vertex path on vertices p+2,...,2p-1.

The changes of internal edges satisfy

    u_(kp+j)-u_j=-q^j(q^(kp)-1),   k=1,2,

of valuation p. A continuant is an integer polynomial in its edges. Telescoping one changed edge at a time therefore proves that every coefficient of A_k-A_0 has valuation at least p. These differences are odd and have degree at most p-2, since all A_k are monic.

Consequently, coefficientwise in Y,

    A_k(tY)/t^p -> S(Y)=Y^p+cY,                       (2.1)
    A_k(rho Y)/rho^p -> Y^p,                          (2.2)
    A'_k(rho Y)/t^(p-1) -> c,                         (2.3)

where rho is chosen in a finite extension with rho^(2p)=t^(2p-1), so v(rho)=alpha. For (2.2), each lower odd exponent j has excess at least p-1+j alpha-p alpha>0. For (2.3), the leading derivative pX^(p-1) has weight e+(p-1)alpha>p-1; every higher odd lower monomial has strictly greater derivative weight than the linear term. The shifted-block difference also has strictly greater derivative weight. Thus (2.3) includes mixed-characteristic terms, not just a formal reduction modulo p.

## 3. End pieces and the exact triple-block identity

A matching contributing to X^(n-2j) in an n-vertex path uses exactly j edges. If all internal edge valuations equal 1, this coefficient has valuation at least j. At a scale beta>1/2 the even paths L_k,R_k are therefore dominated by their constant terms. With

    d=(p-2)!!, f=2^h h!,

their exact alternating-edge constant products give

    L_k(t^beta Y)/t^h -> d,
    R_k(t^beta Y)/t^h -> f,
    df=(p-1)! = -1 in the residue field.             (3.1)

The symbols t^beta denote a chosen element of valuation beta; only beta=1 and beta=alpha, with the choices t and rho, are used. The constants in (3.1) are p-units. In L_k the alternating edges reduce to -1,-3,...,-(p-2); in R_k they reduce to -2,-4,...,-(p-1). The determinant signs cancel those minus signs.

Write B_1=L_0 R_1 and B_2=L_1 R_2. Both satisfy, at either scale,

    B_i/t^(p-1) -> -1,
    v([X^(2j)] B_i)>=p-1-j.                         (3.2)

The middle path M has odd degree 2h-1 and its matching estimate gives

    v(M(t^beta Y))>=h-1+beta.

If D=L_0 M R_2, then coefficientwise

    v(D(t^beta Y))>=3h-1+beta,
    v(D'(t^beta Y))>=3h-1.                           (3.3)

The derivative bound follows either from the matching coefficients or by observing that differentiating a monomial decreases its beta-weight by at most beta. Integer derivative multipliers cannot lower valuation. The coefficientwise convention assigns the zero polynomial infinite valuation.

Partition all path matchings according to their use of joining edges p and 2p. The exact identity is

    P_(3p)=A_0 A_1 A_2
             -u_p B_1 A_2-u_(2p) A_0 B_2
             +u_p u_(2p) D.                         (3.4)

The positive double-joining term removes both ends of the middle block and leaves precisely M. It cannot be dropped without a valuation estimate. Formula (3.4), including this term, is the new whole-block starting point.

## 4. The two residuals and the complete root count

At X=rho Y, divide (3.4) by rho^(3p). Equations (2.2), (3.1), and rho^(2p)=t^(2p-1) make the product term reduce to Y^(3p) and the two single-joining terms to -Y^p and -2Y^p. The double-joining term has weight at least

    2p+3h-1+alpha,

whose excess over 3p alpha is p/2-1+alpha>0. Thus the scaled polynomial is integral and monic, with reduction

    P_(3p)(rho Y)/rho^(3p) -> Y^p(Y^(2p)-3).        (4.1)

This reduction has p zero roots and 2p nonzero roots counted with multiplicity because p>=5. One may read the associated Newton side, but no separability hypothesis is needed to count these roots: in a finite splitting extension a monic integral polynomial has integral roots, and reducing its factorization into linear factors gives exactly the multiplicities in (4.1). Hence exactly 2p roots of the original polynomial, counted with multiplicity, have valuation alpha; the other p have strictly larger valuation. This is not an application of simple-root Hensel lifting to the repeated roots in (4.1).

At X=tY, divide instead by t^(3p-1). The product A_0 A_1 A_2 has weight at least 3p and disappears. The single-joining terms reduce to -S(Y) and -2S(Y). The double-joining term has weight at least 2p+3h, exceeding 3p-1 by h>0. Consequently

    P_(3p)(tY)/t^(3p-1) -> -3(Y^p+cY).             (4.2)

Its derivative is the nonzero constant -3c. Over a finite residue-field extension it has p distinct roots. Hensel lifting produces p distinct roots at scale t. The p-1 nonzero residual roots have valuation 1; the residual zero lifts to the exact root 0 because P_(3p) is odd. It is simple, since the reduced derivative at zero is nonzero. Distinct residual roots imply pairwise distance valuation 1 among these p roots.

These roots lie strictly inside the alpha scale because alpha<1. They exhaust the p roots not counted at alpha. Section 5 verifies simplicity at alpha directly.

## 5. A derivative residual proves the remaining simplicity

Differentiate (3.4) and evaluate at X=rho Y. The three derivative terms from A_0 A_1 A_2, normalized by t^(3p-2), reduce by (2.2)-(2.3) to 3cY^(2p).

For each single-joining term, the derivative hitting its A factor reduces to -kc for k=1,2. When it hits B_i, (3.2) yields

    v(B'_i(rho Y))>=p-2+alpha.

Multiplication by u_(kp) and the remaining A factor then gives weight at least

    p+(p-2+alpha)+p alpha
      =(3p-2)+(alpha-1/2),

strictly higher than the normalization. The double-joining derivative has weight at least 2p+3h-1 by (3.3), exceeding 3p-2 by h. All discarded terms are therefore coefficientwise strictly higher, proving

    P'_(3p)(rho Y)/t^(3p-2) -> 3c(Y^(2p)-1).       (5.1)

If xi is a root of valuation alpha, its unit residue y=xi/rho satisfies y^(2p)=3 by (4.1). Formula (5.1) therefore reduces at that root to 6c, a unit for every p>=5. All 2p such roots are simple and their derivative valuations are exactly 3p-2.

For the other p roots, differentiate the normalized polynomial in (4.2) with respect to Y. The result is P'_(3p)(tY)/t^(3p-2), with constant reduction -3c. Those roots have the same exact derivative valuation. Together there are 3p distinct roots, proving squarefreeness of P_(3p).

## 6. Local factor and discriminant consequences for p>=5

The set of roots of valuation alpha is invariant under K-automorphisms, because K is complete and its valuation extends uniquely to algebraic extensions. Its monic degree-2p root polynomial I lies in K[X]. If a proper monic K-factor had degree j, its nonzero constant term would have valuation j alpha. The value group of K is Z, while gcd(2p-1,2p)=1; thus 2p must divide j. No j strictly between 0 and 2p qualifies. This proves irreducibility, by the classical primitive-side argument, as a consequence of the proved root valuations.

The remaining nonzero roots likewise define a monic factor J of degree p-1 in K[X], giving P_(3p)=X I J. There is no claim that J is irreducible. No finer same-cluster distances among the I roots are needed or asserted.

For a monic separable polynomial the discriminant, up to a sign, is the product of its derivatives at all roots. Section 5 gives

    v(Disc_X P_(3p))=3p(3p-2).                       (6.1)

This is the ordinary polynomial discriminant in the normalization v(t)=1. It is neither a q-discriminant nor an ordinary p-adic valuation normalized by v(p)=1.

## 7. The exceptional prime p=3: a uniform fixed-degree certificate

The factors 3 and 6 in (4.1)-(5.1) are not units at p=3. Indeed exact controls give a different Newton polygon for P_9, with vertices (1,12),(3,6),(9,0) when s=3. No p>=5 local formula is extended to p=3.

Instead form P_9 directly from the actual integer recurrence. Its parity gives

    P_9(X;q)=X Q(X^2;q),

where Q(Y;q) is monic of degree four in Y with coefficients in Z[q]. Put D(q)=Q(0;q) and Delta(q)=Disc_Y Q(Y;q). Exact polynomial identities are

    D=(q-1)^4 (q^2+q+1) R(q),                        (7.1)
    Delta=(q-1)^12 (q+1)^6 (q^2+1)^2
                 (q^2+q+1)^3 E(q),                 (7.2)

where R is the monic degree-14 polynomial

    R=q^14+4q^13+8q^12+14q^11+22q^10+28q^9
       +34q^8+39q^7+39q^6+36q^5+32q^4+25q^3
       +17q^2+11q+5.

E is a nonzero monic polynomial of degree 52 in Z[q]. Its complete coefficient vector in ascending powers is given in Appendix A. The identities are reproducible exact expansions: check_p3_certificate.py builds P_9 from scratch, verifies (7.1)-(7.2), and checks Delta using both the ordinary resultant discriminant and the explicit 16-term monic-quartic formula. It additionally checks

    Disc_X P_9 = 256 D^3 Delta^2.                    (7.3)

This identity also follows directly by grouping the roots as 0 and the four pairs +/-sqrt(y_i). It supplies an independent ordinary-discriminant consistency check.

Now let q have order 3^s with s>=3. The elementary factors in (7.1)-(7.2) do not vanish: their possible root orders are 1,2,3,4. As Phi_(3^s) is the rational minimal polynomial of q, any rational polynomial vanishing at q must be divisible by Phi_(3^s).

Since deg R=14<phi(27)=18<=phi(3^s), R(q) cannot vanish. Since E is nonzero and deg E=52<phi(81)=54, E(q) cannot vanish for s>=4. The sole remaining s=3 case has the explicit monic-division certificate

    E(q) mod (2, q^18+q^9+1)
       =q^13+q^12+q^10+q^9+q^6+q^5+q^2+q+1,     (7.4)

which is nonzero. If Phi_27 divided E over Q, monic division of integer polynomials would give an integer quotient and zero remainder; reduction modulo 2 would contradict (7.4). Thus E(q) is nonzero also at every primitive 27th root.

We have proved D(q)!=0 and Delta(q)!=0 uniformly for every s>=3. Hence Q has four distinct nonzero roots in characteristic zero. Each has two distinct square roots, and all eight roots of Q(X^2) are distinct and nonzero. Along with the simple zero of X Q(X^2), this proves squarefreeness of P_9. Equivalently (7.3) gives the nonzero ordinary discriminant directly.

This is a finite symbolic certificate with a uniform degree/minimal-polynomial argument in s. It is not an extrapolation from numerical spectra or a claimed census over root orders. No exact p=3 discriminant valuation or root-distance classification is claimed.

## 8. Actual H polynomial, characteristic-zero embeddings, and the kernel

For either case of p, all u_j have positive valuation, so P_(3p)(X) reduces to X^(3p). In odd residue characteristic this makes P_(3p)(2) and P_(3p)(-2) units. The standard exact normalization is

    H_(3p)(v^2;q)=v^(3p) P_(3p)(v+v^(-1);q).       (8.1)

At any H root z, H(0)=1 ensures z!=0. Choose v with v^2=z. In characteristic zero v->v^2 is unramified there. The map v->v+v^(-1) is unramified except at v=+/-1, whose X values +/-2 have already been excluded. The prefactor v^(3p) is a unit. Thus (8.1) preserves root multiplicities locally, and the proved P squarefreeness implies squarefreeness of the actual Gaussian H.

For b=3p all w_k=product_(j=1)^k(1-q^j), 0<=k<=b-1, are nonzero because b<p^s. Consecutive P's are coprime: a common root of P_b and P_(b-1) propagates down the recurrence through nonzero u_j to P_0=1, an impossibility. The accepted ordinary-square Christoffel-Darboux identity at a root xi of P_b is

    sum_(k=0)^(b-1) P_k(xi)^2/w_k
       =P'_b(xi) P_(b-1)(xi)/w_(b-1).

All three factors on the right have now been shown nonzero. This proves the original bilinear nonisotropy guard, without positivity or a replacement Hermitian metric.

The p-adic embedding is injective and all primitive roots of a given order are Galois conjugate. Nonzero discriminants and the polynomial kernel identities are algebraic characteristic-zero statements, so these conclusions hold at every primitive complex embedding. No p-adic inequality is interpreted as complex positivity. Existing local/all-A formulas may only be composed where their other independent guards also hold.

## 9. Fresh checks, exact evidence, and limitations

check_boundary.py is newly authored standard-library integer polynomial code. At p=5,7,11,13 and s=2 it rebuilds the actual recurrence and checks the exact triple-block identity including both joining edges, shifted-block coefficient bounds, all three p-block residuals, both target residuals, both derivative residuals, exact Newton vertices, primitive-side denominator, and nonzero residual derivatives. Its cyclotomic reduction is exact: after reduction modulo Phi_(p^s) and substitution q=1+t, the t degree is below e; the weights e*v_p(a_j)+j are distinct modulo e, so the least nonzero weight cannot cancel. The leading-unit rule uses p/t^e -> -1. The p=3 negative control expressly verifies the failure of the generic alpha reduction and the different degree-nine Newton vertices.

check_p3_certificate.py independently rebuilds P_9 with installed SymPy 1.14.0, verifies every polynomial identity and the explicit remainder used in Section 7, and records the full exact coefficients. It does not read the exploratory polynomial file or import prior programs. Neither checker supplies the infinite-prime justification for Sections 2-6; that justification is the symbolic proof above. The p=3 identities plus cyclotomic degree argument constitute the fixed-degree proof in Section 7.

Both final checker commands and output files are retained. SOURCE_BINDINGS.json binds the exact accepted inputs and the fresh index read. MANIFEST.json freezes the final author packet; independent review is still required. Explorations are separately labeled development and are not acceptance evidence. No external service or repository writes were performed.

The next original gate is genuinely later degrees b>3p below the root order, not another audit of the already accepted third partial block. The broader owner remains open at priority 58. This packet neither ranks the result's novelty nor changes the research index.

## Appendix A. Exact E52 coefficient vector

In ascending powers q^0,...,q^52, the coefficients of E in (7.2) are:

    [400,1200,3484,8140,17353,32979,59408,99345,158657,
     240592,350885,490963,664623,868696,1102292,1356748,
     1625307,1893889,2152130,2383469,2577374,2720023,
     2805073,2825452,2782425,2677227,2518707,2315386,
     2080597,1826209,1566017,1310706,1070721,852721,
     661837,499942,367300,261962,181195,121251,78354,
     48745,29108,16603,9008,4611,2207,978,392,138,41,9,1].

The final entry 1 proves both monicity and nonzero degree 52 independently of any evaluation at a root of unity.
