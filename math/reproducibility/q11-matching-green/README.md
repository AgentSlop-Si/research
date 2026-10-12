# Q11 matching Green reproducibility supplement

This self-contained supplement reruns exact finite-field controls for the
accepted Q11 matching Green construction. It includes runnable Python, a
deterministic expected-results certificate, and executable mutation tests.
It needs no source archives, third-party packages, account access, or network
connection. It is a minimal repository supplement, not the complete research
archive or a new independent mathematical acceptance review.

The accepted theorem concerns the full positive-chirp inverse for
q = 483^m, m >= 1, and N = 5q^2. Its 20q+1 permitted additive Green branches
have O(N) compressed exact-field preparation and Theta(Nq) = Theta(N^1.5)
direct application. That is slower than the accepted two-DFT O(N log N)
evaluator. No FFT speedup, bit-cost advantage, stability result, optimality,
or historical-novelty claim is made.

## Run from a clean copy

Use Python 3.10 or later, with only its standard library. From this directory:

```sh
python3 -B -m unittest -v
python3 -B verifier.py --verify-manifest --check expected_results.json
python3 -B verifier.py --verify-manifest --large --check expected_results.json
```

The first command runs 13 regression and mutation tests. The second runs all
small controls. The third additionally runs the limited q=483 checks described
below. Successful verifier runs print JSON with status ALL_ASSERTIONS_PASS;
an assertion, guard failure, manifest mismatch, or certificate mismatch exits
with a nonzero status. Progress goes to standard error. JSON goes to standard
output and may be redirected to a new file. Supplied files are never rewritten.
Do not use Python's -O flag or PYTHONOPTIMIZE: checks use assertions, and the
command refuses optimized execution.

The large option allocates four million-scale tables and other diagnostic
data. Its Python memory use is substantially larger than the raw field-slot
count. The small verifier deliberately forms dense matrices; it is a correctness
oracle, not a memory or runtime benchmark of the streaming algorithm.

## What is actually checked

Small controls use q=1,1,3,3,7,11, with root powers 1,2 at q=1 and q=3:

- All 430,150 assembled matrix entries across these controls, largest N=605
- Both defining inverse products through N=245, totaling 128,250 entries
- 173,000 branch recurrence coordinate checks, with Hamiltonian-cycle and
  zero-holonomy checks
- 124 paid vector applications, including every basis vector at N=5 and N=45
- Instrumented preparation and application operation counts
- Complete matching assignments for s=5,15,35,55

These small q values are outside the frozen q=483^m family. They are exact
algebra and implementation controls, not instances of that theorem.

With --large, q=483, N=1,166,445, p=18,663,121, and omega=65,536:

- All 2,914,905 unordered matching pairs at s=2,415
- Every one of the 1,166,445 diagonal calibrations
- The complete length-N Gauss sum
- 6,515 selected coefficient checks, including 2,415 same-class samples

The large run does **not** assemble the full N-by-N matrix or execute the
9,661-branch full transform. Its application counts are formula evaluations,
not measured execution counts. Finite-field checks do not prove the
infinite-family theorem over Q(omega); the linked accepted report contains
that argument. Fixed seeded samples are reproducible coverage, not a
probabilistic correctness guarantee.

The separate tests actually alter a live endpoint, omit the calibration,
remove a zero boundary, and misplace reverse boundaries, then detect changed
matrix or vector results. They also reject imprimitive roots, composite
moduli, unit holonomy, and non-Hamiltonian permutations, and verify the paid
diagonal as its own legal Green branch.

## Target and permitted representation

Let h=(N+1)/2, F_ij=omega^(ij), A_ii=omega^(h i^2), and
B=(F^(-1)+A)^(-1). Put eta=omega^(q^4), G=q(1+2eta^2+2eta^3),
c=NG, and rho=(1+c)^(-1). The checked entry identity is

```text
B_ij = rho [omega^(ij) - G omega^(-h(i+j)^2)
            + c omega^(-h i^2) delta_ij].
```

Each branch is L_b(I-W_b)^(-1)R_b with diagonal endpoints, allowed zero
endpoint masks, a single Hamiltonian structural cycle on the original
coordinates, and (W_b x)_i=w_i x_(sigma_b(i)). Zero edge weights are allowed.
The inverse guard is 1-product(w_i) != 0. No unmatched endpoint permutations
or free diagonal terms are introduced.

Set s=5q and S_a={a+su:0<=u<q}. Since s^2=5N, each S_a-by-S_b block of
each of the two kernel terms has rank one. Round t pairs {t+d,t-d} modulo s
and leaves S_t single. Zero-separated paths pack one forward and one reverse
branch per kernel mode. A final W=0 branch removes the duplicated singleton
diagonal and inserts the target diagonal. The count is 4s+1=20q+1.

## Cost convention

Preparation builds P[k]=omega^k, U[k]=rho P[k], V[k]=-rho G P[k], and D[i].
The code counts every multiplication and addition/subtraction in these four
table loops: 4N-1 multiplications and 2N additions. Scalar setup, root
certification, Gauss-sum validation, and other diagnostic work are separate
and are not silently included in that ledger. Endpoint evaluation in the
paid application is a table lookup with modular integer addressing.

For the literal application schedule, the measured small-instance counts are

```text
multiplications = N(4s+5)
additions       = 2(s+1)(2N-s).
```

For q=483 those formulas give 11,273,690,925 multiplications and
11,260,855,200 additions. Four-table preparation gives 4,665,779
multiplications and 2,332,890 additions. Routing, addressing, endpoint
visits, and expanded descriptors are not free: their orders are O(Ns),
with Theta(Ns) expanded writes/storage when materialized. The streaming
algorithm's field storage is O(N); the cyclotomic field degree grows with N.
These are field-operation claims, not unit-bit-cost or Python timing claims.

## Sources and boundaries

- [Accepted construction and full proof](../../reviewed_rounds/2026-10-12-green-ranking-slices/q11-matching-green-baseline.md)
- [Bounded prior-work comparison](../../reviewed_rounds/2026-10-12-prime-sampler-attribution/q11-matching-prior-comparison.md)
- [Independent attribution precision addendum](../../reviewed_rounds/2026-10-12-prime-sampler-attribution/q11-matching-prior-addendum.md)
- [Credits and licensing status](NOTICE.md)
- [Machine-readable source pins and changes](provenance.json)

The broader Q11 problem remains open. The fixed-field impossibility and
ordinary-order-only lower bound are unchanged; reordered zero-edge branches
do not establish arbitrary-cycle optimality. The accepted five-dimensional
minimum-three result is preserved. No all-length or negative-family
extension follows. Classical mechanisms and unresolved assembly priority
are credited in NOTICE.md.

FILE_MANIFEST.json hashes every other payload file; it intentionally excludes
itself. Its integrity must be established from the surrounding trusted
repository commit or independently recorded publication manifest. The file
hashes detect byte changes; they are not digital signatures or mathematical
proofs. Original accepted artifacts were not altered to create this derivative.

This package is public-safe in content. Repository access and licensing are
separate matters: no visibility change or open-source license is supplied.
