# Independent review: separation-rank theory and Phase32

9 October 2026 UTC. The principal mathematical statements in both
archives are accepted, with one Phase32 reporting correction and a
trivial-length sampling-law qualification below. No uploaded program
was executed. Fresh independently authored checkers reproduce the
claimed finite controls.

## 1. Simultaneous separation: accepted all-length representation gate

This archive uses separation rank on rectangles separated by specified
row and column orderings. It does not use the operator-Schmidt rank of
a tensor realignment. These two flattening models must not be mixed.

The independent-row/column half-selection lemma is correct. In each
order pair, either the lowest half of the remaining rows precedes the
highest half of the remaining columns, or the reverse orientation
works. Failure of both would create a strict cyclic chain of
inequalities. Previous separations survive restriction. After d
distinct order pairs, the common rectangle has side

m=floor(N/2^d).

If its branch separation-rank budgets sum to R, the sum has rank at
most R there. A weighted Hamiltonian Green inverse has rank at most one
on such a rectangle: the unique directed arc product factors at a
separating cut. This argument does not divide by any edge weight, so
zero edges and zero cycle holonomy are covered whenever the inverse
exists. Independent row/column endpoint permutations and diagonal
gauges merely transport the two orderings and preserve the rank bound.

For the unitary Fourier matrix U, every m-by-m submatrix A has
Frobenius norm squared m^2/N and operator norm at most one. Hence
rank(A)>=m^2/N. This proves the necessary exact-representation bound

m^2<=NR

