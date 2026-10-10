# Phase 23 fully charged field-operation ledger

In each method, every counted addition, multiplication and inversion costs one unit. The FFT reference, Phase 22, and Phase 23 share the same preinitialized root table and Green matrices. The ledger includes residual preparation, probes, interpolation, candidate certification, forcing decoding, Green solve and any fallback. It excludes root/field construction and does not measure bit complexity or numerical stability.

## Two unknown graph filters and two unknown defects (structured inputs)

| N | Phase 22 | Phase 23 | Full Bluestein/Green | Saving vs Phase 22 | Saving vs baseline |
|---:|---:|---:|---:|---:|---:|
| 1,024 | 182,464 | 147,437 | 124,546 | 19.20% | -18.38% |
| 2,048 | 275,187 | 210,464 | 266,925 | 23.52% | 21.15% |
| 4,096 | 456,905 | 332,790 | 570,070 | 27.16% | 41.62% |
| 8,192 | 816,792 | 573,893 | 1,213,181 | 29.74% | 52.70% |
| 16,384 | 1,533,180 | 1,052,713 | 2,573,090 | 31.34% | 59.09% |
| 32,768 | 2,962,215 | 2,006,612 | 5,440,325 | 32.26% | 63.12% |

## Generic random inputs (discovery fails, exact FFT fallback)

| N | Phase 22 | Phase 23 | Full FFT | Phase 23 overhead over baseline |
|---:|---:|---:|---:|---:|
| 1,024 | 264,231 | 229,349 | 124,546 | 84.15% |
| 2,048 | 459,303 | 394,725 | 266,925 | 47.88% |
| 4,096 | 864,293 | 740,323 | 570,070 | 29.86% |
| 8,192 | 1,707,553 | 1,464,799 | 1,213,181 | 20.74% |
| 16,384 | 3,464,219 | 2,983,897 | 2,573,090 | 15.97% |
| 32,768 | 7,121,427 | 6,165,969 | 5,440,325 | 13.34% |

## Proof-driven per-stage savings

- For fixed support budget `s`, adjacent `(s+1) x (s+1)` Hankel pencils require only `2s+2` exact Fourier samples, not `4s`.
- Phase 22 generated each frequency separately: `4s*3N=12sN` sample field operations (counting multiplications and additions).
- Phase 23 shared prefix: `m=2s+2`, `(2m-1)N=(4s+3)N` sample field operations; at `s=4`, from `48N` to `19N`.
- The joint-pencil compiler makes the two Hankel windows from the same `(2s+2)` precomputed values per parameter sample. It returns exactly the same resultant as the independent-pencils compiler on 75 tested cases.
- Output correctness comes from a complete cyclic identity and spectral invertibility certificate, followed by an exact Bluestein fallback if no candidate passes. Short prefixes are never accepted as full proof.

## Exact savings decomposition in this benchmark

Across all six lengths, the difference between Phase 22 and Phase 23 is exactly `29*N + 5,331` counted field operations on the selected structured family, and exactly `29*N + 5,186` on the tested generic-input fallback family. The `29*N` term is forced by the probe change (`48*N -> 19*N`), while the additional constant comes from the joint Hankel-pencil implementation and minor branch-specific counts. These identities were checked against each raw benchmark record, not curve-fitted to an extrapolation. They are **not universal formulas for every possible candidate arrangement**.

## Limits

This is a **structured-input** certified acceleration only. On generic inputs the candidate family fails the trace sieve and Phase 23 still executes the ordinary FFT; positive discovery overhead remains. Only a field-arithmetic proxy is reported. Python wall times in `PHASE23_BENCHMARK.json` are supplementary implementation diagnostics, not cross-language or mathematical complexity evidence.
