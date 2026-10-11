# Independent bounded CHIRP code review

Verdict: PASS FOR THE BOUNDED DENSE REFERENCE. Read REVIEWED_STATEMENT.md for the exact accepted scope and REPORT.md for the detailed review. Optimized and production validation remain open.

This review preserves the candidate v1 source unchanged, binds it by Library identity and archive/code hashes, independently replays the fresh author controls, and adds explicit-family exhaustive, adversarial, certificate, boundary, and resource-cutoff controls. Historical uploaded source programs remain inert.

Python 3.10 or later; standard library only. Run from this directory:

    python independent_controls.py
    python boundary_controls.py

Those commands regenerate INDEPENDENT_RESULTS.json and BOUNDARY_RESULTS.json. The distributed logs are separate shell captures of the review runs. Reruns will change provenance durations and generated result hashes. Keep the distributed immutable archive as the reviewed evidence.

The candidate/ tree is the unchanged reviewed source payload. To replay its author tests without changing the preserved test evidence, first copy candidate/ to a temporary directory and run test_chirp_exact.py there.

- REPORT.md and REVIEWED_STATEMENT.md: verdict, reasoning, exact contracts, limitations
- VERDICT.json: machine-readable disposition
- INPUT_VERIFICATION.json: pinned Library v1 readback and manifest/source verification
- INDEPENDENT_RESULTS.json and BOUNDARY_RESULTS.json: fresh independent controls
- AUTHOR_REPLAY_RESULTS.json and AUTHOR_REPLAY.log: unmodified author-suite replay
- INDEPENDENT_RUN.log and BOUNDARY_RUN.log: independent execution provenance
- ROW_GUIDANCE.json: proposed disposition only; no edits applied
- candidate/: exact candidate payload and its accepted theorem sources
- inputs/: exact candidate archive
- PACKAGE_MANIFEST.json: payload hashes

No Sheet or GitHub edits are performed by the review programs.
