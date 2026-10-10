# Reproduction

From the root of the outer ZIP:

```sh
bash RUN.sh
```

The tests use `numpy`, `scipy`, and `mpmath`; installed versions can be newer. The exact finite-field certificate code uses only the Python standard library and the two inherited Phase 40 helper files; the numerical synthesis requires NumPy/SciPy. No network access or external service is needed.

Fast manual commands from the Phase 41 directory:

```sh
OPENBLAS_NUM_THREADS=1 python -m unittest -v tests_phase41
python phase41_exact_jacobian.py
python phase41_three_exact.py
python phase41_arbitrary_amplitude.py
OPENBLAS_NUM_THREADS=1 python phase41_full_audit.py
OPENBLAS_NUM_THREADS=1 python phase41_high_precision.py
```

A high-precision Newton residual is NOT a proof of a nearby exact solution absent certified convergence bounds. Do not interpret it as an all-input FFT identity. Complete Phase 40 preservation is in `previous_full_phase40_checkpoint.zip`.
