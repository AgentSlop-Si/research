# An exact eight-bank construction for N=7

10 October 2026. Author certificate; independently accepted in the stated scope. This is an upper-bound construction only. It does not use or certify any proposed lower bound.

## Result and field scope

Let q be a primitive seventh root of unity and K=Q(q). Let L be the splitting field over K of the explicit cubic g below. Over L, the negative Fourier matrix F[k,t]=q^(−kt), 0≤k,t≤6, is a sum of eight legal signed magnetic banks, with orientation multiplicities

(n_++, n_-+, n_+-, n_--) = (3,1,1,3).

In particular this gives an eight-bank realization over the complex numbers. It is not asserted that the parameters lie in K itself. The cubic is separable, so [L:K]≤6. Every step below is exact in characteristic zero. No finite-field lift is assumed.

The construction counts whole phase-weighted banks in the accepted grammar. It makes no arithmetic-runtime, FFT speedup, or historical-priority claim. A minimum of eight would additionally require an independently accepted lower bound; that question is separate from this artifact.

## 1. Original grammar and the eight parameters

Use S e_i=e_(i+1 mod7), T e_i=q^i e_i, and W_(a,b)=S^a T^b. A bank is

R=(1/7) sum_(j=0)^6 w_j [I−alpha S^epsilon−beta q^(epsilon delta j)T^delta]^(-1),

with epsilon,delta∈{+1,−1} and Delta=1−alpha^7−beta^7≠0. All eight banks have beta=1.

Define

s2=(−8+35q+25q²+28q³+q⁴−17q⁵)/29,
s3=(−3−5q−16q²−4q³+4q⁴+19q⁵)/29,
g(t)=t³+s2 t−s3.

Let x1,x2,x3 be its three roots, in any order. The banks are

1–3: (++), alpha=x1,x2,x3;
4: (−+), alpha=1;
5: (+−), alpha=1;
6–8: (−−), alpha=x1,x2,x3.

The three cubic nodes are pairwise distinct and nonzero. Indeed s3≠0, and

disc(g)=(665859+635064q+863499q²+425987q³+275146q⁴−15036q⁵)/24389≠0.

Also g(1)=(24+40q+41q²+32q³−3q⁴−36q⁵)/29≠0, so no cubic node equals the singleton parameter 1. The displayed nonzero polynomials have degree less than six, so cannot vanish at q because Phi_7=1+q+⋯+q^6 is irreducible over Q. The same argument applies to each nonzero certificate below. The guards are −x_i^7 for each triple and −1 for each singleton, hence all are nonzero.

## 2. Why this cubic handles both isolated edge rows

Put

C=(1/7) sum_(j=0)^6 q^(−j²), H=q/(1+q), f(a,b)=q^(2(a+b)²),

where all exponents of q are read modulo seven. The desired Weyl coefficient is C f(a,b), and C≠0 by the usual Gauss-sum identity (also checked directly by the certificate).

At b=1, the delta=−1 banks contribute only to a=0. The singleton (−+) with alpha=1 has normalized amplitude H, forced by a=6. Define m0=1 and, for a=2,3,4,5,

G_a=(1−q^(a+1))/(1−q), B_a=(1−q^(a−1))/(1−q^(−1)),
m_(a−1)=q^(2(a+1)²)/(H G_a)−B_a/G_a.

All divided Gaussian factors are nonzero. The remaining nonaxis equations ask for three atomic weights A_i such that

sum_i A_i x_i^j=m_j, j=0,1,2,3,4,

with normalized bank amplitudes h_i=H A_i/x_i. Let

D=m2−m1²=1+4q−q²+3q⁴≠0.

For a depressed cubic, the required recurrence is

m3=−s2 m1+s3, m4=−s2 m2+s3 m1.

Solving these two equations gives

s2=(m1 m3−m4)/D, s3=m3+s2 m1,

which reduce exactly to the coefficients in section 1. Since the cubic roots are distinct, their 3×3 Vandermonde is invertible. The first three moments determine A_i uniquely; the two recurrence equations then give the last two moments. This proves all six nonaxis entries at b=1.

The normalized amplitudes' first three sums K_d=sum_i h_i x_i^d are particularly simple:

K0=H(m2+s2)/s3, K1=H, K2=H m1.

