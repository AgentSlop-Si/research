from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from typing import Iterable, Sequence


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
    """Return prime ell and a primitive `order`th root modulo ell."""
    if order < 2:
        raise ValueError("order >= 2 required")
    factors = list(factorint(order))
    m = 1
    while True:
        ell = m * order + 1
        if is_prime(ell):
            g = primitive_root(ell)
            zeta = pow(g, (ell - 1) // order, ell)
            if pow(zeta, order, ell) == 1 and all(pow(zeta, order // r, ell) != 1 for r in factors):
                return ell, zeta
        m += 1


def identity(n: int) -> list[list[int]]:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def zeros(rows: int, cols: int) -> list[list[int]]:
    return [[0] * cols for _ in range(rows)]


def matmul(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]], mod: int) -> list[list[int]]:
    if not a or not b or len(a[0]) != len(b):
        raise ValueError("dimension mismatch")
    out = [[0] * len(b[0]) for _ in range(len(a))]
    for i, row in enumerate(a):
        oi = out[i]
        for k, av in enumerate(row):
            av %= mod
            if not av:
                continue
            for j, bv in enumerate(b[k]):
                if bv:
                    oi[j] = (oi[j] + av * bv) % mod
    return out


def matrix_equal(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]], mod: int) -> bool:
    return len(a) == len(b) and all(
        len(ra) == len(rb) and all((x - y) % mod == 0 for x, y in zip(ra, rb))
        for ra, rb in zip(a, b)
    )


def matrix_inverse(a: Sequence[Sequence[int]], mod: int) -> list[list[int]]:
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("square required")
    x = [[v % mod for v in row] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        pivot = next((i for i in range(c, n) if x[i][c]), None)
        if pivot is None:
            raise ValueError("singular")
        x[c], x[pivot] = x[pivot], x[c]
        inv = pow(x[c][c], -1, mod)
        x[c] = [v * inv % mod for v in x[c]]
        for i in range(n):
            if i != c and x[i][c]:
                f = x[i][c]
                x[i] = [(u - f * v) % mod for u, v in zip(x[i], x[c])]
    return [row[n:] for row in x]


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


def kronecker(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]], mod: int) -> list[list[int]]:
    ar, ac = len(a), len(a[0])
    br, bc = len(b), len(b[0])
    out = [[0] * (ac * bc) for _ in range(ar * br)]
    for i in range(ar):
        for j in range(ac):
            av = a[i][j] % mod
            if not av:
                continue
            for r in range(br):
                for c in range(bc):
                    out[i * br + r][j * bc + c] = av * b[r][c] % mod
    return out


def shift_matrix(n: int) -> list[list[int]]:
    out = [[0] * n for _ in range(n)]
    for j in range(n):
        out[(j + 1) % n][j] = 1
    return out


def modulation_matrix(n: int, mod: int, zeta: int) -> list[list[int]]:
    return [[pow(zeta, j, mod) if i == j else 0 for j in range(n)] for i in range(n)]


def fourier_matrix(n: int, mod: int, zeta: int, inverse: bool = False) -> list[list[int]]:
    root = pow(zeta, -1, mod) if inverse else zeta
    scale = pow(n, -1, mod) if inverse else 1
    return [[scale * pow(root, i * j % n, mod) % mod for j in range(n)] for i in range(n)]


def matrix_power(a: Sequence[Sequence[int]], e: int, mod: int) -> list[list[int]]:
    out = identity(len(a))
    base = [list(row) for row in a]
    while e:
        if e & 1:
            out = matmul(out, base, mod)
        base = matmul(base, base, mod)
        e >>= 1
    return out


def flatten(a: Sequence[Sequence[int]]) -> list[int]:
    return [v for row in a for v in row]


def weyl_monomials(n: int, mod: int, zeta: int) -> list[list[int]]:
    x = shift_matrix(n)
    z = modulation_matrix(n, mod, zeta)
    xp = identity(n)
    out: list[list[int]] = []
    for _a in range(n):
        zp = identity(n)
        for _b in range(n):
            out.append(flatten(matmul(xp, zp, mod)))
            zp = matmul(zp, z, mod)
        xp = matmul(xp, x, mod)
    return out


def weyl_algebra_rank(n: int, mod: int, zeta: int) -> int:
    return rank_mod(weyl_monomials(n, mod, zeta), mod)


def linear_equation_rank_commutant(x: Sequence[Sequence[int]], z: Sequence[Sequence[int]], mod: int) -> int:
    """Rank of A -> (AX-XA, AZ-ZA). Nullity is centralizer dimension."""
    d = len(x)
    equations: list[list[int]] = []
    for op in (x, z):
        for i in range(d):
            for j in range(d):
                row = [0] * (d * d)
                for k in range(d):
                    if op[k][j]:
                        row[i * d + k] = (row[i * d + k] + op[k][j]) % mod
                    if op[i][k]:
                        row[k * d + j] = (row[k * d + j] - op[i][k]) % mod
                equations.append(row)
    return rank_mod(equations, mod)


