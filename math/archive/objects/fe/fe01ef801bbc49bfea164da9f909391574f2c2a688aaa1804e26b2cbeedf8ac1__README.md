# Fourier endpoint audit reproduction

Read ENDPOINT_AUDIT.md for the independent mathematical audit, precise field and model restrictions, and the bounded odd-cut extension. CHECKPOINT_ADDITION.md is the concise integration summary.

Run `python3 independent_checks.py` and `python3 independent_screen_checks.py` from this directory. Python 3.10+ standard library is the only dependency. The programs write CHECK_RESULTS.json and SCREEN_CHECK_RESULTS.json respectively. Existing RUN.log and SCREEN_RUN.log preserve the successful audit runs.

The original source archive is included unchanged in the supplement's source directory. It does not need to be extracted or executed to reproduce these independent checks. SOURCE_INPUTS.json records its exact identity and verified source manifest. SHA256SUMS.txt covers the supplement contents other than itself.

The accepted theorem is an exact single-matrix quasiseparable-rank optimum over C. It is not a new FFT evaluator or a fully charged arithmetic-complexity improvement.
