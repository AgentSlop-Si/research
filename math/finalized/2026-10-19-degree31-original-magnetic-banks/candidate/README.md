# Degree-31 original-bank finite certificate

Start with REPORT.md. The main deliverable is DEGREE31_LITERAL_CERTIFICATE.json, with all actual field roots, sixteen original banks and every raw weight.

The minimal independent-style literal replay is `python -I independent_literal_check.py` with that JSON beside the script. It proves field irreducibility first, then checks both inverse orders, all sectors and all target entries using only Python's standard library. It does not execute inherited source code.

Read ARITHMETIC_PROOF.md for the 178-bit and actual-modulus arithmetic proof, OPERATION_LEDGER.md for preparation/application costs, SEARCH_SCOPE_AMENDMENT.json for the same-field modulus representation change, and SOURCE_PINS.json for source provenance. FIRST_HIT_REPLAY.json records a fresh complete failed-prefix/first-hit replay.

Candidate checks are not independent-review acceptance. Use the separate scope-limited independent review supplied alongside this directory for that decision. No owner closure or general field classification is asserted.