def linear_equation_rank_swap(x: Sequence[Sequence[int]], z: Sequence[Sequence[int]], mod: int) -> int:
    """Rank of J -> (JX-ZJ, JZ-X^{-1}J)."""
    d = len(x)
    xi = matrix_inverse(x, mod)
    equations: list[list[int]] = []
    pairs = ((x, z), (z, xi))
    for right, left in pairs:
        for i in range(d):
            for j in range(d):
                row = [0] * (d * d)
                for k in range(d):
                    if right[k][j]:
                        row[i * d + k] = (row[i * d + k] + right[k][j]) % mod
                    if left[i][k]:
                        row[k * d + j] = (row[k * d + j] - left[i][k]) % mod
                equations.append(row)
    return rank_mod(equations, mod)


def direct_sum_weyl(n: int, multiplicity: int, mod: int, zeta: int) -> tuple[list[list[int]], list[list[int]]]:
    return (
        kronecker(shift_matrix(n), identity(multiplicity), mod),
        kronecker(modulation_matrix(n, mod, zeta), identity(multiplicity), mod),
    )


def deterministic_invertible_matrix(m: int, mod: int, seed: int = 1) -> list[list[int]]:
    # Unit upper-triangular, deterministic and always invertible.
    out = identity(m)
    for i in range(m):
        for j in range(i + 1, m):
            out[i][j] = (seed + 3 * i + 5 * j) % mod
    return out


def swap_operator(n: int, multiplicity: int, mod: int, zeta: int, u: Sequence[Sequence[int]] | None = None) -> list[list[int]]:
    f = fourier_matrix(n, mod, zeta)
    if u is None:
        u = identity(multiplicity)
    return kronecker(f, u, mod)


def verify_swap_covariance(n: int, multiplicity: int) -> dict[str, int | bool]:
    mod, zeta = coefficient_field(n)
    x, z = direct_sum_weyl(n, multiplicity, mod, zeta)
    u = deterministic_invertible_matrix(multiplicity, mod, seed=n + multiplicity)
    j = swap_operator(n, multiplicity, mod, zeta, u)
    ji = matrix_inverse(j, mod)
    xi = matrix_inverse(x, mod)
    ok1 = matrix_equal(matmul(matmul(j, x, mod), ji, mod), z, mod)
    ok2 = matrix_equal(matmul(matmul(j, z, mod), ji, mod), xi, mod)
    d = n * multiplicity
    comm_rank = linear_equation_rank_commutant(x, z, mod)
    swap_rank = linear_equation_rank_swap(x, z, mod)
    return {
        "n": n,
        "multiplicity": multiplicity,
        "dimension": d,
        "field": mod,
        "covariance_ok": ok1 and ok2,
        "commutant_dimension": d * d - comm_rank,
        "swap_solution_dimension": d * d - swap_rank,
        "expected_dimension": multiplicity * multiplicity,
    }


def vector_add(a: Sequence[int], b: Sequence[int], q: int) -> tuple[int, ...]:
    return tuple((x + y) % q for x, y in zip(a, b))


def vector_sub(a: Sequence[int], b: Sequence[int], q: int) -> tuple[int, ...]:
    return tuple((x - y) % q for x, y in zip(a, b))


def vector_scale(c: int, a: Sequence[int], q: int) -> tuple[int, ...]:
    return tuple((c * x) % q for x in a)


def dot(a: Sequence[int], b: Sequence[int], q: int) -> int:
    return sum(x * y for x, y in zip(a, b)) % q


def all_vectors(q: int, n: int) -> list[tuple[int, ...]]:
    return [tuple(x) for x in product(range(q), repeat=n)]


@dataclass(frozen=True)
class EmbeddingCertificate:
    q: int
    dimension: int
    primitive_pairing: int
    direct_factor_ok: bool
    row_spectator_ok: bool
    col_spectator_ok: bool
    spectator_pairing_ok: bool


