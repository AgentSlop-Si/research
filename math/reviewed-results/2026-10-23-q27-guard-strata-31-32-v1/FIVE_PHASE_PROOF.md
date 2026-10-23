# Q27: double-pole cancellation for every original 3+2 five-phase family

23 October 2026. Candidate, complete author certificates and pending
independent review. No external publication action is part of this work.

## Scope and statement

Use exactly the original N=8 chart in `sources/CHART.json`, SHA-256
`5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98`.
All ordered cycles, seeds 42420/42520, Gaussian pairs, fourteen fixed tree
edges, six original inverse guards, unweighted three-Green stage sums and
order M=S_1 S_0 are preserved. Encoded coordinate 24t+e uses t=0,1 and local
edge e. Local edge 8b+j sends cycle[j-1] to cycle[j]; edges 0,...,6 have gain
one, and the seventeen edges 7,...,23 use their listed Gaussian gains.
Multiply exactly the five listed original gains by independent arbitrary
complex unit phases. All other gains are frozen.

The label set consists of every legal one-edge-per-active-branch placement
with all three branches active in one stage and exactly two branches active
in the opposite stage. Precisely:

* [7,a,b,c,d], with a in 8..15, b in 16..23, and (c,d) in
  {(31,e):e in 32..47} union {(e,f):e in 32..39,f in 40..47};
* [c,d,31,a,b], with a in 32..39, b in 40..47, and (c,d) in
  {(7,e):e in 8..23} union {(e,f):e in 8..15,f in 16..23}.

There are 2*8*8*(16+64)=10,240 distinct labels, each a five-dimensional
original phase family. The candidate theorem established by the complete
finite certificates below is that no such family contains an original
six-guard unit-phase point externally invertible-complex row/column
monomial-equivalent to F8. Arbitrary invertible diagonal rescalings and row
and column permutations are allowed.

This is not arbitrary five-phase motion or the full 34-phase fiber. It is
not covered by accepted triples, whole one-free-branch exclusions, the 256
original branch-zero 2+2 four-phase families, or the 2,176 distribution-3+1
four-phase families. Shared lower-dimensional specializations are not new
coordinate labels. No owner closure, priority change, construction,
complexity or historical novelty claim follows.

## 1. Original polynomial model and the first pole-stratum reduction

The definitions and proof in the bound four-phase predecessor
`sources/FOUR_PHASE_PROOF.md` apply without alteration to five independent
variables, one per active branch. They are restated here to make all
premises and the original-ideal link explicit.

For branch t,b, put d_tb=1-h_tb*m_tb, where h_tb is its nonzero original
norm-one holonomy and m_tb its active multiplier or 1. Set

  B_tb=sum_(k=0)^7 W_tb^k,
  D_t=product_b d_tb,
  A_t=sum_b B_tb product_(c!=b) d_tc,
  Delta=D_1 D_0, N=A_1 A_0, R=product_j x_j,
  Ntilde=R*conjugate(N)(x^-1), H=N entrywise-multiplied by Ntilde.

There is no transpose in Ntilde's definition. W_tb^8=h_tb*m_tb I proves
N=Delta M on the original inverse domain. N and Ntilde are multiaffine;
H has coordinate degree at most two. On the unit torus,
H=R*|Delta|^2*|M|^2. Fourier monomial equivalence therefore requires all 784
original 2-by-2 H minors P to vanish.

Let F be the product of the five active guards. The remaining original
sixth guard is a fixed nonzero constant. Set

  K_ij=H_ij-H_i0-H_0j+H_00 (1<=i,j<=7), E=K/F.

E is a polynomial and is multiaffine. For completeness, formal reciprocal
conjugation and norm-one gains give G+G^dagger=I, S_t+S_t^dagger=3I. With
c_t=-1/(h_t0*h_t1*h_t2), this clears to

  Ntilde=c_1 c_0 (3D_1 I-A_1^T)(3D_0 I-A_0^T).                         (1)

At a single active pole the cycle numerator factors B=u v^T with u_i v_i=1.
Formula (1) makes H have equal columns at a stage-0 pole and equal rows at
a stage-1 pole. Hence K vanishes modulo each of the five pairwise coprime
prime guards. Their product F divides K, including all intersecting poles.
Degree additivity proves E multiaffine. This is polynomial division, not
localization or removal of exceptional points.

