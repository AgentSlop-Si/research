# Full-source review 06: v11_test_checkpoint.py

- SHA-256: 48dfdc7feccf9c6295e22ebe1ad8ed8824d33a0ed5b129962082bf692cb4c993
- Exact bytes: 7352; complete lines read: 1–179
- Assigned batch: 02_addition_1906_centered_01.json
- Representative path: additions/1906_centered/extracted/fft_hero1_centered_v12/v11_test_checkpoint.py
- Snapshot: ../source_snapshots/06_v11_test_checkpoint.py.txt
- Method: complete first-to-last inert reading, dependency-context inspection, and stored-evidence reconciliation. No supplied execution/import/compilation/syntax parse.
- Findings: F06
- New exact-hash full-review credit: yes, subject to final concurrent deduplication check.

## Verdict and evidence impact
Full static read complete. Thirteen fixed-seed v11 regression methods are retained inside the centered-v12 package. Their saved 13-pass log is consistent with the source method list. They test inherited v11 functions, not all centered-v12 functionality. In particular the precision stress is mixed-precision decoder-storage stress, and the allocation/work tests inspect formulas rather than measured runtime or peak memory.

## Complete control-flow audit
- Lines 1–16: imports NumPy, SciPy jv, prototype, and unit_step_core; setUp resets the same RNG seed for each unittest method, providing deterministic per-test streams.
- Lines 18–26: all n=2,…,299 exact nearest-grid maps; uniqueness and integer residual constraint checked. The floating reference k*q/n+0.5 is accurate enough at these small bounded integers. This does not cover large fixed-width index overflow or near-large-integer tie behavior.
- Lines 28–37: selected decoder vs full decoder on arbitrary summary vectors at three q/block pairs; useful interface test, but shared primitives/root conventions limit independence.
- Lines 39–47: streamed Clenshaw vs retained reference at five n values, rank=10.
- Lines 49–63: 900 seeded pointwise Bessel-addition controls for nonnegative z and delta; expected tail is from the same prototype, so this is finite numerical support.
- Lines 65–78: 8 fusion-center comparisons (four n values, H=0,1), comparing implementation error to deterministic bound times norm.
- Lines 80–91: six scalar parameter evaluations at n=2^exp−1 show a declining halfwidth-zero ratio for sampled exponents; this is not an asymptotic proof or allocation of those enormous arrays.
- Lines 93–109: 250 randomized rows at one n/state-family measure empirical squared deviations around the deterministic fused center. Correlations across outputs are allowed; maximum empirical variance below a conservative formula is not unbiasedness, a confidence interval, or a universal variance certificate.
- Lines 111–122: one fixed-seed n=61 end-to-end randomized sample with nine rows; its success does not establish the stated global failure probability.
- Lines 124–135: complex64 vs complex128 call-path stress at n=257 and ranks 4,8,12. Inspection of exact prototype.py shows complex128 input, phase/Bessel compression and Clenshaw stages; SelectedDecoderPlan casts summaries/storage while its FFT explicitly promotes to complex128. Thus this test does not exercise a uniformly binary32 end-to-end implementation or certify every primitive assumed by the analytic precision model. It also calls streamed_bessel_chirp_row, not the fused path requiring the separate decoder-on-summaries theorem.
- Lines 137–146: four scalar sufficient-mantissa formula evaluations; observed ratio behavior is a formula regression, not proof of Theta(log N) or a verified arbitrary-precision implementation.
- Lines 148–165: allocation_model returns accounting formulas, including literal zero rank-dependent full-length storage. The work-ratio test independently forms q+R(q/block) divided by Rq. Neither instruments real allocations or operations, nor includes all Bessel/phase preparation, FFT, scan, aggregation, and bit costs.
- Lines 167–175: exact zero-signal invariant for one valid configuration.
- Lines 178–179: unittest entry point.

## Guards, dependencies, and cost
All configured sizes/blocks are valid and fixed. Invalid dimensions, empty/nonfinite signals, degenerate state rejection, overflow/underflow, difficult boundary classifications, and malformed summary shapes are not directly tested here. The dependency snapshots identify prototype=25590a19… and unit_step_core=6a95e865…; they are not full reviewed by this package and no installed NumPy/SciPy versions were validated. Largest actual vector length is small (q≤512 for transform tests), while n≈2^120 occurs only in scalar model calculations. Per row the retained path pays rank-many short FFTs plus full scans/Clenshaw; sampled model savings in input fusion alone do not remove those terms.

## Stored evidence reconciliation
The exact saved log lists all 13 methods and reports “Ran 13 tests … OK”; the enclosing run_all.py sets cwd to the sibling directory. This review neither repeated that run nor certifies the logged runtime. Prior V11_FP_CONTRACT_REVIEW.md explicitly supplies a conditional summary-interface repair and declines to certify NumPy/SciPy/BLAS. The narrowed interpretation above is consistent with that existing caveat, not a newly demonstrated numerical failure.
