from __future__ import annotations


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
    """Return a prime p=k*n+1 and a primitive n-th root omega in F_p."""
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
    a %= p
    if a == 0:
        raise ZeroDivisionError("zero has no inverse")
    return pow(a, p - 2, p)


def index_inverses_prime(n: int) -> list[int]:
    """All nonzero inverses modulo prime n in O(n) word operations."""
    if not is_prime(n):
        raise ValueError("n must be prime")
    out = [0] * n
    out[1] = 1
    for m in range(2, n):
        out[m] = (n - (n // m) * out[n % m] % n) % n
    return out


def mat_zero(n: int, m: int) -> list[list[int]]:
    return [[0] * m for _ in range(n)]


def mat_identity(n: int) -> list[list[int]]:
    out = mat_zero(n, n)
    for i in range(n):
        out[i][i] = 1
    return out


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
            raise ValueError("singular matrix")
        aug[rank], aug[pivot] = aug[pivot], aug[rank]
        z = inv(aug[rank][c], p)
        aug[rank] = [(v * z) % p for v in aug[rank]]
        for r in range(n):
            if r != rank and aug[r][c] % p:
                f = aug[r][c] % p
                aug[r] = [(x - f * y) % p for x, y in zip(aug[r], aug[rank])]
        rank += 1
    return [row[n:] for row in aug]


def flatten(a: list[list[int]]) -> list[int]:
    return [v for row in a for v in row]


def solve_linear_columns(columns: list[list[int]], target: list[int], p: int) -> list[int] | None:
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
