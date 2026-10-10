# Quick reproducibility

```bash
cd hero17_phase9_root_exchange
python -m unittest discover -v
python independent_audit.py
```

The standalone module `phase9.py` has no external imports beyond the Python standard library. It needs an even N, a prime p with N | (p-1), and a supplied primitive Nth root w in Fp. The `fixture(N)` function chooses tiny research fields only for tests.

To inspect one-swap scaling and honest end-to-end comparisons, see `AUDIT_RESULTS.json`. Numbers are exact counts of scalar modular additions/multiplications in the Python execution ledger, not wall-clock speed and not an optimized FFT lower bound. Modular inversions are counted separately.
