# Phase25 independent audit supplement

The original Phase25 upload is preserved unchanged in `source_archives/`. No submitted code was executed or imported.

Start with `PHASE25_AUDIT.md`. It verifies the affine-run/rank/hidden-cut claims, supplies explicit missing-invertibility and failed-pivot counterexamples, proves a whole-matrix linear-time pivoted repair, and improves the small-coupling condition bound to 155/98.

Files:
- `PHASE25_AUDIT.md`: findings, proofs, corrected scope, and prior-Phase24 comparison.
- `CHECKPOINT_ADDITION.md`: concise corrected checkpoint to preserve alongside the original.
- `frontier_solver.py`: independently authored exact modular whole-matrix solver; no submitted imports.
- `independent_checks.py`: bounded exact controls; Python standard library only.
- `CHECK_RESULTS.json`, `RUN.log`: fresh successful independent checks.
- `SOURCE_INPUTS.json`: input identity and inspected-member hashes.
- `SOURCE_VERIFICATION.json`: source-archive member and source-manifest verification.
- `PORTABILITY_CHECK.json`: successful independent execution from an unrelated copied directory.
- `SHA256SUMS.txt`: hashes for this supplement's files, excluding itself.

Reproduce from any extracted location with Python 3:

    sha256sum -c SHA256SUMS.txt
    python independent_checks.py

The checker rewrites its results with a fresh elapsed time, so verify the supplied seal before rerunning; a fresh run intentionally changes the results hash. No network or connection to the Library is needed. Archive extraction is not required to reproduce the independent mathematical controls.

The fixed-modulus executable is exact arithmetic, not a certified floating-point solver. The repaired theorem still requires nonsingular individual resolvents and nonsingular sum. No arbitrary-input faster FFT is claimed.
