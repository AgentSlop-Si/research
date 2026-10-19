# Independent review: complete fixed-witness three-coordinate exclusion

## Verdict and scope

ACCEPT. Final acceptance is recorded in VERDICT.json and bound to the complete
candidate FULL_MANIFEST.json, SHA-256
eb53d5009f728deb13fa55a2d467e43ce5a18249f0c4e32b3aa833633a6bb3cd. The mathematical result independently checked here is:
all 5,744 newly submitted three-coordinate labels through the pinned original
N=8 chart are excluded from external invertible-complex row/column monomial
equivalence to F8 on their original guarded unit-phase domains.

This review does not rerun the inherited 240 exclusion proofs. Combining the new
5,744 labels with that inherited accepted set gives all C(34,3)=5,984 labels.
The conclusion concerns this one frozen witness, selected multiplicative phase
coordinates, original six inverse guards, unweighted three-Green stage sums and
product S2 S1. It is not a theorem about the full 34-phase fiber, other witnesses,
four or more moving phases, nonunit internal gains, other dimensions, a free
interstage diagonal, Fourier algorithms, complexity, or novelty.

## Source and model reconstruction

The core manifest was byte-verified before review and copied into input/. Its
SHA-256 is 7116974db5eed031ad7fe5e4e907c2850c341bdc65cc2c7eb647527f544c93aa.
The chart is the full 3,138-byte original chart, SHA-256
5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98.
Every core entry's size and hash matched. The final full freeze is checked
separately; optional control data do not replace proof obligations.

Independent source checks examine N=8, all six length-eight permutations, all
34 Gaussian pairs, seeds 42420 and 42520, phase indices 7 through 23, coefficients
[1,1,1], product order S2*S1, and the first seven unit tree edges in each stage.
The exact gain corresponding to pair (a,b) is reconstructed as
((a^2-b^2)+2ab i)/(a^2+b^2), independently of the author's ratio implementation.
All 48 gains have unit norm. The six exact holonomies are independently multiplied,
are nonzero with norm one, and differ from one. They are recorded in
INDEPENDENT_STRUCTURE.json. Seed-to-chart historical provenance is inherited
from the accepted source review; seed metadata and the entire fixed chart are
checked here. No historical generation or accepted exclusion program is executed.

For each label the selected original gains are changed to their witness gain
times x,y,z in sorted encoded-label order. The independent arithmetic does not
import or call any author module. It writes I-W directly from the convention
that edge 8b+j goes from cycle[j-1] to cycle[j], independently inverts each of the
six matrices, forms both stage sums and their ordered product, and multiplies
by all six guards. It evaluates at all eight points of {0,1}^3 in each Gaussian
embedding, then uses Boolean difference interpolation to recover every triaffine
coefficient of N=Delta M. The degree bound is established symbolically below,
so this interpolation is complete, not a sampling assumption.

At these points each branch guard is either 1 or its checked nonzero frozen
guard. Every direct inverse is checked on both multiplication sides, and its
elimination determinant is compared with the original branch guard. This totals
551,424 direct Green inversions and 70,582,272 inverse-entry comparisons. Zero
coordinate values are used safely in these polynomial reconstruction checks;
no unit-phase interpretation is assigned to them.

## Exact polynomial construction and pole containment

Let K=Q(i). For a branch write d=1-hm, where m is the product of that branch's
selected variables. The weighted-cycle identity W^8=hm I gives
B=sum_{j=0}^7 W^j and (I-W)B=B(I-W)=dI. Thus, with
A_s=sum_b B_sb product_{c!=b}d_sc and D_s=product_b d_sb,
N=A_2 A_1=Delta M, Delta=D_2 D_1. Every path encounters a chosen edge at most
once. Variables belonging to different branches and stages are disjoint, so
all entries of N are triaffine. No guard or matrix entry is inverted in this
polynomial definition. Inactive guards are nonzero constants and Delta=cF,
where c is nonzero and F is the product of the active guards.

Define Nt=xyz conjugate(N)(1/x,1/y,1/z). This is a polynomial, coefficient
conjugation being essential. The P for all 784 row-pair/column-pair windows are
the two-by-two minors of the entrywise product N*Nt. On the unit torus they are
(xyz)^2 |Delta|^4 times the corresponding squared-modulus minors of M.
Invertible complex left and right monomials applied to F8 give squared entry
moduli equal to positive row factors times positive column factors; permutations
preserve this rank-one property. Therefore these P are necessary equations for
the requested full complex-monomial target. Their sufficiency is never asserted.
No entry, anchor or determinant of M is divided out; zero-entry components remain.