Use the invertible affine guard coordinates y_j=1-h_j*x_j. If t is the
fully active stage, let J be the ideal of its three guard variables.
A_t lies in J^2, D_t in J^3, and the factor 3D_t I-A_t^T in J^2. Therefore
H and K lie in J^4. F contains the product of those three variables and a
nonzero polynomial independent of them. K=F E then gives E in J. Consequently
every 2-by-2 minor T of E lies in J^2. Its complete containing support is
all multiquadratic exponent vectors with full-stage total degree at least
two: 23*9=207 monomials. That bound alone does not give the desired rank.
The pilot rank205<207 was not treated as either an exclusion or a witness.

## 2. A second symbolic reduction on the opposite double-pole stratum

Let the partially active stage have two original moving guards f,g and
remaining fixed guard d!=0. Write its two active cycle numerators as
B_1(f), B_2(g), with pole residues

  U=B_1(0)=u v^T, V=B_2(0)=r s^T,
  u_i v_i=r_i s_i=1.

One exact choice is u=U[:,0], v^T=U[0,:], and similarly for V. The pole
substitutions x=h^-1 are frozen nonzero Gaussian rationals. Thus all u,v,r,s
and everything below are constants in the original coefficient ring.
The third branch, its weights, and its nonzero guard d remain original.

In the ideal I=(f,g), the leading terms of this stage are

  A=d(g U+f V) mod I^2,
  3D I_8-A^T=-d(g U^T+f V^T) mod I^2.                                (2)

Indeed D=d f g lies in I^2; no branch numerator has a hidden pole.
The coefficient f*g of H is determined by the cross products in (2).
For a partial stage 1 those cross products have fixed left vectors

  w=u entrywise-multiplied by s,
  z=r entrywise-multiplied by v,
  w_i z_i=1.

After double-centering they have fixed left vectors
alpha=(w_i-w_0)_(i=1)^7 and beta=(z_i-z_0)_(i=1)^7.
Thus, over the fraction field of the other stage variables only,

  E restricted to f=g=0 = alpha p^T + beta q^T                         (3)

for suitable seven-component p,q. A common frozen scalar and the other
stage's active-guard product are absorbed into p,q. For a partial stage 0,
the analogous assertion has alpha,beta as fixed right vectors; their order
may be reversed, which only changes every wedge by one common sign.

The fraction field in this derivation is not an admissibility assumption.
After multiplying by the square of the other stage's nonzero formal guard
product, the minor identities following from (3) are polynomial identities.
Since the polynomial ring is an integral domain, their polynomial
cross-differences themselves vanish. No guard is inverted in any equation
used for the certificate, and no pole component is discarded.

Index the 21 ordered row pairs and column pairs lexicographically. Let

  rho_(a,r)=alpha_a beta_r-alpha_r beta_a.

For a partial stage 1, (3) gives T_(a,r;b,c)=rho_(a,r)*phi_(b,c) after
restriction to f=g=0. Choose a reference pair q whose frozen rho_q is
nonzero, and define polynomial equations

  Q_(a,r;b,c)=rho_q T_(a,r;b,c)-rho_(a,r) T_(q;b,c).                    (4)

For a partial stage 0 use the identical construction on column pairs:

  Q_(a,r;b,c)=rho_q T_(a,r;b,c)-rho_(b,c) T_(a,r;q).                    (5)

Every Q is a constant linear combination of the original centered minors.
Each vanishes at f=g=0, so Q belongs to I. It also belongs to J^2 by section
1. The two groups of variables are disjoint. Therefore its entire support
is contained in

  S={e in {0,1,2}^5 : full-stage total degree >=2,
                           partial-stage total degree >=1}.            (6)

This support has exactly (27-4)*(9-1)=184 monomials. This is a
characteristic-zero theorem, not a modular support guess or an unexplained
rank205 dependency.

The reference is not an additional variable guard. Each label and
specialization records the 21 frozen rho values and its selected reference
pair. Its nonzero residue proves rho_q!=0 in Q(i). The computation must fail
rather than exclude points if all references vanish; no label is omitted
for this reason. Equations (4)-(5) multiply by rho_q and never divide by it.

## 3. Exact determinant and original-ideal certificate

For each label form the 441 Q coefficient rows, indexed as all lexicographic
row-pair/column-pair combinations, and all 184 columns in S. Each completed
certificate records 184 original rows with nonzero determinant residue.
Let C be that exact Gaussian-rational 184-by-184 coefficient matrix and
let d_C=det(C)!=0.

