"""Exact tridiagonal sandwich for nondegenerate rank-one scan sums.

No Fourier speedup is claimed. The evaluator charges every field operation.
The dense routines below are verification only and are never part of apply().
"""
from dataclasses import dataclass


class Counted:
    def __init__(self, field):
        self.field = field
        self.zero, self.one = field.zero, field.one
        self.counts = dict(add=0, sub=0, mul=0, inv=0)

    def add(self, a, b):
        self.counts['add'] += 1
        return self.field.add(a, b)

    def sub(self, a, b):
        self.counts['sub'] += 1
        return self.field.sub(a, b)

    def mul(self, a, b):
        self.counts['mul'] += 1
        return self.field.mul(a, b)

    def inv(self, a):
        self.counts['inv'] += 1
        return self.field.inv(a)

    def total(self):
        return sum(self.counts.values())


@dataclass
class Sandwich:
    alpha: list
    beta: list
    lower: list
    diagonal: list
    upper: list

    def apply(self, field, values):
        """A = L^-1 T R^-1, using 9N-8 field gates for N>=2."""
        n = len(self.diagonal)
        if len(values) != n:
            raise ValueError('wrong input length')
        z = list(values)
        for i in range(n-2, -1, -1):
            z[i] = field.add(z[i], field.mul(self.beta[i+1], z[i+1]))
        w = [field.mul(self.diagonal[i], z[i]) for i in range(n)]
        for i in range(1, n):
            w[i] = field.add(w[i], field.mul(self.lower[i], z[i-1]))
        for i in range(n-1):
            w[i] = field.add(w[i], field.mul(self.upper[i], z[i+1]))
        for i in range(1, n):
            w[i] = field.add(w[i], field.mul(self.alpha[i], w[i-1]))
        return w

    def blocks(self, zero):
        """Contiguous exact block-diagonal components of T."""
        n = len(self.diagonal)
        starts = [0]
        for i in range(n-1):
            if self.upper[i] == zero and self.lower[i+1] == zero:
                starts.append(i+1)
        return list(zip(starts, starts[1:] + [n]))


def prepare(field, p, q, u, v, diagonal):
    """Strict lower p_i q_j, strict upper u_i v_j, arbitrary diagonal.

    Require all p_i,v_i nonzero. These are coefficients, never fresh data.
    For N>=2, this exact implementation charges 17N-19 field gates;
    an inversion and a multiplication each count as one separate gate.
    """
    n = len(diagonal)
    if n < 2 or any(len(a) != n for a in (p, q, u, v)):
        raise ValueError('equal coefficient arrays of length at least two required')
    if any(a == field.zero for a in p) or any(a == field.zero for a in v):
        raise ValueError('nondegenerate p and v required')
    alpha = [field.zero] + [field.mul(p[i], field.inv(p[i-1])) for i in range(1, n)]
    beta = [field.zero] + [field.mul(v[i], field.inv(v[i-1])) for i in range(1, n)]
    md = [diagonal[0]] + [field.sub(diagonal[i], field.mul(field.mul(alpha[i], u[i-1]), v[i])) for i in range(1, n)]
    lower = [field.zero] + [field.sub(field.mul(p[i], q[i-1]), field.mul(alpha[i], diagonal[i-1])) for i in range(1, n)]
    td = [md[0]] + [field.sub(md[i], field.mul(beta[i], lower[i])) for i in range(1, n)]
    upper = []
    for i in range(n-1):
        ui = u[i] if i == 0 else field.sub(u[i], field.mul(alpha[i], u[i-1]))
        upper.append(field.sub(field.mul(ui, v[i+1]), field.mul(beta[i+1], md[i])))
    upper.append(field.zero)
    return Sandwich(alpha, beta, lower, td, upper)


def generator_matrix(field, p, q, u, v, diagonal):
    return [[diagonal[i] if i == j else field.mul(p[i], q[j]) if i > j else field.mul(u[i], v[j])
             for j in range(len(diagonal))] for i in range(len(diagonal))]


def dense_parts(field, plan):
    n = len(plan.diagonal)
    l = [[field.one if i == j else field.neg(plan.alpha[i]) if i == j+1 else field.zero for j in range(n)] for i in range(n)]
    r = [[field.one if i == j else field.neg(plan.beta[j]) if j == i+1 else field.zero for j in range(n)] for i in range(n)]
    t = [[plan.diagonal[i] if i == j else plan.lower[i] if i == j+1 else plan.upper[i] if j == i+1 else field.zero for j in range(n)] for i in range(n)]
    return l, t, r


def cut_ranks(field, matrix, rank):
    n = len(matrix)
    return [(rank(field, [row[s:] for row in matrix[:s]]), rank(field, [row[:s] for row in matrix[s:]])) for s in range(1, n)]


def permutation_matrix(field, permutation):
    n = len(permutation)
    if sorted(permutation) != list(range(n)):
        raise ValueError('not a permutation')
    return [[field.one if j == permutation[i] else field.zero for j in range(n)] for i in range(n)]


def crossing_counts(permutation):
    n = len(permutation)
    return [sum(permutation[i] >= s for i in range(s)) for s in range(1, n)]


def row_support(matrix, zero):
    return [sum(x != zero for x in row) for row in matrix]
