#!/usr/bin/env python3
"""New exact controls for route, resolvent, mask, and bank folding identities."""
import json
import random
from pathlib import Path
from check_n16_outer_gate import LABELS, PRIME, determinant, pivots, multiply

HERE = Path(__file__).resolve().parent


def cover_and_splice(a, b, label):
    axis, c, sign = label
    p = []
    for v in range(a * b):
        x, y = divmod(v, b)
        if axis == "H":
            x = (x + sign * (2 * y + c)) % a
        else:
            y = (y + sign * (2 * x + c)) % b
        p.append(x * b + y)
    seen, reps = bytearray(a * b), []
    for v in range(a * b):
        if not seen[v]:
            reps.append(v)
            w = v
            while not seen[w]:
                seen[w] = 1
                w = p[w]
            assert w == v
    q = p.copy()
    for j, v in enumerate(reps):
        q[v] = p[reps[(j + 1) % len(reps)]]
    return p, q, reps


def project(v, a, b):
    x, y = divmod(v, 2 * b)
    return (x % a) * b + y % b


def fiber(v, a, b):
    x, y = divmod(v, b)
    return [(x + dx * a) * (2 * b) + y + dy * b for dx in (0, 1) for dy in (0, 1)]


def fold(vector, a, b):
    out = [0] * (a * b)
    for v, value in enumerate(vector):
        w = project(v, a, b)
        out[w] = (out[w] + value) % PRIME
    return out


def direct_defect(vector, small, large, a, b):
    out = [0] * (a * b)
    for v, value in enumerate(vector):
        dst1 = project(large[v], a, b)
        dst2 = small[project(v, a, b)]
        out[dst1] = (out[dst1] + value) % PRIME
        out[dst2] = (out[dst2] - value) % PRIME
    return out


def sparse_defect(vector, ts, ps, rs, tl, pl, rl, a, b):
    out = [0] * (a * b)
    for v in rl:
        dst1, dst2 = project(pl[v], a, b), project(tl[v], a, b)
        out[dst1] = (out[dst1] + vector[v]) % PRIME
        out[dst2] = (out[dst2] - vector[v]) % PRIME
    for v in rs:
        value = sum(vector[z] for z in fiber(v, a, b)) % PRIME
        out[ps[v]] = (out[ps[v]] - value) % PRIME
        out[ts[v]] = (out[ts[v]] + value) % PRIME
    return out


def apply_green(p, weights, vector):
    n = len(p)
    order, v = [], 0
    for _ in range(n):
        order.append(v)
        v = p[v]
    assert v == 0 and len(set(order)) == n
    carry, product = 0, 1
    for v in order:
        carry = (vector[v] + weights[v] * carry) % PRIME
        product = product * weights[v] % PRIME
    assert product != 1
    last = carry * pow((1 - product) % PRIME, -1, PRIME) % PRIME
    out = [0] * n
    for v in order:
        last = (vector[v] + weights[v] * last) % PRIME
        out[v] = last
    return out


def route_controls():
    rng, records = random.Random(77419), []
    for r in range(1, 7):
        for rectangular in (False, True):
            b = 1 << r
            a = b * (2 if rectangular else 1)
            n = a * b
            for j, label in enumerate(LABELS):
                ts, ps, rs = cover_and_splice(a, b, label)
                tl, pl, rl = cover_and_splice(2 * a, 2 * b, label)
                assert all(project(tl[v], a, b) == ts[project(v, a, b)] for v in range(4 * n))
                bad = [v for v in range(4 * n) if project(pl[v], a, b) != ps[project(v, a, b)]]
                assert len(bad) <= len(rl) + 4 * len(rs)
                rank = None
                if n <= 128:
                    mat = [[0] * len(bad) for _ in range(n)]
                    for cc, v in enumerate(bad):
                        mat[project(pl[v], a, b)][cc] += 1
                        mat[ps[project(v, a, b)]][cc] -= 1
                    rank = len(pivots(mat)) if bad else 0
                    assert rank <= len(rl) + len(rs) - 2
                x = [rng.randrange(PRIME) for _ in range(4 * n)]
                direct = direct_defect(x, ps, pl, a, b)
                assert direct == sparse_defect(x, ts, ps, rs, tl, pl, rl, a, b)
                tau = pow(j + 2, -1, PRIME)
                glx = apply_green(pl, [tau] * (4 * n), x)
                lhs = [(v - w) % PRIME for v, w in zip(fold(glx, a, b),
                       apply_green(ps, [tau] * n, fold(x, a, b)))]
                rhs = apply_green(ps, [tau] * n,
                      sparse_defect(glx, ts, ps, rs, tl, pl, rl, a, b))
                assert lhs == [tau * v % PRIME for v in rhs]
                if n <= 128:
                    ws = [2 + (v % 5) for v in range(n)]
                    wl = [ws[project(v, a, b)] for v in range(4 * n)]
                    gx = apply_green(pl, wl, x)
                    lhsw = [(v - w) % PRIME for v, w in zip(fold(gx, a, b),
                            apply_green(ps, ws, fold(x, a, b)))]
                    dd = sparse_defect(gx, ts, ps, rs, tl, pl, rl, a, b)
                    rhsw = apply_green(ps, ws, [w * v % PRIME for w, v in zip(ws, dd)])
                    assert lhsw == rhsw
                    mask = [11 + v % 7 for v in range(n)]
                    left = fold([mask[project(v, a, b)] * x[v] % PRIME for v in range(4 * n)], a, b)
                    assert left == [v * w % PRIME for v, w in zip(mask, fold(x, a, b))]
                records.append({"N": n, "rectangle": rectangular, "label": label,
                                "small_cycle_count": len(rs), "large_cycle_count": len(rl),
                                "defect_supported_columns": len(bad),
                                "support_bound": len(rl) + 4 * len(rs),
                                "rank_mod_prime_if_computed": rank,
                                "rank_bound": len(rl) + len(rs) - 2,
                                "first_disagreeing_column": None if not bad else {
                                    "large_vertex": bad[0],
                                    "projected_large_successor": project(pl[bad[0]], a, b),
                                    "small_successor_of_projection": ps[project(bad[0], a, b)]}})
            print("routes", n, rectangular, flush=True)
    return records


