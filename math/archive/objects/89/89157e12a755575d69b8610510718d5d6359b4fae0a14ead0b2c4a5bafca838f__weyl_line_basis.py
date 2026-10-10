from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable

from finite_field import (
    field_for_length,
    flatten,
    inv,
    is_prime,
    mat_identity,
    mat_mul,
    matrix_inverse,
    matrix_rank,
    primitive_root,
    solve_linear_columns,
)


def field_for_length_from_k(n: int, start_k: int = 2) -> tuple[int, int]:
    """Find a prime p=k*n+1, k>=start_k, and a primitive n-th root."""
    if not is_prime(n) or n == 2:
        raise ValueError("n must be an odd prime")
    k = max(2, start_k)
    while True:
        p = k * n + 1
        if is_prime(p):
            g = primitive_root(p)
            omega = pow(g, k, p)
            if omega != 1 and pow(omega, n, p) == 1:
                return p, omega
        k += 1


def zero(n: int, m: int | None = None) -> list[list[int]]:
    return [[0] * (n if m is None else m) for _ in range(n)]


def add_scaled(a: list[list[int]], b: list[list[int]], scalar: int, p: int) -> None:
    for i in range(len(a)):
        for j in range(len(a[0])):
            a[i][j] = (a[i][j] + scalar * b[i][j]) % p


def matrix_power(a: list[list[int]], e: int, p: int) -> list[list[int]]:
    n = len(a)
    out = mat_identity(n)
    base = [row[:] for row in a]
    while e:
        if e & 1:
            out = mat_mul(out, base, p)
        base = mat_mul(base, base, p)
        e >>= 1
    return out


def shift_matrix(n: int) -> list[list[int]]:
    out = zero(n)
    for j in range(n):
        out[(j + 1) % n][j] = 1
    return out


def modulation_matrix(n: int, p: int, omega: int, exponent: int = 1) -> list[list[int]]:
    out = zero(n)
    for j in range(n):
        out[j][j] = pow(omega, exponent * j, p)
    return out


def weyl_matrix(n: int, p: int, omega: int, h: int, r: int) -> list[list[int]]:
    """W_(h,r)=X^h Z^r; W e_j=omega^(r*j)e_(j+h)."""
    out = zero(n)
    for j in range(n):
        out[(j + h) % n][j] = pow(omega, r * j, p)
    return out


def green_matrix(n: int, p: int, omega: int, alpha: int, h: int, r: int) -> list[list[int]]:
    w = weyl_matrix(n, p, omega, h, r)
    a = mat_identity(n)
    for i in range(n):
        for j in range(n):
            a[i][j] = (a[i][j] - alpha * w[i][j]) % p
    return matrix_inverse(a, p)


