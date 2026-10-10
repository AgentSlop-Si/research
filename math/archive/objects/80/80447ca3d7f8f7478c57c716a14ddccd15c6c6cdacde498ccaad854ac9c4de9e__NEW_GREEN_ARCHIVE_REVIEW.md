# Independent review of Phase31 and Green-bank v18

9 October 2026 UTC. Both newly supplied archives are accepted within the
scopes below. No uploaded program was imported, compiled, or executed.
The reviewer read the source proofs and code, then authored new Python
and C++ checks. The two archive hashes and all members are recorded in
SOURCE_PROVENANCE.json. All 39 Phase31 and 16 bank-v18 internal manifest
entries match their recorded SHA256 values.

## Phase31: complete five-generator exclusions at N4 and N8

The seven-quadratic 3-by-4 projective-window argument is valid. Each
quadratic is a necessary 2-by-2 ratio-minor equation for two-sided
diagonal equivalence after the selected ordered row/column mapping.
Multiplying seven quadrics by five variables gives 35 cubics. If their
35-by-35 coefficient matrix has full rank, their span contains every
coordinate cube, so their common projective zero set is empty.

Seven is minimal for this specific degree-three, linear-multiplier
spanning certificate: h quadratic relations supply at most 5h cubic
rows, while the cubic space has dimension 35. This is not a lower bound
on all possible proof methods or on Fourier algorithms.

The Segre dimension discussion also checks. The projective rank-one
r-by-c variety has codimension (r-1)(c-1). A projective five-generator
3-by-3 window cannot be empty by that method, whereas 3-by-4 has room
for an exclusion. If the coefficient map loses rank, its projective
kernel itself gives common zeros of the minors; that does not rescue a
3-by-3 empty-set certificate.

### Independent numerical-algebraic replay

The reviewer reconstructed the two outer mixers, the Fourier target,
and all five middle generators from previously sealed explicit cycle,
gauge-exponent, and rational-coupling data. The fifth alpha=1/13 term
was already explicitly specified in the preceding five-generator
dimension controls. All six matrices match each new binary input
byte-for-byte at N=4,8,16. Outer inverses, all target entries, all
denominators, and primitive root orders were checked in the exact field.

A newly authored C++ program uses unordered degree-two monomial pairs,
degree-three index multisets, and independent Gaussian elimination.
It rechecks the exact seven minors, not the uploaded executable.

- N4: all 576 ordered 3-by-4 mappings have rank 35.
- N8: all 564,480 mappings have rank 35.
- N16: the same 100,000 distinct sampled indices have rank 35. Their
  exact Random(310031) sample sequence was independently reproduced.
  The total universe is 146,764,800; this is not exhaustive.
- The independently reconstructed planted N8 target has rank 34 at
  the correct mapping, case 9682.

All four output rank streams match the supplied bytes exactly. In
particular the independently regenerated exhaustive N8 hash is
81b6cca8a880659e2ca3583bd0f145914fdb8ba9af5973024df010c5f7cb4dc3.

Because the rational/cyclotomic input has good reduction modulo
998244353 with the verified primitive root, nonzero modular minors lift
to nonzero characteristic-zero minors. Exhausting ordered mappings
covers the restriction of every full pair of internal permutations.
Thus the N4 and N8 exclusions cover arbitrary complex projective
middle coefficients, both internal permutations, and invertible masks
for precisely these fixed outer mixers and five seeded generators.

### Auxiliary results

A separate newly authored checker also reproduces:

- Six generators, N4: all 576 windows have cubic rank 56.
- Six generators, N8 and N16: 24 sampled windows each have rank 56.
- Seven generators, N8 and N16: three sampled 3-by-5 windows each have
  cubic rank 84.

The sampled larger cases remain samples. Independently implemented
cyclic application of the five-term middle pencil matches dense
application on every basis vector and two additional vectors at
N4,N8,N16. Its O(N) supplied-coefficient application is valid, but the
audited pencil is excluded as the requested Fourier middle matrix.
Dense feasibility checks and coefficient generation are additional
work; no Fourier execution cost is hidden inside this test.

## Bank-v18: a valid prime-length sum obstruction

