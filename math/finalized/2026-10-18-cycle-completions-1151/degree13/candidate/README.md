# Degree-thirteen original Fourier network

The explicit certificate attains sixteen original signed-resolvent physical banks over F_(53^13). The inherited field-uniform lower theorem then gives equality. External independent review is pending.

- REPORT.md: precise theorem, field, grammar, proof, transfer and limits.
- DEGREE13_LITERAL_CERTIFICATE.json: all 16 physical bank records, 208 raw weights, 208 amplitudes, 16 guards, roots, annihilator and final 169 entries.
- independent_literal_check.py: standalone standard-library checker consuming only that inert certificate; validates irreducibility and every literal branch with a backward recurrence plus both matrix products.
- INDEPENDENT_LITERAL_RESULT.json: exact second-implementation receipt. This is not external reviewer acceptance.
- verify_literal.cpp: reconstruction using actual roots and full sector systems; Gauss-Jordan verification of all literal branches.
- search_degree13.cpp: deterministic 75-bit-field search, also supplying the C++ arithmetic definitions.
- NONSTABLE_CANDIDATE.json: first split candidate, separate from the fully verified certificate.
- FIELD_IRREDUCIBILITY.json: all thirteen exact Frobenius remainders and gcd proof.
- SEARCH_SCOPE.json and FAILED_PREFIX.log: exact finite discovery scope and failed prefix; no nonexistence claim.
- OPERATION_LEDGER.md: charged representation, construction and evaluation interfaces.
- SOURCE_PINS.json and sources/: byte-bound inherited dependencies.
- COLD_REPLAY.json: isolated Python checks, fresh C++ reconstruction and fresh deterministic discovery.
- MANIFEST.json: final artifact byte bindings.

Run `python -I independent_literal_check.py` from a disposable copy. Reconstruct with `g++ -O3 -std=c++17 verify_literal.cpp -o verify_literal && ./verify_literal`. Discover with `g++ -O3 -std=c++17 search_degree13.cpp -o search_degree13 && ./search_degree13 1031`. Programs overwrite their own output receipts in the working folder. No external write was performed.
