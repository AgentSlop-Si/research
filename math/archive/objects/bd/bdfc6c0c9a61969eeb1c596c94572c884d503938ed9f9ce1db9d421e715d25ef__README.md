# Exact Fourier sparse-jet lifting — research checkpoint

**No new sub-NlogN FFT is claimed.** This package proves an exact promise-to-full-input reduction and implements its scalar-arithmetic compiler.

- `THEORY.md`: theorem, proofs, complete model, scoped synthesis barriers, and the missing construction.
- `circuit.py`: scalar straight-line circuits, origin-regular Hessian-vector compiler, independent bivariate formal jets, and explicit positive/negative-control potentials.
- `verify.py`: seven exact test groups; standard library only.
- `RESULTS.json`: recorded fresh test run.
- `SOURCE_LEDGER.md`: sources actually accessed and coverage limitations.

Run:

```bash
python verify.py
```

The constructed four-point source is a classical finite control. Larger Fourier-positive sources intentionally use quadratic-size direct quadratic forms. They do not establish the desired asymptotic upper bound. The linear-size prefix-square controls have dense full-rank Hessians, but compute a different matrix.