def character_packet_matrix(
    n: int, p: int, omega: int, alpha: int, h: int, s: int
) -> list[list[int]]:
    """H_(h,s)=(1/n) sum_r omega^(-r*s)(I-alpha X^h Z^r)^(-1).

    Uses the exact roots-of-unity filtered power formula, not dense inversions.
    """
    if not is_prime(n) or n == 2:
        raise ValueError("n must be an odd prime")
    h %= n
    if h == 0:
        raise ValueError("h must be nonzero")
    den = (1 - pow(alpha, n, p)) % p
    if den == 0:
        raise ValueError("singular alpha")
    scale = inv(den, p)
    out = zero(n)
    alpha_m = 1
    for m in range(n):
        q0 = (h * m * (m - 1) // 2) % n
        for j in range(n):
            if (m * j + q0 - s) % n == 0:
                i = (j + m * h) % n
                out[i][j] = (out[i][j] + scale * alpha_m) % p
        alpha_m = alpha_m * alpha % p
    return out


def packet_support_degrees(a: list[list[int]]) -> tuple[int, int, int]:
    row_max = max(sum(v != 0 for v in row) for row in a)
    n = len(a)
    col_max = max(sum(a[i][j] != 0 for i in range(n)) for j in range(n))
    total = sum(v != 0 for row in a for v in row)
    return row_max, col_max, total


def offdiag_block_matrix(
    n: int, p: int, omega: int, alpha: int, x: int
) -> list[list[int]]:
    """Fourier-diagonalized coefficient block B_x(delta,h)."""
    inv2_n = pow(2, -1, n)
    rows: list[list[int]] = []
    for delta in range(1, n):
        row = []
        for h in range(1, n):
            ratio = delta * pow(h, -1, n) % n
            exponent = (-x * delta * (delta - h) * inv2_n) % n
            row.append(pow(alpha, ratio, p) * pow(omega, exponent, p) % p)
        rows.append(row)
    return rows


def negation_permutation_sign(n: int) -> int:
    perm = [((-d) % n) - 1 for d in range(1, n)]
    inversions = sum(perm[i] > perm[j] for i in range(len(perm)) for j in range(i + 1, len(perm)))
    return -1 if inversions & 1 else 1


def leading_term_certificate(n: int, x: int) -> dict[str, int | list[int]]:
    """Formal unique top-degree determinant term for B_x.

    The entry alpha exponent is [delta/h] in {1,...,n-1}. The total is at
    most (n-1)^2, with equality uniquely at h=-delta for every row.
    """
    if not is_prime(n) or n == 2:
        raise ValueError("n must be an odd prime")
    sigma2 = sum((d * d) % n for d in range(1, n)) % n
    return {
        "n": n,
        "x": x % n,
        "top_degree": (n - 1) ** 2,
        "unique_top_columns": [(-d) % n for d in range(1, n)],
        "top_root_exponent_mod_n": (-x * sigma2) % n,
        "permutation_sign": negation_permutation_sign(n),
    }


def packet_basis_columns(
    n: int, p: int, omega: int, alpha: int
) -> tuple[list[list[int]], list[tuple[int, int]]]:
    cols: list[list[int]] = []
    labels: list[tuple[int, int]] = []
    for h in range(1, n):
        for s in range(n):
            cols.append(flatten(character_packet_matrix(n, p, omega, alpha, h, s)))
            labels.append((h, s))
    return cols, labels


def offdiag_restriction(mat: list[list[int]]) -> list[int]:
    n = len(mat)
    return [mat[i][j] for i in range(n) for j in range(n) if i != j]


def packet_offdiag_rank(n: int, p: int, omega: int, alpha: int) -> int:
    cols, _ = packet_basis_columns(n, p, omega, alpha)
    restricted = []
    for col in cols:
        mat = [col[i * n : (i + 1) * n] for i in range(n)]
        restricted.append(offdiag_restriction(mat))
    rows = len(restricted[0])
    return matrix_rank([[c[r] for c in restricted] for r in range(rows)], p)


def find_generic_field_alpha(n: int, max_fields: int = 40) -> tuple[int, int, int]:
    """Find an exact finite-field specialization where all B_x are invertible."""
    start_k = 2
    for _ in range(max_fields):
        p, omega = field_for_length_from_k(n, start_k)
        k = (p - 1) // n
        start_k = k + 1
        for alpha in range(2, p):
            if pow(alpha, n, p) == 1:
                continue
            if all(matrix_rank(offdiag_block_matrix(n, p, omega, alpha, x), p) == n - 1 for x in range(n)):
                return p, omega, alpha
    raise RuntimeError(f"no generic specialization found for n={n}")


def fourier_matrix(n: int, p: int, omega: int) -> list[list[int]]:
    return [[pow(omega, i * j, p) for j in range(n)] for i in range(n)]


def gauged_fourier_matrix(n: int, p: int, omega: int) -> list[list[int]]:
    """M=diag(omega^(-i^2)) F, so M[i,i]=1."""
    return [[pow(omega, (i * j - i * i) % n, p) for j in range(n)] for i in range(n)]


def common_weyl_generator(n: int, p: int, omega: int) -> list[list[int]]:
    return weyl_matrix(n, p, omega, 1, -1)


def chirp_coefficients(n: int, p: int, omega: int) -> list[int]:
    inv2_n = pow(2, -1, n)
    return [pow(omega, (-h * (h + 1) * inv2_n) % n, p) for h in range(n)]


def chirp_polynomial_matrix(n: int, p: int, omega: int) -> list[list[int]]:
    u = common_weyl_generator(n, p, omega)
    coeffs = chirp_coefficients(n, p, omega)
    out = zero(n)
    power = mat_identity(n)
    for coeff in coeffs:
        add_scaled(out, power, coeff, p)
        power = mat_mul(power, u, p)
    return out


def chirp_spectrum(n: int, p: int, omega: int) -> list[int]:
    coeffs = chirp_coefficients(n, p, omega)
    return [sum(coeffs[h] * pow(omega, k * h, p) for h in range(n)) % p for k in range(n)]


def solve_fourier_green_line(
    n: int, p: int, omega: int, alpha: int
) -> tuple[int, list[int], list[list[int]]]:
    """Solve M=lambda I+sum_(h!=0) A_h (I-alpha X^h Z^-h)^-1."""
    target = flatten(gauged_fourier_matrix(n, p, omega))
    mats = [green_matrix(n, p, omega, alpha, h, -h) for h in range(1, n)]
    ident = mat_identity(n)
    columns = [flatten(m) for m in mats] + [flatten(ident)]
    sol = solve_linear_columns(columns, target, p)
    if sol is None:
        raise ValueError("specialization does not admit the expected line representation")
    return sol[-1], sol[:-1], mats


def combine_green_line(
    n: int, p: int, scalar_i: int, coeffs: list[int], mats: list[list[list[int]]]
) -> list[list[int]]:
    out = mat_identity(n)
    for i in range(n):
        for j in range(n):
            out[i][j] = scalar_i if i == j else 0
    for a, m in zip(coeffs, mats):
        add_scaled(out, m, a, p)
    return out


def matrices_equal(a: list[list[int]], b: list[list[int]], p: int) -> bool:
    return all((x - y) % p == 0 for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def finite_field_case(n: int) -> dict:
    p, omega, alpha = find_generic_field_alpha(n)
    block_ranks = [matrix_rank(offdiag_block_matrix(n, p, omega, alpha, x), p) for x in range(n)]
    basis_rank = packet_offdiag_rank(n, p, omega, alpha)
    lam, line_coeffs, line_mats = solve_fourier_green_line(n, p, omega, alpha)
    target = gauged_fourier_matrix(n, p, omega)
    line_reconstruction = combine_green_line(n, p, lam, line_coeffs, line_mats)
    polynomial = chirp_polynomial_matrix(n, p, omega)
    packet_degrees = []
    for h, s in ((1, 0), (1, 1), (2 % n, 0), (2 % n, 3 % n)):
        packet_degrees.append(packet_support_degrees(character_packet_matrix(n, p, omega, alpha, h, s)))
    return {
        "n": n,
        "field_prime": p,
        "omega": omega,
        "alpha": alpha,
        "block_ranks": block_ranks,
        "packet_offdiag_rank": basis_rank,
        "expected_offdiag_dimension": n * (n - 1),
        "green_line_identity": matrices_equal(target, line_reconstruction, p),
        "chirp_polynomial_identity": matrices_equal(target, polynomial, p),
        "green_line_identity_scalar": lam,
        "green_line_nonzero_coefficients": sum(a != 0 for a in line_coeffs),
        "chirp_spectrum_nonzero": sum(v != 0 for v in chirp_spectrum(n, p, omega)),
        "packet_degree_samples": packet_degrees,
        "leading_terms": [leading_term_certificate(n, x) for x in range(n)],
    }
