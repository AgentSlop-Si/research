# Independent ACCEPT: the frozen Q27 stage-2 branch-1 triple family

## Decision and precise scope

Accept the 46 newly submitted exclusion certificates for exactly the labels in
FAMILY.json. Together with the ten previously accepted labels, these exhaust all
56 coordinate triples (2;a,b,c) with 8 <= a < b < c <= 15 in the fixed original
chart. The classification is exclusion of external invertible-complex row/column
monomial equivalence to F8 on each original guarded unit-complex slice. The same
necessary-modulus proof excludes every common nonzero entry-modulus target.

The inherited accepted union therefore increases from 194 to 240 of 5,984
three-coordinate labels, leaving 5,744 unclassified. The full 34-phase fiber
remains OPEN. This is a completed finite frozen family, not a full-fiber result.
The 194 inherited proofs are inherited and were not rerun in this review.

Every new label has a positive characteristic-zero coefficient certificate.
There are no missing cases, solver-failure classifications, feasible witnesses,
or null certificates in the accepted 46-case result. A multiplier identity is
an exclusion witness; it is not a numerical feasible point.

## Independent reconstruction

Only the new review programs in this packet were executed. Neither author code
nor any historical program was imported, executed, compiled, evaluated, or used
as a library. Candidate programs and their executable binaries remain inert
archive members for byte-manifest checks. Exact arithmetic uses Python integers
and fractions, not the author's GMP solver.

The source definitions and prior contract were read before the new certificate
review. The original chart is independently checked from seeds 42420 and 42520:
six cycles, 34 Gaussian pairs, and spanning-tree selection by graph reachability.
All 48 frozen gains have unit norm, and edges 0 through 6 of each stage have gain
one. The branch edge 8b+j sends cycle[j-1] to cycle[j]. Stage sums have coefficients
one, the product order is M = S2 S1, and G_sb = (I-W_sb)^(-1).

For each new label, x,y,z multiply precisely its three stage-2 branch-1 gains.
All other 31 free gains and all tree gains remain fixed. Every label was rebuilt
separately. No symmetry transfer, relabeling of an inherited certificate, branch
weight, interstage matrix, or different witness was used.

A fresh directed-path construction produces each B = I+W+...+W^7. Independent
matrix multiplication checks both (I-W)B = f I and B(I-W) = f I. All six guard
polynomials and holonomies are rebuilt from the original gain products; all five
inactive guards are separately nonzero. For the active branch,

f = 1 - h21 xyz,
h21 = (-4335586066535028372496 + 1298149621513208810103 i)
      / 4525759492081695535625,
H = 4525759492081695535625 > 0.

Thus n = (B + f(G20+G22))S1 = fM on the original guarded domain. The least positive
integer S clearing all real and imaginary coefficient denominators is recomputed.
All 64 entries of N = Sn are checked Gaussian-integral and triaffine and compared
coefficient-for-coefficient with the author's frozen numerator.

The coefficient-conjugate reversal is

Ntilde(x,y,z) = xyz conjugate(N)(1/x,1/y,1/z).

For every 1 <= r,c <= 7, independently form

P_rc = N_rc N_00 Ntilde_rc Ntilde_00
       - N_r0 N_0c Ntilde_r0 Ntilde_0c.

Exact sparse polynomial division by f, zero-remainder checking, positive rational
content extraction, and multiplication back establish P_j = f c_j q_j. Each q_j
is primitive Gaussian-integral and c_j > 0. No guard, variable, anchor, or matrix
entry is divided out. Across 46 cases, every coefficient of all 2,944 numerator
entries, 2,254 original defects and 2,254 normalized quotients matches the freeze.
There are 131,726 nonzero original-polynomial coefficients and 90,342 nonzero
quotient coefficients.

## Literal certificate verification

The predeclared multiplier space is span(1,z,y,x), with 196 possible Gaussian
coefficients. Independently rebuilding all columns gives 85 full monomial rows
for each case. Actual successful certificates use 42 nonzero constant
multipliers each, 1,932 in total; no affine term is needed in these witnesses.
This is an existence result, not a minimal-degree or full-rank result.

For each label the positive common denominator d and every Gaussian-integer
numerator a_j are validated. Common content is one: gcd(d, all real and imaginary
numerators) = 1. Denominators range from 3,134 to 3,942 decimal digits. The largest
stored scalar has 13,093 bits, within the 65,536-bit contract cap.

Full exact accumulation over Q(i) verifies, separately,

