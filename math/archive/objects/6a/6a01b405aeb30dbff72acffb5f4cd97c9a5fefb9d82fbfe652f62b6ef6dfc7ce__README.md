# Unequal block and coprime Green source audit

Read `audit/ROUGH_LENGTH_AND_COPRIME_GREEN_AUDIT.md` for the results, proof scope, implementation corrections, independent fusion and verification inventory. `audit/DISPOSITION.json` separates accepted, inherited and still-open claims. The completed companion Gaussian review is preserved in `audit/companion_evidence/GAUSSIAN_ALL_LENGTH_AUDIT.md`; together the reviews support the conditional supplied-constant RAM all-length approximation theorem. This report owns covariance, source correspondence, exact frames and the v14 tradeoff. No finite-precision, exact-FFT or novelty claim follows.

Both original Library archives and their complete extracted members are retained unchanged. `SOURCE_MANIFEST.json` and `hero0/SOURCE_MANIFEST.json` identify every original member. Source bytecode is preserved only as inert data.

Reproduce only the independently written checker:

    cd audit
    OPENBLAS_NUM_THREADS=1 python3 independent_checks.py

The checker reads source manifests and ASTs as data and never executes uploaded code. It regenerates `CHECK_RESULTS.json`. Its console output was saved in `CHECK_RUN.log`. `STATIC_CORRECTIONS.json` is the separately readable duplicate of the static counterexamples in the regenerated results.

`SHA256SUMS.txt` covers every source and audit file except itself and `SEAL.json`. `SEAL.json` records its hash and the verified file count. No master or Library changes were made.
