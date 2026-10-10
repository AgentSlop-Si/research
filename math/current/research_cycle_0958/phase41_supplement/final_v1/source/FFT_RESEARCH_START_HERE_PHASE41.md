# FFT graph/Green research — Phase 41 continuation

**Start with:** `fft_green_phase41_unit_holonomy/THEOREM.md`, then `CHECKPOINT.md`, `RUN.md`.

**Main exact new theorem:** Two weighted Hamiltonian-cycle Green resolvents with unit-modulus edge gains cannot sum to an externally diagonally/permutationally equivalent DFT for any `N>8`, even if both scalar coefficients are arbitrary complex numbers. Proof is all-size, elementary, and does not rely on spectral conditioning or special graph orders.

**Exact finite-size positive theorems:** Two fixed-strength phase-only cycles have a real Jacobian rank deficit for four complex Fourier row-pair ratios. Three independent unit-phase cycles have full real Jacobian rank for the *entire* N-1-ratio signature of two Fourier rows at N=8,16,32,64. Two cycles with arbitrary complex amplitudes have full complex local rank through N=128. Certificates use two exact finite fields and rational-Gaussian unit weights where applicable.

**Numerical (not exact) construction:** Three unit-phase cycles and separately two complex-amplitude cycles reproduce the first two Fourier rows after external diagonal calibration at N=8,16,32 with ~1e-11 accuracy. The third row and full Fourier equations fail. Offline fitting is expensive, and some instances are poorly conditioned.

**Verdict:** NO new arbitrary-input `o(N log N)` FFT, NO integer multiplication improvement, and NO independently verified publication novelty.

Run `bash RUN.sh`. The prior complete Phase 40 (containing the earlier history) is in `fft_green_phase41_unit_holonomy/previous_full_phase40_checkpoint.zip`.
