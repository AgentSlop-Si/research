# Reproduction entry points

Use a disposable copy: these commands can overwrite receipts. Python 3.12 was used for the recorded checks; the rank-two and sparse-mask suites require SymPy. Degree-seventeen C++ reconstruction requires GNU C++17. The root integrity check needs only Python's standard library.

## Integrity only

From the packet root, run `python verify_package.py`. This checks the allowlist, all public bytes, nested public manifests, portable source metadata and syntax. It performs no scientific computation or network request.

## Scientific checks

- Degree seventeen: `python -I degree17/candidate/independent_literal_check.py`; independent review: `python -I degree17/review/review_check.py`. Full reconstruction/discovery replay: `python -I degree17/candidate/cold_replay.py`. These are expensive exact checks, distinct from packaging.
- Mersenne: `python mersenne_stream/candidate/fresh_controls.py`; independent suite: `python mersenne_stream/review/independent_checks.py`. Candidate source/package bindings: `python mersenne_stream/candidate/verify_package.py`.
- Centered: from centered_integration/candidate run `python run_integration.py`, `python check_retained_outputs.py`, `python check_boundary_controls.py`, then `python verify_packet.py --fresh`. Independent retained arithmetic: `python centered_integration/review/independent_audit.py`; second 320-bit oracle: `python centered_integration/review/independent_oracle_crosscheck.py`. Run independent checks against the pristine disposable candidate before a timed rerun changes its manifest-bound receipts, or rebuild a new explicit local manifest for that new run.
- Rank two: `python rank_two/candidate/check_rank_two.py`; independent suite: `python rank_two/review/independent_controls.py`.
- Sparse masks: `python sparse_masks/candidate/verify_exact.py`; independent suite: `python sparse_masks/review/fresh_controls.py`.
- Persistent cache: `python persistent_cache/candidate/check_cache.py`; independent suite: `python persistent_cache/review/independent_checks.py`.

If a candidate run regenerates a manifest-bound file, the old integrity manifest must correctly fail afterward. Use a fresh disposable copy for each suite or create new clearly labelled receipts/manifests. Never overwrite the published evidence and call it the original review.
