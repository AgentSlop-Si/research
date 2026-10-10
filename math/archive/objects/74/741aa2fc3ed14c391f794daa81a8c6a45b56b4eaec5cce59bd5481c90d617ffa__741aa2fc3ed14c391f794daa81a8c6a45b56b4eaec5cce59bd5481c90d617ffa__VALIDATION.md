# Phase 25 validation (2026-10-09)

**Status:** Tests passed in this session. This is not independent external verification or peer review.

## Freshly rerun tests

- **21 Phase 25 tests:** `python -m unittest discover -s tests -v` in this directory. They cover the general affine-run formula, all odd slopes and all cyclic strides at `N=16,32,64,128`, commutator ranks, finite-field cyclic solves and their inverses, exact 4-track banded LU + Woodbury inverses through `N=1024`, exact hidden rank-five blocks, and a separate NumPy check of the Fourier singular-value approximation lower bound.
- **7 Phase 24 tests:** rerun successfully from the original adjacent `fft_green_phase24_ordering_defect` directory.
- **24 Phase 23 tests:** rerun successfully from the original adjacent `fft_green_phase23_real_resolvent` directory.
- **52 tests newly rerun across Phases 23–25** in total. Earlier Phase 12–22 test results are preserved in nested archives and are **not** represented here as freshly rerun.
- `audit.py`: independent iterative radix-two modular FFT compared all Fourier outputs for 2 different two-run orders at `N=16,64,256,1024,4096,16384`, for three nodes per order (`z=0`, an Nth root, and a nonroot sample), totaling **36 exact full-vector comparisons**. The twisted Green sum forward/inverse identity was also audited at every one of those sizes, including `N=16384`.
- Exact finite-field dense submatrix rank controls pass through `N=128`; numerical spectral condition checks through `N=64` support the separate analytic uniform bound.

## Claims explicitly not made

- No general `O(N)` or `o(N log N)` Fourier transform is demonstrated.
- No integer-multiplication bit-complexity improvement is demonstrated.
- The finite-field test data do not guarantee floating-point numerical stability for near-resonant complex parameters.
- The fixed-parameter twisted sum's **full natural cut rank** is a finite-instance observation; its **rank-five hidden balanced cut** is an all-size theorem.

## Reproduce

```
cd fft_green_phase25_affine_order
python -m unittest discover -s tests -v
python audit.py
sha256sum -c SHA256SUMS.txt
```
