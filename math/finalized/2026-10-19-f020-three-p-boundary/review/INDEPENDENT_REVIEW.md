# Independent review: F020 at the boundary b = 3p

19 October 2026 UTC. Candidate directory: `f020_three_p_boundary_20261019_1613`.

## Verdict and precise scope

**PASS: accepted within the precise scope below.** The boundary statement is valid: for every odd prime p and every primitive p^s-th root q satisfying 3p < p^s, the actual recurrence polynomial P_(3p) and actual Gaussian Rogers–Szego polynomial H_(3p) are squarefree in characteristic zero. The original ordinary-square bilinear Christoffel–Darboux kernel is nonzero at every P_(3p) root.

For p >= 5, there are exactly 2p roots of valuation alpha=(2p−1)/(2p), p−1 roots of valuation 1, and one simple root 0, using v(q−1)=1. The degree-2p factor is irreducible over Q_p(q), and v(Disc P_(3p))=3p(3p−2). The discriminant formula is asserted only for p >= 5. The p=3 proof is a separate exact cyclotomic argument.

The accepted third partial-block theorem and its independent review are dependencies only. Combining them with this boundary gives squarefreeness and the stated kernel guard for 0 <= b <= 3p with b < p^s. Nothing here proves a degree beyond 3p, unrestricted F020 closure, or any other all-A hypothesis. No prior theorem is counted as new work, and there is no historical-originality claim.

This acceptance binds to candidate report SHA-256 `90385545114303539d4c29e9cc6cde2383480d6ad94cad83899ecc4f1cab0762` and candidate manifest SHA-256 `df02f0cc8bc18de23b120a2b5f6b08dda89492c08467641d78e34026aadb8354`. All 26 candidate manifest entries, all 44 entries of the four accepted dependency manifests, all ten original/copy source bindings, and both prior acceptance bindings passed independent verification. Details are in INPUT_VERIFICATION.json.

## 1. Quantifiers and accepted input

For p >= 5, 3p < p^s is equivalent to s >= 2. For p=3 it is equivalent to s >= 3. The strict inequality matters: the p=3, s=2, degree-9 case is outside this result.

Put K=Q_p(q), t=q−1, v(t)=1, e=v(p)=p^(s−1)(p−1), and u_j=1−q^j. The shifted cyclotomic polynomial is Eisenstein, so v(K^×)=Z. Every edge below 3p is nonzero. For p >= 5 the two bridge edges satisfy

    v(u_p)=v(u_(2p))=p,
    u_p/t^p -> −1,  u_(2p)/t^p -> −2.

Every internal edge of each p-vertex block has valuation 1. Let h=(p−1)/2 and c=(−1)^(h+1). The accepted p-block theorem gives a monic odd block

    A_0(X)=X^p+lambda X+E(X),
    v(lambda)=p−1, lambda/t^(p−1) -> c,

where every coefficient of E has valuation at least p−1 and E has only odd powers >=3. This input was checked in the accepted third-block source and its cited p-block proof. It is not treated as a newly established theorem here.

Let A_1 and A_2 be the p-vertex blocks starting at p+1 and 2p+1. Shifting an internal edge by ip, i=1,2, changes it by −q^j(q^(ip)−1), of valuation p. The continuant is an integer polynomial in its edges, so each coefficient of A_i−A_0 has valuation at least p. All blocks have the same parity and leading coefficient. Thus the same p-block estimates and leading linear coefficient c hold for all three blocks.

## 2. Exact three-block identity

For vertices a through b, denote their continuant by C[a,b], with the empty block equal to 1. Define

    D=C[1,p−1],       E=C[p+2,2p],
    G=C[p+1,2p−1],    J=C[2p+2,3p],
    M=C[p+2,2p−1],
    R_1=DE,          R_2=GJ.

All four blocks D,E,G,J have degree p−1=2h; M has degree p−2=2h−1. Expanding across both bridges gives exactly

    P_(3p)=A_0 A_1 A_2
          −u_p R_1 A_2 −u_(2p) A_0 R_2
          +u_p u_(2p) D M J.                         (1)

The last sign is positive, and removal of both middle-block endpoint vertices gives M with exactly the indices above. The identity also follows by partitioning matchings according to whether each bridge is selected. It is not a shifted or altered polynomial family.

Matching expansion proves the coefficient bounds

    v([X^(2j)]R_i) >= p−1−j,                         (2)
    v([X^(2j+1)]DMJ) >= 3h−1−j.                     (3)

In (2), 0 <= j <= p−1; in (3), 0 <= j <= 3h−1. The product of the constant residuals in either R_i is the product of odd residues 1,3,...,p−2 and even residues 2,4,...,p−1. Therefore Wilson's theorem gives

    R_1(0)/t^(p−1) -> −1,
    R_2(0)/t^(p−1) -> −1.                           (4)

