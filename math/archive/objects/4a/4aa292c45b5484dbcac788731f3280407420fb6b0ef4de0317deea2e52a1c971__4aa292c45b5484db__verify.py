#!/usr/bin/env python3
"""Exact finite-field audits for Annihilator-Closed Fourier Feedback.

No faster FFT is implemented here. Dense Fourier matrices and Gaussian
elimination are independent test oracles, never claimed fast primitives.
The Green/Horner kernels have separately instrumented scalar operation counts.
Requires only Python's standard library. Run: python verify.py --output RESULTS.json
"""
from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

Matrix = list[list[int]]
Vector = list[int]
FIELDS = (65537, 998244353)


def eye(n: int) -> Matrix:
    return [[int(i == j) for j in range(n)] for i in range(n)]


def zeros(n: int) -> Matrix:
    return [[0] * n for _ in range(n)]


def add(a: Matrix, b: Matrix, p: int, sign: int = 1) -> Matrix:
    return [[(x + sign * y) % p for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a: Matrix, c: int, p: int) -> Matrix:
    return [[c * x % p for x in row] for row in a]


def mul(a: Matrix, b: Matrix, p: int) -> Matrix:
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) % p for col in bt] for row in a]


def mv(a: Matrix, x: Sequence[int], p: int) -> Vector:
    return [sum(u * v for u, v in zip(row, x)) % p for row in a]


