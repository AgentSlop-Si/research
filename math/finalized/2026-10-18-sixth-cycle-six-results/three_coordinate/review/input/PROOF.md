# Q27: exclusion of all remaining 5,744 three-coordinate slices

Candidate theorem, 18 October 2026. Independent review is required before acceptance.

## 1. Exact scope and source

Keep the byte-pinned original N=8 chart in `sources/CHART.json`, SHA-256
5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98.
Its seeds are 42420 and 42520; all six cycles, 34 witness phases, fourteen fixed
unit tree gains, six inverse guards, unweighted three-Green stage sums, and
M=S2 S1 are unchanged. There is no interstage diagonal. The source review is
`sources/FROZEN_REVIEW.md`, Git blob 0fb2b065b626d756850e0d5e9a2028b43bc06449
in AgentSlop-Si/research. Prior prose is context only; no historical executable
was run, imported, compiled, or evaluated.

Coordinates are (s,e), s=0,1 in the certificate (stages 1,2 in prose), e=7,...,23.
The encoded label is 24s+e. Each selected gain is its original witness gain times
one of x,y,z, in ascending encoded-label order. All other gains stay fixed.

From all C(34,3)=5,984 labels remove exactly the 240 accepted labels:
- same stage (7,a,b), 8<=a<=15, 16<=b<=23: 128;
- same stage (a,b,c), 8<=a<b<c<=15: 112.

The remaining families are disjoint and exhaustive:
- three in branch 2 of one stage: 112;
- same stage, two in one branch and one in another: 1,008;
- mixed stages, the two-coordinate stage uses one branch: 1,904;
- mixed stages, the two-coordinate stage uses two branches: 2,720.

The certificate enumerates all 5,744 labels and excludes Fourier equivalence on
each guarded unit-phase slice. It does not rerun or strengthen the accepted 240
proofs. In conjunction with that inherited acceptance it covers all 5,984 labels.
It does not cover four or more moving phases, other frozen witnesses, or the full
34-phase fiber.

## 2. Exact numerator and all-window necessary modulus ideal

Work over K=Q(i). For each original branch b in stage s let h_sb be its frozen
holonomy and let m_sb be the product of the moving variables on that branch.
The exact guard is d_sb=1-h_sb m_sb. Write

B_sb = I+W_sb+...+W_sb^7,    D_s = product_b d_sb,
A_s = sum_b B_sb product_{c != b} d_sc,
Delta=D_2 D_1,              N=A_2 A_1=Delta M.

Each path uses each selected edge at most once. Branch variables are disjoint,
as are stage variables, so every entry of N has coordinate degree at most one.
This formula retains all six guards, including constant guards, without division
by any guard. All frozen h are nonzero norm-one Gaussian rationals and h!=1;
`STRUCTURE_CHECKS.json` records exact values. Thus Delta=cF for a nonzero scalar c,
where F is the product of the active guard factors.

Let R=xyz and define Nt=R conjugate(N)(1/x,1/y,1/z), coefficientwise conjugation.
For every pair of distinct rows a<r and columns b<c use the polynomial

P_arbc = N_rc N_ab Nt_rc Nt_ab - N_rb N_ac Nt_rb Nt_ac.

There are 28*28=784 windows. These are the 2-by-2 minors of N entrywise-multiplied
by Nt. On the unit torus,

P_arbc = R^2 |Delta|^4
  ( |M_rc M_ab|^2 - |M_rb M_ac|^2 ).

Invertible complex row/column monomial equivalence to F8 implies all 784 defects
vanish: squared entry moduli factor into positive row and column factors, and
permutations preserve the rank-one property. This is a necessary condition, not
an asserted characterization of Fourier equivalence. No entry or anchor is
inverted, and zero-entry components are not discarded.

At any active pole d_sb=0, B_sb has rank one, because a weighted cycle with
holonomy one has a simple eigenvalue 1. The cleared stage numerator, and hence N,
has rank at most one there. The reciprocal-conjugate involution preserves this
pole up to a nonzero Laurent monomial, so Nt likewise has rank at most one.
Therefore every P is divisible by each active guard. These binomials are
irreducible, use disjoint nonempty variable sets, and are pairwise relatively
prime. Hence P=FQ over K[x,y,z]. Each variable occurs in exactly one active factor,
so each Q has coordinate degree at most three.

## 3. The new cut-edge support lemma

Suppose x and y affect different edges of the same original cycle. Then every Q
has zero coefficient whenever its x exponent is zero and its y exponent is three,
and likewise with x and y exchanged. This holds for arbitrary placement of the
third variable and in either stage.