No cancellation is prohibited by the bounds; they are lower bounds from exact sums of matching products. Equation (4) establishes the needed exact leading constants.

## 3. The two scale reductions and all error costs

Choose rho in a finite extension such that rho^(2p)=t^(2p−1); then v(rho)=alpha=(2p−1)/(2p). All polynomial valuations in this review are coefficientwise. Since alpha>1/2 and alpha<1, the block estimates give

    A_i(rho Y)/rho^p -> Y^p,
    R_i(rho Y)/t^(p−1) -> −1.

The lower linear term of A_i lies above its leading term by (p−1)/(2p)>0, and every higher lower odd term has a larger gap. The nonconstant terms of R_i have gap at least 2alpha−1>0. In the double-bridge term, (3) gives valuation at least

    2p+3h−1+alpha.

This exceeds 3p alpha by (p−2)/2+alpha>0. Using rho^(2p)=t^(2p−1) in (1) therefore proves

    P_(3p)(rho Y)/rho^(3p) -> Y^(3p)−3Y^p.          (5)

At the smaller scale t, the same estimates give

    A_i(tY)/t^p -> Y^p+cY,
    R_i(tY)/t^(p−1) -> −1.

The triple product has valuation at least 3p, one above the target 3p−1. The double-bridge term has valuation at least 2p+3h, exceeding 3p−1 by h>0. Hence

    P_(3p)(tY)/t^(3p−1) -> −3(Y^p+cY).              (6)

All coefficients in both normalizations are integral. At p >= 5 the coefficients −3 and c are nonzero. In particular the coefficient of X is exactly of valuation 3p−2 with leading residue −3c, proving directly that 0 is a simple root.

The two reductions together give the exact lower Newton polygon of P_(3p)/X:

    (0,3p−2), (p−1,2p−1), (3p−1,0).

Its slopes are −1 and −alpha. Thus precisely p−1 nonzero roots have valuation 1 and precisely 2p have valuation alpha, initially counted with multiplicity. The residual in (5) is inseparable; no simple-root Hensel conclusion is drawn from (5).

## 4. Derivative separation, including the delicate joining derivative

At scale rho, differentiation of each p-block gives

    A_i'(rho Y)/t^(p−1) -> c.

Indeed the derivative of X^p has valuation e+(p−1)alpha>p−1; higher odd lower terms have valuation at least p−1+2alpha; and derivatives of shifted-block errors have coefficient valuation at least p. No characteristic-p differentiation is substituted for the characteristic-zero derivative.

The three differentiated full-block products in (1), divided by t^(3p−2), give 3cY^(2p). Differentiating the A factor in the two single-bridge terms gives respectively −c and −2c by (4). It remains to check differentiation of R_i and the double-bridge term.

From (2), R_i'(rho Y) has valuation at least p−2+alpha. Hence each product u_(ip) R_i'(rho Y) A_j(rho Y) has valuation at least

    2p−2+(p+1)alpha.

Its strict excess over 3p−2 is

    (p+1)alpha−p = (p−1)/(2p) > 0.                 (7)

From (3), the derivative of the double-bridge term has valuation at least 2p+3h−1. Its excess over 3p−2 is h>0. Integer factors introduced by differentiation can only improve these bounds. These are the complete potentially low-cost terms. Thus

    P_(3p)'(rho Y)/t^(3p−2) -> 3c(Y^(2p)−1).       (8)

For a root x of valuation alpha, Y=x/rho is a residue unit and (5) gives Y^(2p)=3 in the residue field. The right side of (8) is therefore 6c, nonzero for every p >= 5. All 2p roots counted in that Newton segment are distinct.

Equation (6) has derivative −3c, a unit. Its p distinct residual roots lift by Hensel; the zero residual root is the exact root 0, whose derivative was already shown nonzero. The other p−1 lifted roots have valuation 1 and are distinct from every alpha-root. Every pair of these p lifted roots, including 0, has difference valuation 1 because their scaled residues are distinct. Alternatively, differentiating the integral normalized polynomial in (6) gives P_(3p)'(tY)/t^(3p−2) -> −3c directly. The entire degree is now exhausted by distinct roots.

Every one of the 3p roots has derivative valuation 3p−2, including 0. Since P_(3p) is monic, the product-of-derivatives formula proves

    v(Disc P_(3p))=3p(3p−2), p >= 5.

The alpha-root set is Galois-stable, so its monic degree-2p factor is in K[X]. A proper monic factor of degree j would have nonzero constant valuation j(2p−1)/(2p), an integer. Since gcd(2p−1,2p)=1, this requires 2p|j, impossible for 0<j<2p. Thus that factor is irreducible. This uses the value group of K, not the fractional value group of the auxiliary extension.

## 5. Separate exact certificate for p=3

The reviewer independently rebuilt the actual integer recurrence through P_9 and obtained

    P_9(X;q)=X Q_4(X^2;q),

