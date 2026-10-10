#!/usr/bin/env python3
"""New independent checks; no uploaded project code is imported or executed.

Exact checks use SymPy. Floating-point checks use NumPy. The proof is in PROOF.md;
these finite checks are not the basis of the all-size theorem.
"""
import json
import math
from pathlib import Path
import numpy as np
import sympy as sp

RNG = np.random.default_rng(20261009)
RESULTS = {"seed": 20261009, "exact_fourier4": [], "numerical_perturbations": [],
           "product_checks": [], "scope_controls": {}}


def norm1(a):
    return float(np.linalg.norm(a, 1))


def kappa1(a):
    return norm1(a) * norm1(np.linalg.inv(a))


def rank_numeric(a, scale=1.0):
    singular_values = np.linalg.svd(a, compute_uv=False)
    tolerance = 2e-9 * max(scale, float(singular_values[0]) if len(singular_values) else 0.0)
    return int(np.sum(singular_values > tolerance))


def fourier(n):
    j = np.arange(n)
    return np.exp(-2j * np.pi * np.outer(j, j) / n) / math.sqrt(n)


def exact_checks():
    n = 4
    f = sp.Matrix(n, n, lambda i, j: sp.I ** (-i*j) / 2)
    assert f.conjugate().T * f == sp.eye(n)
    for r in range(n):
        for trial in range(3):
            if r:
                while True:
                    u = sp.Matrix(n, r, lambda i, j: int(RNG.integers(-3, 4)) + sp.I*int(RNG.integers(-2, 3)))
                    v = sp.Matrix(r, n, lambda i, j: int(RNG.integers(-3, 4)) + sp.I*int(RNG.integers(-2, 3)))
                    update = u*v / 97
                    if update.rank() == r and (f + update).det() != 0:
                        break
            else:
                update = sp.zeros(n)
            g = f + update
            gi = g.inv()
            inverse_difference = f.inv() - gi
            assert (inverse_difference - f.inv() * (g-f) * gi).applyfunc(sp.simplify) == sp.zeros(n)
            assert inverse_difference.rank() == r
            subset = list(range(r+1))
            witness_small = update[:, subset].nullspace()[0]
            x = sp.zeros(n, 1)
            for index, value in zip(subset, witness_small):
                x[index] = value
            assert x != sp.zeros(n, 1)
            assert (update*x).applyfunc(sp.simplify) == sp.zeros(n, 1)
            assert (g*x-f*x).applyfunc(sp.simplify) == sp.zeros(n, 1)
            # Norm scalar comparisons use evaluated exact entries; all rank,
            # inverse, and witness equalities above are symbolic exact checks.
            gn = np.array(g.evalf(35).tolist(), dtype=complex)
            gin = np.array(gi.evalf(35).tolist(), dtype=complex)
            lower = math.sqrt(n)/(r+1)
            assert norm1(gn) >= lower-1e-12
            assert norm1(gin) >= lower-1e-12
            assert norm1(gn)*norm1(gin) >= n/(r+1)**2-1e-12
            RESULTS["exact_fourier4"].append({"rank": r, "trial": trial,
                "symbolic_inverse_rank_and_witness": "PASS",
                "norm1": norm1(gn), "inverse_norm1": norm1(gin)})


