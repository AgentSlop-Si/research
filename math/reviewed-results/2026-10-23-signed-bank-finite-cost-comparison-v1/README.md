# Finite N19 signed bank cost comparison

23 October 2026. Accepted finite arithmetic comparison and descriptive recorded warm timings.

## Conclusion

For the accepted N = 19, d = 4, m = 15 fixture with 32 original signed banks, the literal executed-style bank implementation took a final recorded median of 11.3429919375 ms per complete transform. The same-field exact length-64 Bluestein implementation took 177.586699219 microseconds. The bank therefore took 63.8729814079 times as long, about 64 times slower for this implementation and run. The earlier retained run gave a ratio of 69.0335219166. Neither result is a bank-over-FFT speedup.

This is not a universal runtime ratio, optimized-library contest, complex floating-point comparison, hardware or parallel-network latency result, asymptotic improvement, novelty determination, or broader research closure. No new timing run was performed to prepare this deliverable.

## Exact scope and arithmetic

All methods compute the same negative unnormalized transform y[a] = sum(t = 0 to 18) 5^(-a*t) x[t] over the accepted field L = F191[A,B]/(f11(A), B² + 78B + 121), represented by 22 base-field coordinates. The direct coefficients lie in F191, whereas bank intermediates generally require L. The full finite-bank realization and all 361 matrix entries were independently accepted before this comparison.

| Method | L multiplication calls | L add or subtract calls | Scalar / general products on archived mixed input |
|---|---:|---:|---:|
| Direct 19 point DFT | 361 | 342 | 361 / 0 |
| Literal bank executed style | 23,104 | 23,104 | 2,888 / 20,216 |
| Literal bank optimized addition schedule | 23,104 | 22,477 | 2,888 / 20,216 |
| Exact length 64 Bluestein | 486 | 768 | 241 / 245 |

The optimized schedule was actually executed in this comparison, but not in the earlier full-realization acceptance. Its 22,477 additions do not replace that earlier recorded 23,104 add/subtract tally. The difference is 608 input negations and 19 initial zero accumulations; caching signed inverses pays 32 setup negations.

A scalar product uses 22 base-field multiplications in the common kernel; a general extension product uses 746. Thus extension-operation calls are not equal-cost machine operations or timing predictions. The recorded scalar/general splits apply to the archived mixed input, not every vector. Dedicated quadratic/subfield kernels were not implemented. The exact FFT is valid but is not claimed to be optimal.

## Both retained timing runs

Times below are medians of seven retained batch-average times, in microseconds per complete transform.

| Method | Earlier run | Final run | Calls per batch |
|---|---:|---:|---:|
| Direct DFT | 28.663902 | 29.982016 | 4,000 |
| Literal bank executed style | 11,118.4810625 | 11,342.9919375 | 16 |
| Literal bank optimized addition schedule | 11,471.256125 | 12,733.1371875 | 16 |
| Exact Bluestein | 161.059160156 | 177.586699219 | 256 |

These are author-recorded numerical observations, not independently reproduced timings. The environment was shared Linux x86_64, reporting AMD EPYC 9V74 80-Core Processor and GCC 14.2.0. CPU affinity and frequency were not isolated. Methods used unequal batches in fixed order, without randomized order or confidence intervals. Eight untimed equality-validation calls per method were the explicit warmup; no batch was discarded. The same eight cached inputs and all output coordinates were consumed. The volatile output checksum was not recorded, so independently reconstructed expected checksums must not be described as measured checksum observations.

## Cold setup and storage boundaries

The warm measurements include application, input selection, copies, zero-fill, traffic and output-checksum consumption. They exclude frozen-data loading, input generation, coefficient setup, correctness comparisons, compilation and output-file writes. No cold end-to-end speed ratio is established.