Proof. For a stage with variable product R_s and denominator D_s, formal unitary
weighted-cycle algebra gives S_s+S_s^dagger=3I, where dagger is transpose followed
by coefficient conjugation and reciprocal variables. For every branch,

m_sb conjugate(d_sb)(reciprocal variables)=-h_sb^(-1)d_sb,

including m_sb=1 for fixed branches. Therefore, for the nonzero scalar
c_s=-1/(h_s0 h_s1 h_s2),

R_s conjugate(A_s)(reciprocal variables)=c_s(3D_s I-A_s^T).

Consequently

Nt=c_2 c_1 (3D_2 I-A_2^T)(3D_1 I-A_1^T).

Set x=0. The active cycle is cut into a directed path. The coefficient of y in
its path numerator B is U V^T, up to the fixed nonzero gain of the y edge: a path
using that edge factors into the path before it and the path after it. U is
supported strictly on the downstream component after the y edge, and V on the
upstream component before it. These two vertex sets are disjoint. This remains
true when the remaining variable occurs on the cycle. Thus U entrywise-multiplied
by V is identically zero.

At x=0 the holonomy guard of that cycle is 1, hence D_s is independent of y.
All other branch terms in A_s are independent of y. The y coefficient of A_s is
a scalar polynomial times U V^T, and that of 3D_s I-A_s^T is the opposite scalar
times V U^T. If s=1, the y coefficients of N and Nt have right factors V^T and U^T;
if s=2, they have left factors U and V. In either case their entrywise product is
zero. Thus N entrywise-multiplied by Nt has y degree at most one after x=0, and
every P has y degree at most two there. F at x=0 is a nonzero polynomial independent
of y. From P=FQ in this integral domain, Q at x=0 has y degree at most two.
This proves the coefficient statement; exchange x,y for its counterpart. QED.

No phase, holonomy, edge, stage, or multiplier is transported between labels.
The lemma gives a universal support bound; every label still has its own
reconstructed coefficient matrix and its own nonzero minor.

## 4. Four exact coefficient spaces

The names x,y,z below may be permuted for the placement under discussion. A
permutation of variable coordinates changes no dimension or target membership.

### A. Three edges in the same branch: dimension 46

Apply the cut-edge lemma to all three pairs. Every Q is in

V_46=span{x^i y^j z^k: 0<=i,j,k<=3, max(i,j,k)-min(i,j,k)<=2}.

There are 46 monomials. In particular 1 belongs to this space. A rank-46
coefficient minor proves the 784 Q span V_46, so 1 is their K-linear combination.
Thus F belongs to the ideal I generated by the original 784 P.

### B. Mixed stages; two edges in the same branch: dimension 56

Name the pair x,y and the other-stage variable z. The cut-edge lemma gives

V_56=span{x^i y^j z^k: 0<=i,j,k<=3, |i-j|<=2}.

There are 56 monomials. Again 1 belongs to V_56. A rank-56 minor proves F in I.

### C. Same stage; two edges in one branch, one in another: dimension 41

Name the pair x,y, the singleton z. Set f=1-hxy, g=1-kz, F=fg and J=(f,g).
At their simultaneous pole each term of the affected cleared stage numerator
lies in J, so N and Nt are entrywise in J. Every P is therefore in J^4.
After P=fgQ, Q belongs to J^2. This colon statement can be seen in the Laurent
ring K[x,x^(-1),t,z] under t=xy, where f,g are independent affine coordinates:
(J^4:fg)=J^2. The injection from K[x,y,z] is sufficient for the constraints below;
no root or zero-variable component is removed in the eventual polynomial identity.

The cut-edge lemma also gives Q in V_56. To count its intersection with J^2,
group monomials by delta=i-j, delta=-2,-1,0,1,2. Substitution y=t/x makes each
block x^delta times a fixed power of t times a polynomial of t degree at most
3-|delta| and z degree at most 3. The fixed t power is invertible at t=1/h.
Membership in J^2 imposes the value and two first derivatives at
(t,z)=(1/h,1/k): exactly three independent conditions on each block. Independence
follows already from the polynomials 1,t,z, since 3-|delta|>=1.

The five unconstrained block dimensions are 8,12,16,12,8. Subtracting 3 from
each gives dimension 41. Denote the resulting exact K-space W_41. The target
F=fg lies in W_41. A rank-41 minor therefore proves F is a K-linear combination
of the Q, hence F^2 belongs to I.

### D. Mixed stages; two different branches in one stage: dimension 52

Name the two same-stage variables x,y; put u=x-1/h, v=y-1/k. The third variable
z belongs to the other stage. The affected stage numerator is entrywise in
J=(u,v). The reciprocal formula gives the same statement for its reversed
conjugate. Hence N,Nt are entrywise in J and P is in J^4.

