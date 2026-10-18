from __future__ import annotations

import collections
import json
import math
from pathlib import Path


def vp(n: int, p: int, cap: int) -> int:
    if n == 0:
        return cap
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def factors(n: int):
    d = 2
    out = []
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


def field(q: int):
    m = 1
    while True:
        ell = m * q + 1
        if prime(ell):
            for g in range(2, ell):
                if all(pow(g, (ell - 1) // r, ell) != 1 for r in factors(ell - 1)):
                    z = pow(g, (ell - 1) // q, ell)
                    if pow(z, q, ell) == 1 and all(pow(z, q // r, ell) != 1 for r in factors(q)):
                        return ell, z
        m += 1


def gauss_kernel(q: int, b: int, ell: int, zeta: int):
    invq = pow(q, -1, ell)
    inv2 = pow(2, -1, q)
    out = [[0] * q for _ in range(q)]
    for x in range(q):
        for y in range(q):
            out[x][y] = invq * sum(
                pow(zeta, (-b * z * z * inv2 + (y - x) * z) % q, ell)
                for z in range(q)
            ) % ell
    return out


def order(x: int, ell: int):
    for d in range(1, ell):
        if pow(x, d, ell) == 1:
            return d
    raise RuntimeError


def verify_support():
    rows = []
    for p, k in ((3, 2), (3, 3), (5, 2), (7, 2)):
        q = p**k
        ell, zeta = field(q)
        for v in range(k + 1):
            b = 0 if v == k else p**v
            a = gauss_kernel(q, b, ell, zeta)
            supports = {sum(x != 0 for x in row) for row in a}
            expected = p ** (k - v)
            assert supports == {expected}
            cross_order = 1
            if v < k:
                g = p**v
                cr = a[0][0] * a[g][g] * pow(a[0][g] * a[g][0] % ell, -1, ell) % ell
                cross_order = order(cr, ell)
                assert cross_order == expected
                # Order alone cannot detect b -> -b.
                assert cr == pow(zeta, (-g) % q, ell)
            rows.append({"p": p, "k": k, "valuation": v, "support": expected, "cross_order": cross_order})
    return rows


def verify_sl2_q9():
    q = 9
    group = []
    for a in range(q):
        for b in range(q):
            for c in range(q):
                for d in range(q):
                    if (a * d - b * c) % q == 1:
                        group.append((a, b, c, d))
    counts = collections.Counter(vp(b, 3, 2) for a, b, c, d in group)
    assert counts == {0: 486, 1: 108, 2: 54}
    h1 = [s for s in group if s[1] % 3 == 0]
    hset = set(h1)
    for a, b, c, d in h1:
        assert (d % q, (-b) % q, (-c) % q, a % q) in hset
    for x in h1:
        for y in h1:
            a, b, c, d = x
            e, f, g, h = y
            product = ((a*e+b*g)%q, (a*f+b*h)%q, (c*e+d*g)%q, (c*f+d*h)%q)
            assert product in hset
    return {"group_size": len(group), "valuation_counts": dict(counts), "easy_subgroup_size": len(h1)}


def main():
    result = {
        "support_certificates": verify_support(),
        "sl2_q9": verify_sl2_q9(),
        "status": "independent exact finite-field checks passed",
    }
    path = Path(__file__).with_name("independent_results.json")
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
