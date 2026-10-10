# Phase 42 | Graph-signature collision and noncommuting Green escape

**Main question:** Can a fixed number of independently ordered weighted Hamiltonian-cycle Green resolvents, or products of their sums, reproduce the exact DFT with sub-`N log N` online work?

## Results

- An all-length restricted impossibility theorem for **sums of q cycles**: `N <= q(q+1)^q` is necessary for exact Fourier equivalence, even for arbitrary complex edge amplitudes and independent per-term monomial gauges.
- For the actual **three Phase 41 cycle orders at N=128**, all **10,668,000 four-row subsets** have a forced 4x4 projective collision, excluding every possible choice of Green weights and arbitrary *external* phase/coordinate gauges.
- An exact differential finding for one three-cycle sum: full parameter rank `2N+1`, so locally only three phase freedoms remain after two rows are fixed.
- A positive constructive lead: a **two-stage product of three-cycle sums** has full local three-row phase rank `4(N-1)` through N=64. It escapes the rank restriction but still fails Fourier covariance.

**No `o(N log N)` FFT achieved.** Local Jacobian rank, matrix density, and a fit to a few Fourier columns or rows never suffice.

## Contents

- `THEOREM.md`: complete mathematical statements, derivations, assumptions and limitations.
- `CHECKPOINT.md`: exact chain-recovery point for Phase 43.
- `phase42_all_row_audit.cpp`: pure integer all-four-row verifier. Reads the three cycles from `graph_N*.txt`.
- `phase42_three_row.py`: exact three-row real Jacobian of one three-cycle sum (two split primes).
- `phase42_signature_gate.py`: characteristic-zero nonvanishing tests for the conditional three-row capacity lemma.
- `phase42_minor_witness.py`: explicit 4x4 Green and Fourier minor comparisons.
- `phase42_product_control.py`: shows the rank obstruction disappears under a noncommuting Green-sum product, but the Weyl equations still fail.
- `phase42_product_jacobian.py`: exact full-rank three-row Jacobian certificate for the two-stage product.
- `phase42_product_fd.py`: independent numerical derivative check.
- `tests_phase42.py`, `RUN.sh`: full current suite, no network required.
- `phase40_*` / `phase41_*`: copied code dependencies, preserving standalone execution.
- `previous_full_phase41_checkpoint.zip`: the whole prior research chain, retained unmodified.

## First command

```bash
bash RUN.sh
```

The small signed/complex derivative tests require `numpy` only for optional finite differences, and the default exact certificate algorithms use standard Python and a C++17 compiler. No special-purpose CAS or online lookup is required.
