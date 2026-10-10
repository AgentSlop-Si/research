"""Exact sparse-grading decimation of the full finite q-exponential operator.

No Fourier backend is used. The hybrid direct-filter / direct-circulant
implementation is subquadratic, but slower asymptotically than ordinary FFT.
See README.md for the family closure, three-call recursion and complete costs.
"""
from collections import Counter
from dataclasses import dataclass
from fixed_kernel import Counted, prepare


def factor(field, values, phase, sign):
    """(I + phase J_sign) x, where J_sign is the cyclic upper shift."""
    edge = phase if sign == 1 else field.neg(phase)
    return [field.add(values[i], field.mul(phase, values[i+1]))
            for i in range(len(values)-1)] + [
                field.add(values[-1], field.mul(edge, values[0]))]


def inverse_factor(field, values, phase, sign, inverse_denominator):
    """Two exact backward scans; denominator = 1-sign*(-phase)^len(values)."""
    h = len(values)
    acc = values[-1]
    for i in range(h-2, -1, -1):
        acc = field.sub(values[i], field.mul(phase, acc))
    first = field.mul(inverse_denominator, acc)
    if h == 1:
        return [first]
    edge = phase if sign == 1 else field.neg(phase)
    result = [field.zero] * h
    result[0] = first
    result[-1] = field.sub(values[-1], field.mul(edge, first))
    for i in range(h-2, 0, -1):
        result[i] = field.sub(values[i], field.mul(phase, result[i+1]))
    return result


def polynomial_from_first_column(field, column, sign):
    return [column[0]] + [column[-k] if sign == 1 else field.neg(column[-k])
                          for k in range(1, len(column))]


def direct_cyclic(field, coefficients, values, sign):
    """Direct polynomial in J_sign, with every scalar gate charged."""
    h = len(values)
    out = []
    for i in range(h):
        acc = field.zero
        for k, coefficient in enumerate(coefficients):
            term = field.mul(coefficient, values[(i+k) % h])
            acc = (field.sub(acc, term) if sign == -1 and i+k >= h
                   else field.add(acc, term))
        out.append(acc)
    return out


@dataclass
class Level:
    n: int
    r: int
    diagonal: list
    inverse_diagonal: list
    phases: list
    minus_inverse_denominators: list
    cyclic_kernel: list
    minus_kernel: list
    minus_inverse_kernel: list


@dataclass
class DecimationPlan:
    n: int
    q: object
    powers: list
    half: object
    sigma: list
    sigma_inverse: list
    kernel: list
    levels: list
    preparation: dict


def prepare_decimation(field, n, q):
    base = prepare(field, n, q)
    c = Counted(field)
    powers = [field.one]
    for _ in range(1, n):
        powers.append(c.mul(powers[-1], q))
    half = c.inv(field.integer(2))
    sigma, sigma_inverse = [], []
    for j in range(n):
        a = c.mul(powers[(-j) % n], base.kernel[j])
        b = c.mul(powers[j], base.factorial[j])
        sigma.append(c.neg(a) if j % 2 else a)
        sigma_inverse.append(c.neg(b) if j % 2 else b)
    levels = []
    size, r = n, 1
    while size >= 2:
        phases = powers[:r]
        diagonal = [powers[(-r*i) % n] for i in range(size)]
        inverse_diagonal = [powers[(r*i) % n] for i in range(size)]
        # Dense kernels are prepared only where they beat r factor passes.
        cyclic_kernel = []
        if r > size:
            column = [field.one] + [field.zero]*(size-1)
            for phase in phases:
                column = factor(c, column, phase, 1)
            cyclic_kernel = polynomial_from_first_column(c, column, 1)
        inverse_denominators, minus_kernel, minus_inverse_kernel = [], [], []
        if size > 2:
            h = size//2  # even, so denominator is 1+q^(a*h)
            for a in range(r):
                inverse_denominators.append(c.inv(c.add(field.one, powers[(a*h) % n])))
            if r > h:
                column = [field.one] + [field.zero]*(h-1)
                inverse_column = list(column)
                for a, phase in enumerate(phases):
                    column = factor(c, column, phase, -1)
                    inverse_column = inverse_factor(c, inverse_column, phase,
                                                    -1, inverse_denominators[a])
                minus_kernel = polynomial_from_first_column(c, column, -1)
                minus_inverse_kernel = polynomial_from_first_column(c, inverse_column, -1)
        levels.append(Level(size, r, diagonal, inverse_diagonal, phases,
                            inverse_denominators, cyclic_kernel,
                            minus_kernel, minus_inverse_kernel))
        size //= 2
        r *= 2
    return DecimationPlan(n, q, powers, half, sigma, sigma_inverse,
                           base.kernel, levels,
                           dict(q_factorial=base.preparation, decimation=dict(c.count)))


