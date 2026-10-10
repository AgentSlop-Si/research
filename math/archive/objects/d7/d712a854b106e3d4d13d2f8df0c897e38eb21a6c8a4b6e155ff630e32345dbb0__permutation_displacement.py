#!/usr/bin/env python3
"""Exact certificates for the permutation-displacement Fourier gate.

For F_N[k,j]=omega^(k*j), output cyclic shift Z satisfies Z F = F D
(up to the selected shift convention), where D=diag(omega^j).
For an input permutation P, rank(ZF-FP)=rank(D-P).

The nullity of D-P equals the number of permutation cycles whose index sum is
0 modulo N. Consequently min_P rank(D-P)=floor(N/2).

This module contains independent finite-field verification, exhaustive small-N
searches, and explicit minimizers. It is a scoped obstruction, not a general
FFT lower bound.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from typing import Iterable, Sequence
import math
import sympy as sp


def cycles_of(perm: Sequence[int]) -> list[list[int]]:
    n = len(perm)
    seen = [False] * n
    out: list[list[int]] = []
    for i in range(n):
        if seen[i]:
            continue
        c = []
        j = i
        while not seen[j]:
            seen[j] = True
            c.append(j)
            j = perm[j]
        out.append(c)
    return out


def zero_sum_cycle_count(perm: Sequence[int]) -> int:
    n = len(perm)
    return sum(1 for c in cycles_of(perm) if sum(c) % n == 0)


def predicted_rank(perm: Sequence[int]) -> int:
    return len(perm) - zero_sum_cycle_count(perm)


def explicit_minimizer(n: int) -> tuple[int, ...]:
    """Permutation achieving rank floor(n/2).

    It fixes 0, transposes j with -j, and for even n fixes n/2.
    """
    if n < 2:
        raise ValueError("n >= 2")
    p = list(range(n))
    for j in range(1, (n + 1) // 2):
        k = (-j) % n
        p[j] = k
        p[k] = j
    return tuple(p)


def theoretical_min_rank(n: int) -> int:
    if n < 2:
        raise ValueError("n >= 2")
    return n // 2


def find_prime_root(n: int) -> tuple[int, int]:
    """Return prime p and primitive n-th root omega modulo p."""
    if n < 2:
        raise ValueError("n >= 2")
    c = 1
    while True:
        p = c * n + 1
        if sp.isprime(p):
            g = sp.primitive_root(p)
            omega = pow(int(g), c, p)
            # Exact order check.
            if pow(omega, n, p) != 1:
                raise AssertionError("root failure")
            for q in sp.factorint(n):
                if pow(omega, n // q, p) == 1:
                    raise AssertionError("nonprimitive root")
            return int(p), int(omega)
        c += 1


def rank_mod(matrix: Sequence[Sequence[int]], p: int) -> int:
    a = [list(map(lambda x: int(x) % p, row)) for row in matrix]
    if not a:
        return 0
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c] % p), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], p - 2, p)
        a[r] = [(v * inv) % p for v in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [(a[i][j] - q * a[r][j]) % p for j in range(n)]
        r += 1
        if r == m:
            break
    return r


def d_minus_p_matrix(n: int, perm: Sequence[int], p: int, omega: int) -> list[list[int]]:
    a = [[0] * n for _ in range(n)]
    # P e_j = e_{perm[j]}; matrix has P[perm[j],j]=1.
    for j in range(n):
        a[j][j] = pow(omega, j, p)
        a[perm[j]][j] = (a[perm[j]][j] - 1) % p
    return a


def fourier_matrix(n: int, p: int, omega: int) -> list[list[int]]:
    return [[pow(omega, (k * j) % n, p) for j in range(n)] for k in range(n)]


def matmul(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]], p: int) -> list[list[int]]:
    m, q, n = len(a), len(b), len(b[0])
    if len(a[0]) != q:
        raise ValueError("shape mismatch")
    out = [[0] * n for _ in range(m)]
    for i in range(m):
        for t in range(q):
            at = a[i][t] % p
            if at:
                for j in range(n):
                    out[i][j] = (out[i][j] + at * b[t][j]) % p
    return out


def submat(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]], p: int) -> list[list[int]]:
    return [[(x - y) % p for x, y in zip(rx, ry)] for rx, ry in zip(a, b)]


def permutation_matrix(perm: Sequence[int]) -> list[list[int]]:
    n = len(perm)
    out = [[0] * n for _ in range(n)]
    for j, i in enumerate(perm):
        out[i][j] = 1
    return out


def output_shift_matrix(n: int) -> list[list[int]]:
    """Z e_k=e_(k+1); then (Z F)[k,j]=F[k-1,j]."""
    out = [[0] * n for _ in range(n)]
    for j in range(n):
        out[(j + 1) % n][j] = 1
    return out


def fourier_displacement_rank(n: int, perm: Sequence[int]) -> int:
    p, omega = find_prime_root(n)
    f = fourier_matrix(n, p, omega)
    z = output_shift_matrix(n)
    pm = permutation_matrix(perm)
    # With our shift convention ZF = F*diag(omega^{-j}).  Use inverse root
    # in D-P certificate, which has the same zero-sum cycle criterion.
    lhs = matmul(z, f, p)
    rhs = matmul(f, pm, p)
    return rank_mod(submat(lhs, rhs, p), p)


def d_minus_p_rank(n: int, perm: Sequence[int]) -> int:
    p, omega = find_prime_root(n)
    # Output shift convention uses omega^{-j}; replace omega by inverse.
    return rank_mod(d_minus_p_matrix(n, perm, p, pow(omega, p - 2, p)), p)


def exhaustive_minimum(n: int) -> dict:
    if n > 10:
        raise ValueError("exhaustive search intended for n<=10")
    best = n + 1
    count = 0
    example = None
    histogram: dict[int, int] = {}
    for perm in permutations(range(n)):
        r = predicted_rank(perm)
        histogram[r] = histogram.get(r, 0) + 1
        if r < best:
            best, count, example = r, 1, perm
        elif r == best:
            count += 1
    return {
        "n": n,
        "minimum_rank": best,
        "theoretical_minimum": theoretical_min_rank(n),
        "number_of_minimizers": count,
        "example": list(example) if example is not None else None,
        "histogram": {str(k): v for k, v in sorted(histogram.items())},
    }


def verify_random(n: int, perms: Iterable[Sequence[int]]) -> list[dict]:
    p, omega = find_prime_root(n)
    inv = pow(omega, p - 2, p)
    rows = []
    for perm in perms:
        pred = predicted_rank(perm)
        exact = rank_mod(d_minus_p_matrix(n, perm, p, inv), p)
        disp = fourier_displacement_rank(n, perm)
        if pred != exact or exact != disp:
            raise AssertionError((n, perm, pred, exact, disp))
        rows.append({"predicted": pred, "matrix_rank": exact, "fourier_displacement_rank": disp})
    return rows


if __name__ == "__main__":
    import json, random
    out = {"exhaustive": [exhaustive_minimum(n) for n in range(2, 10)]}
    rng = random.Random(20261010)
    random_checks = []
    for n in (11, 12, 16, 25, 32, 49, 64):
        ps = []
        for _ in range(12):
            p = list(range(n)); rng.shuffle(p); ps.append(tuple(p))
        ps.append(explicit_minimizer(n))
        random_checks.append({"n": n, "rows": verify_random(n, ps)})
    out["random_checks"] = random_checks
    print(json.dumps(out, indent=2))