The repeated-halving separation lemma is sound. Starting with equal
lower/upper halves in one total order, each new order admits an
orientation retaining at least ceil(m/2) points on each side. Earlier
separations survive restriction and simultaneous side reversal. Hence
t orders admit a simultaneously separated rectangle of side at least
floor(N/2^t).

On such a rectangle, a cyclic scalar Green kernel has a fixed wrap
choice and rank at most one. At alpha=0 it is zero because the row and
column sets are disjoint. Left/right diagonal gauges preserve the rank
bound. A sum of t terms therefore has rectangle rank at most t.

For complex Fourier matrices of prime order, every square minor is
nonzero. This classical ingredient also follows from the sharp prime
cyclic uncertainty inequality in Terence Tao's primary paper,
[An uncertainty principle for cyclic groups of prime order](https://arxiv.org/abs/math/0308286):
a singular k-by-k minor would produce a nonzero vector supported on at
most k columns whose transform vanishes on k rows, contradicting the
support-sum lower bound N+1. No novelty claim is made for this input.

Therefore a prime-length monomial Fourier matrix represented as a sum
of t independently ordered, diagonally gauged Hamiltonian Green
resolvents must satisfy

floor(N/2^t)<=t, equivalently N<2^t(t+1).

This yields t>=log2(N)-log2(log2(N))-O(1). It precludes a constant
or sublogarithmic bank over unbounded prime lengths. A literal program
that separately evaluates every O(N) term consequently costs
Omega(N log N). It does not lower-bound a genuinely joint evaluator.

### Independently reproduced checks

The reviewer independently regenerated the cycles, gauges, couplings,
simultaneously separated sets, and modular eliminations. All seven
certificate records for t=2,...,8 match exactly, including Fourier
determinants, individual ranks, bank rank, field moduli, and set sizes.
The largest instance is N=2309 with eight terms and a separated
13-by-13 rectangle: bank rank 8 versus Fourier rank 13.

All 40,320 second orders at N=8 were independently exhausted with the
first order fixed. The minimum retained side is 2 and the full size
histogram matches. The three bounded-cycle controls at N=109,257,1297
also reproduce exactly.

These finite fields verify the recorded examples only. The all-prime
complex theorem uses the classical full-spark property, not an
extrapolation from selected modular Fourier minors.

### Necessary wording for the bounded-cycle extension

The common-cycle-cell argument is valid and gives

floor(N/(2^t product(c_r)))<=t.

Its theorem must continue to assume prime complex Fourier length, as
in the preceding section. Each resolvent must exist on every one of
its cycles: 1-alpha_r^L!=0 for each actual cycle length L. A single
condition alpha_r^N!=1 is not sufficient for arbitrary multi-cycle
permutations. These are explicit guard clarifications, not a new
extension to composite Fourier lengths or singular resolvents.

## Relationship to the current construction work

The new Phase31 theorem fixes its outer mixers and allows five middle
generators plus arbitrary internal permutations. The newly sealed N4
fixed-pole theorem instead varies all three two-term couplings but
fixes the internal permutations and poles 1/4,1/5. Neither scope should
be silently substituted for the other.

Bank-v18 is a theorem about sums of single Green terms at prime
Fourier lengths. The current candidate is a product of Green-sum
stages at dyadic lengths, with variable poles and later root-free
weighted-cycle enlargements. Expanding a product does not turn each
summand into one of the resolvents in bank-v18. Moreover composite
Fourier matrices do not have the required all-minors property. Thus
bank-v18 does not exclude the current three-stage product direction.

The root-free family also permits zero wrap holonomy; those broken
cycle limits require their own stated branch and cannot automatically
be identified with a diagonally gauged nonzero scalar-coupling cycle.

The useful lessons are concrete: independent O(N) scans do not by
themselves produce a Fourier identity; source-window rank failure is
only a necessary local signal; and any positive continuation needs
global mask/twiddle compatibility with a charged coefficient rule.
The new operator-separation-rank mask gate uses a different contiguous
tensor-coordinate argument for products and must be reviewed under its
own assumptions. None of these results is a general FFT lower bound.

## Reproduction

Run only the newly authored review scripts and compile only
independent_rectangular_audit.cpp. The uploaded source directories are
read as proof/code text and data. REPRODUCE.md gives the complete
independent replay commands. Original archives, explicit family data,
rebuilt inputs, generated rank streams, checker outputs, and hashes
are retained in the sealed checkpoint.
