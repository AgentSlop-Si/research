# Q27: 280 four-phase same-branch slices through the original N=8 witness

Candidate theorem, 19 October 2026. Independent review is required for acceptance.

## 1. New result and precise boundary

For either stage, either fully free branch, and any four of that branch's eight
edges, multiply the four original gains by x,y,z,w in ascending edge-index order.
Freeze every other gain at the original witness. On the original six-guard
unit-phase domain, no resulting matrix is externally invertible-complex
row/column monomial-equivalent to F8. This is exactly
2 stages × 2 branches × C(8,4) = 280 slices.

The source is the 3,138-byte CHART.json at commit
7769fb444edb0b63ebbce7e31dc52966ba08f4f0, Git blob
d0a7a859b27574b0fd327587ba9e831984a98714, SHA-256
5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98.
The pinned accepted three-coordinate proof and review are retained in sources/.
Their algorithms were not executed, imported, compiled, or evaluated.

Both seeds 42420/42520, all six ordered cycles, all 34 witness gains, fourteen
fixed unit tree gains, all six inverse guards, the three unweighted Green sums
in each stage, and product M=S2*S1 are preserved. No interstage diagonal or other
parameter is introduced. The four-coordinate result is new relative to the
pinned accepted triple theorem; that theorem is not rerun or relabeled.

The proposed dimension 146 support bound is true but is not attained. A new
two-cut lemma sharpens the upper space to dimension 126. Every one of the 280
coefficient matrices has characteristic-zero rank exactly 126. The resulting
ideal identities exclude all 280 labels. No failed rank 146 test is being treated
as a feasible Fourier witness.

The result does not settle the full 34-phase fiber, other four-coordinate
placements, five-or-more-coordinate motions, other witnesses, or any Fourier
algorithm, complexity, or novelty-priority claim. Q27 remains open at its current
priority; this packet requests no owner closure or registry mutation.

## 2. Original chart, polynomial numerators, and necessary equations

Let K=Q(i). For each original branch in stage s=0,1, let h_sb be the product of
its frozen edge gains. The gain of a free edge is (a+ib)/(a-ib) for its pinned
Gaussian pair. Every gain has norm one. Every h_sb is nonzero, has norm one,
and differs from one, as checked exactly in STRUCTURE_CHECKS.json.

For a selected label let R=xyzw and let b be its selected branch in stage s.
Write d_sb=1-h_sb R for the active branch and d_tc=1-h_tc for each inactive
branch. All six are the original inverse guards. Put

B_tc = I+W_tc+...+W_tc^7,
D_t = product_c d_tc,
A_t = sum_c B_tc product_(j!=c) d_tj,
Delta = D_1 D_0,  N=A_1 A_0=Delta M.

The edge convention is exactly that edge 8b+j sends cycle[j-1] to cycle[j].
The identity W_tc^8=(1-d_tc)I proves the displayed numerator formula. Every
path in B has length at most 7 and meets a selected edge at most once. Only one
branch moves. Thus N is coordinatewise affine in x,y,z,w. There is no division
by any guard in its construction. Delta=cF with F=1-hR and a fixed nonzero c
(the product of the other five guards).

Define Nt=R conjugate(N)(1/x,1/y,1/z,1/w), with coefficient conjugation and no
transpose. It is a polynomial. Let H=N entrywise-multiplied by Nt. For each
row pair a<r and column pair b<c, use the original polynomial

P_arbc = H_rc H_ab - H_rb H_ac.

There are C(8,2)^2=784 such polynomials. On the unit torus,

P_arbc = R^2 |Delta|^4
 ( |M_rc M_ab|^2 - |M_rb M_ac|^2 ).

An invertible complex left/right monomial transform of F8 has squared entry
moduli equal to positive row factors times positive column factors. Every
2-by-2 minor of its squared-modulus matrix is therefore zero, including after
row or column permutations. Hence all 784 P are necessary equations for the
requested equivalence. Their sufficiency is not assumed. No matrix entry,
anchor, or determinant of M is inverted or saturated away.

## 3. Exact divisibility and the proposed 146-dimensional support

