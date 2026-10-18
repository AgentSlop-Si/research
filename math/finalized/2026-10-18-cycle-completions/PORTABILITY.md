# Public preservation, provenance, and portability

All six final independent reviews apply to the originally inspected bytes and their precise scopes. This package contains selected scientific reports, code, fixtures, and recorded results, with disclosed location/privacy adaptations only. Original byte copies and original manifests/seals remain privately retained. Private research-register snapshots, their direct fingerprints, Library locators, private conversation links, caches, whole source archives, and workflow sealing helpers are excluded.

Public candidate/review manifests are newly computed for the selected portable copies. Hashes quoted in original reports and run records are historical reviewed-byte identities; they are not assertions that an adapted public copy has the same hash. COPY_BINDINGS.json records both identities. No original scientific program, historical program, or adapted checker was executed during packaging.

The sole production-code adaptation replaces the absolute dependency location in shared_product/candidate/run_shared.py with a package-relative path. Its arithmetic and the dependency SHA-256 guard are unchanged; the dependency itself is byte-exact. All other production arithmetic implementations are byte-exact. Review-script adaptations resolve included candidate/dependency files and current manifests. No mathematical control was removed.

Included original R30 source and builder files are inert inspection evidence. They are not a complete independently executable historical archive. No original-compiler execution is claimed. All complete source archives remain outside this public package.

## Explicit copy adaptations

- `outer_stream/candidate/SOURCE_BINDINGS.json`: Replace private source locations with public relative/descriptive references; remove private attribution locators only. Bind only included scientific source bodies with package-relative paths; omit historical manifest dependencies.
- `outer_stream/review/PROOF_AUDIT.md`: Replace private source locations with public relative/descriptive references; remove private attribution locators only.
- `outer_stream/review/independent_review.py`: Use the included public candidate for portable reproduction; scientific controls unchanged. Verify the included public scientific dependency bodies; original full source bindings remain private.
- `outer_stream/review/oracle_crosscheck.py`: Use the included public candidate for portable reproduction; scientific controls unchanged. Bind the recomputed public candidate manifest count; the original run had 20 members.
- `sparse_recovery/candidate/SOURCE_PROVENANCE.md`: Retain the local-only execution fact without private workflow details.
- `sparse_recovery/review/independent_controls.py`: Use the deduplicated included candidate rather than a duplicate immutable snapshot; original snapshot remains private.
- `shared_product/candidate/SOURCE_PINS.json`: Replace private source locations with public relative/descriptive references; remove private attribution locators only. Bind included scientific dependencies by public relative path and current hashes; retain original hashes separately.
- `shared_product/candidate/run_shared.py`: Replace one absolute dependency path by a package-relative path; unchanged primitive hash guard and arithmetic.
- `shared_product/review/HARNESS_THRESHOLD_CORRECTION.log`: Replace private source locations with public relative/descriptive references; remove private attribution locators only.
- `shared_product/review/RESULTS.json`: Replace private source locations with public relative/descriptive references; remove private attribution locators only.
- `shared_product/review/REVIEW.md`: Replace private source locations with public relative/descriptive references; remove private attribution locators only.
- `shared_product/review/independent_review_controls.py`: Use the included public candidate for portable reproduction; scientific controls unchanged.
- `frobenius_support/candidate/REPORT.md`: Replace the private register-cell source paragraph with the mathematical gate; omit the private snapshot and its direct fingerprints. Remove private register priority while preserving the open parent status.
- `frobenius_support/candidate/RESULT.json`: Omit private register-snapshot fingerprints and unrelated table-count/priority metadata; scientific results unchanged.
- `frobenius_support/review/CANDIDATE_BINDING.json`: Omit private register-snapshot fingerprints and unrelated table-count/priority metadata; scientific results unchanged.
- `frobenius_support/review/INDEPENDENT_ARITHMETIC.json`: Omit private register-snapshot fingerprints and unrelated table-count/priority metadata; scientific results unchanged.
- `frobenius_support/review/independent_review_check.py`: Use the included public candidate for portable reproduction; scientific controls unchanged.
- `mersenne_setup/candidate/SOURCE_PINS.json`: Replace private source locations with public relative/descriptive references; remove private attribution locators only. Bind included scientific dependencies by public relative path and current hashes; retain original hashes separately.
- `mersenne_setup/review/REVIEW.md`: Replace private source locations with public relative/descriptive references; remove private attribution locators only.
- `mersenne_setup/review/independent_checks.py`: Use the deduplicated included candidate rather than a duplicate immutable snapshot; original snapshot remains private. Resolve the portable source pins relative to the candidate.
- `fourier_interface/candidate/INPUT_REFERENCES.json`: Replace private source locations with public relative/descriptive references; remove private attribution locators only. Bind included privacy-adapted scientific evidence; original reviewed hashes remain historical metadata.
- `fourier_interface/review/REVIEW.md`: Replace private source locations with public relative/descriptive references; remove private attribution locators only.
- `fourier_interface/review/independent_controls.py`: Use the included public candidate for portable reproduction; scientific controls unchanged. Resolve public source evidence paths relative to the candidate and verify the public evidence hashes.
- `fourier_interface/review/independent_results.json`: Replace private source locations with public relative/descriptive references; remove private attribution locators only.
- `mersenne_setup/candidate/dependencies/negacyclic_final_review_20261017_1741/REVIEW.md`: Replace private source locations with public relative/descriptive references; remove private attribution locators only.
- `fourier_interface/candidate/dependencies/fourier_rewrite_completion_20261017_2130/PROOF.md`: Replace private source locations with public relative/descriptive references; remove private attribution locators only.
- `fourier_interface/candidate/dependencies/fourier_rewrite_final_review_20261017_2141/REVIEW.md`: Replace private source locations with public relative/descriptive references; remove private attribution locators only.

## Reproduction instructions and limits

- Run python3 verify_package.py at the package root for read-only byte, exact-file-set, syntax, and privacy checks. This does not re-audit the mathematics.
- Review each complete script before running it. Run scientific programs only in a disposable copy, from their own folder, so recorded evidence and release manifests are not overwritten.
- Python 3 and its standard library suffice for the selected production paths. This package installs no dependency. The inherited R30 inspection-only sources are not a standalone execution bundle.
- outer_stream/candidate/launch.py and outer_stream/review/launch_review.py retain the original capped finite workloads. Other scripts retain their finite supplied workloads; resource restrictions are the caller’s responsibility.
- sparse_recovery/review/independent_controls.py and mersenne_setup/review/independent_checks.py use the sibling candidate directory instead of duplicate reviewed snapshots. Original duplicate snapshots remain private.
- Portable integrity checks hash the selected public copies and included evidence. Original metadata/hash counts can differ from new reproduction metadata; original results remain evidence of the original run only.
- Outer source pin checks omit three old manifest dependencies, while retaining the eleven cited scientific implementation/proof/review bodies. Original all-fourteen bindings remain private.
- The Frobenius portable checksum list excludes the private register snapshot. No scientific premise or numerical evidence is removed.
- Read REQUIRED_CLARIFICATIONS.md before using any asymptotic, probability, support, or closure claim. No external publication action is authorized or performed by this package.
