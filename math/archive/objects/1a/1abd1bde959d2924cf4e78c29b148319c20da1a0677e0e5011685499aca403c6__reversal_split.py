#!/usr/bin/env python3
"""The minimising permutation is negation; its two halves are cosine/sine transforms.

For omega=exp(2*pi*i/N), the kernel basis
u_j=e_j+omega^(-j)e_(-j) transforms to
2*omega^(-j/2)*cos(2*pi*(k+1/2)j/N).
The complementary basis with a minus sign transforms to the matching sine
family.  Thus the floor(N/2) displacement is not missing information: the
nullspace and forcing halves are two independent dense trigonometric transforms.
"""
from __future__ import annotations
import math
import numpy as np


def split_bases(n: int) -> tuple[np.ndarray, np.ndarray]:
    if n < 2:
        raise ValueError
    w = np.exp(2j * np.pi / n)
    ker = []
    comp = []
    # Fixed zero coordinate is in the kernel.
    e0 = np.zeros(n, complex); e0[0] = 1; ker.append(e0)
    for j in range(1, (n + 1) // 2):
        k = (-j) % n
        u = np.zeros(n, complex); u[j] = 1; u[k] = w ** (-j)
        v = np.zeros(n, complex); v[j] = 1; v[k] = -w ** (-j)
        ker.append(u); comp.append(v)
    if n % 2 == 0:
        # Self-inverse N/2 coordinate is not in ker(D-P).
        e = np.zeros(n, complex); e[n // 2] = 1; comp.append(e)
    return np.stack(ker, axis=1), np.stack(comp, axis=1)


def fourier(n: int) -> np.ndarray:
    w = np.exp(2j * np.pi / n)
    k = np.arange(n)[:, None]
    j = np.arange(n)[None, :]
    return w ** (k * j)


def verify(n: int) -> dict:
    f = fourier(n)
    u, v = split_bases(n)
    fu, fv = f @ u, f @ v
    # Verify explicit cosine/sine formula for pair columns (skip e0 and even fixed point).
    max_cos = 0.0
    max_sin = 0.0
    w = np.exp(2j * np.pi / n)
    kk = np.arange(n)
    pair_count = (n - 1) // 2
    for idx, j in enumerate(range(1, pair_count + 1)):
        phase = w ** (-j / 2)
        c = 2 * phase * np.cos(2 * np.pi * (kk + .5) * j / n)
        s = 2j * phase * np.sin(2 * np.pi * (kk + .5) * j / n)
        max_cos = max(max_cos, float(np.max(np.abs(fu[:, idx + 1] - c))))
        max_sin = max(max_sin, float(np.max(np.abs(fv[:, idx] - s))))
    return {
        'n': n,
        'kernel_dimension': u.shape[1],
        'complement_dimension': v.shape[1],
        'kernel_transform_rank': int(np.linalg.matrix_rank(fu, tol=1e-9)),
        'complement_transform_rank': int(np.linalg.matrix_rank(fv, tol=1e-9)),
        'combined_rank': int(np.linalg.matrix_rank(np.concatenate([fu, fv], axis=1), tol=1e-9)),
        'max_cosine_formula_error': max_cos,
        'max_sine_formula_error': max_sin,
    }


if __name__ == '__main__':
    import json
    print(json.dumps([verify(n) for n in (7, 8, 9, 16, 25, 32, 64)], indent=2))
