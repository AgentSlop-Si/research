# Inverse multipliers and the fixed60 backend

This supplement addresses Q30 and Q32 of the continuous theory review. It contains complete scoped proofs, fresh independently authored controls, and explicit unresolved dependencies. It does not execute, import, compile, or AST-parse supplied research programs.

Read first:

1. `INVERSE_MULTIPLIER_CONTRACT.md`: conditional inverse error theorem; certified full-chirp sup-norm preparation; exact O(N) source-boundary coefficient/spectral preparation; Stieltjes–Wigert identification; finite-word stability and conditioning boundary.
2. `FIXED60_EXACT_AND_NORM_CERTIFICATE.md`: independent exact fixed60 coefficient/CRT proof; intermediate norm and finite-word coefficient-error bounds; the F61 source setup assertion counterexample.
3. `fresh_backend_results.json`: exact rational and modular certificates, including all72 selected central coefficients, all 36 pre/post order costs, and root-specific rank controls.
4. `fresh_chirp_results.json`: numerical sign/gcd controls, explicitly supplementary to the proofs.
5. `findings.json`: queue closure versus unresolved dispositions. Independent review metadata is added only after a reviewer returns it.

The new controls can be rerun with Python's standard library:

`python fresh_backend_certificates.py`

`python fresh_chirp_controls.py`

These are new audit programs. They do not load the supplied research modules. Their exact arithmetic is deliberately verification-oriented; run times are not benchmarks for the proposed algorithms.

Bottom line: Q32's selected mathematical backend is closed with a corrected finite-field scope. Q30's inverse application contract and some preparation subcases are closed, and general exact-field preparation now has a linear ledger. The general finite-word inverse transfer remains conditional on a stable sup-norm preparation and a useful complex spectral lower bound. Constant 60 is not an asymptotic saving. These are project proof/certificate results, not external peer review or historical-priority determinations.