The polynomial F=1-hxyzw is irreducible over K. Indeed its quotient makes every
variable a unit and is a Laurent polynomial ring in three variables. On F=0,
the active weighted cycle has holonomy one. Its eigenvalue 1 is simple, so
B=I+W+...+W^7 has rank one. The active stage numerator is the fixed nonzero
product of its two inactive guards times B. Thus N has rank at most one there.
Coefficient conjugation and reciprocal variables preserve the divisor because
conjugate(h)=h^(-1). Nt also has rank at most one there. Entrywise multiplication
of two matrices of rank at most one has rank at most one. All 784 P therefore
vanish on this irreducible divisor, and F divides each P in K[x,y,z,w].

Write P=FQ. Since each P has coordinate degree at most 4 and F has degree 1 in
each variable, each Q has coordinate degree at most 3. This is degree additivity
in each variable over an integral domain, without a generic-point exception.

For a stage let R_t be its selected-variable product (R or 1), and use formal
conjugate-reciprocal transpose, denoted dagger. Unit frozen gains give
W^dagger=W^(-1), hence G+G^dagger=I and S_t+S_t^dagger=3I. Also

R_t conjugate(D_t)(reciprocals)=c_t D_t,
c_t=-1/(h_t0 h_t1 h_t2).

It follows that

R_t conjugate(A_t)(reciprocals)=c_t(3D_t I-A_t^T),
Nt=c_1 c_0(3D_1 I-A_1^T)(3D_0 I-A_0^T).

These are first rational-function identities; both sides of each cleared
identity are polynomials, so they remain valid at zero coordinates.

One-cut lemma. Choose any two distinct selected edges with variables u,v and
set u=0. The active cycle becomes a directed path. Its coefficient of v in B
factors as U V^T, retaining both other variables as polynomial coefficients.
U is supported downstream of the v-edge and V upstream; these vertex sets are
disjoint. The active guard becomes 1, so D is independent of v and all other
branch terms in A are independent of v. The v coefficients of A and
3D I-A^T are opposite scalar multiples of U V^T and V U^T. If the active
stage is0, the v coefficients of N and Nt retain right factors V^T and U^T;
if it is1, they retain left factors U and V. Their entrywise product vanishes.
Thus H at u=0 has v-degree at most 1, and P at u=0 has v-degree at most 2.

Equivalently H has no exponent vector with one coordinate0 and another2.
In particular every H exponent has spread at most 1. Every P exponent then has
spread at most 2. Dividing by F preserves exponent differences: coefficientwise,

Q_e = P_e + h Q_(e-(1,1,1,1)),

with coefficients having a negative index defined as zero. Induction along this
diagonal proves that every Q exponent has spread at most 2. Therefore every Q
lies in the proposed space

V146 = span{x^e : e in {0,1,2,3}^4, max(e)-min(e)<=2}.

It is the union of the monomial cubes {0,1,2}^4 and {1,2,3}^4, with intersection
{1,2}^4, so its dimension is 2*3^4-2^4=146. This establishes the proposed bound
in characteristic zero for every original window and all 280 labels.

## 4. New two-cut lemma and the sharper 126-dimensional space

The variables x,y,z,w are in cyclic order along the selected branch. Define
cyclic total variation

TV(e)=|e_x-e_y|+|e_y-e_z|+|e_z-e_w|+|e_w-e_x|.

Claim: every monomial of every H entry has exponent e in {0,1,2}^4 with
spread at most 1 and TV(e)<=2. This is a 27-dimensional monomial space.

Proof. The spread bound is already proved by the one-cut lemma. Among the 31
exponents in {0,1,2}^4 having spread at most 1, the only ones with TV>2 are
(0,1,0,1),(1,0,1,0),(1,2,1,2),(2,1,2,1).

