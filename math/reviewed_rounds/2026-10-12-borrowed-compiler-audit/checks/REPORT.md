# Fresh independent borrowed-register compiler check report

12 October 2026 UTC. Publication edition of the completed bounded-check report.

## Verdict

PASS, bounded implementation correctness. A new standard-library-only implementation derived from the mathematical equations reproduces the complete local width-r compiler and passes all exact tests described below. No supplied executable program was imported or run. This result supports the construction's correctness at the tested widths; it makes no historical originality or global runtime claim.

## Main findings

1. Full Fourier basis comparisons pass at widths 1–12, 15, 16, 17, 23, and 32: 181 columns in total. Each column is compared with the literal positive-exponent Fourier formula over a verified prime field. Every transformed column also passes an inverse-word round trip, and the separately normalized strict shear/monomial word passes the same Fourier basis comparison.
2. Every emitted gate is validated for coordinate range, disjointness within its layer, and nonzero scaling. Recursive intermediate and scratch banks are disjoint and chosen solely from the parent block. Every rectangular displacement chunk is independently reconstructed coefficient by coefficient from its three outer products.
3. A full recursive width-16 triangular Toeplitz transform and its inverse pass all 16 basis columns over exact Q(i), plus a dense nonzero input. This uses the actual complex regularizer 1 + sum(lambda * conjugate(lambda)), rather than a finite-field replacement.
4. Actual fixed-C synchronized Fourier slot programs pass all 85 tensor basis columns for coprime axes (2,3), (3,5), (2,3,5), and (2,17). The final case executes a common schedule of 407,017 slots on width 34. It uses prefix-tree monomial and sector adapters and conventional C-tensor butterflies, with no imported fast engine.
5. A separate synchronized width-20 test on coprime axes (4,5) passes every basis column while both local words actively use dirty scratch. Other-axis operations change those entries between a local word's cancellation steps. This directly tests the claimed absence of a cross-axis interference problem.
6. Seven rejection/corruption controls are detected: overlapping gates, an out-of-range coordinate, zero scaling, a self-pair, omitted regularizer correction, a corrupted FFT shear, and a corrupted packing permutation.

## Recursive local circuit counts

| Width | Generalized layers | Strict layers after one final normalization | Scalar data operations |
|---:|---:|---:|---:|
| 16 | 25,035 | 25,035 | 75,568 |
| 17 | 31,293 | 31,309 | 94,133 |
| 23 | 52,863 | 51,741 | 150,359 |
| 32 | 59,211 | 59,211 | 363,104 |

These are this fresh compiler's finite instruction counts, not measured runtime or an independently proven asymptotic bound. The strict count can decrease because normalization removes empty generalized layers. At width 17, the increase demonstrates that mixed disjoint child layers really occur and are handled by a single final split, rather than inserting a factor of two into each recursive recurrence.

A shear costs two scalar data operations, a scaling one, and swaps are counted separately in the JSON. Prepared coefficients and schedule storage are not data registers. The test interpreter copies Python lists and uses additional arrays; only the emitted abstract word has exactly the specified data-coordinate width.

## Additional exact checks

- Five rectangular Toeplitz accumulation shapes, with 51 full basis columns covering source, target, and scratch roles, plus arbitrary nonzero scratch and inverse checks.
- Four nested product shapes, with 51 full basis columns and explicit restoration of every intermediate and FFT scratch coordinate.
- Zero and singular all-ones Toeplitz kernels over Q(i), with 16 basis columns.
- Six-C conversion for shear coefficients 0, 1, and 2−3i, with both basis columns of each exact Q(i) map.
- The three small Fourier tensor cases compare a batched all-basis interpreter with a separate vector-at-a-time interpreter, in addition to the literal tensor Fourier oracle.

## Preparation and model boundaries

Forward compiler scalar preparation is counted separately in [RESULTS.json](RESULTS.json). For example, width 32 uses 48,489 counted field multiplications, 16,431 additions, 49,343 negations, and 28,867 inversions during forward-word preparation, plus 290 candidate-shift checks. The fixed-C compiler has separate preparation counters for each axis. These are arithmetic-operation counts in the chosen exact field; they do not include rational bit complexity and should not be interpreted as a practical cost comparison.

In finite fields, the implementation chooses a scalar avoiding the finite spectral zero set. That is not the complex norm-regularization algorithm. The independent Q(i) checks exercise the actual complex formula at the first recursive width, including singular convolution kernels. This package does not implement arbitrary cyclotomic characteristic-zero fields, so the full recursive Fourier basis tests are modular rather than Q(zeta_16) tests.

The synchronized evaluator uses ordinary O(k 2^k) tensor butterflies and shares adapter preparation across test basis columns. Identity slots may be skipped. Prefix traversal, packing permutations, complete sector coverage, and sector widths are explicitly checked. No claim is made that this evaluator has the imported engine's exponent or that it yields a sub-N-log-N global algorithm.

## Evidence identity and exclusions

The main and supplemental fresh check runs completed successfully. [RESULTS.json](RESULTS.json) and [SUPPLEMENT_RESULTS.json](SUPPLEMENT_RESULTS.json) are unchanged copies of their result records. Source and report hashes are identified in [PROVENANCE.json](../PROVENANCE.json); publication file hashes are in [MANIFEST.json](../MANIFEST.json). The source programs and original run logs are not included in this documentation checkpoint. Their hashes identify preserved evidence but do not provide a self-contained, publicly rerunnable reproduction package.

The authored candidate suite was not rerun. Its separate recorded 455 modular and 10 characteristic-zero positive cases and six negative controls must not be attributed to these fresh executions. The original authored package was statically inspected, including its source-hash bindings and manuscript agreement.

This is finite exact reproduction, not formal verification, a proof for all sizes, validation of a new asymptotic exponent, a rebuilt tensor engine, a CRT/Bluestein implementation, a floating-point stability result, a practical speed comparison, a bit-complexity theorem, or a priority finding. Successful finite reproduction does not establish that the O(log² r) compiler theorem is new.
