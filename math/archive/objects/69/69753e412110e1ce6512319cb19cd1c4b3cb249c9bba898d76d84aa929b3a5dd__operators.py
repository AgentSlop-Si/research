"""Finite q-Weyl conjugation with its essential wraparound boundary term."""
from dataclasses import dataclass
from fixed_kernel import Counted


@dataclass
class SparsePlan:
    n: int
    q: object
    diagonal: list
    upper: list
    corner: object
    preparation: dict


def prepare_sparse(field, n, q):
    if n < 2 or n & (n-1):
        raise ValueError('N must be a power of two at least 2')
    c = Counted(field)
    powers = [field.one]
    for _ in range(1, n):
        powers.append(c.mul(powers[-1], q))
    diagonal = [powers[(-j) % n] for j in range(n)]
    upper = [c.sub(q, diagonal[j]) for j in range(n-1)]
    half, inverse_n = c.inv(field.integer(2)), field.one
    for _ in range(n.bit_length()-1):
        inverse_n = c.mul(inverse_n, half)
    corner = c.neg(c.mul(q, inverse_n))
    return SparsePlan(n, q, diagonal, upper, corner, dict(c.count))


def apply_sparse_c(field, plan, x):
    """C=B+Q^-1-(q/N)A^(N-1), exactly 2N multiplications and N adds.

The negative corner coefficient is already prepared. The operation does not
materialize a dense matrix or invoke H_q(C).
"""
    if len(x) != plan.n:
        raise ValueError('wrong input length')
    n = plan.n
    out = [field.add(field.mul(plan.diagonal[j], x[j]),
                     field.mul(plan.upper[j], x[j+1])) for j in range(n-1)]
    out.append(field.add(field.mul(plan.diagonal[-1], x[-1]),
                         field.mul(plan.corner, x[0])))
    return out


def apply_c_charged(field, plan, x):
    c = Counted(field)
    result = apply_sparse_c(c, plan, x)
    n = plan.n
    return result, {'field_operations': dict(c.count),
        'input_reads': 2*n, 'coefficient_reads': 2*n, 'output_writes': n}


def horner_c(field, plan, coefficients, x):
    """Fully charged direct polynomial action; a dense degree-N-1 H is quadratic."""
    if not coefficients:
        raise ValueError('nonempty coefficient list required')
    if len(x) != plan.n:
        raise ValueError('wrong input length')
    c, n = Counted(field), plan.n
    out = [c.mul(coefficients[-1], value) for value in x]
    for scalar in reversed(coefficients[:-1]):
        value = apply_sparse_c(c, plan, out)
        out = [c.add(value[j], c.mul(scalar, x[j])) for j in range(n)]
    degree = len(coefficients)-1
    return out, {'field_operations': dict(c.count),
        'sparse_matvecs': degree, 'degree': degree,
        'full_output_writes': n,
        'intermediate_vector_writes': 2*n*degree,
        'model': 'Unit exact field arithmetic and explicit O(log N)-bit word indexing; not bit complexity.'}


def identity(field, n):
    return [[field.one if i == j else field.zero for j in range(n)] for i in range(n)]


def matrix_add(field, a, b):
    return [[field.add(x, y) for x, y in zip(row, other)] for row, other in zip(a, b)]


def matrix_sub(field, a, b):
    return [[field.sub(x, y) for x, y in zip(row, other)] for row, other in zip(a, b)]


def matrix_scale(field, scalar, a):
    return [[field.mul(scalar, value) for value in row] for row in a]


def lower_kernel(field, coefficients):
    n = len(coefficients)
    return [[coefficients[i-j] if i >= j else field.zero for j in range(n)] for i in range(n)]


def build_operators(field, plan, kernel):
    """Dense matrices exist only in this independent audit helper."""
    n = plan.n
    a = [[field.one if i == j+1 else field.zero for j in range(n)] for i in range(n)]
    b = [[plan.upper[i] if j == i+1 else field.zero for j in range(n)] for i in range(n)]
    u = [[plan.diagonal[i] if i == j else field.zero for j in range(n)] for i in range(n)]
    corner = [[plan.corner if i == n-1 and j == 0 else field.zero for j in range(n)] for i in range(n)]
    w = matrix_add(field, b, corner)
    c = matrix_add(field, u, w)
    ha = lower_kernel(field, kernel)
    hb = [[field.zero for _ in range(n)] for _ in range(n)]
    for i in range(n):
        product = field.one
        for j in range(i, n):
            if j > i:
                product = field.mul(product, plan.upper[j-1])
            hb[i][j] = field.mul(kernel[j-i], product)
    return {'A': a, 'B': b, 'U': u, 'W': w, 'C': c,
            'corner': corner, 'H_A': ha, 'H_B': hb}