Each active d=1-hm is irreducible: after quotienting, the product m is a nonzero
constant, so its variables are units, and solving for one identifies the quotient
with a Laurent polynomial ring in the other active variables, together with the
unrelated variables. On this irreducible divisor W is a weighted cycle of
holonomy one. Its eigenvalue 1 is simple and B has rank one. The cleared affected
stage, hence N, has rank at most one there. Coefficient conjugation and reciprocal
variables preserve this divisor because conjugate(h)=h^(-1). Hence Nt also has
rank at most one on the dense open part of this divisor where all variables
are nonzero. Its polynomial two-by-two minors then vanish on the entire
irreducible divisor, including points with unrelated zero coordinates. Their
entrywise product has rank at most one, so every P vanishes modulo d. Thus d divides P over K. Different active guards have disjoint
nonempty variable sets, are nonassociate irreducibles and are relatively prime.
Their product F divides every P. Write P=FQ. Degree additivity in each individual
variable over an integral domain proves that every Q has coordinate degree at
most three.

## Independent proof of the cut-edge support bound

Formal conjugate-reciprocal transpose gives W^dagger=W^(-1), so for each branch
G+G^dagger=I and for a stage S+S^dagger=3I. If R_s is the product of its selected
variables, then
R_s conjugate(A_s)(reciprocals)=c_s(3D_s I-A_s^T),
c_s=-1/(h_s0 h_s1 h_s2).
Consequently Nt=c_2 c_1(3D_2 I-A_2^T)(3D_1 I-A_1^T).
These are rational identities first proved in the function field. Both sides of
the displayed cleared identities are polynomials, so they remain valid after
setting a coordinate to zero. No unitarity or invertibility at a zero gain is
being assumed.

Suppose x and y are on distinct edges of the same cycle and set x=0. The cycle
becomes a directed path. Cutting that path additionally at the y edge partitions
vertices into an upstream set and a disjoint downstream set. The coefficient of
y in B factors as U V^T: U is supported downstream, V upstream. An additional
variable on the path can be retained in these factors. Therefore U_j V_j=0
identically for every vertex j, also when the third variable is zero.

The active guard becomes 1 and D_s becomes independent of y. The y coefficients
of A_s and 3D_s I-A_s^T are respectively a scalar polynomial times U V^T and its
negative times V U^T. If this is stage 1, the y coefficients of N and Nt retain
right factors V^T and U^T; if stage 2 they retain left factors U and V. Their
entrywise product is zero in either case. Thus N*Nt has y degree at most one
after x=0, and P has y degree at most two. F at x=0 is a nonzero polynomial
independent of y. Since P=FQ, Q at x=0 has y degree at most two. Exchanging x,y
proves the other forbidden case. This proves the exact coefficient zeros at
exponents (0,3) and (3,0), with every exponent of the third variable retained.
It uses no branch, stage, edge or certificate transport between labels.

## Exact coefficient spaces and target membership

1. All three edges in one branch. Apply the support bound to every pair.
The permissible monomials x^i y^j z^k, 0<=i,j,k<=3, have
max(i,j,k)-min(i,j,k)<=2. Direct integer enumeration gives dimension 46.
This space contains 1.

2. Mixed stages, with two edges in one branch. Applying the bound to that pair
gives |i-j|<=2, with the third exponent unrestricted from 0 to 3. The resulting
space has dimension 56 and contains 1.

3. Same stage, two edges in one branch and one in a different branch. Name the
pair x,y, put f=1-hxy, g=1-kz, J=(f,g). At f=g=0 each term of the affected
A_s lies in J, as does 3D_s I-A_s^T. Thus entries of N and Nt lie in J and
P lies in J^4. In K[x,x^(-1),t,z], t=xy, f and g are independent affine
coordinates. The monomial ideal calculation (J^4:fg)=J^2 proves that Q belongs
to J^2 after this injective localization. Only the resulting linear conditions
are needed; no contraction claim or discarded x=0 component is used.

The cut-edge support has five Laurent x-degree blocks delta=-2,...,2.
In block delta, the polynomial is x^delta times t^max(0,-delta) times a
polynomial of t-degree <=3-|delta| and z-degree <=3. Its raw dimensions are
8,12,16,12,8. At t0=1/h,z0=1/k, the value and two first partial derivatives
must vanish separately in each block, since distinct x powers are independent.
Multiplication by t^max(0,-delta) is invertible on the first-order jet space
at nonzero t0. The polynomials 1,t,z already give three independent jets since
3-|delta|>=1. Exactly three conditions per block therefore leave dimension
56-15=41. This defines a K-linear subspace of the original polynomial space.
The polynomial F=fg lies in it: its support is permitted and it has order two
at the intersection. The localization was used to prove constraints, not to
move the final identity out of K[x,y,z].

4. Mixed stages, two different branches in one stage. Put u=x-1/h,v=y-1/k
for the same-stage pair. Entries of the affected cleared numerator and its
reciprocal reversal lie in J=(u,v); hence P lies in J^4. Here
F=c uv(1-lz), c nonzero. Multiplication by nonzero 1-lz is injective on
K[u,v,z]/J^n, a free K[z]-module on u,v monomials of total degree <n.
Also (J^4:uv)=J^2 by monomial divisibility. Therefore Q lies in J^2.
Translation of x,y preserves the full coordinatewise cubic space. Omitting
1,u,v for each of the four z exponents leaves dimension 64-12=52.
F belongs to this space and to J^2.

