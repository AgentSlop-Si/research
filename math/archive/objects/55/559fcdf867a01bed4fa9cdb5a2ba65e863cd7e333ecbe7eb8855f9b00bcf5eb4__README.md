# Certified growing-fiber FFT

Exact sparse-intermediate Fourier algorithm with proven cost

    O(N log(b+2) + sqrt(N)*b^2).

For b=polylog(N), this is O(N log log N) on the certified input class. **Generic inputs do not satisfy this promise; the optional full FFT fallback retains O(N log N) worst-case cost.** This is not a new unrestricted FFT bound. Publication novelty is unverified.

Files:

- `THEORY.md`: model, full construction, proofs, limits and prior-art distinctions.
- `fiber_fft.py`: standard-library-only finite-field implementation.
- `verify.py`: exact reproducible tests and operation profiles.
- `RESULTS.json`: recorded output.
- `SOURCE_LEDGER.md`: project review coverage and source limitations.

Run from this directory:

```bash
python verify.py
```

Example:

```python
from fiber_fft import certified_fiber_fft, make_fiber_signal

p, N = 65537, 64
w = pow(3, (p-1)//N, p)  # This prime/root choice is a test fixture.
Q, M, b = 8, 8, 2
modes = [[(t, 5), ((t+1) % M, 1)] for t in range(Q)]
x = make_fiber_signal(N, p, w, modes)  # Input generator, not part of recovery.

result = certified_fiber_fft(x, p, w, b, fallback=True)
print(result['accepted'])
print(result['output'])
print(result['count'])
```

The transform receives only the raw x, not `modes`. `green=True` instead tests the fibers of P*x, where P=7I+S+2D^-1, and recovers F*x by the certified L^-1 recurrence. Some finite-field/length parameters may make a Green denominator singular; such choices raise an explicit error. Arbitrary floating-point inputs are not supported by this exact recognizer.

The counts use unit-cost field operations. They are not hardware instructions or a bit-complexity/time comparison with FFTW. The largest recorded structured case remains 2.4% above the included full-radix arithmetic baseline despite the better asymptotic bound.

## Total budget instead of a cap on each fiber

`certified_aggregate_fft(x,p,w,total_budget=K0,green=False,fallback=False)` accepts exactly when the sum of internal fiber mode counts is <=K0. It permits fully dense individual fibers. It has O(N log log N) asymptotic success-or-rejection work when K0=O(sqrt(N)*polylog(N)), with all heavy full transforms charged. See THEORY.md Section 9 for the bound including finite-size thresholds. This is still not an unrestricted fast FFT. Recorded operation-comparison profiles use the simpler per-fiber-cap variant.
