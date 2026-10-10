from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import gcd
from typing import Iterable, Sequence


def vp(n: int, p: int, cap: int | None = None) -> int:
    n = int(n)
    if n == 0:
        if cap is None:
            raise ValueError("vp(0) requires cap")
        return cap
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


def coefficient_field(order: int) -> tuple[int, int]:
    """Return prime ell and an element of exact multiplicative order `order`."""
    if order < 2:
        raise ValueError("order >= 2 required")
    m = 1
    factors = list(factorint(order))
    while True:
        ell = m * order + 1
        if is_prime(ell):
            g = primitive_root(ell)
            zeta = pow(g, (ell - 1) // order, ell)
            if pow(zeta, order, ell) == 1 and all(pow(zeta, order // r, ell) != 1 for r in factors):
                return ell, zeta
        m += 1


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


def identity(n: int) -> list[list[int]]:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def matmul(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]], mod: int) -> list[list[int]]:
    if not a or not b or len(a[0]) != len(b):
        raise ValueError("dimension mismatch")
    n, m = len(a), len(b[0])
    out = [[0] * m for _ in range(n)]
    for i, row in enumerate(a):
        oi = out[i]
        for t, av in enumerate(row):
            av %= mod
            if not av:
                continue
            bt = b[t]
            for j, bv in enumerate(bt):
                if bv:
                    oi[j] = (oi[j] + av * bv) % mod
    return out


def transpose(a: Sequence[Sequence[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*a)]


def rank_mod(a: Sequence[Sequence[int]], mod: int) -> int:
    if not a:
        return 0
    x = [[v % mod for v in row] for row in a]
    rows, cols = len(x), len(x[0])
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if x[i][c]), None)
        if pivot is None:
            continue
        x[r], x[pivot] = x[pivot], x[r]
        inv = pow(x[r][c], -1, mod)
        x[r] = [v * inv % mod for v in x[r]]
        for i in range(rows):
            if i != r and x[i][c]:
                f = x[i][c]
                x[i] = [(u - f * v) % mod for u, v in zip(x[i], x[r])]
        r += 1
        if r == rows:
            break
    return r


def det_mod(a: Sequence[Sequence[int]], mod: int) -> int:
    if len(a) != len(a[0]):
        raise ValueError("square required")
    x = [[v % mod for v in row] for row in a]
    n = len(x)
    out = 1
    for c in range(n):
        pivot = next((i for i in range(c, n) if x[i][c]), None)
        if pivot is None:
            return 0
        if pivot != c:
            x[c], x[pivot] = x[pivot], x[c]
            out = -out
        pv = x[c][c]
        out = out * pv % mod
        inv = pow(pv, -1, mod)
        for i in range(c + 1, n):
            if x[i][c]:
                f = x[i][c] * inv % mod
                for j in range(c, n):
                    x[i][j] = (x[i][j] - f * x[c][j]) % mod
    return out % mod


def int_to_tuple(index: int, q: int, n: int) -> tuple[int, ...]:
    out = []
    for _ in range(n):
        out.append(index % q)
        index //= q
    return tuple(out)


def tuple_to_int(x: Sequence[int], q: int) -> int:
    out = 0
    mul = 1
    for v in x:
        out += (v % q) * mul
        mul *= q
    return out


def all_vectors(q: int, n: int) -> list[tuple[int, ...]]:
    return [int_to_tuple(i, q, n) for i in range(q ** n)]


def dot(x: Sequence[int], y: Sequence[int], q: int) -> int:
    return sum(a * b for a, b in zip(x, y)) % q


def dft_matrix_1d(q: int, mod: int, zeta: int, inverse: bool = False) -> list[list[int]]:
    root = pow(zeta, -1, mod) if inverse else zeta
    scale = pow(q, -1, mod) if inverse else 1
    return [[scale * pow(root, (i * j) % q, mod) % mod for j in range(q)] for i in range(q)]


def tensor_fourier_matrix(q: int, n: int, mod: int, zeta: int) -> list[list[int]]:
    pts = all_vectors(q, n)
    return [[pow(zeta, dot(x, y, q), mod) for y in pts] for x in pts]


def cyclic_fourier_witness(order: int) -> tuple[int, int, int]:
    """Return coefficient field, primitive root, and exact cross-ratio order."""
    mod, zeta = coefficient_field(order)
    # rows 0,1; columns 0,1 -> zeta
    return mod, zeta, multiplicative_order(zeta, mod)