Set x=z=0. Cutting the cycle at these opposite selected edges creates two
disjoint directed path components. The y-edge lies in one and the w-edge in
the other. No surviving path can use both. Thus, over K[y,w], the active stage
numerator is A0+y a U_y V_y^T+w b U_w V_w^T, where a,b are fixed scalars and
U_y,V_y are supported on the component containing y, while U_w,V_w are
supported on the disjoint component containing w. (Fixed unselected gains are
absorbed into these factors.) D is constant. The reciprocal-transpose formula
therefore has the corresponding transposed coefficients with a minus sign.

There is no yw term in N or Nt. The coefficient of yw in H is the sum of the
entrywise products of their y and w coefficients. For active stage 0 these have
right-factor products V_y entrywise U_w and V_w entrywise U_y, both zero by
disjoint component support. For active stage 1 the corresponding left-factor
products U_y entrywise V_w and U_w entrywise V_y vanish. Hence H has no
(0,1,0,1) coefficient. Cutting y=w=0 proves the other lower alternating zero.

Finally H satisfies the exact reciprocal symmetry

H=R^2 conjugate(H)(1/x,1/y,1/z,1/w).

Therefore coefficient e is conjugate to coefficient (2,2,2,2)-e. The two upper
alternating coefficients vanish as well. This proves the claim. Counting gives
31-4=27. Equivalently these are a constant level 0 or 1 plus the incidence vector
of a cyclic interval of the four selected edges, with the shared all-ones
exponent counted once. QED.

Total variation is subadditive: TV(e+f)<=TV(e)+TV(f). Consequently every P,
being a difference of products of two H entries, is supported on exponents of
spread at most 2 and TV<=4. Both properties are invariant under subtracting
(1,1,1,1). The same coefficient recurrence for Q therefore proves the sharper
unprojected containment

Q in V126 = span{x^e : e in {0,1,2,3}^4,
                  max(e)-min(e)<=2 and TV(e)<=4}.

The count is 126. In {0,1,2}^4 precisely ten exponent vectors have TV>4: the two
alternating 0/2 vectors have variation 8, and the eight obtained by changing one
of their four coordinates to 1 have variation 6. Thus 71 of that cube's 81
monomials survive. The shifted cube {1,2,3}^4 has the same count. Their entire
intersection {1,2}^4 survives, so dim V126=2*71-16=126.

In particular 1 belongs to V126. The 20 excluded columns of V146 vanish by this
proof, not by modular testing. Thus a 146-by-146 coefficient minor cannot be
nonzero in characteristic zero. The successful 126-by-126 minors below give the
correct complete certificate rather than an unresolved rank 146 failure.

## 5. Complete fixed minors and a characteristic-zero ideal certificate

Both COVERAGE_PRIMARY.jsonl and COVERAGE_CONJUGATE.jsonl contain one certificate
per label, in the exact order: stage 0,1; branch 1,2; lexicographic four-subsets of
the branch's edge positions 0,...,7. A label records original edge indices8b+j,
encoded coordinates 24s+e, selected windows, selected coefficient columns, and
the determinant residue. All 280 records in each embedding have rank 126.

Rows are original windows indexed by 28 times the lexicographic row-pair index
plus the lexicographic column-pair index, pairs taken from combinations(0,...,7,2).
Column 64i+16j+4k+l means x^i y^j z^k w^l. Every record uses all 126 allowed
columns in natural increasing order. Rows are in their recorded order; the
determinant is for precisely that order. No projected polynomial equation is
asserted. The arithmetic reconstructs all 784 full original windows per label,
checks each full quotient, its cubic and 126 support, and multiplies FQ back in
all 625 coefficient positions including the possible outer-degree terms.

Use the ring

R0=Z[i,(a+ib)^(-1),(a-ib)^(-1) for all 34 pinned witness pairs].

All frozen gains, conjugate gains, holonomies and inverse holonomies lie in R0.
The constructions of N,Nt,H,P use only ring operations. The constant-term
recurrence Q_e=P_e+h Q_(e-ones) proves that each quotient coefficient belongs
to R0 as well. No guard is inverted to build these coefficients.