sum_j a_j q_j = d H f,
sum_j (a_j/c_j) P_j = d H f^2.

The second check directly accumulates reconstructed original P_j. It is not
inferred by multiplying the first identity by f. Each constant-certificate
check includes the full 44-monomial quotient support and 63-monomial original
support, including every coefficient that must cancel. Unsupported monomials
cannot be dropped by a selected-row projection. Modular ranks, sample values,
and source digests are never substitutes for these characteristic-zero checks.

## Why the original target is excluded

On the complex unit torus, reciprocals are conjugates. Consequently,

P_rc = S^4 (xyz)^2 |f|^4
       (|M_rc M_00|^2 - |M_r0 M_0c|^2).

A nonzero constant-entry-modulus matrix, after invertible complex row/column
monomial operations, has squared entry magnitudes factoring into a positive row
factor times a positive column factor. Row and column permutations preserve that
property, so all displayed anchored minors vanish. This necessary condition
applies in particular to external monomial equivalence to F8.

If the target were attained, all P_j would vanish. The second literal identity
would imply d H f^2 = 0, contradicting characteristic zero, d>0, H>0 and the
original guard f!=0. No sufficiency of the anchored conditions is required, and
no additional matrix-entry nonvanishing hypothesis is used.

Algebraically f^2 belongs to the ideal of the original P_j over Q(i), and the
ideal becomes the unit ideal on localization at f. The polynomial identity is
valid over characteristic-zero extensions. Its modulus/Fourier interpretation
here is restricted to unit-complex moving gains.

## Direct original-model and mutation controls

At (1,1,1), at ((3+4i)/5,(5+12i)/13,(8+15i)/17), and at
((20+21i)/29,(-7+24i)/25,(9-40i)/41), the checker independently eliminates every
original I-W for each label. It verifies determinant equals the corresponding
original guard and both multiplication orders for every inverse. There are 828
successful original-matrix inversions, 8,832 exact numerator-entry comparisons
N=SfM, and 6,762 exact modulus-bridge comparisons. These supplement the symbolic
proof and do not replace it.

For every label, (1,1,conjugate(h21)) has f=0, all five inactive guards remain
nonzero, and direct elimination detects a singular original active inverse.
The target dHf^2 vanishes there. This genuine original pole remains excluded;
denominator clearing does not admit it.

All 23 additional mutation tests reject the altered input. Fourteen full exact
polynomial accumulations detect: multiplier perturbation, omitted multiplier,
changed denominator, target power one, reversed target sign, changed content,
unsupported x^9/y^9/z^9 terms, omitted coefficient conjugation, reversed stage
order, moving variables to stage one, replacing the third edge, and a changed
anchor. Exact nonzero residual coefficients are saved in NEGATIVE_CONTROLS.json.
Six tests separately check source/schema bindings: altered contract bytes,
altered frozen bytes, wrong stage label, missing guard, negative anchor metadata,
and reversed multiplier order. Three enumeration controls reject a missing case,
a duplicate, or an inserted inherited case. Binding controls are not misreported
as wrong-model polynomial computations.

## Sources, completeness and replay limits

The accepted-194 archive, its candidate input, the accepted-193 archive, and its
author input all have independently verified complete manifests: unique safe
member paths, exact sizes and SHA-256 values, and no unmanifested members. Current
ledger and review bytes are matched to sealed members. The chart and three inert
source snapshots are matched through the accepted source chain. Every new
certificate is bound to the fixed contract and its full frozen-input bytes.

The family is independently enumerated as C(8,3)=56 labels minus the exact ten
already accepted stage-2 branch-1 labels. The new 46 labels are duplicate-free
and disjoint from the inherited 194 labels. Their union is recorded separately
in COVERAGE_240.json. Coordinate-label counting does not assert disjointness of
the geometric slices, which share the frozen witness.

The bound zero-solve receipts are checked, but archive bytes alone do not prove
wall-clock pre-solve chronology. Model sources retain their inherited inert-text
provenance limitation. No historical-source authenticity, discovery priority,
author identity, canonical repository state, new proof of inherited exclusions,
minimal degree, rank upper bound, all-route conclusion, FFT speedup, lower bound,
or full-fiber closure is claimed.

The final candidate archive and clean replay hashes are recorded in VERDICT.json
and COLD_REPLAY.json. Cold replay reconstructs every model again from sealed
source data and executes only independently authored review programs. No external
state, live spreadsheet, GitHub repository, permission, or sharing setting was
changed by this review.