def inv(a: Matrix, p: int) -> Matrix:
    n = len(a)
    aug = [list(row) + ident for row, ident in zip(a, eye(n))]
    for col in range(n):
        pivot = next((r for r in range(col, n) if aug[r][col] % p), None)
        if pivot is None:
            raise ValueError("singular test-oracle matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        z = pow(aug[col][col] % p, -1, p)
        aug[col] = [v * z % p for v in aug[col]]
        for r in range(n):
            if r != col and aug[r][col]:
                z = aug[r][col]
                aug[r] = [(x - z * y) % p for x, y in zip(aug[r], aug[col])]
    return [row[n:] for row in aug]


def rank(a: Matrix, p: int) -> int:
    if not a:
        return 0
    b = [row[:] for row in a]
    r = 0
    for col in range(len(b[0])):
        pivot = next((i for i in range(r, len(b)) if b[i][col] % p), None)
        if pivot is None:
            continue
        b[r], b[pivot] = b[pivot], b[r]
        z = pow(b[r][col] % p, -1, p)
        b[r] = [x * z % p for x in b[r]]
        for i in range(r + 1, len(b)):
            z = b[i][col]
            if z:
                b[i] = [(x - z * y) % p for x, y in zip(b[i], b[r])]
        r += 1
        if r == len(b):
            break
    return r


def root_of_unity(n: int, p: int) -> int:
    if n < 2 or n & (n - 1) or (p - 1) % n:
        raise ValueError("test roots require dyadic n >= 2 dividing p-1")
    w = pow(3, (p - 1) // n, p)
    if pow(w, n, p) != 1 or pow(w, n // 2, p) == 1:
        raise ValueError("3 did not yield a primitive root at this test length")
    return w


def fourier(n: int, p: int) -> Matrix:
    w = root_of_unity(n, p)
    return [[pow(w, i * j, p) for j in range(n)] for i in range(n)]


def shift_diagonal(n: int, p: int) -> tuple[Matrix, Matrix]:
    w = root_of_unity(n, p)
    s, d = zeros(n), zeros(n)
    for j in range(n):
        s[(j + 1) % n][j] = 1
        d[j][j] = pow(w, j, p)
    return s, d


def poly_matrix(coeff: Sequence[int], k: Matrix, p: int) -> Matrix:
    n = len(k)
    out = zeros(n)
    for c in reversed(coeff):
        out = add(mul(out, k, p), scale(eye(n), c, p), p)
    return out


def inverse_coefficients(mu: Sequence[int], p: int) -> Vector:
    """Coefficients of (mu(1)-mu(z))/((1-z)*mu(1)), ascending order."""
    if len(mu) < 2 or mu[-1] % p == 0:
        raise ValueError("annihilator must have positive stated degree")
    m = sum(mu) % p
    if m == 0:
        raise ValueError("resonance: mu(1)=0 does not certify invertibility")
    mi = pow(m, -1, p)
    suffix = 0
    q = [0] * (len(mu) - 1)
    for j in range(len(mu) - 1, 0, -1):
        suffix = (suffix + mu[j]) % p
        q[j - 1] = suffix * mi % p
    return q


def certificate(a: Matrix, b: Matrix, mu: Sequence[int], p: int) -> dict[str, bool]:
    n = len(a)
    s, d = shift_diagonal(n, p)
    k = mul(b, a, p)
    h = add(eye(n), k, p, -1)
    j = add(eye(n), mul(a, b, p), p, -1)
    cubic = add(mul(mul(h, d, p), b, p), mul(mul(b, s, p), j, p), p, -1)
    seed = mv(h, [1] * n, p) == [row[0] for row in b]
    mu_valid = len(mu) >= 2 and mu[-1] % p != 0
    closure = mu_valid and poly_matrix(mu, k, p) == zeros(n)
    nonresonant = mu_valid and sum(mu) % p != 0
    return {"cubic_phase": cubic == zeros(n), "seed": seed,
            "annihilator": closure, "nonresonant": nonresonant}


def dense_kernel(a: Matrix, b: Matrix, mu: Sequence[int], x: Sequence[int], p: int) -> Vector:
    q = inverse_coefficients(mu, p)
    u = mv(b, x, p)
    v = [q[-1] * z % p for z in u]
    for c in reversed(q[:-1]):
        v = mv(b, mv(a, v, p), p)
        v = [(z + c * t) % p for z, t in zip(v, u)]
    return v


@dataclass
class Counts:
    mul: int = 0
    add: int = 0
    inverse: int = 0

    def multiply(self, a: int, b: int, p: int) -> int:
        self.mul += 1
        return a * b % p

    def plus(self, a: int, b: int, p: int) -> int:
        self.add += 1
        return (a + b) % p

    def invert(self, a: int, p: int) -> int:
        self.inverse += 1
        return pow(a, -1, p)


class GreenPlan:
    """L (I-diag(weights) P_cycle)^-1 R with fully charged scalar scan.

    The cycle list c means (P z)[c[t]] = z[c[t+1]]. Individual zero
    weights are valid. Only product(weights)==1 is singular.
    Numeric parameter generation is NOT included in the scan setup counts.
    """
    def __init__(self, cycle: Sequence[int], weights: Sequence[int],
                 left: Sequence[int], right: Sequence[int], p: int):
        self.n = len(cycle)
        if self.n == 0 or any(len(x) != self.n for x in (weights, left, right)):
            raise ValueError("nonempty equal-length arrays required")
        seen = [False] * self.n
        for c in cycle:
            if not isinstance(c, int) or c < 0 or c >= self.n or seen[c]:
                raise ValueError("cycle must list every coordinate exactly once")
            seen[c] = True
        self.cycle, self.p = list(cycle), p
        self.a = [x % p for x in weights]
        self.left = [x % p for x in left]
        self.right = [x % p for x in right]
        self.prefix: Vector = []
        self.setup = Counts()
        total = 1
        for c in self.cycle:
            self.prefix.append(total)
            total = self.setup.multiply(total, self.a[c], p)
        denom = self.setup.plus(1, -total, p)
        if denom == 0:
            raise ValueError("singular Green cycle: product(weights)=1")
        self.denom_inv = self.setup.invert(denom, p)

    def apply(self, x: Sequence[int], count: Counts | None = None) -> Vector:
        if len(x) != self.n:
            raise ValueError("wrong vector length")
        c = count if count is not None else Counts()
        p = self.p
        v = [c.multiply(r, t, p) for r, t in zip(self.right, x)]
        total = 0
        for pref, index in zip(self.prefix, self.cycle):
            total = c.plus(total, c.multiply(pref, v[index], p), p)
        z = [0] * self.n
        z[self.cycle[0]] = c.multiply(total, self.denom_inv, p)
        nxt = z[self.cycle[0]]
        for t in range(self.n - 1, 0, -1):
            index = self.cycle[t]
            z[index] = c.plus(v[index], c.multiply(self.a[index], nxt, p), p)
            nxt = z[index]
        return [c.multiply(l, t, p) for l, t in zip(self.left, z)]

    def denominator(self) -> Matrix:
        out = eye(self.n)
        for t, index in enumerate(self.cycle):
            nxt = self.cycle[(t + 1) % self.n]
            out[index][nxt] = (out[index][nxt] - self.a[index]) % self.p
        return out

    def oracle_matrix(self) -> Matrix:
        out = inv(self.denominator(), self.p)
        return [[self.left[i] * out[i][j] * self.right[j] % self.p
                 for j in range(self.n)] for i in range(self.n)]


class PairPlan:
    def __init__(self, g0: GreenPlan, g1: GreenPlan):
        if (g0.n, g0.p) != (g1.n, g1.p):
            raise ValueError("incompatible Green plans")
        self.g0, self.g1, self.n, self.p = g0, g1, g0.n, g0.p

    def apply(self, x: Sequence[int], count: Counts | None = None) -> Vector:
        c = count if count is not None else Counts()
        v, w = self.g0.apply(x, c), self.g1.apply(x, c)
        return [c.plus(a, b, self.p) for a, b in zip(v, w)]

    def oracle_matrix(self) -> Matrix:
        return add(self.g0.oracle_matrix(), self.g1.oracle_matrix(), self.p)


def fast_polynomial_kernel(a: PairPlan, b: PairPlan, q: Sequence[int],
                           x: Sequence[int]) -> tuple[Vector, Counts]:
    """Evaluate p(BA)B x. This is an inverse ONLY with a valid annihilator."""
    if len(q) == 0 or (a.n, a.p) != (b.n, b.p):
        raise ValueError("nonempty polynomial and compatible operators required")
    c = Counts()
    u = b.apply(x, c)
    v = [c.multiply(q[-1], t, a.p) for t in u]
    for coeff in reversed(q[:-1]):
        v = b.apply(a.apply(v, c), c)
        v = [c.plus(z, c.multiply(coeff, t, a.p), a.p) for z, t in zip(v, u)]
    return v, c


def random_green(n: int, p: int, rng: random.Random, zero_edge: bool = False) -> GreenPlan:
    cycle = list(range(n))
    rng.shuffle(cycle)
    while True:
        weights = [rng.randrange(1, p) for _ in range(n)]
        if zero_edge:
            weights[rng.randrange(n)] = 0
        left = [rng.randrange(1, p) for _ in range(n)]
        right = [rng.randrange(1, p) for _ in range(n)]
        try:
            return GreenPlan(cycle, weights, left, right, p)
        except ValueError:
            continue


def random_pair(n: int, p: int, rng: random.Random) -> PairPlan:
    return PairPlan(random_green(n, p, rng), random_green(n, p, rng))


def basis(n: int, j: int) -> Vector:
    return [int(i == j) for i in range(n)]


def nilpotent(n: int, degree: int, p: int) -> Matrix:
    """Dense-looking similarity of block Jordan nilpotents. Exact degree=degree."""
    if not 1 <= degree <= n:
        raise ValueError("invalid nilpotency degree")
    j = zeros(n)
    for start in range(0, n, degree):
        for i in range(start, min(n, start + degree) - 1):
            j[i][i + 1] = 1
    g = [[int(i >= k) for k in range(n)] for i in range(n)]
    return mul(mul(g, j, p), inv(g, p), p)


def oracle_feedback(target: Matrix, k: Matrix, p: int) -> tuple[Matrix, Matrix]:
    """Uses a dense target oracle: algebra control, NOT candidate synthesis."""
    b = mul(add(eye(len(k)), k, p, -1), target, p)
    a = mul(inv(b, p), k, p)
    assert mul(b, a, p) == k
    return a, b


def test_oracle_fourier() -> dict:
    cases = vectors = entries = 0
    rng = random.Random(17731)
    details = []
    for p in FIELDS:
        for n in (2, 4, 8, 16, 32):
            f = fourier(n, p)
            for degree in sorted({1, min(2, n), min(3, n), min(5, n)}):
                k = nilpotent(n, degree, p)
                mu = [0] * degree + [1]
                a, b = oracle_feedback(f, k, p)
                assert all(certificate(a, b, mu, p).values())
                q = inverse_coefficients(mu, p)
                assert mul(add(eye(n), k, p, -1), poly_matrix(q, k, p), p) == eye(n)
                for x in [basis(n, j) for j in range(n)] + [[rng.randrange(p) for _ in range(n)] for _ in range(3)]:
                    assert dense_kernel(a, b, mu, x, p) == mv(f, x, p)
                    vectors += 1
                    entries += n
                cases += 1
                details.append({"p": p, "N": n, "degree": degree})
    return {"status": "pass", "cases": cases, "vectors": vectors,
            "output_entries": entries, "scope": "Dense Fourier-oracle-derived algebra controls; NOT cheap Fourier factorizations.",
            "details": details}


def test_negative_certificates() -> dict:
    cases = 0
    details = []
    for p in FIELDS:
        for n in (4, 8, 16, 32):
            k = nilpotent(n, 2, p)
            mu = [0, 0, 1]
            f = fourier(n, p)
            a, b = oracle_feedback(scale(f, 2, p), k, p)
            c = certificate(a, b, mu, p)
            assert c == {"cubic_phase": True, "seed": False, "annihilator": True, "nonresonant": True}
            cases += 1
            a, b = oracle_feedback(eye(n), k, p)
            c = certificate(a, b, mu, p)
            assert c["annihilator"] and c["nonresonant"] and not c["cubic_phase"]
            cases += 1
            a, b = oracle_feedback(f, k, p)
            bad = certificate(a, b, [1, 0, 1], p)
            assert bad["cubic_phase"] and bad["seed"] and not bad["annihilator"]
            cases += 1
            c = certificate(eye(n), zeros(n), [0, 1], p)
            assert c["cubic_phase"] and c["annihilator"] and not c["seed"]
            cases += 1
            c = certificate(eye(n), eye(n), [-1, 1], p)
            assert c["annihilator"] and not c["nonresonant"]
            try:
                inverse_coefficients([-1, 1], p)
            except ValueError:
                pass
            else:
                raise AssertionError("resonance was not rejected")
            cases += 1
            details.append({"p": p, "N": n, "rejected_types": ["scalar multiple of Fourier", "non-Fourier exact closure", "false annihilator", "zero input map", "resonant loop"]})
    return {"status": "pass", "rejected_cases": cases, "details": details}


def test_green() -> dict:
    rng = random.Random(819377)
    cases = vectors = entries = 0
    for p in FIELDS:
        for n in (2, 4, 8, 16, 32, 64, 128):
            for zero_edge in (False, True):
                g = random_green(n, p, rng, zero_edge)
                assert vars(g.setup) == {"mul": n, "add": 1, "inverse": 1}
                matrix = g.oracle_matrix()
                xs = [basis(n, j) for j in range(n)] if n <= 32 else []
                xs += [[rng.randrange(p) for _ in range(n)] for _ in range(4)]
                for x in xs:
                    count = Counts()
                    out = g.apply(x, count)
                    assert out == mv(matrix, x, p)
                    assert vars(count) == {"mul": 4 * n, "add": 2 * n - 1, "inverse": 0}
                    vectors += 1
                    entries += n
                cases += 1
    try:
        GreenPlan([0, 1], [1, 1], [1, 1], [1, 1], FIELDS[0])
    except ValueError:
        pass
    else:
        raise AssertionError("singular Green cycle accepted")
    return {"status": "pass", "plans": cases, "vectors": vectors,
            "output_entries": entries, "includes_zero_weights": True,
            "setup_and_apply_operation_counts": "exactly checked"}


def test_polynomial_kernel() -> dict:
    rng = random.Random(61321)
    cases = 0
    sample_counts = []
    for p in FIELDS:
        for n in (4, 8, 16, 32):
            a, b = random_pair(n, p, rng), random_pair(n, p, rng)
            am, bm = a.oracle_matrix(), b.oracle_matrix()
            k = mul(bm, am, p)
            for d in (1, 2, 3, 5):
                q = [rng.randrange(1, p) for _ in range(d)]
                oracle = mul(poly_matrix(q, k, p), bm, p)
                for _ in range(3):
                    x = [rng.randrange(p) for _ in range(n)]
                    y, counts = fast_polynomial_kernel(a, b, q, x)
                    assert y == mv(oracle, x, p)
                    expected = {"mul": (17 * d - 8) * n,
                                "add": (11 * d - 6) * n - 4 * d + 2, "inverse": 0}
                    assert vars(counts) == expected
                    cases += 1
                sample_counts.append({"p": p, "N": n, "degree": d, **vars(counts)})
    return {"status": "pass", "vectors": cases,
            "scope": "Checks polynomial action and costs only; random loop is NOT asserted to have this annihilator or to be Fourier.",
            "sample_counts": sample_counts}


def test_fullrank_short_closure() -> dict:
    rng = random.Random(7719)
    cases = 0
    for p in FIELDS:
        for n in (4, 8, 16, 32):
            g = random_green(n, p, rng)
            b = g.oracle_matrix()
            a = scale(inv(b, p), 2, p)
            k = mul(b, a, p)
            assert k == scale(eye(n), 2, p)
            mu = [-2, 1]
            c = certificate(a, b, mu, p)
            assert c["annihilator"] and c["nonresonant"]
            assert not all(c.values())
            t = mul(poly_matrix(inverse_coefficients(mu, p), k, p), b, p)
            assert rank(t, p) == n
            assert t != fourier(n, p)
            cases += 1
    return {"status": "pass", "cases": cases,
            "scope": "Full rank and degree-one closure coexist, but do not imply Fourier phases."}


def test_random_minimal_degree() -> dict:
    rng = random.Random(177130)
    details = []
    for p in FIELDS:
        for n in (4, 8, 16, 32):
            for repetition in range(5):
                a, b = random_pair(n, p, rng), random_pair(n, p, rng)
                am, bm = a.oracle_matrix(), b.oracle_matrix()
                k = mul(bm, am, p)
                columns = []
                v = basis(n, 0)
                for _ in range(n):
                    columns.append(v)
                    v = mv(k, v, p)
                krylov = [list(row) for row in zip(*columns)]
                kr = rank(krylov, p)
                # rank N gives lower bound N on minimal-polynomial degree;
                # Cayley-Hamilton supplies the matching upper bound.
                c = certificate(am, bm, [0, 1], p)
                details.append({"p": p, "N": n, "repetition": repetition,
                                "krylov_rank": kr, "minimal_degree_N_certified": kr == n,
                                "cubic_phase": c["cubic_phase"], "seed": c["seed"]})
    return {"status": "completed", "cases": len(details),
            "full_degree_N_certificates": sum(x["minimal_degree_N_certified"] for x in details),
            "scope": "Exact finite samples, NOT an impossibility theorem for designed parameters.",
            "details": details}



def test_cubic_residual_and_rank() -> dict:
    rng = random.Random(71873)
    cases = singular_b = 0
    for p in FIELDS:
        for n in (4, 8, 16, 32):
            for repetition in range(4):
                a = [[rng.randrange(p) for _ in range(n)] for _ in range(n)]
                b = [[rng.randrange(p) for _ in range(n)] for _ in range(n)]
                if repetition % 2 == 0:
                    b[-1] = b[0][:]
                    singular_b += 1
                h = add(eye(n), mul(b, a, p), p, -1)
                try:
                    hinv = inv(h, p)
                except ValueError:
                    # Deterministic sample retry with A=0 retains singular B coverage.
                    a = zeros(n)
                    h = eye(n)
                    hinv = eye(n)
                j = add(eye(n), mul(a, b, p), p, -1)
                t = mul(hinv, b, p)
                ss, dd = shift_diagonal(n, p)
                residual = add(mul(mul(h, dd, p), b, p), mul(mul(b, ss, p), j, p), p, -1)
                dt_minus_ts = add(mul(dd, t, p), mul(t, ss, p), p, -1)
                assert residual == mul(mul(h, dt_minus_ts, p), j, p)
                assert mul(j, add(eye(n), mul(mul(a, hinv, p), b, p), p), p) == eye(n)
                assert rank(t, p) == rank(b, p)
                seed_residual = [(z - row[0]) % p for z, row in zip(mv(h, [1] * n, p), b)]
                assert seed_residual == mv(h, [(1 - row[0]) % p for row in t], p)
                cases += 1
    return {"status": "pass", "cases": cases, "singular_B_cases": singular_b,
            "scope": "Cubic residual identity and rank preservation, including singular B; not candidate synthesis."}


def test_generic_degree_witness() -> dict:
    rng = random.Random(88573)
    cases = 0
    for p in FIELDS:
        half = pow(2, -1, p)
        for n in (4, 8, 16, 32, 64):
            orders = [list(range(n)) for _ in range(4)]
            for order in orders:
                rng.shuffle(order)
            ds = list(range(2, n + 2))
            a = PairPlan(GreenPlan(orders[0], [0]*n, [half]*n, [1]*n, p),
                         GreenPlan(orders[1], [0]*n, [half]*n, [1]*n, p))
            b = PairPlan(GreenPlan(orders[2], [0]*n, [v*half % p for v in ds], [1]*n, p),
                         GreenPlan(orders[3], [0]*n, [v*half % p for v in ds], [1]*n, p))
            k = mul(b.oracle_matrix(), a.oracle_matrix(), p)
            assert k == [[ds[i] if i == j else 0 for j in range(n)] for i in range(n)]
            columns = []
            v = [1] * n
            for _ in range(n):
                columns.append(v)
                v = mv(k, v, p)
            assert rank([list(row) for row in zip(*columns)], p) == n
            cases += 1
    return {"status": "pass", "cases": cases,
            "scope": "Explicit Vandermonde witness for the generic-degree-N theorem for any fixed four cycle orders."}


def test_pure_feedback_obstruction() -> dict:
    rng = random.Random(631)
    details = []
    for p in FIELDS:
        for n in (16, 32, 64, 128):
            finv = inv(fourier(n, p), p)
            for repetition in range(3):
                pg = random_green(n, p, rng)
                qg = random_green(n, p, rng)
                # The no-go proof uses the denominators, not endpoint-scaled maps.
                pm, qm = pg.denominator(), qg.denominator()
                lhs = mul(pm, finv, p)
                rhs = add(mul(pm, qm, p), eye(n), p, -1)
                lhs_min = min(sum(z != 0 for z in row) for row in lhs)
                rhs_max = max(sum(z != 0 for z in row) for row in rhs)
                assert lhs_min >= (n + 1) // 2 and rhs_max <= 4 and lhs != rhs
                details.append({"p": p, "N": n, "repetition": repetition,
                                "min_support_P_Finverse": lhs_min,
                                "max_support_PQ_minus_I": rhs_max})
    return {"status": "pass", "cases": len(details), "details": details,
            "scope": "Independent arithmetic checks of a support obstruction proved in THEORY.md."}


def run_all() -> dict:
    tests = [
        ("oracle_fourier_controls", test_oracle_fourier),
        ("negative_certificates", test_negative_certificates),
        ("green_scan", test_green),
        ("paired_green_polynomial_kernel", test_polynomial_kernel),
        ("fullrank_short_closure_nonfourier", test_fullrank_short_closure),
        ("random_paired_loop_minimal_degree", test_random_minimal_degree),
        ("pure_green_feedback_obstruction", test_pure_feedback_obstruction),
        ("cubic_residual_and_rank", test_cubic_residual_and_rank),
        ("generic_degree_witness", test_generic_degree_witness),
    ]
    out = {"theory": "Annihilator-Closed Fourier Feedback", "date": "2026-10-10",
           "status": "Conditional execution theorem and candidate architecture; no universal fast Fourier construction.",
           "arithmetic": "exact modular arithmetic", "fields": list(FIELDS), "tests": {}}
    for name, function in tests:
        result = function()
        out["tests"][name] = result
        print(name + ": " + result["status"], flush=True)
    out["groups_completed"] = len(tests)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("RESULTS.json"))
    args = parser.parse_args()
    results = run_all()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print("Recorded exact results: " + str(args.output), flush=True)


if __name__ == "__main__":
    main()
