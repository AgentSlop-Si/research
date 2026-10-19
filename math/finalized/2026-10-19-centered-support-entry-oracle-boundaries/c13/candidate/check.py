"""Fresh exact controls for the adapter and elementary query-bound witnesses.

Historical code is never imported. Only adapter.py from this packet is used.
Dense matrix construction/inversion here is a correctness reference and is not
part of the adapter's O(N^2) arithmetic/query claim.
"""
import hashlib
import itertools
import json
import sys
from pathlib import Path
from random import Random
from fractions import Fraction
sys.path.insert(0, str(Path(__file__).resolve().parent))
from adapter import Field, CountingOracle, complete, affine_nonzero_solve


def eye(n, f):
    return [[f.value(int(i == j)) for j in range(n)] for i in range(n)]


def add(a, b, f):
    return [[f.add(u, v) for u, v in zip(ar, br)] for ar, br in zip(a, b)]


def mul(a, b, f):
    result = [[f.value(0) for _ in b[0]] for _ in a]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] = f.add(result[i][j], f.mul(a[i][k], b[k][j]))
    return result


def inv(a, f):
    n, identity = len(a), eye(len(a), f)
    work = [list(a[i]) + identity[i] for i in range(n)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if work[i][j]), None)
        if pivot is None:
            raise ValueError("singular")
        work[j], work[pivot] = work[pivot], work[j]
        factor = work[j][j]
        work[j] = [f.div(v, factor) for v in work[j]]
        for i in range(n):
            if i != j:
                factor = work[i][j]
                work[i] = [f.sub(v, f.mul(factor, u)) for v, u in zip(work[i], work[j])]
    return [row[n:] for row in work]


