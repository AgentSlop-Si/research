# ALG-WEIL-LOCAL: exact corrected implementation acceptance

Prepared 18 October 2026 UTC. Explicit user authorization to execute this exact downloaded package was received before the run.

## Verdict

**PASS the exact corrected-derivative finite implementation gate.** The unmodified, hash-pinned package completed all 13 named test groups, its supplied independent verifier, its result builder, and its source-manifest check. A separately authored oracle then accepted newly observed candidate matrices and emitted records with 102500 actual assertions. No implementation patch was required.

This closes only the corrected-derivative 13-group acceptance interface. It does not replay the original historical exhaustive sources or recover the earlier API/review bytes. ALG-WEIL-LOCAL remains a broader TO RESEARCH owner at priority 42 unless the parent record is explicitly narrowed; Q18 remains a separate priority-37 view. No automatic parent closure follows.

## Immutable source

Archive: [fft_local_ring_weil_v25_signfix.zip](https://github.com/AgentSlop-Si/research/blob/7e13f9ff8c4f8bdd64d5068fcdc7ce03342078cb/math/finalized/2026-10-16-source-repairs-0126/weil_static/fft_local_ring_weil_v25_signfix.zip).

- Repository commit: 7e13f9ff8c4f8bdd64d5068fcdc7ce03342078cb.
- Archive Git blob: 70d29013db10fc0707cf5eb65b0e2d71119e6207.
- Archive size: 257283 bytes.
- Archive SHA-256: e159b6a6148c8020c925afc7f56ea50d4362e64a86988c2cacd58b80eb09a556.
- local_ring_weil.py SHA-256: 259b8047681ea555152e31c921f13653964cdcb09cc4a9ba9d40f4b2dc56266e.
- test_checkpoint.py SHA-256: b5f408217bf20a1abd8cc6d102b627493851124e61331badb4321e4c83ddd810.
- run_all.py SHA-256: 07cb7600f1bc7ffef82c7c7d5be15e219ea7316f8dca40d0a162a5f0a62cf0e7.

SOURCE_BINDINGS.json and INPUT_HASHES.json bind the interpreter and all 17 source members. Every member was rehashed before execution and after independent checking. All 16 entries in the package manifest passed both the unchanged driver and independent checking. All five historical_outputs files and the nested predecessor ZIP remain byte-identical.

The controlling mathematics is the [accepted negative-chirp proof and gate](https://github.com/AgentSlop-Si/research/blob/a4dacc1f15eb910ec7d494f1572bc044e2d0533b/math/finalized/2026-10-17-accepted-next-gates-1256/scientific_packet/weil_fresh_checks_20261017_1203/PROOF_AND_GATE.md). This execution accepts the implementation only at its stated finite interface and conventions; the uniform mathematical conclusion remains supplied by that proof.

## Execution and containment

The exact source was copied into a new work directory. No package source was edited. The 17 source-member paths were individually bind-mounted read-only under a fresh writable output directory inside a bwrap filesystem/process/user/UTS/IPC sandbox. Historical files and the predecessor ZIP were among these read-only mounts.

The launcher used an empty environment with explicit HOME, TMPDIR, PATH, locale, deterministic Python hash seed, disabled user-site imports, and bytecode writes disabled. Assertions were enabled. Limits were 180 seconds wall time with a five-second termination grace period, 120 seconds CPU per process, 512 MiB address space per process, 16 MiB per file, 128 open files, and no core dumps. No package installation, system/security-setting change, or network API was used. Networking inherited the existing environment restrictions; no independent network namespace or stronger network isolation is claimed.

Observed interpreter: Python 3.12.14. Exact interpreter path, full bwrap/limit/environment arguments, timestamps, and exit statuses are retained in RUN_RECORD.json.

Executed outer command:

    python -I -S launch_authorized.py

The unchanged package entry point was:

    python -B -s run_all.py

Its unchanged driver invoked the same interpreter on:

    test_checkpoint.py
    independent_verifier.py
    build_results.py

The driver then checked its static manifest. Driver start: 2026-10-18 19:30:49.898187 UTC. Finish: 19:30:50.591100 UTC. Exit status: 0. Measured elapsed time including launch/containment: approximately 0.693 seconds. The unittest log reports 13 tests in 0.342 seconds. These are observations for this finite run, not asymptotic or production-speed claims.

Complete new logs: logs/run_all.stdout.log and logs/run_all.stderr.log. No historical log was used as fresh evidence.

## Actual 13-group results

All of the following names occur exactly once with an “ok” verdict in the fresh unittest log:

1. test_congruence_parabolics_are_subgroups — PASS.
2. test_cross_ratio_has_exact_residual_root_order — PASS.
3. test_double_cosets_can_refine_valuation_but_not_core_size — PASS.
4. test_exact_support_hierarchy — PASS.
5. test_full_fourier_weyl_element_is_outside_easy_subgroup — PASS.
6. test_gauss_kernel_and_closed_form_agree — PASS.
7. test_nonunit_cell_factorization — PASS.
8. test_operation_ledger — PASS.
9. test_predecessor_archive_present_and_hashed — PASS.
10. test_sl2_valuation_counts — PASS.
11. test_upper_shear_has_negative_chirp_convention — PASS.
12. test_upper_shear_signed_phase_for_every_q9_scalar — PASS.
13. test_upper_shear_weyl_covariance_label — PASS.

The fresh independent oracle compared these names with the inert test source's actual method definitions. Acceptance does not rely on the result builder's hard-coded “13”.

The suite covers representative upper-shear scalars for q=9,25,27,49; all nine scalars at q=9, including negative representatives; five explicit negative-versus-positive chirp controls; signed residual ratios; covariance; exhaustive SL2 enumeration at q=9,25; bounded q=9 subgroup and double-coset checks; a seeded q=27 subgroup product; operation-count formulas; and the predecessor archive hash. The larger dimensions 729 and 625 occur only in operation-ledger formulas.

## Fresh emitted records and the historical-equality nuance

All three mutable top-level records were absent from the pinned input archive's top level and were freshly produced by the authorized run:

- work/results.json: SHA-256 5f3a62ebc5133da259a87a583567ba0775dcd6f71bafb2dfb8a20bba0f031bd0.
- work/independent_results.json: SHA-256 1971f61cdfaf071d604fac695d367882e9167972eef9e08dda7f2ba6311840d3.
- work/RESULT_SUMMARY.json: SHA-256 c2f22df52ea4ed834d9b91f5dd1882834d9f24fb0229e2318d49928cb0408484.

The first two freshly emitted files are byte-identical to their preserved historical counterparts. This is expected: they record support sizes, root orders, group counts, and other sign-insensitive invariants. The summary changes the automated test count from 10 to 13. Differing output bytes are therefore not the sign-repair certificate. The new sign-sensitive test log and independent candidate-matrix observations establish that evidence.

The independent checker accepted exactly 13 hierarchy rows and 13 supplied-verifier support rows, with the prescribed (p,k,v) domains, blocks=p^v, block length/support/root order=p^(k-v), and dense arithmetic terms=(k-v)*p*p^k. It checked the fresh summary against observed tests and record domains.

Fresh q=9 group records agree with an independent tuple enumeration: SL2 size 648; valuation counts 486,108,54; level-one subgroup size 162. Independent q=25 enumeration gives size 15000 and valuation counts 12500,2000,500. The q=25 independent census is additional finite corroboration of that test, not a claimed emitted q=25 record.

The fresh q=9 lower-Borel double-coset records match independent reconstruction: (valuation,size)=(0,486),(1,54),(1,54),(2,54). The independently reconstructed congruence subgroups have sizes 162 and 54, with all 216 inverses and 29160 ordered products checked.

## Independent candidate observation and oracle

The new adapter checks/observe_q9_candidate.py contains no acceptance oracle. Under the same source-read-only containment and resource limits it imported the authorized core and emitted all three candidate matrix constructions for b=-9,...,17 at q=9. This includes every canonical scalar, every negative representative b-q, and every positive representative b+q without introducing another size suite.

The adapter's exact command, hash, timestamps, and exit status 0 are in OBSERVATION_RUN_RECORD.json. Its complete matrix record is logs/candidate_q9.stdout.json; stderr is retained separately. The observed coefficient field is F_19 with root 4.

The newly written checks/independent_acceptance.py imports no package module. It reads records as data, independently checks prime modulus and exact root order, computes a direct circulant kernel from the accepted negative-chirp formula, and independently reconstructs tuple-based groups. Its source SHA-256 is a8448af47e81f0b27e2c9974b08e8f716083336b3a9a972417a01e574b23111a.

Executed oracle command:

    python -I -S checks/independent_acceptance.py

Exit status: 0. Complete stdout/stderr are retained in logs/independent_acceptance.stdout.log and logs/independent_acceptance.stderr.log. INDEPENDENT_ACCEPTANCE.json contains all counts and exact verdicts.

The oracle passed 102500 actual assertions, including:

- 6561 entrywise comparisons: 27 scalar representatives × three candidate constructions × 81 entries.
- 59049 covariance entry comparisons: all b,a,c,x,y modulo 9, using U_b D(a,c)=D(a+bc,c)U_b.
- 6561 additive-composition entry comparisons: all b,c,x,y modulo 9.
- 729 exact support-locus comparisons and the identity case.
- Eight exact signed cross ratios, eight exact residual-order checks, and rejection of the positive-chirp model for every nonzero q=9 scalar.
- Independent finite-field/root validation, group census, subgroup closure, double-coset reconstruction, record validation, actual test-name checking, and source/history preservation.
- Controls rejecting a changed matrix entry, wrong scalar dispatch, and a stale 10-test summary.

The supplied independent_verifier.py is an additional separate implementation within the same recovered package. It is not counted as a substitute for this newly authored data-only oracle. Likewise, the 102500 checks above are separate from the supplied suite; no inflated claim about the original 13 groups' internal assertion count is made.

## Acceptance boundary

Accepted: execution of the exact corrected derivative; all 13 named groups; supplied verifier and result emission; independent signed q=9 matrix/dispatch/covariance/additive controls; fresh record validation; preserved original source and historical evidence.

Not accepted by this result: replay of the original positive-sign source or original historical exhaustive logs; recovery of unrecovered earlier API/review bytes; malformed-input qualification; characteristic-two or general symmetric-congruence extensions; all global Weil normalization relations; numerical production qualification; full preparation/bit/storage costs; historical novelty; unrestricted evaluator lower bounds; or a faster general FFT.

No repair was necessary, and the fixed finite gate stops here. The original source identities, priorities, history, and unrelated obligations remain intact. No repository or workbook was edited by this worker.
