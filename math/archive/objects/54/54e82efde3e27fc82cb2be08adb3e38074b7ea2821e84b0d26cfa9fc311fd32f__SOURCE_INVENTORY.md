# Research lineage, attribution and source inventory

The file `PRIOR_PHASE24_COMPLETE.zip` is an unmodified copy of `fft_hero1_phase24_20261010.zip` from the previous checkpoint, which itself contains the untouched Phase 23 archive and earlier research lineage.

`phase24_source/` holds byte-identical Python files from the unpacked Phase 24 folder for local reproducibility of Phase 25's integrated Green certificate. The existing Phase 24 theorem, cost ledger, tests and code remain accessible in the preserved prior archive.

**New Phase 25 authorship/integration:** `gt3_deferred.py` (CRT-indexed three-way deferred Fourier graph, optimized twiddle skipping, cached partial Winograd-3 codelet, independent CT3 comparison), `gt3_green.py` (unchanged Phase 23 sparse-rational certified candidate integrated with exact GT3 fallback), `entropy_gate.py` (sanity check of Ailon's known entropy potential), `test_phase25*.py`, `audit_phase25.py`, `benchmark_phase25.py`, documentation and receipts.

**Prior work explicitly credited:** Good and Thomas for coprime-factor FFT indexing; Cooley and Tukey for mixed-radix FFT; Winograd for arithmetic-efficient small DFTs; Ailon for the 2×2 unitary lower bound; Morgenstern for bounded-coefficient arguments; previous Hero #1 checkpoints for Green and deferred-FFT integration. Neither these foundational results nor their novelty is claimed here.

All source files and the immutable old archive have SHA-256 checksums in `MANIFEST.sha256`; no current archive's checksum is circularly included in its own manifest.