at every length. Prime Fourier full-spark gives the stronger m<=R at
prime lengths. The classical prime ingredient is supported by
[Tao's primary paper](https://arxiv.org/abs/math/0308286); novelty is not
claimed for it or for the elementary rank/norm inequalities.

The operator-norm approximation bound is also valid. If B is the
candidate's rank-at-most-R rectangle and P projects onto its column
space, then

||A-B||_F^2 >= ||(I-P)A||_F^2 >= m^2/N-R.

Coordinate restriction cannot increase operator norm, and a square
m-by-m matrix has Frobenius norm at most sqrt(m) times operator norm.
Therefore

||U-M||_2^2 >= max(0,m/N-R/m),

with zero bound when m=0. This proof works regardless of the branch
coefficients' size or conditioning. The target for this norm statement
is unitary Fourier; arbitrary nonunitary endpoint scalings of the
target are not silently norm-preserving.

For Q Green branches, R=Q and d<=Q. Thus the exact all-length branch
count is at least (1/2)log2(N)-O(log log N), the prime-length count is
log2(N)-O(log log N), and fixed Q gives asymptotic operator-error floor
at least 2^(-Q/2). These are additive representation restrictions,
not unrestricted arithmetic lower bounds or product-stage theorems.

### Independent controls

The fresh checker independently regenerates all 148 stored modular
rank records across 22 schedules, with arbitrary independent row and
column endpoint permutations. Every record matches, including the
Fourier submatrix ranks. It also checks direct weighted arc products,
30 zero-edge cases, and 20 shared-order cases.

All 48 prime cyclotomic controls are independently recomputed over
the integers: the small Fourier determinant is reduced modulo
z^p-1, and its coefficients are not all equal. Since the prime
cyclotomic polynomial is 1+...+z^(p-1), this certifies the selected
complex minors are nonzero. The general norm theorem is proved
analytically above, not inferred from modular experiments.

The archive's historical AUDIT_MANIFEST describes earlier source
reviews; this review does not claim to have re-audited every historical
archive listed there. The present theorem does not require those
historical novelty or audit assertions.

## 2. Phase32: accepted exact partial-column interpolation

For any fixed Hamiltonian orders and q selected input columns, each
row response determinant is a nonzero polynomial in the q independent
couplings after clearing Green denominators. Distinct assignments of
selected columns give distinct exponent tuples, because one cycle
assigns distinct distances to distinct input columns. Thus no
determinant terms cancel identically.

The same argument proves every Cramer numerator is nonzero as a
polynomial when all selected target entries are nonzero. The omitted
variable's selected target column is determined by the other
assignments, so there is no hidden monomial collision. Intersecting
these finitely many nonempty open conditions proves unique,
everywhere-nonzero output gauges for generic admissible couplings.

The augmented q+1-column determinant has the same distinct-monomial
property. Therefore matching q+1 columns with the fixed q Green
responses is generically impossible, while exceptional couplings
remain outside that generic claim. This does not automatically extend
to input-side diagonal gauges or products of stages.

For Fourier targets, the stated Kronecker substitution with
D=N+1, t=1/(2q!), alpha_s=t^(D^s) is a valid deterministic existence
law. Distinct exponent vectors remain distinct base-D powers; all
nonzero Fourier coefficients have modulus one, and the smallest power
dominates the remaining at-most-q!-1 terms. Its extreme exponent/bit
sizes are a real cost, not an efficient numerical prescription.

### Sampling-law guard qualification

The displayed degree d=Nq^2(N-1) can also cover the positive-integer
pole guard for N>=2, but that needs an explicit argument. In each of
the q output rows belonging to the selected input set, one determinant
exponent is zero in every term. The total determinant/Cramer product
degree is consequently at most d-q(N-1). Multiplying by
product_s(alpha_s-1), the only positive-integer pole obstruction,
still has degree at most d for N>=2. Schwartz–Zippel therefore gives
the stated at-least-one-half success law on sets of size greater than
2d at those lengths.

As written, the universal N>=q>=1 wording includes N=q=1, where d=0
and the permitted set {1} is entirely singular. State N>=2 for that
sampling corollary, or separately exclude 1 at N=1. The main generic
interpolation theorem and all tested Fourier lengths are unaffected.

## 3. Phase32 exact replay and corrected metadata

The independent checker uses a triangular linear-system solver and a
recursive radix-two Fourier reference, rather than the uploaded
Gauss–Jordan and iterative implementations. It rebuilds every
published seeded operator, including all cycle choices, couplings,
nonzero gauges, and rejections. Every saved operator fingerprint
matches exactly.

Reproduced results include:

- Five fitted columns through N=4096, all entries exact.
- The actual next column fails in every output coordinate at every
  published size, as does the dense-vector Fourier comparison.
- Both full Weyl identities fail on the independently tested dense
  inputs, while the selected-basis identities pass as implied by the
  fitted columns.
- Seven-column controls and the extra-null-direction four-column
  controls reproduce their stated behavior.
- Residual ranks are N-5 at N=8,16,32,64, and the rowwise augmented
  six-column systems have rank six in the checked small cases.
- q=N controls at N=8,16 reproduce every Fourier entry and a dense
  vector. They retain O(N^2) online and naive O(N^4) setup costs.
- Nine cyclic solves match independent sparse Gaussian solves, and
  all q=3 determinant/Cramer/augmented monomial checks pass.

### Reporting bug: 16 saved probe-column labels are wrong

The source audit function chooses the correct first unfitted column
and computes its mismatch count. Later it reuses the local variable j
while checking cycle successors, then writes that overwritten value
as out_of_sample_basis_column. Consequently 16 of the 17 records label
the wrong probe, sometimes one of the already fitted columns.

The N8 five-column record, for example, reports column 3 although the
actual failing probe is column 5. All wrong labels match the last
vertex of the final generated cycle, confirming the source of the
error. The independent output records every correction: actual probe
columns are 5 for q5 fits, 4 for four-column extra-direction fits,
and 7 for q7 fits. The operator fingerprints and all actual mismatch
counts pass. This is a reporting defect, not a failure of interpolation.

The supplied source is preserved unchanged; the corrected record is
PHASE32_INDEPENDENT_REVIEW.json.

## 4. Integration with the current product construction

Phase32 is a precise warning against inferring a Fourier algorithm
from overlapping local windows or selected-basis Weyl success. Its
q-column identities genuinely hold, yet the unseen columns and
global identities fail. Phase31 is not contradicted: it fixed the
generator gauges, while Phase32 solves for qN row gauges.

The new separation theorem strengthens the earlier prime-only bank
gate and covers the root-free weighted-cycle branches, including zero
wraps. A two-branch additive stage at dyadic N>=64 cannot itself be
Fourier, despite its possibly large rank on the natural half cut: a
different rectangle is simultaneously separated in its two orders.

Likewise adding input gauges cannot turn a fixed five-branch sum into
an exact all-length Fourier family. For dyadic N>=8192 the all-N
bound alone excludes it. A growing logarithmic branch count and a
genuinely joint evaluator are different questions.

Products of such sums remain outside this additive theorem. The
operator-Schmidt/realignment mask gate and any new simultaneous-cut
product obstruction use different invariants and must retain their
own coordinates, routing assumptions, and cost scopes. No result
here is a general FFT lower bound or a new fast full transform.

## Reproduction

check_phase32.py and check_separation_theory.py are new review code.
They read the uploaded JSON records but do not import or execute the
uploaded programs. Exact outputs, original archives, source hashes,
and a separate-directory byte-identical replay accompany the seal.