def classify_fourier_submatrix(rows: Sequence[Sequence[int]], cols: Sequence[Sequence[int]], q: int) -> EmbeddingCertificate:
    if len(rows) != q or len(cols) != q:
        raise ValueError("q rows and q columns required")
    n = len(rows[0])
    if any(len(v) != n for v in rows) or any(len(v) != n for v in cols):
        raise ValueError("dimension mismatch")
    x0 = tuple(rows[0])
    y0 = tuple(cols[0])
    u = vector_sub(rows[1], x0, q)
    v = vector_sub(cols[1], y0, q)
    primitive = dot(u, v, q)
    row_spectator_ok = True
    col_spectator_ok = True
    spectator_pairing_ok = True
    row_w: list[tuple[int, ...]] = []
    col_w: list[tuple[int, ...]] = []
    for i in range(q):
        wi = vector_sub(vector_sub(rows[i], x0, q), vector_scale(i, u, q), q)
        row_w.append(wi)
        row_spectator_ok &= dot(wi, v, q) == 0
    for j in range(q):
        wj = vector_sub(vector_sub(cols[j], y0, q), vector_scale(j, v, q), q)
        col_w.append(wj)
        col_spectator_ok &= dot(u, wj, q) == 0
    for wi in row_w:
        for wj in col_w:
            spectator_pairing_ok &= dot(wi, wj, q) == 0
    direct_factor_ok = primitive == 1
    if direct_factor_ok:
        # Every ambient vector splits uniquely as t*u + k with k orthogonal to v.
        for x in all_vectors(q, n):
            t = dot(x, v, q)
            k = vector_sub(x, vector_scale(t, u, q), q)
            if dot(k, v, q) != 0 or vector_add(vector_scale(t, u, q), k, q) != x:
                direct_factor_ok = False
                break
    return EmbeddingCertificate(
        q=q,
        dimension=n,
        primitive_pairing=primitive,
        direct_factor_ok=direct_factor_ok,
        row_spectator_ok=row_spectator_ok,
        col_spectator_ok=col_spectator_ok,
        spectator_pairing_ok=spectator_pairing_ok,
    )


def normalized_exponent_table(rows: Sequence[Sequence[int]], cols: Sequence[Sequence[int]], q: int) -> list[list[int]]:
    """Cross-ratio exponents of the additive character table, independent of gauges."""
    out = [[0] * q for _ in range(q)]
    x0, y0 = rows[0], cols[0]
    for i in range(q):
        dx = vector_sub(rows[i], x0, q)
        for j in range(q):
            dy = vector_sub(cols[j], y0, q)
            out[i][j] = dot(dx, dy, q)
    return out


def is_ordered_fourier_embedding(rows: Sequence[Sequence[int]], cols: Sequence[Sequence[int]], q: int) -> bool:
    exps = normalized_exponent_table(rows, cols, q)
    return all(exps[i][j] == (i * j) % q for i in range(q) for j in range(q))


def exhaustive_embedding_audit_q3_n2() -> dict[str, int]:
    q, n = 3, 2
    pts = all_vectors(q, n)
    triples = list(permutations(pts, q))
    count = 0
    classified = 0
    nontrivial_spectators = 0
    for rows in triples:
        for cols in triples:
            if not is_ordered_fourier_embedding(rows, cols, q):
                continue
            count += 1
            cert = classify_fourier_submatrix(rows, cols, q)
            if cert.direct_factor_ok and cert.row_spectator_ok and cert.col_spectator_ok and cert.spectator_pairing_ok:
                classified += 1
            x0, y0 = rows[0], cols[0]
            u = vector_sub(rows[1], x0, q)
            v = vector_sub(cols[1], y0, q)
            if any(vector_sub(vector_sub(rows[i], x0, q), vector_scale(i, u, q), q) != (0, 0) for i in range(q)) or any(
                vector_sub(vector_sub(cols[j], y0, q), vector_scale(j, v, q), q) != (0, 0) for j in range(q)
            ):
                nontrivial_spectators += 1
    return {
        "ordered_row_triples": len(triples),
        "ordered_col_triples": len(triples),
        "candidate_pairs": len(triples) ** 2,
        "fourier_embeddings": count,
        "classified_embeddings": classified,
        "nontrivial_spectator_embeddings": nontrivial_spectators,
    }


def nilpotent_lift_embedding(q: int, n: int = 2) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    # Works for q = p^2. Spectator coordinates are p-multiples, so all cross pairings vanish mod p^2.
    fac = factorint(q)
    if len(fac) != 1:
        raise ValueError("prime square required")
    p, k = next(iter(fac.items()))
    if k != 2 or n < 2:
        raise ValueError("q must be p^2 and n>=2")
    rows = []
    cols = []
    for i in range(q):
        rv = [0] * n
        cv = [0] * n
        rv[0] = i
        cv[0] = i
        rv[1] = (p * ((2 * i + 1) % p)) % q
        cv[1] = (p * ((3 * i + 2) % p)) % q
        rows.append(tuple(rv))
        cols.append(tuple(cv))
    return rows, cols


def operation_ledger(n: int, ambient_rank: int) -> dict[str, int | str]:
    q = n
    ambient_dimension = q ** ambient_rank
    return {
        "target_length": q,
        "ambient_dimension": ambient_dimension,
        "minimal_primitive_weyl_block_dimension": q,
        "embedding_input_moves": q,
        "embedding_output_moves": q,
        "restricted_core": f"one full F_{q}",
        "ambient_tensor_radix_dense_terms": ambient_rank * q * ambient_dimension,
        "direct_target_dense_terms": q * q,
    }
