# Phase 42 verification ledger

**Date:** October 10, 2026.

## Current phase

`python -m unittest -v tests_phase42`: **9 tests passed**. These include:

- Exact real three-row Jacobian certificates in both split primes at N=8,16,32,64; ranks `2N+1` and two-row ranks `2N-2`.
- Exact two-stage three-row product certificates in both split primes; ranks `4(N-1)` at N=8,16,32,64.
- Independent complex finite differences for the product Jacobian, max relative error below `7e-10` at N=8,16.
- Complete C++ integer-signature audit of all `10,668,000` unordered 4-row subsets at N=128 with **zero** missing collisions, plus counterexamples to overgeneralization at N=16,32,64.
- Finite-field Green-sum rank-3 versus Fourier-minor rank-4 controls in both primes at N=32,64,128.
- Finite-field Green-product rank-4 escape, with **both** Fourier Weyl identities failing in all tested coordinates at N=32,64,128, alongside independently implemented reference FFT controls that satisfy both equations.
- Conditional three-row signature obstruction checks for the Phase41 graph/phase samples at N=16,32,64,128; all realized projective signature classes have nonzero cofactor-phase discrepancy witnesses and no modular singular exceptions.

**Independent exact fields:** `998244353`, `2013265921`.

## Inherited suite

The original Phase41 `tests_phase41.py` was independently rerun from its actual extracted archive: **11 tests passed**. They were not inferred from historical logs.

## Exhaustive counts (pure integers)

| N | Four-row subsets | Collision found | No collision | Mean columns checked |
|---:|---:|---:|---:|---:|
| 16 | 1,820 | 268 | 1,552 | 15.54 |
| 32 | 35,960 | 32,273 | 3,687 | 19.20 |
| 64 | 635,376 | 634,951 | 425 | 17.30 |
| 128 | 10,668,000 | 10,668,000 | 0 | 15.49 |

Because all four-row subsets pass at N=128, the fixed graph family is excluded for arbitrary *external* monomial equivalence and arbitrary complex edge gains. No corresponding blanket statement is made at N=16,32,64.

## Completeness and boundaries

- Verified positive control: a product of Green sums escapes the additive 4x4 rank obstruction. The product **does not** meet the exact DFT Weyl equations.
- Exact rank certificates and conditional signatures support a local *differential* result, not a full FFT factorization.
- The uniform `N<=q(q+1)^q` theorem follows algebraically for the stated class. There is no general-input FFT complexity upper bound in this package.
- Offline C++ verification, input-independent preprocessing, and parameter discovery have not been mistaken for free online arithmetic.

## Fresh-extraction note

The new Phase 42 test suite passed from a clean extraction (9 tests). A combined `RUN.sh historical` attempt was interrupted during the optional inherited-suite step; the older Phase 41 ZIP was then extracted independently and its **11 tests passed** in a separate fresh process. After regeneration the Phase 42 manifest and ZIP were rebuilt, and the final file checks were repeated. The interruption did not affect the nine current-phase results.
