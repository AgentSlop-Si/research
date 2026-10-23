# Q27: a reusable double-pole annihilator and one original six-phase exclusion

23 October 2026. Candidate, pending independent review. This packet makes no
GitHub, spreadsheet, owner-closure, FFT, complexity or novelty claim.

## 1. Exact statement and preserved original model

Use the original N=8 chart in `sources/CHART.json`, SHA-256
`5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98`.
All six ordered cycles, seeds 42420/42520, 34 original Gaussian gain pairs,
14 fixed tree edges, unweighted three-Green stage sums and product M=S_1 S_0
are preserved. Local edge 8b+j sends cycle[j-1] to cycle[j]; local edges
0,...,6 have gain one, and edges 7,...,23 have their listed gains
(a+ib)/(a-ib). An encoded coordinate is 24t+local edge.

Multiply precisely the six original gains at

  [7, 8, 16, 31, 32, 40]

by independent arbitrary complex unit phases x_0,...,x_5. All other gains
are frozen. These are one original legal free edge per branch in each stage.
There are exactly six original inverse guards, one for each active branch.
No free interstage diagonal, branch weights, nonunit gain, added guard or
entry nonvanishing condition is permitted.

**Candidate theorem.** This one six-dimensional original phase family has
no point on its original six-guard unit-phase domain externally
invertible-complex row/column monomial-equivalent to F8. All row and column
permutations and arbitrary invertible complex diagonal scalings are allowed.

This is one specific six-coordinate family, not all 4,096 one-edge-per-branch
six-phase placements. It is not a full 34-phase fiber result. Earlier
three-, four-, five-, and whole one-free-branch exclusions remain separate;
the present family can have all six multipliers move simultaneously. No
cardinality claim about disjoint images is made.

## 2. Original equations and the first support reduction

Work over K=Q(i). For each original branch let h_tb be its frozen norm-one
nonzero holonomy and y_j=1-h_tb*x_j its active guard. These six guard
coordinates are an invertible affine coordinate change over K. Put

  d_tb=y_j, B_tb=sum_(k=0)^7 W_tb^k,
  D_t=product_b d_tb,
  A_t=sum_b B_tb product_(c!=b) d_tc,
  F=D_1 D_0=product_(j=0)^5 y_j,
  N=A_1 A_0, R=product_(j=0)^5 x_j,
  Ntilde=R*conjugate(N)(x^-1), H=N entrywise-multiplied by Ntilde.

There is no transpose in Ntilde's definition. W_tb^8=h_tb*x_j I gives
N=F M on the original guarded domain. Paths of length at most seven contain
an edge at most once, other-branch guards have disjoint variables, and stages
have disjoint variables. Thus N and Ntilde are multiaffine and H has
coordinate degree at most two. On the unit torus H=R*|F|^2*|M|^2.
External Fourier monomial equivalence requires rank(H)<=1. Hence the
original 784 two-by-two H minors P must all vanish. Only necessity is used.

Let K_ij=H_ij-H_i0-H_0j+H_00, for 1<=i,j<=7. Every original active guard
divides K. The complete argument, also used in the bound earlier packets,
is as follows. Formal reciprocal-conjugate transpose gives
G+G^dagger=I and S_t+S_t^dagger=3I. For c_t=-1/(h_t0*h_t1*h_t2),

  Ntilde=c_1 c_0(3D_1 I-A_1^T)(3D_0 I-A_0^T).                         (1)

At any original single pole, its B has the quotient-ring factorization
u v^T with u_i v_i=1. Formula (1) makes H have identical columns at a stage-0
pole and identical rows at a stage-1 pole. Double-centering therefore
vanishes modulo every guard. The six factors 1-h_j*x_j are pairwise coprime
prime polynomials, so E=K/F is polynomial and degree additivity makes it
multiaffine. Pole intersections are retained; no guard is inverted in E.

Let J_t be the ideal of the three stage-t guard coordinates. A_t is in
J_t^2 and D_t in J_t^3, so H and K are in J_t^4. As F has stage-total-degree
three, E is in J_t for both stages. Every two-by-two E minor T is therefore
in J_0^2 and J_1^2. Its containing support has 23^2=529 monomials, consisting
of all exponents in {0,1,2}^6 with total degree at least two in each stage.
The 441 T equations alone cannot span this entire containing space, and
rank441<529 is not treated as an exclusion or a witness.

## 3. Fixed annihilators of all three double-pole directions

