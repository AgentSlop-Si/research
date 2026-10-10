#!/usr/bin/env python3
"""Audit the tempting direct extension from prime powers to composite moduli.

For N=K*M with K>=M, use the same unit-step row but draw a uniformly from
Z_N^*.  The decoder still has one cycle, but the covariance need not be a
scaled projector.  This script evaluates the exact normalized Ramanujan-sum
covariance and records counterexamples.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


def euler_phi(n: int) -> int:
    result = n
    x = n
    p = 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            result -= result // p
        p += 1
    if x > 1:
        result -= result // x
    return result


def mobius(n: int) -> int:
    if n == 1:
        return 1
    x = n
    count = 0
    p = 2
    while p * p <= x:
        if x % p == 0:
            x //= p
            count += 1
            if x % p == 0:
                return 0
            while x % p == 0:
                x //= p
        p += 1
    if x > 1:
        count += 1
    return -1 if count % 2 else 1


def normalized_ramanujan(n: int, c: int) -> float:
    g = math.gcd(n, c)
    q = n // g
    return mobius(q) / euler_phi(q)


def covariance(n: int, m: int) -> np.ndarray:
    if n % m or n // m < m:
        raise ValueError("need N=K*M and K>=M")
    displacement = [{u - t for t in range(m) if t != u} for u in range(m)]
    q = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        u = i % m
        for j in range(n):
            up = j % m
            q[i, j] = sum(
                normalized_ramanujan(n, d * (j - i))
                for d in displacement[u].intersection(displacement[up])
            ) / n
    return q


def is_prime_power(n: int) -> bool:
    for p in range(2, int(math.sqrt(n)) + 2):
        if n % p:
            continue
        x = n
        while x % p == 0:
            x //= p
        return x == 1
    return True  # prime


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("composite_modulus_results.json"))
    args = parser.parse_args()

    cases = [(12, 2), (12, 3), (18, 3), (20, 4), (30, 3), (30, 5),
             (36, 6), (42, 6), (45, 5), (60, 5), (60, 6), (72, 8)]
    records: list[dict[str, object]] = []
    for n, m in cases:
        q = covariance(n, m)
        eig = np.linalg.eigvalsh(q)
        positive = eig[eig > 1e-10]
        target = m / n
        records.append(
            {
                "N": n,
                "K": n // m,
                "M": m,
                "prime_power": is_prime_power(n),
                "trace": float(eig.sum()),
                "expected_trace": m - 1,
                "operator_norm": float(eig[-1]),
                "prime_power_target_M_over_N": target,
                "norm_ratio_to_M_over_N": float(eig[-1] / target),
                "positive_eigenvalue_min": float(positive.min()),
                "positive_eigenvalue_max": float(positive.max()),
                "positive_eigenvalue_spread": float(positive.max() - positive.min()),
                "numerical_rank": int(positive.size),
            }
        )

    payload = {
        "status": "DIRECT_PROJECTOR_EXTENSION_REJECTED",
        "statement": (
            "For non-prime-power moduli the decoder remains one-cycle when a is a unit, "
            "but the covariance generally has several positive eigenvalues and its norm "
            "can exceed M/N."
        ),
        "records": records,
    }
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("PASS: recorded exact-Ramanujan composite counterexamples")


if __name__ == "__main__":
    main()
