# F020: the single successor degree b = 3p+1

19 October 2026 UTC. Scoped author proof candidate; independent review required. No external write, owner closure, scoring change, or originality claim.

## Result and exact scope

Let p be an odd prime, q a primitive p^s-th root of unity, and assume 3p+1<p^s. For the actual polynomials

    P_0=1, P_1=X, P_(n+1)=X P_n−(1−q^n)P_(n−1),
    H_n(z;q)=sum_(k=0)^n [n choose k]_q z^k,

the polynomials P_(3p+1) and H_(3p+1) are squarefree in characteristic zero. At every root xi of P_(3p+1), the original ordinary-square kernel

    sum_(k=0)^(3p) P_k(xi;q)^2 / product_(j=1)^k(1−q^j)

is nonzero. These are bilinear algebraic squares, not absolute-value squares.

For p>=5, put t=q−1 and normalize v(t)=1 in K=Q_p(q). The degree 3p+1 polynomial has exactly:

- 2p roots of valuation alpha=(2p−1)/(2p);
- p−1 roots of valuation 1;
- 2 roots of valuation gamma=(p+1)/4.

Their respective derivative valuations are 3p−2+alpha, 3p−1, and 3p−2+gamma. Consequently the ordinary polynomial discriminant satisfies

    v(Disc_X P_(3p+1)) = 9p^2+(p−7)/2.                (0.1)

No version of this local classification or discriminant valuation is asserted for p=3. The p=3 conclusion uses a separate exact degree-ten certificate, valid for all s>=3. For p>=5 the strict below-order hypothesis permits every s>=2. There is no allowed s=2 case at p=3.

Composed with the accepted range b<=3p and b<p^s, this establishes b<=3p+1 and b<p^s. Only b=3p+1 is new here. Nothing is claimed for b>=3p+2, an entire fourth partial block, arbitrary odd-composite root orders, unrestricted F020/all-A closure, computational improvement, or historical originality. Newton polygons, Hensel lifting, continuants, and discriminant identities remain classical tools.

## 1. Accepted inputs, notation, and normalization

The accepted boundary proof is `original-source/f020_three_p_boundary_20261019_1613/REPORT.md`, SHA-256 `90385545114303539d4c29e9cc6cde2383480d6ad94cad83899ecc4f1cab0762`. Its independent acceptance is `original-source/f020_three_p_boundary_review_20261019_1618/INDEPENDENT_REVIEW.md`, with the verdict bound to the preceding report and its manifest. Source copies, hashes, and full source-manifest checks accompany this packet. Prior programs are neither imported nor executed.

For Sections 1–5 assume p>=5. Set

    u_j=1−q^j, h=(p−1)/2, c=(−1)^(h+1),
    d=(p−2)!!, f=2^h h!, df=(p−1)! = −1 mod p,
    L=p+3h=(5p−3)/2, W=p+L=(7p−3)/2.

The accepted valuation setup gives v(K^×)=Z and e=v(p)=p^(s−1)(p−1). Non-p-multiple edges below the root order have valuation 1, and

    u_(kp)/t^p -> −k, k=1,2,3.                       (1.1)

All three residues are units for p>=5. Let rho satisfy rho^(2p)=t^(2p−1), so v(rho)=alpha. Every displayed polynomial reduction is coefficientwise in its displayed indeterminate.

Write G=P_(3p). The accepted proof supplies the polynomial reductions

    G(rho Y)/rho^(3p) -> Y^p(Y^(2p)−3),              (1.2)
    G(tY)/t^(3p−1) -> −3(Y^p+cY),                    (1.3)
    G'(rho Y)/t^(3p−2) -> 3c(Y^(2p)−1).              (1.4)

These are integral normalized polynomials. In particular the coefficient of X in G has valuation 3p−2 and leading residue −3c. The accepted p-block coefficient estimate is also used: each length-p block beginning at 1 or p+1 has reduction Y^p at rho scale after normalization by rho^p, and reduction Y^p+cY at t scale after normalization by t^p. No assertion about root persistence is assumed or inferred merely from these facts.

