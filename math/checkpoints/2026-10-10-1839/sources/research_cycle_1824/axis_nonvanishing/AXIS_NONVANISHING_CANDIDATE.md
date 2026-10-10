# Generic axis nonvanishing from a zero-constant degeneration

10 October 2026. New standalone author derivation, pending independent review. The automatic reciprocal-coprime axis implication is not used. No accepted theorem or predecessor file is changed. This note proves a candidate sufficient range for all polynomial guards; a stronger bank theorem must not be treated as accepted before independent review.

## 1. Exact claim and the deliberately enlarged envelope

Let N be odd, let q be a primitive Nth root in characteristic zero, and set K=Q(q). Assume

    d≥4,  N≥8d−10,  m=N−d.

In particular m≥(N−1)/2. Let A_(N,m) be the whole-left Fourier recurrence matrix defined below, and let W=ker A_(N,m), viewed as polynomials of degree at most m.

**Candidate theorem.** There is a K-linear subspace U⊆W whose monic slice contains a nonempty K-defined polynomial open set of degree-m polynomials g with

    g(0)≠0,  g squarefree,  rank X_N(g)=N.

Here X_N is the original quotient-coordinate axis matrix. Thus generic full axis rank holds on U, and consequently its axis-rank open set is also nonempty on the monic slice of W. The same is true for the simultaneous legal-node and axis guards. No saturation assumption on A is needed.

The auxiliary space U is the annihilator of a deliberately larger and simpler envelope than the accepted constrained triple space. Put

    h=4^(−1) mod N,  e=2^(−1) mod N,
    rho=q^e,  C_k=q^(h k²),
    D(z)=∏_{j=2}^{d−1}(1−q^j z).

Every D(q^k), 0≤k≤m, is nonzero, since 2≤j+k≤N−1. Define E⊆K^(m+1) by

    E = { ((C_k P(rho^k)+R(q^k))/D(q^k))_(k=0)^m :
            deg P≤3d−7, deg R≤d−2 }.

P and R are unrestricted polynomials subject only to these degree bounds. Set

    U=E^⊥,  U_0={g∈U:g(0)=0}.

This is an ordinary coefficient-pairing annihilator, with no conjugation. The dimension bound is

    dim U≥(m+1)−[(3d−6)+(d−1)]=N−5d+8≥3d−2.

Because P=0,R=D gives the all-ones vector in E, every member of U vanishes at 1. This proves the forced root directly for this chosen subspace; it does not assert saturation or the same fixed divisor for every recurrence kernel.

### Why U⊆W

For clarity, the recurrence definitions and the only inherited envelope identity are recorded here. For signs epsilon,delta, write

    G_(epsilon,delta)(a,b)=[r+ell choose ell]_(q^(epsilon delta))

when r+ell≤N−1, and zero otherwise, where r=[epsilon a]_N and ell=[delta b]_N. Let f(a,b)=q^(h(a+b)²). For 1≤b≤(N−1)/2 put

    T_b=1/G_-+(N−b,b),
    v_b(j)=(f(j,b)−T_b G_-+(j,b))/G_++(j,b),
             1≤j≤N−b−1.

The rows of A_(N,m) are (v_b(a+k))_(k=0)^m for a,b≥1 and a+b≤d−1. All displayed denominators are nonzero.

The Gaussian product calculation in the accepted whole-left envelope gives, with s=a+b,

    D(q^k)v_b(a+k)
      =Q_b q^(h s²) C_k rho^(s k) F_(a,b)(q^k)
         −B_b R_(a,b)(q^k)F_(a,b)(q^k),

where

    Q_b=∏_{j=1}^b(1−q^j),
    B_b=T_b(−1)^b q^(b(b+1)/2),
    F_(a,b)(z)=D(z)/∏_{j=1}^b(1−q^(a+j)z),
    R_(a,b)(z)=∏_{j=1}^b(1−q^(a−j)z).

The quotient F is a polynomial of degree d−2−b. In the variable t=rho^k, q^k=t², so the chirp polynomial is a scalar multiple of

    t^s F_(a,b)(t²),

of degree s+2(d−2−b)=2d−4+a−b≤3d−7, since a+b≤d−1 and b≥1. The ordinary polynomial has degree d−2. Thus every actual recurrence row belongs to E. Taking annihilators proves U⊆W. This inclusion uses no equality-of-ranks assumption.

