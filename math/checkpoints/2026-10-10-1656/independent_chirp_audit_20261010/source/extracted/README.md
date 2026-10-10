# Hero #17 — Phase 23

**Chirped q-Green Cayley-Graph Union:** exact linear-time N-point DFTs for an automatically recognized family whose base-normalized Hankel rank can be linear in N.

This package **does not** solve the universal exact O(N) FFT.

Files:
- `phase23.py`: blind raw-input recognizer; deterministic sparse chirp phase gate; short-/wrapped-jump, subgroup-coset and resonant one-pole executors; exact NTT fallback.
- `phase22.py`: retained standalone Phase22 implementation, serving as the standard NTT reference.
- `test_phase23.py`: regression suite, including exhaustive eligible-parameter comparisons for small sizes.
- `independent_audit.py`: exact full-spectrum and direct-sum comparisons, fixed-chirp operation ledger.
- `coset_audit.py`: four spectral strategies through N=177147, with separate N-point NTT preparation and online ledger.
- `AUDIT_RESULTS.json`, `COSET_AUDIT_RESULTS.json`: machine-readable exact test results and operation counts.
- `PROOF_CERTIFICATE.md`, `RESEARCH.md`, `CHAIN_CHECKPOINT.md`: mathematical proofs, boundaries, follow-up handoff.
- `PHASE22_PREDECESSOR.zip`: complete prior phase source and lineage.
- `SHA256SUMS.txt`: source/results integrity checks.

Run `python -m unittest -q test_phase23` and `python independent_audit.py`, then `python coset_audit.py` for the full large-instance audit. See `RUN.md` for details. Input fields must have odd N and an explicitly supplied primitive 2N-th root of unity.

All numerical counts are finite-field *scalar operation* counts, **not** wall-clock measurements or general FFT lower bounds. Hashing and discrete-log oracles are not used.
