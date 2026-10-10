# START HERE: Phase 27 — Non-affine Green orderings and Fourier phase recovery

**Date:** October 10, 2026

Main research package: `fft_green_phase27_nonaffine_phase_recovery/`.

- `THEOREM.md` — full proofs: all-affine rank gap for random Hamiltonian cycles, exact dense rank-two trap, integer expansion certificates, generic high-cut-rank Green mixer, phase failure, and four-probe Fourier gauge reconstruction.
- `CHECKPOINT.md` — what is established and where Phase 28 starts.
- `RUN.md`, `VALIDATION.md` — standalone Python commands, current and inherited tests.
- `audit.json` — exact finite-instance evidence; its spectral N=256 certificate verifies all balanced graph cuts through Sylvester positivity, not sampled cuts.
- `previous_full_phase26_checkpoint.zip` — complete Phase 12–26 lineage, nested, with source proofs and code.

**Research status:** no arbitrary-input `o(N log N)` FFT. The non-affine Hamiltonian Green stage is mathematically strong as a mixer but fails Fourier projective phase constraints. The main new synthesis tool recovers Fourier permutations and diagonal gauges using two forward columns and two transpose rows, *after* a primitive pair is found, with a conventional O(N log N) reference check.

Use the Phase 27 code to test independently ordered, **complex internally gauged Green sums/products** against projective Fourier normal form and the exact Weyl equations. Do not repeat the affine-run/collision/hidden-cut shortcuts rejected in earlier phases.
