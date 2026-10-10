# FFT RESEARCH — START HERE: PHASE 15

**Status:** Phase 15 exact residual compression; **no** new sub-`N log N` Fourier algorithm. The entire Phase 14/13/12 history is embedded as `previous_full_phase14_checkpoint.zip` in the full archive.

## What we established

1. The Galois residual `A` from Phase 14 has `O(N log B)` application instead of naive sparse `Theta(N B (1+log(N/B)))`, where `N=BL`, `B>=sqrt N` for the single-mask factorization.
2. Specifically `A=R (I_L tensor F_B) P`, with `R` a frequency-folding *O(N)*-work reversible network. `R R* = diag(L/d)` (each output's orbit length is d), and the normalized R is unitary.
3. Implementing the entire transform still requires **exactly `(N/2) log2 N` radix-2 butterflies**, by an analytic count. No asymptotic gain; optimizing R alone cannot help.
4. A product of t *pure* inverse-sparse Green stages with bounded inverse row sparsity s needs `t >= log_s N`, regardless of intermediate permutation or phase masks. This does not exclude sums of resolvents.

## Next genuine open research gate

Look for a **cross-bank Green/Haar reuse identity** that fuses both costly Fourier banks: the L B-point transforms and the orbitwise transforms. Demand exact Weyl covariance, Galois covariance, explicit charged work and an all-N statement. The new Phase 15 executor is the reproducible reference and countercontrol.

## Files to open

- `fft_green_phase15_folding/THEOREM.md` — full statement and proofs.
- `fft_green_phase15_folding/CHECKPOINT.md` — continuity and restrictions.
- `fft_green_phase15_folding/phase15_executor.py` — exact modular residual+DFT engine.
- `fft_green_phase15_folding/haar_coherence.py` — exact inverse and O(N) wavelet folding.
- `fft_green_phase15_folding/tests/test_phase15.py` — checks.
- `previous_full_phase14_checkpoint.zip` — full preceding chain.

No data-dependent collision assumptions are needed for correctness. No empirical simulation is presented as a proof of asymptotic speedup.
