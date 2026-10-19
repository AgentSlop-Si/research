# Independent review: F020 at b = 3p+1

19 October 2026 UTC. This review concerns only the single successor degree 3p+1, composed with the already accepted range when explicitly stated. It makes no originality, performance, priority, or unrestricted-closure claim. No external writes were performed.

## Verdict

PASS within the following exact scope. This acceptance binds to candidate REPORT.md SHA-256 160aec115887d4c7e02bf5c3213f30b526275e14ebe6aaa5d66d1465c1920117 and candidate MANIFEST.json SHA-256 db88b6dfc44009f4bbaefae34f553504cece03f5af9c6bbc96077247dfb09582. All 25 candidate manifest entries, all 46 accepted dependency manifest entries, and all five source-copy bindings were independently verified. The full independently computed p=3 discriminant coefficients and integer cyclotomic remainders match the frozen author evidence.

For every odd prime p and every primitive p^s-th root q satisfying 3p+1 < p^s, the actual recurrence

    P_0=1, P_1=X, P_(n+1)=XP_n−(1−q^n)P_(n−1)

has squarefree P_(3p+1) in characteristic zero. The actual Gaussian polynomial H_(3p+1) is squarefree, and the original ordinary-square Christoffel–Darboux kernel is nonzero at every P_(3p+1) root.

For odd primes p>=5, with v(q−1)=1, the root groups have sizes and valuations

    2p at alpha=(2p−1)/(2p),
    p−1 at 1,
    2 at gamma=(p+1)/4.

Their derivative valuations are respectively 3p−2+alpha, 3p−1, and 3p−2+gamma. The ordinary X-discriminant valuation is exactly 9p^2+(p−7)/2. These local conclusions are not asserted at p=3, which is handled by a separate exact certificate.

Together with the accepted predecessor range this extends the supported degree range to b<=3p+1 with b<p^s. No degree b>=3p+2 is proved here, and no other all-A guard follows automatically.

## 1. Accepted dependency and quantifiers

The prior accepted boundary report is the packet f020_three_p_boundary_20261019_1613, with independent review f020_three_p_boundary_review_20261019_1618. Its three polynomial reductions—not merely its asserted root count—are used below. The accepted p-block coefficient estimates in that report also suffice for the short adjacent-polynomial argument.

The hypothesis means s>=2 for p>=5 and s>=3 for p=3. Put K=Q_p(q), t=q−1, e=v(p)=p^(s−1)(p−1), u_j=1−q^j, h=(p−1)/2, c=(−1)^(h+1), d=(p−2)!!, and f=2^h h!. The field K has integral value group, and df=(p−1)!=−1 in the residue field. For p>=5 the three bridge edges satisfy

    u_(kp)/t^p -> −k, k=1,2,3.

These residues are all units. The extension from k=2 in the predecessor to k=3 is legitimate because p does not divide 3. It is not legitimate at p=3, which the candidate correctly separates.

For G=P_(3p) and rho^(2p)=t^(2p−1), the accepted integral reductions are

    G(rho Y)/rho^(3p) -> Y^p(Y^(2p)−3),
    G(tY)/t^(3p−1) -> −3(Y^p+cY),
    G'(rho Y)/t^(3p−2) -> 3c(Y^(2p)−1).

In particular the linear coefficient of G has exact valuation 3p−2 and residue −3c. No assumed persistence of individual predecessor roots is used.

## 2. Independent derivation of the adjacent-polynomial estimates

Write C[a,b] for the continuant on vertices a,...,b, with internal edges u_a,...,u_(b−1). Set

    A=C[1,p], B=C[p+1,2p], T=C[2p+1,3p−1],
    D=C[1,p−1], E=C[p+2,2p], J=C[p+1,2p−1],
    U=C[2p+2,3p−1], M=C[p+2,2p−1].

For V=P_(3p−1), partitioning matchings according to bridge-edge selection gives exactly

    V=ABT−u_p DET−u_(2p) AJU+u_pu_(2p) DMU.

The sign of the double-bridge term is positive. Both M and U have odd degree p−2. This identity was independently verified over the integer polynomial ring at p=3,5,7, without importing or executing a candidate checker.

The four even paths D,E,J,T have degree 2h. Matching bounds give coefficient valuation at least h−j at X^(2j). At a scale beta>1/2 their constant monomial dominates; the constant residues after division by t^h are d,f,d,d respectively. The odd paths M,U have scale valuation at least h−1+beta. The two p-block estimates supply scale weights p alpha at rho and p at t.