Choose j to be the fully active stage's branch-zero variable and k the first
partial-stage variable. For the first list of labels, j=0,k=3; for the
second, j=2,k=0. The monomial y_j^2*y_k belongs to S and is nonzero throughout
the original legal domain. If its column is ell, the exact adjugate gives

  d_C*y_j^2*y_k=sum_(r=0)^183 cofactor(C)_(r,ell) Q_(selected_row_r).      (7)

The complete coefficient support (6), rather than modular row-space
membership alone, is what makes this identity valid in characteristic zero.

For every centered E minor, Cauchy-Binet gives F^2*T as a fixed signed sum
of nine original H minors: use row pairs (0,a),(0,r),(a,r), column pairs
(0,b),(0,c),(b,c), and signs (+1,-1,+1) in each direction. Substitute this
identity into (4) or (5), then (7). The result is the exact ideal statement

  d_C*F^2*y_j^2*y_k belongs to the ideal of the original 784 H minors.    (8)

It retains every original zero-coordinate and pole component. All its
factors are nonzero on the original guarded unit torus, whereas Fourier
monomial equivalence forces the generators to vanish. This proves the
stated exclusion for every label whose certificate is completed and lifted.
Neither 1 in the Q ideal nor a full-fiber unit-ideal certificate is claimed.

## 4. Denominator ledger, specialization, and exhaustive obligations

The coefficient ring is exactly

  R0=Z[i,(a+ib)^(-1),(a-ib)^(-1) for all34 originalGaussian pairs].

Original gains, conjugates, holonomies, inverse holonomies, polynomial guard
quotients, guard-coordinate transforms, pole residues, alpha,beta,rho, and
Q coefficients all lie in R0. Guard division has constant coefficient one
and uses the recurrence q_e=p_e+h*q_(e-unit). The coordinate transform uses
only h^-1. Pole residues substitute x=h^-1. No variable guard, reference
rho, matrix entry or determinant is added to the denominator ledger.

The prime65537 is checked by trial division. The two roots256 and65281
square to -1, and every original inverted Gaussian factor has nonzero image.
They give coefficient-ring maps R0->F65537, not field embeddings Q(i)->F_p.
Conjugate coefficients are evaluated using the opposite root. A recorded
nonzero determinant proves the exact characteristic-zero determinant in (7)
is nonzero. Nothing is inferred from modular rootlessness.

`COEFFICIENT_SCHEMES.json` explicitly records both complete184-column
orders. `CERTIFICATES_COMPLETE.jsonl` has one record per label and embedding,
with exact coordinates, original row indices, reference pair and rho values,
nonzero determinant, column scheme and equation-matrix hash. The required
count is20,480 records for10,240 labels. Every row must have rank184 and a
nonzero determinant. Missing, duplicated, failed or partial runs do not
establish the complete theorem.

The newly authored driver constructs all paths and original polynomials,
checks full F*E multiply-back, checks the triple-stage support, constructs
rho from actual original branch pole residues, checks rank-one residue
factorization, forms (4) or (5), verifies every removed coefficient is zero,
and selects full-support determinants. Coefficients use exact integer
arithmetic modulo65537, with every intermediate bounded below signed64-bit
capacity. The original-model implementation was authored during this same
research session for the four-phase packet and is included as
`original_model.py`; no historical research program was executed.

## 5. Remaining scope

The structural cancellation theorem is reusable; the determinant obligation
is finite and specific to this pinned original chart. No constant-rank
claim over unspecified frozen charts or arbitrary edge placements is made.
If the complete certificates and independent review pass, the exact new
accepted delta is the10,240 distribution-3+2 five-phase labels. All previous
exclusions remain intact. Distribution3+3 six-phase motion and the original
full34-phase fiber remain unresolved. A failed rank test is not a legal
surviving witness, and none is claimed here.

## 6. Completed author controls

The exhaustive run completed all20,480 certificates in both embeddings,
with rank184 and nonzero determinant in every case. COMPLETE_VALIDATION.json
checks the exact counts, unique labels, identical label lists in both
embeddings, coefficient schemes, row counts, and nonzero reference weights.
EXACT_CONTROLS.json records two exact Gaussian-rational original-model
fixtures, all21 frozen rho weights for four structurally different placements
verified against their modular values, every original single pole, triple
pole and zero-coordinate retention, and negative controls for wrong rho,
wrong conjugation, duplicate equation rows and row-sign mutations. These
controls supplement, not replace, the characteristic-zero proof and complete
coefficient certificates. Independent acceptance is a separate obligation.
