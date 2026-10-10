# Reproducing finite controls

These scripts are reviewable, newly authored finite controls. They are not the production algorithm and do not certify an asymptotic runtime or historical novelty. No uploaded/predecessor research program was run to obtain the supplied records.

Use working copies if running them: several scripts write their JSON results beside their source, which would change the checksum-pinned release tree. Re-running ordinary floating-point stress controls may yield small platform-dependent numeric differences. The exact combinatorial assertions are distinct from those numerical cases.

## Standalone controls

- `controls/constructor/check_packed_identities.py`: Python 3 standard library. Exact integer identities and compact toy eager tables. Writes `EXACT_CONTROL_RESULTS.json` beside itself.
- `controls/independent/check_packed_controls.py`: Python 3 plus NumPy. Tiny eager complex-state tables, exact finite total-map checks, and explicitly uncertified numerical stress tests. Writes `control_results.json` beside itself.
- `controls/all_length_independent/check_all_length_controls.py`: Python 3 standard library. Exact-integer fixed-lattice fallback arithmetic, high-precision Decimal references, and ordinary floating interpolation falsification checks. Writes `CONTROL_RESULTS.json` beside itself. It has no relocated-source dependency.
- `limits/check_guard_thresholds.py`: Python 3; prints exact parameter/count checks only. It does not allocate an FFT or response table.

## All-length author's original-layout dependency

`controls/all_length_author/check_all_length_parameters.py` is preserved byte-for-byte with its recorded results. It derives a research root from its original location and checks four root-relative source paths. It is therefore NOT directly portable when invoked from its relocated release directory.

To run an unchanged copy, prepare a separate temporary root and restore these original relative locations from the bundle:

- `research_cycle_0958/algorithms/FINAL_THEOREM_AND_PROOF.md` from `provenance/ACCEPTED_UNPACKED_COMPARISON.md`
- `q01_finalization_1345/revision_v3/public/Q01_FINALIZATION.md` from `provenance/Q01_FINALIZATION_v3_HISTORICAL.md`
- `q01_finalization_review_1350/public/INDEPENDENT_ACCEPTANCE.md` from `provenance/Q01_ACCEPTANCE_HISTORICAL.md`
- `packed_fft_candidate_1355/executor_derivation/DYADIC_PACKED_THEOREM.md` from `theorems/DYADIC_PACKED_THEOREM.md`
- `packed_fft_candidate_1355/all_length_extension/check_all_length_parameters.py` from `controls/all_length_author/check_all_length_parameters.py`

Invoke the last copied script with Python 3. The script verifies the expected source hashes before checking integer parameter inequalities and writes a new `PARAMETER_CONTROL_RESULTS.json` next to the working copy. It never executes, imports, or compiles the four mathematical source documents. No original private conversation, cloud account, or Library access is needed.

The manifest records original research-source paths only as provenance and relocation information; those are not network locations or private conversation links.
