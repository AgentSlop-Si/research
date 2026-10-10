# Reproduction

From the extracted package directory:

```bash
python -m unittest discover -v
python independent_audit.py
```

The first command runs 14 exact regression test groups. The second independently checks 110 complete projector transforms, 120 commutativity cases, 120 correction-rank cases, a complete length-65536 output against a separate iterative NTT reference, 39 direct Fourier-bin residual checks at that length, and an eight-output sharing experiment. The audit overwrites `AUDIT_RESULTS.json`.

All arithmetic is exact modulo a suitable prime; the implementation does not call NumPy, SciPy, FFTW, network APIs or hidden FFTs in the **new projector executor**. The independent oracles intentionally use direct DFTs and FFTs.

The operation ledger counts field additions, multiplications, root setup, constant inverse exponentiation, primitive-root validation, and output writes. Integer indexing is tracked separately. A supplied prime field is part of the model, not built for free.