## 2. Shift facts and the exact counts

All sequence identities below are defined for integer k, although the known equality initially holds only on the actual columns. Let S be the forward shift. Since 2h=e modulo N,

    C_(k+1)=q^h rho^k C_k.

A factor S−lambda sends C_k P(rho^k) to C_k times the polynomial

    T_lambda P(t)=q^h t P(rho t)−lambda P(t).

Every nonzero P gains exactly one degree and a nonzero leading coefficient. Therefore any finite product of these factors is injective on polynomial P, and raises its degree by exactly the number of factors.

Write

    M=∏_{j=0}^{d−2}(S−q^j),
    L_x=∏_{j=0}^{d−2}(S−xq^j),  x≠0.

M annihilates R(q^k). L_x annihilates x^k D(q^k). M² annihilates both R(q^k) and kD(q^k).

An order-r forward operator applied to a known zero interval k=a,…,b gives a zero interval a,…,b−r. We always count both endpoints. At the present bound all intervals used below are nonempty.

## 3. No nonzero envelope vector is supported on {0,1,m}

Suppose v∈E is supported on {0,1,m}. Its scaled sequence

    B(k)=C_k P(rho^k)+R(q^k)

is zero for k=2,…,m−1. Apply M, of order d−1. The result is a pure chirp with polynomial degree at most

    (3d−7)+(d−1)=4d−8,

zero at k=2,…,m−d. This interval has N−2d−1 points. Since

    N≥8d−10≥6d−6,
    N−2d−1≥4d−7>4d−8,

and 4d−8<N, interpolation at distinct rho^k forces the transformed polynomial to vanish identically. Injectivity of all T_lambda gives P=0.

Then R(q^k) is zero at k=2,…,m−1, or m−2 distinct points. The bound gives m−2>d−2, so R=0. Consequently v=0.

Thus delta_0, delta_1, delta_m are linearly independent modulo E. In particular:

- U contains polynomials of full degree m and with nonzero constant;
- on U_0, the coefficient functionals c_1 and c_m are linearly independent;
- U_0 has a full-degree member, and t² is not a fixed divisor of U_0.

For the second assertion, a relation alpha c_1+beta c_m=0 on U_0 would put alpha delta_1+beta delta_m in U_0^⊥=E+span(delta_0), contradicting the support result unless alpha=beta=0.

## 4. The only nonzero fixed root of U_0 is 1

All arguments may be extended from K to its algebraic closure. Suppose x≠0 is a common root of U_0. Linear annihilator duality gives

    (x^k)_(k=0)^m ∈ E+span(delta_0).

Hence a scaled envelope B(k)=C_k P(rho^k)+R(q^k) agrees with x^k D(q^k) at k=1,…,m. Apply M L_x, of order 2d−2. The target and ordinary part are annihilated. The remaining pure chirp has degree at most 5d−9 and is zero at

    k=1,…,m−2d+2,

an interval of N−3d+2 points. The exact threshold is

    N−3d+2≥5d−8>5d−9  ⇔  N≥8d−10.

Also 5d−9<N. Distinct-node interpolation and the highest-degree argument give P=0.

Now R(q^k)=x^k D(q^k) for k=1,…,m. Their difference obeys the monic recurrence M L_x, of order at most 2d−2 and with nonzero constant coefficient. Since m≥2d−2, these consecutive zeros propagate forwards and backwards to every integer k. Comparison at k=0 and k=N, using D(1)≠0, gives x^N=1. Write x=q^s.

Every coefficient of D, in degrees 0,…,d−2, is nonzero. Indeed it is a nonzero power of q times a Gaussian coefficient [d−2 choose j]_q, and every numerator and denominator factor has exponent strictly between 0 and N.

The identity R(q^k)=q^(sk)D(q^k) for all k identifies R with z^s D(z) modulo z^N−1. Therefore the translate by s of the cyclic interval I={0,…,d−2} is contained in I. Both have the same size, so I+s=I. A proper nonempty cyclic interval has no nontrivial translation stabilizer: it has exactly one boundary position belonging to I whose successor does not belong to I. Hence s=0 and x=1.

The root 1 is already common because the all-ones vector belongs to E. There is no assertion here that a generic polynomial has no other roots; this statement concerns only roots fixed throughout the linear space.

## 5. The root 1 is not doubled, even after imposing g(0)=0

