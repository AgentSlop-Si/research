#!/usr/bin/env python3
"""Independent exact checks. Standard library only; no uploaded code imports.

Dense matrices and Gaussian elimination below are test oracles, not claimed
subquadratic Fourier executors. The half-cycle evaluator itself is linear.
"""
import argparse
import json
import random
from collections import deque
from fractions import Fraction
from pathlib import Path

P = 998244353
HERE = Path(__file__).resolve().parent


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def add(a, b, p=P):
    return [[(u + v) % p for u, v in zip(x, y)] for x, y in zip(a, b)]


def scale(a, c, p=P):
    return [[c * v % p for v in row] for row in a]


def mul(a, b, p=P):
    out = [[0] * len(b[0]) for _ in a]
    for i, row in enumerate(a):
        for k, u in enumerate(row):
            if u:
                for j, v in enumerate(b[k]):
                    out[i][j] = (out[i][j] + u * v) % p
    return out


def sub(a, rr, cc):
    return [[a[i][j] for j in cc] for i in rr]


def rank(a, p=P):
    if not a or not a[0]:
        return 0
    b = [row[:] for row in a]
    r = 0
    for c in range(len(b[0])):
        pivot = next((i for i in range(r, len(b)) if b[i][c] % p), None)
        if pivot is None:
            continue
        b[r], b[pivot] = b[pivot], b[r]
        z = pow(b[r][c], -1, p)
        b[r] = [v * z % p for v in b[r]]
        for i in range(r + 1, len(b)):
            z = b[i][c]
            if z:
                b[i] = [(u - z * v) % p for u, v in zip(b[i], b[r])]
        r += 1
        if r == len(b):
            break
    return r


def inv(a, p=P):
    n = len(a)
    e = eye(n)
    b = [row[:] + e[i] for i, row in enumerate(a)]
    for c in range(n):
        pivot = next((i for i in range(c, n) if b[i][c] % p), None)
        if pivot is None:
            raise ValueError("singular")
        b[c], b[pivot] = b[pivot], b[c]
        z = pow(b[c][c], -1, p)
        b[c] = [v * z % p for v in b[c]]
        for i in range(n):
            if i != c:
                z = b[i][c]
                if z:
                    b[i] = [(u - z * v) % p for u, v in zip(b[i], b[c])]
    return [row[n:] for row in b]


def determinant(a, p):
    b = [row[:] for row in a]
    ans = 1
    for c in range(len(b)):
        pivot = next((i for i in range(c, len(b)) if b[i][c] % p), None)
        if pivot is None:
            return 0
        if pivot != c:
            b[c], b[pivot] = b[pivot], b[c]
            ans = -ans
        ans = ans * b[c][c] % p
        z = pow(b[c][c], -1, p)
        for i in range(c + 1, len(b)):
            t = b[i][c] * z % p
            b[i] = [(u - t * v) % p for u, v in zip(b[i], b[c])]
    return ans % p


def cut_ranks(a):
    n = len(a)
    return [(rank(sub(a, range(k), range(k, n))),
             rank(sub(a, range(k, n), range(k)))) for k in range(1, n)]


def qsep(a):
    return max(max(pair) for pair in cut_ranks(a)) if len(a) > 1 else 0


def poly(a, coefficients):
    n = len(a)
    e = eye(n)
    out = [[0] * n for _ in range(n)]
    for coefficient in reversed(coefficients):
        out = add(mul(a, out), scale(e, coefficient))
    return out


def signed_cycle(n):
    a = [[0] * n for _ in range(n)]
    for j in range(n - 1):
        a[j + 1][j] = 1
    a[0][n - 1] = P - 1
    return a


def base_matrix(n, kind, rng):
    if kind == "cycle":
        return signed_cycle(n)
    a = [[0] * n for _ in range(n)]
    for i in range(n):
        a[i][i] = 7 + i
        if i:
            a[i][i - 1] = -2 % P
        if i + 1 < n:
            a[i][i + 1] = -1 % P
    if kind == "tridiagonal_plus_rank1":
        u = [rng.randrange(1, 10) for _ in range(n)]
        v = [rng.randrange(1, 10) for _ in range(n)]
        a = add(a, [[x * y % P for y in v] for x in u])
    return a