## 2. The needed adjacent polynomial and its exact block identity

For vertices a through b let C[a,b] be the path continuant with internal edges u_a,...,u_(b−1), with an empty path equal to 1. Define

    A_0=C[1,p],             A_1=C[p+1,2p],
    T=C[2p+1,3p−1],
    L_0=C[1,p−1],           R_1=C[p+2,2p],
    L_1=C[p+1,2p−1],        U=C[2p+2,3p−1],
    M=C[p+2,2p−1].

Here T,L_0,R_1,L_1 have even degree p−1=2h, while U,M have odd degree p−2=2h−1. Put V=P_(3p−1). Partitioning matchings by the two joining edges gives the exact identity

    V=A_0 A_1 T −u_p L_0 R_1 T −u_(2p) A_0 L_1 U
                    +u_p u_(2p) L_0 M U.           (2.1)

The double-joining term is included. In particular neither its sign nor the odd length of each remaining middle/tail path is omitted.

For an n-vertex path whose internal edges all have valuation 1, the coefficient of X^(n−2j) has valuation at least j, since each matching uses j edges. At either beta=alpha or beta=1 this implies:

- every even path above has valuation at least h at X of scale beta;
- its constant term is the unique lowest-weight monomial, because beta>1/2;
- T,L_0,L_1 have normalized constant residue d, and R_1 has residue f;
- each odd path U,M has coefficientwise scaled valuation at least h−1+beta.

The residues of the alternating edge products yield the constants d,f directly, with the continuant signs cancelling the minus signs in u_j/t -> −j. They are units.

At rho scale the four terms of (2.1) have valuation bounds

    2p alpha+h=L,
    p+3h=L,
    p+2h−1+(p+1)alpha,
    2p+3h−2+2alpha.

The last two bounds exceed L by (p+1)(alpha−1/2)>0 and p−2+2alpha>0, respectively. The first two residues are dY^(2p) and −d. Therefore

    V(rho Y)/t^L -> d(Y^(2p)−1).                    (2.2)

At t scale those same four bounds become L+1, L, L+h+1, and L+p. Only the second term survives. Thus

    V(tY)/t^L -> −d.                                (2.3)

These bounds remain valid at every higher scale beta>=1, and the constant reduction in (2.3) remains −d there. This last statement follows by replacing tY by an element of valuation beta times Y: nonconstant monomials only gain valuation. In particular it requires no new tail theorem beyond this even path of length p−1.

## 3. Three scale reductions and a complete count

Let F=P_(3p+1). The original recurrence is exactly

    F=XG−u_(3p)V.                                  (3.1)

At rho scale the first term, divided by rho^(3p+1), has reduction Y^(p+1)(Y^(2p)−3). The second term has valuation at least W, and its strict excess over (3p+1)alpha is

    W−(3p+1)alpha = (p−1)^2/(2p)>0.                (3.2)

Hence the integral monic normalized polynomial satisfies

    F(rho Y)/rho^(3p+1) -> Y^(p+1)(Y^(2p)−3).       (3.3)

In a finite splitting extension, a monic integral polynomial has integral roots. Reducing its factorization shows that exactly 2p roots, counted with multiplicity, have valuation alpha, and the other p+1 have valuation strictly greater than alpha. The repeated nonzero roots of the residue polynomial in characteristic p do not justify simple-root Hensel lifting, and no such lifting is used at this scale.

At t scale, W−3p=(p−3)/2>0, including the smallest generic prime p=5. Equations (1.3), (2.3), and (3.1) give

    F(tY)/t^(3p) -> −3Y^2(Y^(p−1)+c).              (3.4)

Its p−1 nonzero roots are simple: at one such root y the derivative is −3cy, a unit. After a finite residue-field extension, simple-root Hensel lifting therefore gives p−1 distinct roots of valuation 1. The repeated residual zero is not lifted using this assertion.

Choose sigma with sigma^2=t^((p+1)/2). Its valuation is gamma=(p+1)/4>1, and

    W=3p−2+2gamma.

