Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 3546bc5d4a6bc716cb16f920eae145c52c6bcc62f322c914b18ddd3010bbce35

---

# N256 affine-target path isolation: independent bounded acceptance

Date: 2026-10-12 UTC. Verdict: **ACCEPT, bounded local result only.**

The reviewed candidate is `N256_Affine_Path_Isolation_CANDIDATE_2026-10-12.zip`,
6,322,970 bytes, SHA-256
`f1d9b74368471856f34937533127b3eb7087b6bb230a955b89baf32df719fe71`.
Its manifest SHA-256 is
`d2ec4fd5ac5d4d5bcad6677d4723e5d8d9617e063af80d5b1ee633dfa1e7f12b`.

**N256::full-feasibility remains OPEN.** This is later-uploaded-result verification
and a precisely stated local corollary, not a new Fourier factorization, global
impossibility result, FFT speedup, or historical-priority finding.

## Accepted statement

Over K = Q(zeta), zeta^128 + 1 = 0, let U_F[i,j] = zeta^(ij)/16. Fix the three
archived affine permutations, the literal rational generator point, and the
normalization and Schur charts specified below. Let U0 be the product of the
four normalized synthetic stages and U(t) = U0 + t(U_F - U0).

The 2,036 selected necessary rank-gate residuals, together with the extra
mask-64-side-A residual at physical entry (33,0), form 2,037 regular rational
functions F of the 2,036 normalized outer variables x and t. At (x0,0), F=0 and
the full Jacobian D_(x,t)F is invertible. Thus (x0,0) is an isolated reduced zero
locally, both analytically and algebraically. No nonconstant formal or finite
ramified Puiseux curve in these normalized (x,t) coordinates passes through it.
In particular, no full factorization branch with varying t can approach this
point along this target path.

This does not assert that all four raw stages are uniquely determined at fixed
target: internal-stage or redundant-generator/gauge motions with x=x0 and t=0
are outside the asserted isolation. It does not rule out other starting points,
other components, other target paths, or Fourier solutions at t=1.

## Exact model and admissible chart

The stage entries are a_i b_j below the diagonal, d_i on it, and c_i e_j above it.
The product is S4 P3 S3 P2 S2 P1 S1, with P_s v = v[p_s]. The three GF(2) column
lists are exactly:

- [190,52,71,48,22,117,118,121]
- [58,20,167,24,254,26,247,78]
- [140,249,103,236,246,36,32,51]

All are permutations. The separately recorded Toffoli sequence is unused.
There is no substitution of a general quasiseparable parametrization.

At the rational point, normalize S1 by left diagonal scaling and S4 by right
diagonal scaling to make their diagonals one. Normalize the four scalar
rescalings b1[0], e1[255], a4[255], c4[0] to one. Discard only the structurally
unused a[0], b[255], c[255], e[0] slots of each outer stage. The active counts are
1,018+1,018=2,036, in the exact archived parameter order. The reviewer constructs
these coordinates first as Python Fractions, then reduces those same rational
values into each field. All 516 divisors and every resulting rational generator
denominator have good reduction.

These are local gauges, not global exclusions. Left scaling of S1 is absorbed
by right diagonal scaling of S2 conjugated through P1; right scaling of S4 is
absorbed by left diagonal scaling of S3 conjugated through P3. Diagonal scaling
preserves the separated-generator form. The selected gauge coordinates and all
outer diagonals must be nonzero to enter this normalization. No assertion is
made about charts where they vanish.

The rational residuals require det U(t) and each selected Schur pivot determinant
to be nonzero. The synthetic point also has all four stage determinants nonzero.
These conditions specify an open neighborhood of the point; they are not
discarded by taking an affine closure. Any smaller outer-only feasibility system
must retain actual determinant-unit conditions, such as eta_s det(S_s)-1=0.
By contrast, full equality with the invertible Fourier matrix forces stage
invertibility and needs no separate determinant saturation.

