# FFT frequency-shift median research v5

This bundle continues the sparse-surrogate FFT research after the v4 coordinate-sampling barrier.

## Main result

For `N=K*M`, one randomized full-output Fourier estimate is computed with

```text
O(N log M + (N/M) log(N/M) + N)
```

complex arithmetic operations. It is unbiased and every output has the exact variance

```text
(M-1) ||x||_2^2 / N.
```

The coordinatewise median of `2t-1` independent estimates has a rigorous simultaneous all-output bound. A balanced-bucket extension replaces `M-1` by a tunable collision factor `c-1`; after all long FFTs are charged, it gives the same asymptotic tradeoff as selecting a smaller `M`. With suitable growing `M`, the arithmetic count is `o(N log N)` for arbitrary fresh dense inputs, but the result is approximate—not an exact or machine-precision FFT.

## Files

- `RESEARCH.md` — derivation, theorem, complexity, experiments, limitations, and next steps.
- `prototype.py` — readable implementation plus reproducible experiments.
- `results.json` — saved experiment output.
- `test_checkpoint.py` — automated algebra, variance, and scaling checks.

## Run

```bash
python prototype.py --output results.json
python test_checkpoint.py
```

Requires Python 3.10+ and NumPy.