The linear term in G, multiplied by X, gives a quadratic contribution with residue −3cY^2 in F(sigma Y)/t^W. To check every higher term, integrality in (1.3) gives

    v([X^j]G)>=3p−1−j.

For every odd j>=3, the term [X^j]G · X^(j+1) has excess over W at least

    (j−1)(gamma−1)>0.

Using the constant reduction (2.3) at this higher scale, and (1.1) for k=3, proves

    F(sigma Y)/t^W -> −3(cY^2+d).                  (3.5)

Because p is odd and c,d,3 are units, this quadratic has two distinct nonzero roots over a finite residue extension. Hensel lifting yields two distinct roots of valuation gamma. The 2p roots at alpha, the p−1 roots at 1, and these two roots count the full degree 3p+1. Simplicity of the first group is checked next, not assumed from counting.

## 4. A root-aware derivative argument

It would be incorrect to claim that F' at rho scale is globally dominated by XG': the G term in F'=G+XG'−u_(3p)V' has a lower possible coefficientwise weight. Instead use the exact polynomial

    R=XF'−F = X^2G' + u_(3p)(V−XV').               (4.1)

Differentiating a monomial and then multiplying by X preserves its scaled monomial weight; the integer exponent can only increase valuation. Consequently (2.2) bounds V−XV' at rho scale below by L. The perturbation in (4.1) has valuation at least W. Its strict excess over the normalization of X^2G' is

    W−(3p−2+2alpha) = (p−3)/2+1/p>0.              (4.2)

For p=5 this gap is exactly 6/5; it never vanishes in the permitted generic range. By (1.4),

    R(rho Y)/(rho^2 t^(3p−2))
        -> 3cY^2(Y^(2p)−1).                       (4.3)

If xi is one of the 2p roots of F of valuation alpha, its residue y=xi/rho is nonzero and satisfies y^(2p)=3 by (3.3). Thus (4.3) evaluated there is 6cy^2, a unit for every p>=5. Since R(xi)=xi F'(xi), this proves that all 2p such roots are simple and

    v(F'(xi))=3p−2+alpha.

For the roots of valuation 1, differentiating the integral normalized polynomial in (3.4) gives a unit derivative at each nonzero residual root. The chain-rule normalization is F'(tY)/t^(3p−1), so their derivative valuation is 3p−1. For the two roots at gamma, differentiating (3.5) yields nonzero residue −6cY; their derivative valuation is W−gamma=3p−2+gamma.

All roots of F are now proved distinct. For a monic polynomial its ordinary discriminant is, up to sign, the product of the derivatives at all roots. Summing the proved valuations gives

    2p(3p−2+alpha)+(p−1)(3p−1)+2(3p−2+gamma)
       =9p^2+(p−7)/2,

which proves (0.1). This is the ordinary discriminant in X with v(t)=1; it is not a q-discriminant or a valuation normalized by v(p)=1. No discriminant formula is carried into p=3.

## 5. The separate prime p=3

Here the required below-order degree is b=10, so s>=3. Rebuild P_10 directly over Z[q,X] from the specified recurrence. Its even parity gives

    P_10(X;q)=Q_5(X^2;q),

where Q_5 is monic quintic in Y. Let D(q)=Q_5(0;q) and Delta(q)=Disc_Y Q_5(Y;q), the ordinary Y-discriminant. The exact constant product is

    D=−(1−q)(1−q^3)(1−q^5)(1−q^7)(1−q^9).        (5.1)

It is nonzero at every primitive 3^s-th root with s>=3, since none of those five positive exponents reaches 27.

The self-contained exact checker constructs Q_5 rather than reading stored coefficients. It computes Delta as a monic degree-140 integer polynomial. Its full ascending coefficient vector, and all six Q_5 coefficient vectors, are retained in EXACT_CHECKS.json. The two needed certificates are

    Delta mod (2,Phi_27)
      =q^17+q^16+q^15+q^13+q^8+q^5+q^3,           (5.2)

    Delta mod (2,Phi_81)
      =q^51+q^49+q^48+q^47+q^45+q^44+q^43
       +q^37+q^36+q^34+q^32+q^31+q^30+q^27
       +q^25+q^24+q^23+q^21+q^20+q^15+q^14
       +q^9+q^6+q^4+q^2+q.                        (5.3)

Both are nonzero. If either monic cyclotomic polynomial divided Delta over Q, monic integer division would have zero remainder, including modulo 2. Thus Delta is nonzero at primitive roots of orders 27 and 81. For s>=5, deg Phi_(3^s)>=162>140, so the nonzero Delta cannot vanish at a primitive 3^s-th root by the minimal-polynomial degree bound.

Consequently Q_5 has five distinct nonzero roots at every allowed q. Their ten square roots in characteristic zero are all distinct, which proves squarefreeness of P_10. As an additional exact ordinary-discriminant check, the program independently requests the full X-discriminant and verifies

    Disc_X P_10 = −1024 D Delta^2.                  (5.4)

The sign and constant in (5.4) are the even-composition identity for a monic quintic Q_5. This section is a finite exact polynomial certificate followed by a uniform degree argument, not an extrapolation from numerical roots. It makes no root-slope, irreducibility, or discriminant-valuation assertion for p=3.

## 6. Actual Rogers–Szego family and the original kernel

For n=3p+1 the established normalization is

    H_n(v^2;q)=v^n P_n(v+v^(-1);q).                (6.1)

All u_j have positive valuation, so P_n reduces to X^n; therefore P_n(2) and P_n(−2) are units in odd residue characteristic. Also H_n(0)=1. At an H_n root z choose v!=0 with v^2=z. Both v->v^2 and v->v+v^(-1) are unramified in characteristic zero at that point, the latter because its only ramification values ±2 have just been excluded. The prefactor v^n is a unit. Hence (6.1) preserves multiplicities and the proved P_n squarefreeness transfers to the actual Gaussian H_n.

Every w_k=product_(j=1)^k u_j for 0<=k<=n−1 is nonzero because n<p^s. A common root of P_n,P_(n−1) propagates downward through the recurrence to P_0=1, which is impossible. The original diagonal Christoffel–Darboux identity at a root xi of P_n is

    sum_(k=0)^(n−1) P_k(xi)^2/w_k
       =P_n'(xi)P_(n−1)(xi)/w_(n−1).

Each factor on the right is now nonzero. The identity concerns ordinary algebraic squares and does not assume positivity or replace the bilinear metric with a Hermitian one.

The p-adic embedding is injective, and primitive roots of any fixed order are Galois conjugate. These discriminant and kernel nonvanishing statements therefore hold at every primitive characteristic-zero embedding, including the complex ones.

## 7. Fresh reproducibility and stopping point

`check_uniform.py` is newly authored standard-library code. At p=5,7,11,13,17,19,23 it rebuilds the exact recurrence over F_p[T]/(T^(W+2)) with q=1+T. It checks the adjacent-polynomial identity (2.1), all accepted reductions actually used, (2.2)–(2.3), all three new scales, the exact root-aware derivative identity (4.1), its reduction (4.3), both simple-root derivative reductions, and the exact lower Newton vertices

    (0,W), (2,3p−2), (p+1,2p−1), (3p+1,0).

All tested target weights are at most W, and W<e_min=p(p−1) for every p>=5. Thus dropping integer multiples of p cannot conceal a term at a tested weight; omitted T powers likewise lie above every target, including after differentiation. The checks are faithful finite transcription controls, while Sections 1–4 prove the unlimited prime statement.

`check_exact.py` freshly rebuilds the integer recurrence, computes the degree-ten certificate in Section 5, verifies both nonzero remainders and rational gcds, and checks (5.4). At n=10,16,22 it independently rebuilds the Gaussian binomial coefficients and verifies (6.1), H_n(0)=1, and the polynomial CD telescope. It imports no prior checker or exploratory coefficient file.

The report and evidence will be frozen in MANIFEST.json. The independent reviewer must decide acceptance. The next uncovered degree is b=3p+2 below the root order; no result about it is asserted here. F020 remains open, F023 remains its alias, and the inherited priority remains 58. No external writes were performed.
