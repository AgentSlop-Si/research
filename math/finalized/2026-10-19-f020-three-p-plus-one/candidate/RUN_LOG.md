# Author run log

All times UTC, 19 October 2026. All source/program paths refer to this packet unless an absolute path is given.

- 17:01: read the accepted b=3p proof and its independent acceptance. Did not run prior code.
- 17:03: exploratory reconstruction of P_10 gave Q_5 ordinary discriminant degree 140 and the two nonzero mod-2 cyclotomic remainders. Exploratory code/data are isolated under development and are not read by the final checkers.
- 17:05: `python check_uniform.py > UNIFORM_RUN.stdout 2> UNIFORM_RUN.stderr`: PASS at p=5,7,11,13,17,19,23; about 2.5 seconds.
- 17:06–17:09: an initial exact-check implementation was interrupted because expression-level expansion of products for the CD check was unnecessarily slow. No assertion failure was reported. This implementation is retained as development/check_exact.initial.py. The final program uses native Poly multiplication for the same exact equality.
- 17:09: `python check_exact.py > EXACT_RUN.stdout 2> EXACT_RUN.stderr`: PASS; about 5.1 seconds. Exact P_10/Q_5 ordinary discriminants, both necessary cyclotomic remainders, and H/CD identities at n=10,16,22 pass. SymPy version and coefficients appear in EXACT_CHECKS.json.
- 17:10: `python verify_sources.py > SOURCE_RUN.stdout 2> SOURCE_RUN.stderr`: source-manifest verification and accepted-report/review bindings checked.

No numerical root computation is used. No checker imports prior/checker code. No external writes, canonical status changes, priority changes, or novelty claims were made.
