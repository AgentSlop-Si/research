"""Exact conditional compiler rule for a complete orbit of Toeplitz kernels.

This is an operator-pattern rewrite, valid for every input. It is not a general
DFT evaluator and does not collapse applications to separate input vectors.
"""
from collections import Counter

from fixed_kernel import Counted, lower_convolution, prepare
from linear_filters import counted_power


def _validate(n, b, x):
    if n < 2 or n & (n-1) or b < 2 or b & (b-1) or n % b:
        raise ValueError('N and b must be powers of two, with 2 <= b <= N')
    if len(x) != n:
        raise ValueError('input length differs from N')


def full_orbit_reference(field, n, q, b, x):
    """Directly apply b sequential full-size coefficient-modulated kernels.

The orbit root is q^(N/b); all phases and coefficient tables are built here.
This slow audit path is not a claimed fast algorithm.
"""
    _validate(n, b, x)
    plan = prepare(field, n, q)
    c, traffic = Counted(field), Counter()
    xi = counted_power(c, q, n//b)
    v, phase = list(x), field.one
    for _ in range(b):
        scalar, kernel = field.one, []
        for j in range(n):
            kernel.append(c.mul(plan.kernel[j], scalar))
            if j+1 < n:
                scalar = c.mul(scalar, phase)
        v = lower_convolution(c, kernel, v, traffic)
        phase = c.mul(phase, xi)
    return v, {'field_operations': dict(c.count), 'array_traffic': dict(traffic),
               'base_kernel_preparation': plan.preparation}


def collapsed_orbit(field, n, q, b, x):
    """Apply the recognized orbit as b shorter residue-chain convolutions.

No full-size kernel is prepared. q^b is formed with log2(b) squarings. The
constructor assumes the graph pattern is already verified; a pattern matcher
must inspect its b nodes and symbolic phase labels in O(b) work.
"""
    _validate(n, b, x)
    m = n//b
    root_counter = Counted(field)
    small_q = q
    for _ in range(b.bit_length()-1):
        small_q = root_counter.mul(small_q, small_q)
    if m == 1:
        return list(x), {'root_preparation': dict(root_counter.count),
            'kernel_preparation': {}, 'field_operations': {},
            'array_traffic': {'output_copy_reads': n, 'output_copy_writes': n},
            'chain_count': b, 'chain_length': m}
    plan = prepare(field, m, small_q)
    c, traffic = Counted(field), Counter()
    out = [field.zero] * n
    for residue in range(b):
        chain = [x[residue+b*j] for j in range(m)]
        result = lower_convolution(c, plan.kernel, chain, traffic)
        for j, value in enumerate(result):
            out[residue+b*j] = value
    traffic['gather_reads'] += n
    traffic['gather_writes'] += n
    traffic['scatter_reads'] += n
    traffic['scatter_writes'] += n
    return out, {'root_preparation': dict(root_counter.count),
        'kernel_preparation': plan.preparation, 'field_operations': dict(c.count),
        'array_traffic': dict(traffic), 'chain_count': b, 'chain_length': m}


def false_fourier_collapse(field, plan, x):
    """Deliberately wrong negative control: pretend diag(d)R equals J.

F=S T diag(d) R T R S, but the legal norm rewrite needs T J T.
This routine replaces that actual middle operator with J to exhibit failure.
"""
    n = plan.n
    v = [field.mul(a, z) for a, z in zip(plan.factorial, x)]
    v.reverse()
    v = collapsed_orbit(field, n, plan.q, 2, v)[0]
    v = [field.neg(z) if j % 2 else z for j, z in enumerate(v)]
    return [field.mul(a, z) for a, z in zip(plan.factorial, v)]
