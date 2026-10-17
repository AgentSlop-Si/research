"""Q16 BUCKETS candidate. Exact dyadic data path; paid, certified preparation.

This module does not recover frequencies, draw randomness, normalize/scan the
source, implement a dense fallback, or accept caller-prepared taps or roots.
The unchanged accepted compact_window module is the sole window dependency.
"""
from dataclasses import dataclass
from compact_window import (Ledger, WindowSpec, Interval, Scalar,
                            prepare_window, nearest_even, CertificationError)


def nat(value, name, L, minimum=0):
    L.parameter(value)
    if value < minimum:
        raise ValueError(name + ' below domain')
    return value


@dataclass(frozen=True)
class DyadicSource:
    """Already represented immutable random-access input, not a validation pass.

    values[t] is ((real_numerator, real_exponent), (imag_numerator, imag_exponent)).
    Every exponent is in [0, fractional_bits_bound], and |n| <= 2**exponent.
    The complete source's prior validation/norm guarantee belongs to the caller.
    Only queried entries are checked and aligned; no callback is accepted.
    """
    values: tuple
    fractional_bits_bound: int


@dataclass(frozen=True)
class CertifiedReal:
    numerator: int
    bits: int
    enclosure: Interval
    error_units: int  # On the enclosure grid, NOT on the output grid.


@dataclass(frozen=True)
class CertifiedRoot:
    real: CertifiedReal
    imag: CertifiedReal


@dataclass(frozen=True)
class BucketResult:
    numerators: tuple
    bits: int


def rounded_enclosure(a, bits, L):
    if a.bits < bits:
        raise ValueError('rounding must coarsen the enclosure grid')
    unit = L.shift(L.sub(a.bits, bits))
    n = nearest_even(L.add(a.lo, a.hi), L.mul(2, unit), L)
    center = L.mul(n, unit)
    error = max(abs(L.sub(center, a.lo)), abs(L.sub(center, a.hi)))
    L.event('certified_scalar_round')
    return CertifiedReal(n, bits, a, error)


def finite_isqrt(n, L):
    """Greedy root bits; fixed ceil(bit_length(n)/2) iterations, no tolerance loop."""
    if type(n) is not int or n < 0:
        raise ValueError('nonnegative integer square-root argument required')
    L.record('sqrt_input', (), n)
    root = 0
    steps = L.div(L.add(n.bit_length(), 1), 2)
    for j in range(steps - 1, -1, -1):
        trial = L.add(root, L.shift(j))
        if L.mul(trial, trial) <= n:
            root = trial
        L.event('sqrt_bit')
    # These checks are unreachable failures for valid integers, not abort policy.
    upper = L.add(root, 1)
    if not L.mul(root, root) <= n < L.mul(upper, upper):
        raise CertificationError('integer square-root invariant')
    return root


def prepare_scale(M, P, K, L):
    square_scale = L.shift(L.mul(2, K))
    floor_target = L.div(square_scale, M)
    low = finite_isqrt(floor_target, L)
    exact = L.mul(L.mul(low, low), M) == square_scale
    high = low if exact else L.add(low, 1)
    a = Interval(low, high, K)
    value = rounded_enclosure(a, L.add(P, 2), L)
    if value.error_units > L.shift(L.sub(K, P)):
        raise CertificationError('scale rho certificate')
    L.event('scale_preparation')
    return value


def prepare_roots(B, P, L):
    Q = L.add(P, 2)
    J = L.add(P, 8)
    K = L.add(J, L.add(L.mul(2, L.add(J, 1).bit_length()), 16))
    if L.mul(64, L.add(K, 9)) > L.shift(L.sub(K, J)):
        raise CertificationError('root working precision guard')
    scalar = Scalar(K, L)  # No hidden cached pi/roots, even after window construction.
    roots = []
    count = L.div(B, 2)
    L.allocate(count)
    for j in range(count):
        # exp(-2 pi i j/B); exact sine argument reduction includes all axes.
        real_interval = scalar.sin_pi(L.add(B, L.mul(4, j)), L.mul(2, B))
        imag_interval = scalar.sin_pi(L.mul(-2, j), B)
        real = rounded_enclosure(real_interval, Q, L)
        imag = rounded_enclosure(imag_interval, Q, L)
        error_sq = L.add(L.mul(real.error_units, real.error_units),
                         L.mul(imag.error_units, imag.error_units))
        if error_sq > L.shift(L.mul(2, L.sub(K, P))):
            raise CertificationError('complex root rho certificate')
        roots.append(CertifiedRoot(real, imag))
        L.event('fft_root_preparation')
    L.allocate(count)  # Retained tuple copy, as a cumulative upper charge.
    return tuple(roots), K