Starting from the accepted frozen inverses and raw weights, bank cache preparation records 1,230 L products and 640 L add/subtract calls, plus separately shared q-power preparation. FFT-specific setup records 342 L products and 384 add/subtract calls and pays root search, twiddles, transformed kernel and normalization. Upstream field/root recovery, bank construction and dense validation remain separate costs. The earlier combined approximately 0.427-second construction/validation run is not a warm bank application time; the separately recorded factorization time is approximately 0.009 seconds.

The 608 archived inverse matrices contain 4,828,736 coordinates. Their actual uint8 archive occupies exactly 4,828,736 bytes; representing the same coordinates as 32-bit integers would require 19,314,944 bytes before container overhead. The warm evaluator does not load these matrices. An L element in the benchmark occupies 22 int32 coordinates, not a single machine word. The minimal prepared bank cache uses 1,248 L elements, excluding q/sign data; the comparison retains another 32 inverses to support both schedules.

## Evidence and reproducibility

The retained benchmark source, frozen input file, all eight inputs and complete expected outputs, both raw timing records, sanitizer record, development history, original and clarified reports/manifests, and independent review/check source are inventoried in PUBLIC_MANIFEST.json. TIMING_INVENTORY.json records the compiler flags, method order, batch design, raw values and evidence limits. DOCUMENTARY_LOCATOR_MAP.json inside the evidence archive maps cited scientific locators to the accepted published fixture and nested archives.

The independent reviewer recorded 19,673 checks, including all 3,344 direct-output coordinates, the complete frozen-data projection, branch traversal, exact root and chirp identities, arithmetic/storage formulas and medians from retained records. It did not compile or run the comparison benchmark or independently replay its dynamic scalar/general splits. The sanitizer success and runtime method equalities remain execution records from the comparison author. The full finite-fixture matrix acceptance is inherited rather than re-awarded here.

The first run predates the final addition of a verify-only option. Both raw timing runs are retained; the development log states their arithmetic algorithms are unchanged. A distinct first-run source snapshot and raw compiler stdout/stderr are not present in the accepted package. The final source and reported compiler commands are preserved; this deliverable does not invent missing records.

The scientific source and evidence have not been rerun or modified during packaging. Machine-specific derived benchmark binaries may be omitted only with their exact sizes and hashes retained. Scientific data, source, raw batches, output checks and prior versions must not be omitted.

## Accepted fixture source

The underlying complete finite realization is published at immutable commit b5b43b8e4a1c4384537be668046117c74c98e8e2:

https://github.com/AgentSlop-Si/research/blob/b5b43b8e4a1c4384537be668046117c74c98e8e2/math/reviewed-results/2026-10-23-signed-bank-refined-space-and-finite-realization-v1/FINITE_REPORT.md

Its complete two-part evidence archive has combined SHA-256 71250e6c41a349a8b1a885f8dc51cd658a5afa110cf19236f421798713a36786 and contains the full uint8 inverse archive and its existing source/projection/omission inventory. This comparison is a separate scoped addition; it does not change the earlier finite-realization result.

## Package verification

Concatenate evidence.zip.part001 and evidence.zip.part002, in that order, to recover evidence.zip. The parts and combined archive are hash-bound by PUBLIC_MANIFEST.json. Run python verify_package.py from this directory to check every direct file, part, archive member, nested archive and source projection without running research or timing code. The complete accepted fixture is nested at dependencies/fixture/evidence.zip with its own public manifest.

Only the two machine-specific derived comparison binaries are omitted from this package; their exact sizes and SHA-256 hashes remain in the projection inventory. The nested fixture preserves its prior two binary omissions with their original inventory. All scientific source, data, recorded outputs, both timing arrays and both report versions are retained. The three locator-projected comparison/review files are explicitly mapped; all other comparison/review evidence is byte-exact. Original manifests remain historical original-hash records, not silently regenerated manifests.

The retained independent check source uses original hashes and checks omitted binaries. It is therefore documentary source, not a claim of an unchanged one-command portable scientific replay. The package verifier checks archival integrity only. No previously recorded scientific check or timing result is newly reproduced by that verifier.