def det(a, f):
    a, value = [list(row) for row in a], f.value(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return f.value(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            value = f.sub(0, value)
        pivot_value = a[j][j]
        value = f.mul(value, pivot_value)
        for i in range(j + 1, len(a)):
            ratio = f.div(a[i][j], pivot_value)
            for k in range(j + 1, len(a)):
                a[i][k] = f.sub(a[i][k], f.mul(ratio, a[j][k]))
    return value


def diag(d, f):
    return [[f.value(d[i] if i == j else 0) for j in range(len(d))] for i in range(len(d))]


def perm(p, f):
    return [[f.value(int(j == p[i])) for j in range(len(p))] for i in range(len(p))]


def directions(data, f):
    n = len(data["a"])
    u, v = [[f.value(0) for _ in range(n)] for _ in range(n)], [[f.value(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        u[i][data["r0"][i]] = f.add(u[i][data["r0"][i]], f.value(data["a"][i]))
        u[i][data["r1"][i]] = f.add(u[i][data["r1"][i]], f.value(data["b"][i]))
        j, k = data["s0"][i], data["s1"][i]
        v[i][j] = f.add(v[i][j], f.value(data["d"][j]))
        v[i][k] = f.add(v[i][k], f.value(data["e"][k]))
    return u, v


def canonical(n, b=0, e=0, vshift=1):
    identity, shift = list(range(n)), [(i + 1) % n for i in range(n)]
    return {"r0": identity, "r1": shift, "s0": identity,
            "s1": [(i + vshift) % n for i in range(n)],
            "a": [1] * n, "b": [b] * n, "d": [1] * n, "e": [e] * n}


def verify_plans(data, btarget, answer, f):
    n, plans = len(data["a"]), answer["plans"]
    u, v = directions(data, f)
    q0 = mul(diag([f.div(1, t) for t in answer["x"]], f), u, f)
    q1 = mul(v, diag([f.div(1, t) for t in answer["y"]], f), f)
    t0, t1 = inv(q0, f), inv(q1, f)
    assert add(t0, t1, f) == btarget
    def green(tau, weights):
        denom = eye(n, f)
        for i in range(n):
            denom[i][tau[i]] = f.sub(denom[i][tau[i]], weights[i])
        return inv(denom, f)
    formula0 = mul(mul(perm(plans["r0_inverse"], f), green(plans["tau0"], plans["w0"]), f),
                   diag(plans["right_scale0"], f), f)
    formula1 = mul(mul(diag(plans["left_scale1"], f), green(plans["tau1"], plans["w1"]), f),
                   perm(plans["s0_inverse"], f), f)
    assert formula0 == t0 and formula1 == t1


def graph_controls(rng):
    count = 0
    for p in (2, 3, 5):
        f = Field(p)
        for nvars in range(1, 5):
            for trial in range(40):
                equations = []
                for _ in range(rng.randrange(1, 9)):
                    u, v = rng.randrange(nvars), rng.randrange(nvars)
                    a, b, k = (rng.randrange(p) for _ in range(3))
                    equations.append((u, v, a, b, k))
                witness = next((values for values in itertools.product(range(1, p), repeat=nvars)
                                if all((a * values[u] + b * values[v]) % p == k
                                       for u, v, a, b, k in equations)), None)
                answer = affine_nonzero_solve(nvars, equations, f)
                assert answer["ok"] == (witness is not None), (p, equations, answer, witness)
                count += 1
    return count


def positive_controls(rng):
    rows = []
    for p in (2, 3, 5, 7, 241):
        f = Field(p)
        for n in range(3, 10):
            for trial in range(6):
                for attempt in range(2000):
                    r0, s0, cycle0, cycle1 = (list(range(n)) for _ in range(4))
                    for permutation in (r0, s0, cycle0, cycle1):
                        rng.shuffle(permutation)
                    tau0, tau1 = [None] * n, [None] * n
                    for cycle, tau in ((cycle0, tau0), (cycle1, tau1)):
                        for i in range(n):
                            tau[cycle[i]] = cycle[(i + 1) % n]
                    data = {"r0": r0, "r1": [r0[tau0[i]] for i in range(n)],
                            "s0": s0, "s1": [tau1[s0[i]] for i in range(n)],
                            "a": [rng.randrange(1, p) for _ in range(n)],
                            "b": [rng.randrange(p) for _ in range(n)],
                            "d": [rng.randrange(1, p) for _ in range(n)],
                            "e": [rng.randrange(p) for _ in range(n)]}
                    u, v = directions(data, f)
                    try:
                        ui, vi = inv(u, f), inv(v, f)
                        break
                    except ValueError:
                        pass
                else:
                    raise AssertionError("Positive generator failed")
                x, y = [[rng.randrange(1, p) for _ in range(n)] for _ in range(2)]
                btarget = add(mul(ui, diag(x, f), f), mul(diag(y, f), vi, f), f)
                oracle = CountingOracle(lambda i, j: btarget[i][j])
                answer = complete(data, oracle, f)
                assert answer["ok"], (p, n, answer)
                assert answer["target_queries"] == oracle.calls <= 4 * n * n
                assert answer["sandwich_entries"] == n * n
                assert answer["supported_equations"] <= 4 * n
                assert answer["sandwich_field_operations"] <= 12 * n * n
                assert answer["graph_field_operations"] <= 72 * n
                assert answer["graph_certificate"]["forbidden_comparisons"] <= 6 * n * n + n
                verify_plans(data, btarget, answer, f)
                # A projective gauge changes directions but preserves feasibility.
                row_gauge, col_gauge = [[rng.randrange(1, p) for _ in range(n)] for _ in range(2)]
                gauged = dict(data)
                gauged["a"] = [f.mul(g, a) for g, a in zip(row_gauge, data["a"])]
                gauged["b"] = [f.mul(g, b) for g, b in zip(row_gauge, data["b"])]
                gauged["d"] = [f.mul(g, d) for g, d in zip(col_gauge, data["d"])]
                gauged["e"] = [f.mul(g, e) for g, e in zip(col_gauge, data["e"])]
                answer2 = complete(gauged, lambda i, j: btarget[i][j], f)
                assert answer2["ok"]
                verify_plans(gauged, btarget, answer2, f)
                rows.append({"p": p, "n": n, "trial": trial,
                             "queries": oracle.calls, "sandwich_ops": answer["sandwich_field_operations"],
                             "graph_ops": answer["graph_field_operations"]})
    return rows


def negative_controls():
    f, data = Field(241), canonical(5, -2, -3, 2)
    u, v = directions(data, f)
    k = add(u, v, f)
    k[0][0] = f.add(k[0][0], 1)
    btarget = mul(mul(inv(u, f), k, f), inv(v, f), f)
    answer = complete(data, lambda i, j: btarget[i][j], f)
    assert not answer["ok"] and answer["stage"] == "scale_system"
    assert answer["sandwich_entries"] == 25
    # This is a fresh shift-one/shift-two analogue, not the historical route
    # witness: that review does not list its complete permutation vectors.
    fq = Field()
    uq, vq = directions(data, fq)
    kq = add(uq, vq, fq)
    kq[0][0] += 1
    determinants = [det(m, fq) for m in (uq, vq, kq)]
    assert determinants == [-31, -242, -923]
    cases = {"off_support_pass_scale_failure": answer["reason"]}
    bad = canonical(4)
    bad["a"][0] = 0
    result = complete(bad, lambda i, j: int(i == j), f)
    assert result["reason"] == "zero_base_coordinate"
    cases["zero_base"] = result["reason"]
    result = complete(canonical(4, -1), lambda i, j: int(i == j), f)
    assert result["reason"] == "singular_denominator"
    cases["singular_denominator"] = result["reason"]
    bad = canonical(4)
    bad["r1"] = [1, 0, 3, 2]
    result = complete(bad, lambda i, j: int(i == j), f)
    assert result["reason"] == "non_hamiltonian_prescribed_route"
    cases["fixed_zero_edge_route"] = result["reason"]
    result = complete(canonical(4), lambda i, j: 2 * int(i == j) + int((i, j) == (0, 2)), f)
    assert result["reason"] == "off_support_residual"
    cases["off_support"] = result["reason"]
    result = complete(canonical(3), lambda i, j: int(i == j), Field(2))
    assert result["reason"] == "field_exhaustion"
    cases["F2_exhaustion"] = result["reason"]
    result = complete(canonical(3), lambda i, j: int(i == j), Field(3))
    assert result["ok"]
    cases["F3_control"] = "accepted"
    result = complete(canonical(3), lambda i, j: 0, Field(2))
    assert result["ok"] and not result["target_invertibility_checked"]
    cases["singular_target_sum_allowed"] = "accepted_with_target_guard_explicitly_unchecked"
    return cases, determinants


def query_witness_controls():
    f, records, total_alternatives = Field(), [], 0
    for kind in ("zero_edges", "nonzero_edges"):
        for n in range(3, 11):
            data = canonical(n, *( (0, 0) if kind == "zero_edges" else (-2, -3)))
            u, v = directions(data, f)
            b0 = add(inv(u, f), inv(v, f), f)
            b0i = inv(b0, f)
            base = complete(data, lambda i, j: b0[i][j], f)
            assert base["ok"]
            verify_plans(data, b0, base, f)
            candidates = [(a, b) for a in range(n) for b in range(n)
                          if a != b and (kind == "zero_edges" or b != (a + 1) % n)]
            expected = n * (n - 1) if kind == "zero_edges" else n * (n - 2)
            assert len(candidates) == expected
            for a, b in candidates:
                # Matrix determinant lemma: choose either delta=1 or delta=2,
                # avoiding the sole possible rank-one singularity.
                delta = Fraction(1) if 1 + b0i[b][a] != 0 else Fraction(2)
                perturb = [list(row) for row in b0]
                perturb[a][b] += delta
                assert det(perturb, f) != 0
                answer = complete(data, lambda i, j: perturb[i][j], f)
                assert not answer["ok"] and answer["reason"] == "off_support_residual"
                sandwich_delta = mul(mul(u, [[delta if (i, j) == (a, b) else Fraction(0)
                                               for j in range(n)] for i in range(n)], f), v, f)
                assert sandwich_delta[a][b] == delta
                total_alternatives += 1
            records.append({"family": kind, "n": n, "invertible_rejecting_alternatives": expected,
                            "base_target_queries": base["target_queries"]})
    return records, total_alternatives


def general_matching_controls(rng):
    # Exercise the N^2-|S| matching argument for arbitrary legal nontrivial
    # endpoint permutations, independently of the canonical lower-bound family.
    f, count = Field(241), 0
    for n in range(3, 9):
        for _ in range(6):
            r0, s0 = list(range(n)), list(range(n))
            rng.shuffle(r0)
            rng.shuffle(s0)
            data = canonical(n, -2, -3)
            data.update(r0=r0, r1=[r0[(i + 1) % n] for i in range(n)],
                        s0=s0, s1=[(s0[i] + 1) % n for i in range(n)])
            u, v = directions(data, f)
            support = {(i, j) for i in range(n) for j in range(n) if u[i][j] or v[i][j]}
            matching_u = {r0[i]: i for i in range(n)}  # column -> distinct row
            matching_v = {i: s0[i] for i in range(n)}  # row -> distinct column
            selected = [(a, b) for a in range(n) for b in range(n)
                        if (matching_u[a], matching_v[b]) not in support]
            assert len(selected) == n * n - len(support)
            for a, b in selected:
                assert f.mul(u[matching_u[a]][a], v[b][matching_v[b]]) != 0
            count += 1
    return count


def encode(value):
    if isinstance(value, Fraction):
        return str(value)
    raise TypeError(type(value).__name__)


def main():
    rng = Random(202610191525)
    graph_count = graph_controls(rng)
    positives = positive_controls(rng)
    negatives, determinants = negative_controls()
    witnesses, alternatives = query_witness_controls()
    matching = general_matching_controls(rng)
    result = {"status": "PASS", "graph_systems_against_exhaustive_nonzero_search": graph_count,
              "fixed_direction_positives": len(positives), "projective_gauge_positives": len(positives),
              "fresh_analogue_determinants_over_Q": determinants,
              "negative_and_field_controls": negatives,
              "entry_query_witness_families": witnesses,
              "invertible_rejecting_single_entry_alternatives": alternatives,
              "general_matching_controls": matching,
              "positive_operation_counts": positives,
              "scope": "Finite exact controls, not proof of the all-size theorem or an asymptotic benchmark",
              "adapter_sha256": hashlib.sha256(Path(__file__).with_name("adapter.py").read_bytes()).hexdigest()}
    Path(__file__).with_name("RESULTS.json").write_text(json.dumps(result, indent=2, default=encode) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("positive_operation_counts", "entry_query_witness_families")}, indent=2, default=encode))


if __name__ == "__main__":
    main()