class BucketEngine:
    """One paid preparation followed by bounded exact BUCKETS calls.

    The constructor creates its own prepared state. That state is not a public
    deserialization interface; replacing private state is outside the contract.
    Provide a shared Ledger only to retain already-paid theorem_spec work.
    """
    def __init__(self, spec, ledger=None):
        self.ledger = ledger if ledger is not None else Ledger()
        L = self.ledger
        L.event('bucket_engine_constructor')
        if type(spec) is not WindowSpec:
            raise ValueError('exact WindowSpec required')
        self._window = prepare_window(spec, L)
        self._spec = spec
        self._roots, self._K = prepare_roots(spec.B, spec.P, L)
        self._scale = prepare_scale(spec.M, spec.P, self._K, L)
        self._b = L.sub(spec.B.bit_length(), 1)
        self._Q = L.add(spec.P, 2)
        # General bound, including reduced fixtures for which b*rho is not small.
        # A=2M^2, D=2W*rho; E=(A+D)*(1+rho)^(b+1)-A+rho.
        R = L.shift(spec.P)
        A = L.mul(2, L.mul(spec.M, spec.M))
        p = L.add(self._b, 1)
        n = L.power(L.add(R, 1), p)
        ebits = L.mul(spec.P, L.add(self._b, 2))
        den = L.shift(ebits)
        e = L.add(L.sub(L.mul(L.add(L.mul(A, R), L.mul(2, spec.W)), n),
                        L.mul(A, den)), L.shift(L.sub(ebits, spec.P)))
        self._error_numerator, self._error_bits = e, ebits
        accepted_n = L.mul(L.mul(24, L.add(spec.m, 1)), L.mul(spec.M, spec.M))
        self._accepted_error = e <= L.mul(accepted_n, L.shift(L.sub(ebits, spec.P)))
        # E plus ideal output bound A also bounds final complex magnitude.
        self._output_bound_numerator = L.add(L.mul(A, den), e)
        L.event('bucket_error_bound_preparation')

    def run(self, source, sigma, tau):
        L = self.ledger
        L.event('buckets_call')
        spec = self._spec
        # Revalidation is real work and recharged, including every beta field.
        spec.validate(L)
        nat(sigma, 'sigma', L, 1)
        nat(tau, 'tau', L)
        if sigma >= spec.M or L.mod(sigma, 2) != 1 or tau >= spec.M:
            raise ValueError('sigma must be an odd residue; tau must be a residue')
        if type(source) is not DyadicSource or type(source.values) is not tuple:
            raise ValueError('immutable, already represented DyadicSource required')
        F = nat(source.fractional_bits_bound, 'fractional_bits_bound', L)
        source_length = L.record('source_length', (), len(source.values))
        if source_length != spec.M:
            raise ValueError('source length does not match M')
        B = spec.B
        bins = [(0, 0) for _ in range(B)]
        L.allocate(L.mul(3, B))  # Pair slots and two exact zero numerators.
        exponent = L.add(F, spec.P)
        for tap in self._window.taps:
            t = tap.t
            index = L.mod(L.add(L.mul(sigma, t), tau), spec.M)
            sample = source.values[index]
            L.event('source_query')
            if type(sample) is not tuple or len(sample) != 2:
                raise ValueError('complex sample must have two Cartesian dyadics')
            aligned = []
            L.allocate(2)
            for value in sample:
                if type(value) is not tuple or len(value) != 2:
                    raise ValueError('Cartesian sample must be (numerator, exponent)')
                n, e = value
                if type(n) is not int or type(e) is not int:
                    raise ValueError('sample fields must be exact integers')
                L.record('source_integer_field', (), n)
                L.record('source_integer_field', (), e)
                if not 0 <= e <= F:
                    raise ValueError('sample exponent violates declared bound')
                unit = L.shift(e)
                if abs(n) > unit:
                    raise ValueError('sample Cartesian magnitude exceeds one')
                aligned.append(L.mul(n, L.shift(L.sub(F, e))))
                L.event('sample_alignment')
            slot = L.mod(t, B)
            old_r, old_i = bins[slot]
            bins[slot] = (L.add(old_r, L.mul(tap.numerator, aligned[0])),
                          L.add(old_i, L.mul(tap.numerator, aligned[1])))
            L.allocate(3)
            L.event('tap_fold')
        # Explicit paid bit reversal; no dense M-index table or opaque FFT.
        for i in range(B):
            reverse = 0
            residue = i
            for _ in range(self._b):
                reverse = L.add(L.mul(2, reverse), L.mod(residue, 2))
                residue = L.div(residue, 2)
                L.event('bit_reverse_bit')
            if i < reverse:
                bins[i], bins[reverse] = bins[reverse], bins[i]
                L.event('bit_reverse_swap')
            L.event('bit_reverse_index')
        root_unit = L.shift(self._Q)
        for stage in range(1, L.add(self._b, 1)):
            length = L.shift(stage)
            half = L.div(length, 2)
            stride = L.div(B, length)
            for start in range(0, B, length):
                for j in range(half):
                    left = L.add(start, j)
                    right = L.add(left, half)
                    root = self._roots[L.mul(j, stride)]
                    ar, ai = bins[left]
                    br, bi = bins[right]
                    rr, ri = root.real.numerator, root.imag.numerator
                    vr = L.sub(L.mul(br, rr), L.mul(bi, ri))
                    vi = L.add(L.mul(br, ri), L.mul(bi, rr))
                    ur, ui = L.mul(ar, root_unit), L.mul(ai, root_unit)
                    bins[left] = (L.add(ur, vr), L.add(ui, vi))
                    bins[right] = (L.sub(ur, vr), L.sub(ui, vi))
                    L.allocate(6)
                    L.event('fft_butterfly')
            exponent = L.add(exponent, self._Q)
            L.event('fft_stage')
        final_exponent = L.add(exponent, self._scale.bits)
        round_den = L.shift(L.sub(final_exponent, spec.P))
        output = []
        L.allocate(B)
        for real, imag in bins:
            real = nearest_even(L.mul(real, self._scale.numerator), round_den, L)
            imag = nearest_even(L.mul(imag, self._scale.numerator), round_den, L)
            # Each Cartesian component is bounded by the complex norm envelope.
            bound_shift = L.shift(L.sub(self._error_bits, spec.P))
            if (L.mul(abs(real), bound_shift) > self._output_bound_numerator or
                    L.mul(abs(imag), bound_shift) > self._output_bound_numerator):
                raise CertificationError('output amplitude envelope')
            output.append((real, imag))
            L.allocate(3)
            L.event('bucket_output')
        L.allocate(B)
        return BucketResult(tuple(output), spec.P)