Let L=p+3h=(5p−3)/2. At rho the four displayed terms have weights bounded below by

    2p alpha+h=L,
    p+3h=L,
    p+2h−1+(p+1)alpha,
    2p+3h−2+2alpha.

The latter two have positive excesses (p+1)(alpha−1/2) and p−2+2alpha over L. The first term reduces to dY^(2p), using rho^(2p)=t^(2p−1). The second reduces to −d, because u_p/t^p=−1 and df=−1. Therefore

    V(rho Y)/t^L -> d(Y^(2p)−1).

At t the corresponding bounds are L+1,L,L+h+1,L+p, so

    V(tY)/t^L -> −d.

At every larger scale beta>=1 the nonconstant monomials only gain valuation. This proves the same constant reduction at the central scale without an unproved higher-tail extension.

## 3. Root counts at three genuinely separate scales

Let F=P_(3p+1)=XG−u_(3p)V and W=p+L=(7p−3)/2.

At rho the perturbation has weight at least W, whose excess over (3p+1)alpha is (p−1)^2/(2p)>0. Hence the monic normalized polynomial has reduction

    F(rho Y)/rho^(3p+1) -> Y^(p+1)(Y^(2p)−3).

Reduction of a monic integral splitting factorization counts exactly 2p roots of valuation alpha, with multiplicity; the remaining p+1 have larger valuation. This count does not use simple-root Hensel lifting on an inseparable residual polynomial.

At t, W−3p=(p−3)/2>0, so

    F(tY)/t^(3p) -> −3Y^2(Y^(p−1)+c).

Its p−1 nonzero residual roots are simple, with derivative −3cy at such a root y. Hensel lifting after a finite residue extension gives p−1 distinct roots of valuation 1. The double zero is not mistakenly declared simple.

Choose sigma with sigma^2=t^((p+1)/2), giving gamma=(p+1)/4>1 and W=3p−2+2gamma. Integrality of the accepted t-scale reduction gives v([X^j]G)>=3p−1−j. Since G is odd, the linear term is followed only by j>=3, and every such term in XG at sigma has strict excess (j−1)(gamma−1)>0 over W. The remaining constant contribution is determined by V and u_(3p), yielding

    F(sigma Y)/t^W -> −3(cY^2+d).

This quadratic has two distinct nonzero roots in a finite residue extension. It therefore produces two distinct roots of valuation gamma. Integral nonmonic polynomials are sufficient for this simple-root Hensel application; there is no assumption that the normalized polynomial remains monic at t or sigma.

The counts 2p+(p−1)+2=3p+1 exhaust the full degree. The valuation groups are disjoint because alpha<1<gamma. For p=5 they are 9/10,1,3/2, and the middle perturbation excess is 1. Thus the smallest generic prime is safely included.

## 4. Outer-root simplicity and derivative valuations

The direct global rho reduction of F' would be invalid because the G term need not have sufficiently high weight. The candidate instead uses the exact Euler cancellation

    R=XF'−F=X^2G'+u_(3p)(V−XV').

For each monomial, differentiating and then multiplying by X preserves its scale weight; the integer exponent cannot decrease valuation. Thus V−XV' has rho-scale weight at least L. Its contribution to R has weight at least W, with strict excess

    W−(3p−2+2alpha)=(p−3)/2+1/p>0.

At p=5 this is 6/5. There is no equality or hidden borderline term. The accepted derivative reduction consequently gives

    R(rho Y)/(rho^2 t^(3p−2)) -> 3cY^2(Y^(2p)−1).

For an outer F-root xi, its residue y=xi/rho satisfies y^(2p)=3 and y!=0. The displayed residue is 6cy^2, a unit for all p>=5. Since R(xi)=xi F'(xi), each outer root is simple and v(F'(xi))=3p−2+alpha.

Differentiation of the integral t-scale reduction gives valuation 3p−1 at every nonzero t-scale root. Differentiation at sigma gives nonzero residue −6cY and valuation W−gamma=3p−2+gamma at the central roots. These operations differentiate the characteristic-zero integral normalized polynomials before reduction; mixed-characteristic multiples cannot lower any discarded valuation.

The monic discriminant product formula then gives

    2p(3p−2+alpha)+(p−1)(3p−1)+2(3p−2+gamma)
      =9p^2+(p−7)/2.