This is the reusable symbolic step. For either stage t and each of its
three unordered branch pairs (a,b), restrict to the corresponding two guards
f=g=0. Let z be the remaining stage guard. The active branch pole residues
are U=u v^T and V=r s^T, with u_i v_i=r_i s_i=1. They are frozen constants:
substitute the two relevant x=h^-1 into those two original branch numerators.
Their dependence is only on their own branch variables, not on z or the
other stage. To first order in (f,g),

  A_t=z(g U+f V) mod (f,g)^2,
  3D_t I-A_t^T=-z(g U^T+f V^T) mod (f,g)^2.                           (2)

The coefficient f*g of centered H follows from the two cross products in
(2). For stage 1 the fixed left vectors are

  alpha_i=u_i*s_i-u_0*s_0,
  beta_i=r_i*v_i-r_0*v_0, 1<=i<=7.

For stage 0 the same construction supplies fixed right vectors, possibly
in reversed order, which changes every wedge by one common sign. Let
rho_t^(a,b) be the 21-component vector

  rho_(i,j)=alpha_i*beta_j-alpha_j*beta_i, i<j.

Over the fraction field of the other variables, the E matrix restricted to
f=g=0 has these two fixed directions. The residual z factor is scalar and
does not affect them. Consequently T, viewed as a 21-by-21 polynomial matrix
of row-pair/column-pair minors, satisfies

  T|_(f=g=0)=rho_1^(a,b) * v^T      when t=1,
  T|_(f=g=0)=u * (rho_0^(a,b))^T    when t=0.                         (3)

No pole is removed by this fraction-field derivation. Multiplying the
cross-differences by the square of the nonzero formal guard product clears
the derivation; the cross-differences are already polynomials, and an
integral polynomial ring has no torsion by a nonzero polynomial. Hence the
resulting annihilation identities are polynomial identities on the entire
double-pole strata, including their intersections.

For each stage assemble its three direction vectors as columns of a
21-by-3 constant matrix R_t. Select three row indices I_t for which
V_t=(R_t)_(I_t,:) has nonzero determinant delta_t. Define an 18-by-21 matrix
L_t, with rows indexed by i outside I_t, by

  (L_t)_i = delta_t*e_i^T - (R_t)_(i,:)*adj(V_t)*E_(I_t),              (4)

where E_(I_t) selects the three reference coordinates. Then L_t R_t=0,
using adj(V_t)V_t=delta_t I. All entries are frozen Gaussian rationals in
the original coefficient ring. No delta_t is divided out. Its nonzero
specialized residue certifies a nonzero constant, not an extra phase guard.
The actual reference indices, determinants, direction matrices and L_t
entries are recorded in each META file.

Define the 18-by-18 polynomial matrix of equations

  Q=L_1 T L_0^T.                                                     (5)

Every Q entry is a constant linear combination of the original centered
minors. Formula (3) and L_t R_t=0 imply that every Q vanishes on each of the
three double-pole strata of each stage. In a three-variable polynomial ring,

  (y_a,y_b) intersection (y_a,y_c) intersection (y_b,y_c)
                   = (y_a*y_b, y_a*y_c, y_b*y_c).

Thus every monomial of Q contains at least two distinct guard variables
from each stage. Q is still coordinatewise of degree at most two. Its entire
support is contained in

  B={e in {0,1,2}^6 : at least two e_j>0 in each stage}.                (6)

A stage has 3*(2^2)+2^3=20 such exponent triples. Hence |B|=20^2=400,
with 18^2=324 equations. This support proof is in characteristic zero, not a
modular zero-pattern inference.

## 4. One degree of polynomial multipliers closes the single family

Take the 324 Q entries and their six single-guard multiples y_j Q, giving
2,268 original-ideal polynomial equations. Their complete containing support
is

  C=B union union_(j=0)^5 (B+unit_j).                                 (7)

There are 1,360 monomials. The 400 original monomials are supplemented by
those with exactly one coordinate equal to three. For each such coordinate,
the other two coordinates in its stage must not both be zero: eight choices.
The opposite stage has 20 choices. Therefore |C|=400+6*8*20=1360. Different
three-coordinate positions cannot overlap, and all columns are explicitly
listed in lexicographic order in META_256.json and META_65281.json.

Rows are ordered in seven blocks: first Q, then y_0 Q,...,y_5 Q. Within each
block, the 18-by-18 Q entries are in row-major order, with their retained
21-pair indices in ascending order. The two certificate files each record
1,360 selected original equation rows and a nonzero determinant residue.
Let C0 be the exact 1,360-by-1,360 Gaussian-rational coefficient matrix of
one such specified minor, and d_C=det(C0)!=0.

