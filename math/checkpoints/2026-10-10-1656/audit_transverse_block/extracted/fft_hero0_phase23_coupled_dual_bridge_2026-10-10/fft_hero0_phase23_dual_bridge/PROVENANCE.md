# Provenance, attribution and qualification

**Checkpoint:** 2026-10-10, Hero #0 Phase 23.

- Baseline: `fft_hero0_phase22_transverse_bridge_2026-10-10.zip`, carried forward verbatim as `prior_phase22_bundle.zip`. Its internal archive contains Phase21 and earlier research. Its 88 archived Phase19–22 tests were rerun in this session and passed.
- New files: `phase23_dual_phase.py`, `test_phase23.py`, `audit_phase23.py`, `THEOREMS.md`, `RESULTS.json`, `CHAIN_HANDOFF.md` and this provenance.
- Method: derived fully coupled off-rook tensor decomposition, applied classical Schur-product rank inequality and exact singular spectra of punctured Fourier matrices, and verified characteristic-zero proofs with finite-field consistency tests. Separately proved trigonometric imaginary-phase rank and counted its effective factor supports in both orientations.
- Numerical tests do not imply external mathematical novelty, and finite-field certificates are not replacements for the characteristic-zero proofs. Matrices with sufficiently high transverse rank are NOT excluded by the results.
- Field models: The rank-product result holds over any field with the requisite primitive roots (and nonzero N); norm/imaginary claims are stated over C. GF(65537) computational tests use primitive roots for the tested power-of-two lengths.
- Prior-art search found the Zheng–Riccietti–Gribonval 2023 butterfly sparse matrix factorization work and companion two-layer identifiability paper. No comprehensive literature priority audit was performed.
- No universal exact O(N) FFT or general FFT lower bound has been proved.
- The final regression includes 17 new tests (including genuine complex cyclic Green solver comparisons) plus 88 inherited methods, for **105 passed**. This is a reproducibility check, not peer review.
