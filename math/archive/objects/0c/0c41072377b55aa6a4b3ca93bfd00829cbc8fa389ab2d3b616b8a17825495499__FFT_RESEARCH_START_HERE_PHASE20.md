# Start here — FFT/Green research Phase 20, October 9, 2026

This project has evolved through Phases 12–20 in search of a sub-`N log N` exact Fourier transform and, eventually, faster arbitrary-precision multiplication. **No such new algorithm has been established in our work.** The present branch is independent from CrocSwap/Swapnil-jain's integer-multiplication approach.

## New checkpoint and tools

The folder `fft_green_phase20_weyl_shared_state/` contains the new theorems, exact code and tests:

1. `CHECKPOINT.md` explains what was proved and the next testable research task.
2. `THEOREM.md` gives the complete Weyl characterization, sharp norm gap, two-column projective phase obstruction, real one-mask rigidity, and restricted Green lower bounds.
3. `weyl_gate.py` validates exact finite-field Fourier intertwiners using `1+3h` black-box calls for `h` independent trials, instead of dense inversion.
4. `projective_gate.py` uses just **two black-box calls** to reject every possible outer phase/permutation gauge when a Fourier cross ratio or column-pair fingerprint fails.
5. `previous_full_phase19_checkpoint.zip` contains all earlier phases, archives and supplied original research.

## Validation and scope

The new Phase 20 deterministic suite contains **74 tests**. The inherited Phase 12–19 chain contains **128 tests**. Re-run the fresh-extraction validator for the combined result. Large sampled, independently permuted **near-resonant** Green products fail the exact Fourier phase gate; this does not exclude *all* parameter choices. The new commutator and mask theorems have explicit restricted hypotheses; do not extend them to arbitrary permuted noncommuting Green sums.

## Critical next question

Can we construct a fixed-degree, constant-number-of-term, near-resonant Green product with **genuinely internal complex phases** that satisfies the complete projective Fourier subgroup fingerprint for all column pairs, then BOTH Weyl intertwiners, for every power-of-two size, with arithmetic work below `N log N` including all preparation and movement?

No sampling, gauge fitting, precomputed Fourier table, or single matrix-density property alone establishes that result.
