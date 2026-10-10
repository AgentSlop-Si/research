# Remaining FFT gates and implementations: exact-source review

Completed 2026-10-10. Full first-to-last inert review of 46 distinct source hashes, 343,250 bytes and 8,172 lines from batch_01.json. Source snapshots and numbered copies are sealed with per-hash findings and coverage.

## Findings that change how the material can be used

1. `adaptive_fft.py` (S02, a1094fc0…) has a dependent-basis registration defect: `fft_family(register=True)` can reduce the stored basis to one row while retaining two original spectra, making a later span query dimensionally inconsistent. Rank recognition also uses `allclose`; it is approximate, even when surrounding language says validated or exact reuse.
2. `cost_aware_fft.py` (S40,150e8e4d…) has a spectrum-only fallback defect: `sparse_from_known_changes(..., method='auto')` can choose native FFT of the zero placeholder raw signal plus edits, dropping the supplied base spectrum. For N=2, base [1,1] and edit at0 of+1, the required output [3,1] differs from placeholder output [1,1]. This was established by source tracing and independently authored arithmetic, without running the source.
3. `arbitrary_output.py` (S15,b0f64933…) can reuse stale calibration output when `project_stream_with_sample` receives a sample different from the constructor's sample. The zero-trial planner intent is also defeated by `max(1,limit)`. Memory budgets and divisor assumptions need qualification.
4. The archived `benchmark_lazy_results.json` is consistent with the quick source S23 (18 rows,200/128 updates), and inconsistent with full source S22's default41-row,500/256 grid. Shared output names are not evidence that both exact hashes were executed.
5. The C++ cache benchmark reads double memory via `uint64_t*`, a strict-aliasing portability issue. FFTW new-array alignment assumptions are not made explicit. Component timing columns mix seed work/fixed repetitions with median elapsed totals. No compilation was attempted.
6. Several mathematical checks are strong within their actual domains: fixed N5 exact extension-field identities, finite-horizon retained Schur identities, modular rank witnesses, Boolean-domain completion obstructions and conditional annihilator inversion. Their domains must remain attached. Dense oracle synthesis, hidden ordinary FFTs, restricted parameter families, finite samples and output descriptors do not establish a new global FFT algorithm.

## Fresh independent checks

51 newly authored reviewer checks passed. They include:
- A literal path-sum reproduction of the retained N16,b2,H5 beyond-horizon vector [0,57313,0,510], contradicting the stored naive zero route.
- Verification of all25 serialized N5 decomposition entries and50 two-sided target-inverse entries at each of four primitive zeta5 embeddings modulo241. The nonsquare discriminant reduction is also checked. These are bounded reductions, not a fresh characteristic-zero execution.
- Exact local h24 network arithmetic and rational exponent margin. No transfer of the original label/network lemma or global recurrence is inferred.
- Declared shear ledger formulas, source-digest binding, orbit storage/output counts and several exhaustive-fixture count formulas.
- Minimal arithmetic counterexamples supporting the static API defects above, a general-purpose rank-helper early-return defect, and rational-input truncation in the orbit descriptor.

`FRESH_REVIEWER_CHECKS.json` distinguishes each scope. Only reviewer-authored metadata/arithmetic programs ran. None imports or reads source as executable input.

## Provenance, dependencies and stored results

- Every assigned local snapshot was rehashed and byte-counted. Selected archive-member identities were verified for40 hashes across24 archives. Six newer construction sources have no indexed archive occurrence; their existing standalone originals were verified instead. All38 accessible listed standalone occurrences matched their source hash.
-341 unique adjacent/contextual evidence files were captured and hashed. They are supporting historical material. Full-source-read credit applies only to the46 assigned source hashes, not to all collected documents or sibling code.
-`DEPENDENCY_RECONCILIATION.json` maps24 direct sibling dependency matches without importing them. Nine unique dependency hashes were not yet accepted in the start registry/frozen inventory; they remain a closure boundary, possibly assigned to other concurrent reviews. Runtime import resolution is untested.
-The optimizer driver S26 occurs with two distinct `multi_view` and two distinct `view_optimizer` dependency hashes. One driver hash does not define a unique historical runtime closure.
-The fixed-N5 reconstruction certificate input is byte-identical to the exact-three result: a95e7fadaebcb91b11f86cf4336b9ca0b0ba745e6cc3212c05ae501daeddd205.
-43 manifest contexts yielded697 parsed entries:564 matches,1 mismatch and132 unresolved relative references. Comparisons use verified captured non-code bytes and archive inventory metadata for uninspected sibling source; they are not blanket execution provenance.
-The mismatch is inherited `fft_phase9_unified_reuse/baseline_phase6_graph/PACKAGE_MANIFEST.json`: it declares test_log hash84dac68c… but the archive has16bc3485…. An inherited `baseline_sum_product_v8` manifest names an absent `benchmark_output.log`. Most other unresolved names are copied predecessor manifests with old relative layouts. Those are recorded as unresolved, not silently rebound by basename.

## Boundaries

Supplied-source execution/import/compilation/AST parsing: none. Historical PASS and timing reports remain historical. Authorship is preserved from the inventory and remains unresolved where it was unresolved; a first-person comment does not establish origin. Source inspection is not a universal correctness proof, a new global FFT result, or a novelty assessment. The central registry and all prior review packages were left unchanged.

Primary audit trail: SOURCE_REVIEWS.json / SOURCE_REVIEWS.md, COVERAGE.json, PROVENANCE.json, STORED_RESULT_BINDINGS.json, STORED_RESULT_NOTES.tsv, STORED_MANIFEST_RECONCILIATION.json, DEPENDENCY_RECONCILIATION.json, FRESH_REVIEWER_CHECKS.json and READ_LOG.json.
