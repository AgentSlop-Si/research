# Reproduce the lower bound

These independently authored controls prove the exact two-row incompatibility and check the literal signed-bank model. They are separate from all author and predecessor research programs.

Requirements: Python 3 and SymPy. Make a disposable copy of this directory before running the controls, because they regenerate result JSON files beside themselves.

    python verify_isolated_rows.py
    python verify_literal_model.py

The first control derives both isolated rows, verifies U R + V F = 1 over Q(q), and computes the modular resultant and Sylvester determinant. The second verifies the literal resolvent expansion, all target trace coefficients, the transpose/reflection symmetries and unique corner supports. Exact certificate and result JSON files are included.

The two JSON files under sources are inert frozen author coefficients and modular certificate data. FROZEN_COMPARISON_RESULTS.json records the accepted independent comparison, including equality of all 81 quotient-matrix entries. No author research program is included or required.

See the [proof](../../notes/01_lower_bound.md) and [scoped acceptance](../../receipts/lower_acceptance.json).
