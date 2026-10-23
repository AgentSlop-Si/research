# Integrity and reproduction boundaries

## Data-only integrity check

Run `python verify_package.py` from the public package directory. `python -O verify_package.py` performs the same explicit checks because it does not rely on assertions. The checker reads only local package bytes, reconstructs the original source archive in memory, checks every included archive member and original checksum line, validates original candidate/reviewer inventories against original/public mappings, and checks source-binding declarations. It never imports or executes scientific programs and writes no files.

The four ZIP files are each independently valid and at most 409,600 bytes. Unpacking source-archive-01.zip, source-archive-02.zip and source-archive-03.zip yields three binary chunks. Concatenate their `original-archive-parts/Phase56_Lightweight_Fresh.zip.part001`, `.part002`, `.part003` contents in that order to reconstruct the exact original ZIP. Expected size is 812345 bytes and SHA-256 is 179a5b7de5575e7c05adf354421a70b8914fb698a3b1b81e22d38e242a737272. The checker performs this reconstruction in memory, so extraction is not necessary for integrity verification.

## Scientific replay is not certified

Candidate `verify_exact.py` is standard-library-only but overwrites its adjacent EXACT_RECEIPT.json and uses assertions. Python -O disables those assertions and must not be described as a valid candidate verification. Independent `fresh_checks.py` uses explicit RuntimeError checks and prints its 62-control result. Its preserved ordinary and optimized result files are byte-identical historical outputs, not newly run controls.

The historical archive contains all six historical scientific programs, original MANIFEST.sha256, all fit/root witnesses and certification receipts. Some programs require NumPy, mpmath and optional SciPy; versions and runtime are not locked. `jacobian_probe.py` and `fourier_fit_experiment.py` retain absolute output paths under /mnt/data/phase56_work. `validate_phase56.py` launches other scientific programs. Certification/refinement writes output files. Preserve the frozen evidence and use only disposable copies if separately undertaking scientific work.

There is no turnkey replay, root-isolation implementation, environment validation, fresh numerical run, proof rerun or external provenance fetch claim. This package preserves exact evidence and its boundaries; data integrity is not a substitute for mathematical review.