def chirp_matrix_1d(q: int, b: int, mod: int, zeta: int) -> list[list[int]]:
    inv2 = pow(2, -1, q)
    return [[pow(zeta, (b * x * x * inv2) % q, mod) if x == y else 0 for y in range(q)] for x in range(q)]


def upper_shear_1d(q: int, b: int, mod: int, zeta: int) -> list[list[int]]:
    f = dft_matrix_1d(q, mod, zeta)
    fi = dft_matrix_1d(q, mod, zeta, inverse=True)
    return matmul(matmul(fi, chirp_matrix_1d(q, b % q, mod, zeta), mod), f, mod)


def predicted_upper_shear_1d(q: int, p: int, s: int, b: int, mod: int, zeta: int) -> list[list[int]]:
    b %= q
    v = vp(b, p, s)
    if v == s:
        return identity(q)
    g = p ** v
    q1 = q // g
    u = (b // g) % q1
    eta = pow(zeta, g, mod)
    inv2 = pow(2, -1, q1)
    gauss = sum(pow(eta, (u * z * z * inv2) % q1, mod) for z in range(q1)) % mod
    scale = gauss * pow(q1, -1, mod) % mod
    inv2u = pow((2 * u) % q1, -1, q1)
    out = [[0] * q for _ in range(q)]
    for x in range(q):
        for y in range(q):
            if (x - y) % g:
                continue
            X, Y = x // g, y // g
            e = (-(Y - X) * (Y - X) * inv2u) % q1
            out[x][y] = scale * pow(eta, e, mod) % mod
    return out


def kronecker(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]], mod: int) -> list[list[int]]:
    ar, ac, br, bc = len(a), len(a[0]), len(b), len(b[0])
    out = [[0] * (ac * bc) for _ in range(ar * br)]
    for i in range(ar):
        for j in range(ac):
            av = a[i][j] % mod
            if not av:
                continue
            for r in range(br):
                row = out[i * br + r]
                for c in range(bc):
                    row[j * bc + c] = av * b[r][c] % mod
    return out


def diagonal_upper_shear(q: int, p: int, s: int, diagonal: Sequence[int], mod: int, zeta: int) -> list[list[int]]:
    # int_to_tuple stores the first coordinate as the least-significant / fastest digit.
    # Hence the global matrix is M_(n-1) tensor ... tensor M_0.
    out = [[1]]
    for b in reversed(tuple(diagonal)):
        out = kronecker(out, predicted_upper_shear_1d(q, p, s, b, mod, zeta), mod)
    return out


def support_counts(a: Sequence[Sequence[int]]) -> tuple[list[int], list[int]]:
    rows = [sum(v != 0 for v in row) for row in a]
    cols = [sum(a[i][j] != 0 for i in range(len(a))) for j in range(len(a[0]))]
    return rows, cols


def cross_ratio(a: Sequence[Sequence[int]], r0: int, r1: int, c0: int, c1: int, mod: int) -> int:
    den = a[r0][c1] * a[r1][c0] % mod
    if den == 0:
        raise ZeroDivisionError("cross ratio needs nonzero entries")
    return a[r0][c0] * a[r1][c1] % mod * pow(den, -1, mod) % mod


def smith_valuation_profile(diagonal: Sequence[int], p: int, s: int) -> tuple[int, ...]:
    return tuple(sorted(vp(x, p, s) for x in diagonal))


def predicted_core_stats(p: int, s: int, valuations: Sequence[int]) -> dict[str, int | tuple[int, ...]]:
    vals = tuple(int(v) for v in valuations)
    if any(v < 0 or v > s for v in vals):
        raise ValueError("valuation out of range")
    q = p ** s
    block_count = p ** sum(vals)
    row_support = p ** sum(s - v for v in vals)
    nontrivial = [p ** (s - v) for v in vals if v < s]
    max_root_order = max(nontrivial, default=1)
    return {
        "q": q,
        "dimension": q ** len(vals),
        "block_count": block_count,
        "row_support": row_support,
        "max_root_order": max_root_order,
        "factor_lengths": tuple(nontrivial),
    }


def cross_ratio_orders(a: Sequence[Sequence[int]], mod: int, limit: int = 200) -> set[int]:
    n = len(a)
    out: set[int] = set()
    checked = 0
    for r0 in range(n):
        for r1 in range(r0 + 1, n):
            for c0 in range(n):
                for c1 in range(c0 + 1, n):
                    vals = (a[r0][c0], a[r0][c1], a[r1][c0], a[r1][c1])
                    if all(vals):
                        out.add(multiplicative_order(cross_ratio(a, r0, r1, c0, c1, mod), mod))
                        checked += 1
                        if checked >= limit:
                            return out
    return out


