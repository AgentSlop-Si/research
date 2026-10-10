#!/usr/bin/env python3
"""Exact finite-field certificate for the v15 polyphase collapse.

Uses F_998244353, whose multiplicative group supports the tested Q and 2Q
orders.  No floating-point FFT is used here.
"""
from __future__ import annotations

import json
from pathlib import Path

P = 998244353
GEN = 3


def inv(x: int) -> int:
    return pow(x % P, P - 2, P)


def root(order: int) -> int:
    if (P - 1) % order:
        raise ValueError(f"order {order} does not divide P-1")
    return pow(GEN, (P - 1) // order, P)


def tri(t: int) -> int:
    return t * (t - 1) // 2


def phase(q: int, m: int, a: int, beta: int, b: int, t: int) -> int:
    omega = root(q)
    h = q & 1
    e = (a * tri(t) + (a * m * b + beta) * t) % q
    z = pow(omega, e, P)
    if h:
        eta = root(2 * q)
        z = z * pow(eta, t, P) % P
    return z


def dft(values: list[int], omega: int, inverse_sign: bool = False) -> list[int]:
    n = len(values)
    sign_root = inv(omega) if not inverse_sign else omega
    return [sum(values[j] * pow(sign_root, j * k, P) for j in range(n)) % P for k in range(n)]


def batched_summaries(x: list[int], q: int, m: int, a: int, beta0: int) -> list[list[int]]:
    k = q // m
    omega_m = pow(root(q), k, P)
    out = [[0] * k for _ in range(m)]
    for r in range(m):
        for b in range(k):
            out[r][b] = sum(
                phase(q, m, a, beta0, b, t) * x[b * m + t] * pow(omega_m, r * t, P)
                for t in range(m)
            ) % P
    return out


def joint_exact(x: list[int], q: int, m: int, a: int = 1, beta0: int = 2) -> list[int]:
    if q % m:
        raise ValueError
    k = q // m
    omega_q = root(q)
    omega_k = pow(omega_q, m, P)
    omega_m = pow(omega_q, k, P)
    d = batched_summaries(x, q, m, a, beta0)
    f = [dft(row, omega_k) for row in d]
    inv_m = inv(m)
    g = [[0] * k for _ in range(m)]
    for t in range(m):
        for p0 in range(k):
            g[t][p0] = sum(f[r][p0] * pow(inv(omega_m), t * r, P) for r in range(m)) % P
            g[t][p0] = g[t][p0] * inv_m % P
    h = [[0] * k for _ in range(m)]
    for t in range(m):
        c = phase(q, m, a, beta0, 0, t)
        ci = inv(c)
        for q0 in range(k):
            h[t][q0] = g[t][(q0 + a * t) % k] * ci % P
    out = [0] * q
    for q0 in range(k):
        lanes = [h[t][q0] * pow(inv(omega_q), q0 * t, P) % P for t in range(m)]
        z = dft(lanes, omega_m)
        for s in range(m):
            out[q0 + k * s] = z[s]
    return out


def direct(x: list[int], q: int) -> list[int]:
    return dft(x, root(q))


def run_certificate() -> dict:
    cases = [(56, 7), (119, 7), (136, 8), (238, 14)]
    records = []
    for q, m in cases:
        if (P - 1) % q or ((q & 1) and (P - 1) % (2 * q)):
            raise AssertionError("bad test order")
        basis_checked = q if q <= 119 else 24
        for j in range(basis_checked):
            x = [0] * q
            x[j] = 1
            assert joint_exact(x, q, m) == direct(x, q)
        # Deterministic dense vectors, independently checked.
        for seed in range(6):
            x = [((j + 1) * (seed + 3) + j * j * 17 + 5) % P for j in range(q)]
            assert joint_exact(x, q, m) == direct(x, q)
        records.append({
            "q": q, "m": m, "k": q // m,
            "basis_vectors_checked": basis_checked,
            "dense_vectors_checked": 6,
            "field": P,
            "status": "exact",
        })
    return {"records": records, "all_passed": True}


if __name__ == "__main__":
    out = run_certificate()
    Path(__file__).with_name("finite_field_results.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
