"""Linear-work exact spectrum preparation for the root-dependent q-kernel.

The FFT application is ordinary radix two, not a sub-N-log-N FFT algorithm.
An exact primitive 2N-th root eta is SUPPLIED; q = eta**2.
"""
from collections import Counter
from dataclasses import dataclass


class Counted:
    def __init__(self, field):
        self.field, self.count = field, Counter()
    def __getattr__(self, name):
        return getattr(self.field, name)
    def add(self, a, b):
        self.count['add'] += 1
        return self.field.add(a, b)
    def sub(self, a, b):
        self.count['sub'] += 1
        return self.field.sub(a, b)
    def mul(self, a, b):
        self.count['mul'] += 1
        return self.field.mul(a, b)
    def neg(self, a):
        self.count['neg'] += 1
        return self.field.neg(a)
    def inv(self, a):
        self.count['constant_inverse'] += 1
        return self.field.inv(a)


@dataclass
class FFTPlan:
    n: int
    powers: list
    permutation: list
    inverse_n: object
    inverse_length: object


@dataclass
class KernelPlan:
    fft: FFTPlan
    spectrum: list
    preparation: dict
    method: str


def fft_plan(c, n, eta):
    if n < 2 or n & (n-1):
        raise ValueError('N must be a power of two at least 2')
    powers = [c.one]
    for _ in range(1, 2*n):
        powers.append(c.mul(powers[-1], eta))
    half = c.inv(c.integer(2))
    inverse_n = c.one
    for _ in range(n.bit_length()-1):
        inverse_n = c.mul(inverse_n, half)
    inverse_length = c.mul(inverse_n, half)
    # Linear total integer work; no N separate log(N)-step bit reversals.
    permutation = [0]
    while len(permutation) < 2*n:
        doubled = [2*j for j in permutation]
        permutation = doubled + [j+1 for j in doubled]
    return FFTPlan(n, powers, permutation, inverse_n, inverse_length)


def fft(c, plan, values, inverse=False, traffic=None):
    m = 2*plan.n
    if len(values) != m:
        raise ValueError('FFT input length must be 2N')
    out = [values[j] for j in plan.permutation]
    if traffic is not None:
        traffic['permutation_index_reads'] += m
        traffic['permutation_value_reads'] += m
        traffic['permutation_value_writes'] += m
    width = 2
    while width <= m:
        half, stride = width//2, m//width
        for base in range(0, m, width):
            for j in range(half):
                idx = j*stride
                if inverse:
                    idx = (-idx) % m
                u = out[base+j]
                v = c.mul(plan.powers[idx], out[base+j+half])
                out[base+j] = c.add(u, v)
                out[base+j+half] = c.sub(u, v)
                if traffic is not None:
                    traffic['butterfly_value_reads'] += 2
                    traffic['butterfly_twiddle_reads'] += 1
                    traffic['butterfly_value_writes'] += 2
        width *= 2
    if inverse:
        out = [c.mul(plan.inverse_length, value) for value in out]
        if traffic is not None:
            traffic['normalization_value_reads'] += m
            traffic['normalization_value_writes'] += m
    return out


def prepare_orbit(field, n, eta):
    c = Counted(field)
    plan = fft_plan(c, n, eta)
    factors = [c.sub(c.one, root) for root in plan.powers]
    v = [c.zero] * (2*n)
    # The even orbit's zero coefficient removes dependence on v[0].
    v[2] = plan.inverse_n
    for r in range(1, n):
        v[(2*r+2) % (2*n)] = c.add(
            c.mul(factors[2*r], v[2*r]), plan.inverse_n)
    # Odd orbit: composition y -> 2*y + b; closure gives y = -b.
    b = c.zero
    for r in range(n):
        b = c.sub(c.mul(factors[2*r+1], b), plan.inverse_n)
    v[1] = c.neg(b)
    for r in range(n-1):
        v[2*r+3] = c.sub(
            c.mul(factors[2*r+1], v[2*r+1]), plan.inverse_n)
    return KernelPlan(plan, v, dict(c.count), 'orbit')


def coefficient_kernel(c, plan):
    """Backward recurrence from t[N-1]=1/N: N-1 multiplies/subtracts."""
    n = plan.n
    kernel = [c.zero] * n
    kernel[-1] = plan.inverse_n
    for j in range(n-1, 0, -1):
        kernel[j-1] = c.mul(c.sub(c.one, plan.powers[2*j]), kernel[j])
    return kernel


def prepare_radix(field, n, eta):
    """Same complete plan and kernel, with an ordinary preprocessing FFT."""
    c = Counted(field)
    plan = fft_plan(c, n, eta)
    kernel = coefficient_kernel(c, plan)
    spectrum = fft(c, plan, kernel + [c.zero]*n)
    return KernelPlan(plan, spectrum, dict(c.count), 'radix')


def apply(field, plan, x):
    """T*x: 2 length-2N FFTs plus a diagonal; all output entries retained.

Traffic counters describe a logical array implementation, not every temporary
Python-list allocation or interpreter reference operation. Those add O(N)
traffic and space here and are not claimed to match these counters exactly.
"""
    n = plan.fft.n
    if len(x) != n:
        raise ValueError('wrong input length')
    c, traffic = Counted(field), Counter()
    padded = list(x) + [c.zero]*n
    traffic['padding_input_reads'] = n
    traffic['padding_output_writes'] = 2*n
    spectrum = fft(c, plan.fft, padded, traffic=traffic)
    product = [c.mul(a,b) for a,b in zip(spectrum, plan.spectrum)]
    traffic['diagonal_value_reads'] = 4*n
    traffic['diagonal_value_writes'] = 2*n
    values = fft(c, plan.fft, product, inverse=True, traffic=traffic)
    out = values[:n]
    traffic['output_value_reads'] = n
    traffic['output_value_writes'] = n
    return out, {'field_operations': dict(c.count), 'array_traffic': dict(traffic)}


def expected_preparation(n, method):
    l = n.bit_length()-1
    if method == 'orbit':
        return dict(mul=5*n+l-2, add=n-1, sub=4*n-1,
                    neg=1, constant_inverse=1)
    if method == 'radix':
        return dict(mul=n*l+4*n+l-1, add=n*(l+1),
                    sub=n*l+2*n-1, constant_inverse=1)
    raise ValueError(method)


def expected_online(n):
    l = n.bit_length()-1
    return dict(mul=2*n*l+6*n, add=2*n*(l+1), sub=2*n*(l+1))
