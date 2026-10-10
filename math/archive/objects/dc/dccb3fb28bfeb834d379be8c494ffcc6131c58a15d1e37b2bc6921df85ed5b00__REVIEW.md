# Chirp, bit-reversal and offset-phase source review

## Result

Eight exact source hashes have now received complete first-to-last static inspection: 57,867 bytes and 1,358 lines. All eight are new full-read coverage relative to the frozen inventory, additive registry and all 155 existing COVERAGE.json files found at the initial scan. No supplied source was executed, imported, compiled or parsed. No central registry was edited.

No stored-result error was established in these eight files. The core algorithms are consistent with their stated restricted finite-field or finite-witness domains. The main limitations are qualification and input-validation boundaries, rather than defects in the actual stored inputs.

## Findings that affect use

1. Historical checks are not newly rerun results. The preserved chirp checker reports 118,617 exhaustive vectors; the extension reports eight successful groups; the bit-reversal checker reports 34 modular ranks, six saved minors and 1,020 coordinate finite differences; the offset checker reports 3,230 exact grids, eight rational covariance identities, three corrected rank certificates and five all-state numerical cases. Current work verifies identities and stored-data consistency, not those algorithms by execution.
2. Assertions carry much of the acceptance logic. Running the main checkers or provenance verifier under Python optimization can remove critical tests and still permit PASS output. No evidence shows that the preserved successful runs used that unsupported mode. The manifest wrapper's explicit exceptions survive optimization, and unittest's assertEqual methods survive it, but underlying source asserts remain conditional on mode.
3. General API validation is incomplete. Arbitrary prime/root/dimension inputs, large int64 values and unsupported offset block parameters are not fully guarded. The actual hard-coded or seed-validated cases remain inside safe domains. In particular, the bit-reversal largest dot-product bound is 6,184,752,906,240, below 2^63; no stored overflow was found.
4. The chirp extension is standalone. Its polynomial-r Bareiss/Toeplitz eliminants and geometric scan have not been substituted into the preserved factorial-eliminant recognizer. The original O_r(N) statement remains a fixed-r supplied-field arithmetic claim; it is not an unrestricted linear DFT or a runtime speed result.
5. Dense certificate checking is expensive. Only the separated-generator scan has 5Nt multiplications and 4Nt additions. Dense Jacobian/elimination and all-state covariance checks do not inherit the proposed estimator's arithmetic costs.
6. Exact versus numerical evidence remains separated. Offset grids, Fraction covariance identities and Chebyshev ranks are exact finite certificates; complex-root/eigenvalue calculations are numerical checks with explicit tolerances. The unnormalized rank-one block is intentional for the sketch's mean, not an accidentally missing factor.
7. Dependency lineage is verified without claiming source review. The v12 core matches the exact v9 prototype and v11 core; the v12 fused reference matches the exact v11 prototype. All 17 v12 manifest entries and three archive hashes pass inert-byte verification. These dependency hashes receive no new full-source coverage.

## Integrity and acceptance

The current outer manifests for 1906_chirp, 1908 and 1910 match every listed payload and their intended complete file sets. The preserved earlier approved 1908 subset also matches; its later source-archive additions are explicitly outside that earlier subset. There is no manifest mismatch after normalizing harmless './' paths.

Accept these eight files as completely read static source reviews with the scoped historical evidence described in each per-source document. Do not promote this to a fresh successful run, a dependency-closure audit, all-material completion, arbitrary-size bit-reversal saturation, an FFT factorization, practical speedup, numerical stability or novelty acceptance.

## Package guide

- COVERAGE.json: per-hash completion and new-coverage flags
- per_source/: eight complete code reviews, with line scopes, correctness, guards, costs and acceptance
- snapshots/: exact assigned source bytes
- evidence_snapshots/: preserved source packages, results, logs, fixtures and archive bytes
- DEDUPLICATION.json: manifest identities and exact matching records
- DEPENDENCY_IDENTITIES.json: local import, subprocess and byte-lineage identities
- MANIFEST_CHECKS.json: inert checksum/set reconciliation
- STORED_RESULT_RECONCILIATION.json: stored-data and count checks, explicitly not a rerun
- PRESERVATION.json: before/snapshot/after byte checks
- SHA256SUMS and SEAL.json: review-package integrity seal

The two small build/write scripts in this package were authored for this review. They only inventory/copy inert evidence, reconcile metadata and assemble reports. They are not supplied research source and do not earn research-code coverage.
