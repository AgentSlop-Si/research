#!/usr/bin/env python3
"""Fresh standard-library checks for the effective positive-sign cutoff.

This file does not import or execute historical research code. The accepted
sources are read only as inert bytes for SHA-256 verification. The checks are
small algebraic/combinatorial controls, not a new finite-N target enumeration.
"""
from hashlib import sha256
from itertools import product
from math import comb, factorial
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "source_inputs"
if not SOURCE.is_dir():
    SOURCE = HERE.parent / "coverage_audit_first89" / "source_bytes"
INPUTS = [
    ("8fcf5b11cd161e33b8fcab05acae7bf1f17d0f6775b9d2cca6c8f3807b1ea82f",
     "REVIEW.md"),
    ("aa91fdec5f08cc03e33652869d41be9f9a53bf3c37838c2d5f8d58532dd54586",
     "ACCEPTED_TWO_GREEN_EXCLUSION.md"),
]


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def mul(a, b):
    # Exact arithmetic in Z[t]/(1+t+t^2+t^3+t^4).
    out = [0] * 7
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    for k in range(6, 3, -1):
        c = out[k]
        out[k] = 0
        for d in range(1, 5):
            out[k - d] -= c
    return tuple(out[:4])


ONE = (1, 0, 0, 0)
ZERO = (0, 0, 0, 0)
ETA = (0, 1, 0, 0)


def epow(k):
    ans = ONE
    for _ in range(k % 5):
        ans = mul(ans, ETA)
    return ans


def polyadd(a, b):
    out = dict(a)
    for monomial, coefficient in b.items():
        out[monomial] = out.get(monomial, 0) + coefficient
    return {k: v for k, v in out.items() if v}


def polyscale(c, a):
    return {k: c * v for k, v in a.items() if c * v}


def polymul(a, b):
    out = {}
    for (ag, ax), av in a.items():
        for (bg, bx), bv in b.items():
            monomial = (ag + bg, ax + bx)
            out[monomial] = out.get(monomial, 0) + av * bv
    return {k: v for k, v in out.items() if v}


def evaluate(poly, g, x):
    return sum(c * g ** eg * x ** ex for (eg, ex), c in poly.items())


