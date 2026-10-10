# Reproduction

From extracted archive root:

```bash
python -m unittest -v test_phase16
python independent_audit.py
```

Expected: **19 test groups**, audit `PASS`, `120` complete direct-DFT comparisons, `1,368` complete-transform coefficients, `4,912` exhaustive nonzero 3-coordinate vectors over GF(17), six finite-field denominator rank cases and 13 Harper matrix-algebra classifications.

To rerun predecessor:

```bash
mkdir -p old
python -m zipfile -e PHASE15_PREDECESSOR.zip old
(cd old && python -m unittest -q test_phase15)
```

Expected predecessor: **21 tests**.

Use `PROOF_CERTIFICATE.md` rather than finite tests for all-N mathematical claims. No O(N) general FFT algorithm is implemented.
