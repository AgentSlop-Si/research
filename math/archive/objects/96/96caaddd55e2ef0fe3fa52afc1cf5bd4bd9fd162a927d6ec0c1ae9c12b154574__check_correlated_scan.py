"""Independent exact checks for the correlated forcing scan obstruction.

This file was authored for this audit. It does not import uploaded code.
Finite-field first moments test the algebraic rank argument; Bessel
nonvanishing over the complex numbers is proved separately in the report.
"""
import json
import random
from pathlib import Path

P = 998244353
HALF = pow(2, -1, P)


def rank(a):
    a = [row[:] for row in a]
    n, m = len(a), len(a[0])
    r = 0
    for c in range(m):
        j = next((j for j in range(r, n) if a[j][c] % P), None)
        if j is None:
            continue
        a[r], a[j] = a[j], a[r]
        v = pow(a[r][c] % P, -1, P)
        a[r] = [(v * x) % P for x in a[r]]
        for j in range(r + 1, n):
            v = a[j][c] % P
            if v:
                a[j] = [(x - v * y) % P for x, y in zip(a[j], a[r])]
        r += 1
        if r == min(n, m):
            break
    return r


def det(a):
    a = [row[:] for row in a]
    n, d = len(a), 1
    for c in range(n):
        j = next((j for j in range(c, n) if a[j][c] % P), None)
        if j is None:
            return 0
        if j != c:
            a[c], a[j] = a[j], a[c]
            d = -d
        pivot = a[c][c] % P
        d = d * pivot % P
        inv = pow(pivot, -1, P)
        for j in range(c + 1, n):
            v = a[j][c] * inv % P
            if v:
                for k in range(c + 1, n):
                    a[j][k] = (a[j][k] - v * a[c][k]) % P
                a[j][c] = 0
    return d % P


def nearest_ratio(n, d):
    # Ties upward; selected target nodes in this test have no ties.
    return (2 * n + d) // (2 * d)


def one_case(q, m, a, beta, n, extension, rng):
    k = q // m
    omega = pow(3, (P - 1) // q, P)
    assert pow(omega, q, P) == 1 and pow(omega, q // 2, P) == P - 1
    rootk = pow(omega, m, P)
    b = [pow(omega, (m * (a * u + beta) + a * m * (m - 1) // 2) % q, P)
         for u in range(k)]
    boundary = [[0] * k for _ in range(k)]
    for u in range(k):
        boundary[u][u] = 1
        boundary[u][(u + m) % k] = (boundary[u][(u + m) % k] - b[u]) % P
    assert rank(boundary) == k
    cycle_checks = 0
    for u in range(m):
        product = 1
        for j in range(k // m):
            product = product * b[(u + j * m) % k] % P
        expected = pow(omega, (k * (a * u + beta) + a * k * (k - 1) // 2) % q, P)
        assert product == expected and pow(product, m, P) == P - 1
        cycle_checks += 1

    # Actual equal-block forcing: gamma_t times the periodic boundary map
    # acting on the a-permuted K-point Fourier channel.
    base = []
    for t in range(q):
        u = t % k
        gamma = pow(omega, (a * t * (t - 1) // 2 + beta * t) % q, P)
        base.append([
            gamma * (pow(rootk, ((a * u) % k) * j, P)
                     - b[u] * pow(rootk, ((a * (u + m)) % k) * j, P)) % P
            for j in range(k)
        ])
    assert rank(base) == k

    ai = pow(a, -1, q)
    selected = {}
    invn = pow(n, -1, P)
    for target in range(n):
        j = nearest_ratio(q * target, n)
        t = ai * j % q
        assert t not in selected
        selected[t] = (q * target - n * j) * invn % P
    rows = sorted(selected)
    values = [selected[t] for t in rows]
    assert len(set(values)) == n
    w = [None] * q
    for t in rows:
        w[t] = selected[t]
    for t in range(q):
        if w[t] is None:
            if extension == "zero":
                w[t] = 0
            elif extension == "match_next_selected":
                nxt = next(rows[j] for j in range(len(rows)) if rows[j] > t) if t < rows[-1] else rows[0]
                w[t] = w[nxt]
            else:
                w[t] = rng.randrange(P)

    comm = [[(w[t] - w[u]) * (HALF if u >= t else -HALF) % P
             for u in range(q)] for t in rows]
    principal = [[comm[i][u] for u in rows] for i in range(n)]
    expected_det = (1 if n % 2 == 0 else -1) * pow(4, -1, P) % P
    for i in range(n):
        expected_det = expected_det * (values[i] - values[(i + 1) % n]) % P
    assert expected_det != 0 and det(principal) == expected_det

    out = [[sum(c * base[u][j] for u, c in enumerate(row)) % P for j in range(k)]
           for row in comm]
    unweighted_rank = rank(out)
    first_moment = [[v * j % P for j, v in enumerate(row)] for row in out]
    first_moment_rank = rank(first_moment)
    assert unweighted_rank >= max(0, k - (q - n))
    assert first_moment_rank >= max(0, k - 1 - (q - n))

    return {"Q": q, "M": m, "K": k, "N": n, "a": a, "beta": beta,
            "extension": extension, "boundary_cycle_checks": cycle_checks,
            "unweighted_rank": unweighted_rank,
            "first_moment_rank": first_moment_rank,
            "unweighted_lower_bound": max(0, k - (q - n)),
            "first_moment_lower_bound": max(0, k - 1 - (q - n))}


def main():
    rng = random.Random(92025109)
    cases = []
    for q, m in [(8, 2), (16, 2), (16, 4), (32, 2), (32, 4), (64, 4), (64, 8), (128, 8)]:
        for a, beta in [(1, 0), (3, 2), (q - 1, q - 3)]:
            for n in sorted({q - 1, q - 3, max(q // 2 + 1, q - q // m + 1)}):
                for extension in ["zero", "match_next_selected", "random"]:
                    cases.append(one_case(q, m, a, beta, n, extension, rng))
    results = {
        "status": "PASS", "field": P,
        "case_count": len(cases),
        "boundary_cycle_checks": sum(c["boundary_cycle_checks"] for c in cases),
        "selected_commutator_determinants": len(cases),
        "correlated_rank_inequalities": 2 * len(cases),
        "limitations": ["Finite tests corroborate the proof, not an asymptotic speedup.",
                        "First-moment field weights test the same algebraic restriction; they are not Bessel values.",
                        "No uploaded code was executed, imported, or used as a dependency."],
        "cases": cases,
    }
    Path(__file__).with_name("CHECK_RESULTS.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({k: v for k, v in results.items() if k != "cases"}, indent=2))


if __name__ == "__main__":
    main()
