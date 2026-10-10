# Reproduce Hero #1 Phase 28

Use Python 3.11+ and `sympy` (for the characteristic-zero proof). There are no network dependencies at runtime. Run commands in the extracted `fft_hero1_phase28` directory:

```sh
python -m unittest -v test_phase28
python baseline/fft_hero1_phase27/test_phase27.py -v
python symbolic_check.py
python weave_optimizer.py
python audit_phase28.py
python benchmark_phase28.py
```

The matrix audit and benchmark write their JSON results alongside their scripts, so the package runs from any extraction directory. Arithmetic and correctness do not depend on those output files.

`audit_phase28.py` independently checks `pow(omega,j*k,p)` against each circuit on all basis vectors in two prime fields. `symbolic_check.py` verifies codelet identities using exact `QQ[z]/Φ_n(z)` quotient arithmetic. Root-selection validity is checked by the original plan. The prior archive retains previous code and results untouched.

The operation counters are **field-arithmetic proxies**. They do not include integer indexing, memory traffic, primality certification, word/bit complexity or floating-point errors. The source and results are provided for independent mathematical inspection, not as proof of historic novelty.
