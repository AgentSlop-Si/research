# Simultaneous Fourier inverse-sparsity budgets

Owner: M-SPARSE-DEFECT. Candidate, ready for independent mathematical review.

Read `REPORT.md` for the equality characterization and four stated result scopes. Read `SOURCE_BINDINGS.json` for exact accepted-source bindings. `RESULTS.json` records successful exact controls, and `MANIFEST.json` binds every packet member except the manifest and its seal.

Reproduce from this directory with Python 3 and SymPy:

```sh
python verify_exact.py > VERIFY.log 2> VERIFY.stderr
```

Expected: `all_passed: true`, 149 divisor cases, 15 direct inverse cases, 208,116 exhaustive small masks, and empty `VERIFY.stderr`.

The proofs cover all stated dimensions; bounded controls are not substituted for proofs. General composite-budget classification and exact nonsharp values remain open. No external service was modified.
