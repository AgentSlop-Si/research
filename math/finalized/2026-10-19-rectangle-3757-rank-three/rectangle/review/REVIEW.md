# Independent review: the N = 3757 complex rank-three gate

Date: 19 October 2026 UTC. Owner M-RECTANGLE-TILING; priority 42 unchanged.

## Decision

The mathematical argument passes independent review. For arbitrary nonempty
Cartesian subsets of the original complex Fourier matrix F_3757, actual
rank at most three implies

    min(a,b) <= 51 or max(a,b) <= 78.

For actual rank three the exact local minimum density is

    3(a+b)/(ab) >= 16/221 = 272/3757 > 238/3757.

The lower endpoint is attained by a legal 51-by-221 rank-three rectangle.
There is no rank-three equality at the target rank-one density. Subject to
the retained rank-one and rank-two theorems, whose pinned proofs were read,
the target disjoint/no-sharing optimum is 894,166. Every optimizer has
exactly 3,757 full rank-one coset products with unordered side sizes
{17,221}. The claimed nonsharp higher-rank-area penalty 7/3757 is valid.

This review accepts this isolated target and its stated structural lemma.
It makes no all-length conclusion, successor-target selection, owner or
priority change, publication action, or novel-result priority claim. The
accepted N = 2873 checks and full tiling were not rerun.

The fresh independent controls in this directory pass. The universal
mathematical proof is the primary certificate. Finite samples of actual
minors are explicitly supplemental and do not exhaust arbitrary selected
Fourier rectangles.

## 1. What was reviewed independently

The reviewed candidate is
`../candidate/REPORT.md`. Its final hash and the completed author package are bound in REVIEW_PINS.json. The reviewer
also read the supplied N = 2873/3757 gate report, the pinned mixed-prime
supported-column separation proof, and the pinned rank-two density and
rank-one equality proofs. No historical author or reviewer program was
imported or executed.

The main source hashes are reproduced and verified by independent_controls.py:

- Supplied gate report: ef02706ac4265a67e5ff56f7f4d7bcfe41c987caf17e3cb0885f896d84bff1d5.
- Mixed-prime report: f986376ce3666499fcb7b53d9db16cf575c8f75862dd449cfc22e477dc279f66.
- Rank-two report: 7aacb964f32e3061d1f1c0d7d1d554e281a3d5d219b53dc11948c7bc83971cdf.

All ranks here are over C. The cyclotomic computations are exact
characteristic-zero computations. No finite-field rank, numerical sampling,
or scalar shape filter is used as a substitute for the uniform rank proof.

## 2. Independently checked universal argument

### Initial residue restrictions

Assume a >= 52 and b >= 79. If the columns occupy four classes modulo 17,
then a > 3*13 gives four rows in one class modulo 13. After row/column
scaling, these indices give a minor of F_289 on four distinct rows and
columns distinct modulo 17. The transposed prime-power minor theorem
makes that minor nonsingular. Thus the column occupancy is at most three.
Transposition gives the same restriction on the rows, since b > 3*13.

The prime-power theorem's Schur/Vandermonde argument is valid for arbitrary
higher digits. The numerator differences are units modulo 17 and the
factorial denominator involves only 1,2,3. The quotient is an integer
polynomial, so reduction modulo 1-zeta_289 correctly proves nonvanishing
in characteristic zero. This is not an assertion about arbitrary minors
whose residues repeat.

### Supported-column spaces

Fix the occurring row residues y modulo 17 and write r = y+17k. A column
fiber v modulo 221 consists of selected v+221w. On row class y, its
multipliers are zeta_17^(yw). Any s chosen distinct w in such a fiber
invert the prime-17 matrix on the s occurring y residues. Hence the full
column span contains the representative column supported on each row
class separately. For several fibers T, these supported spaces have
sum of dimensions

    sum_y rank F_221[A_y,T].

The factors zeta_3757^(yv) are nonzero column scalings on each supported
block. All representatives and all selected higher digits are covered.
Direct sum refers only to disjoint coordinate supports inside one tile;
it neither permits nor assumes sharing between tiles.

