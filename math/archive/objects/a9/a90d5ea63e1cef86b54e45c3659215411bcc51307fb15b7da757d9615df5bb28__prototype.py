from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from time import perf_counter
from typing import Iterable


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    p = 3
    while p * p <= n:
        if n % p == 0:
            return False
        p += 2
    return True


def factor_distinct(n: int) -> list[int]:
    out: list[int] = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        out.append(n)
    return out


def primitive_root(p: int) -> int:
    if not is_prime(p):
        raise ValueError("p must be prime")
    fac = factor_distinct(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError("no primitive root found")


def field_for_length(n: int) -> tuple[int, int]:
    """Return prime p=k*n+1 and a primitive n-th root omega in F_p."""
    if not is_prime(n) or n == 2:
        raise ValueError("n must be an odd prime")
    k = 2
    while True:
        p = k * n + 1
        if is_prime(p):
            g = primitive_root(p)
            omega = pow(g, k, p)
            if pow(omega, n, p) == 1 and omega != 1:
                return p, omega
        k += 1


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def mat_zero(n: int, m: int) -> list[list[int]]:
    return [[0] * m for _ in range(n)]


def mat_identity(n: int) -> list[list[int]]:
    out = mat_zero(n, n)
    for i in range(n):
        out[i][i] = 1
    return out


def mat_add(a: list[list[int]], b: list[list[int]], p: int) -> list[list[int]]:
    return [[(x + y) % p for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def mat_mul(a: list[list[int]], b: list[list[int]], p: int) -> list[list[int]]:
    n = len(a)
    k = len(b)
    m = len(b[0])
    out = [[0] * m for _ in range(n)]
    for i in range(n):
        oi = out[i]
        for t in range(k):
            at = a[i][t] % p
            if at:
                bt = b[t]
                for j in range(m):
                    oi[j] = (oi[j] + at * bt[j]) % p
    return out


def mat_vec(a: list[list[int]], x: list[int], p: int) -> list[int]:
    return [sum(v * y for v, y in zip(row, x)) % p for row in a]


def matrix_rank(a: list[list[int]], p: int) -> int:
    if not a:
        return 0
    m = [row[:] for row in a]
    rows, cols = len(m), len(m[0])
    rank = 0
    for c in range(cols):
        pivot = next((r for r in range(rank, rows) if m[r][c] % p), None)
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        z = inv(m[rank][c], p)
        m[rank] = [(v * z) % p for v in m[rank]]
        for r in range(rows):
            if r != rank and m[r][c] % p:
                f = m[r][c] % p
                m[r] = [(x - f * y) % p for x, y in zip(m[r], m[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def matrix_inverse(a: list[list[int]], p: int) -> list[list[int]]:
    n = len(a)
    aug = [row[:] + eye for row, eye in zip(a, mat_identity(n))]
    rank = 0
    for c in range(n):
        pivot = next((r for r in range(rank, n) if aug[r][c] % p), None)
        if pivot is None:
            raise ValueError("singular")
        aug[rank], aug[pivot] = aug[pivot], aug[rank]
        z = inv(aug[rank][c], p)
        aug[rank] = [(v * z) % p for v in aug[rank]]
        for r in range(n):
            if r != rank and aug[r][c] % p:
                f = aug[r][c] % p
                aug[r] = [(x - f * y) % p for x, y in zip(aug[r], aug[rank])]
        rank += 1
    return [row[n:] for row in aug]


def solve_linear_columns(columns: list[list[int]], target: list[int], p: int) -> list[int] | None:
    """Solve sum_j coeff[j]*columns[j]=target over F_p, or return None."""
    rows = len(target)
    cols = len(columns)
    aug = [[columns[c][r] % p for c in range(cols)] + [target[r] % p] for r in range(rows)]
    pivot_cols: list[int] = []
    rr = 0
    for c in range(cols):
        pivot = next((r for r in range(rr, rows) if aug[r][c] % p), None)
        if pivot is None:
            continue
        aug[rr], aug[pivot] = aug[pivot], aug[rr]
        z = inv(aug[rr][c], p)
        aug[rr] = [(v * z) % p for v in aug[rr]]
        for r in range(rows):
            if r != rr and aug[r][c] % p:
                f = aug[r][c] % p
                aug[r] = [(x - f * y) % p for x, y in zip(aug[r], aug[rr])]
        pivot_cols.append(c)
        rr += 1
        if rr == rows:
            break
    for r in range(rr, rows):
        if all(aug[r][c] % p == 0 for c in range(cols)) and aug[r][-1] % p:
            return None
    sol = [0] * cols
    for r, c in enumerate(pivot_cols):
        sol[c] = aug[r][-1] % p
    return sol


def flatten(a: list[list[int]]) -> list[int]:
    return [v for row in a for v in row]


def shift_modulation_matrix(n: int, p: int, omega: int, r: int, h: int = 1) -> list[list[int]]:
    out = mat_zero(n, n)
    for j in range(n):
        out[(j + h) % n][j] = pow(omega, r * j, p)
    return out


def green_matrix(n: int, p: int, omega: int, alpha: int, r: int, h: int = 1) -> list[list[int]]:
    w = shift_modulation_matrix(n, p, omega, r, h)
    a = mat_identity(n)
    for i in range(n):
        for j in range(n):
            a[i][j] = (a[i][j] - alpha * w[i][j]) % p
    return matrix_inverse(a, p)


def green_apply_cycle(x: list[int], p: int, omega: int, alpha: int, r: int, h: int = 1) -> list[int]:
    """Apply (I-alpha X^h Z^r)^(-1) in O(n) field operations."""
    n = len(x)
    if gcd(h, n) != 1:
        raise ValueError("h must be a unit modulo n")
    order = [(t * h) % n for t in range(n)]
    # y[i_t] = x[i_t] + coeff_t * y[i_(t-1)]
    coeff = [alpha * pow(omega, r * ((order[t] - h) % n), p) % p for t in range(n)]
    A = 1
    B = 0
    for t in range(1, n):
        A = coeff[t] * A % p
        B = (x[order[t]] + coeff[t] * B) % p
    den = (1 - coeff[0] * A) % p
    if den == 0:
        raise ValueError("singular Green denominator")
    y0 = (x[order[0]] + coeff[0] * B) * inv(den, p) % p
    y = [0] * n
    y[order[0]] = y0
    for t in range(1, n):
        y[order[t]] = (x[order[t]] + coeff[t] * y[order[t - 1]]) % p
    return y



def index_inverses_prime(n: int) -> list[int]:
    """All inverses modulo prime n in O(n) word operations."""
    if not is_prime(n):
        raise ValueError("n must be prime")
    out = [0] * n
    out[1] = 1
    for m in range(2, n):
        out[m] = (n - (n // m) * out[n % m] % n) % n
    return out

def u_h(t: int, h: int, n: int) -> int:
    return (t * (t - h) * inv(2 * h, n)) % n


def character_packet_apply(
    x: list[int], p: int, omega: int, alpha: int, s: int, h: int = 1
) -> list[int]:
    """Apply H_s=(1/n) sum_r omega^(-rs)(I-alpha X^h Z^r)^(-1) in O(n)."""
    n = len(x)
    if gcd(h, n) != 1:
        raise ValueError("h must be a unit")
    den = (1 - pow(alpha, n, p)) % p
    if den == 0:
        raise ValueError("singular packet")
    scale = inv(den, p)
    out = [0] * n
    if s % n == 0:
        for j, value in enumerate(x):
            out[j] = (out[j] + value) % p
    inverses = index_inverses_prime(n)
    # For each nonzero orbit length m, q=m*j+h*C(m,2)=s has one j.
    alpha_m = alpha % p
    for m in range(1, n):
        comb = h * m * (m - 1) // 2
        j = ((s - comb) * inverses[m]) % n
        i = (j + m * h) % n
        out[i] = (out[i] + alpha_m * x[j]) % p
        alpha_m = alpha_m * alpha % p
    return [(scale * v) % p for v in out]


def literal_character_packet_apply(
    x: list[int], p: int, omega: int, alpha: int, s: int, h: int = 1
) -> list[int]:
    n = len(x)
    inv_n = inv(n % p, p)
    out = [0] * n
    for r in range(n):
        weight = inv_n * pow(omega, (-r * s) % n, p) % p
        y = green_apply_cycle(x, p, omega, alpha, r, h)
        for i in range(n):
            out[i] = (out[i] + weight * y[i]) % p
    return out


def weighted_packet_entry(
    i: int,
    j: int,
    weights: list[int],
    p: int,
    omega: int,
    alpha: int,
    h: int = 1,
) -> int:
    n = len(weights)
    inv_h_n = inv(h, n)
    m = ((i - j) * inv_h_n) % n
    q = (m * j + h * m * (m - 1) // 2) % n
    hq = 0
    for r, c in enumerate(weights):
        hq = (hq + c * pow(omega, r * q, p)) % p
    den = (1 - pow(alpha, n, p)) % p
    return pow(alpha, m, p) * hq % p * inv(den, p) % p


def packet_matrix(
    weights: list[int], p: int, omega: int, alpha: int, h: int = 1
) -> list[list[int]]:
    n = len(weights)
    return [
        [weighted_packet_entry(i, j, weights, p, omega, alpha, h) for j in range(n)]
        for i in range(n)
    ]


def packet_fiber_minor(
    weights: list[int], p: int, omega: int, alpha: int, h: int = 1
) -> tuple[int, tuple[int, int, int, int]]:
    n = len(weights)
    # Fixed deterministic generic choice. Search if a zero packet entry makes the test uninformative.
    for i in range(n):
        ip = (h - i) % n
        if ip == i:
            continue
        for j in range(n):
            jp = (h - j) % n
            if jp == j or i == j or (i + j - h) % n == 0:
                continue
            a = weighted_packet_entry(i, j, weights, p, omega, alpha, h)
            b = weighted_packet_entry(i, jp, weights, p, omega, alpha, h)
            c = weighted_packet_entry(ip, j, weights, p, omega, alpha, h)
            d = weighted_packet_entry(ip, jp, weights, p, omega, alpha, h)
            if any(v != 0 for v in (a, b, c, d)):
                return (a * d - b * c) % p, (i, ip, j, jp)
    raise RuntimeError("no usable fiber minor")


def affine_fourier_minor(
    n: int,
    p: int,
    omega: int,
    rows_cols: tuple[int, int, int, int],
    a: int = 1,
    b: int = 0,
    c: int = 1,
    d: int = 0,
) -> int:
    i, ip, j, jp = rows_cols
    def f(x: int, y: int) -> int:
        return pow(omega, ((a * x + b) * (c * y + d)) % n, p)
    return (f(i, j) * f(ip, jp) - f(i, jp) * f(ip, j)) % p


def cyclic_green_matrix(n: int, p: int, alpha: int) -> list[list[int]]:
    # A=I-alpha*C, where C shifts by one.
    A = mat_identity(n)
    for j in range(n):
        A[(j + 1) % n][j] = (A[(j + 1) % n][j] - alpha) % p
    return A


def undirected_distance_matrix_from_support(a: list[list[int]]) -> list[list[int]]:
    n = len(a)
    adj = [set() for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and (a[i][j] != 0 or a[j][i] != 0):
                adj[i].add(j)
                adj[j].add(i)
    inf = 10**9
    dist = [[inf] * n for _ in range(n)]
    for s in range(n):
        dist[s][s] = 0
        q = [s]
        for v in q:
            for w in adj[v]:
                if dist[s][w] == inf:
                    dist[s][w] = dist[s][v] + 1
                    q.append(w)
    return dist


def graph_diameter(a: list[list[int]]) -> int:
    d = undirected_distance_matrix_from_support(a)
    return max(max(row) for row in d)


def minimal_inverse_polynomial_degree(a: list[list[int]], p: int) -> int | None:
    """Small exact diagnostic: least d with A^-1 in span(I,A,...,A^d)."""
    n = len(a)
    target = flatten(matrix_inverse(a, p))
    power = mat_identity(n)
    cols: list[list[int]] = []
    for d in range(n * n):
        cols.append(flatten(power))
        if solve_linear_columns(cols, target, p) is not None:
            return d
        power = mat_mul(power, a, p)
    return None


def benchmark_character_packet(ns: Iterable[int] = (31, 61, 127), repeats: int = 3) -> list[dict]:
    rows: list[dict] = []
    for n in ns:
        p, omega = field_for_length(n)
        alpha = 2
        while pow(alpha, n, p) == 1:
            alpha += 1
        x = [(17 * j * j + 5 * j + 3) % p for j in range(n)]
        s = n // 3
        t0 = perf_counter()
        for _ in range(repeats):
            fast = character_packet_apply(x, p, omega, alpha, s)
        tf = (perf_counter() - t0) / repeats
        t0 = perf_counter()
        for _ in range(repeats):
            slow = literal_character_packet_apply(x, p, omega, alpha, s)
        ts = (perf_counter() - t0) / repeats
        if fast != slow:
            raise AssertionError("packet benchmark mismatch")
        rows.append({"N": n, "field": p, "fast_seconds": tf, "literal_seconds": ts, "speedup": ts / tf})
    return rows


if __name__ == "__main__":
    import json
    print(json.dumps(benchmark_character_packet(), indent=2))
