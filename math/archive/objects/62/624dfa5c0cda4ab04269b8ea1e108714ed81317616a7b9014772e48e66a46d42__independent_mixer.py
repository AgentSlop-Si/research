"""Independently authored phase-12 arithmetic evaluator; no uploaded imports.

The caller supplies an explicit permutation. Validation is a linear seen-array
pass. p=None is floating complex; p=998244353 is an exact finite-field audit
of the unnormalized stage. This is NOT a Fourier transform.
"""
import math


class Arithmetic:
    def __init__(self, p=None):
        self.p = p
        self.count = 0
        self.imag = 1j if p is None else pow(3, (p - 1) // 4, p)
        if p is not None and self.imag * self.imag % p != p - 1:
            raise ValueError('field needs this specified square root of -1')

    def reduce(self, x):
        return x if self.p is None else x % self.p

    def add(self, x, y):
        self.count += 1
        return self.reduce(x + y)

    def sub(self, x, y):
        self.count += 1
        return self.reduce(x - y)

    def mul(self, x, y):
        self.count += 1
        return self.reduce(x * y)

    def inv(self, x):
        self.count += 1
        return 1 / x if self.p is None else pow(x, -1, self.p)


class Forest:
    def __init__(self, parents, alpha, arithmetic):
        self.parents = list(parents)
        self.n = len(parents)
        self.op = arithmetic
        op = arithmetic
        children = [[] for _ in parents]
        roots = []
        for v, parent in enumerate(parents):
            if parent == -1:
                roots.append(v)
            elif type(parent) is int and 0 <= parent < self.n and parent != v:
                children[parent].append(v)
            else:
                raise ValueError('invalid parent')
        self.order = list(roots)
        for v in self.order:
            self.order.extend(children[v])
        if len(self.order) != self.n:
            raise ValueError('parent graph has a cycle')
        self.q = [0] * self.n
        alpha2 = op.mul(alpha, alpha)
        for v in reversed(self.order):
            d = 1
            for c in children[v]:
                d = op.add(d, op.mul(alpha2, self.q[c]))
            self.q[v] = op.inv(d)
        s = op.mul(op.imag, alpha)
        self.g = [op.mul(s, q) for q in self.q]

    def apply(self, x, inverse=False):
        if len(x) != self.n:
            raise ValueError('length mismatch')
        op = self.op
        # Negation of precomputed couplings is charged in inverse applications.
        g = [op.sub(0, v) for v in self.g] if inverse else self.g
        rhs = list(x)
        for v in reversed(self.order):
            parent = self.parents[v]
            if parent != -1:
                rhs[parent] = op.add(rhs[parent], op.mul(g[v], rhs[v]))
        y = [0] * self.n
        for v in self.order:
            value = op.mul(self.q[v], rhs[v])
            parent = self.parents[v]
            if parent != -1:
                value = op.add(value, op.mul(g[v], y[parent]))
            y[v] = value
        return [op.sub(op.mul(2, v), z) for v, z in zip(y, x)]


def validate_and_invert(order):
    n = len(order)
    inverse = [-1] * n
    for i, v in enumerate(order):
        if type(v) is not int or v < 0 or v >= n or inverse[v] != -1:
            raise ValueError('not a permutation')
        inverse[v] = i
    return inverse


def path_parents(order):
    parents = [-1] * len(order)
    for i in range(1, len(order)):
        parents[order[i]] = order[i - 1]
    return parents


class Mixer:
    def __init__(self, row_permutation, p=None):
        n = len(row_permutation)
        if n < 2 or n % 2:
            raise ValueError('positive even length required')
        inverted = validate_and_invert(row_permutation)
        self.n = n
        self.m = n // 2
        self.op = Arithmetic(p)
        op = self.op
        a = op.inv(32)
        self.path1 = Forest(path_parents(list(range(n))), a, op)
        self.path2 = Forest(path_parents(inverted), a, op)
        size = 1
        while 2 * size + 1 <= self.m:
            size = 2 * size + 1
        self.tree_size = size
        tree_parent = [-1 if v == 0 or v >= size else (v - 1) // 2
                       for v in range(self.m)]
        self.tree = Forest(tree_parent, 2, op)
        self.e = op.inv(512)
        self.ie = op.mul(op.imag, self.e)
        denom = op.add(1, op.mul(self.e, self.e))
        self.reverse_scale = op.inv(denom)
        # sqrt of a single N-independent constant, charged separately.
        self.normalization = 1 / math.sqrt(denom) if p is None else 1

    def involution(self, x):
        return (self.tree.apply(x[self.m:]) +
                self.tree.apply(x[:self.m], inverse=True))

    def rotation(self, x, inverse=False):
        op = self.op
        coefficient = op.sub(0, self.ie) if inverse else self.ie
        rx = self.involution(x)
        y = [op.add(v, op.mul(coefficient, w)) for v, w in zip(x, rx)]
        scale = self.normalization
        if op.p is not None and inverse:
            scale = self.reverse_scale
        return [op.mul(scale, v) for v in y]

    def apply(self, x, inverse=False):
        if len(x) != self.n:
            raise ValueError('length mismatch')
        if inverse:
            y = self.rotation(x, inverse=True)
            y = self.path1.apply(y, inverse=True)
            return self.path2.apply(y, inverse=True)
        return self.rotation(self.path1.apply(self.path2.apply(x)))

