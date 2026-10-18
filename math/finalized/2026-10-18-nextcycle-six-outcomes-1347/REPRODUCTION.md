# Integrity and scientific reproduction

Run python verify_package.py from this public root to check the complete allowlist, all root and current route manifests, public source bindings, copy bindings, Python syntax and final review gate. It performs no scientific imports, scientific computation, network access or external writes.

For any scientific rerun, first copy the public packet into a disposable directory. Candidate/reviewer programs can overwrite their own results and will invalidate a sealed manifest. Read the individual REPORT.md and review report for exact commands and dependencies; packaging did not rerun any of them.

- degree19/candidate: standalone field/literal checks and cold replay; degree19/review: review_check.py, supplemental_check.py and cold_replay.py. Historical bind_inputs.py is unnecessary: inert inputs are already retained.
- native_product/candidate: verify_package.py is local hash verification; fresh_controls.py executes science. native_product/review/independent_cost_checks.py executes the independent controls.
- prime_cube/candidate/check_prime_cube.py and prime_cube/review/independent_controls.py execute exact controls; exploratory sampling is not the proof.
- sparse_codimension_three/candidate/verify_exact.py and review/fresh_controls.py execute the exact checks.
- centered_bv/candidate: run_example.py, fresh_checks.py and check_plans.py regenerate the expensive fixture and controls; verify_packet.py without --fresh checks the retained completed packet. Read the review for its separate independent execution/check scope.
- charzero_chirp/candidate/verify_exact.py verifies the retained exact identities without the exploratory solvers. make_certificates.py is a separate symbolic certificate-generation path, unnecessary for checking.

The root verifier is the publication-integrity entry point. Historical measured times and historical review hashes remain scientific receipts of their original runs, not performance promises or a claim of a new run on relocated files.
