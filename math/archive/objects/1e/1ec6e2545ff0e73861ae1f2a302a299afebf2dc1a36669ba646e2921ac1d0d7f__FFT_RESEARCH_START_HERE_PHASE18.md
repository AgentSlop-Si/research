# FFT GRAPH/GREEN RESEARCH — START HERE (PHASE 18)

**Date:** October 9, 2026. **Research status: no `o(N log N)` FFT yet.**

This archive preserves the **complete research chain** from the original nonunitary Green work, through Phases 12–17, and adds Phase 18. It deliberately does **not** switch to the CrocSwap or Swapnil-jain integer-multiplication strategy.

## Read in order
1. `fft_green_phase18_harper_covariance/CHECKPOINT.md` — exactly where the research is and what to do next.
2. `fft_green_phase18_harper_covariance/THEOREM.md` — derivations, scope, known prior art, proofs, operation accounting.
3. `fft_green_phase18_harper_covariance/harper_certificate.py` — exact Fourier polynomial reconstruction from sparse Harper operators and parity, degrees, two zero modes.
4. `fft_green_phase18_harper_covariance/weyl_gate.py` — test arbitrary central diagonal/permutation masks between noncommuting Green sums without exhaustive search.
5. `fft_green_phase18_harper_covariance/dual_intertwiner.py`, `commutant_dimension.py` — exact two sparse intertwiners and commutant characterization.
6. `fft_green_phase18_harper_covariance/previous_full_phase17_checkpoint.zip` — *full original chain*, nested unchanged.

## Phase 18 additions
- A scalar rational function of one commuting cyclic Harper operator cannot produce the DFT for `N` divisible by 4: two distinct Fourier eigenphases occur at Harper eigenvalue zero. The basic degeneracy was already known in the literature.
- A parity-resolved exact polynomial does work: `F=p_+(H)P_+ + p_-(H)P_-` with exact degrees `N/2` and `N/2-2` and `coeff_top(p_+)=1/(2 sqrt(N))`. Its straightforward execution is quadratic, not faster than FFT.
- A single diagonal mask with phases only `±1,±i` suffices algebraically between two **general real orthogonal eigenbasis matrices**, but those matrices still carry `Ω(N log N)` two-coordinate orthogonal-gate complexity.
- The sparse Harper duality identities characterize Fourier up to a 2-dimensional ambiguity, resolvable by one probe vector.
- Exact modular 1/2-cycle invariants rule out *every middle diagonal and permutation mask* for fixed sampled complex-gauged Green-sum outer stages at `N=8,16,32,64`; these are **finite counterexamples only**.

## Run
From `fft_green_phase18_harper_covariance`:

```
OPENBLAS_NUM_THREADS=1 PYTHONPATH=. python -m unittest discover -s tests -v
python harper_certificate.py
python weyl_gate.py
python commutant_dimension.py
python dual_intertwiner.py
OPENBLAS_NUM_THREADS=1 python spectral_basis_control.py
```

**Phase 19 gate:** keep products of independently ordered *noncommuting* Green sums. Target symbolic sparse dual intertwining `MT=VM`, `MV=TM`. Eliminate center diagonal/permutation gauges through the phase invariant first. Verify an actual full DFT with complete operation and memory accounting before claiming a faster algorithm.