## Why the equations are universal necessary conditions

Put M=S3 P2 S2. For a full factorization,
H=S1 U^-1 S4=P1^-1 M^-1 P3^-1. For a balanced input color set C and forward output
set R complementary to that color transported through P2, the selected inverse
block is M^-1[C^c,R^c]. Complementary nullity for invertible M gives it the same
rank as M[R,C]. The reviewer reconstructs the physical row/column pullbacks
directly from the three permutations and checks every archived selected set.

For mask64, the two alternating-color boundary counts are 3 and 13. A separated
scan's complementary-color block has rank at most its boundary count: split the
rows into monochromatic runs, with one lower and/or upper rank-one contribution
per adjoining source side. Splitting the two-stage product at its intermediate
color partition and applying rank subadditivity gives the universal bound16.
The counts were independently reconstructed, rather than read from a rank test.

For P22 and P26, the reviewer independently builds all scalar x,L,R,y dependency
edges of the two inner scans, the middle permutation, and scalar input/output
terminals. Splitting scalar signals into input/output nodes lets each archived
cut edge carry one scalar degree of freedom. Both side-A and side-D separators
were checked as literal graph edges and each disconnects its terminals after
removal: 22,22,26,26 edges, respectively. Each graph has 6,136 edges. This proves
the rank bounds over every field and all coefficients. It does not infer a
universal rank bound from sampled matrices.

The synthetic rational target is a genuine four-stage product. Therefore it is
an exact characteristic-zero common zero of these necessary equations, without
needing to infer vanishing from modular zero. Nonzero modular pivot minors give
the required characteristic-zero pivot invertibility.

## Independent arithmetic and derivative reconstruction

Only the reviewer's new programs were executed. The candidate programs and all
uploaded original programs were kept inert. All frozen input hashes were checked
against the candidate manifest and found byte-for-byte within the recursively
nested original ZIP. The top source SHA-256 is
`f7c52f45137688dff48a2a5d6af550d56c45297e3bcd5072565b371e2774e798`.
The nested full-model and saturation sources match their separately pinned
5,696,733-byte and 5,658,352-byte archives, respectively.

For Schur residual Z=D-C B^-1 A, direct differentiation gives dZ=L(dH)Q.
The reviewer constructs these annihilators from the archived pivots and verifies
the entire Schur residual blocks vanish in each field. Instead of the candidate's
per-parameter rank-one feature algorithm, the review computes reverse-mode
prefix/suffix derivatives of each scalar functional l S1 T S4 q. For example,
the S1 a_i derivative is l_i sum_(j<i) b_j (T S4 q)_j, with the other three arrays
handled by their appropriate prefix/suffix adjoints. All 2,036 parameter columns
also receive direct matrix-entry derivative checks on independently selected
Schur functionals. A full simultaneous parameter direction is reconstructed as
dS1 and dS4 and projected through every mask64 residual.

The target derivative is dT=-T(U_F-U0)T and is verified by the differentiated
inverse identity U0 dT+(U_F-U0)T=0. The roots have exact order256 and satisfy
zeta^128+1=0 in the corresponding prime fields. The normalized Fourier inverse
is checked exactly.

Square determinants use last-available row pivots, normalized pivot rows, exact
signed-int64 arithmetic, and no floating-point routines. The complete bordered
matrix is transposed and independently eliminated in its entirety. It is not
accepted from det(J) times the claimed scalar residual. Dot-product accumulation
is bounded by 2037*(65536)^2 < 2^63; row updates and all prefix sums also remain
within the signed-int64 bound.

Results:

- GF(65537), root282: det J=20796; det bordered=24460; residual58063.
  Normalized stage determinants: 42568,33714,32694,30922. det U0=2565.
  Schur pivots A,D,P22A: 60147,23101,56463.
- GF(12289), root8340: det J=10584; det bordered=2574; residual8799.
  Normalized stage determinants: 4559,2187,2109,6589. det U0=6479.
  Schur pivots A,D,P22A,P26A: 9565,7769,1816,8973.

