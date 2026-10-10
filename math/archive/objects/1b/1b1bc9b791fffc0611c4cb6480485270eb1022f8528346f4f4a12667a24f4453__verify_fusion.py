"""Exact finite-field support checks for sparse-surrogate graph fusion."""
from __future__ import annotations

import itertools
import json
from pathlib import Path
import random


def support(v):
    return sum(z != 0 for z in v)


def defect(v, lam, shift, p):
    n = len(v)
    return [(v[i] - lam*v[(i+shift) % n]) % p for i in range(n)]


def main():
    p, g, n = 257, 3, 8
    # 257 is prime by complete trial division; g has order 256.
    assert all(p % d for d in range(2, 17))
    assert pow(g, 256, p) == 1 and pow(g, 128, p) != 1
    assert p-1 > 2*(n-1)**2
    x = [pow(g, i*i, p) for i in range(n)]
    ratio_checks = 0
    for shift in range(1, n):
        ratios = [x[i] * pow(x[(i+shift) % n], -1, p) % p for i in range(n)]
        assert len(set(ratios)) == n
        ratio_checks += 1

    corrections = [[0]*n]
    for i in range(n):
        for value in (1, x[i], p-1):
            y = [0]*n
            y[i] = value
            corrections.append(y)
    rng = random.Random(20261009)
    for k in (2, 3):
        for _ in range(12):
            y = [0]*n
            for i in rng.sample(range(n), k):
                y[i] = rng.randrange(1, p)
            corrections.append(y)

    checks = 0
    for shift, lam, y in itertools.product(range(1, n), range(p), corrections):
        dx, dy = defect(x, lam, shift, p), defect(y, lam, shift, p)
        residual = [(a-b) % p for a, b in zip(x, y)]
        dr = defect(residual, lam, shift, p)
        k = support(y)
        assert support(dx) >= n-1
        assert support(dy) <= 2*k
        assert dr == [(a-b) % p for a, b in zip(dx, dy)]
        assert support(dr) >= support(dx)-2*k
        assert support(dr) >= n-1-2*k
        checks += 1

    y = [0]*n
    y[3] = pow(g, 9, p)*(1-pow(g, 4, p)) % p
    lam = pow(g, -12, p)
    tight_defect = defect([(a-b) % p for a,b in zip(x,y)], lam, 2, p)
    assert support(y) == 1 and support(tight_defect) == n-3

    # Exact l1 anti-contraction examples: positive equal-mass atoms.
    contraction_checks = 0
    for size in (8, 16, 32):
        for k in (1, 2, 4):
            for indices in ([0]*k, list(range(k)), [i % 2 for i in range(k)]):
                counts = [indices.count(i) for i in range(size)]
                # Multiply residual by k to avoid rational arithmetic.
                residual_scaled = [k-size*c for c in counts]
                used = support(counts)
                assert sum(abs(v) for v in residual_scaled) == 2*k*(size-used)
                assert support(residual_scaled) == size
                contraction_checks += 1

    report = {"status": "PASS", "field": p, "generator": g, "N": n,
              "witness": x, "all_shift_ratio_checks": ratio_checks,
              "all_lambda_sparse_correction_checks": checks,
              "tested_corrections": len(corrections),
              "tight_example": {"lambda": lam, "shift": 2,
                                "correction": y, "defect_support": support(tight_defect)},
              "exact_residual_noncontraction_checks": contraction_checks,
              "scope": "Exact tests support the stated restricted fusion lemmas, not a universal FFT lower bound."}
    Path(__file__).with_name("results.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k not in ("witness", "tight_example")}, sort_keys=True))


if __name__ == "__main__":
    main()
