# Reproduction and source identity

## Verify the package

From the package root, run with Python 3.10 or later:

    python -I -S verify_package.py

The verifier uses only the standard library. It checks every payload file's byte count and SHA256, the manifest hash in `SHA256SUMS`, the exact checksum file set, and absence of unexpected payload files. Integrity verification is not a mathematical proof or external-publication receipt.

## Rerun the independent scientific controls

The scientific checker requires Python 3.10 or later and NumPy. Versions used for the verified packaging run are recorded in `CHECK_RUN_RECEIPT.json`. It uses no network, imported historical source programs or files outside its own directory. Run in a copy if preserving the exact sealed output matters:

    python -I checks/independent_controls.py

The script overwrites `checks/FRESH_CONTROLS.json`. On the packaging environment the output was byte-identical to the sealed independent-review result. Floating-point output may vary slightly across NumPy/platform versions; the checker's assertions use explicit tolerances. Such a rerun may invalidate the original byte manifest even when all mathematical controls pass.

The verified controls cover:

- Five exact Weyl joint-equation solution dimensions over F97; ten exhaustive calibrated-probe cases over F5/F7; wrong-scalar rejection; and the seven-call ledger for two probes.
- Nine complex numerical sharp-gap equality and random-map inequality controls. Floating calculations corroborate the analytic proof.
- 2,264 exact modular parity submatrix ranks: every nonzero mask pair and all four signs at N=4,8,16 over F97 and F193. These finite checks do not replace the characteristic-zero sampling theorem.
- The universal-set specialization with ranks 7 over F12289 and 8 over F65537, and the corrected weighted capacity 124 for the r=2 regression.
- Forty-two exact tensor flattening ranks over fourteen square/rectangular sizes, including unit radices, with direct digit-exponent consistency checks.
- All 230,400 pairs of invertible 2x2 matrices over F5 for the endpoint-support equality characterization; 1,024 minimizing pairs. This is support accounting over the two endpoint factors, not 230,400 separately reconstructed tensors.

The report's analytic arguments establish the qualified all-size statements. Bounded tests cannot establish them by extrapolation. Larger historical executions, source-program implementations, timings, original archive recovery and unrelated theorem records were not replayed here.

## Original versus publication bytes

`SOURCE_BINDINGS.json` maps every named theorem to its pinned mathematical report and historical accepted decision. `PUBLIC_PROVENANCE.json` records the source and output hashes, byte counts and exact editorial transformations. `SOURCE_TO_GIT_PATH.json` maps all package files to the intended repository destination; the repository commit itself must be verified separately.

The Weyl and parity reports and both historical outcome ledgers are unchanged source bytes. The tensor report's public derivative removes four private Library identifiers and replaces a source-location sentence with an explicit historical-context sentence. Its mathematical text is unchanged. The pinned tensor input is itself a supplied export; the package does not assert byte equality to an unavailable earlier original or reconcile distinct historical export labels.

The author and independent reports are marked `.public.md`. They retain the mathematical sections, guards, comparisons and test scopes while removing workbook identifiers, row bindings, transient live-count metadata and application workflow prose. The original report hashes remain bound in provenance and the public verdict. The exact-payload public summary omits individual native-cell digests and local request paths while retaining acceptance, exact payload hashes, aggregate preservation results and all application requirements. The actual mutation payload and native worksheet snapshots are deliberately absent.

Historical source reports can refer to companion programs, archives and evidence that are not part of this compact package. Those references identify their historical context. They are not promises of source recovery or newly performed execution. Inclusion of broad historical reports or ledgers does not finalize other records.