def apply_family(field, level, values):
    """D_r = p_r(J_n) diag(q^(-r*i)), p_r(z)=prod_(a<r)(1+q^a z)."""
    v = [field.mul(a, b) for a, b in zip(level.diagonal, values)]
    if level.cyclic_kernel:
        return direct_cyclic(field, level.cyclic_kernel, v, 1)
    for phase in level.phases:
        v = factor(field, v, phase, 1)
    return v


def apply_minus(field, level, values, inverse=False):
    """Apply M_- or its inverse, without an uncharged dense matrix."""
    h = len(values)
    if inverse:
        v = list(values)
        if level.minus_inverse_kernel:
            v = direct_cyclic(field, level.minus_inverse_kernel, v, -1)
        else:
            for phase, denominator in zip(level.phases, level.minus_inverse_denominators):
                v = inverse_factor(field, v, phase, -1, denominator)
        return [field.mul(level.inverse_diagonal[i], v[i]) for i in range(h)]
    v = [field.mul(level.diagonal[i], values[i]) for i in range(h)]
    if level.minus_kernel:
        return direct_cyclic(field, level.minus_kernel, v, -1)
    for phase in level.phases:
        v = factor(field, v, phase, -1)
    return v


def split_coordinates(field, plan, level_index, values):
    level = plan.levels[level_index]
    h = level.n//2
    s = [field.mul(plan.half, field.add(values[i], values[i+h])) for i in range(h)]
    a = [field.mul(plan.half, field.sub(values[i], values[i+h])) for i in range(h)]
    return s, apply_minus(field, level, a, inverse=True)


def merge_coordinates(field, plan, level_index, first, second):
    a = apply_minus(field, plan.levels[level_index], second)
    return ([field.add(x, y) for x, y in zip(first, a)] +
            [field.sub(x, y) for x, y in zip(first, a)])


def _recursive_polynomial(field, plan, index, coefficients, values, nodes):
    level = plan.levels[index]
    n = level.n
    nodes[index] += 1
    if len(coefficients) != n or len(values) != n:
        raise ValueError("This evaluator pads the polynomial to the node dimension")
    if n == 2:
        dx = apply_family(field, level, values)
        return [field.add(field.mul(coefficients[0], values[i]),
                          field.mul(coefficients[1], dx[i])) for i in range(n)]
    x, y = split_coordinates(field, plan, index, values)
    even, odd = coefficients[::2], coefficients[1::2]
    summed_coefficients = [field.add(a, b) for a, b in zip(even, odd)]
    summed_values = [field.add(a, b) for a, b in zip(x, y)]
    a = _recursive_polynomial(field, plan, index+1, even, x, nodes)
    b = _recursive_polynomial(field, plan, index+1, odd, y, nodes)
    c = _recursive_polynomial(field, plan, index+1, summed_coefficients, summed_values, nodes)
    db = apply_family(field, plan.levels[index+1], b)
    upper = [field.add(u, v) for u, v in zip(a, db)]
    lower = [field.sub(field.sub(cj, aj), bj) for cj, aj, bj in zip(c, a, b)]
    return merge_coordinates(field, plan, index, upper, lower)


def apply_polynomial(field, plan, coefficients, values):
    """Exact p(C)x with all coefficient-dependent work charged online."""
    c = Counted(field)
    nodes = Counter()
    gauged = [c.mul(a, b) for a, b in zip(plan.sigma_inverse, values)]
    result = _recursive_polynomial(c, plan, 0, coefficients, gauged, nodes)
    result = [c.mul(a, b) for a, b in zip(plan.sigma, result)]
    return result, dict(field_operations=dict(c.count),
                        recursive_nodes_by_depth=dict(nodes),
                        full_output_coordinates=plan.n,
                        ordinary_fft_calls=0)


def apply_full_h(field, plan, values):
    return apply_polynomial(field, plan, plan.kernel, values)
