from __future__ import annotations

from math import gcd
from finite_field import (
    index_inverses_prime,
    inv,
    mat_identity,
    mat_vec,
    matrix_inverse,
)


def shift_modulation_matrix(n: int, p: int, omega: int, r: int, h: int = 1) -> list[list[int]]:
    """W_r=X^h Z^r, with W_r e_j=omega^(r*j)e_(j+h)."""
    out = [[0] * n for _ in range(n)]
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
        raise ValueError("h must be invertible modulo n")
    order = [(t * h) % n for t in range(n)]
    coeff = [alpha * pow(omega, r * ((order[t] - h) % n), p) % p for t in range(n)]
    a_prod = 1
    b_sum = 0
    for t in range(1, n):
        a_prod = coeff[t] * a_prod % p
        b_sum = (x[order[t]] + coeff[t] * b_sum) % p
    den = (1 - coeff[0] * a_prod) % p
    if den == 0:
        raise ValueError("singular Green denominator")
    y0 = (x[order[0]] + coeff[0] * b_sum) * inv(den, p) % p
    y = [0] * n
    y[order[0]] = y0
    for t in range(1, n):
        y[order[t]] = (x[order[t]] + coeff[t] * y[order[t - 1]]) % p
    return y


def u_h(t: int, h: int, n: int) -> int:
    return (t * (t - h) * inv(2 * h, n)) % n


def character_packet_apply(
    x: list[int], p: int, omega: int, alpha: int, s: int, h: int = 1
) -> list[int]:
    """Apply H_s=(1/n)sum_r omega^(-r*s)(I-alpha X^h Z^r)^(-1) in O(n)."""
    n = len(x)
    if gcd(h, n) != 1:
        raise ValueError("h must be invertible modulo n")
    den = (1 - pow(alpha, n, p)) % p
    if den == 0:
        raise ValueError("singular packet")
    scale = inv(den, p)
    out = [0] * n
    if s % n == 0:
        for j, value in enumerate(x):
            out[j] = (out[j] + value) % p
    inverses = index_inverses_prime(n)
    alpha_m = alpha % p
    for m in range(1, n):
        q0 = h * m * (m - 1) // 2
        j = ((s - q0) * inverses[m]) % n
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


def packet_hat(weights: list[int], q: int, p: int, omega: int) -> int:
    return sum(c * pow(omega, r * q, p) for r, c in enumerate(weights)) % p


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
    m = ((i - j) * inv(h, n)) % n
    q = (m * j + h * m * (m - 1) // 2) % n
    den = (1 - pow(alpha, n, p)) % p
    return pow(alpha, m, p) * packet_hat(weights, q, p, omega) % p * inv(den, p) % p


def weighted_packet_matrix(
    weights: list[int], p: int, omega: int, alpha: int, h: int = 1
) -> list[list[int]]:
    n = len(weights)
    return [
        [weighted_packet_entry(i, j, weights, p, omega, alpha, h) for j in range(n)]
        for i in range(n)
    ]


def literal_weighted_packet_matrix(
    weights: list[int], p: int, omega: int, alpha: int, h: int = 1
) -> list[list[int]]:
    n = len(weights)
    out = [[0] * n for _ in range(n)]
    for r, coeff in enumerate(weights):
        g = green_matrix(n, p, omega, alpha, r, h)
        for i in range(n):
            for j in range(n):
                out[i][j] = (out[i][j] + coeff * g[i][j]) % p
    return out


def packet_fiber_minor(
    weights: list[int], p: int, omega: int, alpha: int, h: int = 1
) -> tuple[int, tuple[int, int, int, int]]:
    """Return one generic 2x2 fiber determinant, which the theorem says is zero."""
    n = len(weights)
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
    row_slope: int = 1,
    row_shift: int = 0,
    col_slope: int = 1,
    col_shift: int = 0,
) -> int:
    i, ip, j, jp = rows_cols
    def f(x: int, y: int) -> int:
        return pow(
            omega,
            ((row_slope * x + row_shift) * (col_slope * y + col_shift)) % n,
            p,
        )
    return (f(i, j) * f(ip, jp) - f(i, jp) * f(ip, j)) % p


def noncommutator_witness(n: int, p: int, omega: int, r: int, q: int, h: int = 1) -> int:
    """Scalar lambda with W_r W_q=lambda W_q W_r."""
    return pow(omega, h * (r - q), p)


def apply_matrix(a: list[list[int]], x: list[int], p: int) -> list[int]:
    return mat_vec(a, x, p)