The formula for K0 follows from 1/x_i=(x_i²+s2)/s3. The singleton (−+) amplitude is H. Assign the singleton (+−), in its ell=6 sector, amplitude q²−K0−H, and assign zero to the three opposite-delta ell=6 amplitudes. This sets the axis a=0 too.

Simultaneous reflection (a,b)↦(−a,−b) preserves f(a,b). It exchanges ++ with −− and −+ with +− while preserving epsilon delta. Applying this exact reflection gives the complete b=6 row. No one-coordinate or Fourier-conjugation symmetry is assumed.

## 3. The other rows: explicit exact nonsingular solves

For 0≤r≤6, let (p_r0,p_r1,p_r2) be the coefficients of t^r modulo g(t). Thus

p_0=(1,0,0), p_1=(0,1,0), p_2=(0,0,1),
p_r=−s2 p_(r−2)+s3 p_(r−3), r≥3.

For a row b, order eight transformed unknowns as

z_b=(K_++0,K_++1,K_++2,h_-+,h_+-,K_--0,K_--1,K_--2).

For any orientation let r=[epsilon a]_7, ell=[delta b]_7. Put

G_(epsilon,delta)(a,b)=[r+ell choose ell]_(q^(epsilon delta)) if r+ell≤6, and zero otherwise.

The 7×8 matrix M_b has a-th row

( G_++ p_r0, G_++ p_r1, G_++ p_r2,
  G_-+, G_+-,
  G_-- p_u0, G_-- p_u1, G_-- p_u2 ),

where r=a and u=[−a]_7. Every occurrence of G uses its own orientation and hence its own r and ell. The singletons have alpha=1. This is exactly the bank coefficient matrix after replacing each triple by its three power moments.

For b=0,2,3 solve M_b z_b=f_b, with f_b[a]=f(a,b), as follows. Keep the indicated seven columns, set the omitted coordinate to zero, and invert that square submatrix. Columns are zero-based.

- b=0: columns (0,1,2,3,5,6,7).
- b=2: columns (0,1,2,3,4,5,6).
- b=3: columns (0,1,2,3,4,6,7).

Their exact determinants, in those column orders and increasing a row order, are

d0=−(370501134818472+889546502909192q+1166936870814012q²+994193630954024q³+501377982443436q⁴+58844381586428q⁵)/500246412961,

d2=(726−4387q−12368q²−16345q³−13989q⁴−6744q⁵)/841,

d3=1+3q+5q²+5q³+3q⁴+q⁵.

Each is nonzero by irreducibility of Phi_7. Thus these solves exist uniquely on their selected seven columns. All data and solutions lie in K.

Define the reflection permutation

J(z0,z1,z2,z3,z4,z5,z6,z7)=(z5,z6,z7,z4,z3,z0,z1,z2).

Set z4=J(z3) and z5=J(z2). For b=1 use the explicit vector

z1=(K0,H,H m1,H,q²−K0−H,0,0,0)

from section 2, and set z6=J(z1). This completely specifies all seven transformed amplitude vectors, using only exact field arithmetic and three declared 7×7 inversions.

Direct exact elimination independently verifies the full row ranks

rank(M_0),…,rank(M_6)=(7,5,7,7,7,7,5).

The deficient edge ranks do not cause an inconsistency: section 2 gives the needed target in their column spans, and all 49 normalized coefficient equations are checked exactly. The section gives a sufficient construction, not a classification of all eight-bank solutions or all singular strata.

## 4. Complete amplitudes and branch weights

For any transformed triple moments k0,k1,k2 define

A_(k0,k1,k2)(t)=[k2+t k1+(t²+s2)k0]/g'(t), with g'(t)=3t²+s2.

This is well defined at each root because the discriminant is nonzero. Lagrange interpolation gives

sum_i A_(k0,k1,k2)(x_i) x_i^d=k_d, d=0,1,2.

For row b, assign normalized amplitudes in sector ell=[delta b]_7 as follows:

- The three ++ banks: A_(z_b0,z_b1,z_b2)(x_i).
- The singleton −+: z_b3.
- The singleton +−: z_b4.
- The three −− banks: A_(z_b5,z_b6,z_b7)(x_i).

