# HERO #17 — Phase 16

**Fourier–Green interface rigidity and sharp interpolation certificates.**

Target: fresh, arbitrary-input, full-spectrum exact DFT. **Target not solved.**

Main proof: `PROOF_CERTIFICATE.md`.
Research/limitations: `RESEARCH.md`.
Recovery: `CHAIN_CHECKPOINT.md`.

Executable files:
- `phase16.py` — entirely explicit modular linear algebra and boundary construction (no numerical FFT oracle).
- `test_phase16.py` — 19 new named unit tests.
- `independent_audit.py` — independent direct DFT and exhaustive finite-field checks, writes `AUDIT_RESULTS.json`.
- `PHASE15_PREDECESSOR.zip` — unchanged canonical prior phase archive.

Run `python -m unittest -v test_phase16` and `python independent_audit.py`.

Dependencies: Python standard library only. `GF(p)` arithmetic is exact; field inversions are not constant-time *bit* operations. Direct modular basis verification and Gauss elimination are **test methods**, not evidence of efficient runtime.