The two primes use different explicitly pinned 2,036-row minors. They are not
two residues asserted to belong to one common rational determinant. Either
nonzero certificate individually suffices for the corresponding theorem.

The faithful int64 Jacobian hashes match the candidate. The historical uint16
hashes also match, but they are only provenance checks because the residue65536
is not faithfully representable in uint16. Mathematical acceptance uses the full
int64 matrices and exact determinants. The review additionally pins faithful
bordered-matrix hashes.

Negative controls reject a singular matrix and verify row-swap sign. Replacing
the final forcing by a compatible value yields an explicit nonzero null vector
of the full bordered matrix. The corrected full mask64 residual counts match:
11528 per side in GF(65537), 11527 per side in GF(12289).

## Lifting and isolation, rather than only a tangent claim

All matrix entries before target inversion lie in the localization of the
rational generator coefficient ring at the checked normalization divisors. The
remaining denominators are products of det U0 and the selected Schur pivot
determinants. Their modular reductions are nonzero. Adjoining zeta and reducing
zeta to the specified primitive root therefore gives a valid homomorphism from
the relevant coefficient localization to the prime field. A determinant that
were zero over K would reduce to zero. The observed nonzero bordered determinant
is consequently nonzero over K. This argument never uses modular zero as proof
of characteristic-zero zero or finite-field rank as an upper bound.

At the common zero, D_(x,t)F is invertible. The complex analytic inverse-function
theorem gives a neighborhood in which F=0 only at (x0,0). Algebraically, the
independent linear terms span the cotangent space; Nakayama's lemma gives the
maximal ideal as the localized equation ideal, so this is an isolated reduced
point on the regular chart. For a nonconstant positive-valuation Puiseux vector
h(u), the least-order term of F((x0,0)+h(u)) is D F times the nonzero least-order
coefficient of h. Invertibility makes cancellation impossible. This includes
finite ramification t=u^m, and is stronger than merely excluding t'(0)=1 lifts.

This local corollary is valid. The uploaded Phase52 already contained the
square/bordered certificates and first-order obstruction. The review verifies
those earlier results and accepts the explicitly derived isolation/ramification
scope; it does not label the determinant values as newly discovered.

## Additional controls and exact limitations

The reviewer independently checked 784,384 all-basis lifted equation instances
per field, 1,568,768 total, by comparing the prefix/suffix recurrence with dense
stage multiplication. The raw saved product differs from Fourier in 65,535
entries at p65537 and 65,532 at p12289. Every raw stage determinant agrees with
the division-free two-state transfer. The all-zero-diagonal, all-off-diagonal-one
stage is invertible, with determinant -255 in both fields; the all-ones stage is
singular and cannot satisfy a determinant reciprocal equation. Symbolic transfer
identities for n=1,2,3 were independently checked.

The 64 scalar energy inequalities and 62 overlaps of size8192 were independently
reconstructed. The two disjoint strongest blocks require48 each, and the exact
uniform-on-support assignment attains total96. This is a scalar relaxation
witness only, not a network. Model counts, degree distinctions, and chart sizes
were checked. This review does not independently revalidate all82 gates or the
full1,151-seed symbolic reduction, and does not upgrade their scope.

The full Fourier fiber can be closed only by an exact characteristic-zero
full-entry factorization witness or a complete characteristic-zero infeasibility
certificate for the full model (or a proved equivalent all-chart saturated
formulation). Neither is present. The chosen path system itself has (x0,0), so
its ideal is not the unit ideal.

## Scope and remaining work

Existing full-model, saturation, stability and relaxation acceptances are retained. The full Fourier-feasibility question remains open. Isolation concerns only the specified normalized synthetic point on the specified affine target path, including ramified varying-target lifts. Other points, components, paths and fixed-target internal/gauge motions are not excluded.