This is the ordinary X-discriminant with v(t)=1. No p=3 specialization of this valuation is justified or claimed.

## 5. Independent p=3 certificate

The reviewer independently rebuilt P_10 over Z[X,q], extracted P_10(X)=Q_5(X^2), and computed its ordinary Y-discriminant Delta directly. The constant polynomial is

    D=Q_5(0)=product_(j in {1,3,5,7,9})(q^j−1),

of degree 25. It cannot vanish at a primitive 3^s root for s>=3 because each listed positive exponent is below 27.

Delta is a monic degree-140 integer polynomial. Exact integer division and rational gcd calculations against Phi_27 and Phi_81 independently gave nonzero remainders and gcd degree zero. Modulo 2 the remainders agree coefficient-for-coefficient with the candidate's explicit certificates. Full integer remainders and the complete Delta coefficient vector are retained in P3_CHECKS.json.

For s>=5, deg Phi_(3^s)>=162>140, so the nonzero Delta cannot be divisible by the primitive root's rational minimal polynomial. Orders 27 and 81 were separately checked, exhausting every allowed s. This is an infinite-order proof based on a fixed-degree exact certificate and a degree bound, not a numerical extrapolation.

A separate direct calculation of the full degree-ten ordinary X-discriminant verified

    Disc_X P_10 = −1024 D Delta^2.

Therefore Q_5 has five distinct nonzero roots; their ten characteristic-zero square roots are all distinct. The p=3 squarefreeness claim passes without any unproved local valuation assertion.

## 6. Actual H normalization, embeddings, and bilinear kernel

The exact Gaussian identity

    H_n(v^2;q)=v^n P_n(v+v^(-1);q)

was independently checked at n=10,16,22 by rebuilding Gaussian coefficients with their Pascal recurrence. H_n(0)=1. Since every u_j has positive valuation, P_n reduces to X^n and P_n(2),P_n(−2) are units for odd p. At an H_n root one has v!=0 and P_n's root is not ±2. Thus both coordinate maps v->v^2 and v->v+v^(-1) are unramified there, and the prefactor v^n is a local unit. Multiplicities transfer, proving squarefreeness of the actual H family.

For n=3p+1, all weights w_k=product_(j=1)^k u_j, 0<=k<=n−1, are nonzero by n<p^s. Consecutive recurrence polynomials are coprime by downward propagation through those nonzero edges. A fresh denominator-cleared polynomial calculation at n=10,16,22 verified the full ordinary-square CD telescope, not merely one telescoping step. At a P_n root the identity reads

    sum_(k=0)^(n−1) P_k(xi)^2/w_k
      =P_n'(xi)P_(n−1)(xi)/w_(n−1),

which is nonzero by squarefreeness and coprimality. No positivity or Hermitian replacement is used.

An injective p-adic embedding proves algebraic nonvanishing for the corresponding cyclotomic element. Every primitive root of a fixed order is Galois conjugate, so the statements hold for every primitive characteristic-zero embedding, including every primitive complex q.

## 7. Fresh reproducibility and finite-check limitations

Three reviewer programs were authored and run from scratch; none imports or executes a candidate or historical checker.

- check_recurrence.py builds exact recurrence coefficients in F_p[T]/(T^cut). At p=5,7,11,13,17,19,23,29,31 it checks V at both relevant scales, F at all three scales, Euler derivative cancellation, middle and central derivative residuals, even parity, exact Newton vertices, derivative units, and the discriminant valuation sum.
- check_exceptional.py rebuilds P_10 and Q_5, computes the full ordinary quintic discriminant, verifies integer/mod-2 remainders and rational gcds for orders 27 and 81, and independently checks the full degree-ten discriminant identity.
- check_exact_identities.py rebuilds the integer path recurrence at p=3,5,7, checks the adjacent-polynomial block identity and successor recurrence, rebuilds actual Gaussian coefficients, and verifies the complete denominator-cleared CD identity at n=10,16,22.

Every modular weighted target is at most W, and W<p(p−1)<=v(p) for p>=5. Every omitted T power is above W as well. Thus reduction modulo p and T truncation cannot conceal a term at a tested weight, including after the particular X derivatives. At p=5, W=16<20=v(p), providing an explicit small-prime check of this safeguard. The finite prime controls validate transcription; the unlimited prime theorem rests on the symbolic estimates above.

All controls pass. The final candidate, accepted dependency manifests, and reviewer artifacts are checksum-bound separately. F020 remains open beyond this degree.