def numerical_checks():
    for n in (2, 3, 4, 5, 8, 16, 32, 64):
        f = fourier(n)
        for r in sorted(set((0, 1, min(2, n-1), n//2, n-1))):
            for trial in range(3):
                if r:
                    u = (RNG.normal(size=(n,r)) + 1j*RNG.normal(size=(n,r))) / math.sqrt(n)
                    v = (RNG.normal(size=(r,n)) + 1j*RNG.normal(size=(r,n))) / math.sqrt(n)
                    update = (0.02, 0.3, 2.0)[trial] * (u @ v)
                else:
                    update = np.zeros((n,n), dtype=complex)
                g = f + update
                gi = np.linalg.inv(g)
                assert rank_numeric(update) <= r
                inverse_difference = f.conj().T - gi
                identity_rhs = f.conj().T @ update @ gi
                assert np.allclose(inverse_difference, identity_rhs, rtol=2e-8, atol=2e-8)
                assert rank_numeric(inverse_difference) <= r
                subset = RNG.permutation(n)[:r+1]
                _, _, vh = np.linalg.svd(update[:,subset], full_matrices=True)
                x = np.zeros(n, dtype=complex)
                x[subset] = vh[-1,:].conj()
                assert np.linalg.norm(update @ x) < 1e-8
                fx = f @ x
                assert np.linalg.norm(fx, np.inf) <= math.sqrt((r+1)/n)*np.linalg.norm(x)+1e-10
                assert np.linalg.norm(fx, 1) >= math.sqrt(n/(r+1))*np.linalg.norm(x)-1e-10
                norm_lower = math.sqrt(n)/(r+1)
                assert norm1(g) >= norm_lower-1e-10
                assert norm1(gi) >= norm_lower-1e-10
                assert norm1(g)*norm1(gi) >= n/(r+1)**2-1e-10
                RESULTS["numerical_perturbations"].append({"n": n, "rank_budget": r,
                    "trial": trial, "kappa1": norm1(g)*norm1(gi),
                    "condition_lower_bound": n/(r+1)**2})


def product_left(factors, n):
    result = np.eye(n, dtype=complex)
    for factor in factors:
        result = factor @ result
    return result


def product_checks():
    for n in (2, 4, 8, 16, 32):
        tmat = 3*np.eye(n) - np.eye(n, k=1) - np.eye(n, k=-1)
        for t in (0, 1, 2, 3):
            for b in sorted(set((0, 1, t, t+2, n+1))):
                tagged = []
                for index in range(t):
                    p = np.eye(n)[RNG.permutation(n)]
                    bmat = p @ tmat @ p.T
                    m = np.linalg.inv(bmat) + np.linalg.inv(tmat)/20
                    if index % 2:
                        m = np.linalg.inv(m)
                    assert kappa1(m) <= 7+1e-10
                    tagged.append((m, m))
                for _ in range(b):
                    u = RNG.normal(size=n) + 1j*RNG.normal(size=n)
                    h = np.eye(n) - 2*np.outer(u,u.conj()) / np.vdot(u,u)
                    assert rank_numeric(h-np.eye(n)) == 1
                    assert np.allclose(h @ h, np.eye(n), atol=1e-10)
                    tagged.append((h, np.eye(n)))
                for _ in range(3):
                    p = np.eye(n)[RNG.permutation(n)]
                    q = np.diag(np.exp(1j*RNG.uniform(-np.pi, np.pi, size=n))) @ p
                    assert abs(kappa1(q)-1) < 1e-12
                    tagged.append((q,q))
                scalar = (0.7+0.2j)*np.eye(n)
                tagged.append((scalar,scalar))
                RNG.shuffle(tagged)
                aa = [pair[0] for pair in tagged]
                cc = [pair[1] for pair in tagged]
                a = product_left(aa,n)
                g = product_left(cc,n)
                telescope = np.zeros((n,n), dtype=complex)
                for j in range(len(tagged)):
                    left = product_left(aa[j+1:],n)
                    right = product_left(cc[:j],n)
                    telescope += left @ (aa[j]-cc[j]) @ right
                assert np.allclose(a-g,telescope,atol=1e-9,rtol=1e-9)
                actual_rank = rank_numeric(a-g,scale=max(norm1(a),norm1(g)))
                assert actual_rank <= min(n,b)
                assert kappa1(g) <= 7**t+1e-7
                RESULTS["product_checks"].append({"n": n, "green_factors": t,
                    "rank_one_factors": b, "observed_difference_rank": actual_rank,
                    "retained_kappa1": kappa1(g), "retained_condition_upper_bound": 7**t})


def scope_checks():
    f = fourier(4)
    tiny = 1e-6*np.eye(4)
    assert rank_numeric(f-tiny) == 4
    assert norm1(tiny) < math.sqrt(4)/(4+1)
    assert kappa1(tiny) >= 4/(4+1)**2
    diagonal = np.diag([1,2,4,8])
    assert abs(kappa1(diagonal)-8) < 1e-12
    for b in range(100):
        assert (b+1)**2 <= 4**b <= 7**b
    RESULTS["scope_controls"] = {
        "full_rank_individual_norm_extension_is_false": True,
        "large_rank_condition_bound_remains_true": True,
        "arbitrary_diagonal_gain_condition": kappa1(diagonal),
        "integer_count_inequality_checked_through_B": 99,
    }


if __name__ == "__main__":
    exact_checks()
    numerical_checks()
    product_checks()
    scope_checks()
    RESULTS["summary"] = {"status": "PASS", "exact_fourier4_instances": len(RESULTS["exact_fourier4"]),
        "numerical_low_rank_instances": len(RESULTS["numerical_perturbations"]),
        "product_instances": len(RESULTS["product_checks"]),
        "uploaded_code_imported_or_executed": False}
    output = Path(__file__).with_name("results.json")
    output.write_text(json.dumps(RESULTS,indent=2)+"\n")
    print(json.dumps(RESULTS["summary"],indent=2))