def matrix_mod_p_rank(a: Sequence[Sequence[int]], p: int) -> int:
    return rank_mod([[x % p for x in row] for row in a], p)


def block_matrix(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]], c: Sequence[Sequence[int]], d: Sequence[Sequence[int]]) -> list[list[int]]:
    n = len(a)
    return [list(a[i]) + list(b[i]) for i in range(n)] + [list(c[i]) + list(d[i]) for i in range(n)]


def split_blocks(smat: Sequence[Sequence[int]]) -> tuple[list[list[int]], list[list[int]], list[list[int]], list[list[int]]]:
    n2 = len(smat)
    if n2 % 2:
        raise ValueError("even size required")
    n = n2 // 2
    A = [list(row[:n]) for row in smat[:n]]
    B = [list(row[n:]) for row in smat[:n]]
    C = [list(row[:n]) for row in smat[n:]]
    D = [list(row[n:]) for row in smat[n:]]
    return A, B, C, D


def matadd(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]], mod: int) -> list[list[int]]:
    return [[(x + y) % mod for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def matsub(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]], mod: int) -> list[list[int]]:
    return [[(x - y) % mod for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def matrix_inverse_mod(a: Sequence[Sequence[int]], mod: int) -> list[list[int]]:
    n = len(a)
    x = [[v % mod for v in row] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        pivot = next((i for i in range(c, n) if gcd(x[i][c], mod) == 1), None)
        if pivot is None:
            raise ValueError("matrix not invertible over ring")
        x[c], x[pivot] = x[pivot], x[c]
        inv = pow(x[c][c], -1, mod)
        x[c] = [v * inv % mod for v in x[c]]
        for i in range(n):
            if i != c and x[i][c]:
                f = x[i][c]
                x[i] = [(u - f * v) % mod for u, v in zip(x[i], x[c])]
    return [row[n:] for row in x]


def lower_parabolic(A: Sequence[Sequence[int]], C: Sequence[Sequence[int]], q: int) -> list[list[int]]:
    """[[A,0],[C,A^-T]]. Caller is responsible for symplectic condition A^T C symmetric."""
    n = len(A)
    AinvT = transpose(matrix_inverse_mod(A, q))
    z = [[0] * n for _ in range(n)]
    return block_matrix(A, z, C, AinvT)


def coordinate_swap(n: int, indices: Iterable[int], q: int) -> list[list[int]]:
    chosen = set(indices)
    A = [[0] * n for _ in range(n)]
    B = [[0] * n for _ in range(n)]
    C = [[0] * n for _ in range(n)]
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        if i in chosen:
            B[i][i] = -1 % q
            C[i][i] = 1
        else:
            A[i][i] = 1
            D[i][i] = 1
    return block_matrix(A, B, C, D)


def symplectic_multiply(s: Sequence[Sequence[int]], t: Sequence[Sequence[int]], q: int) -> list[list[int]]:
    return matmul(s, t, q)


def unit_rank(smat: Sequence[Sequence[int]], p: int) -> int:
    _, B, _, _ = split_blocks(smat)
    return matrix_mod_p_rank(B, p)


def full_weyl(n: int, q: int) -> list[list[int]]:
    return coordinate_swap(n, range(n), q)


def direct_sum(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]) -> list[list[int]]:
    ar, br = len(a), len(b)
    out = [[0] * (ar + br) for _ in range(ar + br)]
    for i in range(ar):
        out[i][:ar] = list(a[i])
    for i in range(br):
        out[ar + i][ar:] = list(b[i])
    return out


@dataclass(frozen=True)
class CoreCertificate:
    p: int
    s: int
    n: int
    valuations: tuple[int, ...]
    dimension: int
    block_count: int
    row_support: int
    max_root_order: int


def certificate_from_valuations(p: int, s: int, valuations: Sequence[int]) -> CoreCertificate:
    stats = predicted_core_stats(p, s, valuations)
    return CoreCertificate(
        p=p,
        s=s,
        n=len(tuple(valuations)),
        valuations=tuple(valuations),
        dimension=int(stats["dimension"]),
        block_count=int(stats["block_count"]),
        row_support=int(stats["row_support"]),
        max_root_order=int(stats["max_root_order"]),
    )


def quadratic_form(z: Sequence[int], E: Sequence[Sequence[int]], q: int) -> int:
    return sum(z[i] * E[i][j] * z[j] for i in range(len(z)) for j in range(len(z))) % q


def matvec(a: Sequence[Sequence[int]], x: Sequence[int], q: int) -> tuple[int, ...]:
    return tuple(sum(a[i][j] * x[j] for j in range(len(x))) % q for i in range(len(a)))


def direct_upper_shear_nd(q: int, E: Sequence[Sequence[int]], mod: int, zeta: int) -> list[list[int]]:
    n = len(E)
    if any(len(row) != n for row in E):
        raise ValueError("square E required")
    pts = all_vectors(q, n)
    inv2 = pow(2, -1, q)
    invQ = pow(q ** n, -1, mod)
    qforms = [quadratic_form(z, E, q) * inv2 % q for z in pts]
    out = [[0] * len(pts) for _ in pts]
    for xi, x in enumerate(pts):
        for yi, y in enumerate(pts):
            diff = tuple((y[j] - x[j]) % q for j in range(n))
            total = 0
            for z, qf in zip(pts, qforms):
                e = (qf + dot(diff, z, q)) % q
                total = (total + pow(zeta, e, mod)) % mod
            out[xi][yi] = invQ * total % mod
    return out


def image_set(a: Sequence[Sequence[int]], q: int) -> set[tuple[int, ...]]:
    n = len(a)
    return {matvec(a, x, q) for x in all_vectors(q, n)}


def congruence_transform(E: Sequence[Sequence[int]], A: Sequence[Sequence[int]], q: int) -> list[list[int]]:
    return matmul(matmul(transpose(A), E, q), A, q)


def sample_nonzero_cross_ratio_orders(a: Sequence[Sequence[int]], mod: int, max_checks: int = 2000) -> set[int]:
    n = len(a)
    out: set[int] = set()
    checks = 0
    for r0 in range(n):
        for r1 in range(r0 + 1, n):
            for c0 in range(n):
                for c1 in range(c0 + 1, n):
                    if a[r0][c0] and a[r0][c1] and a[r1][c0] and a[r1][c1]:
                        out.add(multiplicative_order(cross_ratio(a, r0, r1, c0, c1, mod), mod))
                        checks += 1
                        if checks >= max_checks:
                            return out
    return out


def exponent_of_product_group(p: int, exponents: Sequence[int]) -> int:
    return p ** max(exponents, default=0)


def group_order_from_exponents(p: int, exponents: Sequence[int]) -> int:
    return p ** sum(exponents)


def cyclic_equivalence_exponent_gate(p: int, exponents: Sequence[int]) -> bool:
    """Necessary cross-ratio condition for additive Fourier of a p-group to be cyclic Fourier."""
    return exponent_of_product_group(p, exponents) == group_order_from_exponents(p, exponents)


def zero_matrix(n: int, m: int | None = None) -> list[list[int]]:
    if m is None:
        m = n
    return [[0] * m for _ in range(n)]


def scalar_identity(n: int, scalar: int, mod: int) -> list[list[int]]:
    return [[scalar % mod if i == j else 0 for j in range(n)] for i in range(n)]


def lower_shear_symplectic(C: Sequence[Sequence[int]], q: int) -> list[list[int]]:
    n = len(C)
    I = identity(n)
    Z = zero_matrix(n)
    return block_matrix(I, Z, C, I)


def gl_symplectic(A: Sequence[Sequence[int]], q: int) -> list[list[int]]:
    n = len(A)
    AinvT = transpose(matrix_inverse_mod(A, q))
    Z = zero_matrix(n)
    return block_matrix(A, Z, Z, AinvT)


def is_symmetric(a: Sequence[Sequence[int]], q: int) -> bool:
    return all((a[i][j] - a[j][i]) % q == 0 for i in range(len(a)) for j in range(len(a)))


def is_unit_det(a: Sequence[Sequence[int]], q: int) -> bool:
    # determinant over integers modulo q; dimensions used in tests are small.
    n = len(a)
    if n == 1:
        det = a[0][0] % q
    elif n == 2:
        det = (a[0][0] * a[1][1] - a[0][1] * a[1][0]) % q
    elif n == 3:
        det = 0
        for j in range(3):
            minor = [[a[r][c] for c in range(3) if c != j] for r in range(1, 3)]
            det += (-1 if j % 2 else 1) * a[0][j] * (minor[0][0] * minor[1][1] - minor[0][1] * minor[1][0])
        det %= q
    else:
        try:
            matrix_inverse_mod(a, q)
            return True
        except ValueError:
            return False
    return gcd(det, q) == 1


def lower_shear_operator(q: int, C: Sequence[Sequence[int]], mod: int, zeta: int) -> list[list[int]]:
    n = len(C)
    if not is_symmetric(C, q):
        raise ValueError("C must be symmetric")
    pts = all_vectors(q, n)
    inv2 = pow(2, -1, q)
    phases = [pow(zeta, quadratic_form(x, C, q) * inv2 % q, mod) for x in pts]
    return [[phases[i] if i == j else 0 for j in range(len(pts))] for i in range(len(pts))]


def gl_operator(q: int, A: Sequence[Sequence[int]], mod: int) -> list[list[int]]:
    n = len(A)
    if not is_unit_det(A, q):
        raise ValueError("A must be invertible")
    pts = all_vectors(q, n)
    out = [[0] * len(pts) for _ in pts]
    for j, y in enumerate(pts):
        x = matvec(A, y, q)
        out[tuple_to_int(x, q)][j] = 1 % mod
    return out


def full_fourier_operator(q: int, n: int, mod: int, zeta: int) -> list[list[int]]:
    return tensor_fourier_matrix(q, n, mod, zeta)


def partial_fourier_operator(q: int, n: int, indices: Iterable[int], mod: int, zeta: int) -> list[list[int]]:
    chosen = set(indices)
    pts = all_vectors(q, n)
    out = [[0] * len(pts) for _ in pts]
    for xi, x in enumerate(pts):
        for yi, y in enumerate(pts):
            if any(x[j] != y[j] for j in range(n) if j not in chosen):
                continue
            e = sum(x[j] * y[j] for j in chosen) % q
            out[xi][yi] = pow(zeta, e, mod)
    return out


def matrices_projectively_equal(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]], mod: int) -> tuple[bool, int | None]:
    scalar = None
    for i in range(len(a)):
        for j in range(len(a[0])):
            x, y = a[i][j] % mod, b[i][j] % mod
            if x == 0 or y == 0:
                if x != y:
                    return False, None
                continue
            cand = x * pow(y, -1, mod) % mod
            if scalar is None:
                scalar = cand
            elif cand != scalar:
                return False, None
    return True, scalar if scalar is not None else 0


