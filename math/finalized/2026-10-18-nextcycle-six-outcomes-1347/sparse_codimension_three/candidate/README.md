# Codimension-three sparse inverse defect

Candidate research packet for M-SPARSE-DEFECT. Read `REPORT.md` for the complete proofs and exact scope.

New results:

- The Fourier inverse-row floor at `s=N−3` is sharp exactly when `3 | N`; every equality mask splits into full `3×3` blocks with an explicit phase congruence test.
- Whenever the accepted equality mask does not exist, an explicit positive squared-gap lower bound is `s^6 / (2^22 N^10 (N−s)^(2φ(N)−2))`.

Reproduce all controls with Python 3 and SymPy:

    python verify_exact.py > VERIFY.log 2> VERIFY.stderr

A successful run writes `RESULTS.json` and ends with `PASS`. All arithmetic is exact. The script neither imports nor runs previous checkers. Source snapshots and bindings are included. `MANIFEST.json` binds the packet; `SEAL.json` binds the report, checker, and manifest.

This is a candidate for independent review. Parent owner remains TO RESEARCH, priority 42. No external state was changed.
