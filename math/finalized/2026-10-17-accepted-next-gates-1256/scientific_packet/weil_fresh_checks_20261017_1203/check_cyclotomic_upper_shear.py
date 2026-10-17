#!/usr/bin/env python3
"""Fresh exact formula checker. Never imports or reads research modules.

Arithmetic is integer polynomial reduction modulo Phi_(p^k), with denominators
cleared in matrix identities. Only this newly authored file is executed.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path
from time import perf_counter


class Cyclotomic:
    def __init__(self, p, k):
        self.p, self.k, self.q = p, k, p ** k
        self.step = self.q // p
        self.degree = self.q - self.step
        self.zero = (0,) * self.degree
        self.one = (1,) + (0,) * (self.degree - 1)
        roots = []
        for e in range(self.q):
            v = [0] * self.degree
            if e < self.degree:
                v[e] = 1
            else:
                for j in range(p - 1):
                    v[e - self.degree + j * self.step] = -1
            roots.append(tuple(v))
        self.roots = tuple(roots)

    def root(self, e):
        return self.roots[e % self.q]

    def add(self, a, b):
        return tuple(x + y for x, y in zip(a, b))

    def scale(self, a, n):
        return tuple(n * x for x in a)

    def shift(self, a, e):
        e %= self.q
        if e == 0:
            return a
        out = [0] * self.degree
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(self.roots[(i + e) % self.q]):
                    if y:
                        out[j] += x * y
        return tuple(out)

    def mul(self, a, b):
        # Full polynomial multiplication and descending monic reduction.
        coeffs = [0] * (2 * self.degree - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    if y:
                        coeffs[i + j] += x * y
        for e in range(len(coeffs) - 1, self.degree - 1, -1):
            value = coeffs[e]
            if value:
                coeffs[e] = 0
                for j in range(self.p - 1):
                    coeffs[e - self.degree + j * self.step] -= value
        return tuple(coeffs[:self.degree])

    def sum(self, seq):
        v = [0] * self.degree
        for a in seq:
            for i, x in enumerate(a):
                v[i] += x
        return tuple(v)


def check_case(p, k):
    r = Cyclotomic(p, k)
    q, half = r.q, pow(2, -1, r.q)
    count = Counter()

    def check(ok, group, detail=None):
        count[group] += 1
        if not ok:
            raise AssertionError({"q": q, "group": group, "detail": detail})

    # Sanity controls for the exact quotient and two independent product routes.
    check(r.root(q) == r.one, "arithmetic_root_order")
    for e in range(1, q):
        check(r.root(e) != r.one, "arithmetic_root_order", e)
    for e in range(q):
        for f in range(q):
            check(r.mul(r.root(e), r.root(f)) == r.root(e + f),
                  "arithmetic_root_products", [e, f])
    check(r.sum(r.root(e) for e in range(q)) == r.zero,
          "arithmetic_orthogonality")

    def kernel_numerator(b, d):
        return r.sum(r.root(-b * z * z * half + d * z) for z in range(q))

    S = [[kernel_numerator(b, d) for d in range(q)] for b in range(q)]
    for d in range(q):
        check(S[0][d] == r.scale(r.one, q) if d == 0 else S[0][d] == r.zero,
              "identity_entries", d)

    supports = []
    for b in range(1, q):
        g = 1
        while b % (g * p) == 0:
            g *= p
        m, u = q // g, b // g
        inv2m, inv2um = pow(2, -1, m), pow(2 * u, -1, m)
        Gminus = r.sum(r.root(g * (-u * z * z * inv2m)) for z in range(m))
        Gplus = r.sum(r.root(g * (u * z * z * inv2m)) for z in range(m))
        check(Gminus != r.zero, "gauss_nonzero", b)
        check(r.mul(Gminus, Gplus) == r.scale(r.one, m),
              "gauss_product", b)
        for d in range(q):
            expected = r.zero if d % g else r.scale(
                r.shift(Gminus, g * (d // g) ** 2 * inv2um), g)
            check(S[b][d] == expected, "completed_square_numerators", [b, d])
            check((S[b][d] != r.zero) == (d % g == 0),
                  "support_numerators", [b, d])
        check(sum(v != r.zero for v in S[b]) == m, "support_row_count", b)
        ratio_exp = -g * pow(u, -1, m)
        check(r.mul(S[b][0], S[b][0]) == r.shift(
            r.mul(S[b][g], S[b][-g]), ratio_exp), "signed_cross_ratio", b)
        check(r.root(ratio_exp * m) == r.one, "core_order_divides_m", b)
        check(r.root(ratio_exp * (m // p)) != r.one,
              "core_order_exact_m", b)
        # The old positive-chirp operator has numerator S[-b].
        check(S[b] != S[(-b) % q], "wrong_positive_chirp_rejected", b)
        supports.append({"b": b, "g": g, "m": m, "u": u,
                         "cross_ratio_zeta_exponent": ratio_exp % q})

    # Equivalent to all displacement covariance entries by the written proof.
    # Do not multiply this actual count by the redundant x,a coordinates.
    for b in range(q):
        for c in range(q):
            for t in range(q):
                check(S[b][(t + b * c) % q] == r.shift(
                    S[b][t], c * t + b * c * c * half),
                      "weyl_reduced_exact_equalities", [b, c, t])

    for b in [-2 * q - 1, -q, -1, q, 2 * q + 1]:
        for d in range(q):
            check(kernel_numerator(b, d) == S[b % q][d],
                  "noncanonical_b_equalities", [b, d])

    # All additive group pairs for the smaller cases. For larger q, a stated
    # identity/generator/inverse pair set. The proof covers every b,c uniformly.
    if q <= 9:
        pairs = [(b, c) for b in range(q) for c in range(q)]
    else:
        pairs = sorted({(b, c % q) for b in range(q) for c in (0, 1, -b)})
    for b, c in pairs:
        for d in range(q):
            lhs = r.sum(r.mul(S[b][t], S[c][(d - t) % q]) for t in range(q))
            check(lhs == r.scale(S[(b + c) % q][d], q),
                  "additive_shear_convolution", [b, c, d])

    if q <= 9:
        F = [[r.root(x * y) for y in range(q)] for x in range(q)]
        Fminus = [[r.root(-x * y) for y in range(q)] for x in range(q)]
        for x in range(q):
            for y in range(q):
                got = r.sum(r.mul(Fminus[x][z], F[z][y]) for z in range(q))
                check(got == (r.scale(r.one, q) if x == y else r.zero),
                      "dense_fourier_inverse", [x, y])
        for b in range(q):
            CF = [[r.mul(r.root(-b * z * z * half), F[z][y])
                   for y in range(q)] for z in range(q)]
            for x in range(q):
                for y in range(q):
                    got = r.sum(r.mul(Fminus[x][z], CF[z][y]) for z in range(q))
                    check(got == S[b][(y - x) % q],
                          "dense_fourier_conjugation", [b, x, y])

    return {"p": p, "k": k, "q": q, "cyclotomic_degree": r.degree,
            "scalar_b_cases": q, "actual_assertions": sum(count.values()),
            "assertions_by_group": dict(sorted(count.items())),
            "direct_kernel_numerators": q * q,
            "implied_matrix_entries_via_circulant_identity": q ** 3,
            "additive_pair_count": len(pairs),
            "additive_pair_coverage": "all pairs" if q <= 9 else "c=0,1,-b, deduplicated",
            "signed_support_cases": supports}


def main():
    started = perf_counter()
    cases = [check_case(p, k) for p, k in
             [(3, 1), (5, 1), (7, 1), (3, 2), (11, 1), (13, 1), (5, 2), (3, 3)]]
    totals = Counter()
    for case in cases:
        totals.update(case["assertions_by_group"])
    result = {
        "status": "PASS", "arithmetic": "Z[X]/Phi_(p^k)(X), exact integer coefficients; denominators cleared",
        "independence": "New checker, standard library only; no supplied, historical or candidate code read, imported or executed by this checker",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Formula-only proof controls, not candidate implementation acceptance",
        "scalar_b_cases": sum(c["scalar_b_cases"] for c in cases),
        "actual_assertions": sum(totals.values()),
        "assertions_by_group": dict(sorted(totals.items())),
        "direct_kernel_numerators": sum(c["direct_kernel_numerators"] for c in cases),
        "implied_matrix_entries_via_circulant_identity": sum(c["implied_matrix_entries_via_circulant_identity"] for c in cases),
        "cases": cases, "elapsed_seconds": round(perf_counter() - started, 6),
        "not_run": ["13 corrected derivative test groups", "historical SL2/subgroup exhaustive suites",
                    "candidate or original module", "earlier bounded API"]
    }
    output = Path(__file__).with_name("EXACT_CHECK_RESULTS.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "cases"}, indent=2))


if __name__ == "__main__":
    main()
