#!/usr/bin/env python3
"""Exact arithmetic-only scope check. No FFT/table construction or imports.

This is a new standalone calculation of the frozen theorem's branch guard and
response-entry count, not execution of any predecessor/research program.
"""


def parameters(v, t):
    assert v >= 1 and 2 <= t <= v + 1
    # For positive n, ceil(log2(n)) = (n - 1).bit_length().
    p = t + 10 + v.bit_length()
    k = (2 * v + p + 5).bit_length()
    b = 2 * (p + k + 1)
    return p, k, b


def first_eligible_v(t):
    v = max(1, t - 1)
    # Exhaustively reject every smaller admissible v using exact integers.
    while 64 * parameters(v, t)[2] > v:
        v += 1
    return v


expected = {
    2: (5120, 25, 14, 80, 675),
    8: (5888, 31, 14, 92, 777),
    16: (6912, 39, 14, 108, 913),
    53: (11904, 77, 15, 186, 1575),
}

for t, expected_row in expected.items():
    v = first_eligible_v(t)
    p, k, b = parameters(v, t)
    assert 64 * b == v
    assert 64 * parameters(v - 1, t)[2] > v - 1
    P = 1 << ((v // (16 * b)).bit_length() - 1)
    assert 16 * b * P <= v < 16 * b * (2 * P)
    d, g = P.bit_length() - 1, p + 10
    A, B = 2 * b * P, b * P
    # These are scalar integer COUNTS. No response table is allocated.
    entries = ((1 << g) - 1) * (1 << A) + d * (1 << B)
    upper_exponent = entries.bit_length()
    assert (v, p, k, b, upper_exponent) == expected_row
    assert P == 4 and d == 2
    assert 1 << (upper_exponent - 1) < entries < 1 << upper_exponent
    assert entries < 1 << v
    print(f"t={t}: v_min={v}, p={p}, k={k}, b={b}, P={P}, d={d}, g={g}")
    print(f"  N=2^{v}")
    print(f"  response entries=(2^{g}-1)*2^{A}+{d}*2^{B}")
    print(f"  2^{upper_exponent - 1} < entries < 2^{upper_exponent}")
    print(f"  2^({upper_exponent - 1 - v}) < entries/N < 2^({upper_exponent - v})")

print("PASS: all exact guard minima and entry-count bounds verified.")