Because b↦[delta b]_7 is a permutation, this assigns every sector of every bank exactly once. The actual sector amplitude is C times the normalized amplitude h_(n,ell).

Finally define every original branch weight by

w_(n,j)=C Delta_n sum_(ell=0)^6 h_(n,ell) q^(−epsilon_n delta_n j ell), j=0,…,6.

There is no additional scaling: the original bank already includes 1/7. These equations are a complete exact algebraic specification of all eight parameters and all 56 branch weights. A permutation of the cubic roots only permutes banks with the same orientation.

[EXACT_WITNESS.json](../controls/upper/sources/EXACT_WITNESS.json) additionally records every transformed amplitude and the reduced degree≤2 sector polynomial in t for all four groups, with coefficients in the rational basis 1,q,…,q⁵. Evaluating its generic polynomial at x1,x2,x3 gives all three separate bank amplitudes. No numerical root selection or numerical linear solve occurs.

### Denominator and legality ledger

The construction divides only by nonzero quantities: 7 and 29; 1+q and 1−q^j for 1≤j≤6; D; s3; d0,d2,d3; and g'(x_i). The final branch guards are −x_i^7 and −1. Vandermonde denominators are nonzero because the roots are distinct. Every rational coefficient denominator in the literal certificate is a nonzero integer in characteristic zero. Intermediate elimination pivots are checked before inversion. The JSON also supplies checked inverses of t, −t^7, and g'(t) in K[t]/g.

## 5. Literal original-resolvent verification

The accepted exact certificate derives the moments from their displayed edge formulas, constructs the cubic and row matrices, solves the three square systems, applies the explicit edge/reflection recipe, and checks all 49 coefficient equations. The independent control separately checks every saved amplitude and extracts the target Weyl coefficients from the direct trace of the original Fourier matrix. [The independent verdict](02_upper_bound.md) and [exact controls](../controls/upper/README.md) give the reproducible public checks.

For a literal check that does not stop at the Weyl expansion, it uses the cubic algebra E=K[t]/g. Since g is separable, the trace of h(t) is the sum of its evaluations at the three distinct roots; explicitly,

Trace_E/K(a0+a1 t+a2 t²)=3a0−2s2 a2.

For every orientation group and every phase j, it constructs the actual 7×7 matrix

X=alpha S^epsilon+q^(epsilon delta j)T^delta,

with alpha=t for a triple and alpha=1 for a singleton. It computes X^7 and verifies X^7=(alpha^7+1)I. It then forms

Q^(-1)=(I+X+⋯+X^6)/(−alpha^7)

and checks both (I−X)Q^(-1)=I and Q^(-1)(I−X)=I. Evaluating a triple identity at any cubic root proves the corresponding literal branch identity. The 28 generic phase checks therefore cover all 56 individual resolvents: 42 in the two triples and 14 singletons.

After multiplying by the exact w_(n,j)/7, it sums the triples by this algebra trace and the singletons ordinarily. It checks equality to q^(−kt) in all 49 original matrix entries. Thus the construction is certified in the original inverse-matrix grammar, including every guard and every normalization.

The independently authored public verifier checks both its own exact construction and this frozen author witness in separate runs. See [reproduction instructions](../controls/upper/README.md). No author or predecessor research program is needed or included.

## 6. Bounded search and proof boundary

The modular probe tested the first small candidate y=1,s1=0 and immediately found suitable rank certificates at q=7 modulo29. That discovery observation is not the existence proof. The final proof uses the exact characteristic-zero cubic, exact nonzero determinant formulas, and exact original matrix arithmetic above.

In particular the reduced-basis s2,s3 formulas have denominator29; reducing those displayed fractions directly modulo29 would be invalid. One can instead reduce their original D-denominator expressions at the prime (29,q−7), where D has residue20, but no such reduction is needed or relied on in this final proof. No finite-field point is presumed to lift.

Source mathematics: the accepted signed magnetic-resolvent grammar, the earlier N=5 five-bank construction, and the isolated N=7 edge moments. This upper construction does not depend on the separate N=7 lower-bound proof. The frozen original note and witness hashes are recorded in [source acceptance](../SOURCE_ACCEPTANCE.json) and the [upper receipt](../receipts/upper_acceptance.json).
