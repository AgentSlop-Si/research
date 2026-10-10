#!/usr/bin/env python3
"""Fresh controls for the refinement review; imports no supplied audit/source code."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import numpy as np

SEED = 10392026
rng = np.random.default_rng(SEED)
ROOT = Path(__file__).resolve().parent

def dft(n):
    k = np.arange(n)
    return np.exp(-2j * np.pi * np.outer(k, k) / n) / np.sqrt(n)

def unitary(n):
    z = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    q, _ = np.linalg.qr(z)
    return q

def rank(a):
    if a.size == 0:
        return 0
    return int(np.count_nonzero(np.linalg.svd(a, compute_uv=False) > 1e-8))

def norm(a):
    if a.size == 0:
        return 0.0
    return float(np.linalg.norm(a, 2))

counts = {"positive_quantile_attainments": 0, "strictly_intermediate_attainments": 0,
          "complementary_rank_checks": 0, "zero_quantile_boundary_cases": 0,
          "parity_threshold_cases": 0, "parity_infimum_cases": 0,
          "exact_rational_integer_envelope_checks": 0, "empty_class_rank_checks": 0}
maxima = {"squared_attainment_residual": 0.0, "inverse_identity_residual": 0.0,
          "forbidden_support_residual": 0.0, "parity_spectrum_residual": 0.0}
records = []

# Independent construction from the proof; test both flat and nonflat unitaries.
for family in ("dft", "general_unitary"):
    for n in range(2, 13):
        u = dft(n) if family == "dft" else unitary(n)
        for _ in range(12):
            t = int(rng.integers(1, n + 1))
            m = int(rng.integers(1, n + 1))
            I = np.sort(rng.choice(n, t, replace=False))
            J = np.sort(rng.choice(n, m, replace=False))
            Ic = np.setdiff1d(np.arange(n), I)
            Jc = np.setdiff1d(np.arange(n), J)
            d = int(rng.integers(1, min(t, m) + 1))
            left, sv, _ = np.linalg.svd(u[np.ix_(J, I)], full_matrices=False)
            if sv[d-1] <= 1e-8:
                continue
            Q = np.zeros((n, d), dtype=complex)
            Q[J, :] = left[:, :d]
            up = np.zeros_like(u)
            up[:, Ic] = u[:, Ic]
            M = u - Q @ Q.conj().T @ up
            H = np.linalg.inv(M)
            E = np.zeros_like(H)
            E[np.ix_(I, Jc)] = H[np.ix_(I, Jc)]
            B = H - E
            err = norm(M - u)
            expected_squared = max(0.0, 1.0 - float(sv[d-1] ** 2))
            residual = abs(err * err - expected_squared)
            maxima["squared_attainment_residual"] = max(maxima["squared_attainment_residual"], residual)
            maxima["inverse_identity_residual"] = max(maxima["inverse_identity_residual"], norm(M @ H - np.eye(n)))
            maxima["forbidden_support_residual"] = max(maxima["forbidden_support_residual"], norm(B[np.ix_(I, Jc)]))
            assert residual < 1e-11
            assert rank(E) <= t-d
            assert rank(M[np.ix_(J, Ic)]) <= m-d
            assert rank(H[np.ix_(I, Jc)]) == rank(M[np.ix_(J, Ic)]) + t-m
            counts["positive_quantile_attainments"] += 1
            counts["complementary_rank_checks"] += 1
            if 1e-8 < expected_squared < 1-1e-8:
                counts["strictly_intermediate_attainments"] += 1
            # Make global defect rank larger without changing the local block.
            F = np.zeros_like(H)
            F[:, J] = rng.normal(size=(n, m)) + 1j * rng.normal(size=(n, m))
            E2, B2 = E+F, B-F
            assert norm(B2[np.ix_(I, Jc)]) < 1e-12
            assert rank(E2[np.ix_(I, Jc)]) == rank(E[np.ix_(I, Jc)])
            assert norm((B2+E2)-H) < 1e-10

# sigma_d = 0 boundary: no equality, explicit feasible scaled permutation.
P = np.array([[0., 1.], [1., 0.]])
for delta in (1.0, .2, .01, .0001):
    M = delta*P
    H = np.linalg.inv(M)
    assert H[0, 0] == 0
    assert abs(norm(M-np.eye(2))-(1+delta)) < 1e-12
    counts["zero_quantile_boundary_cases"] += 1

# Parity rank cutoff and strict-error infimum.
for n in (4, 8, 12, 16, 20, 24):
    q = n//4
    U = dft(n)
    even, odd = np.arange(0, n, 2), np.arange(1, n, 2)
    sv = np.linalg.svd(U[np.ix_(even, even)], compute_uv=False)
    expected = np.r_[np.ones(q), np.zeros(q)]
    maxima["parity_spectrum_residual"] = max(maxima["parity_spectrum_residual"], float(np.max(np.abs(sv-expected))))
    H = U.conj().T
    E = np.zeros_like(H)
    E[np.ix_(even, odd)] = H[np.ix_(even, odd)]
    B = H-E
    assert rank(E) == q and norm(B[np.ix_(even, odd)]) == 0
    assert norm(np.linalg.inv(H)-U) < 1e-11
    counts["parity_threshold_cases"] += 1
    for delta in (.2, .01, .0001):
        error = norm(delta*np.eye(n)-U)
        assert error > 1 and error <= 1+delta+1e-12
        records.append({"N": n, "delta": delta, "error": error})
        counts["parity_infimum_cases"] += 1

# Exact rational test, including r=0 and all alpha in a quarter-step grid.
for n in range(1, 31):
    for numerator in range(1, 4*n+1):
        alpha = Fraction(numerator, 4)
        envelope = max(Fraction(t)-Fraction(t*t)/alpha for t in range(1, n+1))
        for r in range(n+3):
            expected = alpha <= (1 if r == 0 else 4*r)
            assert (r >= envelope) == expected
            counts["exact_rational_integer_envelope_checks"] += 1

# Impossibility d>|J| follows from inverse block rank >=t-|J|.
for n in range(2, 10):
    H = unitary(n)
    for t in range(1, n+1):
        for m in range(t):
            local_rank = rank(H[np.ix_(np.arange(t), np.arange(m, n))])
            assert local_rank >= t-m
            counts["empty_class_rank_checks"] += 1

result = {"status": "pass", "seed": SEED, "numpy_version": np.__version__,
          "independence": "No source or earlier audit control script was run or imported.",
          "counts": counts, "maximum_residuals": maxima,
          "parity_infimum_records": records,
          "caveat": "Floating point controls supplement the independent proof; they are not a proof or exact rank certificate.",
          "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(ROOT / "INDEPENDENT_REFINEMENT_RESULTS.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
