# Independent separating residual at degree 2p

19 October 2026. Local theoretical note; no external or canonical-record write. The estimates below hold uniformly for every odd prime p and every primitive p^s-th root q with s >= 2. This note uses the accepted coefficient bounds in the two supplied reports and supplies the missing second-scale separation.

## Statement

Let t=q−1, v(t)=1, e=v(p)=p^(s−1)(p−1),

- alpha=(2p−1)/(2p),
- c0=(−1)^((p+1)/2) in the valuation ring and c its residue,
- u_j=1−q^j,
- C=product_(j=1)^p u_(2j−1)=−P_(2p)(0).

Choose kappa with kappa²=C. Choose any root a of the explicit auxiliary equation

    a^p+c0 t^(p−1)a=kappa.

These are finite algebraic extensions of the complete base field; neither choice uses a root of P_(2p). Then v(kappa)=p−1/2 and v(a)=alpha. The actual polynomial has the integral translated normalization

    P_(2p)(a+tZ)/(2 kappa t^p)  ->  Z^p+cZ.

Here the arrow means coefficientwise reduction modulo the maximal ideal. The residual derivative is the nonzero constant c. It therefore gives p distinct roots around a. Their negatives give p distinct roots around −a, exhausting all 2p roots.

If i²=−1 in a finite residue-field extension, the residual roots are precisely i F_p. Thus the roots may be written

    x_r=a+t z_r,     z_r reduces to i r,     r in F_p,

and their negatives. All within-cluster pairwise differences have valuation exactly 1, and all between-cluster differences have valuation exactly alpha. Consequently

    v(Disc_X(P_(2p)))=p(4p−3).

## Proof

### 1. Auxiliary centers

The odd numbers 1,3,...,2p−1 consist, modulo p, of 0 and each nonzero residue once. The sole multiple of p is p. Hence v(C)=p+(p−1)=2p−1, and C/t^(2p−1) reduces to (−1)(p−1)!=1. Thus v(kappa)=p−1/2.

The Newton polygon of X^p+c0 t^(p−1)X−kappa has points (0,p−1/2),(1,p−1),(p,0). The middle point lies strictly above the segment between the endpoints: its excess is (p−1)/(2p). Therefore the Newton polygon has one slope −alpha, and every root a has valuation alpha. Choosing −a supplies the center for −kappa. Consistent fractional-power normalizations put a and −a in the two original residual classes +1 and −1, in either order.

### 2. Approximation by the squared auxiliary polynomial

Set A0(X)=X^p+c0 t^(p−1)X. Write the accepted block identity as

    P_(2p)(X)=F_p(X) P_p(X)−u_p R(X),
    R(X)=G_(p−1)(X) P_(p−1)(X).

The constant term of R is the product of all odd edge coefficients except u_p, so u_p R(0)=C.

The accepted p-block estimates state that every lower coefficient of P_p has valuation at least p−1, and its linear coefficient divided by t^(p−1) reduces to c. Since coefficients belong to the base field, whose value group is Z, the difference between that linear coefficient and c0 t^(p−1) has valuation at least p. Since P_p is odd, every other omitted monomial has degree at least 3. For a variable of valuation alpha this proves

    v(P_p−A0) >= min(p+alpha,p−1+3alpha)>p,

where the second term is absent if p=3. The accepted shifted-edge comparison gives F_p−P_p coefficientwise valuation at least p. This difference is odd, so

    v(F_p−P_p)>=p+alpha>p.

All these estimates hold coefficientwise after X=a+tZ, because v(a)=alpha<1=v(t).

Each of the two even continuants in R has p−1 vertices and unit-order internal edges. Its coefficient of X^(2j) has valuation at least (p−1)/2−j, by the matching expansion. Consequently the coefficient of X^(2k) in R has valuation at least p−1−k. As 2alpha−1>0,

    v(u_p(R(X)−R(0)))
      >=p+(p−2)+2alpha
       =2p−1/p
       >2p−1/2.

Let L=2p−1/2=v(kappa t^p). Both A0(a+tZ) and the two odd blocks have valuation at least p alpha=p−1/2. The preceding bounds therefore imply the coefficientwise approximation

    P_(2p)(a+tZ)
      = A0(a+tZ)^2−C + E(Z),    v(E)>L.

### 3. The simple residual

By the defining equation of a,

    A0(a+tZ)−kappa
      =t^p(Z^p+c0 Z)
       +sum_(k=1)^(p−1) binom(p,k) a^(p−k)t^k Z^k.

Every coefficient in the sum has valuation

    e+(p−k)alpha+k >= e+(p−1)alpha+1 > p.

Thus (A0(a+tZ)−kappa)/t^p is integral and reduces to Z^p+cZ. Factoring the difference of squares now gives

    (A0(a+tZ)^2−kappa²)/(2 kappa t^p)
      -> Z^p+cZ,

because v(t^p/kappa)=1/2>0 and 2 is a unit. The error E vanishes under this normalization. This proves the displayed residual for the actual P_(2p).

### 4. Root count, spacing, and discriminant

The residual derivative is c != 0, so it has p distinct roots in a finite residue-field extension, each lifting by simple-root Hensel. If i²=−1, then

    i^(p−1)=(−1)^((p−1)/2)=−c,

so the roots are exactly i F_p. The lifts x_r=a+t z_r satisfy v(x_r−x_s)=1 for r != s because z_r−z_s has nonzero residue.

The polynomial P_(2p) is even. Hence −x_r are also roots. A difference between a root in the first list and one in the negative list is 2a+t(z_r+z_s); its valuation is alpha<1. Thus the two lists are disjoint and exhaust the degree 2p. This proves squarefreeness uniformly.

There are p(p−1) unordered within-cluster pairs in total and p² cross-cluster pairs. For a monic polynomial the discriminant is the product of squared pairwise differences, giving

    v(Disc)=2p(p−1)+2p² alpha=p(4p−3).

## Actual-root-centered version

Once any root xi in one boundary cluster is selected, the identical estimates give

    P_(2p)(xi+tZ)/(2 xi^p t^p) -> Z^p+cZ.

This formulation also proves that the entire original p-fold cluster lies in the closed radius-v=1 disc around xi, with precisely the spacing above. The auxiliary-center formulation supplies the same result without selecting a root of the target polynomial first.

## Scope

This resolves the entire first b=2p boundary for odd p and s>=2. It does not assert a subsequent-block theorem or unrestricted degree squarefreeness. A finite exact local transcription check was freshly authored and run for p=3,5,7,11; the proof above, rather than those checks, supplies the unlimited result.

## Independent irreducibility shortcut

The accepted boundary already states that every root of the degree-2p monic polynomial has valuation alpha=(2p−1)/(2p), in lowest terms. Over K=Q_p(q), normalized valuation values of nonzero elements are integers. If a monic factor over K had degree m with 0<m<2p, its nonzero constant term would have valuation m alpha, which must be integral. Coprimality of 2p−1 and 2p forces 2p to divide m, a contradiction. Hence P_(2p) is irreducible over K. Characteristic zero then gives squarefreeness immediately. The translated residual above supplies additional cluster geometry and the exact discriminant valuation; it is not required for the logical nonvanishing conclusion.
