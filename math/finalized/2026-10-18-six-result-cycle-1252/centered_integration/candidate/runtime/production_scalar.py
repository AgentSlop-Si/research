"""Fresh finite Q16 scalar/coefficient kernel, authored 2026-10-17.

Only integer arithmetic is used. This module is intentionally independent of
historical executable modules. It implements the source-pinned outer contract
from its explicit recurrence. The wrapper is responsible for sparse-output
provenance; this kernel validates arithmetic parameters and retained incidences.
"""
from dataclasses import dataclass


class CertificateError(ArithmeticError):
    """A deterministic implementation/certificate defect, not recovery failure."""


class DenseRequired(ValueError):
    pass


class Paid:
    """Monotone conservative schoolbook ledger; never reset by validation/setup.

    Integer primitives pay operand/result widths. Constant-sized Python
    bookkeeping, tuple construction, comparisons, abs/bit_length, loop/index
    updates, record copies and ledger counter arithmetic receive an explicit
    2048-per-event envelope in report(). This is binary-model accounting, not
    a claim about interpreter instructions, runtime allocations or wall time.
    """
    def __init__(self):
        self.operations = {}
        self.arithmetic_bit_work = 0
        self.produced_integer_bits = 0
        self.max_integer_bits = 1
        self.events = 0
        self.copied_input_bits = 0

    def event(self, name, count=1):
        if type(name) is not str or type(count) is not int or count < 0:
            raise ValueError('invalid ledger event')
        self.operations[name] = self.operations.get(name, 0) + count
        self.events += count

    def record(self, name, operands, result):
        self.event(name)
        width_sum = 2
        for v in (*operands, result):
            if type(v) is not int:
                raise ValueError('ledger integer required')
            w = max(1, abs(v).bit_length()) + 1
            width_sum += w
            self.max_integer_bits = max(self.max_integer_bits, w)
        self.arithmetic_bit_work += 16 * width_sum * width_sum
        self.produced_integer_bits += max(1, abs(result).bit_length()) + 1
        return result

    def integer(self, value, name, minimum=None):
        self.event('exact_type_validation')
        if type(value) is not int:
            raise ValueError(name + ' must be a built-in integer')
        self.record('input_read_copy', (), value)
        self.copied_input_bits += max(1, abs(value).bit_length()) + 1
        if minimum is not None and value < minimum:
            raise ValueError(name + ' below minimum')
        return value

    def add(self, x, y): return self.record('add', (x, y), x + y)
    def sub(self, x, y): return self.record('subtract', (x, y), x - y)
    def mul(self, x, y): return self.record('multiply', (x, y), x * y)
    def neg(self, x): return self.record('negate', (x,), -x)
    def floor(self, x, y):
        if y <= 0: raise ValueError('positive denominator required')
        return self.record('floor_divide', (x, y), x // y)
    def ceil(self, x, y): return self.neg(self.floor(self.neg(x), y))
    def mod(self, x, y):
        if y <= 0: raise ValueError('positive modulus required')
        return self.record('modulo', (x, y), x % y)
    def bits(self, x): return self.record('bit_length', (x,), x.bit_length())
    def shift(self, exponent):
        self.integer(exponent, 'binary exponent', 0)
        return self.record('binary_shift_allocation', (exponent,), 1 << exponent)
    def power(self, base, exponent):
        self.integer(base, 'power base')
        self.integer(exponent, 'power exponent', 0)
        ans = self.record('power_initial_one', (), 1)
        rest = exponent
        while rest:
            self.event('power_loop')
            if self.mod(rest, 2): ans = self.mul(ans, base)
            rest = self.floor(rest, 2)
            if rest: base = self.mul(base, base)
        return ans

    def report(self):
        # Reading/reporting itself is charged and therefore never clears work.
        self.event('ledger_report')
        count = self.events + 256
        width = self.max_integer_bits + count.bit_length() + 8
        control_work = 2048 * count * width * width
        storage = self.produced_integer_bits + 2048 * count * width
        return {
            'operations': dict(sorted(self.operations.items())),
            'arithmetic_bit_work': self.arithmetic_bit_work,
            'control_copy_width_bit_work_upper': control_work,
            'total_bit_work_upper': self.arithmetic_bit_work + control_work,
            'cumulative_integer_and_control_storage_bits_upper': storage,
            'produced_integer_bits': self.produced_integer_bits,
            'max_integer_bits': self.max_integer_bits,
            'events': self.events,
            'copied_input_bits': self.copied_input_bits,
            'model': 'schoolbook integer arithmetic plus 2048-per-event control/copy/width envelope; excludes test driver serialization and host runtime costs',
        }


@dataclass(frozen=True)
class Interval:
    lo: int
    hi: int
    bits: int
    def __post_init__(self):
        if type(self.lo) is not int or type(self.hi) is not int or type(self.bits) is not int:
            raise ValueError('interval fields must be built-in integers')
        if self.lo > self.hi or self.bits < 0:
            raise ValueError('invalid interval')


def make_interval(lo, hi, bits, paid):
    paid.event('interval_validation_copy', 4)
    return Interval(lo, hi, bits)


def clip(a, lower, upper, paid):
    paid.event('analytic_intersection', 4)
    if a.hi < lower or upper < a.lo:
        raise CertificateError('analytic enclosure intersection is empty')
    return make_interval(max(a.lo, lower), min(a.hi, upper), a.bits, paid)


def interval_product(a, b, paid):
    paid.event('product_grid_check')
    if a.bits != b.bits: raise ValueError('interval grids differ')
    corners = tuple(paid.mul(x, y) for x in (a.lo, a.hi) for y in (b.lo, b.hi))
    paid.event('four_corner_storage_comparison', 12)
    scale = paid.shift(a.bits)
    return make_interval(paid.floor(min(corners), scale), paid.ceil(max(corners), scale), a.bits, paid)


def normalized_quotient(a, denominator, normalization, paid):
    """All four corners of a/(normalization*denominator), K-grid."""
    paid.event('quotient_domain_check', 4)
    if a.bits != denominator.bits: raise ValueError('interval grids differ')
    paid.integer(normalization, 'normalization', 1)
    if denominator.lo <= 0:
        raise CertificateError('denominator lower endpoint is not positive')
    unit = paid.shift(a.bits)
    low = high = None
    for x in (a.lo, a.hi):
        for y in (denominator.lo, denominator.hi):
            paid.event('quotient_corner')
            numerator = paid.mul(x, unit)
            divisor = paid.mul(normalization, y)
            left, right = paid.floor(numerator, divisor), paid.ceil(numerator, divisor)
            low = left if low is None else min(low, left)
            high = right if high is None else max(high, right)
    paid.event('four_corner_storage_comparison', 12)
    return clip(make_interval(low, high, a.bits, paid), paid.neg(unit), unit, paid)


def signed_power(a, exponent, paid):
    """Actual production odd/even endpoint-power operator; no absolute substitute."""
    paid.event('signed_power_call')
    paid.integer(exponent, 'signed exponent', 1)
    if type(a) is not Interval: raise ValueError('exact Interval required')
    unit = paid.shift(a.bits)
    if a.lo < -unit or a.hi > unit:
        raise ValueError('signed power interval outside [-1,1]')
    if paid.mod(exponent, 2):
        low, high = a.lo, a.hi
    else:
        low = 0 if a.lo <= 0 <= a.hi else min(abs(a.lo), abs(a.hi))
        high = max(abs(a.lo), abs(a.hi))
    paid.event('signed_endpoint_selection', 12)
    divisor = paid.shift(paid.mul(a.bits, paid.sub(exponent, 1)))
    result = make_interval(paid.floor(paid.power(low, exponent), divisor),
                           paid.ceil(paid.power(high, exponent), divisor), a.bits, paid)
    return clip(result, paid.neg(unit), unit, paid)


class Scalar:
    """Finite fixed-term Machin pi and point-Taylor sine, newly authored code."""
    def __init__(self, bits, paid):
        if type(paid) is not Paid: raise ValueError('exact Paid ledger required')
        self.paid = paid
        self.bits = paid.integer(bits, 'scalar bits', 16)
        self.unit = paid.shift(bits)
        self.terms = paid.add(bits, 8)
        self.sine_calls = 0
        paid.event('pi_setup')
        a, b = self._arctangent(5), self._arctangent(239)
        self.pi = make_interval(paid.sub(paid.mul(16, a.lo), paid.mul(4, b.hi)),
                                paid.sub(paid.mul(16, a.hi), paid.mul(4, b.lo)), bits, paid)
        paid.event('pi_guards', 3)
        if not paid.mul(3, self.unit) < self.pi.lo <= self.pi.hi < paid.mul(4, self.unit):
            raise CertificateError('pi enclosure guard failed')
        if paid.sub(self.pi.hi, self.pi.lo) > paid.mul(20, paid.add(self.terms, 1)):
            raise CertificateError('pi width budget failed')

    def _arctangent(self, reciprocal):
        w = self.paid
        lo = hi = 0
        odd_power = reciprocal
        square = w.mul(reciprocal, reciprocal)
        for j in range(self.terms):
            w.event('atan_term')
            denominator = w.mul(w.add(w.mul(2, j), 1), odd_power)
            left = w.floor(self.unit, denominator)
            right = w.ceil(self.unit, denominator)
            if j % 2:
                lo, hi = w.sub(lo, right), w.sub(hi, left)
            else:
                lo, hi = w.add(lo, left), w.add(hi, right)
            odd_power = w.mul(odd_power, square)
        tail = w.ceil(self.unit, w.mul(w.add(w.mul(2, self.terms), 1), odd_power))
        if self.terms % 2: lo = w.sub(lo, tail)
        else: hi = w.add(hi, tail)
        return make_interval(lo, hi, self.bits, w)

    def sin_pi(self, numerator, denominator):
        w = self.paid
        w.integer(numerator, 'sine numerator')
        w.integer(denominator, 'sine denominator', 1)
        w.event('sine_call')
        self.sine_calls = w.add(self.sine_calls, 1)
        a = w.mod(numerator, w.mul(2, denominator))
        sign = 1
        if a > denominator:
            a = w.sub(w.mul(2, denominator), a)
            sign = -1
        if w.mul(2, a) > denominator: a = w.sub(denominator, a)
        if a == 0:
            w.event('exact_zero_sine')
            return make_interval(0, 0, self.bits, w)
        if w.mul(2, a) == denominator:
            w.event('exact_unit_sine')
            exact = w.mul(sign, self.unit)
            return make_interval(exact, exact, self.bits, w)
        left = w.floor(w.mul(self.pi.lo, a), denominator)
        right = w.ceil(w.mul(self.pi.hi, a), denominator)
        x = w.floor(w.add(left, right), 2)
        angle_radius = max(w.sub(x, left), w.sub(right, x))
        w.event('angle_guards', 3)
        if not 0 <= x <= w.mul(2, self.unit):
            raise CertificateError('point Taylor angle outside [0,2]')
        x_squared = w.mul(x, x)
        unit_squared = w.mul(self.unit, self.unit)
        term_lo = term_hi = sum_lo = sum_hi = x
        for j in range(1, self.terms):
            w.event('sine_taylor_term')
            twice = w.mul(2, j)
            divisor = w.mul(unit_squared, w.mul(twice, w.add(twice, 1)))
            term_lo = w.floor(w.mul(term_lo, x_squared), divisor)
            term_hi = w.ceil(w.mul(term_hi, x_squared), divisor)
            if j % 2:
                sum_lo, sum_hi = w.sub(sum_lo, term_hi), w.sub(sum_hi, term_lo)
            else:
                sum_lo, sum_hi = w.add(sum_lo, term_lo), w.add(sum_hi, term_hi)
        factorial = 1
        stop = w.add(w.mul(2, self.terms), 2)
        for j in range(2, stop):
            w.event('factorial_step')
            factorial = w.mul(factorial, j)
        tail_power = w.add(self.bits, w.add(w.mul(2, self.terms), 1))
        tail = w.ceil(w.shift(tail_power), factorial)
        if tail > 1: raise CertificateError('fixed Taylor remainder budget failed')
        radius = w.add(angle_radius, tail)
        out = make_interval(w.sub(sum_lo, radius), w.add(sum_hi, radius), self.bits, w)
        if sign < 0: out = make_interval(w.neg(out.hi), w.neg(out.lo), self.bits, w)
        out = clip(out, w.neg(self.unit), self.unit, w)
        if w.sub(out.hi, out.lo) > w.mul(64, w.add(self.terms, 1)):
            raise CertificateError('fixed sine width budget failed')
        return out


def sqrt_ratio(N, M, bits, paid):
    """Exactly K+2 bisections, returning a containing interval of width 2^-K."""
    paid.event('sqrt_setup')
    target = paid.floor(paid.mul(M, paid.shift(paid.mul(2, bits))), N)
    lo, hi = 0, paid.shift(paid.add(bits, 2))
    for _ in range(paid.add(bits, 2)):
        paid.event('sqrt_bisection')
        mid = paid.floor(paid.add(lo, hi), 2)
        if paid.mul(mid, mid) <= target: lo = mid
        else: hi = mid
    if paid.sub(hi, lo) != 1:
        raise CertificateError('fixed sqrt bisection did not isolate integer root')
    return clip(make_interval(lo, paid.add(lo, 1), bits, paid), 0,
                paid.mul(3, paid.shift(bits)), paid)


def nearest_even(numerator, positive_denominator, paid):
    """Round an arbitrary signed rational with floor/remainder tie parity."""
    paid.integer(numerator, 'rounding numerator')
    paid.integer(positive_denominator, 'rounding denominator', 1)
    lower = paid.floor(numerator, positive_denominator)
    remainder = paid.sub(numerator, paid.mul(lower, positive_denominator))
    twice = paid.mul(2, remainder)
    paid.event('nearest_even_tie_check', 3)
    if twice > positive_denominator or (twice == positive_denominator and paid.mod(lower, 2)):
        return paid.add(lower, 1)
    return lower


def rounded_certificate(real, imag, p, A, paid):
    paid.event('complex_certificate_call')
    if real.bits != imag.bits or p > real.bits or A > p:
        raise ValueError('certificate precision parameters invalid')
    K = real.bits
    mid_divisor = paid.shift(paid.sub(paid.add(K, 1), p))
    zr = nearest_even(paid.add(real.lo, real.hi), mid_divisor, paid)
    zi = nearest_even(paid.add(imag.lo, imag.hi), mid_divisor, paid)
    lift = paid.shift(paid.sub(K, p))
    lr, li = paid.mul(zr, lift), paid.mul(zi, lift)
    rr = max(abs(paid.sub(lr, real.lo)), abs(paid.sub(lr, real.hi)))
    ri = max(abs(paid.sub(li, imag.lo)), abs(paid.sub(li, imag.hi)))
    paid.event('certificate_radius_comparison', 8)
    left = paid.add(paid.mul(rr, rr), paid.mul(ri, ri))
    right = paid.shift(paid.mul(2, paid.sub(K, A)))
    if left > right:
        paid.event('certificate_failure')
        raise CertificateError('squared-radius certificate failed')
    paid.event('certificate_pass')
    return zr, zi, rr, ri, left, right


@dataclass(frozen=True)
class CoefficientResult:
    ell: int
    k: int
    real_integer: int
    imag_integer: int
    p: int
    K: int
    real_enclosure: Interval
    imag_enclosure: Interval
    radius_real: int
    radius_imag: int
    radius_squared: int
    eta_squared_grid: int
    residue: int
    denominator: Interval | None
    F: Interval
    R: Interval
    powered_R: Interval


class CoefficientEngine:
    """Lazy numerical state for a single parameter header; no phase/row caches."""
    def __init__(self, N, M, D, paid=None):
        if paid is None: paid = Paid()
        if type(paid) is not Paid: raise ValueError('exact Paid ledger required')
        self.paid = paid
        paid.event('kernel_header_validation')
        self.N = paid.integer(N, 'N', 1)
        self.M = paid.integer(M, 'M', 4)
        self.D = paid.integer(D, 'D', 5)
        four_N = paid.mul(4, N)
        expected_M = paid.shift(paid.bits(paid.sub(four_N, 1)))
        if M != expected_M: raise ValueError('M header mismatch')
        self.m = paid.sub(paid.bits(M), 1)
        self.a0 = paid.floor(paid.sub(N, 1), 2)
        self.s = paid.mul(D, self.m)
        self.h = paid.add(paid.mul(16, self.s), 1)
        self.t = paid.add(paid.mul(2, self.h), 2)
        self.dense_required = self.t >= M
        self.J = paid.add(paid.add(paid.mul(paid.add(D, 5), self.m), paid.bits(self.s)), 8)
        self.K = paid.add(paid.add(self.J, paid.mul(2, paid.bits(paid.add(self.J, 1)))), 16)
        self.A = paid.mul(paid.add(D, 3), self.m)
        self.p = paid.add(self.A, 3)
        self.L = paid.floor(M, 4)
        self.q = paid.floor(M, paid.mul(8, self.s))
        self.Q = paid.mul(N, M)
        self.scalar = None
        self.root = None
        self.prepared = False
        paid.event('kernel_header_copy', 18)

    def prepare(self):
        self.paid.event('prepare_call')
        if self.dense_required:
            self.paid.event('dense_guard')
            raise DenseRequired('OUTER_DENSE_REQUIRED')
        if self.prepared:
            self.paid.event('prepare_reuse_check')
            return
        self.scalar = Scalar(self.K, self.paid)
        self.root = sqrt_ratio(self.N, self.M, self.K, self.paid)
        self.prepared = True
        self.paid.event('setup_complete')

    def coefficient(self, ell, k):
        w = self.paid
        w.event('coefficient_call')
        w.integer(ell, 'ell', 0)
        w.integer(k, 'k', 0)
        if ell >= self.N or k >= self.M: raise ValueError('coefficient index outside header')
        if self.dense_required:
            w.event('dense_guard')
            raise DenseRequired('OUTER_DENSE_REQUIRED')
        center = w.floor(w.mul(ell, self.M), self.N)
        stencil_offset = w.mod(w.sub(k, center), self.M)
        if not (stencil_offset <= w.add(self.h, 1) or stencil_offset >= w.sub(self.M, self.h)):
            raise ValueError('pair is not a retained incidence')
        self.prepare()
        U = self.scalar.unit
        residue = w.mod(w.sub(w.mul(ell, self.M), w.mul(k, self.N)), self.Q)
        denominator = None
        if residue == 0:
            w.event('zero_limit')
            limit = w.mul(w.add(w.mul(2, self.L), 1), w.shift(w.sub(self.K, self.m)))
            F = make_interval(limit, limit, self.K, w)
            R = make_interval(U, U, self.K, w)
        else:
            denominator = self.scalar.sin_pi(residue, self.Q)
            if denominator.lo <= 0:
                raise CertificateError('denominator lower endpoint is not positive')
            a = self.scalar.sin_pi(w.mul(w.add(w.mul(2, self.L), 1), residue), self.Q)
            c = self.scalar.sin_pi(w.mul(w.add(w.mul(2, self.q), 1), residue), self.Q)
            F = normalized_quotient(a, denominator, self.M, w)
            R = normalized_quotient(c, denominator, w.add(w.mul(2, self.q), 1), w)
        powered = signed_power(R, self.s, w)
        product = clip(interval_product(F, powered, w), w.neg(U), U, w)
        bound = w.mul(3, U)
        amplitude = clip(interval_product(product, self.root, w), w.neg(bound), bound, w)
        phase_real = self.scalar.sin_pi(w.sub(self.N, w.mul(w.mul(4, self.a0), ell)), w.mul(2, self.N))
        phase_imag = self.scalar.sin_pi(w.neg(w.mul(w.mul(2, self.a0), ell)), self.N)
        real = clip(interval_product(amplitude, phase_real, w), w.neg(bound), bound, w)
        imag = clip(interval_product(amplitude, phase_imag, w), w.neg(bound), bound, w)
        zr, zi, rr, ri, lhs, rhs = rounded_certificate(real, imag, self.p, self.A, w)
        w.event('coefficient_output_copy', 32)
        return CoefficientResult(ell, k, zr, zi, self.p, self.K, real, imag,
                                 rr, ri, lhs, rhs, residue, denominator, F, R, powered)
