# Independent verdict on the N7 mirrored six bank obstruction

10 October 2026

## Verdict

**Accepted in characteristic zero:** six signed magnetic banks with orientation multiplicities `(n_++, n_-+, n_+-, n_--) = (2,1,1,2)` cannot realize the negative Fourier matrix of length seven. The conclusion holds with arbitrary legal parameters and phase weights, in every characteristic-zero extension field containing a primitive seventh root q. A fresh derivation reproduces the complete edge-row parameterization and the exact nonzero axis obstruction.

The independently computed axis multiplication determinant is **14 modulo 29**, at the valid specialization q=7. Verified good reduction turns that nonvanishing certificate into a characteristic-zero obstruction. This is stronger than an isolated finite-field failure.

**Inherited, not newly established here:** the accepted N7 row certificate already gives at least three banks on each delta side, hence at least six in total. The present result does not increase the general lower bound to seven. No six-bank realization, exact N7 minimum, runtime improvement, or historical-priority claim is established.

A separate elementary transpose symmetry also excludes `(1,2,2,1)`. The other two six-bank multiplicity patterns, `(2,1,2,1)` and `(1,2,1,2)`, are interchanged by the same symmetry and are not tested here.

## Reviewed source and independence

The accepted author note has SHA-256 `7d6b742bd6289fd099f3f713204725d5a54b496262733996920c8edb4a2809b8`. Its [public transcription](01_n7_mirrored_pattern.md) updates acceptance status and navigation while preserving the mathematical argument. [Proof status](../PROOF_STATUS.json) binds the accepted source identities.

The review uses the mathematical definitions and literal coefficient data. It does not execute, import, compile, or parse author or predecessor research code. Both controls in this package were written independently:

- `verify_reduction.py` derives the moments from Gaussian coefficients, checks exact identities over Q(q), produces explicit Bezout certificates for all guard gcds, and checks the signed resolvent formula as a polynomial identity in literal 7-by-7 matrices.
- `verify_axis_norm.py` derives the specialized moments directly, expands the augmented determinant by complementary 3-by-3 minors, constructs the full 81-by-81 multiplication matrix, computes its determinant, and provides an explicit inverse of the axis element.

The latter determinant expansion differs from the author's subset recurrence. All 81 axis coefficients and all 6,561 multiplication-matrix entries agree exactly with the frozen source. SymPy is used for exact field and univariate polynomial arithmetic; the complementary-minor expansion and modular matrix elimination are explicit in the independent control.

The inherited lower-bound attribution was verified against the accepted baseline proof record, SHA-256 `ef38042e02ff4771cb396f3b3b61d2bc29fe9f24676b5660306f2a44729c7ffc`, section “N7 symbolic control and still-open small scope.” This source is evidence for the inherited bound, not a new theorem in this checkpoint.

## The model and the exact coefficient checks

Let S e_i=e_(i+1), T e_i=q^i e_i, with indices modulo seven and q a primitive seventh root. Write W_(a,b)=S^a T^b. A legal bank has orientation (epsilon,delta), parameters alpha,beta, guard Delta=1-alpha^7-beta^7 nonzero, and value

    (1/7) sum_(j=0)^6 w_j
      (I-alpha S^epsilon-beta q^(epsilon delta j) T^delta)^(-1).

Its Weyl coefficient formula is

    sum_(ell=0)^6 h_ell sum_(r=0)^(6-ell)
      alpha^r [r+ell choose ell]_(q^(epsilon delta))
      W_(epsilon r,delta ell).

Allowing every h_ell to be independent enlarges the legal class, so impossibility in this class is sufficient for an exclusion with arbitrary beta and weights.

For the negative Fourier matrix F[k,t]=q^(-kt), the trace formula gives

    c(a,b) = (1/7) sum_t q^(-bt-(t+a)t)
           = C q^(2(a+b)^2),
    C = (1/7) sum_t q^(-t^2) != 0.

The independent control verifies all 49 trace coefficients. It also verifies the Gaussian expansion of every power 0 through 6 of alpha S^epsilon+beta T^delta as a polynomial identity, for all four orientations. The seventh power is `(alpha^7+beta^7)I`. Hence the finite geometric sum multiplied on either side by the original resolvent denominator equals `Delta I`. These checks retain symbolic alpha and beta; they are not numerical parameter samples.

Normalize the amplitudes by C from now on, so the target is f(a,b)=q^(2(a+b)^2).

