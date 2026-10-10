from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import prod
from random import Random
from typing import Iterable, Sequence

Matrix = list[list[int]]
Vector = tuple[int, ...]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def prime_factors(n: int) -> list[int]:
    out: list[int] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.append(n)
    return out


def primitive_root(p: int) -> int:
    if not is_prime(p):
        raise ValueError("modulus must be prime")
    factors = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise RuntimeError("primitive root not found")


def coefficient_field(order: int) -> tuple[int, int]:
    """Return prime ell and a primitive `order`-th root in F_ell."""
    if order < 2:
        raise ValueError("order must be at least 2")
    for k in range(1, 200000):
        ell = k * order + 1
        if is_prime(ell):
            g = primitive_root(ell)
            zeta = pow(g, (ell - 1) // order, ell)
            if pow(zeta, order, ell) == 1 and all(
                pow(zeta, order // q, ell) != 1 for q in prime_factors(order)
            ):
                return ell, zeta
    raise RuntimeError(f"coefficient field not found for order {order}")


def zeros(rows: int, cols: int | None = None) -> Matrix:
    if cols is None:
        cols = rows
    return [[0] * cols for _ in range(rows)]


def identity(n: int) -> Matrix:
    out = zeros(n)
    for i in range(n):
        out[i][i] = 1
    return out


def mat_mul(a: Matrix, b: Matrix, mod: int) -> Matrix:
    if not a or not b or len(a[0]) != len(b):
        raise ValueError("shape mismatch")
    bt = list(zip(*b))
    return [
        [sum(x * y for x, y in zip(row, col)) % mod for col in bt]
        for row in a
    ]


def mat_add(a: Matrix, b: Matrix, mod: int) -> Matrix:
    return [[(x + y) % mod for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def transpose(a: Matrix) -> Matrix:
    return [list(col) for col in zip(*a)]


def mat_inv(a: Matrix, mod: int) -> Matrix:
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("matrix must be square")
    aug = [
        [x % mod for x in row] + [1 if i == j else 0 for j in range(n)]
        for i, row in enumerate(a)
    ]
    for col in range(n):
        pivot = next((r for r in range(col, n) if aug[r][col] % mod), None)
        if pivot is None:
            raise ZeroDivisionError("singular matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        inv = pow(aug[col][col], -1, mod)
        aug[col] = [(v * inv) % mod for v in aug[col]]
        for r in range(n):
            if r == col:
                continue
            factor = aug[r][col] % mod
            if factor:
                aug[r] = [(x - factor * y) % mod for x, y in zip(aug[r], aug[col])]
    return [row[n:] for row in aug]


def rank_mod(a: Matrix, mod: int) -> int:
    if not a:
        return 0
    m = [[x % mod for x in row] for row in a]
    rows, cols = len(m), len(m[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if m[r][col]), None)
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        inv = pow(m[rank][col], -1, mod)
        m[rank] = [(x * inv) % mod for x in m[rank]]
        for r in range(rows):
            if r == rank:
                continue
            factor = m[r][col]
            if factor:
                m[r] = [(x - factor * y) % mod for x, y in zip(m[r], m[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def block_matrix(a: Matrix, b: Matrix, c: Matrix, d: Matrix) -> Matrix:
    n = len(a)
    return [a[i] + b[i] for i in range(n)] + [c[i] + d[i] for i in range(n)]


def vectors(p: int, n: int) -> list[Vector]:
    return [tuple(x) for x in product(range(p), repeat=n)]


def vector_index(v: Sequence[int], p: int) -> int:
    out = 0
    for x in v:
        out = out * p + (x % p)
    return out


def dot(x: Sequence[int], y: Sequence[int], p: int) -> int:
    return sum(a * b for a, b in zip(x, y)) % p


def mat_vec_small(a: Matrix, x: Sequence[int], p: int) -> Vector:
    return tuple(sum(v * w for v, w in zip(row, x)) % p for row in a)


def random_invertible(n: int, p: int, rng: Random) -> Matrix:
    while True:
        a = [[rng.randrange(p) for _ in range(n)] for _ in range(n)]
        if rank_mod(a, p) == n:
            return a


def random_symmetric(n: int, p: int, rng: Random) -> Matrix:
    out = zeros(n)
    for i in range(n):
        for j in range(i, n):
            out[i][j] = out[j][i] = rng.randrange(p)
    return out


def symplectic_form(n: int, p: int) -> Matrix:
    i = identity(n)
    z = zeros(n)
    neg_i = [[(-x) % p for x in row] for row in i]
    return block_matrix(z, i, neg_i, z)


def is_symplectic(s: Matrix, p: int) -> bool:
    n2 = len(s)
    if n2 % 2:
        return False
    n = n2 // 2
    lhs = mat_mul(mat_mul(transpose(s), symplectic_form(n, p), p), s, p)
    return lhs == symplectic_form(n, p)


def symplectic_identity(n: int) -> Matrix:
    return identity(2 * n)


def lower_chirp_symplectic(c: Matrix, p: int) -> Matrix:
    n = len(c)
    if c != transpose(c):
        raise ValueError("chirp matrix must be symmetric")
    i, z = identity(n), zeros(n)
    return block_matrix(i, z, [[x % p for x in row] for row in c], i)


def linear_symplectic(a: Matrix, p: int) -> Matrix:
    n = len(a)
    inv_t = transpose(mat_inv(a, p))
    z = zeros(n)
    return block_matrix([[x % p for x in row] for row in a], z, z, inv_t)


def partial_weyl_symplectic(n: int, coords: Iterable[int], p: int) -> Matrix:
    js = set(coords)
    a, b, c, d = zeros(n), zeros(n), zeros(n), zeros(n)
    for k in range(n):
        if k in js:
            b[k][k] = (-1) % p
            c[k][k] = 1
        else:
            a[k][k] = 1
            d[k][k] = 1
    return block_matrix(a, b, c, d)


def upper_right_rank(s: Matrix, p: int) -> int:
    n = len(s) // 2
    return rank_mod([row[n:] for row in s[:n]], p)


def chirp_operator(c: Matrix, p: int, ell: int, omega: int) -> Matrix:
    n = len(c)
    pts = vectors(p, n)
    inv2 = pow(2, -1, p)
    out = zeros(len(pts))
    for idx, x in enumerate(pts):
        cx = mat_vec_small(c, x, p)
        exponent = inv2 * dot(x, cx, p) % p
        out[idx][idx] = pow(omega, exponent, ell)
    return out


def linear_operator(a: Matrix, p: int, ell: int) -> Matrix:
    n = len(a)
    pts = vectors(p, n)
    out = zeros(len(pts))
    for j, y in enumerate(pts):
        x = mat_vec_small(a, y, p)
        out[vector_index(x, p)][j] = 1 % ell
    return out


def partial_fourier_operator(n: int, coords: Iterable[int], p: int, ell: int, omega: int) -> Matrix:
    js = set(coords)
    pts = vectors(p, n)
    out = zeros(len(pts))
    for i, x in enumerate(pts):
        for j, y in enumerate(pts):
            if any(x[k] != y[k] for k in range(n) if k not in js):
                continue
            exponent = sum(x[k] * y[k] for k in js) % p
            out[i][j] = pow(omega, exponent, ell)
    return out


def tensor_fourier(p: int, n: int, ell: int, omega: int) -> Matrix:
    return partial_fourier_operator(n, range(n), p, ell, omega)


def cyclic_fourier(q: int, ell: int, zeta: int) -> Matrix:
    return [[pow(zeta, (i * j) % q, ell) for j in range(q)] for i in range(q)]


def bilinear_fourier(m: Matrix, p: int, ell: int, omega: int) -> Matrix:
    n = len(m)
    pts = vectors(p, n)
    out = zeros(len(pts))
    for i, x in enumerate(pts):
        for j, y in enumerate(pts):
            out[i][j] = pow(omega, dot(x, mat_vec_small(m, y, p), p), ell)
    return out


def column_permutation_for_linear(m: Matrix, p: int) -> list[int]:
    pts = vectors(p, len(m))
    # Column y in bilinear form equals column M y in the standard tensor Fourier.
    return [vector_index(mat_vec_small(m, y, p), p) for y in pts]


def permute_columns(a: Matrix, perm: Sequence[int]) -> Matrix:
    return [[row[j] for j in perm] for row in a]


def support_counts(a: Matrix, mod: int) -> tuple[list[int], list[int]]:
    rows = [sum(x % mod != 0 for x in row) for row in a]
    cols = [sum(a[i][j] % mod != 0 for i in range(len(a))) for j in range(len(a[0]))]
    return rows, cols


def cross_ratio(a: Matrix, i: int, k: int, j: int, l: int, mod: int) -> int:
    den = a[i][l] * a[k][j] % mod
    if den == 0:
        raise ZeroDivisionError("cross ratio requires nonzero entries")
    return a[i][j] * a[k][l] % mod * pow(den, -1, mod) % mod


def random_generator(p: int, n: int, ell: int, omega: int, rng: Random) -> tuple[Matrix, Matrix, str, int]:
    kind = rng.choice(["chirp", "linear", "partial"])
    if kind == "chirp":
        c = random_symmetric(n, p, rng)
        return lower_chirp_symplectic(c, p), chirp_operator(c, p, ell, omega), kind, 0
    if kind == "linear":
        a = random_invertible(n, p, rng)
        return linear_symplectic(a, p), linear_operator(a, p, ell), kind, 0
    r = rng.randrange(1, n + 1)
    coords = rng.sample(range(n), r)
    return partial_weyl_symplectic(n, coords, p), partial_fourier_operator(n, coords, p, ell, omega), kind, r


def random_word(p: int, n: int, ell: int, omega: int, length: int, rng: Random) -> tuple[Matrix, Matrix, list[int]]:
    s_total = symplectic_identity(n)
    u_total = identity(p ** n)
    ranks: list[int] = []
    for _ in range(length):
        s, u, _kind, r = random_generator(p, n, ell, omega, rng)
        s_total = mat_mul(s, s_total, p)
        u_total = mat_mul(u, u_total, ell)
        ranks.append(r)
    return s_total, u_total, ranks


def direct_partial_fft_cost(p: int, n: int, r: int) -> dict[str, int]:
    """Naive exact p-point butterflies for r coordinates.

    Each coordinate has p^(n-1) fibers and each p x p dense transform uses
    p^2 scalar multiply-add terms. This is an explicit ledger, not a lower bound.
    """
    N = p ** n
    fibers_per_coordinate = N // p
    terms = r * fibers_per_coordinate * p * p
    writes = r * N
    return {
        "N": N,
        "coordinates": r,
        "fibers": r * fibers_per_coordinate,
        "dense_terms": terms,
        "writes": writes,
    }


@dataclass(frozen=True)
class RankBudget:
    target_rank: int
    stage_ranks: tuple[int, ...]

    @property
    def total(self) -> int:
        return sum(self.stage_ranks)

    @property
    def valid(self) -> bool:
        return self.target_rank <= self.total
