# Degree-23 original Fourier network

An explicit inert certificate attains 16 original signed-resolvent physical banks over F_(53^23), with transform length N=13. The accepted field-uniform lower theorem gives equality in the original free-cross-singleton grammar. External independent review is pending.

- REPORT.md: exact theorem, arithmetic boundary, original grammar, transfer, and limits.
- DEGREE23_LITERAL_CERTIFICATE.json: full explicit witness, with seven actual support nodes and all raw weights.
- independent_literal_check.py: standalone standard-library JSON-only verifier, generic polynomial arithmetic and backward branch inverses.
- arithmetic_probe.cpp, check_arithmetic.py, ARITHMETIC_CHECK.json: separate multiprecision preflight with 128-bit boundary and truncation negative controls, completed before search.
- search_field.py and field_verify.py: first-irreducible modulus search and exact prime-polynomial irreducibility proof.
- search_degree23.cpp and NONSTABLE_CANDIDATE.json: deterministic first-candidate discovery using GMP unbounded exponents.
- verify_literal.cpp: full actual-root sector solves, Gauss-Jordan branch inverses, and certificate reconstruction.
- SEARCH_SCOPE.json and FAILED_PREFIX.log: finite-search provenance, with no nonexistence claim.
- OPERATION_LEDGER.md: paid preparation, representation, and evaluation costs.
- SOURCE_PINS.json and sources/: inherited accepted degree-19 and earlier source-chain bytes.
- adapt_source.py and source_rebuild_check.py: byte-exact adaptation, source/header/candidate bindings, exponent-path audit, and independent PRNG replay.
- cold_replay.py and COLD_REPLAY.json: disposable-folder arithmetic preflight, two Python certificate checks, C++ reconstruction, undefined-behavior sanitization, failed-prefix replay, and first-hit replay.
- STATUS.json and MANIFEST.json: scope-limited candidate status and final bindings.

Run python -I independent_literal_check.py for a standard-library-only certificate check. Run python -I source_rebuild_check.py and python -I cold_replay.py for complete reproducibility. Full C++ replay needs GNU C++17 and GMP development headers/libraries, linked with -lgmpxx -lgmp (tested GMP 6.3.0). Programs write receipts beside themselves; use a disposable copy for a fresh check.

The 132-bit field order exceeds unsigned128. All active C++ extension exponents are now mpz_class; no earlier 128-bit source is used as an active implementation. No external write was performed.