def dense_bruhat_factor(smat: Sequence[Sequence[int]], q: int) -> tuple[list[list[int]], list[list[int]], list[list[int]], list[list[int]]]:
    A, B, C, D = split_blocks(smat)
    if not is_unit_det(B, q):
        raise ValueError("B must be invertible")
    Binv = matrix_inverse_mod(B, q)
    E_right = matmul(Binv, A, q)
    E_left = matmul(D, Binv, q)
    if not is_symmetric(E_right, q) or not is_symmetric(E_left, q):
        raise AssertionError("symplectic identities should make shears symmetric")
    minusB = [[(-x) % q for x in row] for row in B]
    return E_left, minusB, E_right, B


def representation_from_dense_bruhat(smat: Sequence[Sequence[int]], q: int, mod: int, zeta: int) -> list[list[int]]:
    E_left, minusB, E_right, _ = dense_bruhat_factor(smat, q)
    n = len(E_left)
    return matmul(
        matmul(
            matmul(lower_shear_operator(q, E_left, mod, zeta), gl_operator(q, minusB, mod), mod),
            full_fourier_operator(q, n, mod, zeta),
            mod,
        ),
        lower_shear_operator(q, E_right, mod, zeta),
        mod,
    )


def kernel_vectors(a: Sequence[Sequence[int]], q: int) -> list[tuple[int, ...]]:
    n = len(a)
    zero = (0,) * n
    return [x for x in all_vectors(q, n) if matvec(a, x, q) == zero]


def heisenberg_support_constraint(B: Sequence[Sequence[int]], D: Sequence[Sequence[int]], q: int, x: Sequence[int], y: Sequence[int], v: Sequence[int]) -> bool:
    if matvec(B, v, q) != (0,) * len(v):
        raise ValueError("v must be in ker B")
    Dv = matvec(D, v, q)
    return dot(v, y, q) == dot(Dv, x, q)


def upper_shear_symplectic(B: Sequence[Sequence[int]], q: int) -> list[list[int]]:
    n = len(B)
    if not is_symmetric(B, q):
        raise ValueError("B must be symmetric")
    I = identity(n)
    Z = zero_matrix(n)
    return block_matrix(I, B, Z, I)


def upper_shear_operator_nd(q: int, B: Sequence[Sequence[int]], mod: int, zeta: int) -> list[list[int]]:
    return direct_upper_shear_nd(q, B, mod, zeta)
