from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable


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


def factor_int(n: int) -> list[int]:
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
        raise ValueError("p must be prime")
    factors = factor_int(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise RuntimeError("primitive root not found")


def field_for_length(n: int) -> tuple[int, int]:
    """Return prime p and primitive n-th root omega in F_p."""
    if not is_prime(n) or n == 2:
        raise ValueError("n must be an odd prime")
    for k in range(1, 10000):
        p = k * n + 1
        if is_prime(p):
            g = primitive_root(p)
            w = pow(g, (p - 1) // n, p)
            if pow(w, n, p) == 1 and all(pow(w, d, p) != 1 for d in range(1, n)):
                return p, w
    raise RuntimeError("no field found")


def zeros(n: int) -> list[list[int]]:
    return [[0] * n for _ in range(n)]


def eye(n: int) -> list[list[int]]:
    a = zeros(n)
    for i in range(n):
        a[i][i] = 1
    return a


def mat_add(a: list[list[int]], b: list[list[int]], p: int) -> list[list[int]]:
    return [[(x + y) % p for x, y in zip(rx, ry)] for rx, ry in zip(a, b)]


def mat_scale(c: int, a: list[list[int]], p: int) -> list[list[int]]:
    return [[c * x % p for x in row] for row in a]


def mat_mul(a: list[list[int]], b: list[list[int]], p: int) -> list[list[int]]:
    n = len(a)
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(a[i], bt[j])) % p for j in range(n)] for i in range(n)]


def mat_eq(a: list[list[int]], b: list[list[int]], p: int) -> bool:
    return all((x - y) % p == 0 for rx, ry in zip(a, b) for x, y in zip(rx, ry))


