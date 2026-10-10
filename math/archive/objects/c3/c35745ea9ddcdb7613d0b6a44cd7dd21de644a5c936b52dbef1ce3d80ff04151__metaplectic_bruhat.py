from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from random import Random
from typing import Iterable, Sequence

Matrix = list[list[int]]
SL2 = tuple[int, int, int, int]  # (a,b,c,d)


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
        raise ValueError("p must be prime")
    fac = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError("primitive root not found")


def field_for_length(n: int) -> tuple[int, int]:
    """Find a prime p and a primitive n-th root omega in F_p."""
    if not is_prime(n) or n == 2:
        raise ValueError("n must be an odd prime")
    for k in range(1, 20000):
        p = k * n + 1
        if is_prime(p):
            g = primitive_root(p)
            omega = pow(g, (p - 1) // n, p)
            if pow(omega, n, p) == 1 and all(pow(omega, j, p) != 1 for j in range(1, n)):
                return p, omega
    raise RuntimeError("coefficient field not found")


def zeros(n: int) -> Matrix:
    return [[0] * n for _ in range(n)]


def identity(n: int) -> Matrix:
    out = zeros(n)
    for i in range(n):
        out[i][i] = 1
    return out


def mat_mul(a: Matrix, b: Matrix, p: int) -> Matrix:
    n = len(a)
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(a[i], bt[j])) % p for j in range(n)] for i in range(n)]


def mat_scale(c: int, a: Matrix, p: int) -> Matrix:
    return [[c * x % p for x in row] for row in a]


def mat_vec(a: Matrix, x: Sequence[int], p: int) -> list[int]:
    return [sum(v * w for v, w in zip(row, x)) % p for row in a]


def projective_scalar(a: Matrix, b: Matrix, p: int) -> int | None:
    """Return lambda with a=lambda*b, or None."""
    lam: int | None = None
    for ra, rb in zip(a, b):
        for x, y in zip(ra, rb):
            x %= p
            y %= p
            if y:
                cur = x * pow(y, -1, p) % p
                if lam is None:
                    lam = cur
                elif cur != lam:
                    return None
            elif x:
                return None
    return lam


def projectively_equal(a: Matrix, b: Matrix, p: int) -> bool:
    return projective_scalar(a, b, p) is not None


def nonzero_pattern(a: Matrix, p: int) -> list[list[int]]:
    return [[1 if x % p else 0 for x in row] for row in a]


def is_monomial(a: Matrix, p: int) -> bool:
    n = len(a)
    return all(sum(x % p != 0 for x in row) == 1 for row in a) and all(
        sum(a[i][j] % p != 0 for i in range(n)) == 1 for j in range(n)
    )


def all_entries_nonzero(a: Matrix, p: int) -> bool:
    return all(x % p != 0 for row in a for x in row)


def sl2_mul(x: SL2, y: SL2, n: int) -> SL2:
    a, b, c, d = x
    e, f, g, h = y
    return (
        (a * e + b * g) % n,
        (a * f + b * h) % n,
        (c * e + d * g) % n,
        (c * f + d * h) % n,
    )


def sl2_det(x: SL2, n: int) -> int:
    a, b, c, d = x
    return (a * d - b * c) % n


def sl2_identity() -> SL2:
    return (1, 0, 0, 1)


def sl2_elements(n: int) -> list[SL2]:
    return [(a, b, c, d) for a, b, c, d in product(range(n), repeat=4) if (a * d - b * c) % n == 1]


def lower_shear(t: int, n: int) -> SL2:
    return (1, 0, t % n, 1)


def upper_shear(t: int, n: int) -> SL2:
    return (1, t % n, 0, 1)


def scale_symplectic(a: int, n: int) -> SL2:
    a %= n
    if a == 0:
        raise ValueError("scale must be nonzero")
    return (a, 0, 0, pow(a, -1, n))


def weyl_element(n: int) -> SL2:
    return (0, (-1) % n, 1, 0)


def is_easy_borel(s: SL2, n: int) -> bool:
    """Lower Borel: b=0. Its Weil operator is monomial in position basis."""
    return s[1] % n == 0


@dataclass(frozen=True)
class BruhatCertificate:
    kind: str  # borel or big
    parameters: tuple[int, ...]


def bruhat_certificate(s: SL2, n: int) -> BruhatCertificate:
    a, b, c, d = (x % n for x in s)
    if (a * d - b * c) % n != 1:
        raise ValueError("not in SL2")
    if b == 0:
        # s = L(c/a) D(a)
        return BruhatCertificate("borel", (c * pow(a, -1, n) % n, a))
    # s = L(d/b) D(-b) W L(a/b)
    ib = pow(b, -1, n)
    return BruhatCertificate("big", (d * ib % n, (-b) % n, a * ib % n))


