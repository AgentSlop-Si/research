#!/usr/bin/env python3
"""Independent read-only audit of integer JSON witnesses. No uploaded code import.

Run: python check_bitrev.py [input_directory] [output_directory]
Default inputs are ./inputs; output is ./checks. Python 3.10+ and NumPy suffice.
All matrix arithmetic is int64 with a checked dot-product overflow bound.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import platform
import random
import sys
import time

import numpy as np


TERMS = ("d", "L", "V", "U", "W")


def multiply(a, b, prime):
    assert a.shape[-1] * (prime - 1) ** 2 < 2**63
    return (a @ b) % prime


def stage_matrix(parameters, prime):
    n = len(parameters["d"])
    answer = np.empty((n, n), dtype=np.int64)
    for row in range(n):
        for col in range(n):
            value = parameters["d"][row] if row == col else (
                parameters["L"][row] * parameters["V"][col] if row > col
                else parameters["U"][row] * parameters["W"][col])
            answer[row, col] = int(value) % prime
    return answer


def product(stages, permutation, prime):
    answer = np.eye(len(permutation), dtype=np.int64)
    for index, stage in enumerate(stages):
        if index:
            answer = answer[permutation, :]
        answer = multiply(stage, answer, prime)
    return answer


def reconstruct(parameters, permutation, prime):
    """Use the rank-one derivative of each coordinate and outer products.

    Every local coordinate derivative is u v^T. Its global derivative is
    (left u) (v^T right), avoiding the uploaded derivative construction.
    """
    n, t = len(permutation), len(parameters)
    stages = [stage_matrix(s, prime) for s in parameters]
    identity = np.eye(n, dtype=np.int64)
    before = [identity]
    for k in range(1, t):
        before.append(multiply(stages[k - 1], before[-1], prime)[permutation, :])
    after = [None] * t
    after[-1] = identity
    inverse = np.argsort(permutation)
    for k in range(t - 2, -1, -1):
        after[k] = multiply(after[k + 1], stages[k + 1], prime)[:, inverse]
    columns = []
    for k, s in enumerate(parameters):
        for term in TERMS:
            for i in range(n):
                u, v = identity[:, i].copy(), identity[:, i].copy()
                if term == "L":
                    v[:] = 0
                    v[:i] = s["V"][:i]
                elif term == "V":
                    u[:] = 0
                    u[i + 1:] = s["L"][i + 1:]
                elif term == "U":
                    v[:] = 0
                    v[i + 1:] = s["W"][i + 1:]
                elif term == "W":
                    u[:] = 0
                    u[:i] = s["U"][:i]
                lu = multiply(after[k], u % prime, prime)
                vr = multiply(v % prime, before[k], prime)
                columns.append((np.outer(lu, vr) % prime).ravel())
    return product(stages, permutation, prime), np.array(columns).T, stages


def elimination(matrix, prime):
    """Exact row elimination, with original pivot row and column witnesses.

    The product of unnormalized pivots is the determinant for original rows
    in pivot-selection order. For a full-row-rank square matrix, the extra
    swap parity instead gives the determinant in its original row order.
    """
    a = np.array(matrix, dtype=np.int64, copy=True) % prime
    nr, nc = a.shape
    row_ids = list(range(nr))
    selected_cols = []
    pivots_product, sign, rank = 1, 1, 0
    for col in range(nc):
        if rank == nr:
            break
        candidates = np.flatnonzero(a[rank:, col])
        if not candidates.size:
            continue
        chosen = rank + int(candidates[0])
        if chosen != rank:
            a[[rank, chosen]] = a[[chosen, rank]]
            row_ids[rank], row_ids[chosen] = row_ids[chosen], row_ids[rank]
            sign *= -1
        pivot = int(a[rank, col])
        pivots_product = pivots_product * pivot % prime
        tail = a[rank, col:] * pow(pivot, -1, prime) % prime
        a[rank, col:] = tail
        active = np.flatnonzero(a[rank + 1:, col]) + rank + 1
        if active.size:
            a[active, col:] = (a[active, col:] - a[active, col, None] * tail) % prime
        selected_cols.append(col)
        rank += 1
    return {"rank": rank, "pivot_rows_in_selection_order": row_ids[:rank],
            "pivot_columns": selected_cols,
            "selected_minor_determinant": pivots_product,
            "original_order_determinant": sign * pivots_product % prime
            if nr == nc == rank else None}


def gauge_matrix(parameters, permutation, prime):
    n, t = len(permutation), len(parameters)
    cols = []
    def idx(s, term, i):
        return 5 * n * s + TERMS.index(term) * n + i
    def new():
        return np.zeros(5 * n * t, dtype=np.int64)
    for s, pa in enumerate(parameters):
        for term, i in (("L", 0), ("V", n-1), ("U", n-1), ("W", 0)):
            v = new()
            v[idx(s, term, i)] = 1
            cols.append(v)
        for positive, negative in (("L", "V"), ("U", "W")):
            v = new()
            for i in range(n):
                v[idx(s, positive, i)] = pa[positive][i]
                v[idx(s, negative, i)] = -pa[negative][i]
            cols.append(v)
    for s in range(t-1):
        for j, i in enumerate(permutation):
            v = new()
            for term in ("d", "L", "U"):
                v[idx(s, term, i)] = parameters[s][term][i]
            for term in ("d", "V", "W"):
                v[idx(s+1, term, j)] = -parameters[s+1][term][j]
            cols.append(v)
    return np.array(cols).T % prime


def scan(parameters, vector, prime):
    """Fresh implementation: two accumulators, counted full-charge scalar ops."""
    n = len(vector)
    answer = [int(parameters["d"][i]) * int(vector[i]) % prime for i in range(n)]
    acc = 0
    for i in range(n):
        answer[i] = (answer[i] + int(parameters["L"][i]) * acc) % prime
        acc = (acc + int(parameters["V"][i]) * int(vector[i])) % prime
    acc = 0
    for i in range(n - 1, -1, -1):
        answer[i] = (answer[i] + int(parameters["U"][i]) * acc) % prime
        acc = (acc + int(parameters["W"][i]) * int(vector[i])) % prime
    return np.array(answer, dtype=np.int64)


def main():
    ap = argparse.ArgumentParser()
    base = Path(__file__).resolve().parent
    ap.add_argument("input_directory", nargs="?", type=Path, default=base / "inputs")
    ap.add_argument("output_directory", nargs="?", type=Path, default=base / "checks")
    args = ap.parse_args()
    args.output_directory.mkdir(parents=True, exist_ok=True)
    def read(name):
        return json.loads((args.input_directory / name).read_text())
    records = read("BITREV_RESULTS.json")
    assert len(records) == 34
    gauges_expected = {(x["n"], x["t"], x["field"]): x for x in read("GAUGE_RESULTS.json")}
    results, source_checks = [], []
    started = time.monotonic()
    for n in (8, 16, 32):
        full_t = n // 4 + 1
        raw = read(f"WITNESS_N{n}_T{full_t}.json")
        assert (raw["n"], raw["t"], len(raw["stages"])) == (n, full_t, full_t)
        permutation = raw["permutation"]
        assert permutation == [int(f"{i:0{n.bit_length()-1}b}"[::-1], 2) for i in range(n)]
        parameters = [{term: np.array(s[term], dtype=np.int64).reshape(n) for term in TERMS}
                      for s in raw["stages"]]
        rng = random.Random(99017)
        for s in parameters:
            for term in ("L", "V", "U", "W", "d"):
                assert s[term].tolist() == [rng.randrange(1, 12289) for _ in range(n)]
        source_checks.append({"n": n, "integer_parameters_match_seed_recipe": True,
                              "bit_reversal_permutation": True})
        for t in range(1, full_t+1):
            for p in (12289, 65537):
                assert all(p % x for x in range(2, math.isqrt(p)+1))
                match = [x for x in records if (x["n"], x["t"], x["prime"]) == (n, t, p)]
                assert len(match) == 1
                expected = match[0]
                transform, jac, mats = reconstruct(parameters[:t], permutation, p)
                assert jac.shape == (n*n, 5*n*t)
                rr = elimination(jac, p)
                upper = min(n*n, n + t*(4*n-6))
                assert rr["rank"] == expected["rank"] == expected["theoretical_upper"] == upper
                stage_dets = [elimination(x, p)["original_order_determinant"] for x in mats]
                assert all(x is not None and x != 0 for x in stage_dets)
                # Finite differences are exact because every coordinate has degree <= 1.
                rng = random.Random(20261009+n*100+t+p)
                difference_columns = sorted(rng.sample(range(5*n*t), min(30, 5*n*t)))
                for col in difference_columns:
                    s, coordinate = divmod(col, 5*n)
                    term, i = TERMS[coordinate // n], coordinate % n
                    changed = [{key: val.copy() for key, val in pa.items()} for pa in parameters[:t]]
                    changed[s][term][i] += 1
                    perturbed = product([stage_matrix(pa, p) for pa in changed], permutation, p)
                    assert np.array_equal((perturbed-transform).ravel() % p, jac[:, col])
                g = gauge_matrix(parameters[:t], permutation, p)
                assert not multiply(jac, g, p).any()
                gr = elimination(g, p)["rank"]
                assert gr == 6*t+(t-1)*n
                nullity = 5*n*t-rr["rank"]
                gauge_record = {"jacobian_nullity": nullity, "gauge_rank": gr,
                                "jacobian_kills_gauges": True, "complete": gr == nullity}
                if (n, t, p) in gauges_expected:
                    old = gauges_expected[n, t, p]
                    assert old["jacobian_nullity"] == nullity
                    assert old["independent_gauges"] == gr
                    assert old["gauge_complete"] == (gr == nullity)
                saved_determinant = None
                scan_checks = None
                if t == full_t:
                    cert = raw["certificates_by_field"][str(p)]
                    assert cert == expected
                    cols = cert["full_rank_minor_column_indices"]
                    assert len(cols) == len(set(cols)) == n*n
                    md = elimination(jac[:, cols], p)
                    saved_determinant = md["original_order_determinant"]
                    assert md["rank"] == n*n
                    assert saved_determinant == cert["full_rank_minor_det_mod_prime"]
                    # Basis vectors certify the whole linear transform; add 14 fresh vectors.
                    vectors = list(np.eye(n, dtype=np.int64))
                    vectors += [np.array([rng.randrange(p) for _ in range(n)], dtype=np.int64)
                                for _ in range(14)]
                    for vector in vectors:
                        out = vector.copy()
                        for k, pa in enumerate(parameters):
                            if k:
                                out = out[permutation]
                            out = scan(pa, out, p)
                        assert np.array_equal(out, multiply(transform, vector, p))
                    scan_checks = {"basis_vectors": n, "fresh_vectors": 14,
                                   "multiplications": 5*n*t, "additions": 4*n*t,
                                   "permutation_reads": (t-1)*n}
                item = {"n": n, "t": t, "prime": p, "rank": rr["rank"],
                        "upper_bound": upper, "jacobian_sha256_le_i64":
                        hashlib.sha256(jac.astype("<i8").tobytes()).hexdigest(),
                        "rank_certificate": rr, "stage_determinants": stage_dets,
                        "finite_difference_columns": difference_columns,
                        "finite_differences_passed": True, "gauges": gauge_record,
                        "saved_full_rank_minor_determinant": saved_determinant,
                        "scan_checks": scan_checks}
                results.append(item)
                (args.output_directory / "checks.json").write_text(json.dumps({
                    "complete": len(results) == 34, "results": results,
                    "source_checks": source_checks}, indent=2)+"\n")
                print(f"PASS N={n} t={t} p={p}: rank={rr['rank']}, gauges={gr}, saved_det={saved_determinant}", flush=True)
    summary = {"status": "PASS", "rank_checks": len(results),
               "saved_minor_checks": sum(x["saved_full_rank_minor_determinant"] is not None for x in results),
               "finite_difference_checks": sum(len(x["finite_difference_columns"]) for x in results),
               "gauge_checks": len(results), "source_checks": source_checks,
               "seconds": time.monotonic()-started,
               "python": sys.version, "numpy": np.__version__, "platform": platform.platform()}
    (args.output_directory / "summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
