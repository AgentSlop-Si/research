# CrocSwap transfer audit — method, not the exponent route

**Pinned snapshot:** `CrocSwap/integer-mult-bounds`, commit `3b6b66891c0ac888521cf591fe306c6286601d4f` (2026-10-09). Read `README.md`, `research/coordinated-frames-and-entrance-banks/PROOF.md`, `research/community-round8-audit/BANK-SCHEDULE.md`, and `docs/research/community-round8-review.md` through the connected GitHub repository.

## Facts checked in that snapshot

- The GitHub README reports a **conditional** multiplier bound `O(n(log n)^(1-kappa))` with `kappa=330942774629799/500000000000000000`.
- The selected construction trades local scalar additions against carrier arcs, schedules bank reuse only after conflict-free completion, verifies actual physical words and dirty-register restoration, and prices root/bank/adapter fees.
- The repository explicitly warns that finite witness replay and maintainer review do not discharge retained analytic, uniform recursion, fixed-tape, compilation and recovery interfaces. These conditions cannot be silently imported as unconditional FFT results.

## Ideas *transferred* to our independent Fourier path

1. **Whole-word accounting, not local identity counts.** The centered lift charges every rank-dependent K-FFT and length-Q scan. The proof distinguishes reducing the number of channels from reducing total operations.
2. **Conflict-free shared resources.** One chirp state and one computed output carrier are reused across R Bessel orders / randomized rows, only after verifying when the underlying inputs are identical. Merely batching R independent scans is not an O(N) algorithm.
3. **Exact certificates plus positive and corruption controls.** The rank-independent convolution bound has a separate algebraic proof and direct numeric regression tests, and the `center_override=0` branch checks byte-for-byte agreement with the existing v11 executor outputs in the tested cases.
4. **Precision is part of the inventory.** Reusing two approximate carrier transition phases N times introduces a possible O(Nu) error from root inaccuracies. This is disclosed, not hidden under a balanced-scan depth bound.
5. **Immutable checkpoint and regression.** Baseline v11 files are carried unmodified and their 13 tests rerun; the Green Phase 22 and rank-window suites are independently verified from their source archives. New source/results include a SHA256 manifest.

## Techniques deliberately *not* imported

No kappa exponent optimization, Clifford/group frame swapping, recursive bit-register supplier, fixed-tape assumptions, paid auxiliary-bank oracle, or new integer-multiplication conclusion. These are a different architecture. Their success or failure is not a verdict on exact Green/Fourier circuits.

## Novelty boundary

Global phase centering, Jacobi–Anger expansions, Neumann addition, and convolution-norm inequalities are standard ideas. This checkpoint is a concrete **project-specific composition and verification**. It should not be represented as a literature-priority proof.
