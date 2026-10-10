# Phase 37 — start here / chain recovery

**Main archive:** `fft_green_research_phase37_2026-10-10.zip`

1. Read `fft_green_phase37_curvature/CHECKPOINT.md` for the exact starting point, assumptions, and Phase 38 research gate.
2. Read `THEOREM.md` for the all-length exponent-curvature distinction and the two-mask, all-complex-coupling exclusion at the six certified sizes.
3. Run `python -m unittest -v tests_phase37`, then `python verify_certificates.py --regenerate`.
4. Do not reinterpret **dense complex phases**, **maximal phase-matrix rank**, or **green graph expansion** as exact Fourier covariance. Both Weyl equations remain final gates.

**Status:** No worst-case `o(N log N)` FFT. New exact phase-curvature obstruction for primitive-holonomy Green kernels; exact two-plaquette complex-coupling exclusions for a seeded noncommuting six-Green, two-internal-mask circuit at `N=4..128`. Earlier Phase 12–36 history nested and preserved.
