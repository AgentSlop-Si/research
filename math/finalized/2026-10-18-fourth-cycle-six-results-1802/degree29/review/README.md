# Degree-29 independent final review

Verdict: ACCEPT_SCOPE_LIMITED. Read INDEPENDENT_REVIEW.md for the theorem, inherited lower-bound dependency, arithmetic controls, and exclusions.

Standalone mathematical replay: `python -I review_check.py`.
Supplemental modulus-search, packing, exponent, and provenance checks: `python -I supplemental_check.py`.
Isolated cold replay, fresh GMP/UBSan probe, and executable unsafe-16-bit controls: `python -I cold_replay.py`.

The mathematical checker reads only inert certificate JSON, uses safe 17-bit packed convolution with ordinary-convolution differentials, polynomial-Euclidean inversion, and explicit geometric-power branch inverses. No candidate discovery or literal-verification program is imported or executed.
