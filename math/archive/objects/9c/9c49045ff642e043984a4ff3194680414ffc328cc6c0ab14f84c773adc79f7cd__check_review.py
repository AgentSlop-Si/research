"""Targeted numeric regression checks plus exact residual-support checks."""
from fractions import Fraction
from pathlib import Path
import json
import warnings
import numpy as np
from sparse_surrogate import approximate_dft_all
from scaled_adapter import scaled_approximate_dft_all


def main():
    failures = []
    for magnitude in [1e-200, 1e200]:
        x = np.full(64, magnitude, dtype=np.complex128)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            try:
                out, plan = approximate_dft_all(x, .25, .05,
                    rng=np.random.default_rng(1), return_plan=True)
                failures.append({'magnitude': magnitude, 'method': plan.method,
                    'dc_error_over_true_l2': float(abs(out[0]/(8*magnitude)-1))})
            except Exception as exc:
                failures.append({'magnitude': magnitude,
                    'exception': type(exc).__name__ + ': ' + str(exc)})
    fixed = []
    for n in [64, 1024]:
        for magnitude in [1e-200, 1.0, 1e200]:
            out, plan = scaled_approximate_dft_all(
                np.full(n, magnitude, dtype=np.complex128), .25, .05,
                rng=np.random.default_rng(1), return_plan=True)
            normalized = out / magnitude
            ref = np.fft.fft(np.ones(n), norm='ortho')
            error = float(np.max(np.abs(normalized-ref))/np.sqrt(n))
            assert np.isfinite(out).all() and error <= .25
            assert plan.plan_on_scaled_input.method != 'zero'
            fixed.append({'n': n, 'magnitude': magnitude,
                'error_over_true_l2': error,
                'method': plan.plan_on_scaled_input.method})
    # Exact rational witnesses for the stated correction-backend obstruction.
    support_checks = 0
    for n in [4, 8, 16, 32]:
        for k in range(1, n//2):
            x = [Fraction(j+1) for j in range(n)]
            y = [Fraction(0) for _ in range(n)]
            # Includes exact cancellations on some sampled coordinates.
            for j in range(k):
                y[j] = x[j] if j % 2 else -x[j]
            residual_support = sum(a != b for a, b in zip(x, y))
            b = 1 << (residual_support-1).bit_length()
            assert residual_support >= n-k > n//2 and b == n
            support_checks += 1
    result = {'status': 'PASS', 'source_range_failures_reproduced': failures,
        'scaled_adapter_cases': fixed, 'exact_rational_residual_cases': support_checks,
        'scope': 'Targeted numerical fixes and exact small support witnesses; not an exact FFT or a floating-error theorem.'}
    Path(__file__).with_name('review_checks.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'scaled_adapter_cases': len(fixed),
        'exact_rational_residual_cases': support_checks}))


if __name__ == '__main__':
    main()
