# Independent ALG-064 fallback acceptance

Read REVIEW.md and ACCEPTANCE.json. Acceptance binds only the final candidate manifest recorded in FINAL_CANDIDATE_BINDINGS.json.

review_checks.py is the independently authored control suite. It uses a third pi formula and direct exact-rational DFT enclosures, imports no candidate oracle/checker, and verifies candidate hashes before and after execution. Its CAND constant points at the reviewed local candidate directory. Run with Python 3 and the standard library. Running it writes only reviewer results/logs in this review directory.

AUTHOR_REPRODUCTION_RESULTS.json verifies the separate copied-source rerun under author_reproduction/. Its output vectors match the candidate byte-for-byte. INITIAL_CANDIDATE_BINDINGS.json and PRELIMINARY_CORRECTIONS.json document the superseded first candidate and required corrections; final acceptance applies only to the final manifest.

MANIFEST.json covers all final review files except itself and bytecode caches. No external service was changed by this review.
