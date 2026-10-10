#!/usr/bin/env python3
"""Fresh v13 audit checks. Uploaded modules are read as text, never imported/run.

Exact checks use integers/Fraction. NumPy is used only for separately labelled
floating-point spectral comparisons. No source test/prototype is executed.
"""
from __future__ import annotations

import ast
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source_evidence"


def factors(n):
    out = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def phi(n):
    r = n
    for p in factors(n):
        r -= r//p
    return r


def mu(n):
    f = factors(n)
    return 0 if max(f.values(), default=0) > 1 else (-1)**len(f)


def divisors(n):
    return [d for d in range(1, math.isqrt(n)+1) if n % d == 0] + [n//d for d in range(1, math.isqrt(n)+1) if n%d == 0 and d*d != n]


def ramanujan(n, t):
    return sum(d*mu(n//d) for d in divisors(math.gcd(n, t)))


def exact_bound_data(n, m):
    ph = phi(n)
    positive = Counter(math.gcd(n, d) for d in range(1, m))
    prefixes = {g: [0]*m for g in positive}
    for g in positive:
        for u in range(1, m):
            prefixes[g][u] = prefixes[g][u-1] + (math.gcd(n, u) == g)
    maxima = {g: max(prefixes[g][u] + prefixes[g][m-1-u] for u in range(m)) for g in positive}
    V = sum((F(2*c, phi(n//g)) for g, c in positive.items()), F(0))
    C = sum((F(maxima[g], phi(n//g)) for g in positive), F(0))
    for g, c in maxima.items():
        assert c <= (m-1)//g
        assert F(ph, phi(n//g)) <= g
        assert c <= 2*positive[g]
    assert C <= V <= F(m*(m-1), ph)
    assert C <= F((m-1)*len(positive), ph)
    return C, V, maxima


def exact_q_numerator(n, m):
    """Returns A with Q=A/(N phi(N)) from integer Ramanujan sums."""
    ds = [set(range(u-m+1, u+1)) - {0} for u in range(m)]
    table = [ramanujan(n, j) for j in range(n)]
    return np.array([[sum(table[(d*(j-i)) % n] for d in ds[i%m] & ds[j%m])
                      for j in range(n)] for i in range(n)], dtype=object)


def exact_ldl_positive(a):
    """No floating point: ordinary rational LDL for positive definite input."""
    a = [[F(v) for v in row] for row in a]
    n = len(a)
    for k in range(n):
        pivot = a[k][k]
        assert pivot > 0, (n, k, pivot)
        for i in range(k+1, n):
            for j in range(i, n):
                a[j][i] -= a[i][k]*a[j][k]/pivot
                a[i][j] = a[j][i]


def grid_constant_output(value_over_tau):
    """Independent exact bin-center calculation for identical input rows."""
    centers = []
    for shift in (F(0), F(7, 3), F(14, 3)):
        bin_id = (value_over_tau - shift) // 7
        centers.append(7*(F(bin_id)+F(1, 2))+shift)
    return sorted(centers)[1]


def main():
    start = time.time()
    result = {"uploaded_code_executed": False}
    pairs = least_count = strict = 0
    max_v_over_c = (F(0), None)
    for n in range(4, 3001):
        f = factors(n)
        for m in range(2, math.isqrt(n)+1):
            if n % m:
                continue
            C, V, _ = exact_bound_data(n, m)
            pairs += 1
            strict += C < V
            if V/C > max_v_over_c[0]:
                max_v_over_c = (V/C, [n, m])
            if m == min(f):
                assert C == F(m-1, phi(n)) and V == 2*C
                least_count += 1
    result["exact_divisor_bounds"] = {"all_admissible_pairs_through_n": 3000,
        "pairs": pairs, "strict_C_less_V": strict, "least_factor_cases": least_count,
        "largest_V_over_C": str(max_v_over_c[0]), "at": max_v_over_c[1]}

    ram_count = 0
    for n in range(2, 257):
        for t in range(n):
            z = n//math.gcd(n, t)
            assert F(ramanujan(n, t), phi(n)) == F(mu(z), phi(z))
            ram_count += 1
    result["exact_ramanujan_identity_cases"] = ram_count

    ldl = []
    for m in range(2, 50):
        w = [[F(m-1-abs(i-j)) - (F(1, 2) if i == j else 0) for j in range(m)] for i in range(m)]
        exact_ldl_positive(w)
        ldl.append(m)
    result["exact_W_minus_half_identity_LDL_sizes"] = ldl

    cases = [(4,2),(6,2),(8,2),(9,3),(10,2),(12,2),(15,3),(18,2),
             (21,3),(25,5),(27,3),(35,5),(45,3),(49,7),(63,3),(77,7),(121,11)]
    spectral = []
    for n, p in cases:
        assert min(factors(n)) == p and n%p == 0
        k = n//p
        ph = phi(n)
        a = exact_q_numerator(n, p)
        assert np.array_equal(a, a.T)
        assert sum(a[i,i] for i in range(n)) == (p-1)*n*ph
        w = np.array([[p-1-abs(i-j) for j in range(p)] for i in range(p)], dtype=object)
        if k%p == 0:
            assert np.array_equal(a@a, (p-1)*n*a)
            expected = np.array([float(F(p-1,ph))]*(p*phi(k)) + [0.]*(n-p*phi(k)))
            exact_certificate = "A^2=(p-1)N A"
        else:
            j = p*(p-1)*np.eye(p, dtype=object)-w
            ak = np.eye(n, dtype=object)
            jk = np.eye(p, dtype=object)
            for power in range(1,5):
                ak = ak@a
                jk = jk@j
                assert np.trace(ak) == phi(k)*(k**power)*np.trace(jk)
            eigw = np.linalg.eigvalsh(np.array(w,dtype=float))
            vals = ((p-1)-eigw/p)/ph
            expected = np.array(list(vals)*phi(k)+[0.]*(n-p*phi(k)))
            exact_certificate = "integer spectral moments 1..4"
        actual = np.linalg.eigvalsh(np.array(a, dtype=float)/(n*ph))
        err = float(np.max(np.abs(np.sort(actual)-np.sort(expected))))
        assert err < 2e-12, (n,p,err)
        improved = F(p-1, ph) if k%p == 0 else F(2*p*(p-1)-1, 2*p*ph)
        if p == 2 and k%p:
            improved = F(1, 2*ph)
        assert actual[-1] <= float(improved)+2e-12
        spectral.append({"N":n,"p":p,"exact_check":exact_certificate,
                         "spectrum_max_error":err,"norm_numeric":float(actual[-1]),
                         "rational_bound":str(improved)})
    result["least_factor_spectrum"] = spectral

    # Exact source-implied counterexample. M=1 means the row itself is exact.
    assert grid_constant_output(F(0)) == F(7,6)
    assert grid_constant_output(F(1,3)) == F(7,6)
    # tau=sqrt(3); target real=1/sqrt(3)=tau/3; target imaginary=0.
    err_squared = 3*((F(7,6)-F(1,3))**2+F(7,6)**2)
    claimed_failure = F(6*2**51, 6**26)
    assert err_squared == F(37,6) > 4
    assert claimed_failure < F(1,10000)
    result["exact_offset_certificate_counterexample"] = {
        "N":3,"prime":2,"Q":4,"M":1,"input":"e_0", "rows":51,
        "g":3,"normalized_tolerance":2,"failure_probability_actual":1,
        "error_squared":str(err_squared),"claimed_failure":str(claimed_failure),
        "claimed_failure_float":float(claimed_failure)}

    # The two block rules, independently computed for an explicit disagreement.
    q = 256
    natural_block = max(2**j for j in range(9) if 2**j <= math.log(q) and 2**(2*j) <= q)
    base2_block = max(2**j for j in range(9) if 2**j <= math.log2(q) and 2**(2*j) <= q)
    assert (natural_block, base2_block) == (4,8)
    result["bessel_block_mismatch"] = {"N":129,"Q":q,"planner_M":natural_block,"executor_M":base2_block}

    # Static source inspection only. Parsing creates syntax trees, never code.
    static = {}
    for filename in ("prototype.py","composite_cycle_core.py","offset_class_core.py","v11_fused_reference.py","unit_step_core.py"):
        body = (SOURCE/filename).read_text()
        tree = ast.parse(body)
        function_calls = {}
        for node in tree.body:
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
                function_calls[node.name] = [{"call":ast.unparse(c.func),"line":c.lineno}
                                             for c in ast.walk(node) if isinstance(c,ast.Call)]
        static[filename] = {"sha256":hashlib.sha256(body.encode()).hexdigest(), "function_calls":function_calls}
    (ROOT/"STATIC_CALLS.json").write_text(json.dumps(static,indent=2)+"\n")
    calls = {c["call"] for c in static["prototype.py"]["function_calls"]["execute_candidate"]}
    assert "offset_core.streaming_offset_class_fft" in calls
    assert "bessel_core.streaming_fused_all_length_fft" in calls
    calls = {c["call"] for c in static["prototype.py"]["function_calls"]["bessel_candidate"]}
    assert "offset_core.choose_prime_power_block" in calls
    assert not any("addition_kernel_error_bound" in c for c in calls)
    result["static_ast_assertions"] = "PASS"
    result["runtime_seconds"] = time.time()-start
    result["status"] = "PASS: independent checks, with source certificate counterexample confirmed"
    (ROOT/"CHECK_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
