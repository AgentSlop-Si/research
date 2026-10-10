"""Heuristic nonlinear search for a two-gauged-Green representation.

This is deliberately *not* used as proof. It provides a small positive control at
N=4 and finite-search negative evidence at N=5,6,8. Requires SciPy.
"""
from __future__ import annotations
import json
import numpy as np
from scipy.optimize import least_squares


def cycle_matrix(order):
    n = len(order)
    p = np.zeros((n, n), complex)
    for t, j in enumerate(order):
        p[order[(t + 1) % n], j] = 1
    return p


def dft(n):
    j = np.arange(n)
    return np.exp(-2j * np.pi * np.outer(j, j) / n) / np.sqrt(n)


def unpack(theta, n):
    half = len(theta) // 2
    z = theta[:half] + 1j * theta[half:]
    k = 0
    l1 = z[k:k+n]; k += n
    r1 = np.r_[1 + 0j, z[k:k+n-1]]; k += n - 1
    l2 = z[k:k+n]; k += n
    r2 = np.r_[1 + 0j, z[k:k+n-1]]; k += n - 1
    a, b = z[k], z[k+1]
    return l1, r1, l2, r2, a, b


def residual(theta, n, p, q, f):
    l1, r1, l2, r2, a, b = unpack(theta, n)
    try:
        g1 = np.linalg.inv(np.eye(n) - a * p)
        g2 = np.linalg.inv(np.eye(n) - b * q)
        s = l1[:, None] * g1 * r1[None, :] + l2[:, None] * g2 * r2[None, :]
        e = (s - f).ravel()
        if not np.all(np.isfinite(e)):
            raise FloatingPointError
        return np.r_[e.real, e.imag]
    except Exception:
        return np.full(2 * n * n, 1e6)


def run_case(n, order2, tries=4, max_nfev=1500, seed=0):
    p = cycle_matrix(list(range(n)))
    q = cycle_matrix(order2)
    f = dft(n)
    rng = np.random.default_rng(seed)
    m = 4 * n
    best = float("inf")
    for _ in range(tries):
        z = (rng.normal(size=m) + 1j * rng.normal(size=m)) * 0.2
        z[-2] = 0.3 * np.exp(1j * rng.uniform(0, 2*np.pi))
        z[-1] = 0.3 * np.exp(1j * rng.uniform(0, 2*np.pi))
        x0 = np.r_[z.real, z.imag]
        sol = least_squares(residual, x0, args=(n, p, q, f), max_nfev=max_nfev,
                            ftol=1e-12, xtol=1e-12, gtol=1e-12)
        best = min(best, float(np.linalg.norm(sol.fun)))
    return {"n": n, "order2": list(order2), "tries": tries, "best_residual_l2": best}


def main():
    cases = [
        (4, [0, 3, 2, 1], 1, 2500),
        (5, [0, 4, 3, 2, 1], 5, 1800),
        (6, [0, 5, 4, 3, 2, 1], 5, 1800),
        (8, [0, 7, 6, 5, 4, 3, 2, 1], 3, 1200),
    ]
    out = [run_case(n, o, t, e, seed=1700+n) for n, o, t, e in cases]
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
