# FFT Green research — START HERE (Phase 36)

**Date:** October 10, 2026  
**Goal:** Seek an exact general-input faster-than-`N log N` Fourier method using genuinely reusable noncommuting Green graph operations, accounting for all arithmetic, preprocessing, memory and precision. **Not achieved yet.**

Open the `fft_green_phase36_two_mask/` folder, read `CHECKPOINT.md` and `THEOREM.md`, and run the commands in `RUN.md`.

Phase 36 results:

1. Two positive middle masks can always calibrate the first Fourier row and column for positive bi-regular Green triples. Matrix-free Sinkhorn processing uses `O(N)` arithmetic per iteration; the explicit near-uniform cyclic Green bridge has N-independent contraction.
2. All two-mask circuits with **positive real middle B** and sufficiently **nearidentity outer A,C** have a proved nonzero **spectral-operator-norm Fourier approximation floor**, even with completely arbitrary complex masks and internal permutations. The explicit eta=1/100 outer Green construction has a floor tending to approximately `0.639505`.
3. For general complex middle B, nearidentity outers force the *entrywise phase-matrix rank* of B to be at least ~`0.993199 N` if exact Fourier equality is to hold. This is necessary but not sufficient.
4. A single `O(N)` complex cyclic Green solve may have **full** phase rank yet just 2–3 distinct `2x2` cross-ratio values, whereas Fourier has `N` values. Stronger phase coherence is necessary; rank and dense mixing alone fail.
5. Exact `Q(i)` projective non-reality certificate at N=4, finite-size spectral controls and 65536-point first-cross calibration are reproducible. The entire prior Phase 35 and earlier history is nested in `fft_green_phase36_two_mask/previous_full_phase35_checkpoint.zip`.

**Phase 37 target:** Create and verify a genuinely complex, noncommuting internal Green network which passes Fourier projective cross-ratio tests and both exact Weyl identities, rather than adding more positive or gauge-removable phases. Account for every operation and bit of precision. Avoid repeating additive fixed-q constructions and conventional butterfly optimizations.
