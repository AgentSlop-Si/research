"""Static sign-corrected v25 derivative.

For odd q=p^k, F[x,y]=zeta^(xy), C_b[x,x]=zeta^(b*x*x/2),
this module uses U(b)=F^-1 C_(-b) F. Original execution logs do not
certify this derivative; see README.md for verification boundaries.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import gcd


def vp(n: int, p: int, k: int | None = None) -> int:
    if n == 0:
        if k is None:
            raise ValueError("vp(0) requires cap k")
        return k
    n = abs(n)
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def factorint(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


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


def primitive_root(prime: int) -> int:
    if not is_prime(prime):
        raise ValueError("prime modulus required")
    phi = prime - 1
    factors = list(factorint(phi))
    for g in range(2, prime):
        if all(pow(g, phi // r, prime) != 1 for r in factors):
            return g
    raise RuntimeError("primitive root not found")


def coefficient_field(q: int) -> tuple[int, int]:
    m = 1
    while True:
        ell = m * q + 1
        if is_prime(ell):
            g = primitive_root(ell)
            zeta = pow(g, (ell - 1) // q, ell)
            if pow(zeta, q, ell) == 1 and all(pow(zeta, q // r, ell) != 1 for r in factorint(q)):
                return ell, zeta
        m += 1


def matmul(a: list[list[int]], b: list[list[int]], mod: int) -> list[list[int]]:
    n, mid, m = len(a), len(b), len(b[0])
    if len(a[0]) != mid:
        raise ValueError("dimension mismatch")
    out = [[0] * m for _ in range(n)]
    for i in range(n):
        oi = out[i]
        for t, av in enumerate(a[i]):
            if av:
                bt = b[t]
                for j in range(m):
                    oi[j] = (oi[j] + av * bt[j]) % mod
    return out


def identity(n: int) -> list[list[int]]:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def rank_mod(a: list[list[int]], mod: int) -> int:
    if not a:
        return 0
    x = [row[:] for row in a]
    rows, cols = len(x), len(x[0])
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if x[i][c] % mod), None)
        if pivot is None:
            continue
        x[r], x[pivot] = x[pivot], x[r]
        inv = pow(x[r][c], -1, mod)
        x[r] = [(v * inv) % mod for v in x[r]]
        for i in range(rows):
            if i != r and x[i][c] % mod:
                f = x[i][c] % mod
                x[i] = [(u - f * v) % mod for u, v in zip(x[i], x[r])]
        r += 1
        if r == rows:
            break
    return r


def dft_matrix(q: int, mod: int, zeta: int, inverse: bool = False) -> list[list[int]]:
    root = pow(zeta, -1, mod) if inverse else zeta
    scale = pow(q, -1, mod) if inverse else 1
    return [[scale * pow(root, (i * j) % q, mod) % mod for j in range(q)] for i in range(q)]


def chirp_matrix(q: int, b: int, mod: int, zeta: int) -> list[list[int]]:
    inv2 = pow(2, -1, q)
    return [[pow(zeta, (b * x * x * inv2) % q, mod) if x == y else 0 for y in range(q)] for x in range(q)]


def upper_shear_matrix(q: int, b: int, mod: int, zeta: int) -> list[list[int]]:
    f = dft_matrix(q, mod, zeta)
    fi = dft_matrix(q, mod, zeta, inverse=True)
    # W^-1 L(-b) W = U(b), with positive-exponent F and C.
    c = chirp_matrix(q, (-b) % q, mod, zeta)
    return matmul(matmul(fi, c, mod), f, mod)


def upper_shear_gauss_matrix(q: int, b: int, mod: int, zeta: int) -> list[list[int]]:
    invq = pow(q, -1, mod)
    inv2 = pow(2, -1, q)
    out = [[0] * q for _ in range(q)]
    for x in range(q):
        for y in range(q):
            t = y - x
            total = 0
            for z in range(q):
                e = (-b * z * z * inv2 + t * z) % q
                total = (total + pow(zeta, e, mod)) % mod
            out[x][y] = invq * total % mod
    return out


def predicted_upper_shear(q: int, p: int, k: int, b: int, mod: int, zeta: int) -> list[list[int]]:
    b %= q
    v = vp(b, p, k)
    if v == k:
        return identity(q)
    g = p ** v
    q1 = q // g
    u = (b // g) % q1
    if gcd(u, q1) != 1:
        raise ValueError("unit part expected")
    eta = pow(zeta, g, mod)
    inv2 = pow(2, -1, q1)
    gauss = sum(pow(eta, (-u * z * z * inv2) % q1, mod) for z in range(q1)) % mod
    scale = gauss * pow(q1, -1, mod) % mod
    inv2u = pow((2 * u) % q1, -1, q1)
    out = [[0] * q for _ in range(q)]
    for x in range(q):
        for y in range(q):
            if (x - y) % g:
                continue
            X = x // g
            Y = y // g
            e = ((Y - X) * (Y - X) * inv2u) % q1
            out[x][y] = scale * pow(eta, e, mod) % mod
    return out


def support_counts(a: list[list[int]]) -> tuple[list[int], list[int]]:
    rows = [sum(v != 0 for v in row) for row in a]
    cols = [sum(a[i][j] != 0 for i in range(len(a))) for j in range(len(a[0]))]
    return rows, cols


def cross_ratio(a: list[list[int]], r0: int, r1: int, c0: int, c1: int, mod: int) -> int:
    den = a[r0][c1] * a[r1][c0] % mod
    if den == 0:
        raise ZeroDivisionError("cross ratio needs nonzero entries")
    return a[r0][c0] * a[r1][c1] % mod * pow(den, -1, mod) % mod


def multiplicative_order(x: int, mod: int) -> int:
    if x % mod == 0:
        raise ValueError("nonzero required")
    order = mod - 1
    for r, e in factorint(order).items():
        for _ in range(e):
            if order % r == 0 and pow(x, order // r, mod) == 1:
                order //= r
            else:
                break
    return order


@dataclass(frozen=True)
class SL2:
    a: int
    b: int
    c: int
    d: int
    q: int

    def normalized(self) -> "SL2":
        return SL2(self.a % self.q, self.b % self.q, self.c % self.q, self.d % self.q, self.q)

    def det(self) -> int:
        return (self.a * self.d - self.b * self.c) % self.q

    def __matmul__(self, other: "SL2") -> "SL2":
        if self.q != other.q:
            raise ValueError("different rings")
        q = self.q
        return SL2(
            (self.a * other.a + self.b * other.c) % q,
            (self.a * other.b + self.b * other.d) % q,
            (self.c * other.a + self.d * other.c) % q,
            (self.c * other.b + self.d * other.d) % q,
            q,
        )

    def inverse(self) -> "SL2":
        if self.det() != 1:
            raise ValueError("not SL2")
        return SL2(self.d, -self.b, -self.c, self.a, self.q).normalized()


def enumerate_sl2(q: int) -> list[SL2]:
    out = []
    for a in range(q):
        for b in range(q):
            for c in range(q):
                for d in range(q):
                    if (a * d - b * c) % q == 1:
                        out.append(SL2(a, b, c, d, q))
    return out


def cell_valuation(s: SL2, p: int, k: int) -> int:
    return vp(s.b % s.q, p, k)


def valuation_class_counts_formula(p: int, k: int) -> dict[int, int]:
    q = p ** k
    phi_q = q - q // p
    out: dict[int, int] = {0: phi_q * q * q, k: phi_q * q}
    for v in range(1, k):
        number_b = p ** (k - v) - p ** (k - v - 1)
        out[v] = phi_q * q * number_b
    return out


def lower_parabolic(a: int, c_over_a: int, q: int) -> SL2:
    a %= q
    if gcd(a, q) != 1:
        raise ValueError("a must be a unit")
    return SL2(a, 0, (c_over_a * a) % q, pow(a, -1, q), q)


def upper_shear(b: int, q: int) -> SL2:
    return SL2(1, b % q, 0, 1, q)


def factor_nonunit_cell(s: SL2, p: int) -> tuple[SL2, SL2]:
    q = s.q
    if s.det() != 1 or s.b % p != 0:
        raise ValueError("requires SL2 and nonunit b")
    if gcd(s.a, q) != 1:
        raise AssertionError("a is automatically a unit")
    ainv = pow(s.a, -1, q)
    left = lower_parabolic(s.a, s.c * ainv, q)
    u = upper_shear(s.b * ainv, q)
    if left @ u != s.normalized():
        raise AssertionError("factorization failed")
    return left, u


def in_congruence_parabolic(s: SL2, p: int, t: int) -> bool:
    return s.b % (p ** t) == 0


def core_size_from_valuation(p: int, k: int, v: int) -> tuple[int, int]:
    if not 0 <= v <= k:
        raise ValueError("bad valuation")
    return p ** v, p ** (k - v)


def radix_p_dense_terms(p: int, k: int, v: int) -> int:
    q = p ** k
    return (k - v) * p * q
