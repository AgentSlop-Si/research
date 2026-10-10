# Phase 41: Unit-phase obstruction / three-cycle local escape

This continuation starts with Phase 40's graph-holonomy framework and develops a sharp distinction between unit-modulus **phases** and arbitrary nonzero complex **edge amplitudes**.

## Main result

A sum of **two** independently ordered cyclic Green resolvents whose individual edge gains all have modulus one cannot be made Fourier-equivalent at **any length N>8**, even using arbitrary external row/column complex scalings and permutations and arbitrary complex scalar weights on the two summands. `THEOREM.md` supplies a short complete proof based on the fact that each cycle has at most two row-ratio signatures; after a flat-modulus constraint, the sum has at most eight values per row pair, but Fourier has a row pair with N different values.

The result is a restriction on a **two-resolvent phase-only sum**—not on general FFTs, products of Green sums, non-unit amplitude gains or three summands.

## Constructive controls

* Two unit-phase Green cycles: exact real Jacobian ranks 4,5,6 for 2,3,4 anchored complex ratios (certificates at N=8,16,32; N=64 for k=4). The 4-ratio map is 6-real-dimensional, not 8.
* Three unit-phase Green cycles: exact full real Jacobian rank `2*(N-1)` for **all** two-row Fourier-type projective ratios at N=8,16,32,64, certified with rational Gaussian circle gains and two primes.
* Two cycles with arbitrary nonzero complex gains: exact full complex Jacobian rank `N-1` at N=8..128.
* Direct numerical target search: both latter architectures fit **every** projective ratio of the first two Fourier rows to around 1e-11 at N=8,16,32; **the third row fails**. The search is not a proof of exact solvability.
* An exact elementary Möbius template shows how amplitude asymmetry permits continuously varying unit-circle ratios.

**No algorithm beating O(N log N) has been established.** No independent publication novelty review is complete.

## Files

- `THEOREM.md`: full statements, exact proofs, limitations.
- `phase41_phase_geometry.py`: direct path-product Green implementation and Möbius template.
- `phase41_exact_jacobian.py`, `phase41_unit_jacobian_certificates.json`: two-cycle phase-only real Jacobian certificates.
- `phase41_three_exact.py`, `phase41_three_cycle_certificates.json`: three-cycle unit-phase full local-rank certificates.
- `phase41_arbitrary_amplitude.py`, `phase41_arbitrary_amplitude_audit.json`: two-cycle unrestricted complex Jacobian comparison.
- `phase41_unit_holonomy.py`, `phase41_three_cycle.py`, `phase41_actual_target_fit.py`: numerical fits, analytic Jacobians, saved parameter samples.
- `phase41_high_precision.py`, `phase41_highprecision_N*.json`: high-precision corrections (numerical evidence only).
- `phase41_full_audit.py`, `phase41_full_audit.json`: full Fourier dephasing comparisons and failures.
- `tests_phase41.py`: regression tests and independent controls.
- `CHECKPOINT.md`: Phase 42 handoff. `VALIDATION.md`: actual run records.
- `previous_full_phase40_checkpoint.zip`: preserved Phase 40 package.

The small source dependencies `phase40_holonomy.py` and `phase40_local_synthesis.py` are distributed in a sibling `fft_green_phase40_four_middle` folder in the outer ZIP, so the new code runs without access to this chat's other files.