def check_inverse_and_rational(rng):
    records = []
    special = []
    for n in (4, 8, 16):
        m = n // 2
        a = [[int(j == (i + m) % n) for j in range(n)] for i in range(n)]
        assert rank(sub(a, range(m), range(m))) == 0
        assert cut_ranks(a) == cut_ranks(inv(a))
        special.append({"n": n, "principal_rank": 0,
                        "middle_offdiagonal_rank": m})
    for n in (12, 20, 28):
        for kind in ("cycle", "tridiagonal", "tridiagonal_plus_rank1"):
            a = base_matrix(n, kind, rng)
            assert cut_ranks(a) == cut_ranks(inv(a))
            h = qsep(a)
            for dp, dq in ((0, 1), (1, 0), (1, 1), (2, 2),
                           (3, 1), (1, 3), (4, 3), (3, 4)):
                cp = [rng.randrange(1, 100) for _ in range(dp + 1)]
                cq = [rng.randrange(1, 100) for _ in range(dq + 1)]
                # Nonsingularity is checked, never assumed from random sampling.
                denominator = poly(a, cq)
                inverse = inv(denominator)
                assert cut_ranks(denominator) == cut_ranks(inverse)
                value = mul(poly(a, cp), inverse)
                actual = qsep(value)
                assert actual <= h * max(dp, dq)
                records.append({"n": n, "base": kind, "h": h,
                                "degrees": [dp, dq], "qsep": actual,
                                "bound": h * max(dp, dq)})
            # Repeated pole and a numerator/denominator cancellation.
            # q(z)=(z-100)^4, p(z)=(z-100)^2*(1+3z).
            linear = add(a, scale(eye(n), -100))
            den = mul(mul(linear, linear), mul(linear, linear))
            numerator = mul(mul(linear, linear), add(eye(n), scale(a, 3)))
            value = mul(numerator, inv(den))
            reduced = mul(add(eye(n), scale(a, 3)), inv(mul(linear, linear)))
            assert value == reduced
            assert qsep(value) <= 2 * h
    return {"random_rational_cases": records,
            "singular_principal_block_controls": special,
            "repeated_pole_cancellation_cases": 9}


def cycle_action(x, shift):
    n = len(x)
    out = [0] * n
    for j, v in enumerate(x):
        k = j + shift
        out[k % n] = -v if k >= n else v
    return out


def apply_k_mod(x, lam, p=P):
    # Solve (I-lambda*M) z=x by a cyclic scalar recurrence.
    tail = 0
    for v in x[1:]:
        tail = (v + lam * tail) % p
    z0 = (x[0] - lam * tail) * pow(1 + pow(lam, len(x), p), -1, p) % p
    z = [z0]
    for v in x[1:]:
        z.append((v + lam * z[-1]) % p)
    return [(v + w) % p for v, w in zip(x, z)]


def apply_fused_mod(x, p=P):
    m = len(x) // 2
    z = pow(2, m, p)
    alpha = (z + 1) * pow(2, -1, p) % p
    beta = (z - 1) * pow(2, -1, p) % p
    return [(alpha * v + beta * w) % p
            for v, w in zip(x, cycle_action(x, m))]


def apply_k_fraction(x, lam):
    tail = Fraction(0)
    for v in x[1:]:
        tail = v + lam * tail
    z = [(x[0] - lam * tail) / (1 + lam ** len(x))]
    for v in x[1:]:
        z.append(v + lam * z[-1])
    return [v + w for v, w in zip(x, z)]


