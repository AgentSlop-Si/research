"""Newly authored regression controls for the endpoint-rank draft.

This file does not import or execute any supplied research program.
Floating-point controls supplement, and do not replace, the manuscript proofs.
"""
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import json
import math
import numpy as np


ROOT = Path(__file__).resolve().parent
TOL = 2e-9
counts = {
    "exact_critical_algebra": 0,
    "cyclic_cut_recurrence": 0,
    "cyclic_cut_reflection": 0,
    "dyadic_minimax_upper": 0,
    "balanced_square_control": 0,
    "fourier_rectangle_moment": 0,
    "fourier_rectangle_rank": 0,
    "fourier_rectangle_gap": 0,
    "critical_rectangles": 0,
}
residuals = {"moment": 0.0, "rank_bound_violation": 0.0,
             "singular_gap_violation": 0.0}


def rank(A):
    if not A.size:
        return 0
    return int(np.count_nonzero(np.linalg.svd(A, compute_uv=False) > 1e-8))


def reverse_bits(a, m):
    return int(f"{a:0{m}b}"[::-1], 2) if m else 0


def cyclic_Q(N):
    m = N.bit_length() - 1
    b = np.array([reverse_bits(a, m) for a in range(N)])
    return np.exp(2j * np.pi * b[:, None] * b[None, :] / N)


def finite_abelian_table(moduli):
    elements = list(product(*(range(m) for m in moduli)))
    N = len(elements)
    U = np.array([
        [np.exp(2j*np.pi*sum(a*b/m for a, b, m in zip(chi, x, moduli)))
         for x in elements] for chi in elements
    ]) / np.sqrt(N)
    return elements, U


def check_rectangle(moduli, elements, U, rows, cols, critical=False):
    N = len(elements)
    r, h = len(rows), len(cols)
    complement = sorted(set(range(N)) - set(rows))
    col_elements = {elements[j] for j in cols}
    c = []
    for s in elements:
        c.append(sum(tuple((x+y) % m for x, y, m in zip(a, s, moduli))
                     in col_elements for a in col_elements))
    d = h - max(c[1:])
    f = np.array([
        sum(np.exp(2j*np.pi*sum(a*b/m for a, b, m in
                               zip(elements[i], s, moduli)))
            for i in complement) for s in elements
    ])
    V = U[np.ix_(rows, cols)]
    A0 = U[np.ix_(complement, cols)]
    A = A0.conj().T @ A0
    trace2 = float(np.trace(A @ A).real)
    moment = float(np.dot(c, np.abs(f)**2) / N**2)
    B = h*(N-r)/N-d*r*(N-r)/N**2
    K = h-B
    assert abs(trace2-moment) < TOL
    assert trace2 <= B+TOL
    residuals["moment"] = max(residuals["moment"], abs(trace2-moment))
    counts["fourier_rectangle_moment"] += 1
    singular = np.linalg.svd(V, compute_uv=False)
    actual_rank = int(np.count_nonzero(singular > 1e-8))
    ceil_bound = math.ceil(K-1e-10)
    assert actual_rank >= ceil_bound
    residuals["rank_bound_violation"] = max(
        residuals["rank_bound_violation"], float(ceil_bound-actual_rank))
    counts["fourier_rectangle_rank"] += 1
    for t in range(min(r, h)):
        if t < K-1e-10:
            bound = math.sqrt(max(0, 1-math.sqrt(max(0, B)/(h-t))))
            violation = bound-float(singular[t])
            assert violation < TOL
            residuals["singular_gap_violation"] = max(
                residuals["singular_gap_violation"], violation)
            counts["fourier_rectangle_gap"] += 1
    if critical:
        L = N//4
        B_L = L+.75+1/(4*L)+1/(16*L*L)
        delta = math.sqrt(1-math.sqrt(B_L/(L+1)))
        assert singular[L] >= delta-TOL
        assert actual_rank >= L+1
        counts["critical_rectangles"] += 1


for L in range(2, 4097):
    N, r, h = 4*L, 2*L-1, 2*L+1
    B = Fraction(h*(N-r), N)-Fraction(r*(N-r), N*N)
    expected = L+Fraction(3, 4)+Fraction(1, 4*L)+Fraction(1, 16*L*L)
    assert B == expected
    assert h-B > L and B < L+1
    counts["exact_critical_algebra"] += 1

Qs = {N: cyclic_Q(N) for N in (1, 2, 4, 8, 16, 32, 64)}
profiles = {}
for N, Q in Qs.items():
    profile = [rank(Q[:k, k:]) for k in range(N+1)]
    profiles[str(N)] = profile
    for k in range(N+1):
        assert profile[k] == profile[N-k]
        counts["cyclic_cut_reflection"] += 1
    if N >= 4:
        L = N//4
        for k in range(N//2+1):
            p = k//2
            assert profile[k] == (k+1)//2 + rank(Qs[L][:p, p:])
            counts["cyclic_cut_recurrence"] += 1
    if N >= 8:
        assert max(profile) == N//4+1
        assert profile[N//2-1] == N//4+1
        counts["dyadic_minimax_upper"] += 1

for L in range(1, 17):
    N = 4*L
    evens = np.arange(0, N, 2)
    block = np.exp(2j*np.pi*evens[:, None]*evens[None, :]/N)
    assert rank(block) == L
    counts["balanced_square_control"] += 1

# Every critical rectangle at order eight, in each abelian group of that order.
for moduli in ((8,), (4, 2), (2, 2, 2)):
    elements, U = finite_abelian_table(moduli)
    for rows in combinations(range(8), 3):
        for cols in combinations(range(8), 5):
            check_rectangle(moduli, elements, U, rows, cols, critical=True)

# Deterministic diverse rectangles, including full/empty complements and
# odd-prime, mixed, cyclic, and noncyclic group structures.
rng = np.random.default_rng(20261010)
for moduli in ((7,), (9,), (3, 3), (12,), (4, 3), (16,),
               (4, 4), (8, 2), (2, 2, 2, 2), (5, 5)):
    elements, U = finite_abelian_table(moduli)
    N = len(elements)
    for _ in range(120):
        r, h = map(int, rng.integers(1, N+1, size=2))
        rows = sorted(rng.choice(N, size=r, replace=False).tolist())
        cols = sorted(rng.choice(N, size=h, replace=False).tolist())
        check_rectangle(moduli, elements, U, rows, cols)
    if N == 16:
        for _ in range(40):
            rows = sorted(rng.choice(N, size=7, replace=False).tolist())
            cols = sorted(rng.choice(N, size=9, replace=False).tolist())
            check_rectangle(moduli, elements, U, rows, cols, critical=True)

report = {
    "status": "passed",
    "provenance": "newly authored control; no supplied research code imported or run",
    "interpretation": "exact rational algebra controls and floating-point regressions, not proof certificates",
    "numpy_version": np.__version__,
    "tolerance": TOL,
    "counts": counts,
    "largest_observed_residuals": residuals,
    "double_bit_reversal_cut_profiles": profiles,
}
(ROOT / "results.json").write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps(report, indent=2))
