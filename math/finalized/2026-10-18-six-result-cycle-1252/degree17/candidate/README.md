# Degree-seventeen original Fourier network

The explicit certificate attains sixteen original signed-resolvent physical banks over F_(53^17), still at transform length N=13. The inherited field-uniform lower theorem gives equality in the free-cross-singleton grammar. External independent review is pending.

- REPORT.md: exact theorem, field, physical grammar, verification, transfer and limits.
- DEGREE17_LITERAL_CERTIFICATE.json: complete inert JSON witness.
- independent_literal_check.py: standard-library literal checker with generic polynomial arithmetic and backward inverse recurrence; consumes only inert JSON.
- field_verify.py and FIELD_IRREDUCIBILITY.json: exact prime-polynomial irreducibility proof.
- verify_literal.cpp: root factorization, all actual-root sector solves, all literal branch inverses by Gauss-Jordan, and certificate reconstruction.
- search_degree17.cpp and NONSTABLE_CANDIDATE.json: deterministic 98-bit-field discovery.
- SEARCH_SCOPE.json and FAILED_PREFIX.log: bounded discovery scope and failed-prefix evidence, with no impossibility claim.
- OPERATION_LEDGER.md: charged representation, construction and evaluation costs.
- SOURCE_PINS.json and sources/: byte-bound inherited source chain.
- cold_replay.py and COLD_REPLAY.json: disposable-folder reconstruction and two isolated certificate checks, exact discovery and failed-prefix replay.
- STATUS.json and MANIFEST.json: explicit candidate status and final artifact bindings.

Run python -I independent_literal_check.py from a disposable copy. For all reconstruction and replay checks, run python -I cold_replay.py. Programs write their output receipts beside themselves. GNU C++17 and the Python standard library suffice. No external write was performed.
