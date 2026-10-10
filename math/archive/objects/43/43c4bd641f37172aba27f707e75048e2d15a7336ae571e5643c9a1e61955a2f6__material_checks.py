"""Exact rational witnesses for the conditioned-macro material review.

No numerical SVD, floating point, FFT oracle, or claimed #130 implementation.
The complex conditioning bounds follow from the proof in MATERIAL_REVIEW.md;
this script only evaluates the resulting rational lower bounds exactly.
"""
from fractions import Fraction as Q
import json
from pathlib import Path


def identity(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def zero(n):
    return [[Q(0) for _ in range(n)] for _ in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def negative(a):
    return [[-v for v in row] for row in a]


def multiply(a, b):
    assert len(a[0]) == len(b)
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def block(a, b, c, d):
    return [x + y for x, y in zip(a, b)] + [x + y for x, y in zip(c, d)]


def exchange(u):
    """Three transparent block additions; u must be orthogonal."""
    n = len(u)
    one, empty = identity(n), zero(n)
    assert multiply(transpose(u), u) == one
    a1 = block(one, empty, u, one)
    a2 = block(one, negative(transpose(u)), empty, one)
    word = multiply(a1, multiply(a2, a1))
    expected = block(empty, negative(transpose(u)), u, empty)
    assert word == expected
    assert multiply(transpose(word), word) == identity(2 * n)
    return word


def rational(value):
    value = Q(value)
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def matrix(a):
    return [[rational(v) for v in row] for row in a]


def diagonal_condition(entries):
    """Exact spectral condition for a nonzero real diagonal matrix."""
    magnitudes = [abs(Q(v)) for v in entries]
    assert min(magnitudes) > 0
    return max(magnitudes) / min(magnitudes)


def run():
    # A local scale has condition 1; identity padding exposes its scale.
    local = diagonal_condition([100, 100])
    padded = diagonal_condition([100, 100, 1, 1])
    padded_bound = max(Q(1), Q(100)) * max(Q(1), Q(1, 100))
    assert local == 1 and padded == padded_bound == 100

    # Reflection and rational rotation: orthogonal and noncommuting.
    u1 = [[Q(1), Q(0)], [Q(0), Q(-1)]]
    u2 = [[Q(3, 5), Q(-4, 5)], [Q(4, 5), Q(3, 5)]]
    assert multiply(u1, u2) != multiply(u2, u1)
    w1, w2 = exchange(u1), exchange(u2)
    one, empty = identity(2), zero(2)
    bank_permutation = block(empty, one, one, empty)
    second_orientation = multiply(bank_permutation, multiply(w2, bank_permutation))
    corrected = multiply(second_orientation, w1)
    incorrect = multiply(w2, w1)
    expected = multiply(u2, u1)
    expected_wrong = negative(multiply(transpose(u2), u1))
    assert [row[:2] for row in corrected[:2]] == expected
    assert [row[:2] for row in corrected[2:]] == zero(2)
    assert [row[:2] for row in incorrect[:2]] == expected_wrong != expected
    assert multiply(transpose(corrected), corrected) == identity(4)
    # All basis inputs are covered by comparing the complete first block column.
    witness = [[Q(1)], [Q(0)], [Q(0)], [Q(0)]]
    correct_witness = multiply(corrected, witness)
    wrong_witness = multiply(incorrect, witness)
    assert correct_witness != wrong_witness

    bounds = []
    for n in (8, 16, 32, 64, 128, 256):
        m = n // 8
        elementary = Q(n) * Q(14, 11) ** m
        am_gm = Q(n) * Q(7 * n, 22 * (m + 1)) ** m
        assert am_gm >= elementary > n
        bounds.append({
            "n": n, "m": m,
            "elementary_condition_lower_bound": rational(elementary),
            "am_gm_condition_lower_bound": rational(am_gm),
            "elementary_bound_floor": str(elementary.numerator // elementary.denominator),
            "am_gm_bound_floor": str(am_gm.numerator // am_gm.denominator),
        })
    result = {
        "status": "PASS",
        "arithmetic": "fractions.Fraction throughout all matrix witnesses and bounds",
        "padded_condition": {
            "local_diagonal": [100, 100], "ambient_diagonal": [100, 100, 1, 1],
            "local_condition": rational(local), "ambient_condition": rational(padded),
            "correct_padded_bound": rational(padded_bound),
        },
        "alternating_banks": {
            "u1": matrix(u1), "u2": matrix(u2), "noncommuting": True,
            "three_addition_identities_checked": 2,
            "correct_active_block": matrix(expected),
            "same_orientation_active_block": matrix(expected_wrong),
            "correct_e0_output": matrix(correct_witness),
            "wrong_e0_output": matrix(wrong_witness),
            "correct_full_state_orthogonal": True,
        },
        "canonical_root_middle_condition_bounds": bounds,
        "claim_boundary": (
            "The all-N complex condition inequalities are proved in MATERIAL_REVIEW.md. "
            "These exact rational evaluations are certificates of their stated values, "
            "not numerical estimates or a general FFT lower bound."
        ),
        "separate_source_test_run": {
            "command": "PYTHONDONTWRITEBYTECODE=1 python -m unittest -v",
            "tests": 2, "status": "PASS",
            "scope": "Source NumPy toy matrix tests; not re-executed by this exact script.",
        },
    }
    path = Path(__file__).with_name("material_certificates.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "rational_bound_cases": len(bounds),
                      "exchange_identities": 2, "output": str(path)}))


if __name__ == "__main__":
    run()
