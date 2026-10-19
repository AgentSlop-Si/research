# Independent prime-power review packet

Read `REVIEW.md` for the mathematical audit and exact acceptance scope.

- `independent_checks.py`: newly authored independent exact controls, Python standard library only.
- `INDEPENDENT_RESULTS.json`: fresh results and exact test counts.
- `INDEPENDENT_DESCENT_CERTIFICATES.json`: every independent descent state.
- `INDEPENDENT_ORIGINAL_MODEL.json`: exact connected inverse witness and both Gram orders.
- `candidate_frozen/`: unchanged frozen candidate and its original seal.
- `candidate_replay/`: isolated replay of the candidate's new checker.
- `CANDIDATE_BINDING.json`: pinned candidate hashes.
- `CANDIDATE_REPLAY_COMPARISON.json`: byte-identical output verification.
- `VERDICT.json`: machine-readable acceptance and exclusions.
- `MANIFEST.json` and `SEAL.sha256`: review packet integrity.

Reproduce the independent checks with `python independent_checks.py` from this directory. No historical checker or external action is needed.
