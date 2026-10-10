# Reproducible v34 FFT research checkpoint

This is a **scoped exact arithmetic obstruction**, not a faster FFT. It continues the v33 99-edge Fourier phase network unchanged and includes v33's complete ZIP.

Run from this directory:

```bash
python run_all.py
```

It recomputes all support-deletion certificates, verifies exact cyclotomic minors, runs 10 automated test groups, invokes an independent verifier, checks the v33 predecessor hash/CRC and the local content hashes.

Inputs/proofs: `RESEARCH.md`, `CHAIN_CHECKPOINT_2026-10-10_v34.md`, `topology_11.json`.

Code/certificates: `forcing_gate.py`, `valuation_gate.py`, `independent_verifier.py`, `forcing_results.json`, `valuation_results.json`, `test_checkpoint.py`, `MANIFEST.sha256`.

See `OPERATION_LEDGER.csv` and `PRIOR_ART_AUDIT.md` for exact claim limits.
