"""Finite H-specific branch relations and a fully charged candidate rewrite.

The contiguous rewrite uses four half-size O-kernel calls. It is exact, but
does not improve the previous three-call decimation. No operator is free.
"""
from fixed_kernel import Counted
from decimation import apply_family, split_coordinates, merge_coordinates


def shift(values, inverse=False):
    """Cyclic J or J^-1; O(m) copies/index work, no field arithmetic."""
    return values[-1:] + values[:-1] if inverse else values[1:] + values[:1]


def polynomial_action(field, level, coefficients, values):
    """Independent, charged sparse-factor Horner action at this half level."""
    out = [field.mul(coefficients[-1], x) for x in values]
    for coefficient in reversed(coefficients[:-1]):
        out = apply_family(field, level, out)
        out = [field.add(y, field.mul(coefficient, x))
               for x, y in zip(values, out)]
    return out


def four_odd_kernel_rewrite(field, plan, values):
    """Return H_q(C)x via four exact O(D) actions and contiguous relations.

    Fully arbitrary input and complete output. This evaluates the candidate,
    rather than asserting that the phase-related O calls share their work.
    """
    if plan.n < 4:
        raise ValueError('First-split candidate requires N >= 4')
    c = Counted(field)
    gauged = [c.mul(a, b) for a, b in zip(plan.sigma_inverse, values)]
    x, y = split_coordinates(c, plan, 0, gauged)
    odd = plan.kernel[1::2]
    level = plan.levels[1]
    ox = polynomial_action(c, level, odd, x)
    oy = polynomial_action(c, level, odd, y)
    ojx = polynomial_action(c, level, odd, shift(x))
    ojy = polynomial_action(c, level, odd, shift(y))
    doy = apply_family(c, level, oy)
    rojx, rojy = shift(ojx, True), shift(ojy, True)
    upper = [c.add(c.sub(a, c.mul(plan.q, b)), d)
             for a, b, d in zip(ox, rojx, doy)]
    lower = [c.sub(c.add(a, b), c.mul(plan.q, d))
             for a, b, d in zip(ox, oy, rojy)]
    merged = merge_coordinates(c, plan, 0, upper, lower)
    result = [c.mul(a, b) for a, b in zip(plan.sigma, merged)]
    return result, dict(field_operations=dict(c.count), odd_kernel_calls=4,
                       half_size=len(odd), extra_half_operator_actions=1,
                       full_output_coordinates=plan.n, ordinary_fft_calls=0,
                       word_work='O(N) outside the four charged kernel calls')


def branch_symbol(field, q, ratio):
    """2x2 phase-basis block after dividing by the nonzero O_ij."""
    e = field.sub(field.one, field.mul(q, ratio))
    return [[e, field.mul(field.sub(field.one, ratio), e)], [field.one, e]]


def determinant_2(field, matrix):
    return field.sub(field.mul(matrix[0][0], matrix[1][1]),
                     field.mul(matrix[0][1], matrix[1][0]))


def two_odd_call_obstruction(field, n, q):
    """Exact necessary-condition violation for L(J) diag(O,O) R(J).

    This restricts pre/post maps to 2x2 blocks that are functions of J and
    excludes additive bypasses. It is not a lower bound for all two-call schemes.
    """
    m = n//2
    if m < 4:
        raise ValueError('Need a 2x2 rectangle in triangular support')
    lambdas = [field.neg(field.power(q, (-2*i) % n)) for i in range(m)]
    outputs, inputs = (2, 3), (0, 1)
    ratios, determinants = [], []
    for i in outputs:
        ratios.append([field.mul(lambdas[j], field.inv(lambdas[i])) for j in inputs])
        determinants.append([determinant_2(field, branch_symbol(field, q, t))
                             for t in ratios[-1]])
    minor = determinant_2(field, determinants)
    # Formula: (1-q)^2 t00*t11*q*(lambda1-lambda0)
    #          *(lambda2^-1-lambda3^-1), all factors nonzero.
    expected = field.power(field.sub(field.one, q), 2)
    for factor in (ratios[0][0], ratios[1][1], q,
                   field.sub(lambdas[1], lambdas[0]),
                   field.sub(field.inv(lambdas[2]), field.inv(lambdas[3]))):
        expected = field.mul(expected, factor)
    assert minor == expected and minor != field.zero
    return dict(output_indices=outputs, input_indices=inputs,
                determinant_minor=field.encode(minor),
                factorized_value=field.encode(expected),
                nonzero=True)