### One row residue

Each column fiber has at most 17 elements. Since b >= 79, there are at
least four distinct fibers. The semiprime short-support bound says that
four distinct F_221 characters cannot have a nontrivial dependence on
more than 51 rows. Here a >= 52, so rank is at least four.

The short-support proof is sound with arbitrary complex coefficients:
group the k' <= 4 nonzero terms by the order-17 character. Prime-13
minors bound common zeros of the nonzero coefficient functions; prime-17
minors bound zeros at every other point. The resulting total is at most
17(k'-1). Vanishing coefficient functions at individual points only
reduce the active number of characters and do not invalidate the bound.

### Two row residues: the strengthening

There are at most 3*13 = 39 column fibers. If at most two contain two or
more columns, their total capacity is 2*17+37 = 71, below b. Thus choose
three rich fibers. Each supported semiprime block is nonzero, and the
sum of their two positive integer ranks is at most three. The only
budgets are (1,1), (1,2), (2,1); one block has rank one.

For any two distinct frequencies in that block, put delta equal to their
nonzero difference modulo 221. Vanishing 2-by-2 minors confines every
row difference to the kernel of multiplication by delta. Its size is
exactly gcd(delta,221), which is 1,13, or 17. Thus that row class has at
most 17 rows. The other has at least 35 rows. Its three distinct columns
are independent by the 34-zero bound, so its rank is three. Adding the
nonempty rank-one block gives rank at least four, a contradiction.

This checks the potentially dangerous unbalanced row split directly.
It does not assume either class has more than half the rows, and it does
not require a generic choice of the three rich fibers.

### Three row residues

Without a fiber containing three columns, b <= 2*39 = 78. A triple fiber
therefore supplies three independent supported columns and spans the
entire assumed rank-three column space. Within each of the three row
classes every selected column is a scalar multiple of the same nowhere-
zero vector. Thus rows within that class are projectively equivalent on
all selected columns.

Let H be generated by all selected column differences and let K = H^perp
have size d. Projective row equivalence is precisely difference in K,
not just a sufficient relation. Therefore a <= 3d and b <= 3757/d.
The complete divisor list is 1,13,17,221,289,3757. Since a >= 52,
d > 17; every remaining divisor gives b <= 17, contradiction.
This also covers fewer than three actual projective classes.

These cases exhaust all row residue counts; the initial step exhausts
all higher occupancies. Transposition gives the symmetric dichotomy.
No interval, subgroup, random, generic-coefficient, or selected-lift
assumption remains in the statement.

## 3. Density, local sharpness, and equality

For actual rank three, 3 <= a <= b and stable rank gives ab <= 11271.
If a <= 51, then

    3/a+3/b >= 3/a+a/3757 >= 3/51+51/3757 = 16/221.

The second inequality is strict unless a = 51, because
(51-a)(3/(51a)-1/3757) is positive for a < 51. Equality in the first
inequality then requires b = 221. In the other dichotomy branch,
a,b <= 78 gives density >= 1/13 > 16/221.

A legal extremizer is R = K union (1+K) union (2+K), with K the subgroup
of order 17, and C = K^perp of order 221. All rows in each K-coset
coincide on C. The representative rows 0,1,2 on columns 0,17,34 give a
nonzero ordinary Vandermonde determinant. Thus its complex rank is
exactly three, its sides are 51 and 221, and it attains 16/221.
This establishes the local density value without claiming a full
classification of all local rank-three extremizers.

The old relaxation has exactly 750 dangerous shapes and just one equality
shape, (68,156). All 750 violate the new dichotomy. The equality shape is
therefore excluded structurally, not accepted as an actual rectangle.

## 4. Original cost, attainment, and retained qualifications

The target divisors give D = 238 with unique unordered minimizer {17,221}.
The retained sharp rank-two theorem gives E2 = 255. For r >= 4, stable
rank and AM-GM give density >= 4/sqrt(3757) > 245/3757, since
16*3757 = 60112 > 60025 = 245^2. Rank-three density is 272/3757.
Consequently every rank at least two has density at least baseline plus
7/3757. This common penalty is explicitly nonsharp.

Summing densities times areas over a disjoint covering of 3757^2 entries
proves cost >= 894166 + (7/3757) A_(rank>=2). The row cosets of the
order-17 subgroup and the column cosets of its order-221 annihilator
form 3757 rank-one tiles. Each has area 3757 and cost 238, so total cost
is exactly 894166. Independent complete one-dimensional partition checks
certify once-only Cartesian coverage; no N = 2873 replay is involved.

All higher-rank tiles have strict excess. The retained rank-one equality
argument forces full annihilating coset pairs with minimizing side sizes.
Every equality tile has area 3757, so every optimizer has exactly 3757
tiles. A common orientation is not assumed or claimed.

This is the original sum r(a+b) endpoint-incidence model with disjoint
Cartesian products and no inter-tile sharing. Paid root/coefficient
preparation, I/O and storage remain separate. The inherited possible
3757 additions for literal zero-initialized accumulation remain unchanged.
Nothing here establishes unrestricted Fourier circuit complexity.

## 5. Independently written exact controls

Run `python independent_controls.py`. This imports no candidate or
historical checker. RESULTS.json and controls.stdout.txt record execution.

- 14,657 exact prime-17 inversion minors of sizes 1,2,3, after independent
  row and column translation normalization. Every original minor is a
  nonzero scalar multiple of one represented here.
- All 220 nonzero frequency differences modulo 221 and all 24,090
  translated distinct frequency triples; kernel sizes are checked exactly.
- All finite occupancy bounds, positive low-rank budgets, 22 short-support
  integer cases, and all six annihilator divisors.
- All 750 old dangerous scalar shapes and all 33,110 stable-rank shapes
  admitted by the new dichotomy, with exact rational density arithmetic.
- All 48,400 nonzero projective row/column difference pairs, including
  384 zero factors; the zero exceptions are kept, not discarded.
- Exact characteristic-zero target determinant controls across five
  structural families, arbitrary translations and cyclic units, with
  genuine zero boundary controls. The 411 evaluations include the sharp
  local extremizer and duplicate-row/column evaluator checks.
- Twenty-four separate ordinary-polynomial divisions by Phi_3757 cross-
  check the tensor cyclotomic evaluator, including genuine zero cases.
- Every one of the 11,271 local rank-three extremizer entries is checked
  against its representative row; the nonzero three-minor proves rank
  exactly three. This also disproves changing the strict cutoff a > 51
  into a >= 51.
- The one-column rank-one block on 221 rows disproves deleting the distinct
  frequency hypothesis from the 17-row bottleneck.
- All 7,514 entries of the two complete one-dimensional coset partitions
  and the rank-one difference identities verify the target construction.

The determinant evaluator uses the exact tensor basis of
Q(zeta_13,zeta_289), of degree 12*272 = 3264. Ordinary cyclotomic division
is an independently formulated check. These finite checks reinforce the
proof; the sampled selected-index minors are not misreported as exhaustive
Fourier rectangles.

## 6. Final packet reconciliation

The final candidate report has SHA256
034371f74e7e0797ada08ec208a7b31ff3a77bc128eaf31d0adefa98aaa5df2a.
All fourteen author-manifest entries and all four source snapshots pass
byte-length and SHA256 checks; source Git blob checks pass as well. The
read-only published source receipt has the same content and Git blob as
the retained inherited source-pin snapshot.

The author checker was replayed in a separate review copy. All result
fields agree except elapsed time, and both the complete coverage
certificate and dangerous-shape certificate are byte-identical. The
replay took 1.952122 seconds. This replay supplements the separately
written reviewer checker rather than replacing independent verification.
AUTHOR_REPLAY_RECEIPT.json records the binding and outcomes.

Final result: ACCEPT the stated isolated N = 3757 theorem, exact local
rank-three density, strict target equality exclusion, target optimum and
rank-one-only equality classification in the original qualified model.
No unresolved residue pattern or mathematical gap remains in this gate.
