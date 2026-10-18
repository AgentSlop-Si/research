# Degree-29 exact original Fourier-bank certificate

N=13 and characteristic 53 remain fixed. The new explicit field is F53[u]/(u^29+u+8).

Read REPORT.md for the theorem and exact scope, OPERATION_LEDGER.md for costs, and SOURCE_LEDGER.md for provenance. External independent review is pending.

Standalone check (Python standard library):

    python -I independent_literal_check.py
    python -I witness_structure_check.py
    python -I check_convolution_boundary.py

Complete cold replay (GNU C++17 and GMP development libraries also required):

    python -I cold_replay.py

Source adaptation and inherited byte bindings:

    python -I source_rebuild_check.py

The active Python literal checker uses ordinary coefficient convolution. The boundary audit demonstrates corruption of 16-bit packed coefficients at degree 29 and verifies 17-bit replacement arithmetic. All active C++ order-derived exponent paths use GMP mpz_class.

The manifest excludes compiler binaries and caches. No external write was performed by this task.
