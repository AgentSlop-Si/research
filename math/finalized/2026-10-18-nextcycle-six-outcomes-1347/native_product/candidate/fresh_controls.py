"""Finite independent oracles; native multiplication appears here only."""
import hashlib
import itertools
import json
import math
import random
from pathlib import Path
from product_interface import shift_mod, two_wide_convolution, binary_chunks, reconstruct_binary, multiply_interface

ROOT = Path(__file__).parent
rng = random.Random(202610181333)
counts = {}
transcript = []

def record(kind, value):
    counts[kind] = counts.get(kind, 0) + 1
    transcript.append((kind, value))

def oracle_shift(a, sigma, H):
    return [sum(math.comb(i, j) * sigma**(i-j) * a[i] for i in range(j, len(a))) % (1 << H) for j in range(len(a))]

def conv(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out

# Target precision is deliberately smaller than the input/shift height.
for n in range(0, 15):
    for H in [1, 2, 3, 7, 8, 9, 15, 16, 31, 65, 257]:
        for sigma in [-1, 1]:
            vectors = [[0] * n, [(1 << (H+10))-1] * n, [rng.randrange(-(1 << (H+4)), 1 << (H+4)) for _ in range(n)]]
            for a in vectors:
                got = shift_mod(a, sigma, H)
                assert got == oracle_shift(a, sigma, H)
                assert shift_mod(got, -sigma, H) == [x % (1 << H) for x in a]
                record('modular_shift', [n, H, sigma, got])

trace_count = 0
for n in [1, 2, 3, 5, 8, 13]:
    for H in [1, 7, 8, 9, 15, 16, 17, 33, 65, 129, 257]:
        for t in [8, 16, 24, 40]:
            for mode in range(3):
                top = (1 << H) - 1
                a = [top if mode == 0 else 0 if mode == 1 else rng.randrange(1 << H) for _ in range(n)]
                b = [top if mode == 0 else rng.randrange(1 << H) for _ in range(n)]
                ledger = {}
                calls = []
                def product(x, y):
                    calls.append((x.bit_length(), y.bit_length()))
                    # This is an independent instrumented exact oracle.
                    return x*y
                def trace(r, s, j, left, right, c, old, carry, nxt, digit):
                    global trace_count
                    trace_count += 1
                    assert c == sum(left[i] * right[j-i] for i in range(n) if 0 <= j-i < n)
                    R = 1 << t
                    assert 0 <= carry <= n*(R-1)
                    assert 0 <= nxt <= n*(R-1)
                    assert c + old + carry == digit + R*nxt
                got = two_wide_convolution(a, b, H, t, product=product, trace=trace, stats=ledger)
                assert got == [v & top for v in conv(a, b)]
                assert ledger['packed_calls'] == ledger['expected_calls'] == len(calls)
                assert all(max(pair) <= ledger['S'] for pair in calls)
                record('two_wide_convolution', [n, H, t, mode, ledger, got])
record('slab_carry_transitions', trace_count)

for m in range(2, 20):
    for n in range(1, 15):
        for value in [0, 1, (1 << (m*n))-1, rng.randrange(1 << (m*n))]:
            a = binary_chunks(value, m, n)
            assert a == [(value >> (m*i)) & ((1 << m)-1) for i in range(n)]
            assert reconstruct_binary(a, m) == value
            record('binary_window_roundtrip', [m, n, value])

for m in [2, 3, 4]:
    for n in [1, 2]:
        # Exhaustive x,y for n*m <= 6; boundary/random above this.
        bound = 1 << (m*n)
        pairs = itertools.product(range(bound), repeat=2) if m*n <= 6 else [(bound-1, bound-1)] + [(rng.randrange(bound), rng.randrange(bound)) for _ in range(100)]
        for x, y in pairs:
            assert multiply_interface(x, y, m, n) == x*y
            record('full_products_small', [m, n, x, y])
for n in [1, 2, 3, 5, 8, 13, 24]:
    for m in [2, 7, 31, 128, 513]:
        bound = 1 << (m*n)
        for x, y in [(0, bound-1), (bound-1, bound-1)] + [(rng.randrange(bound), rng.randrange(bound)) for _ in range(3)]:
            ledger = {}
            got = multiply_interface(x, y, m, n, stats=ledger)
            assert got == x*y
            a, b = binary_chunks(x, m, n), binary_chunks(y, m, n)
            assert ledger['final_coefficients'] == conv(a, b)
            record('full_products_wide', [n, m, ledger['packed_calls'], hashlib.sha256(hex(got).encode()).hexdigest()])

# Canonical p^d coefficient precision, independent exact grouped oracle.
for m in [2, 3, 4, 5, 7]:
    p = (1 << m) - 1
    for d in [1, 2, 3, 5]:
        for n in [1, 2, 3, 7]:
            radix = p**d
            H = 2*d*m + (n-1).bit_length()
            a = [radix-1] * n
            b = [radix-1] * n
            z = conv(a, b)
            assert max(z) < 1 << H
            got = two_wide_convolution(a, b, H, 16)
            assert got == z
            assert sum(z[i]*radix**i for i in range(len(z))) == sum(a[i]*radix**i for i in range(n))**2
            record('canonical_group_precision', [m, d, n, H, z])

# Native exponent potential: exact integer certificate r^2 >= 2s,
# K*r >= 2s avoids floating-point proof obligations.
for p in [3, 7, 15, 31]:
    for K in [2, 4, 8, 16]:
        for d in range(1, 65):
            s = K*d
            D = K*(p**d-1)**2
            r = K
            while (p**r+1)//2 <= D:
                r += K
            assert r >= 2*d+1 and r >= K
            assert r*r >= 2*s and K*r >= 2*s
            record('native_potential_certificate', [p, K, d, r])

# Negative controls: odd-modulus residues cannot masquerade as 2-adic residues.
a = [3, 3]
H = 5
c = oracle_shift(a, 1, H)
z = conv(c, c)
right = oracle_shift([v % (1 << H) for v in z], -1, H)
wrong = oracle_shift([v % 17 for v in z], -1, H)
assert right == [9, 18, 9] and wrong == [9, 16, 9]
record('negative_odd_modulus', [c, z, right, wrong])

# One fewer final bit loses a valid maximal binary coefficient.
for m in [2, 3, 7]:
    for n in [1, 2, 4, 8]:
        H = 2*m + (n-1).bit_length()
        z = conv([(1 << m)-1] * n, [(1 << m)-1] * n)
        assert z[n-1] >= 1 << (H-1)
        record('negative_low_precision', [m, n, H, z[n-1]])

# Omitting cross-limb products is the tempting but false q-product generalization.
a, b, H, t = [257], [257], 24, 8
correct = two_wide_convolution(a, b, H, t)
diagonal_only = [1 + (1 << 16)]
assert correct == [66049] and diagonal_only != correct
record('negative_diagonal_only', [correct, diagonal_only])

payload = {'status': 'PASS', 'counts': counts, 'slab_carry_transition_count': trace_count,
           'digest': hashlib.sha256(json.dumps(transcript, sort_keys=True).encode()).hexdigest(),
           'production_default_products': 'explicit inherited Karatsuba; independent native oracles only in this harness',
           'timings_claimed': False, 'external_writes': False}
(ROOT/'RESULTS.json').write_text(json.dumps(payload, indent=2, sort_keys=True)+'\n')
print(json.dumps(payload, indent=2, sort_keys=True))
