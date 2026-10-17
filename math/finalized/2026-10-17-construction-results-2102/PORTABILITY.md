# Public-copy portability and evidence status

The frozen final reviews accepted the original candidate artifacts at their precisely stated scopes. This packaging step ran no scientific executable, test suite, historical program or mathematical re-audit. Recorded result files and logs describe the completed original runs.

Public copies omit private filesystem locations, Library object identifiers, a native sheet-row URL, raw numbered research-register cells, and their direct source fingerprints. Scientific scope excerpts replace the two raw FUS-06 register copies. All original-to-public paths, hashes and edited original bytes are retained in a private sidecar that is excluded from the release.

Unchanged scientific source, proof, result and review files are byte-exact copies. The entries below are explicitly adapted; no modified checker is claimed to have been executed or independently reviewed after these publication edits. Hash/source-location preambles use the included public bytes. Mathematical expressions, control loops and algorithms are unchanged.

The six cited adaptive successor source members are copied exactly and hash-checked as inert data. The exact predecessor packed_outer.py member is also included for the equality check. Whole source archives, private transfer scripts, preliminary work, caches and raw native-row preimages are excluded. Included historical source excerpts are evidence, not a complete dependency tree or an instruction to execute them.

Public local manifests are recomputed for the bytes released here. Original full manifests and full original input bindings remain private. Historical result/review records may name an original reviewed-body or manifest hash; those identifiers are not claims that a provenance-adapted public copy has identical bytes. The original numerical/scientific result is not replaced by a packaging result.

## Explicit adaptations

- `rs_scaling/candidate/MANIFEST.json`: Recompute member byte counts and hashes for the portable copies; original reviewed manifest is retained privately.
- `rs_scaling/candidate/SOURCES.json`: Remove private source locations while retaining exact copied-source hashes and roles.; Bind the public scientific scope excerpts; original native-cell hashes are retained privately.
- `rs_scaling/candidate/sources/FUS06_gate.txt`: Replace raw numbered native-register cells with the indicated scientific scope excerpt; omit administrative metadata.
- `rs_scaling/candidate/sources/FUS06_record.txt`: Replace raw numbered native-register cells with the indicated scientific scope excerpt; omit administrative metadata.
- `rs_scaling/review/INPUT_BINDING.json`: Withhold native-register source fingerprints from otherwise preserved original-run evidence.
- `rs_scaling/review/MANIFEST.json`: Recompute member byte counts and hashes for the portable copies; original reviewed manifest is retained privately.
- `rs_scaling/review/RESULTS.json`: Withhold native-register source fingerprints from otherwise preserved original-run evidence.
- `rs_scaling/review/REVIEW.md`: Replace the private candidate directory with the package-relative candidate location.
- `rs_scaling/review/independent_controls.py`: Resolve the candidate relative to this public package; the mathematical controls are unchanged.
- `alg034_producer/review/SAFE_MANIFEST.json`: Recompute member byte counts and hashes for the portable copies; original reviewed manifest is retained privately.
- `alg034_producer/review/antecedents/accepted_all_length_REPORT.md`: Remove the native owner-sheet row link, preserving the public repository reference and all mathematics.
- `alg034_producer/review/independent_controls.py`: Bind the included provenance-redacted antecedent copy; original reviewed-body hash remains recorded in the original review evidence. No mathematical control changes.
- `alg034_buckets/candidate/SAFE_MANIFEST.json`: Recompute member byte counts and hashes for the portable copies; original reviewed manifest is retained privately.
- `alg034_buckets/candidate/vendor/BRIDGE_REVIEW.txt`: Remove a private Library object identifier; retain the antecedent size, content hashes, scope and findings.
- `alg034_buckets/review/REVIEW.md`: Replace private candidate and producer-review directories with package-relative locations.
- `alg034_buckets/review/SAFE_MANIFEST.json`: Recompute member byte counts and hashes for the portable copies; original reviewed manifest is retained privately.
- `alg034_buckets/review/independent_review.py`: Resolve the candidate relative to this public package; independent numerical checks are unchanged.
- `adaptive_packing/candidate/MANIFEST.json`: Recompute member byte counts and hashes for the portable copies; original reviewed manifest is retained privately.
- `adaptive_packing/candidate/README.md`: Describe the included exact source excerpts and portable checker provenance accurately.
- `adaptive_packing/candidate/REPORT.md`: Replace private Library locator with a neutral source-archive provenance description; mathematical text unchanged.
- `adaptive_packing/candidate/SOURCE_PINS.json`: Remove private Library locator; retain original archive digest and exact cited-member hashes.
- `adaptive_packing/candidate/fresh_controls.py`: Replace archive/provenance I/O only with exact included source-member hash checks and predecessor equality; remove private path and Library ID. All mathematics and control loops remain unchanged.
- `adaptive_packing/review/MANIFEST.json`: Recompute member byte counts and hashes for the portable copies; original reviewed manifest is retained privately.
- `adaptive_packing/review/REVIEW.md`: Replace the private reviewed-report path with the public candidate location; the original reviewed-report digest remains historical evidence.
- `adaptive_packing/review/independent_controls.py`: Use the included provenance-redacted report and verify its exact public-copy hash; original reviewed report/hash remain privately bound. Mathematical controls unchanged.

## Reproduction notes

- Preserve the folder layout. The producer and adapter implementations remain byte-exact.
- Each candidate/review control script writes its own result files when executed. Run any reproduction in a separate copy if the recorded evidence should remain intact.
- RS controls use SymPy and mpmath. Other included new controls use the Python standard library. This package does not install dependencies.
- The adaptive portable candidate checker verifies the included exact source members rather than reopening private archives. The adaptive reviewer and producer reviewer check the exact included provenance-redacted report/antecedent bytes. These are disclosed source-binding adaptations, not new scientific executions.