All these are characteristic-zero statements. Modular support and jet checks
in the arithmetic replay are supplementary error controls, not proofs of the
upper bounds. Full coefficient matrices are used, with no unsupported monomials
silently projected away.

## Admissible reductions and independent fixed minors

Use R0=Z[i,(a+ib)^(-1),(a-ib)^(-1) for all 34 original pairs]. Every gain,
conjugate gain, holonomy and inverse holonomy lies in R0. Construction of N and
Nt uses only ring operations. Division by an active guard can use its leading
coefficient -h, which is a unit in R0, so the exact Q also has coefficients in
R0. No frozen guard inversion is necessary for this coefficient-ring assertion.

Complete integer trial division verifies p=1,000,000,009 prime. Both
569,522,298 and 430,477,711 square to -1 modulo p. All 68 inverted Gaussian
factors have nonzero images in both embeddings. Exact holonomies and all frozen
guards also have nonzero images. Thus each reduction R0 -> F_p is a genuine
ring homomorphism. Opposite embeddings implement Gaussian coefficient
conjugation. There is no finite-field interpretation of absolute value.

The independent verifier reconstructs N by direct inversions and interpolation,
forms N*Nt and the requested original polynomial windows, and divides F by a
separate ascending constant-term recurrence. Each division is multiplied back
coefficientwise, including the potential outer-degree terms. Coordinate degrees,
cut-edge support and applicable Taylor jets are checked. It selects exactly the
recorded windows and columns in their recorded order. Ordinary row-pivoted
elimination evaluates that fixed square determinant; no replacement minor is
allowed. Every primary and conjugate record matches exactly.

Independent results:
- 5,744 distinct labels, exactly the complement of the inherited 240
- family counts 112, 1,008, 1,904, 2,720 for dimensions 46, 41, 56, 52
- 11,488 matching nonzero fixed determinant checks
- 589,088 full reconstructed P/F quotient checks
- 551,424 direct inverse determinant and two-sided inverse checks
- 70,582,272 inverse-entry comparisons
- 7,676,256 supplementary modular jet comparisons
- eight duplicate-row determinant controls, all zero

The inspected fresh author C++ source was also compiled in the review directory;
both complete replay certificate files match their frozen originals byte-for-byte.
No historical 240-case program was imported, compiled, executed or evaluated.

Each nonzero modular determinant is the image of its specific exact determinant
in R0, so that exact determinant is nonzero over K. Together with the proved
matching upper-space dimension this makes the selected Q span the entire stated
space. Thus 1 is a K-linear combination of Q in dimensions 46 and 56, and F is
a K-linear combination in dimensions 41 and 52. Consequently F belongs to the
original P ideal in the first two cases, and F^2 belongs in the latter two.
This determinant lift is distinct from an invalid rootlessness or modular
Groebner-unit inference.

## Original guards, zero components and conclusion

Every new slice therefore satisfies I:(xyzF)^infinity=(1), where I is generated
by the original 784 division-free necessary equations. Indeed F or F^2 already
belongs to I globally in K[x,y,z]. No variable-zero component, no entry-zero
component and no denominator component was silently removed to obtain this
polynomial identity. Every inactive guard is an independently checked nonzero
constant; active poles are excluded precisely by the original inverse guards.
Unit phases require xyz nonzero. On this guarded unit torus, all necessary
modulus equations cannot vanish, hence the requested Fourier equivalence is
impossible.

## Reproduction and limits

Run only the newly written independent review programs:

python -I -S independent_checks.py
g++ -O3 -std=c++17 independent_minors.cpp -o independent_minors
./independent_minors

The fixed data and full candidate bindings are included. Recompiling and running
the inspected fresh author verifier is a separate supplementary replay. Runtime
figures in logs are environment-specific and are not complexity claims.
No external state, GitHub repository, permissions or sharing setting was changed
by this review. The accepted historical source chain and 240 proofs remain
inherited, and no historical authorship, discovery priority or canonical
repository-state claim is added.

## Final freeze and clean replay

All 35 full-manifest members and both nested manifests pass independent byte
checks. There are no unmanifested regular input files apart from the manifest
itself. The original accepted review bytes compute exactly to Git blob
0fb2b065b626d756850e0d5e9a2028b43bc06449. The core review copy is exactly that
content plus one trailing newline; SOURCE_BINDINGS.json records the difference.
The core proof and data were never changed after the initial freeze. Optional
author control sources and outputs are inspected and byte-bound but were not
needed or independently replayed for acceptance.

A clean separate-directory replay of the independent programs reconstructs the
entire source/coverage data and all 11,488 fixed minors again. All fixed data
match byte-for-byte and all arithmetic counts agree, ignoring environment-specific
runtime. COLD_REPLAY.json binds the independent program hashes and outcomes.
