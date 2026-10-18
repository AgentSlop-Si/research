# Integrity and isolated scientific reproduction

Run python verify_package.py from this public root. It checks the exact allowlist, root and route manifests, current seals/checksums, copy/source bindings, original-identity declarations, Python syntax, preserved chirp normalization and all final review gates. It imports no scientific program, runs no science, accesses no network, and performs no external writes.

For any scientific rerun, first copy the public packet to a disposable directory. Scientific scripts can overwrite their result files and invalidate a seal. Read each complete candidate/report and independent review for precise assumptions and dependencies. Packaging did not execute any scientific script.

- degree23/candidate contains the GMP C++ construction, literal checker, independent arithmetic checker, source rebuild checks and cold replay; the reviewer retains review_check.py, supplemental_check.py and cold_replay.py. Its immutable inputs are already included; the historical bind_inputs.py snapshot-preparation helper is unnecessary.
- mixed_prime/candidate/check_mixed_prime.py and review/independent_controls.py execute exact controls. The target minor certificate and complete proof are retained; finite controls are not the proof.
- sparse_entrywise/candidate/verify_exact.py and review/fresh_controls.py execute exact symbolic/rational controls. Source classifications remain accepted dependencies.
- dyadic_stage/candidate/verify_exact.py checks the retained parity identities. make_certificates.py regenerates them, while exploration/ contains clearly noncanonical exploratory work. The independent verifier reads proof/certificate data and does not execute candidate programs.
- correlated_precision/candidate/fresh_controls.py executes the service controls; candidate/verify_package.py performs its historical local hash/pin verification. review/independent_checks.py runs independent controls; SMALL_WIDTH_SCOPE_COUNTERCONTROL.json retains the mandatory guard-scope counterexample.
- interleaved_chirp/candidate/check_exact.py checks paid exact cores; review/independent_controls.py runs its separate controls. The canonical-complex approximation is proved through TT-SVD and exact rational sufficient-degree bounds, not executed as a numerical approximation implementation.

Historical timing/logs and original SHA values record original runs. Public source locators and source pins can produce different documentary receipts on rerun; a scientific replay should not be advertised as byte-identical to an old receipt merely because the mathematical outputs agree. The root verifier is the publication-integrity entry point.