Suppose the derivative functional at 1, (k)_(k=0)^m, belonged to E+span(delta_0). Its scaled envelope would agree with kD(q^k) on k=1,…,m. Apply M², of order 2d−2. It annihilates both the target and the ordinary part. The same degree 5d−9 and the same N−3d+2 zero count as in Section 4 force P=0.

The identity R(q^k)=kD(q^k) holds for k=1,…,m. Its difference obeys M² and therefore propagates to every integer k. At k=0 it says R(1)=0; at k=N it says R(1)=ND(1), which is nonzero in characteristic zero. This is impossible.

Thus the derivative functional at 1 is not in E+span(delta_0). Some g∈U_0 has g'(1)≠0. Combining this with Sections 3 and 4 proves the exact fixed divisors

    gcd(U_0)=t(t−1),     gcd(U)=t−1,

up to nonzero scalars, over K and over its algebraic closure. For U, a fixed nonzero root must also be a fixed root of U_0; the constant functional exclusion removes 0, and the derivative exclusion makes the root 1 simple.

This replaces the unnecessarily stronger task of excluding derivative functionals at every point. Only the one forced nonzero base point needs its multiplicity checked.

## 6. A generic reciprocal-root lemma, with universal-polynomial proof

Let F be a characteristic-zero field and V⊆F[t] a linear space with gcd(V)=1 and maximum degree r≥1. Choose a basis f_1,…,f_s, and algebraically independent parameters Z_1,…,Z_s. Put

    F_univ(t)=Σ_i Z_i f_i(t),  H_univ(t)=t^r F_univ(1/t).

Then F_univ has degree r and nonzero constant in F(Z)[t]. Its constant is nonzero because gcd(V)=1 excludes a common factor t. Its leading coefficient is nonzero because r is the actual maximum degree. This accounts for both endpoints before reversal; specializations where the degree drops or the constant vanishes are excluded by polynomial open conditions.

**Irreducibility.** F_univ is irreducible in F[t,Z]. A factorization has total Z-degree 1, so one factor is independent of Z and is a polynomial p(t). This p divides every f_i, hence is constant by gcd(V)=1. Because F_univ has positive t-degree, its irreducibility also implies that it is primitive as a polynomial over F[Z]. Gauss's lemma makes it irreducible in F(Z)[t].

If gcd(F_univ,H_univ)≠1 in F(Z)[t], irreducibility and the equal degree r give

    H_univ=lambda(Z) F_univ.

Applying fixed-grade reversal twice yields lambda(Z)²=1, hence lambda=1 or −1. Comparing the independent parameter coefficients gives

    rev_r(f)=lambda f  for every f∈V.

Conversely, either such identity makes every generic member share all its roots with its reversal. Therefore:

**Generic reciprocal-root criterion.** Unless V is contained in one fixed eigenspace of rev_r with eigenvalue +1 or −1, the polynomial resultant Res_t(F_univ,H_univ) is nonzero. In particular, generic members of V are reciprocal-coprime.

No arbitrary pencil, dimension heuristic, or assumed irreducible exceptional component is used. The base divisor has been removed before applying the lemma.

Apply this to

    V={g/[t(t−1)]:g∈U_0},  r=m−2.

Section 5 gives gcd(V)=1. Section 3 gives maximum degree r and independent endpoint functionals: if g=t(t−1)f, then

    f(0)=−c_1(g),  coefficient_r(f)=c_m(g).

If all f satisfied rev_r(f)=lambda f, the endpoint identity would be

    c_m(g)+lambda c_1(g)=0  on U_0,

contradicting their independence. Thus the residual reciprocal resultant is a nonzero polynomial on V. Its nonzero open set meets the nonzero-leading open set and the nonzero-constant open set. Over the infinite field K, choose a K-point there and normalize its leading coefficient to 1. This produces a monic

    g_0=t(t−1)f∈U_0

with f(0)≠0 and gcd(f,rev_r f)=1. In particular f(1)≠0.

## 7. The zero-node specialization proves a full-rank minor

For any monic degree-m g, including g(0)=0, the quotient remainder vectors p_j of t^j are polynomial in the nonleading coefficients. The axis matrix uses p_[−a]_N with a nonnegative residue exponent, never an inverse of t. Thus X_N(g) and all its N-column minors are defined polynomially on the entire monic coefficient slice.