where Q_4 is monic quartic in its first variable. Let D(q)=Q_4(0;q), and Delta(q)=Disc_Y Q_4(Y;q). Both were independently recomputed from the recurrence, rather than read as candidate input. The exact degrees are 20 and 80.

The reviewer performed exact rational polynomial division and gcd calculations for each of D and Delta against both Phi_27 and Phi_81. All four remainders are nonzero and all four gcds have degree 0. The complete integer coefficient lists of the remainders are recorded in P3_CHECKS.json, which also records Q_4 and the exact factorizations of D and Delta. The candidate's full R14 and E52 vectors were compared against these independent polynomials and matched exactly. The nonzero E52 remainder modulo (2,Phi_27) was independently reproduced. An independent full degree-nine discriminant computation also gives Disc_X P_9=256 D^3 Delta^2 exactly.

For s >= 5, deg Phi_(3^s)=2*3^(s−1) >=162>80. Neither nonzero polynomial D nor Delta can then be divisible by the minimal polynomial Phi_(3^s). This covers every allowed s >=3, without an infinite numerical search or an extrapolation from s=3,4.

It follows that Q_4 has four distinct nonzero roots. In characteristic zero each has two distinct square roots, and roots from different Q_4 roots cannot coincide. Along with 0, these give nine distinct P_9 roots. D!=0 also proves 0 is simple. This certificate does not claim the p>=5 Newton polygon, root valuations, irreducibility conclusion, or discriminant formula at p=3.

## 6. Actual H transfer and original CD kernel

The exact Gaussian identity is

    H_n(v^2;q)=v^n P_n(v+v^(-1);q).

It was additionally reconstructed from the integer Gaussian recurrence at n=9,15,21 in the reviewer's exact checker. H_n(0)=1. All u_j reduce to zero, so P_n(X) reduces to X^n. Therefore P_n(2) and P_n(−2) are units in odd residue characteristic. At an H_n root choose v!=0 with v^2=z. The map v->v^2 is unramified in characteristic zero, and v->v+v^(-1) is unramified except at v=±1, whose values ±2 were just excluded. The prefactor v^n is a local unit. Root multiplicity is consequently preserved, proving squarefreeness of actual H_(3p).

Set w_k=product_(j=1)^k u_j, w_0=1. Every needed factor is nonzero because 3p<p^s. Consecutive P polynomials are coprime by downward recurrence. For

    F_n=P_n' P_(n−1)−P_n P_(n−1)',

the recurrence gives F_n=P_(n−1)^2+u_(n−1)F_(n−1), with F_1=1. Dividing and telescoping yields the original diagonal identity

    sum_(k=0)^(n−1) P_k(x)^2/w_k = F_n(x)/w_(n−1).

At a P_n root, this is P_n'(x)P_(n−1)(x)/w_(n−1), which is nonzero. The exact telescope was also checked at n=9,15,21. These are ordinary algebraic squares, with no Hermitian metric or positivity premise.

All conclusions are algebraic nonvanishing statements. An injective p-adic embedding proves them for the corresponding cyclotomic elements; primitive-root embeddings are Galois conjugate. Thus the result holds at every primitive complex root of the prescribed order, without interpreting p-adic inequalities as complex positivity.

## 7. Independent reproducibility and stopping limits

Three new reviewer programs were written from scratch and executed. No candidate checker, historical checker, or unknown imported code was run.

- `check_uniform.py`: at p=5,7,11,13,17,19,23, rebuilds the exact recurrence modulo p and T^(3p+2), checks the full triple-block identity, both scale reductions, both derivative reductions, parity, Newton vertices, the nonzero derivative values, and the stated discriminant exponent.
- `check_exact_identities.py`: rebuilds the exact integer bivariate recurrence at p=3,5,7 without modular reduction, and checks the triple-block identity, actual Gaussian H transformation, H constant, and derivative CD telescope at degrees 9,15,21.
- `check_p3.py`: independently constructs P_9 and Q_4, computes the exact quartic discriminant, checks all necessary cyclotomic remainders and gcds, verifies the degree bound covering all higher orders, and cross-checks the candidate factor vectors, mod-2 remainder, and full degree-nine discriminant identity.

The modular coefficient-cost controls retain full rigor as transcription checks: every tested target is below 3p, while e>=p(p−1)>3p for p>=5. Any coefficient discarded modulo p therefore has actual valuation strictly above every tested target. The omitted T powers also have degree above every target, even after X differentiation. Thus neither mixed-characteristic integer multiples nor truncated terms can hide a failed tested residual. The unlimited theorem is proved by Sections 1–6; the finite prime instances are not its basis.

Every independent control passed. These checks and the accepted dependency hashes are frozen with the review. No external or canonical write was performed. F020 remains open beyond this stated degree, F023 remains its alias, and priority 58 is unchanged.
