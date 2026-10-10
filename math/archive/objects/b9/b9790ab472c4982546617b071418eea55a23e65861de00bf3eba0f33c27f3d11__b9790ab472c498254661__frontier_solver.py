"""Independent deterministic exact solver for a fixed band plus fixed entries.

No imports from any submitted source. The modulus must be a known prime.
Field-operation complexity is linear in n when bandwidth and the number of
exceptional rows/entries are fixed. Factorization uses row pivoting; it does
not require the band-only matrix or any prescribed principal minor invertible.
"""
from dataclasses import dataclass


@dataclass
class FrontierFactor:
    p: int
    pivots: list
    max_active: int
    max_row_nonzeros: int
    elimination_updates: int

    def solve(self, rhs):
        n = len(self.pivots)
        if len(rhs) != n:
            raise ValueError('RHS length mismatch')
        b = [x % self.p for x in rhs]
        for rid, inv, upper, eliminations in self.pivots:
            for other, coefficient in eliminations:
                b[other] = (b[other] - coefficient * b[rid]) % self.p
        x = [0] * n
        for j in range(n - 1, -1, -1):
            rid, inv, upper, eliminations = self.pivots[j]
            val = b[rid]
            for k, coefficient in upper:
                val = (val - coefficient * x[k]) % self.p
            x[j] = val * inv % self.p
        return x


def factor(rows, width, p):
    """Factor a sparse square matrix supplied as row dictionaries.

    Rows containing any entry outside the declared symmetric band are
    exceptional. Every exceptional row is activated initially. Ordinary rows
    enter before column j when their original index is <= j + width. A pivot
    must exist in this bounded frontier iff the square matrix is nonsingular.
    Raises ArithmeticError on singularity. No dense fallback is used.
    """
    n = len(rows)
    if width < 0 or p < 2:
        raise ValueError('Bad width or prime')
    a = []
    for row in rows:
        clean = {}
        for k, v in row.items():
            if not isinstance(k, int) or not 0 <= k < n:
                raise ValueError('Column index outside matrix')
            if v % p:
                clean[k] = v % p
        a.append(clean)
    exceptional = {i for i, row in enumerate(a)
                   if any(abs(i - j) > width for j in row)}
    active = {i: a[i] for i in exceptional}
    cursor = 0
    pivots = []
    max_active = len(active)
    max_row_nonzeros = max((len(r) for r in a), default=0)
    updates = 0
    for j in range(n):
        while cursor < n and cursor <= j + width:
            if cursor not in exceptional:
                active[cursor] = a[cursor]
            cursor += 1
        max_active = max(max_active, len(active))
        rid = next((i for i, row in active.items() if row.get(j, 0)), None)
        if rid is None:
            raise ArithmeticError(f'Singular matrix: no pivot in column {j}')
        row = active.pop(rid)
        inv = pow(row[j], -1, p)
        upper = [(k, v) for k, v in row.items() if k > j]
        eliminations = []
        for other, target in active.items():
            coefficient = target.pop(j, 0) * inv % p
            if not coefficient:
                continue
            eliminations.append((other, coefficient))
            for k, v in upper:
                new = (target.get(k, 0) - coefficient * v) % p
                if new:
                    target[k] = new
                else:
                    target.pop(k, None)
                updates += 1
            max_row_nonzeros = max(max_row_nonzeros, len(target))
        pivots.append((rid, inv, upper, eliminations))
    return FrontierFactor(p, pivots, max_active, max_row_nonzeros, updates)


def successor(order):
    n = len(order)
    seen = [False] * n
    w = [0] * n
    for t, j in enumerate(order):
        if not isinstance(j, int) or not 0 <= j < n or seen[j]:
            raise ValueError('Not a permutation')
        seen[j] = True
        w[j] = order[(t + 1) % n]
    return w


def two_run(n, a):
    return [(a * t) % n for t in range(n // 2)] + [
        (-1 - a * t) % n for t in range(n // 2)]


def four_track(n):
    return [j for t in range(n // 4)
            for j in (2*t, 2*t+1, 2*t+n//2, 2*t+n//2+1)]


def sparse_denominator(n, alpha, beta, p, a=None):
    if n < 16 or n & (n - 1):
        raise ValueError('Dyadic n >= 16 required')
    if a is None:
        a = n // 2 + 2
    w = successor(two_run(n, a))
    order = four_track(n)
    location = [0] * n
    for j, old in enumerate(order):
        location[old] = j
    rows = [{i: 2 % p} for i in range(n)]
    for old in range(n):
        j = location[old]
        for target, coefficient in ((w[old], -alpha), ((old+1) % n, -beta)):
            i = location[target]
            rows[i][j] = (rows[i].get(j, 0) + coefficient) % p
    return rows, order


def green_apply(order, alpha, x, p):
    n = len(order)
    denominator = (1 - pow(alpha, n, p)) % p
    if not denominator:
        raise ArithmeticError('Singular cyclic resolvent')
    # y[L[0]] = (x[L[0]] + sum_{t=1}^{n-1} alpha^(n-t)x[L[t]])/(1-alpha^n).
    accumulator = 0
    for t in range(1, n):
        accumulator = alpha * (accumulator + x[order[t]]) % p
    value = (x[order[0]] + accumulator) * pow(denominator, -1, p) % p
    y = [0] * n
    y[order[0]] = value
    for t in range(1, n):
        value = (x[order[t]] + alpha * value) % p
        y[order[t]] = value
    return y


def sparse_apply(order, alpha, x, p):
    y = [v % p for v in x]
    for t, j in enumerate(order):
        i = order[(t+1) % len(order)]
        y[i] = (y[i] - alpha*x[j]) % p
    return y


@dataclass
class TwistedInverse:
    n: int
    alpha: int
    beta: int
    p: int
    reordering: list
    factors: FrontierFactor

    @classmethod
    def create(cls, n, alpha, beta, p):
        if pow(alpha, n, p) == 1 or pow(beta, n, p) == 1:
            raise ArithmeticError('Singular cyclic resolvent')
        rows, order = sparse_denominator(n, alpha, beta, p)
        factors = factor(rows, 6, p)
        return cls(n, alpha % p, beta % p, p, order, factors)

    def apply(self, x):
        first = sparse_apply(two_run(self.n, self.n//2+2), self.alpha, x, self.p)
        solved = self.factors.solve([first[i] for i in self.reordering])
        original = [0] * self.n
        for k, j in enumerate(self.reordering):
            original[j] = solved[k]
        return sparse_apply(list(range(self.n)), self.beta, original, self.p)
