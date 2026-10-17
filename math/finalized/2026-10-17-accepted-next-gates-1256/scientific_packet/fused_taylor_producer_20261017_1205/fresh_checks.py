"""Fresh exact controls for the streamed fused producer and linear-state rank.

No prior program is imported or executed. Python arithmetic is an oracle here,
not a timing or bit-cost model.
"""
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent
COUNTS = {"producer_cases": 0, "weight_checks": 0,
          "boundary_sequence_checks": 0, "rank_checks": 0,
          "minimal_state_checks": 0, "matrix_product_checks": 0}
MAX_TMP_BITS = 0


def advance(v, i, j, seed):
    # Current v is seed * binom(i, j), with binom(i,-1)=0.
    if j < 0 or i + 1 < j:
        return 0
    if i + 1 == j:
        return seed
    numerator = v * (i + 1)
    denominator = i + 1 - j
    assert denominator > 0 and numerator % denominator == 0
    return numerator // denominator


def fused(a, m, s):
    global MAX_TMP_BITS
    K = len(a)
    assert m >= 2 and K % s == 0
    p = (1 << m) - 1
    B = K // s
    H = m * s + K + 1
    L = K.bit_length()  # Exactly ceil(log2(K+1)) for integer K>=1.
    G = H + m + L + 3
    if s == K:
        # The scalar endpoint is a copy of the original binary input.
        return [sum(v << (m * i) for i, v in enumerate(a))]
    R = 1
    for _ in range(s):
        R = (R << m) - R
    ans = []
    for r in range(B):
        lo, hi = r * s - 1, (r + 1) * s - 1
        w = int(r == 0)
        left = int(lo == 0)
        right = R if hi == 0 else 0
        u = 0
        for i in range(K):
            direct_w = sum(math.comb(i, r * s + t) * p ** t
                           for t in range(s) if r * s + t <= i)
            assert w == direct_w
            COUNTS["weight_checks"] += 1
            assert left == (math.comb(i, lo) if 0 <= lo <= i else 0)
            assert right == (R * math.comb(i, hi) if hi <= i else 0)
            COUNTS["boundary_sequence_checks"] += 2
            u += a[i] * w
            assert 0 <= u < 1 << H
            if i < K - 1:
                shifted = w << m
                plus = shifted + left
                w = plus - right
                assert w >= 0
                candidates = [shifted, plus, left * (i + 1),
                              right * (i + 1), a[i] * direct_w, u]
                bits = max(v.bit_length() for v in candidates)
                MAX_TMP_BITS = max(MAX_TMP_BITS, bits)
                assert bits <= G
                left = advance(left, i, lo, 1)
                right = advance(right, i, hi, R)
        ans.append(u)
    return ans


def direct(a, m, s):
    p = (1 << m) - 1
    K = len(a)
    c = [sum(a[i] * math.comb(i, j) for i in range(j, K))
         for j in range(K)]
    return [sum(c[r * s + t] * p ** t for t in range(s))
            for r in range(K // s)]


def check_case(a, m, s):
    out = fused(a, m, s)
    assert out == direct(a, m, s)
    p = (1 << m) - 1
    X = sum(v << (m * i) for i, v in enumerate(a))
    assert X == sum(v * p ** (s * r) for r, v in enumerate(out))
    COUNTS["producer_cases"] += 1
    return out


def rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    h, w = len(a), len(a[0])
    row = 0
    for col in range(w):
        pivot = next((j for j in range(row, h) if a[j][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        z = a[row][col]
        a[row] = [x / z for x in a[row]]
        for j in range(row + 1, h):
            z = a[j][col]
            if z:
                a[j] = [x - z * y for x, y in zip(a[j], a[row])]
        row += 1
        if row == h:
            break
    return row


def observable_matrix(K, s, p, h):
    # Columns represent f_j on degree < K-h; rows E_s((1+z)^t F).
    n = K - h
    rows = []
    for t in range(h + 1):
        for r in range(K // s):
            rows.append([sum(math.comb(t, r * s + u - j) * p ** u
                             for u in range(s)
                             if 0 <= r * s + u - j <= t)
                         for j in range(n)])
    return rows


def pack_coeff(f, p, s):
    return [sum(f[r * s + t] * p ** t for t in range(s))
            for r in range(len(f) // s)]


def check_state(K, s, p, rng):
    q = K - s
    for _ in range(12):
        f = [rng.randint(-99, 99) for _ in range(K - 1)] + [0]
        last = sum(f[q + t] * p ** t for t in range(s))
        state = f[:q] + [last]
        new_f = [f[0]] + [f[j] + f[j - 1] for j in range(1, K)]
        new_last = (p + 1) * state[-1] + (f[q - 1] if q else 0)
        expected = new_f[:q] + [sum(new_f[q + t] * p ** t
                                   for t in range(s))]
        got = ([f[0]] + [f[j] + f[j - 1] for j in range(1, q)]
               if q else []) + [new_last]
        assert got == expected
        COUNTS["minimal_state_checks"] += 1


def main():
    rng = random.Random(202610171205)
    for m, K in [(2, 1), (2, 2), (2, 3), (2, 4), (3, 3)]:
        for s in range(1, K + 1):
            if K % s == 0:
                for a in itertools.product(range(1 << m), repeat=K):
                    check_case(a, m, s)
    for m in (2, 3, 4, 7, 13, 31):
        p = (1 << m) - 1
        for K in (2, 6, 12, 24, 35, 48):
            for s in range(1, K + 1):
                if K % s:
                    continue
                for a in ([0] * K, [p] * K,
                          [rng.randrange(p + 1) for _ in range(K)],
                          [p if i % 2 else 0 for i in range(K)]):
                    check_case(a, m, s)
    for K in range(1, 19):
        for s in range(1, K + 1):
            if K % s:
                continue
            for p in (3, 7, 15):
                for h in range(s):
                    observed = rank(observable_matrix(K, s, p, h))
                    target = K // s + (K // s - 1) * h
                    assert observed == target, (K, s, p, h, observed, target)
                    COUNTS["rank_checks"] += 1
                check_state(K, s, p, rng)
    for m in (2, 4, 7):
        for d in (1, 2, 3):
            for M in (2, 3, 4):
                K, s = d * M * M, d * M
                p = (1 << m) - 1
                for maximum in (False, True):
                    a = ([p] * K if maximum else
                         [rng.randrange(p + 1) for _ in range(K)])
                    b = ([p] * K if maximum else
                         [rng.randrange(p + 1) for _ in range(K)])
                    u, v = check_case(a, m, s), check_case(b, m, s)
                    diag = [sum(u[i] * v[j] for i in range(M)
                                for j in range(M) if i + j == k)
                            for k in range(2 * M - 1)]
                    result = sum(t * p ** (s * k) for k, t in enumerate(diag))
                    X = sum(t << (m * i) for i, t in enumerate(a))
                    Y = sum(t << (m * i) for i, t in enumerate(b))
                    assert result == X * Y
                    COUNTS["matrix_product_checks"] += 1
    summary = {
        "status": "all fresh exact controls passed",
        "counts": COUNTS,
        "largest_checked_temporary_bits": MAX_TMP_BITS,
        "seed": 202610171205,
        "limitations": "Exact arithmetic checks, not complexity benchmarks or universal proofs.",
    }
    (HERE / "CONTROL_RESULTS.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
