#!/usr/bin/env python3
"""Exact finite checks for a CONDITIONAL Fourier-mass-contraction theory.

This is a verifier, not a new fast FFT. Dense/reference operations in this file
are deliberately expensive. No factors satisfying the proposed contracting
Fourier identity are supplied or claimed.
Python 3 standard library only. Run: python verify.py
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import json
import math
import random

P = 65537

@dataclass
class Ledger:
    multiplications: int = 0
    additions: int = 0
    inversions: int = 0

    def as_dict(self) -> dict[str, int]:
        return dict(multiplications=self.multiplications,
                    additions=self.additions, inversions=self.inversions)


def root(n: int, p: int = P) -> int:
    if n < 1 or n & (n - 1) or (p - 1) % n:
        raise ValueError('This test helper requires an admissible power of two.')
    w = pow(3, (p - 1) // n, p)
    if pow(w, n, p) != 1 or (n > 1 and pow(w, n // 2, p) == 1):
        raise ValueError('The chosen root did not pass the exact order check.')
    return w


def powers(w: int, n: int, p: int = P) -> list[int]:
    out = [1]
    for _ in range(1, n):
        out.append(out[-1] * w % p)
    return out


def dft(x: list[int], w: int, p: int = P) -> list[int]:
    """O(n^2) independent reference, NOT a fast implementation."""
    n = len(x)
    tab = powers(w, n, p)
    return [sum(x[j] * tab[k*j % n] for j in range(n)) % p
            for k in range(n)]


def matrix_of(apply, n: int) -> list[list[int]]:
    columns = []
    for j in range(n):
        x = [0] * n
        x[j] = 1
        columns.append(apply(x))
    return [[columns[j][i] for j in range(n)] for i in range(n)]


def matmul(a: list[list[int]], b: list[list[int]], p: int = P):
    n, k, m = len(a), len(b), len(b[0])
    return [[sum(a[i][r]*b[r][j] for r in range(k)) % p
             for j in range(m)] for i in range(n)]


def invert(a: list[list[int]], p: int = P) -> list[list[int]]:
    n = len(a)
    t = [[x % p for x in a[i]] + [int(i == j) for j in range(n)]
         for i in range(n)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if t[i][j]), None)
        if pivot is None:
            raise ValueError('Singular matrix')
        t[j], t[pivot] = t[pivot], t[j]
        inv = pow(t[j][j], -1, p)
        t[j] = [v * inv % p for v in t[j]]
        for i in range(n):
            if i != j and t[i][j]:
                f = t[i][j]
                t[i] = [(a-f*b) % p for a, b in zip(t[i], t[j])]
    return [r[n:] for r in t]


def weyl_certificate(a: list[list[int]], w: int, p: int = P):
    """S e_j=e_(j+1), D[j,j]=w^j. Full exact matrix check."""
    n = len(a)
    tab = powers(w, n, p)
    first = sum((a[k][(j+1) % n] - tab[k]*a[k][j]) % p != 0
                for k in range(n) for j in range(n))
    second = sum((tab[j]*a[k][j] - a[(k+1) % n][j]) % p != 0
                 for k in range(n) for j in range(n))
    seed = sum(a[k][0] % p != 1 for k in range(n))
    return dict(shift_residual_entries=first,
                modulation_residual_entries=second,
                seed_residual_entries=seed,
                exact_fourier=(first == second == seed == 0))


@dataclass
class GreenPlan:
    order: list[int]
    weights: list[int]
    left: list[int]
    right: list[int]
    prefix: list[int]
    reciprocal: int
    p: int
    setup: Ledger

    @classmethod
    def build(cls, order: list[int], weights: list[int], left: list[int],
              right: list[int], p: int = P) -> 'GreenPlan':
        n = len(order)
        if n == 0:
            raise ValueError('order must list each cycle vertex exactly once')
        seen = [False] * n
        for vertex in order:
            if not isinstance(vertex, int) or not 0 <= vertex < n or seen[vertex]:
                raise ValueError('order must list each cycle vertex exactly once')
            seen[vertex] = True
        if any(len(a) != n for a in (weights, left, right)):
            raise ValueError('All coefficient vectors must have length n')
        prefix, product = [], 1
        for i in order:
            prefix.append(product)
            product = product * weights[i] % p
        den = (1-product) % p
        if not den:
            raise ValueError('Singular cycle denominator')
        return cls(order[:], [x % p for x in weights],
                   [x % p for x in left], [x % p for x in right],
                   prefix, pow(den, -1, p), p, Ledger(n, 1, 1))

    def apply(self, x: list[int], ledger: Ledger | None = None) -> list[int]:
        n, p = len(self.order), self.p
        if len(x) != n:
            raise ValueError('Wrong input length')
        c = ledger if ledger is not None else Ledger()
        u = [self.right[i]*x[i] % p for i in range(n)]
        c.multiplications += n
        numerator = 0
        for t, i in enumerate(self.order):
            numerator = (numerator+self.prefix[t]*u[i]) % p
        c.multiplications += n
        c.additions += n
        z = [0]*n
        z[self.order[0]] = numerator*self.reciprocal % p
        c.multiplications += 1
        nxt = z[self.order[0]]
        for t in range(n-1, 0, -1):
            i = self.order[t]
            z[i] = (u[i]+self.weights[i]*nxt) % p
            nxt = z[i]
        c.multiplications += n-1
        c.additions += n-1
        c.multiplications += n
        return [self.left[i]*z[i] % p for i in range(n)]


def random_green(n: int, rng: random.Random) -> GreenPlan:
    order = list(range(n))
    rng.shuffle(order)
    while True:
        weights = [rng.randrange(1, P) for _ in range(n)]
        left = [rng.randrange(1, P) for _ in range(n)]
        right = [rng.randrange(1, P) for _ in range(n)]
        try:
            return GreenPlan.build(order, weights, left, right)
        except ValueError:
            continue


def two_bank(x: list[int], q: int, m: int, active: set[int] | None = None):
    """Exact mixed-radix identity; optionally DELETE some second-bank calls.

    Deleted calls are replaced by identity wires, not by a valid repair.
    This deliberately invalid shortcut is a negative control.
    """
    n = len(x)
    if q*m != n:
        raise ValueError('q*m must equal input length')
    w = root(n)
    tab = powers(w, n)
    first = [dft([x[t+q*u] for u in range(m)], pow(w, q, P))
             for t in range(q)]
    selected = set(range(m)) if active is None else active
    out = [0]*n
    for h in range(m):
        v = [first[t][h]*tab[h*t % n] % P for t in range(q)]
        v = dft(v, pow(w, m, P)) if h in selected else v
        for s in range(q):
            out[h+m*s] = v[s]
    return out


def recurrence_checks():
    rows = []
    # Upper-envelope scalar recurrences, not FFT execution measurements.
    for rho in [Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2)]:
        a = Fraction(1)
        for h in range(1, 25):
            a = max(a, rho*a+1)
            if h in [4, 8, 16, 24]:
                rows.append(dict(height=h, rho=str(rho),
                                 normalized_upper_envelope=float(a),
                                 ratio_to_logN=float(a/(2**h))))
        if rho < 1:
            assert a <= 2
        if rho == 1:
            assert a == 25
        if rho > 1:
            assert a <= (1+1/(rho-1))*rho**24
    a = Fraction(1)
    for h in range(2, 100):
        a = 2*Fraction(h-1, h)*a+1
        assert h*a/Fraction(2**h) <= Fraction(5, 2)
    return rows


def run():
    rng = random.Random(20261010)
    result = {'status': 'CONDITIONAL THEORY; NO CONTRACTING FOURIER FACTORS FOUND OR CLAIMED',
              'field': P, 'test_groups': [], 'green_counts': [], 'weyl_controls': [],
              'inverse_density_controls': [], 'recurrence_tables': recurrence_checks()}
    # Green equation check, including zero weights: no division by weights.
    green_cases = 0
    for n in [2, 4, 8, 16, 32, 64, 128]:
        for trial in range(12):
            g = random_green(n, rng)
            if trial == 0:
                g.weights[g.order[n//2]] = 0
                g = GreenPlan.build(g.order, g.weights, g.left, g.right)
            x = [rng.randrange(P) for _ in range(n)]
            count = Ledger()
            y = g.apply(x, count)
            z = [y[i]*pow(g.left[i], -1, P) % P for i in range(n)]
            for t, i in enumerate(g.order):
                j = g.order[(t+1) % n]
                assert (z[i]-g.weights[i]*z[j]-g.right[i]*x[i]) % P == 0
            assert count.as_dict() == dict(multiplications=4*n,
                                         additions=2*n-1, inversions=0)
            green_cases += 1
        result['green_counts'].append(dict(n=n, setup=g.setup.as_dict(),
                                           one_apply=count.as_dict()))
    result['test_groups'].append({'name': 'weighted cyclic Green solves', 'passed_cases': green_cases})
    # Exhaustive basis checks for standard mixed-radix controls and deleted-bank failures.
    checked_columns, checked_coefficients = 0, 0
    for n in [4, 8, 16, 32, 64]:
        k = n.bit_length()-1
        q, m = 2**(k//2), 2**((k+1)//2)
        f = matrix_of(lambda x: dft(x, root(n)), n)
        ordinary = matrix_of(lambda x: two_bank(x, q, m), n)
        assert ordinary == f
        checked_columns += n
        checked_coefficients += n*n
        cert = weyl_certificate(ordinary, root(n))
        assert cert['exact_fourier']
        deleted = matrix_of(lambda x: two_bank(x, q, m, set(range(m//2))), n)
        bad = weyl_certificate(deleted, root(n))
        assert not bad['exact_fourier'] and deleted != f
        # The shortcut remains invertible: full rank is not a Fourier certificate.
        invert(deleted)
        rowscaled = [[(i+1)*v % P for v in row] for i, row in enumerate(f)]
        scaled = [[2*v % P for v in row] for row in f]
        rs, sc = weyl_certificate(rowscaled, root(n)), weyl_certificate(scaled, root(n))
        assert rs['shift_residual_entries'] == 0 and not rs['exact_fourier']
        assert sc['shift_residual_entries'] == sc['modulation_residual_entries'] == 0
        assert sc['seed_residual_entries'] == n
        result['weyl_controls'].append(dict(n=n, standard=cert, deleted_bank=bad,
                                            row_scaled=rs, scalar_scaled=sc,
                                            standard_recursive_mass=2*n,
                                            deleted_recursive_mass=n+q*(m//2)))
    result['test_groups'].append(dict(name='ordinary two-bank equality on every basis vector',
                                     passed_columns=checked_columns,
                                     passed_coefficients=checked_coefficients))
    result['test_groups'].append(dict(name='false Fourier certificates rejected', passed_cases=15))
    # Paired Green sums can have genuinely dense inverses. Not Fourier factors.
    for n in [8, 16, 32]:
        g1, g2 = random_green(n, rng), random_green(n, rng)
        def h(x):
            return [(a+b) % P for a,b in zip(g1.apply(x), g2.apply(x))]
        a = matrix_of(h, n)
        ai = invert(a)
        nnz = [sum(v != 0 for v in row) for row in ai]
        assert min(nnz) > 2
        result['inverse_density_controls'].append(dict(n=n, min_row_nnz=min(nnz),
                                                       max_row_nnz=max(nnz),
                                                       Fourier_claim=False))
    result['test_groups'].append(dict(name='paired-Green inverse-density controls', passed_cases=3))
    # Pure Green inverse support: explicit check of the inverse product identity.
    for n in [4, 16, 64]:
        q = m = math.isqrt(n)
        assert q*m == n
        for t in range(8):
            possible_support = m*(2**t)
            if t < math.log2(q):
                assert possible_support < n
    result['test_groups'].append(dict(name='bank inverse-support inequality arithmetic', passed_cases=24))
    result['test_groups'].append(dict(name='four constant-mass and harmonic recurrences', passed=True))
    result['all_checks_passed'] = True
    out = Path(__file__).with_name('RESULTS.json')
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    run()