## The edge reduction with all degenerate cases covered

On b=1, let the three positive-delta banks be (++ with x), (++ with z), and (-+ with y). The other delta side contributes only at a=0. At a=6, the singleton endpoint forces

    H=q/(1+q),    h_y=H/y,

so y is nonzero. For a=1,...,5 set

    G_a=[a+1]_q=(1-q^(a+1))/(1-q),
    B_a=[8-a]_(q^-1)=(1-q^(a-1))/(1-q^-1).

All G_a are nonzero. Put m_0=1 and

    m_(a-1)=q^(2(a+1)^2)/(H G_a) - (B_a/G_a)y^(6-a).

The bracket in the backward factor is **8-a**, not a-1. The frozen author's corrected note and literal coefficients use the right factor.

With A=h_x x/H and B=h_z z/H, the remaining edge equations are precisely

    A+B=1,    A x^j+B z^j=m_j,    j=1,2,3,4.

These are necessary even when x or z is initially zero. Their exact moments are

    m1=-1-q-q^4-q^5-(q^2+q^5)y^4,
    m2=1+q+q^3+q^4-(1+q^3+q^4)y^3,
    m3=-q^2-(1+q^2+q^3+q^4+q^5)y^2,
    m4=-q^2-q^3-(q^2+q^3+q^4+q^5)y.

Define

    D=m2-m1^2,
    Sn=m3-m1 m2,
    Pn=m1 m3-m2^2,
    R=D m4-Sn m3+Pn m2,
    E=Sn^2-4 Pn D.

R is the 3-by-3 Hankel determinant of m0,...,m4. Every two-node sequence satisfies R=0. The independent exact computation gives

    deg(D,Sn,Pn,R,E)=(8,7,6,9,14),
    gcd(R,y)=gcd(R,D)=gcd(R,Pn)=gcd(R,E)=1.