def bank_controls():
    records = []
    for r in range(0, 9):
        m = 1 << r
        omega = pow(3, (PRIME - 1) // (2 * m), PRIME)
        assert pow(omega, m, PRIME) == PRIME - 1
        small = [[pow(omega, 2 * i * j, PRIME) for j in range(m)] for i in range(m)]
        mismatch = [[0] * (2 * m) for _ in range(m)]
        selector = [[0] * (2 * m) for _ in range(m)]
        for i in range(m):
            for j in range(2 * m):
                top = pow(omega, i * j, PRIME)
                bottom = pow(omega, (i + m) * j, PRIME)
                plus, minus = (top + bottom) % PRIME, (top - bottom) % PRIME
                wanted_plus = 2 * small[i][j // 2] % PRIME if j % 2 == 0 else 0
                wanted_minus = 2 * pow(omega, i, PRIME) * small[i][j // 2] % PRIME if j % 2 else 0
                assert plus == wanted_plus and minus == wanted_minus
                mismatch[i][j] = (plus - small[i][j % m]) % PRIME
                selector[i][j] = (2 * int(j == 2 * i) - int(j % m == i)) % PRIME
        if m <= 64:
            assert multiply(small, selector) == mismatch
        even_minor = [[selector[i][2 * j] for j in range(m)] for i in range(m)]
        value = determinant(even_minor)
        assert value == pow(2, m - 1, PRIME)
        records.append({"m": m, "exact_plus_entries": 2 * m * m,
                        "exact_minus_entries": 2 * m * m,
                        "selector_even_minor_determinant": value,
                        "expected_determinant_2_power_m_minus_1": pow(2, m - 1, PRIME)})
    global_records = []
    for a, b in ((2, 2), (4, 2), (4, 4), (8, 4), (8, 8)):
        n = a * b
        active = set(range(a // 2))
        active_large = active | {x + a for x in active}
        omega = pow(3, (PRIME - 1) // (2 * b), PRIME)
        difference = [[0] * (4 * n) for _ in range(n)]
        for row in range(n):
            x, y = divmod(row, b)
            for col in range(4 * n):
                xx, yy = divmod(col, 2 * b)
                if xx % a != x:
                    continue
                if xx in active_large:
                    left = (pow(omega, y * yy, PRIME) + pow(omega, (y + b) * yy, PRIME)) % PRIME
                else:
                    left = int(yy % b == y)
                right = pow(omega, 2 * y * (yy % b), PRIME) if x in active else int(yy % b == y)
                difference[row][col] = (left - right) % PRIME
        rank = len(pivots(difference))
        assert rank == b * len(active)
        global_records.append({"N": n, "m": b, "active_small": sorted(active),
                               "active_large": sorted(active_large),
                               "entrywise_bank_defect_rank": rank,
                               "active_mass": b * len(active)})
    return {"block_identities": records, "global_folding": global_records}


def main():
    result = {"status": "PASS", "prime": PRIME,
              "scope": "Exact finite controls for proved identities; no coefficient lift or Fourier factorization supplied.",
              "routes": route_controls(), "banks": bank_controls(),
              "provenance": "Fresh checker plus the newly authored exact matrix helpers in check_n16_outer_gate.py; no uploaded research code executed."}
    (HERE / "LIFT_DEFECT_CONTROLS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "route_instances": len(result["routes"]),
                      "block_bank_sizes": len(result["banks"]["block_identities"])}), flush=True)


if __name__ == "__main__":
    main()