def main():
    report = {}
    hashes = {}
    for digest, basename in INPUTS:
        filename = f"{digest}__{basename}"
        observed = sha256((SOURCE / filename).read_bytes()).hexdigest()
        assert observed == digest, (filename, observed)
        hashes[filename] = observed
    report["accepted_source_hashes"] = hashes

    # All four primitive embeddings, without floating-point approximations.
    anchors = []
    scalar_norm = ONE
    g_norm = ONE
    entry_checks = 0
    for a in range(1, 5):
        assert epow(5 * a) == ONE and epow(a) != ONE
        g0 = add(ONE, scale(2, add(epow(2 * a), epow(3 * a))))
        assert mul(g0, g0) == scale(5, ONE)
        cube = mul(mul(g0, g0), g0)
        assert cube == scale(5, g0)
        scalar = add(ONE, scale(5, g0))
        assert scalar != ZERO
        g_norm = mul(g_norm, g0)
        scalar_norm = mul(scalar_norm, scalar)
        for i, j in product(range(5), repeat=2):
            F = epow(a * i * j)
            C = epow(-3 * a * (i + j) ** 2)
            diag = epow(-3 * a * i ** 2) if i == j else ZERO
            H = add(add(F, scale(-1, mul(g0, C))), mul(cube, diag))
            anchored = add(add(F, scale(-1, mul(g0, C))),
                           scale(5, mul(g0, diag)))
            assert H == anchored
            entry_checks += 1
        anchors.append({"embedding_exponent": a, "g0": g0,
                        "anchor_scalar": scalar})
    assert g_norm == scale(25, ONE)
    assert scalar_norm == scale(15376, ONE)
    report["cyclotomic"] = {"embeddings": anchors,
                            "anchor_entry_checks": entry_checks,
                            "norm_g0": 25, "norm_anchor_scalar": 15376}

    # Every zero/nonzero direction-coordinate pattern has a standard chart.
    chart_bits = set(product((0, 1), repeat=10))
    assert len(chart_bits) == 1024
    status_patterns = 0
    statuses = ((0, 1), (1, 0), (1, 1))
    for pairs in product(statuses, repeat=10):
        selected = tuple(0 if pair[0] else 1 for pair in pairs)
        assert selected in chart_bits
        assert all(pair[pick] for pair, pick in zip(pairs, selected))
        status_patterns += 1
    assert status_patterns == 3 ** 10
    assert factorial(4) ** 2 == 576
    # For a nonzero 11-row augmented minor, all ten direction weights
    # are nonnegative and each side has degree 11-5=6.
    positive_counts = [counts for counts in product(range(1, 8), repeat=5)
                       if sum(counts) == 11]
    assert len(positive_counts) == comb(10, 4)
    for counts in positive_counts:
        weights = [x - 1 for x in counts]
        assert min(weights) >= 0 and sum(weights) == 6
    report["coverage"] = {"charts": 1024, "order_pairs": 576,
                          "coordinate_status_patterns": status_patterns,
                          "possible_positive_index_count_vectors": len(positive_counts),
                          "row_degree": 6, "column_degree": 6}

    Hstar = 12 * factorial(11)
    L = Hstar ** 3
    D = 36 ** 10
    R = comb(D + 10, 10)
    assert Hstar == 479001600
    assert L == 109903340320478724096000000
    assert L < 2 ** 87
    assert D == 3656158440062976
    assert D + 10 < 2 ** 52
    assert R <= (D + 10) ** 10 < 2 ** 520
    # R! <= R^R, so log2(R! L^R) < (520+87)*2^520.
    assert 607 * 2 ** 520 < 2 ** 530
    # (1+A^4)^2 < 2^(2^533+2) < 2^(2^534).
    assert 2 ** 533 + 2 < 2 ** 534
    # No positive degree after cubing equals 2.
    assert all(3 * d != 2 and 3 * d <= 36 for d in range(1, 13))
    report["bound_constants"] = {
        "D": D, "R": str(R), "R_bit_length": R.bit_length(),
        "Hstar": Hstar, "L": L, "L_bit_length": L.bit_length(),
        "cutoff": "2^(2^534)", "all_integer_inequalities": True}

    # Fresh overdetermined coefficient-matrix control for the minor identity.
    # f1=x+x^2, f2=x+x^2-g. Rows are 1,x,x^2; the two columns
    # are independent over Q(g). Select rows 1,x: Q=[[0,-g],[1,1]],
    # det Q=g and adj(Q)*(1,0)^T=(1,-1)^T.
    f1 = {(0, 1): 1, (0, 2): 1}
    f2 = {(0, 1): 1, (0, 2): 1, (1, 0): -1}
    gpoly = {(1, 0): 1}
    assert polyadd(f1, polyscale(-1, f2)) == gpoly
    # Check all rows, including the row omitted from Q, symbolically.
    column_one = [{}, {(0, 0): 1}, {(0, 0): 1}]
    column_two = [polyscale(-1, gpoly), {(0, 0): 1}, {(0, 0): 1}]
    expected_rows = [gpoly, {}, {}]
    assert [polyadd(a, polyscale(-1, b)) for a, b in
            zip(column_one, column_two)] == expected_rows
    # At the determinant's zero specialization the equations do have roots,
    # showing that invertibility at specialization is neither used nor needed.
    assert evaluate(f1, 0, 0) == evaluate(f2, 0, 0) == 0
    assert evaluate(gpoly, 0, 0) == 0
    for g in (-7, -1, 1, 2, 11):
        for x in (-3, 0, 2):
            assert evaluate(f1, g, x) - evaluate(f2, g, x) == g
    report["macaulay_minor_control"] = {
        "symbolic_identity": "g=(x+x^2)-(x+x^2-g)",
        "all_three_rows_checked": True,
        "singular_specialization_checked": True}

    # A field norm example with an explicitly bounded conjugate polynomial.
    # Product over the four embeddings of (g-g0) is (g^2-5)^2.
    # Ring-valued polynomial coefficients, in increasing g degree.
    norm_polynomial = [ONE]
    for anchor in anchors:
        factor = [scale(-1, tuple(anchor["g0"])), ONE]
        out = [ZERO] * (len(norm_polynomial) + 1)
        for i, left in enumerate(norm_polynomial):
            for j, right in enumerate(factor):
                out[i + j] = add(out[i + j], mul(left, right))
        norm_polynomial = out
    assert norm_polynomial == [scale(25, ONE), ZERO, scale(-10, ONE), ZERO, ONE]
    report["field_norm_control"] = "Norm(g-g0)=g^4-10g^2+25"
    report["status"] = "PASS"
    destination = HERE / "ORIGINAL_CHECKS.json"
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "report": str(destination),
                      "checks": list(report)}, indent=2))


if __name__ == "__main__":
    main()