It also finds gcd(R,R')=1. Explicit polynomial multipliers proving each gcd equals one are saved in [the explicit Bezout certificates](../controls/n7/GUARD_BEZOUT_CERTIFICATES.json) and checked by multiplication. Thus R has exactly nine distinct roots over an algebraic closure.

At every root y of R, D is nonzero and Cramer's equations give uniquely

    S=Sn/D=x+z,    P=Pn/D=xz.

The identities `D m2=Sn m1-Pn` and `D m3=Sn m2-Pn m1` hold identically. The final recurrence is exactly R/D=0. The guard gcds imply P nonzero and S^2-4P nonzero. Consequently the nodes x,z are distinct and nonzero at every edge candidate; no zero-node or coincident-node stratum has been silently discarded.

Conversely, take a root y and the two roots x,z of t^2-S t+P. Set

    A=(z-m1)/(z-x),    B=(m1-x)/(z-x),
    h_x=H A/x,    h_z=H B/z,    h_y=H/y.

The second-order recurrence recovers m0,...,m4, proving all six nonaxis edge coefficients. This is a complete edge-row parameterization over an algebraic closure, without a full-matrix existence claim.

## A precise remaining row sufficiency lemma

This lemma records the logical boundary between solving the two edges and solving the full original matrix. Although correct, its conditions are inconsistent for the mirrored pattern by the axis obstruction below.

Take roots y,v of R. Choose x,z with sum S(y), product P(y), and u,w with sum S(v), product P(v). Order the six banks as

    (++ x), (++ z), (-+ y), (+- v), (-- u), (-- w).

For b=0,...,6, define a 7-by-6 matrix M_b. The column for a bank (epsilon,delta,alpha), at row a, is

    alpha^r [r+ell choose ell]_(q^(epsilon delta))  if r+ell<=6,
    0                                                    otherwise,
    r=[epsilon a]_7,    ell=[delta b]_7.

Let f_b have entries q^(2(a+b)^2), a=0,...,6. There exists a legal full representation using these alphas and beta=1 in every bank if and only if

    rank(M_b)=rank([M_b | f_b])    for b=0,2,3,4,5.

Proof: the two edge constructions solve the six nonaxis entries for b=1,6. In each of those rows, an opposite-delta ell=6 amplitude affects only a=0 and can set its axis entry. For every bank the map b -> [delta b]_7 is a bijection; different rows therefore use different amplitudes and do not interfere. The five displayed rank conditions are exactly the remaining linear consistency conditions. All alphas are nonzero, so beta=1 gives Delta=-alpha^7 nonzero. If normalized amplitudes h_(n,ell) solve the rows, raw legal phase weights are

    w_(n,j)=C Delta_n sum_(ell=0)^6
               h_(n,ell) q^(-epsilon_n delta_n j ell).

Exact seven-point orthogonality and the checked resolvent formula reproduce the original Fourier matrix. Necessity follows by taking its Weyl coefficients. If M_b has column rank six, its single 7-by-7 augmented determinant being zero is equivalent to consistency; without that rank assumption determinant zero alone is only necessary.

No sufficient-condition claim in this review treats an augmented determinant zero as sufficient on a rank-deficient stratum.

## The actual axis obstruction

Simultaneous reflection (a,b)->(-a,-b) preserves f and turns the negative edge into the same construction. Work in the finite algebra

    B=K[Y,V]/(R(Y),R(V)),    K=Q(q).

After making R monic, B has dimension 81. Both D(Y) and D(V) are units.

Define U0=1,U1=0,J0=0,J1=1 and use the recurrence with coefficients S,P for U_a,J_a through a=6. For either quadratic root t, t^a=U_a+t J_a. Distinctness of the two roots makes this an invertible change of the duplicate-column basis.

The augmented b=0 matrix therefore has row a

    [ U_a(Y), J_a(Y), Y^r, V^a, U_r(V), J_r(V), q^(2a^2) ],
    r=[-a]_7.

The reverse exponent at a=0 is zero, not seven. Let its determinant be A in B. A full representation would require A(y,v)=0.

At the prime p=29 and q=7, the independent control verifies that q has order seven. The unnormalized leading coefficient of R reduces to 8, and its monic reduction is

    T^9+23T^8+2T^7+5T^6+27T^4+21T^3+12T^2+25T+21.

All scalar divisions used in deriving the moments have nonzero denominators. The inverse of D modulo the monic reduction is, in increasing powers of T,

    [4,4,2,11,9,1,13,13,16].

The independent complementary-minor expansion obtains the same 81 coordinates for A as the author. In the basis indexed by 9i+j for Y^i V^j, its multiplication matrix agrees entry by entry with the frozen author matrix. Its determinant is 14 modulo 29. An explicit 81-coordinate inverse of A is also recorded and checked by multiplication.

For completeness, use the local ring O=(Z[q])_(29,q-7). The monic R has coefficients in O. The quotient O[Y,V]/(R(Y),R(V)) is free of rank 81. The determinant of multiplication by D has nonzero residue, so it is a unit of O; the adjugate supplies the required quotient inverse of D over O. Thus A and its multiplication matrix are defined over this finite free O-algebra. The determinant reduces to 14, and hence is nonzero in K. Therefore A is a unit of B. Every evaluation homomorphism at simultaneous roots of R sends a unit to a nonzero value. This contradicts A(y,v)=0 and proves the characteristic-zero exclusion.

This establishes a nonvanishing algebraic certificate. It does not infer a characteristic-zero result from a finite-field parameter scan.

## The transpose corollary and remaining scope

For a literal bank denominator, S^T=S^-1 and T^T=T. Transposition sends orientation (epsilon,delta) to (-epsilon,delta), and reindexing j to -j changes the phase to the required new convention. Alpha, beta, and Delta are unchanged. Since F^T=F, existence is invariant under this operation. The independent control verifies the literal polynomial matrix identity for all 28 signed phase branches.

It follows that `(1,2,2,1)` is excluded as well. The accepted r_+,r_- bounds and support condition leave the two same-epsilon duplication patterns `(2,1,2,1)` and `(1,2,1,2)`, which transpose into each other. This review has not searched them or decided their feasibility. The general minimum is still only known here to be at least six.

## Reproduction and receipt

The [independent controls and reproduction instructions](../controls/n7/README.md) require Python 3 and SymPy. Run them in a disposable writable copy of that directory to preserve this frozen checkpoint. Each program resolves its companion files relative to its own location and compares only literal JSON data with the frozen certificates.

The [edge results](../controls/n7/EXACT_CONTROL_RESULTS.json) and [axis results](../controls/n7/INDEPENDENT_AXIS_NORM_RESULTS.json) state their exact scopes. [Proof status](../PROOF_STATUS.json) records the reviewed source hashes and accepted conclusions. No remote files were modified in preparing this checkpoint.