def matrix_rank(a: list[list[int]], p: int) -> int:
    m = [row[:] for row in a]
    nr = len(m)
    nc = len(m[0]) if nr else 0
    r = 0
    for c in range(nc):
        pivot = next((i for i in range(r, nr) if m[i][c] % p), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        inv = pow(m[r][c] % p, -1, p)
        m[r] = [(x * inv) % p for x in m[r]]
        for i in range(nr):
            if i != r and m[i][c] % p:
                q = m[i][c] % p
                m[i] = [(x - q * y) % p for x, y in zip(m[i], m[r])]
        r += 1
        if r == nr:
            break
    return r


def fourier_matrix(n: int, p: int, w: int) -> list[list[int]]:
    return [[pow(w, (i * j) % n, p) for j in range(n)] for i in range(n)]


def sym_weyl(n: int, p: int, w: int, a: int, b: int) -> list[list[int]]:
    """D_(a,b)=omega^(ab/2) X^a Z^b, X e_j=e_(j+a)."""
    a %= n
    b %= n
    inv2 = pow(2, -1, n)
    out = zeros(n)
    for j in range(n):
        i = (j + a) % n
        exp = (a * b * inv2 + b * j) % n
        out[i][j] = pow(w, exp, p)
    return out


def trace_product(a: list[list[int]], b: list[list[int]], p: int) -> int:
    n = len(a)
    return sum(a[i][j] * b[j][i] for i in range(n) for j in range(n)) % p


def gauss_constant(n: int, p: int, w: int) -> int:
    return pow(n, -1, p) * sum(pow(w, (j * j) % n, p) for j in range(n)) % p


def fourier_weyl_coefficient(n: int, p: int, w: int, a: int, b: int) -> int:
    inv4 = pow(4, -1, n)
    g = gauss_constant(n, p, w)
    exp = (-(a * a + b * b) * inv4) % n
    return g * pow(w, exp, p) % p


def fourier_weyl_coefficient_direct(n: int, p: int, w: int, a: int, b: int) -> int:
    dminus = sym_weyl(n, p, w, -a, -b)
    f = fourier_matrix(n, p, w)
    return pow(n, -1, p) * trace_product(dminus, f, p) % p


def qnorm(u: tuple[int, int], n: int) -> int:
    a, b = u
    return (a * a + b * b) % n


def symplectic_phase(u: tuple[int, int], v: tuple[int, int], n: int) -> int:
    a, b = u
    c, d = v
    return (b * c - a * d) % n


def dot(u: tuple[int, int], v: tuple[int, int], n: int) -> int:
    return (u[0] * v[0] + u[1] * v[1]) % n


def det2(u: tuple[int, int], v: tuple[int, int], n: int) -> int:
    return (u[0] * v[1] - u[1] * v[0]) % n


def compatibility_kappa(u: tuple[int, int], v: tuple[int, int], n: int) -> int:
    return (dot(u, v, n) + symplectic_phase(u, v, n)) % n


def canonical_partner(u: tuple[int, int], n: int, scale: int = 1) -> tuple[int, int]:
    a, b = u
    return (scale * (a - b) % n, scale * (a + b) % n)


def dephased_fourier_tensor(
    n: int, p: int, w: int, u: tuple[int, int], v: tuple[int, int]
) -> list[list[int]]:
    """Coefficient tensor after removing D_(mu) D_(nv) cocycle."""
    inv2 = pow(2, -1, n)
    sigma = symplectic_phase(u, v, n)
    out = zeros(n)
    for m in range(n):
        for k in range(n):
            a = (m * u[0] + k * v[0]) % n
            b = (m * u[1] + k * v[1]) % n
            coeff = fourier_weyl_coefficient(n, p, w, a, b)
            phase = pow(w, (-sigma * m * k * inv2) % n, p)
            out[m][k] = coeff * phase % p
    return out


def line_chirp_coefficients(n: int, p: int, w: int, u: tuple[int, int]) -> list[int]:
    inv4 = pow(4, -1, n)
    q = qnorm(u, n)
    return [pow(w, (-q * m * m * inv4) % n, p) for m in range(n)]


def line_operator(n: int, p: int, w: int, u: tuple[int, int]) -> list[list[int]]:
    coeffs = line_chirp_coefficients(n, p, w, u)
    out = zeros(n)
    for m, cm in enumerate(coeffs):
        term = sym_weyl(n, p, w, m * u[0], m * u[1])
        for i in range(n):
            for j in range(n):
                out[i][j] = (out[i][j] + cm * term[i][j]) % p
    return out


def predicted_line_operator(n: int, p: int, w: int, u: tuple[int, int]) -> list[list[int]]:
    a, b = (u[0] % n, u[1] % n)
    q = qnorm((a, b), n)
    inv4 = pow(4, -1, n)
    if a == 0:
        scalar = sum(pow(w, (-q * m * m * inv4) % n, p) for m in range(n)) % p
        out = zeros(n)
        for j in range(n):
            out[j][j] = scalar * pow(w, (j * j) % n, p) % p
        return out
    inva = pow(a, -1, n)
    inva2 = inva * inva % n
    inv2 = pow(2, -1, n)
    left_q = (-(a - b) * (a - b) * inv4 * inva2) % n
    right_q = (-(a + b) * (a + b) * inv4 * inva2) % n
    slope = q * inv2 * inva2 % n
    return [
        [pow(w, (left_q * i * i + slope * i * j + right_q * j * j) % n, p) for j in range(n)]
        for i in range(n)
    ]


def exact_two_line_factorization(
    n: int, p: int, w: int, u: tuple[int, int], scale: int = 1
) -> tuple[tuple[int, int], list[list[int]], list[list[int]]]:
    v = canonical_partner(u, n, scale)
    if det2(u, v, n) == 0:
        raise ValueError("directions are not independent; qnorm(u)=0")
    a = line_operator(n, p, w, u)
    b = line_operator(n, p, w, v)
    b = mat_scale(gauss_constant(n, p, w), b, p)
    return v, a, b


@dataclass(frozen=True)
class PairCertificate:
    n: int
    field: int
    u: tuple[int, int]
    v: tuple[int, int]
    kappa: int
    tensor_rank: int
    independent: bool
    factorable: bool


def certify_pair(n: int, u: tuple[int, int], v: tuple[int, int]) -> PairCertificate:
    p, w = field_for_length(n)
    tensor = dephased_fourier_tensor(n, p, w, u, v)
    kappa = compatibility_kappa(u, v, n)
    rank = matrix_rank(tensor, p)
    independent = det2(u, v, n) != 0
    return PairCertificate(n, p, u, v, kappa, rank, independent, independent and kappa == 0)


def all_nonzero_vectors(n: int) -> Iterable[tuple[int, int]]:
    for a, b in product(range(n), repeat=2):
        if a or b:
            yield (a, b)
