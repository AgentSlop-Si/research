# FFT Green research — Phase 22, chain-safe handoff

**Current status:** No demonstrated new `o(N log N)` FFT. New restricted no-go theorem and two exact synthesis gates; runnable tests and preserved history.

1. Open `fft_green_phase22_gram_gate/CHECKPOINT.md` to resume research.
2. Read `fft_green_phase22_gram_gate/THEOREM.md` for claims and proofs, then `PRIOR_ART.md` for novelty caveats.
3. Execute `python -m unittest discover -s tests -v` in the Phase 22 folder (12 tests); `python audit.py` regenerates `audit.json`.
4. Use `phase22_gram.py` for exact bilinear Gram mask/permutation recovery, or `phase22_parity.py` for the `F=HQC` real covariance construction and verifier.
5. For complete old context, extract `fft_green_phase22_gram_gate/previous_full_phase21_checkpoint.zip` (includes Phases 12–21 plus earlier supplied materials).

**Phase 23 gate:** synthesize the real cosine/sine residual `C` from independently ordered noncommuting Green operators satisfying `CZ=RC`, `Ce0=v` exactly, with an `o(N log N)` cost proof. The sparse generator `R` is not itself a fast executor for the dense `C`.