def check_halfcycle(rng):
    modular = []
    for n in (2, 4, 8, 16, 32, 64, 128):
        m = n // 2
        root = pow(3, (P - 1) // m, P)
        assert pow(root, m, P) == 1
        if m > 1:
            assert pow(root, m // 2, P) != 1
        for _ in range(8):
            x = [rng.randrange(P) for _ in range(n)]
            y = x[:]
            phase = 1
            for j in range(m):
                y = apply_k_mod(y, phase)
                phase = phase * root % P
            assert y == apply_fused_mod(x)
        # Verify all columns and support count of the fused evaluator.
        columns = [apply_fused_mod([int(i == j) for i in range(n)])
                   for j in range(n)]
        assert all(sum(v != 0 for v in c) == 2 for c in columns)
        matrix = [list(row) for row in zip(*columns)]
        half_cut_rank = rank(sub(matrix, range(m), range(m, n)))
        assert half_cut_rank == m
        modular.append({"n": n, "word_length": m, "fresh_inputs": 8,
                        "basis_columns": n, "nonzeros_per_column": 2,
                        "natural_half_cut_rank": half_cut_rank})
    rational = []
    for n, phases in ((2, (1,)), (4, (1, -1))):
        for trial in range(5):
            x = [Fraction(rng.randrange(-30, 31), rng.randrange(1, 12))
                 for _ in range(n)]
            y = x[:]
            for phase in phases:
                y = apply_k_fraction(y, Fraction(phase))
            m = n // 2
            a = Fraction(2 ** m + 1, 2)
            b = Fraction(2 ** m - 1, 2)
            expected = [a * v + b * w for v, w in zip(x, cycle_action(x, m))]
            assert y == expected
        rational.append({"n": n, "fresh_exact_rational_inputs": 5})
    return {"modular": modular, "rational": rational}


def check_ports_and_fourier(rng):
    ports = []
    for n in (8, 12, 16, 32):
        size = n + 7
        a = base_matrix(size, "tridiagonal_plus_rank1", rng)
        ai = inv(a)
        h = qsep(a)
        for trial in range(10):
            inputs = rng.sample(range(size), n)
            outputs = rng.sample(range(size), n)
            split = sorted(inputs)[n // 2 - 1] + 1
            il = [i for i, pos in enumerate(inputs) if pos < split]
            ir = [i for i, pos in enumerate(inputs) if pos >= split]
            ol = [i for i, pos in enumerate(outputs) if pos < split]
            ore = [i for i, pos in enumerate(outputs) if pos >= split]
            value = sub(ai, outputs, inputs)
            ranks = [rank(sub(value, ol, ir)), rank(sub(value, ore, il))]
            assert max(ranks) <= h
            assert max(len(ol) * len(ir), len(ore) * len(il)) >= (n * n) // 4
            ports.append({"n": n, "system_size": size, "h": h,
                          "ports_left": [len(il), len(ol)], "ranks": ranks})
    fourier = []
    for n in (4, 8, 16, 32, 64):
        root = pow(3, (P - 1) // n, P)
        powers = [pow(root, j, P) for j in range(n)]
        for trial in range(25):
            rows = rng.sample(range(n), n // 2)
            cols = rng.sample(range(n), n - n // 2)
            matrix = [[powers[(r * c) % n] for c in cols] for r in rows]
            r = rank(matrix)
            lower = (len(rows) * len(cols) + n - 1) // n
            assert r >= lower
            gains_r = [rng.randrange(1, P) for _ in rows]
            gains_c = [rng.randrange(1, P) for _ in cols]
            scaled = [[gains_r[i] * v * gains_c[j] % P for j, v in enumerate(row)]
                      for i, row in enumerate(matrix)]
            assert rank(scaled) == r
            fourier.append({"n": n, "rank_mod_p": r, "lower_bound": lower})
    return {"arbitrary_ports": ports, "scaled_permuted_fourier_cuts": fourier}


def signal_edges(n, ranks, shuffles):
    # A separate graph construction from the documented recurrences.
    infinity = 10 ** 9
    edges = {}
    def connect(u, v, cap=infinity):
        assert (u, v) not in edges
        edges[u, v] = cap
    def port(s, kind, j, cap):
        connect((s, kind, j, "i"), (s, kind, j, "o"), cap)
    for s, width in enumerate(ranks):
        for j in range(n):
            port(s, "x", j, 1)
            port(s, "y", j, 1)
            connect((s, "x", j, "o"), (s, "y", j, "i"))
        for j in range(1, n):
            port(s, "f", j, width)
            connect((s, "x", j - 1, "o"), (s, "f", j, "i"))
            connect((s, "f", j, "o"), (s, "y", j, "i"))
            if j > 1:
                connect((s, "f", j - 1, "o"), (s, "f", j, "i"))
        for j in range(n - 1):
            port(s, "b", j, width)
            connect((s, "x", j + 1, "o"), (s, "b", j, "i"))
            connect((s, "b", j, "o"), (s, "y", j, "i"))
            if j < n - 2:
                connect((s, "b", j + 1, "o"), (s, "b", j, "i"))
    for s, permutation in enumerate(shuffles):
        assert sorted(permutation) == list(range(n))
        for destination, origin in enumerate(permutation):
            connect((s, "y", origin, "o"), (s + 1, "x", destination, "i"))
    return edges


def maxflow(edges, source, sink):
    # Independent integer Edmonds-Karp, used only on this small certificate.
    residual = {}
    neighbours = {}
    for (u, v), cap in edges.items():
        residual[u, v] = residual.get((u, v), 0) + cap
        residual.setdefault((v, u), 0)
        neighbours.setdefault(u, []).append(v)
        neighbours.setdefault(v, []).append(u)
    total = 0
    while True:
        previous = {source: None}
        queue = deque([source])
        while queue and sink not in previous:
            u = queue.popleft()
            for v in neighbours[u]:
                if v not in previous and residual[u, v]:
                    previous[v] = u
                    queue.append(v)
        if sink not in previous:
            return total
        amount = 10 ** 30
        v = sink
        while previous[v] is not None:
            u = previous[v]
            amount = min(amount, residual[u, v])
            v = u
        v = sink
        while previous[v] is not None:
            u = previous[v]
            residual[u, v] -= amount
            residual[v, u] += amount
            v = u
        total += amount


def check_scan(certificate):
    obj = json.loads(certificate.read_text())
    n = obj["n"]
    assert n == 64 and obj["stage_ranks"] == [1, 1]
    permutation = obj["shuffle_stage_2_to_1"]
    rr, cc = obj["R_stage2"], obj["C_stage1"]
    edges = signal_edges(n, [1, 1], [permutation])
    source, sink = ("SRC",), ("SINK",)
    for c in cc:
        edges[source, (0, "x", c, "i")] = 10 ** 9
    for r in rr:
        edges[(1, "y", r, "o"), sink] = 10 ** 9
    nodes = {u for edge in edges for u in edge}
    left = {tuple(x) for x in obj["network_source_partition"]}
    assert len(left) == len(obj["network_source_partition"])
    assert left <= nodes and source in left and sink not in left
    crossing = {(u, v): cap for (u, v), cap in edges.items() if u in left and v not in left}
    claimed = {(tuple(e["tail"]), tuple(e["head"])): e["capacity"]
               for e in obj["network_mincut_crossing_edges"]}
    assert crossing == claimed
    capacity = sum(crossing.values())
    assert capacity == 16
    flow = maxflow(edges, source, sink)
    assert flow == capacity
    bitrev = lambda k: int(format(k, "06b")[::-1], 2)
    physical_rows = [bitrev(k) for k in rr]
    physical_cols = [bitrev(k) for k in cc]
    minor_rows = obj["nonzero_17_minor_physical_rows"]
    minor_cols = obj["nonzero_17_minor_physical_cols"]
    assert len(set(minor_rows)) == len(set(minor_cols)) == 17
    assert set(minor_rows) <= set(physical_rows)
    assert set(minor_cols) <= set(physical_cols)
    fields = []
    for record in obj["finite_fields"]:
        p, z = record["p"], record["root"]
        assert p > 2 and all(p % d for d in range(2, int(p ** 0.5) + 1))
        assert pow(z, 64, p) == 1 and pow(z, 32, p) == p - 1
        matrix = [[pow(z, i * j, p) for j in minor_cols] for i in minor_rows]
        det = determinant(matrix, p)
        full_rank = rank([[pow(z, i * j, p) for j in physical_cols]
                          for i in physical_rows], p)
        assert det == record["shared_minor_det"] != 0
        assert full_rank == record["rank"] == 17
        fields.append({"prime": p, "determinant": det,
                       "full_rectangle_rank_mod_p": full_rank})
    rset, cset = set(rr), set(cc)
    br = sum((j in rset) != (j + 1 in rset) for j in range(n - 1))
    bc = sum((j in cset) != (j + 1 in cset) for j in range(n - 1))
    overlap = len({permutation[j] for j in rr} & cset)
    assert (br, bc, overlap) == (4, 4, 9)
    return {"n": n, "graph_nodes": len(nodes), "graph_edges": len(edges),
            "cut_capacity": capacity, "independent_maxflow": flow,
            "old_interval_bound": br + bc + overlap,
            "fourier_minor_size": 17, "fields": fields,
            "uploaded_code_executed": False}


def check_actual_networks(rng):
    records = []
    for n in (8, 12):
        for stages in (2, 3):
            for width in (1, 2):
                matrices = []
                for _ in range(stages):
                    a = scale(eye(n), rng.randrange(1, 20))
                    for component in range(width):
                        for upper in (False, True):
                            u = [rng.randrange(1, 20) for _ in range(n)]
                            v = [rng.randrange(1, 20) for _ in range(n)]
                            transition = [rng.randrange(1, 20) for _ in range(n)]
                            for j in range(n):
                                running = v[j]
                                for i in range(j + 1, n):
                                    row, col = (j, i) if upper else (i, j)
                                    a[row][col] = (a[row][col] + u[i] * running) % P
                                    running = running * transition[i] % P
                    assert qsep(a) <= width
                    matrices.append(a)
                shuffles = [rng.sample(range(n), n) for _ in range(stages - 1)]
                value = matrices[0]
                for index in range(1, stages):
                    shuffled = [value[j] for j in shuffles[index - 1]]
                    value = mul(matrices[index], shuffled)
                base_edges = signal_edges(n, [width] * stages, shuffles)
                for trial in range(5):
                    rr = rng.sample(range(n), rng.randrange(1, n + 1))
                    cc = rng.sample(range(n), rng.randrange(1, n + 1))
                    edges = dict(base_edges)
                    for c in cc:
                        edges[("SRC",), (0, "x", c, "i")] = 10 ** 9
                    for r in rr:
                        edges[(stages - 1, "y", r, "o"), ("SINK",)] = 10 ** 9
                    flow = maxflow(edges, ("SRC",), ("SINK",))
                    actual = rank(sub(value, rr, cc))
                    assert actual <= flow
                    records.append({"n": n, "stages": stages, "width": width,
                                    "rectangle": [len(rr), len(cc)],
                                    "actual_rank": actual, "maxflow": flow})
    return records


def check_chirp_polynomial(rng):
    p = 2013265921
    records = []
    for n in (2, 3, 4, 5, 6, 8, 10, 15, 16, 30, 32, 64):
        assert (p - 1) % (2 * n) == 0
        zeta = pow(31, (p - 1) // (2 * n), p)
        assert pow(zeta, n, p) == p - 1
        s = 1 - n % 2
        coefficients = [pow(zeta, (-j * j + s * j) % (2 * n), p)
                        for j in range(n)]
        left = [pow(zeta, (k * k - s * k) % (2 * n), p) for k in range(n)]
        right = [pow(zeta, (j * j + s * j) % (2 * n), p) for j in range(n)]
        matrix = [[0] * n for _ in range(n)]
        # Assemble the polynomial using the actual signed-cycle power action,
        # rather than filling the claimed c_(k-j) formula.
        for degree, coefficient in enumerate(coefficients):
            for j in range(n):
                k = j + degree
                matrix[k % n][j] = (coefficient if k < n else -coefficient) % p
        dressed = [[left[k] * matrix[k][j] * right[j] % p for j in range(n)]
                   for k in range(n)]
        expected = [[pow(zeta, 2 * k * j, p) for j in range(n)] for k in range(n)]
        assert dressed == expected
        for trial in range(3):
            x = [rng.randrange(p) for _ in range(n)]
            assert [sum(v * z for v, z in zip(row, x)) % p for row in dressed] == [
                sum(pow(zeta, 2 * k * j, p) * x[j] for j in range(n)) % p
                for k in range(n)]
        records.append({"n": n, "parity_shift": s, "degree": n - 1,
                        "all_entries_verified": n * n, "fresh_inputs": 3})
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan-certificate", type=Path,
                        default=HERE / "scan_certificate.json")
    args = parser.parse_args()
    rng = random.Random(140409102026)
    result = {"model": "exact modular and rational sanity checks; no complexity benchmark",
              "rational_and_inverse": check_inverse_and_rational(rng),
              "halfcycle": check_halfcycle(rng),
              "ports_and_permutations": check_ports_and_fourier(rng),
              "scan_certificate": check_scan(args.scan_certificate),
              "actual_scan_networks": check_actual_networks(rng),
              "chirp_polynomial": check_chirp_polynomial(rng)}
    (HERE / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    print("PASS: 72 rational-degree cases; 9 repeated-pole cancellations;")
    print("3 singular-principal controls; 56 modular and 10 rational fresh halfcycle inputs;")
    print("254 halfcycle basis columns; 40 arbitrary-port cases; 125 scaled Fourier cuts;")
    print("40 actual quasiseparable network minor checks;")
    print("12 all-entry signed-cycle chirp identities and 36 fresh-input checks;")
    print("independent scan cut=maxflow=16 < certified Fourier minor rank 17.")
    print(json.dumps(result["scan_certificate"], indent=2))


if __name__ == "__main__":
    main()