Its exact row-dependence space is

    D_N(g)={A:deg A≤N−1, g|A, g|J_N A, A(1)=0},
    J_N A=t^N A(1/t)+A(0)(1−t^N).

This coefficient identity does not require g(0)≠0 or squarefreeness.

At the g_0 from Section 6, every A∈D_N(g_0) has A(0)=0. Divisibility of J_N A=t^N A(1/t) by f implies rev_r(f)|A. Consequently

    t(t−1)f rev_r(f) | A.

The factors are coprime as needed: f has nonzero constant, and reciprocal coprimality excludes 1 and any overlap between f and its reversal. The divisor has degree 2m−2, and

    2m−2>N−1,

because the present hypothesis implies N>2d+1. Since deg A≤N−1, A=0. Thus rank X_N(g_0)=N.

This is a polynomial-minor test at an illegal zero-node specialization. It does not assign a bank to that zero node, nor apply the reviewed nonzero-constant inverse-remainder criterion outside its hypotheses.

## 8. All legal guards intersect on the same monic slice

Let

    U_1={g∈U:coefficient_m(g)=1}.

Section 3 makes this a nonempty K-affine linear space; in particular it is irreducible and its coordinate ring is an integral domain. The normalized g_0 lies in this exact same U_1. Section 7 therefore gives an N-column axis minor that is not the zero polynomial on U_1.

The constant guard is also nonzero on U_1. Both leading and constant functionals are nonzero on U, and their simultaneous nonzero open set is nonempty; normalizing by the leading coefficient gives the claim on U_1.

For the squarefree guard, divide the exact fixed divisor t−1 from U, obtaining a base-point-free linear space V_1. Its universal polynomial is irreducible over its parameter field by the argument in Section 6. In characteristic zero it is separable, so its discriminant is nonzero. The derivative-at-1 exclusion gives a nonzero evaluation-at-1 polynomial on V_1. Thus generically g=(t−1)h has h squarefree and h(1)≠0, so g is squarefree. Intersecting also with the leading open set and normalizing proves that the degree-m discriminant is nonzero on U_1.

The product of the axis minor, constant coefficient, and discriminant is now a nonzero polynomial on the same affine linear space U_1. The infinite-field polynomial avoidance principle supplies a K-point at which all three are nonzero. This proves the candidate theorem.

As U_1 is a subset of the monic recurrence slice W_1 and the three guards are nonzero at that point, the corresponding product is nonzero on W_1 as well. W_1 is itself a nonempty affine linear space. Hence the simultaneous legal/full-axis set is a nonempty polynomial open set on W_1. No component assumption about a nonlinear incidence or exceptional variety is involved.

## 9. Boundaries, consequence to review, and sources

The main result is the generic-axis theorem and the simultaneous-guard derivation above. It uses the corrected understanding that reciprocal-coprime residuals can still have corank one at legal points; it never infers full axis rank from reciprocal coprimality there. Instead it obtains a nonzero minor at a zero-constant degeneration and then moves back to the legal open set.

If the candidate proof is independently accepted, the unchanged whole-left interpolation and raw-bank recovery in the accepted sources apply to its good g. The arithmetic choice

    d=floor((N+10)/8),  odd N≥23,

satisfies d≥4 and N≥8d−10 and would give the corresponding count 2N−2floor((N+10)/8)+2. This is a consequence proposed for review, not a revision of the currently accepted 9N/5 result in this author package. No minimum, K-split attainment, efficient algorithm, FFT speedup, or historical-priority claim is made.

Sources read as inert mathematical text:

- research_cycle_1735/common_annihilator_barrier/WHOLE_LEFT_RANK_ENVELOPE.md: recurrence definitions, Gaussian envelope, row compatibility and raw-bank construction.
- research_cycle_1735/common_annihilator_barrier/STEP_ONE_LINEAR_BANK_THEOREM.md: step-one chirp shift and accepted 9N/5 baseline.
- research_cycle_1810/direct_axis_guard/DIRECT_AXIS_GUARD.md: corrected quotient-axis duality, counterexamples and simple-root removal.
- research_cycle_1819/axis_criterion_review/INDEPENDENT_REVIEW.md: independent acceptance of the corrected criterion and rejection of the shortcut.

No predecessor script was executed or imported. Fresh finite controls, if supplied with this note, are implementation checks only; none is used to extrapolate a uniform claim.
