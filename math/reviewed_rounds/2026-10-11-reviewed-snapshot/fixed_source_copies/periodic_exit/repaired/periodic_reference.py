"""Fresh research reference. All certification uses exact Python integers.

Input: pairs of bounded integers z_j, representing x_j = z_j * 2**(-f).
Output: dense pairs of integers y_j, representing y_j * 2**output_exponent.
No uploaded/source executor is imported. See IMPLEMENTATION.md for the contract.
"""
from dataclasses import dataclass, field
from math import isqrt


@dataclass
class Meter:
    counts: dict = field(default_factory=dict)
    max_product_bits: int = 0

    def add(self, name, number=1):
        self.counts[name] = self.counts.get(name, 0) + number


class FixedIntervals:
    """Closed intervals with endpoints in units of 2**(-p)."""
    def __init__(self, p, meter):
        self.p, self.s, self.meter = p, 1 << p, meter

    def point(self, n):
        return (n * self.s, n * self.s)

    def add(self, a, b):
        self.meter.add('interval_add')
        return (a[0] + b[0], a[1] + b[1])

    def neg(self, a):
        self.meter.add('interval_neg')
        return (-a[1], -a[0])

    def sub(self, a, b):
        return self.add(a, self.neg(b))

    def half(self, a):
        self.meter.add('interval_half')
        return (a[0] // 2, -((-a[1]) // 2))

    def mul(self, a, b):
        self.meter.add('interval_multiply')
        v = (a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1])
        lo, hi = min(v), max(v)
        self.meter.max_product_bits = max(self.meter.max_product_bits,
                                          abs(lo).bit_length(), abs(hi).bit_length())
        return (lo // self.s, -((-hi) // self.s))

    def sqrt(self, a):
        self.meter.add('integer_sqrt', 2)
        if a[0] < 0:
            raise ArithmeticError('negative square-root interval')
        lo, hi = isqrt(a[0]*self.s), isqrt(a[1]*self.s)
        if hi*hi != a[1]*self.s:
            hi += 1
        return (lo, hi)

    def cmul(self, a, b):
        return (self.sub(self.mul(a[0], b[0]), self.mul(a[1], b[1])),
                self.add(self.mul(a[0], b[1]), self.mul(a[1], b[0])))

    def cadd(self, a, b):
        return (self.add(a[0], b[0]), self.add(a[1], b[1]))

    def csub(self, a, b):
        return (self.sub(a[0], b[0]), self.sub(a[1], b[1]))


def _roots(n, ar):
    """Cold enclosing table for exp(-2*pi*i*j/n), using algebraic half angles.

    Even roots are reused, odd roots are one enclosing product. No trig/libm,
    oracle, cached plan or precomputed coefficient table is used.
    """
    one, zero = ar.point(1), ar.point(0)
    roots = [(one, zero)]
    if n == 1:
        return roots
    roots = [(one, zero), (ar.point(-1), zero)]
    ar.meter.add('root_table_writes', 3)
    m, c = 4, zero
    while m <= n:
        if m == 4:
            alpha = (zero, ar.point(-1))
        else:
            old_c = c
            c = ar.sqrt(ar.half(ar.add(one, old_c)))
            # The radicand is nonnegative. Intersect with its known domain.
            rad = ar.half(ar.sub(one, old_c))
            rad = (max(0, rad[0]), max(0, rad[1]))
            alpha = (c, ar.neg(ar.sqrt(rad)))
        new = []
        for r in roots:
            new.append(r)
            new.append(ar.cmul(r, alpha))
        ar.meter.add('root_table_writes', m)
        roots = new
        m *= 2
    return roots


def _normalized_dft_enclosure(values, normalization_n, p, meter):
    """DFT_len(values)(values) / sqrt(normalization_n), enclosed rigorously."""
    n = len(values)
    ar = FixedIntervals(p, meter)
    roots = _roots(n, ar)
    data = [(ar.point(a), ar.point(b)) for a, b in values]
    meter.add('fft_input_reads', n)
    meter.add('fft_buffer_writes', n)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
            meter.add('bit_reversal_steps')
        j ^= bit
        meter.add('bit_reversal_steps')
        if i < j:
            data[i], data[j] = data[j], data[i]
            meter.add('fft_buffer_writes', 2)
    length = 2
    while length <= n:
        half, stride = length//2, n//length
        for base in range(0, n, length):
            for k in range(half):
                u = data[base+k]
                v = ar.cmul(data[base+k+half], roots[k*stride])
                data[base+k], data[base+k+half] = ar.cadd(u, v), ar.csub(u, v)
                meter.add('butterflies')
                meter.add('fft_buffer_writes', 2)
        length *= 2
    # floor(S/sqrt(N)) is isqrt(floor(S*S/N)). Exact equality is checked.
    low = isqrt(ar.s*ar.s // normalization_n)
    high = low if low*low*normalization_n == ar.s*ar.s else low+1
    meter.add('integer_sqrt')
    scale = (low, high)
    result, error_ticks_squared = [], 0
    for re, im in data:
        re, im = ar.mul(re, scale), ar.mul(im, scale)
        a, b = (re[0]+re[1])//2, (im[0]+im[1])//2
        ra, rb = max(a-re[0], re[1]-a), max(b-im[0], im[1]-b)
        error_ticks_squared += ra*ra + rb*rb
        result.append((a, b))
    meter.add('normalization_and_error_scan', n)
    meter.add('intermediate_output_writes', n)
    return result, error_ticks_squared


def _integer(v):
    return type(v) is int


def _scan(values, f, epsilon_a, epsilon_t, q, meter):
    if type(values) not in (list, tuple):
        raise ValueError('input must be an exact built-in list or tuple')
    n = len(values)
    if n < 1 or n > 2**20 or n & (n-1):
        raise ValueError('N must be a power of two between 1 and 2**20')
    ell = max(1, n.bit_length()-1)
    cap = 4*ell
    if not _integer(f) or abs(f) > cap:
        raise ValueError('common input exponent is out of the bounded contract')
    if not _integer(epsilon_t) or not 0 <= epsilon_t <= cap:
        raise ValueError('epsilon exponent is out of the bounded contract')
    if not _integer(epsilon_a) or not 0 < epsilon_a <= 1 << epsilon_t:
        raise ValueError('epsilon must be in (0, 1]')
    if q is not None and (not _integer(q) or q < 1 or q > n or q & (q-1)):
        raise ValueError('Q must be a power-of-two divisor of N')
    groups = [[0, 0] for _ in range(q)] if q is not None else None
    if q is not None:
        meter.add('group_initialization_writes', q)
    snapshot, energy, maxbits = [], 0, 0
    for j, pair in enumerate(values):
        if type(pair) not in (list, tuple) or len(pair) != 2:
            raise ValueError('each complex input must be a pair of exact integers')
        a, b = pair
        if not _integer(a) or not _integer(b) or max(abs(a), abs(b)) >= 1 << cap:
            raise ValueError('mantissa is not an exact bounded integer')
        energy += a*a + b*b
        maxbits = max(maxbits, abs(a).bit_length(), abs(b).bit_length())
        snapshot.append((a, b))
        if q is not None:
            groups[j % q][0] += a
            groups[j % q][1] += b
    meter.add('external_complex_input_reads', n)
    meter.add('validated_snapshot_writes', n)
    meter.add('exact_energy_terms', n)
    if q is not None:
        meter.add('exact_projection_updates', n)
    return snapshot, energy, groups, maxbits, ell


class CertificationFailure(ArithmeticError):
    """Explicit bounded-resource failure; no approximate answer is returned."""


def _certified(values, normalization_n, target_num, target_den, b, ell, t, meter):
    # Both precision attempts and all cold root setup are inside the timed call.
    # No termination beyond these bounded attempts is silently assumed.
    first_p = b + 5*ell + t + 16
    for p in (first_p, first_p+32):
        meter.add('precision_attempts')
        out, err2 = _normalized_dft_enclosure(values, normalization_n, p, meter)
        if err2 * target_den <= target_num * (1 << (2*p)):
            return out, err2, p
    raise CertificationFailure('two bounded interval precisions failed certification')


def transform(values, *, f=0, epsilon_a=1, epsilon_t=4, q=None):
    """q=None: general baseline; q=power of 2: periodic gate plus fallback.

    Input and pairs must be exact built-in lists or tuples.
    The input must not be changed concurrently during the call. Each raw pair
    is copied while validated, so later code consumes only the owned snapshot.
    On success, the dense dyadic output has relative l2 error <= epsilon for
    the negative-sign unitary DFT. CertificationFailure returns no output.
    """
    meter = Meter()
    x, a, groups, b, ell = _scan(values, f, epsilon_a, epsilon_t, q, meter)
    n, den = len(x), 1 << (2*epsilon_t)
    cert = {'N': n, 'Q': q, 'input_energy_integer': a,
            'epsilon_numerator': epsilon_a, 'epsilon_denominator': 1 << epsilon_t,
            'common_input_exponent': -f}
    if a == 0:
        out = [(0, 0) for _ in range(n)]
        meter.add('dense_output_writes', n)
        return {'output': out, 'output_exponent': -f, 'branch': 'zero',
                'certificate': cert, 'counts': meter.counts, 'max_product_bits': 0}
    accepted = False
    if q is not None:
        m = n//q
        b_energy = sum(re*re+im*im for re, im in groups)
        d = m*a-b_energy
        meter.add('projected_energy_terms', q)
        if d < 0:
            raise ArithmeticError('exact energy identity violated')
        accepted = 2*d*den <= m*a*epsilon_a**2
        cert.update({'M': m, 'projected_energy_numerator': b_energy,
                     'residual_energy_numerator': d, 'energy_denominator': m,
                     'gate_accepted': accepted})
    if accepted:
        # DFT_Q(group sums)/sqrt(N) = sqrt(M) U_Q(mu).
        # Its certified squared error <= epsilon**2 * E_s / 4.
        short, err2, p = _certified(groups, n, epsilon_a**2*b_energy,
                                   4*m*den, b+ell, ell, epsilon_t, meter)
        out = [short[k//m] if k % m == 0 else (0, 0) for k in range(n)]
        # Exact final orthogonal error budget, without floating subtraction.
        assert (d*(1 << (2*p))+m*err2)*den <= epsilon_a**2*m*a*(1 << (2*p))
        branch = 'periodic'
        cert['short_relative_tolerance'] = [epsilon_a, 1 << (epsilon_t+1)]
    else:
        general, err2, p = _certified(x, n, epsilon_a**2*a, den,
                                     b, ell, epsilon_t, meter)
        out = list(general)
        branch = 'general' if q is None else 'fallback'
    meter.add('dense_output_writes', n)
    cert.update({'transform_error_ticks_squared': err2, 'working_fraction_bits': p,
                 'output_grid_exponent': -f-p,
                 'full_relative_l2_error_certified': True})
    return {'output': out, 'output_exponent': -f-p, 'branch': branch,
            'certificate': cert, 'counts': meter.counts,
            'max_product_bits': meter.max_product_bits}
