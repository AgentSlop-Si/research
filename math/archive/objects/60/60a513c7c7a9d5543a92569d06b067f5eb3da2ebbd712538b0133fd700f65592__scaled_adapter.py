"""Range-safe wrapper around the supplied numerical surrogate prototype.

Place the source archive on PYTHONPATH. This does not edit or replace it.
The wrapper prevents the reproduced norm underflow/overflow failures by
working on a normalized vector. It is still a floating-point approximation,
not a finite-precision proof or an exact-complex FFT implementation.
"""
from dataclasses import dataclass
from numbers import Integral
import math
import numpy as np
from sparse_surrogate import approximate_dft_all


@dataclass(frozen=True)
class ScaledPlan:
    input_scale: float
    plan_on_scaled_input: object


def scaled_approximate_dft_all(x, epsilon, delta, **kwargs):
    epsilon, delta = float(epsilon), float(delta)
    if not 0 < epsilon < 1 or not 0 < delta < 1:
        raise ValueError('epsilon and delta must each lie in (0,1)')
    samples = kwargs.get('samples')
    if samples is not None and (not isinstance(samples, Integral)
                                or isinstance(samples, (bool, np.bool_))
                                or samples < 1):
        raise ValueError('samples must be a positive integer')
    a = np.asarray(x, dtype=np.complex128)
    if a.ndim != 1 or a.size < 1 or a.size & (a.size - 1):
        raise ValueError('x must be a nonempty power-of-two 1-D vector')
    if not np.isfinite(a.real).all() or not np.isfinite(a.imag).all():
        raise ValueError('x must be finite')
    # Use component maxima: complex magnitude itself can overflow near the
    # largest finite representable value. Divide real/imag separately so
    # implementations cannot first form a reciprocal of a subnormal scale.
    scale = float(max(np.max(np.abs(a.real)), np.max(np.abs(a.imag))))
    scaled = np.zeros_like(a)
    if scale:
        scaled.real = a.real / scale
        scaled.imag = a.imag / scale
    want_plan = bool(kwargs.pop('return_plan', False))
    output, plan = approximate_dft_all(scaled, epsilon, delta,
                                       return_plan=True, **kwargs)
    output = output * scale
    wrapped_plan = ScaledPlan(scale, plan)
    return (output, wrapped_plan) if want_plan else output