The prime is p=1,000,000,009. Complete trial division verifies primality.
The two embeddings send i to 569,522,298 and 430,477,711; both square to -1 mod p.
Every one of the 68 inverted Gaussian factors has nonzero image in both
embeddings. All six frozen holonomies and all six frozen guards also have
nonzero images. These exact checks are in STRUCTURE_CHECKS.json. Therefore each
modular construction is the image of the characteristic-zero construction under
a genuine homomorphism R0 -> F_p. Coefficient conjugation is implemented by
building the numerator in the opposite Gaussian embedding; it is not treated
as a finite-field absolute value or an automorphism fixing all residues.

For any label let C be its 126-by-126 exact coefficient matrix, using its selected
windows and all columns of V126. Its recorded nonzero determinant residue proves
d=det C is nonzero in R0 and in K. Therefore those selected Q span V126 over K.
Writing C_j0 for the cofactor of row j and the constant-monomial column 0 gives
the following exact, reconstructible polynomial identity in R0[x,y,z,w]:

d F = sum_(j=0)^125 C_j0 P_(selected window j).

Indeed the cofactor combination of the selected Q is the constant d. Every
cofactor is an explicit 125-by-125 determinant of the exactly specified rational
coefficient matrix, so this is a finite characteristic-zero ideal certificate,
not merely a rank heuristic. Since d is a nonzero scalar in K, F is in the ideal
generated by the original 784 P. The selected minor and this adjugate formula
specify the certificate without printing enormous expanded Gaussian rationals.

This is determinant lifting under a checked coefficient-ring homomorphism.
Finite-field rootlessness and modular Groebner-unit conclusions are not used.
All required coefficient zeros and support dimensions were proved above in
characteristic zero. No literal multiplier transport between equal-holonomy
slices is used: each original label has its own reconstructed minor.

## 6. Guards, saturation, and theorem

Let I be the ideal generated by the original 784 P for a label. The certificate
proves F in I, hence I:(xyzw F)^infinity=(1). Since the other five original
inverse guards are fixed nonzero constants, F!=0 is exactly the remaining
inverse-guard condition. Every unit phase also has xyzw!=0. Thus no point of
the guarded unit torus can satisfy all necessary modulus-window equations, and
therefore none can be externally invertible-complex monomial-equivalent to F8.

Variable-zero components were retained in every polynomial identity; zeros
were also deliberately used in the proof's cuts. Pole components were retained
in the original P and removed only by their original inverse guards. No extra
diagonal, anchor, nonzero-entry condition, or unintended feasibility hypothesis
was introduced. All 280 exact labels are covered.

## 7. Fresh execution, finite costs, and review boundary

The programs make_chart_header.py, certify_four.cpp, and verify_structure.py were
written for this attempt. They read the pinned chart as data. No historical
research executable was run, imported, compiled, or evaluated. No external
writes were made by this candidate.

Reproduce from this directory:

python -I -S make_chart_header.py
g++ -O3 -std=c++17 certify_four.cpp -o certify_four
./certify_four > COVERAGE_PRIMARY.jsonl 2> COVERAGE_PRIMARY.log
./certify_four 430477711 > COVERAGE_CONJUGATE.jsonl 2> COVERAGE_CONJUGATE.log
python -I -S verify_structure.py > STRUCTURE_CHECKS.log

The two complete certificate runs contain 560 label/embedding instances,
1,120 independently built Gaussian-embedding numerators,439,040 full original
window quotient/multiply-back checks, and 560 specified nonzero minors of
order 126. Per window there are 81^2 convolution positions for each of the two
products,256 quotient coefficient positions, and 625 full multiply-back
positions. This is a finite arithmetic-cost statement, not a speedup claim.
The exact loop counts are retained in STRUCTURE_CHECKS.json.

Early pilots found rank 126 in the 146 template and confirmed the 20 missing
columns; those observations motivated the two-cut proof but do not replace it.
PILOT.jsonl/PILOT.log are exploratory diagnostics, excluded from the theorem's
required certificate set. The complete final runs use the proved 126 template.

Independent review should check the two-cut support argument, cyclic order,
the characteristic-zero ring homomorphism, exact coverage, and all fixed minors
using a separately authored reconstruction of the original six Green inverses.
The candidate does not certify its own independent acceptance.