The monomial F=product_j y_j belongs to B and is column 420 in the recorded
zero-based column order. The ordinary adjugate identity gives

  d_C*F=sum_(r=0)^1359 cofactor(C0)_(r,420) P_r,                       (8)

where P_r is its selected Q or single-guard-multiple equation. This is a
fully specified exact characteristic-zero identity; it need not print
expanded 1,359-by-1,359 Gaussian-rational determinants.

For every centered E minor, Cauchy-Binet expresses F^2*T as a signed sum of
nine original H minors. Use the row pairs (0,a),(0,r),(a,r), column pairs
(0,b),(0,c),(b,c), and signs (+1,-1,+1) in each direction. Combining with
(5), the permitted monomial multiples, and (8) proves

  d_C*F^3 belongs to the ideal generated by the original 784 H minors. (9)

All original pole and zero-coordinate components remain in this identity.
On the original guarded unit torus d_C*F^3 is nonzero, whereas Fourier
monomial equivalence forces every original H minor to vanish. This proves
the stated single six-phase-family exclusion. It is not a unit-ideal claim.

## 5. Coefficient ring and verified nonzero determinant lifting

Use exactly

  R0=Z[i,(a+ib)^(-1),(a-ib)^(-1) for all 34 original Gaussian pairs].

Original gains, conjugates, h and h^-1 belong to R0. Guard division uses
constant coefficient one and the recurrence q_e=p_e+h*q_(e-unit). Guard
coordinates use h^-1. Pole residues substitute h^-1. All wedge directions,
reference determinants, adjugates, annihilators, equation coefficients and
single-guard multiples use only these coefficients and ring operations.
No variable, original guard, reference determinant or matrix entry is added
to the denominator ledger. Equation (8) multiplies by d_C; it does not
invert d_C in the original ideal.

The prime 65,537 is checked by trial division. Both 256 and 65,281 square to
-1, and all original inverted Gaussian factors have nonzero images. These
are coefficient-ring maps R0->F_65537, not field embeddings of Q(i).
Conjugation uses the opposite root. The recorded full-support determinants
are 56,867 for i->256 and 17,832 for i->65,281, both nonzero. Therefore the
specified characteristic-zero coefficient determinants are nonzero and the
adjugate identity is valid. No finite-field rootlessness or unexplained
modular row-space membership is used.

The newly authored Python builder constructs the original full 729-position
polynomial model, verifies full F*E multiply-back, checks all excluded
support positions, builds both constant annihilators from actual original
pole residues, checks their kernel identities, forms all Q coefficients and
all 2,268 multiplier rows, and records the complete support and matrix hash.
The exact C++ selector computes modular pivots without floating point,
records original selected rows and pivot columns, and accounts for the
pivot-column permutation sign. Its product reduction uses
2^16=-1 modulo 65,537: for z=a*b, (z mod 2^16)-floor(z/2^16), with one
nonnegative adjustment. Since 0<=a,b<=65,536, this is exact and fits int64.
All Python/NumPy integer dot-products are reduced before the next product;
the largest dot-product length is 21 and fits int64.

The original-model implementation was authored earlier in this same
23 October research session and is included. No historical research code
was imported or executed. Reproduction and independent controls are separate
from acceptance; the independent reviewer must reconstruct the original
model and replay the frozen selected minors without choosing replacements.

## 6. Exact delta and remaining gate

The candidate adds exactly one six-coordinate family, [7,8,16,31,32,40],
under the original six guards. The annihilator and support theorem is
reusable for other one-edge-per-branch configurations, but its nonzero
reference determinants and full 1,360-column coefficient rank are separate
obligations. No extrapolation to the other 4,095 six-phase placements is
made. The original full 34-phase fiber and any other unproved original
families remain open. No surviving legal Fourier witness is asserted.

## 7. Author controls

EXACT_CONTROLS.json records two exact Gaussian-rational original-model
fixtures, all 63 direction coefficients and all 378 annihilator coefficients
per stage checked against modular values, exact L_t R_t=0 and nonzero
reference determinants, all six original single poles, both triple-pole
strata, zero-coordinate retention, a deliberately corrupted annihilator
that violates the support condition, and duplicate-row/sign mutations of
the specified 1,360-square coefficient minor. These supplement, rather than
replace, the complete support theorem and independent review.
