# Q27: a guard-stratum certificate for every original 3+1 four-phase family

23 October 2026. Candidate; independent review is required. No novelty, FFT
construction, full-fiber exclusion, owner closure, or publication claim is made.

## Exact original model and new scope

The inert original chart is `sources/CHART.json`, SHA-256
`5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98`.
It is byte-identical to the chart in the accepted cross-stage packet
`bundled predecessor source copies in four_phase/candidate/sources`, whose
published namespace is `math/reviewed-results/2026-10-22-q27-cross-stage-branch-zero-v1`.
The independent accepted review is in that packet's `review` directory.
The earlier chart binding is commit `3834be7716370cfddf84ab1200da62b7887feb05`,
path `math/finalized/2026-10-19-q27-four-phase-same-branch/candidate/sources/CHART.json`.

All six ordered cycles, seeds 42420/42520, 34 original Gaussian pairs, 14 fixed
tree edges, unweighted three-Green stage sums, and order M=S_1 S_0 are kept.
Local edge 8b+j sends cycle[j-1] to cycle[j]. Edges 0,...,6 have gain 1;
edges 7,...,23 have their listed (a+ib)/(a-ib). An encoded coordinate is
24t+e, with t in {0,1}. In every selected coordinate, multiply the original
gain by an independent arbitrary complex unit x_j; freeze every other gain.
The six original inverse conditions are precisely 1-(branch holonomy) != 0.
No branch weights, free interstage diagonal, extra guard or entry assumption
is introduced.

The new family is all 2,176 original four-coordinate placements with exactly
one moving edge in each of the three branches of one stage, and exactly one
moving edge in the opposite stage:

* [7,a,b,c], 8<=a<=15, 16<=b<=23, 31<=c<=47;
* [c,31,a,b], 7<=c<=23, 32<=a<=39, 40<=b<=47.

There are 2*8*8*17=2176 labels. They are distinct. Each is a four-dimensional
phase family, including its lower-dimensional fixed-phase specializations.

**Theorem.** None of these 2,176 families contains a point in its original
six-guard unit-phase domain externally invertible-complex row/column
monomial-equivalent to F8. Arbitrary row/column permutations and arbitrary
invertible diagonal scalings are allowed.

This is the complete original one-edge-per-active-branch distribution 3+1,
not arbitrary four-coordinate motion. It is disjoint in coordinate labels
from the accepted 256 distribution-2+2 families [7,e0,31,24+e1], and is not
contained in the accepted triples or four whole one-free-branch families.
The 128 labels where the opposite moving edge is branch zero are included,
but are not the whole new result. The original full 34-phase fiber remains
open, as do other unsupported multi-coordinate families.

## 1. A reusable symbolic theorem before any enumeration

Work first over K=Q(i). The following argument applies to any two-stage sum
of three weighted eight-cycle Green functions, with norm-one nonzero frozen
gains, one independent multiplier on each active branch, frozen
holonomies different from 1, and at least one frozen branch whenever a stage is not fully
active. The final determinant ranks below are a separate finite obligation
for the pinned chart, not a consequence of these structural assumptions.

Let h_tb be the original frozen branch holonomy, m_tb its one multiplier
if active and 1 otherwise, and define

  d_tb=1-h_tb*m_tb; B_tb=I+W_tb+...+W_tb^7;
  D_t=product_b d_tb;
  A_t=sum_b B_tb product_(c!=b) d_tc;
  Delta=D_1 D_0; N=A_1 A_0.

Since W_tb^8=h_tb*m_tb I, N=Delta M on the original six-guard domain.
Every N entry is coordinatewise affine, because paths of length at most 7
use each edge at most once, other-branch guards have disjoint variables,
and the stages have disjoint variables. Put R=product_j x_j and

  Ntilde=R*conjugate(N)(x_0^-1,...,x_(n-1)^-1);
  H=N entrywise-multiplied by Ntilde.

No transpose appears in this definition. Both are polynomials; H has
coordinate degree at most 2. On the unit torus,
H=R*|Delta|^2*|M|^2 entrywise. Monomial equivalence to F8 requires rank(H)<=1,
because |M|^2 is an outer product of positive row and column factors.
Thus all 784 original 2-by-2 H minors P must vanish. Only necessity is used.

Let F be the product of the active original guards. Frozen guards are
nonzero constants, so Delta=cF with c!=0. Define the double-centered matrix

  K_ij=H_ij-H_i0-H_0j+H_00, 1<=i,j<=7.

