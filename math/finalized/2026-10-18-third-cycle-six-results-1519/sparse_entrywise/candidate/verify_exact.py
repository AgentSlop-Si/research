#!/usr/bin/env python3
"""Fresh exact controls for entrywise Fourier-mask gap stability.

No earlier checker is imported or executed. SymPy handles exact algebraic
matrices and resultants. All trigonometric enclosures use integer intervals.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
from fractions import Fraction
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
FIX = 1 << 120


def floor_frac(x: Fraction) -> int:
    return x.numerator // x.denominator


def ceil_frac(x: Fraction) -> int:
    return -((-x.numerator) // x.denominator)


def atan_bounds(reciprocal: int, terms: int = 40):
    # An even number of terms ends with a negative term: lower partial sum.
    assert terms % 2 == 0
    s = sum((Fraction((-1) ** k, (2 * k + 1) * reciprocal ** (2 * k + 1))
             for k in range(terms)), Fraction(0))
    return s, s + Fraction(1, (2 * terms + 1) * reciprocal ** (2 * terms + 1))


a_lo, a_hi = atan_bounds(5)
b_lo, b_hi = atan_bounds(239)
pi_lo = 16 * a_lo - 4 * b_hi
pi_hi = 16 * a_hi - 4 * b_lo
PI = (floor_frac(pi_lo * FIX), ceil_frac(pi_hi * FIX))
assert 3 * FIX < PI[0] < PI[1] < 4 * FIX


def iadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def isub(a, b):
    return a[0] - b[1], a[1] - b[0]


def imul(a, b):
    products = [x * y for x in a for y in b]
    return min(products) // FIX, -((-max(products)) // FIX)


def idiv(a, positive_integer):
    assert positive_integer > 0
    return a[0] // positive_integer, -((-a[1]) // positive_integer)


def cos_interval(n, k):
    k %= n
    k = min(k, n - k)
    angle = idiv((2 * k * PI[0], 2 * k * PI[1]), n)
    angle2 = imul(angle, angle)
    term = (FIX, FIX)
    total = (FIX, FIX)
    for j in range(1, 33):
        term = idiv(imul(term, angle2), (2 * j - 1) * (2 * j))
        total = isub(total, term) if j % 2 else iadd(total, term)
    # Degree 65 Taylor polynomial has zero degree-65 coefficient. The
    # Lagrange remainder is at most |angle|^66/66!, bounded by next term.
    remainder = idiv(imul(term, angle2), 65 * 66)[1]
    return total[0] - remainder, total[1] + remainder


COS_CACHE = {}


def cos_table(n):
    if n not in COS_CACHE:
        COS_CACHE[n] = [cos_interval(n, k) for k in range(n)]
    return COS_CACHE[n]


def root_sum_norm2_interval(n, exponents):
    table = cos_table(n)
    lo = hi = len(exponents) * FIX
    for a, b in itertools.combinations(exponents, 2):
        c = table[(a - b) % n]
        lo += 2 * c[0]
        hi += 2 * c[1]
    return lo, hi


def sqrt_fraction_interval(x):
    assert x >= 0
    k = math.isqrt((x.numerator * FIX * FIX) // x.denominator)
    if k * k * x.denominator == x.numerator * FIX * FIX:
        return k, k
    return k, k + 1


def sx(x):
    return sp.simplify(sp.expand_complex(x))


def matrix_simplify(m):
    return m.applyfunc(sx)


def matrix_zero(m):
    return all(sx(x) == 0 for x in m)


def assert_matrix_eq(a, b):
    assert matrix_zero(a - b), (a - b)


def norm2_row(m, i):
    return sx(sum(m[i, j] * sp.conjugate(m[i, j]) for j in range(m.cols)))


def nonnegative(x):
    x = sx(x)
    return x.is_nonnegative is True


def principal_minors(m):
    assert_matrix_eq(m, m.conjugate().T)
    out = []
    for k in range(1, m.rows + 1):
        for indices in itertools.combinations(range(m.rows), k):
            det = sx(m.extract(indices, indices).det())
            out.append((indices, det))
    return out


def check_witness(name, F, B, s, rho2, require_bad=False, exact_rho=False):
    n = F.rows
    q = sp.Rational(s, n)
    a2 = 1 - q
    gap = rho2 - a2
    assert 0 <= gap < sp.Rational(1, n)
    assert B.det() != 0
    M = matrix_simplify(B.inv())
    E = matrix_simplify(M - F)
    H = matrix_simplify(rho2 * sp.eye(n) - E * E.conjugate().T)
    h_minors = principal_minors(H)
    assert all(nonnegative(v) for _, v in h_minors)
    if exact_rho:
        assert_matrix_eq(E * E.conjugate().T, rho2 * sp.eye(n))
    supports = [[j for j in range(n) if sx(B[i, j]) != 0] for i in range(n)]
    assert all(len(row) == s for row in supports)
    A = sp.Matrix(n, n, lambda r, c: F[r, c] if r in supports[c] else 0)
    C = F - A
    B0 = A.conjugate().T / q
    K = matrix_simplify(q * (B - B0))
    Z = matrix_simplify(C.conjugate().T * C - a2 * sp.eye(n))
    P = matrix_simplify(q * B * H * B.conjugate().T + K * K.conjugate().T)
    assert all(nonnegative(v) for _, v in principal_minors(P))
    U = matrix_simplify(q * gap * B * B.conjugate().T)
    assert_matrix_eq(Z, U - P + K * C + C.conjugate().T * K.conjugate().T)
    u2, k2 = [], []
    for i in range(n):
        bn = norm2_row(B, i)
        kn = norm2_row(K, i)
        dn = norm2_row(B - B0, i)
        assert sx(q * dn - (norm2_row(B * E, i) - a2 * bn)) == 0
        assert sx(P[i, i] - q * gap * bn) == 0
        assert sx(U[i, i] - P[i, i]) == 0
        assert sx(Z[i, i]) == 0
        assert sx(norm2_row(B0, i) - 1 / q) == 0
        assert nonnegative(q * gap * bn - kn)
        u2.append(sx(q * gap * bn))
        k2.append(kn)
    bad_entries = 0
    for i in range(n):
        for j in range(i + 1, n):
            zn = sx(Z[i, j] * sp.conjugate(Z[i, j]))
            pn = sx(P[i, j] * sp.conjugate(P[i, j]))
            un = sx(U[i, j] * sp.conjugate(U[i, j]))
            assert nonnegative(u2[i] * u2[j] - pn)
            assert nonnegative(u2[i] * u2[j] - un)
            rhs = 2 * sp.sqrt(u2[i] * u2[j]) + sp.sqrt(a2 * k2[i]) + sp.sqrt(a2 * k2[j])
            assert nonnegative(rhs ** 2 - zn)
            bad_entries += int(zn != 0)
    if require_bad:
        assert bad_entries > 0
    wrong_sign = U - P - K * C - C.conjugate().T * K.conjugate().T
    assert not matrix_zero(Z - wrong_sign)
    return {
        "name": name, "N": n, "s": s, "rho2_bound": str(rho2),
        "rho2_exact": exact_rho, "D": str(gap),
        "inverse_row_supports": [len(x) for x in supports],
        "H_principal_minors": [str(v) for _, v in h_minors],
        "bad_gram_pairs": bad_entries, "identities_passed": True,
        "wrong_cross_term_sign_rejected": True,
    }


def matrix_controls():
    I = sp.I
    w = -sp.Rational(1, 2) - I * sp.sqrt(3) / 2
    F3 = sp.Matrix(3, 3, lambda r, c: sp.expand(w ** ((r * c) % 3)) / sp.sqrt(3))
    phases = sp.diag(1, w, w)
    phase = sp.sqrt(3) / 2 - I / 2
    base = matrix_simplify(phase * phases / 2)
    rows = [check_witness("nonsharp_three_by_three", F3, matrix_simplify(base.inv()), 1,
                          sp.Rational(3, 4), require_bad=True, exact_rho=True)]
    scaled = matrix_simplify(sp.diag(1, sp.Rational(21, 20), sp.Rational(19, 20)) * base)
    rows.append(check_witness("nonuniform_nonsharp_three_by_three", F3, matrix_simplify(scaled.inv()), 1,
                              sp.Rational(4, 5), require_bad=True))
    bad = matrix_simplify(sp.diag(1, sp.Rational(11, 10), sp.Rational(9, 10)) * base)
    badE = bad - F3
    badH = matrix_simplify(sp.Rational(4, 5) * sp.eye(3) - badE * badE.conjugate().T)
    negative_minors = [(list(ix), str(v)) for ix, v in principal_minors(badH) if v.is_negative is True]
    assert negative_minors
    F4 = sp.Matrix(4, 4, lambda r, c: (-I) ** (r * c) / 2)
    for d in (1, 2):
        C = sp.zeros(4)
        m = 4 // d
        for t in range(m):
            for r in range(d * t, d * t + d):
                for c in [t + j * m for j in range(d)]:
                    C[r, c] = F4[r, c]
        q = sp.Rational(4 - d, 4)
        B0 = (F4 - C).conjugate().T / q
        B = matrix_simplify(sp.diag(1, sp.Rational(21, 20), 1, sp.Rational(19, 20)) * B0)
        rows.append(check_witness(f"perturbed_four_by_four_d{d}", F4, B, 4 - d,
                                  sp.Rational(d, 4) + sp.Rational(1, 10)))
    return {"witnesses": rows, "false_error_bound_negative_minors": negative_minors}


def cyclotomic_controls():
    x = sp.Symbol("x")
    rng = random.Random(202610181508)
    records, total, zeros, equalities = [], 0, 0, 0
    for n in range(3, 33):
        phi = sp.Poly(sp.cyclotomic_poly(n, x), x, domain=sp.QQ)
        degree = phi.degree()
        assert degree % 2 == 0
        patterns = [[0], [0, 1], [0, n // 2], [0, n // 3, 2 * n // 3],
                    [0, 1, 1], [0, 1, 2, 3], [0, 0, n - 1]]
        patterns += [[rng.randrange(n) for _ in range(t)] for t in (2, 3, 4) for _ in range(3)]
        nzeros = 0
        for exponents in patterns:
            total += 1
            t = len(exponents)
            P = sp.Poly(sum(x ** (k % n) for k in exponents), x, domain=sp.QQ).rem(phi)
            Pb = sp.Poly(sum(x ** ((-k) % n) for k in exponents), x, domain=sp.QQ).rem(phi)
            Q = (P * Pb).rem(phi)
            Qb = sp.Poly(sum(coeff * x ** ((-int(monom[0])) % n)
                             for monom, coeff in Q.terms()), x, domain=sp.QQ).rem(phi)
            assert Q == Qb
            norm = sp.resultant(phi.as_expr(), P.as_expr(), x)
            normb = sp.resultant(phi.as_expr(), Pb.as_expr(), x)
            normq = sp.resultant(phi.as_expr(), Q.as_expr(), x)
            assert norm == normb and normq == norm ** 2
            if P.is_zero:
                assert norm == 0
                zeros += 1
                nzeros += 1
                continue
            assert norm.is_Integer and 1 <= norm <= t ** degree
            threshold = sp.Rational(1, t ** (degree - 2))
            if (Q - sp.Poly(threshold, x, domain=sp.QQ)).is_zero:
                equalities += 1
            else:
                low, high = root_sum_norm2_interval(n, exponents)
                assert low * t ** (degree - 2) >= FIX, (n, exponents, low, high)
        records.append({"N": n, "phi": degree, "patterns": len(patterns), "zero_patterns": nzeros})
    return {"patterns": total, "zero_patterns": zeros, "exact_bound_equalities": equalities,
            "paired_norm_and_conjugation_passed": True, "dimensions": records}


def geometric_controls():
    dimensions = list(range(3, 91)) + [97, 98, 100, 127, 128, 160, 200, 256, 257, 512]
    records, triples, pairs = [], 0, 0
    for n in dimensions:
        table = cos_table(n)
        pair_count = 0
        for k in range(n):
            low, high = 2 * FIX + 2 * table[k][0], 2 * FIX + 2 * table[k][1]
            if n % 2 == 0 and 2 * k == n:
                assert low <= 0 <= high
                continue
            coefficient = 4 if n % 2 else 16
            assert low * n * n >= coefficient * FIX
            pair_count += 1
        pairs += pair_count
        triple_count, minimum = 0, None
        if n % 3:
            for k in range(n // 2 + 1):
                assert abs(3 * k - n) >= 1
            for a in range(n):
                for b in range(a, n):
                    low = 3 * FIX + 2 * (table[a][0] + table[b][0] + table[(a - b) % n][0])
                    assert low * n * n >= FIX, (n, a, b)
                    scaled = (low * n * n * 1_000_000) // FIX
                    minimum = scaled if minimum is None else min(minimum, scaled)
                    triple_count += 1
            triples += triple_count
        records.append({"N": n, "nonzero_pairs": pair_count, "triple_patterns": triple_count,
                        "certified_min_N2_norm2_lower_in_millionths": minimum})
    x = sp.Symbol("x")
    zero_negative_controls = []
    for n in (3, 6, 9, 12, 15, 30):
        P = sp.Poly(1 + x ** (n // 3) + x ** (2 * n // 3), x)
        assert P.rem(sp.Poly(sp.cyclotomic_poly(n, x), x)).is_zero
        zero_negative_controls.append(n)
    return {"exact_interval_scale_bits": 120, "pi_interval_width_fixed_units": PI[1] - PI[0],
            "cosine_taylor_degree": 65, "nonzero_pairs": pairs, "triple_patterns": triples,
            "divisible_by_three_zero_negative_controls": zero_negative_controls,
            "dimensions": records}


def rational_gap_controls():
    count = 0
    for n in range(3, 161):
        phi = int(sp.totient(n))
        assert phi % 2 == 0
        for s in range(1, n - 1):
            d = n - s
            a2, q = Fraction(d, n), Fraction(s, n)
            eta = Fraction(1, n * d ** (phi // 2 - 1))
            clean = eta * eta / (10 * a2)
            assert clean == Fraction(1, 10 * n * d ** (phi - 1))
            old = Fraction(s ** 6, 2 ** 22 * n ** 10 * d ** (2 * phi - 2))
            assert clean > old
            assert clean / old == Fraction(2 ** 22 * n ** 9 * d ** (phi - 1), 10 * s ** 6)
            assert eta <= Fraction(1, n)
            assert eta / a2 <= Fraction(1, 2)
            assert eta * eta / (a2 * q) <= Fraction(1, 2)
            denom_hi = sum([sqrt_fraction_interval(a2)[1],
                            sqrt_fraction_interval(a2 + 2 * eta)[1],
                            sqrt_fraction_interval(eta * eta / q)[1]])
            assert Fraction(denom_hi ** 2, FIX ** 2) < 10 * a2
            assert eta * eta / (4 * a2) < Fraction(1, n)
            count += 1
        if n % 2:
            eta = Fraction(2, n * n)
            assert eta <= Fraction(1, n)
            assert eta ** 2 / (10 * Fraction(2, n)) == Fraction(1, 5 * n ** 3)
        if n >= 4 and n % 3:
            eta = Fraction(1, n * n)
            assert eta ** 2 / (10 * Fraction(3, n)) == Fraction(1, 30 * n ** 3)
    # (1+3/sqrt(2))^2 < 10 is equivalent to 3*sqrt(2)<9/2.
    assert Fraction(18) < Fraction(81, 4)
    return {"budget_pairs": count, "max_N": 160, "all_formula_and_constant_checks_passed": True,
            "strict_improvement_checked": True}


def main():
    out = {"owner": "M-SPARSE-DEFECT", "exact_only": True, "imports_prior_checkers": False}
    for label, fn in [("matrix_controls", matrix_controls),
                      ("cyclotomic_controls", cyclotomic_controls),
                      ("geometric_controls", geometric_controls),
                      ("rational_gap_controls", rational_gap_controls)]:
        out[label] = fn()
        print(label, "PASS", flush=True)
    out["checker_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out["verdict"] = "PASS"
    (ROOT / "RESULTS.json").write_text(json.dumps(out, indent=2) + "\n")
    print("PASS", flush=True)


if __name__ == "__main__":
    main()
