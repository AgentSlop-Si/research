#!/usr/bin/env python3
"""Fresh bounded exact seed gate. No uploaded source or numerical fitting."""
import json
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIME = 998244353
LABELS = [(axis, c, sign) for axis in ("H", "V") for c in (0, 1) for sign in (-1, 1)]


def is_prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))


def cycles(n):
    k = n.bit_length() - 1
    b = 1 << (k // 2)
    a = n // b
    answer = []
    for axis, c, sign in LABELS:
        p = []
        for v in range(n):
            x, y = divmod(v, b)
            if axis == "H":
                x = (x + sign * (2 * y + c)) % a
            else:
                y = (y + sign * (2 * x + c)) % b
            p.append(x * b + y)
        seen = bytearray(n)
        reps = []
        for v in range(n):
            if not seen[v]:
                reps.append(v)
                w = v
                while not seen[w]:
                    seen[w] = 1
                    w = p[w]
                assert w == v
        q = p.copy()
        for i, v in enumerate(reps):
            q[v] = p[reps[(i + 1) % len(reps)]]
        seen, v = set(), 0
        for _ in range(n):
            seen.add(v)
            v = q[v]
        assert len(seen) == n and v == 0
        answer.append(q)
    return answer


def green(p, denominator, prime=PRIME):
    n = len(p)
    tau = pow(denominator, -1, prime)
    wrap = (1 - pow(tau, n, prime)) % prime
    assert wrap
    result = [[0] * n for _ in range(n)]
    initial = pow(wrap, -1, prime)
    for column in range(n):
        row, coefficient = column, initial
        for _ in range(n):
            result[row][column] = coefficient
            row = p[row]
            coefficient = coefficient * tau % prime
    return result


def multiply(a, b, prime=PRIME):
    return [[sum(x * y for x, y in zip(row, column)) % prime
             for column in zip(*b)] for row in a]


def layer(gs, coefficients, prime=PRIME):
    n = len(gs[0])
    return [[sum(coefficients[j][i] * gs[j][i][k] for j in range(8)) % prime
             for k in range(n)] for i in range(n)]


def pivots(a, prime=PRIME):
    mat = [row[:] for row in a]
    rr, selected = 0, []
    for cc in range(len(mat[0])):
        pivot = next((i for i in range(rr, len(mat)) if mat[i][cc] % prime), None)
        if pivot is None:
            continue
        mat[rr], mat[pivot] = mat[pivot], mat[rr]
        inv = pow(mat[rr][cc], -1, prime)
        mat[rr] = [v * inv % prime for v in mat[rr]]
        for i in range(rr + 1, len(mat)):
            factor = mat[i][cc]
            mat[i] = [(u - factor * v) % prime for u, v in zip(mat[i], mat[rr])]
        selected.append(cc)
        rr += 1
        if rr == len(mat):
            break
    return selected


def determinant(a, prime=PRIME):
    mat = [row[:] for row in a]
    answer = 1
    for j in range(len(mat)):
        pivot = next((i for i in range(j, len(mat)) if mat[i][j] % prime), None)
        if pivot is None:
            return 0
        if pivot != j:
            mat[j], mat[pivot] = mat[pivot], mat[j]
            answer = -answer
        factor = mat[j][j]
        answer = answer * factor % prime
        inverse = pow(factor, -1, prime)
        for i in range(j + 1, len(mat)):
            scale = mat[i][j] * inverse % prime
            for k in range(j + 1, len(mat)):
                mat[i][k] = (mat[i][k] - scale * mat[j][k]) % prime
    return answer % prime


def solve(a, rhs, prime=PRIME):
    n = len(rhs)
    mat = [row[:] + [v] for row, v in zip(a, rhs)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if mat[i][j] % prime)
        mat[j], mat[pivot] = mat[pivot], mat[j]
        inv = pow(mat[j][j], -1, prime)
        mat[j] = [v * inv % prime for v in mat[j]]
        for i in range(n):
            if i != j:
                scale = mat[i][j]
                mat[i] = [(u - scale * v) % prime for u, v in zip(mat[i], mat[j])]
    return [row[-1] for row in mat]


def outer_gate(templates, target):
    rows = []
    for i, (t, wanted) in enumerate(zip(templates, target)):
        selected = pivots(t)
        assert len(selected) == 8
        square = [[row[j] for j in selected] for row in t]
        det = determinant(square)
        assert det
        a = solve([list(row) for row in zip(*square)], [wanted[j] for j in selected])
        got = [sum(a[j] * t[j][v] for j in range(8)) % PRIME for v in range(16)]
        bad = [v for v in range(16) if got[v] != wanted[v]]
        rows.append({"row": i, "pivot_columns": selected, "pivot_determinant": det,
                     "outer_coefficients": a, "nonzero_guard": all(a),
                     "residual_failure_columns": bad,
                     "residuals": [(got[v] - wanted[v]) % PRIME for v in range(16)]})
    return rows


def covariance_seed(matrix, z):
    n = len(matrix)
    covariance = all(matrix[i][j + 1] == pow(z, i, PRIME) * matrix[i][j] % PRIME
                     for i in range(n) for j in range(n - 1))
    seed = all(row[0] == 1 for row in matrix)
    return covariance, seed


def main():
    assert is_prime(PRIME)
    n, m = 16, 4
    z = pow(3, (PRIME - 1) // n, PRIME)
    assert pow(z, 8, PRIME) == PRIME - 1 and pow(z, 16, PRIME) == 1
    ps = cycles(n)
    gs = [green(p, j + 2) for j, p in enumerate(ps)]
    b = [[0] * n for _ in range(n)]
    for block in range(4):
        for i in range(m):
            for j in range(m):
                b[4 * block + i][4 * block + j] = (
                    pow(z, 4 * i * j, PRIME) if block < 2 else int(i == j))
    ones = [[1] * n for _ in range(8)]
    h1 = h2 = layer(gs, ones)
    prefix = multiply(multiply(h2, b), h1)
    prefix_det = determinant(prefix)
    assert prefix_det
    transported = [multiply(g, prefix) for g in gs]
    templates = [[transported[j][i] for j in range(8)] for i in range(n)]
    target = [[pow(z, i * j, PRIME) for j in range(n)] for i in range(n)]
    rows = outer_gate(templates, target)
    assert all(len(pivots(t)) == 8 for t in templates)
    certificates = []
    for i, t in enumerate(templates):
        augmented = t + [target[i]]
        selected = pivots(augmented)
        if len(selected) == 9:
            minor = [[row[j] for j in selected] for row in augmented]
            value = determinant(minor)
            assert value
            certificates.append({"row": i, "columns": selected,
                                 "minor_mod_prime": minor,
                                 "determinant_mod_prime": value})
    assert certificates
    supplied_outer = [[1 + 17 * j + 3 * i for i in range(n)] for j in range(8)]
    positive = multiply(layer(gs, supplied_outer), prefix)
    accepted = outer_gate(templates, positive)
    assert all(not row["residual_failure_columns"] and row["nonzero_guard"] for row in accepted)
    assert all(row["outer_coefficients"] == [supplied_outer[j][i] for j in range(8)]
               for i, row in enumerate(accepted))
    changed = None
    for col in range(n):
        candidate = [row[:] for row in positive]
        candidate[0][col] = (candidate[0][col] + 1) % PRIME
        rejected = outer_gate(templates, candidate)
        if rejected[0]["residual_failure_columns"]:
            changed = {"modified_row": 0, "modified_column": col,
                       "failed_residual_columns": rejected[0]["residual_failure_columns"]}
            break
    assert changed is not None
    assert covariance_seed(target, z) == (True, True)
    double_target = [[2 * v % PRIME for v in row] for row in target]
    assert covariance_seed(double_target, z) == (True, False)
    template_diagnostics = []
    for size in (4, 8, 16, 32, 64):
        perms = cycles(size)
        matrices = [green(p, j + 2) for j, p in enumerate(perms)]
        ranks = [len(pivots([g[i] for g in matrices])) for i in range(size)]
        assert ranks == [min(8, size)] * size
        template_diagnostics.append({"N": size, "distinct_cycles": len({tuple(p) for p in perms}),
                                     "row_template_ranks": ranks})
    result = {
        "status": "PASS: fixed inner prefix rejected; verifier controls pass",
        "scope": "All256 inner left-endpoint entries fixed to1; all128 outer entries free. This does not reject other inner coefficients, the full384-variable model, or the general eight-cycle architecture.",
        "field": {"prime": PRIME, "cyclotomic_root": z, "minimal_polynomial": "z^8+1",
                  "prime_verified_by_trial_division": True},
        "model": {"N": 16, "m": 4, "active_blocks": [0, 1], "product": "H3 H2 B H1",
                  "pole_denominators": list(range(2, 10)), "label_order": LABELS,
                  "green_occurrences": 24, "fixed_inner_endpoint_entries": 256,
                  "free_outer_endpoint_entries": 128, "total_endpoint_entries": 384,
                  "cycle_successors": ps},
        "prefix_determinant_mod_prime": prefix_det,
        "outer_elimination_rows": rows,
        "augmented_rank_nine_witnesses": certificates,
        "characteristic_zero_lift_of_negative_result": "The templates have entries in Q(z)/(z^8+1), all rational denominators survive modulo this prime, and a displayed9-by9minor specializes to a nonzero determinant. It is therefore nonzero in characteristic zero. Eight outer templates cannot span the Fourier row, even over any field extension.",
        "positive_control": "All256 product entries pass for a generated admissible outer coefficient set, and all128 supplied outer coefficients are recovered exactly.",
        "changed_entry_negative_control": changed,
        "seed_control": "F16 passes covariance and seed;2F16 passes covariance and fails seed.",
        "template_diagnostics": template_diagnostics,
        "provenance": "Fresh standard-library formula checker, no uploaded code and no numerical optimization."}
    (HERE / "N16_OUTER_GATE_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "rank_nine_witnesses": len(certificates),
                      "first_row": certificates[0]["row"],
                      "first_minor_determinant": certificates[0]["determinant_mod_prime"]}))


if __name__ == "__main__":
    main()
