# FFT research chain — START HERE (Phase 17, October 9, 2026)

Read `fft_green_phase17_nonunitary_sum/CHECKPOINT.md`, then `fft_green_phase17_nonunitary_sum/THEOREM.md`.

**Goal**: Exact faster-than-`N log N` FFT via the user's own Green/graph computation-sharing line; do not merely emulate CrocSwap or OpenAI; account for every operation and memory access. **This goal has NOT been met.**

**New result**: Even nonunitary, arbitrarily ill-conditioned and NONCOMMUTING permuted banded Green inverses have an all-size SUM obstruction: for q terms and sum of half-bandwidths W, `floor(N/2^q)^2 <= W*N` is necessary for equality to normalized DFT. When `2^q | N`, this reads `N<=4^q W`; q tridiagonal terms need q=Ω(log N). Stronger: operator-norm approximation gap `sqrt((m²/N-W)/(m-W))` with `m=floor(N/2^q)` when positive. Proof combines a new balanced two-group selection across arbitrary orders, classical inverse-banded nullity rank identity, and flat-unitary Frobenius/spectral norms. No Chebotarev/prime-length assumption is needed. Finite field controls pass.

**Surviving direction**: A product of two noncommuting Green sums `(G1+G2)(G3+G4)` can have full crosscut rank and O(N) application, so SUM theorem cannot rule it out. Current product controls FAIL `MZ=DM` (full-rank defects). Phase 18 should attack exact Fourier covariance for these products or more general shared-state DAGs, not just rank or entropy.

**Archive**: `fft_green_research_phase17_2026-10-09.zip`, containing the previous full Phase16 checkpoint and entire earlier history as nested archives.

**Current verification**: Rerun Phase17 tests and the Phase16 suite. No new sub-NlogN FFT claim; no peer-reviewed originality claim.
