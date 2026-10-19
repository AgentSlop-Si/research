# Degree-31 independent literal review

The exact scope and acceptance are in INDEPENDENT_REVIEW.md and VERDICT.json.

Minimal replay, Python standard library only:

    python -I literal_review.py inputs/DEGREE31_LITERAL_CERTIFICATE.json
    python -I cold_replay.py

Additional checks against the frozen candidate:

    python -I arithmetic_review.py candidate_snapshot
    python -I provenance_review.py candidate_snapshot
    python -I implementation_probe.py candidate_snapshot

The last command needs the existing GNU C++17 compiler and GMP development libraries; it compiles into a temporary directory. It never calls candidate discovery main. No historical witness is rerun.

The source-copy audit can verify equality to the declared original local paths when those paths remain available; SHA256 and Git-blob pins in the frozen snapshot preserve standalone provenance when not. See CANDIDATE_BINDING.json for final seals.
