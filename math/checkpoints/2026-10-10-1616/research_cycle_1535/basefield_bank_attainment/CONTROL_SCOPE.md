# Control and exploration scope

All programs in this author folder were freshly written during this research pass. They use SymPy or the Python standard library, and some import this folder's fresh_probe.py helper. No prior author/predecessor research program was executed, imported, compiled or parsed. Frozen sources were read as mathematics, inert JSON and acceptance receipts only.

## Completed exact controls

- fresh_full_control.py: exact arithmetic over Q(q), N=7 and N=11; verifies the new split-node recipes, every normalized coefficient, literal Fourier Weyl traces, every raw-weight character identity, both inverse products for all original branches, and all original Fourier entries. N7: 70 branches, 49 entries. N11: 198 branches, 121 entries. See N7_CONTROL_RESULTS.json, N11_CONTROL_RESULTS.json and full_run.log.
- fresh_n7_quadratic_specialization.py: exact coefficients, forced root, quadratic discriminant, guards and selected moment-row minors for the new eight-bank degree-2 construction.
- fresh_rational_root_specialization.py: exact parameter solve and residual quartic for the canonical N11 fourteen-bank construction forced to have roots 7, 8, followed by justified good-reduction tests of every exceptional factor. See N11_RATIONAL_ROOT_SPECIALIZATION.json.

The two preceding smaller-field specializations are proved through exact recurrences, literal bank identities and nonsingular row systems. This author pass does not claim a separate full original-matrix execution for these extension-field specializations. Their independent reviewer defines the additional control scope in its own receipt.

## Exploratory material, not impossibility or canonical construction

- fresh_small_search.py tested fixed root subsets from {q^0,…,q^(N−1)}: 21 nondegenerate N7 degree 3 candidates, 462 N11 degree 6 candidates, 462 N11 degree 7 candidates. No candidate passed every required recurrence. This is only a bounded exact search; it does not exclude any K-only bank count or other node families.
- fresh_two_root_specialization.py found an admissible N11 family specialization with forced roots q, q² and extension degree at most 24. This is a separate exploratory realization. The reviewed canonical addendum instead uses roots 7, 8 and N11_RATIONAL_ROOT_SPECIALIZATION.json. Do not mix their parameter vectors, reduced factors or guard residues.
- fresh_factor_n7.py returned the quadratic factor as irreducible over Q(q). The canonical N7 degree-exactly-2 proof uses the explicit nonsquare residue at (43, q−16), not reliance on a factorization routine.

The general 2N−4 proof is characteristic zero and all-order. Exact small examples and finite-field reviewer checks are corroboration, never a finite-field lifting argument or proof by finitely many samples. No numerical embeddings, source generators, Galois averaging, trace-as-bank operation, network publication or external file modification was used.
