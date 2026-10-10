from __future__ import annotations

import json
from itertools import product
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def factor(n: int) -> list[int]:
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def prime(n: int) -> bool:
    if n < 2:
        return False
    for d in range(2, int(n**0.5) + 1):
        if n % d == 0:
            return False
    return True


def coeff_field(order: int) -> tuple[int, int]:
    m = 1
    while True:
        ell = m * order + 1
        if prime(ell):
            for g in range(2, ell):
                if all(pow(g, (ell - 1) // r, ell) != 1 for r in factor(ell - 1)):
                    z = pow(g, (ell - 1) // order, ell)
                    if pow(z, order, ell) == 1 and all(pow(z, order // r, ell) != 1 for r in factor(order)):
                        return ell, z
        m += 1


def order(x: int, mod: int) -> int:
    d = 1
    y = x % mod
    while y != 1:
        y = y * x % mod
        d += 1
        if d > mod:
            raise RuntimeError("order loop")
    return d


def vectors(q: int, n: int):
    return list(product(range(q), repeat=n))


def dot(x, y, q):
    return sum(a * b for a, b in zip(x, y)) % q


def quad(z, E, q):
    return sum(z[i] * E[i][j] * z[j] for i in range(len(z)) for j in range(len(z))) % q


def kernel(q: int, E, mod: int, zeta: int):
    pts = vectors(q, len(E))
    inv2 = pow(2, -1, q)
    invQ = pow(q ** len(E), -1, mod)
    out = []
    for x in pts:
        row = []
        for y in pts:
            d = tuple((b - a) % q for a, b in zip(x, y))
            total = 0
            for z in pts:
                e = (quad(z, E, q) * inv2 + dot(d, z, q)) % q
                total = (total + pow(zeta, e, mod)) % mod
            row.append(total * invQ % mod)
        out.append(row)
    return pts, out


def image_size(E, q):
    pts = vectors(q, len(E))
    return len({tuple(sum(E[i][j] * x[j] for j in range(len(E))) % q for i in range(len(E))) for x in pts})


def cross_ratio(M, r0, r1, c0, c1, mod):
    return M[r0][c0] * M[r1][c1] % mod * pow(M[r0][c1] * M[r1][c0] % mod, -1, mod) % mod


def run() -> dict:
    q = 9
    mod, zeta = coeff_field(q)
    profiles = [
        ([[1, 0], [0, 1]], 81),
        ([[1, 0], [0, 3]], 27),
        ([[3, 0], [0, 3]], 9),
        ([[3, 0], [0, 0]], 3),
        ([[0, 0], [0, 0]], 1),
        ([[3, 3], [3, 3]], 3),
    ]
    support_records = []
    for E, expected in profiles:
        pts, K = kernel(q, E, mod, zeta)
        supports = {sum(v != 0 for v in row) for row in K}
        img = image_size(E, q)
        assert supports == {expected} == {img}
        support_records.append({"E": E, "support": expected})

    # Dense additive tensor character table: all four-entry ratios are q-th roots.
    pts = vectors(q, 2)
    F = [[pow(zeta, dot(x, y, q), mod) for y in pts] for x in pts]
    sampled_orders = []
    for r0, r1, c0, c1 in [(0, 1, 0, 1), (0, 10, 0, 9), (3, 14, 5, 28), (7, 50, 2, 70)]:
        o = order(cross_ratio(F, r0, r1, c0, c1, mod), mod)
        assert q % o == 0
        sampled_orders.append(o)

    Q = q * q
    modQ, zetaQ = coeff_field(Q)
    cyclic_order = order(zetaQ, modQ)
    assert cyclic_order == Q

    # Noncyclic p-groups of order p^6 have exponent strictly below p^6.
    exponents = [(6,), (5, 1), (4, 2), (3, 3), (2, 2, 2)]
    exponent_gate = []
    for parts in exponents:
        group_order = 3 ** sum(parts)
        exponent = 3 ** max(parts)
        exponent_gate.append({"parts": parts, "order": group_order, "exponent": exponent, "passes": group_order == exponent})
    assert [x["parts"] for x in exponent_gate if x["passes"]] == [(6,)]

    result = {
        "status": "pass",
        "q": q,
        "dimension": Q,
        "support_records": support_records,
        "tensor_cross_ratio_orders": sampled_orders,
        "cyclic_cross_ratio_order": cyclic_order,
        "abelian_exponent_gate": exponent_gate,
    }
    (ROOT / "independent_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
