# Source inventory

All user-facing files, code and the immutable `PRIOR_PHASE25_COMPLETE.zip` have content hashes in `MANIFEST.sha256`. The original Phase 25 archive was copied byte-for-byte from `fft_hero1_phase25_20261010.zip` and is not modified. Phase 26 includes a minimal executable copy of the Phase 25 Good–Thomas evaluator for independent comparison.

- Files hashed: **23** (not counting the manifest itself).
- Phase 26 code modules: `phase26_circuits.py`, `volume_gate.py`, `test_phase26.py`, `test_volume.py`, `benchmark_phase26.py`, `audit_phase26.py`.
- Previous-lineage original archive hash: `2c0fba0e88f80b01fdd1085a06d7aebeb846f3aaaf4285aa07a1f39d4860b707`.
- Tooling and code dependencies: Python standard library only.

The manifest records exact bytes; source files and the original historical checkpoint remain distinct.