def chirp_operator(n: int, p: int, omega: int, t: int) -> Matrix:
    inv2 = pow(2, -1, n)
    out = zeros(n)
    for x in range(n):
        out[x][x] = pow(omega, (t * x * x * inv2) % n, p)
    return out


def scale_operator(n: int, p: int, a: int) -> Matrix:
    """rho(D(a)): e_j -> e_(a j)."""
    out = zeros(n)
    for j in range(n):
        out[(a * j) % n][j] = 1
    return out


def fourier_matrix(n: int, p: int, omega: int) -> Matrix:
    return [[pow(omega, (x * y) % n, p) for y in range(n)] for x in range(n)]


def weil_operator(s: SL2, n: int, p: int, omega: int) -> Matrix:
    """A projectively normalized finite Weil operator.

    Lower shears are chirp multiplications, scales are permutations, and W is
    the unnormalized DFT. Multiplication is exact up to one nonzero scalar.
    """
    cert = bruhat_certificate(s, n)
    if cert.kind == "borel":
        t, a = cert.parameters
        return mat_mul(chirp_operator(n, p, omega, t), scale_operator(n, p, a), p)
    x, r, y = cert.parameters
    return mat_mul(
        mat_mul(
            mat_mul(chirp_operator(n, p, omega, x), scale_operator(n, p, r), p),
            fourier_matrix(n, p, omega),
            p,
        ),
        chirp_operator(n, p, omega, y),
        p,
    )


def direct_big_cell_kernel(s: SL2, n: int, p: int, omega: int) -> Matrix:
    """Independent kernel formula for b!=0, matching weil_operator exactly."""
    a, b, c, d = (x % n for x in s)
    if b == 0:
        raise ValueError("requires big Bruhat cell")
    inv2b = pow((2 * b) % n, -1, n)
    return [
        [pow(omega, ((d * x * x - 2 * x * y + a * y * y) * inv2b) % n, p) for y in range(n)]
        for x in range(n)
    ]


def direct_borel_kernel(s: SL2, n: int, p: int, omega: int) -> Matrix:
    a, b, c, d = (x % n for x in s)
    if b != 0:
        raise ValueError("requires lower Borel")
    out = zeros(n)
    inv2 = pow(2, -1, n)
    # rho(L(c/a)D(a)) sends e_j to a*j, with chirp evaluated at the output.
    t = c * pow(a, -1, n) % n
    for j in range(n):
        x = a * j % n
        out[x][j] = pow(omega, (t * x * x * inv2) % n, p)
    return out


def collapse_word(word: Sequence[SL2], n: int) -> SL2:
    out = sl2_identity()
    for s in word:
        out = sl2_mul(out, s, n)
    return out


def operator_product(word: Sequence[SL2], n: int, p: int, omega: int) -> Matrix:
    out = identity(n)
    for s in word:
        out = mat_mul(out, weil_operator(s, n, p, omega), p)
    return out


def complexity_class(s: SL2, n: int) -> str:
    return "linear_monomial" if is_easy_borel(s, n) else "fourier_equivalent"


def unique_lul_solution(n: int) -> tuple[int, int, int]:
    """Solve L(x) U(y) L(z)=W exhaustively and require uniqueness."""
    target = weyl_element(n)
    sols: list[tuple[int, int, int]] = []
    for x, y, z in product(range(n), repeat=3):
        got = sl2_mul(sl2_mul(lower_shear(x, n), upper_shear(y, n), n), lower_shear(z, n), n)
        if got == target:
            sols.append((x, y, z))
    if len(sols) != 1:
        raise AssertionError((n, sols))
    return sols[0]


def unique_ulu_solution(n: int) -> tuple[int, int, int]:
    target = weyl_element(n)
    sols: list[tuple[int, int, int]] = []
    for x, y, z in product(range(n), repeat=3):
        got = sl2_mul(sl2_mul(upper_shear(x, n), lower_shear(y, n), n), upper_shear(z, n), n)
        if got == target:
            sols.append((x, y, z))
    if len(sols) != 1:
        raise AssertionError((n, sols))
    return sols[0]


def random_sl2_word(n: int, length: int, rng: Random) -> list[SL2]:
    elems = sl2_elements(n)
    return [elems[rng.randrange(len(elems))] for _ in range(length)]


def count_bruhat_cells(n: int) -> tuple[int, int]:
    elems = sl2_elements(n)
    borel = sum(is_easy_borel(s, n) for s in elems)
    return borel, len(elems) - borel


def verify_projective_word(word: Sequence[SL2], n: int, p: int, omega: int) -> int:
    lhs = operator_product(word, n, p, omega)
    rhs = weil_operator(collapse_word(word, n), n, p, omega)
    scalar = projective_scalar(lhs, rhs, p)
    if scalar is None:
        raise AssertionError("projective word law failed")
    return scalar