Then every entry of K is divisible by every active guard and hence by F.
Here is the complete division-free justification, including pole intersections.
With dagger meaning coefficient conjugation, reciprocal variables and
transpose, norm-one edge gains give W^dagger=W^-1 and G+G^dagger=I.
Consequently S_t+S_t^dagger=3I. If R_t is the product of stage t's variables
and c_t=-1/(h_t0*h_t1*h_t2), clearing the formal rational identities gives

  R_t conjugate(D_t)(x^-1)=c_t D_t;
  R_t conjugate(A_t)(x^-1)=c_t(3D_t I-A_t^T);
  Ntilde=c_1 c_0 (3D_1 I-A_1^T)(3D_0 I-A_0^T).

These are polynomial identities, including zero-coordinate points.
Modulo an active guard, the corresponding cycle has holonomy one and its
B is u v^T with u_j v_j=1. This factorization is polynomial in the quotient
ring: take u=B[:,0], v^T=B[0,:], use (I-W)B=0 and diagonal B_jj=1.
For a stage-0 pole A_0=kappa*u v^T. Substitution into the displayed formulas
makes H have identical columns because v_j u_j=1. At a stage-1 pole H has
identical rows. Thus K vanishes modulo every active guard. This remains true
when kappa, another guard product, is zero. No intersecting pole is removed.
The active factors 1-h_j*x_j are pairwise coprime prime polynomials.
Therefore E=K/F is a polynomial 7-by-7 matrix. Degree additivity shows that
E is coordinatewise affine. Rank(H)<=1 implies rank(K)<=1, and on F!=0
therefore rank(E)<=1.

Now use guard coordinates y_j=1-h_j*x_j. This is an invertible affine change
of polynomial coordinates over K, not a restriction of the phase domain.
Suppose all three branches of stage t move. Let J_t be the ideal generated
by its three y variables. In these coordinates A_t belongs to J_t^2 and
D_t belongs to J_t^3, directly from their defining sums/products. The factor
3D_t I-A_t^T also belongs to J_t^2. Therefore every entry of H, and hence K,
belongs to J_t^4. But F is the product of these three variables times active
guards from the other stage. Those other guards have degree zero in J_t.
The identity K=F E and the monomial nature of J_t give E in J_t: multiplying
by the three distinct stage variables shifts every stage-total-degree by
exactly 3, and multiplication by the nonzero other-stage polynomial cannot
annihilate a coefficient. This argument does not invert any guard.

Every 2-by-2 minor T of E therefore belongs to J_t^2. Its coordinate degree
is at most 2. Hence its entire support is contained in

  S={e in {0,1,2}^n : sum_(j in stage t) e_j >=2
                          for every fully active stage t}.             (1)

This is a characteristic-zero support theorem, not a modular zero-pattern
inference. For the distribution 3+1, |S|=(27-4)*3=69: the excluded triple
exponents are (0,0,0),(1,0,0),(0,1,0),(0,0,1).
The same reusable theorem gives the containing support sizes 207 for 3+2
and 529 for 3+3; no rank or exclusion for those families follows here.

## 2. Original-ideal certificate, not a unit-ideal assertion

Let the 441 T rows be all 2-by-2 minors of E. Row order is the lexicographic
product of the 21 pairs of indices 0,...,6 in each direction (these are
original H indices increased by one). Columns are the lexicographic S in
(1), in the variable order of the encoded-coordinate label.

For a label choose j to be the branch-zero variable of the fully moving
stage: j=0 in the first label list and j=1 in the second. The monomial y_j^2
belongs to S, and this original guard is nonzero everywhere in the legal
domain. Let k be its column. A specified nonsingular 69-by-69 coefficient
matrix C, consisting of 69 recorded T rows and every column of S, gives

  d*y_j^2 = sum_(r=0)^68 cofactor(C)_(r,k) T_(selected_row_r),
  where d=det(C)!=0.                                                  (2)

Every cofactor is an exact Gaussian-rational determinant. This is a finite,
reconstructible exact characteristic-zero certificate without expanding huge
rational coefficients. It does NOT claim 1 belongs to the T ideal. In fact
all T vanish on the common triple-pole stratum, so such a claim would be false.

