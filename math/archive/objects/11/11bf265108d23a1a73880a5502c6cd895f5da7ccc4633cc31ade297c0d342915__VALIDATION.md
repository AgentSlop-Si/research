# Phase 41 validation record

All numerical target-fit files are explicitly labelled **experimental**; their small residuals do not establish exact Fourier identities.

- The exact proof of Theorem 41.1 is self-contained in `THEOREM.md`; it does not depend on numerical tests.
- Split-prime exact Jacobian computations use the same underlying rational-Gaussian unit gains and recorded cycle orders for both primes, including actual nonzero square determinant witnesses.
- The three-cycle local-control result applies to explicit graph orders at N=8,16,32,64, not all graph orders.
- The two-cycle non-unit-gain complex Jacobian result applies to explicit graph orders through N=128.
- The first-two-row fits at N=8,16,32 are approximate, and all fail the next Fourier row. The high-precision N=8,16 Newton traces are **not interval-certified**.

Fresh archive validation results follow in the top-level `ARCHIVE_VALIDATION.txt`.

## Fresh-extraction result

On October 10, 2026, 11 Phase 41 regression tests passed from a clean ZIP extraction. The exact rational-Gaussian split-prime rank witnesses regenerated, both numerical full-row comparison suites reproduced, every manifest hash matched, and the nested Phase 40 ZIP passed integrity verification. In the original working directory, Phase 40's 16 regression tests passed separately; the full nested Phase 12-39 history was not rerun in the Phase 41 final audit.