F is a nonzero scalar times uv(1-lz). The factor 1-lz is coprime to J and is a
non-zero-divisor modulo J^n; in these independent coordinates the monomial
calculation gives (J^4:uv(1-lz))=J^2. Thus Q is in J^2.

Intersecting J^2 with coordinatewise cubics gives dimension
64-3*4=52: in shifted coordinates, omit the three (u,v) monomials 1,u,v,
for each of the four z powers. Call this W_52. F is in W_52. A rank-52 minor
therefore proves F^2 belongs to I.

## 5. Exhaustive minors and characteristic-zero transfer

`COVERAGE_PRIMARY.jsonl` contains one reconstructible certificate per remaining
label. Each gives its family, required rank, selected window indices, selected
coefficient columns, and nonzero determinant residue. Windows are indexed by
lexicographically ordered row pairs followed by lexicographically ordered column
pairs, each from combinations(range(8),2): index=28*row_pair+column_pair.
Coefficient column index is 16i+4j+k for monomial x^i y^j z^k.
The selected columns are in recorded order; determinant is in that order.

The primary field is F_p with p=1,000,000,009 and i mapped to 569,522,298.
Primality is checked by complete trial division, and the square root is verified.
Use the coefficient ring

R_0=Z[i,(a+ib)^(-1),(a-ib)^(-1) for all 34 witness pairs].

Every original gain, conjugate gain, holonomy and inverse holonomy lies in R_0.
The path numerator, stage numerator, product, and reversal use only ring
operations. Each active-guard division uses its unit leading coefficient -h,
so Q also has coefficients in R_0. No guard or matrix entry is inverted.
The exact source check verifies all inverted Gaussian integers have nonzero
images in both embeddings; all frozen holonomies and fixed guards are nonzero
as well. Hence the modular construction is the image of the exact
characteristic-zero construction under a genuine ring homomorphism.

A recorded nonzero determinant residue implies that particular exact determinant
is nonzero. Together with the proved upper-space containment and dimension, it
proves equality of the span with V_46, V_56, W_41, or W_52. This is a determinant
lift, not an inference from modular rootlessness or a modular Groebner unit ideal.
No modular zero is used to assert an exact support identity: the support and
Taylor identities were proved above. The second embedding provides redundancy.

The fresh C++ program explicitly reconstructs every path and every quotient. Its
polynomial divisions assert zero remainder, and its degree check asserts cubic
support. It stops collecting rows after the exact upper bound is attained, rather
than needlessly forming the other windows. Every collected window is one of the
784 necessary equations; no projected polynomial identity is asserted.

The complete primary run checks 5,744 labels with zero rank failures. The family
counts are 112, 1,008, 1,904, 2,720, respectively. `verify_structure.py` independently
enumerates the label universe and accepted exclusion set, checks unique coverage,
counts all template monomials, checks all exact holonomies and admissible
reductions, and validates every certificate schema and nonzero residue.

## 6. Saturation and conclusion

For families A,B, F is in I. For C,D, F^2 is in I. Therefore, in every case,

I : (xyz F)^infinity = (1).

The six original guards are required, and every inactive guard is an exact
nonzero constant. Thus the necessary modulus equations have no admissible
unit-torus solution. In particular no point on any remaining three-coordinate
slice is externally invertible-complex monomial-equivalent to F8.

Pole components are retained in the original equations and excluded only by the
original inverse guards. Variable zeros are kept in the polynomial computations;
unit phases already require xyz!=0. No anchor, entry, determinant of M, or
additional feasibility hypothesis is saturated away. A surviving necessary-modulus
component would not have been treated as a feasible Fourier endpoint; none
survives this certificate on the guarded domain.

This is a finite-slice exclusion theorem. It does not assert full-fiber
infeasibility, an FFT construction or speedup, a lower bound, or novelty priority.

## 7. Fresh execution and reproducibility

All executed research programs in this directory were authored for this attempt.
The earlier programs remained inert. There were no external writes.

python -I -S make_chart_header.py
g++ -O3 -std=c++17 verify_all.cpp -o verify_all
./verify_all > COVERAGE_PRIMARY.jsonl 2> COVERAGE_PRIMARY.log
python -I -S verify_structure.py > STRUCTURE_CHECKS.log
./verify_all 430477711 > COVERAGE_CONJUGATE.jsonl 2> COVERAGE_CONJUGATE.log

Review should independently check the cut-edge lemma, curved-intersection
conditions, all-label enumeration, polynomial construction and at least the full
primary minors. The candidate does not label itself independently accepted.