There is a division-free bridge to the original 784 equations. For an E
minor indexed by original rows a<r and columns b<c in {1,...,7}, take row
pairs (0,a),(0,r),(a,r), column pairs (0,b),(0,c),(b,c), and signs +1,-1,+1.
Cauchy-Binet, or direct expansion, gives

  F^2 T_(a,r,b,c) = sum_(u,v=0)^2 sign_u sign_v
                                    P_(row_pair_u,column_pair_v).       (3)

Combining (2) and (3) proves d*F^2*y_j^2 belongs to the ideal generated by
the original 784 H minors. All original pole and zero-coordinate components
remain in this identity. On the original guarded unit torus the left side
is nonzero while Fourier monomial equivalence forces every P=0: contradiction.

## 3. Denominator ledger and the finite coefficient-rank obligation

Use the coefficient ring

  R0=Z[i,(a+ib)^(-1),(a-ib)^(-1) for all 34 original Gaussian pairs].

Original gains, conjugate gains, holonomies and inverse holonomies all lie
in R0. The path numerators and H,K use ring operations. Each division by
1-h*x_j uses constant coefficient 1 and the exact recurrence
q_e=p_e+h*q_(e-unit_j); therefore the polynomial quotient coefficients stay
in R0. The affine guard change x_j=(1-y_j)/h_j uses only h_j^-1 in R0.
Thus E and every T coefficient lie in R0. No variable, branch guard, entry,
anchor, matrix determinant, or extra denominator is inverted in constructing
the equations. The adjugate certificate multiplies by d, rather than
adjoining its inverse to the original ideal.

The prime p=65537 is checked by trial division. Sending i to 256 or 65281
sends i^2+1 to zero. Every one of the 68 inverted Gaussian factors is checked
nonzero in both specializations; every h and every fixed guard is also
checked nonzero. These are coefficient-ring homomorphisms R0 -> F_p, not
embeddings of Q(i) into a finite field. Conjugation uses the opposite root.
All calculations use exact integer modular arithmetic with no floating point.

`CERTIFICATES_COMPLETE_PRIMARY.json` and `CERTIFICATES_COMPLETE_CONJUGATE.json`
record all 2,176 labels, all 69 columns, selected original rows, pivot columns,
nonzero determinant residue, chart holonomies and equation-matrix hash.
Every rank is 69. A nonzero specialized determinant proves that the exact
Gaussian-rational determinant d of that specified C is nonzero. Because
all characteristic-zero coefficient support is included, (2) then follows
by the ordinary adjugate identity. A specialized root count, fitted support,
or modular row-space membership of an unproved smaller support would not
justify this conclusion and is not used.

## 4. Computation, controls and exact delta

`guard_strata.py` was newly authored on 23 October. It builds every original
weighted path numerator from the inert chart; forms the opposite-embedding
reciprocal numerator; computes all 81 H coefficients; performs full exact
guard division and full multiply-back; changes to guard coordinates; checks
all excluded coefficients; constructs all 441 original centered minors; and
selects/reports full-support nonzero determinants. It imports no historical
research code. Maximum matrix dot-product accumulation is 8*(65536)^2,
and all other vector products are reduced after at most two such products;
all fit signed 64-bit integers.

The computational obligation is explicitly finite and chart-specific:
2,176 labels in each of two coefficient-ring specializations. The symbolic
support and ideal-bridge theorem is reusable and separate. No claim that the
rank is constant in an unspecified chart, or across untested coordinate
placements, is made.

Proposed accepted delta: all 2,176 distribution-3+1 original four-phase
families are excluded under the original six guards. This adds to, not
replaces, the earlier 5,984 triples, four whole one-free-branch families,
and 256 distribution-2+2 branch-zero families. Intersections with earlier
families at fixed-phase specializations do not change this coordinate-label
delta. Q27 remains open and retains its existing priority/status. This is
not a five-phase or six-phase exclusion and not evidence of a surviving legal
Fourier witness in those cases.

Author controls in `EXACT_CONTROLS.json` independently use exact Gaussian
rational arithmetic at two legal original-model points and check all six
cycle/inverse-numerator identities, both cleared reciprocity identities per
stage, N=Delta M, and the original modulus relation. Modular controls retain
zero-coordinate algebra, test every single pole and the common triple pole,
reject wrong conjugation, reject fixed-tree/duplicate/same-branch labels, and
detect duplicate-row and sign mutations of a recorded determinant. These
controls supplement, rather than replace, the symbolic proof and complete
finite rank certificates.
