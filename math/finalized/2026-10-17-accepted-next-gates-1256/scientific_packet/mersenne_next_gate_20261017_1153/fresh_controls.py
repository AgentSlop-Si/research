#!/usr/bin/env python3
"""Fresh arithmetic controls only; not a bit-complexity benchmark or proof."""
import json
from itertools import product
from math import comb
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent

def shift_formula(a):
    K = len(a)
    return [sum(comb(i, j) * a[i] for i in range(j, K)) for j in range(K)]

def shift_horner(a):
    c = []
    for x in reversed(a):
        c = [x + (c[0] if c else 0)] + [c[j - 1] + (c[j] if j < len(c) else 0) for j in range(1, len(c) + 1)]
    return c

def pack(c, p, s):
    assert len(c) % s == 0
    return [sum(c[i + j] * p**j for j in range(s)) for i in range(0, len(c), s)]

def value(c, base):
    y = 0
    for x in reversed(c):
        y = y * base + x
    return y

def matrix_product(u, v, R):
    out = [0] * (len(u) + len(v) - 1)
    for i, x in enumerate(u):
        for j, y in enumerate(v):
            out[i + j] += x * y
    return value(out, R), out

def volume(c):
    return sum(x.bit_length() for x in c)

def multiply_z_plus_one(c):
    return [c[0]] + [c[j] + c[j-1] for j in range(1, len(c))]

def main():
    rng = Random(202610171153)
    counts = {"parameter_triplets": 0, "input_roundtrips": 0, "matrix_products": 0,
              "volume_bounds": 0, "exhaustive_monotonic_maxima": 0,
              "linear_witnesses": 0, "eager_product_bounds": 0}
    boundary_rows = []
    for m in range(2, 8):
        p = 2**m - 1
        for K in range(1, 33):
            for s in range(1, K + 1):
                if K % s:
                    continue
                counts["parameter_triplets"] += 1
                N, B = m*K, K//s
                maxima = [p*comb(K, j+1) for j in range(K)]
                umax = pack(maxima, p, s)
                vmax = volume(umax)
                assert 64*vmax >= 3*(N + K*K//s)
                assert vmax <= N + 2*K*K//s
                assert all(u < 2**(m*s+K+1) for u in umax)
                counts["volume_bounds"] += 1
                cases = [[0]*K, [p]*K, [1]+[0]*(K-1),
                         [rng.randrange(p+1) for _ in range(K)],
                         [rng.randrange(p+1) for _ in range(K)]]
                for a in cases:
                    c = shift_formula(a)
                    assert c == shift_horner(a)
                    assert all(x <= y for x, y in zip(c, maxima))
                    u = pack(c, p, s)
                    assert all(x <= y for x, y in zip(u, umax))
                    X = value(a, p+1)
                    assert X == value(c, p) == value(u, p**s)
                    assert volume(u) <= vmax
                    counts["input_roundtrips"] += 1
                    a2 = [rng.randrange(p+1) for _ in range(K)]
                    v = pack(shift_formula(a2), p, s)
                    z, diag = matrix_product(u, v, p**s)
                    assert z == X * value(a2, p+1)
                    assert all(t < B*2**(2*(m*s+K+1)) for t in diag)
                    counts["matrix_products"] += 1
                if 1 < s < K:
                    f = [0]*K
                    f[s-1], f[s-2] = 1, -p
                    assert pack(f, p, s) == [0]*B
                    assert pack(multiply_z_plus_one(f), p, s) == [-p**s, 1]+[0]*(B-2)
                    counts["linear_witnesses"] += 1
                prod_volume = sum((u*v).bit_length() for u in umax for v in umax)
                assert 2*B*vmax-B*B <= prod_volume <= 2*B*vmax
                counts["eager_product_bounds"] += 1
                if m == 2 and s in (1, K) and K in (1, 2, 4, 8, 16, 32):
                    boundary_rows.append({"m":m,"K":K,"s":s,"N":N,"volume":vmax,"H":m*s+K+1})
    # Small exhaustive legal domains independently check simultaneous maxima.
    for m, K in [(2,1),(2,2),(2,3),(2,4),(3,2),(4,2)]:
        p = 2**m-1
        for s in range(1,K+1):
            if K%s:
                continue
            maximum = pack(shift_formula([p]*K),p,s)
            actual = [0]*len(maximum)
            for a in product(range(p+1),repeat=K):
                u = pack(shift_formula(a),p,s)
                actual = [max(x,y) for x,y in zip(actual,u)]
                counts["exhaustive_monotonic_maxima"] += 1
            assert actual == maximum
    # Explicit guard-bit regression found in independent analytical review.
    m, K, s = 2, 4, 2
    p, N = 2**m-1, m*K
    u = pack(shift_formula([p]*K), p, s)
    answer, diag = matrix_product(u, u, p**s)
    v, max_shift_bits = diag[-1], 0
    for coefficient in reversed(diag[:-1]):
        for _ in range(s):
            shifted = v << m
            max_shift_bits = max(max_shift_bits, shifted.bit_length())
            assert shifted.bit_length() <= 2*N+1
            v = shifted-v
            assert v.bit_length() <= 2*N
        v += coefficient
        assert v.bit_length() <= 2*N
    assert v == answer == (2**N-1)**2
    assert max_shift_bits == 2*N+1
    result={"status":"PASS","counts":counts,"boundary_rows":boundary_rows,
            "scratch_guard_regression":{"m":m,"K":K,"s":s,"N":N,"U":u,"S":diag,"answer":answer,"max_shift_bits":max_shift_bits},
            "proof_status":"The universal identities and complexity statements are justified by REPORT.md, not by these finite controls.",
            "historical_scripts_executed":False,"benchmark":False,"random_seed":202610171153}
    (ROOT/"CONTROL_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__ == "__main__":
    main()
