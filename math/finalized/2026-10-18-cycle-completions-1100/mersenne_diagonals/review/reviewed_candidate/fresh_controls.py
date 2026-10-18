"""Fresh exact controls. Native arithmetic below is used as an independent oracle."""
import hashlib
import itertools
import json
import math
import random
from pathlib import Path

from diagonal_core import kmul, inverse_odd, stream_mul, stream_div_odd, parameters, tables, shift

ROOT = Path(__file__).resolve().parent
rng = random.Random(202610181043)
counts = {}
digest = hashlib.sha256()


def record(name, *values):
    counts[name] = counts.get(name, 0) + 1
    def stable(v):
        if isinstance(v, int):
            return hex(v)
        if isinstance(v, (tuple, list)):
            return [stable(w) for w in v]
        return v
    digest.update((name + ':' + repr(stable(values)) + '\n').encode())


for x in range(64):
    for y in range(64):
        assert kmul(x, y) == x * y
        record('karatsuba', x, y)
for b in [15, 16, 17, 31, 32, 33, 63, 65, 129, 257, 511, 1025]:
    for _ in range(8):
        x, y = rng.getrandbits(b), rng.getrandbits(b)
        assert kmul(x, y) == x * y
        record('karatsuba', b, x, y)

for W in range(1, 9):
    mask = (1 << W) - 1
    for u in range(1, 256, 2):
        v = inverse_odd(u, 8)
        assert (v * u) & 255 == 1
        for x in range(1 << W):
            z = stream_div_odd(x, u, W, 8, v)
            assert z == (x * pow(u, -1, 1 << W)) & mask
            record('exhaustive_division', W, x, u)

for W in [1, 7, 8, 9, 15, 17, 31, 63, 64, 65, 127, 128, 129, 257, 511, 1025, 4097, 16385]:
    for t in [8, 16, 32, 64, 128]:
        for _ in range(4):
            u = rng.getrandbits(t) | 1
            x = rng.getrandbits(W)
            mask = (1 << W) - 1
            v = inverse_odd(u, t)
            z = stream_div_odd(x, u, W, t, v)
            assert z == (x * pow(u, -1, 1 << W)) & mask
            assert stream_mul(x, u, W, t) == (x * u) & mask
            # Independently reconstruct every streamed carry and prefix.
            q = (W + t - 1) // t
            carry, X, Y = 0, 0, 0
            R = 1 << t
            for j in range(q):
                a = (x >> (j * t)) & (R - 1)
                b = ((a - carry) * v) & (R - 1)
                total = u * b + carry - a
                assert total % R == 0
                carry = total // R
                X += a << (j * t)
                Y += b << (j * t)
                assert 0 <= carry < u
                assert u * Y == X + (carry << ((j + 1) * t))
            assert Y & mask == z
            record('streamed_arithmetic_and_invariants', W, t, u, x)

for n in [1, 2, 3, 4, 7, 8, 9, 16, 17, 32, 33, 64]:
    for h in [1, n, 8 * n, 128 * n]:
        H, g, W, Bn, B, t = parameters(n, h)
        U, v, V = tables(n, W, t)
        for i in range(n):
            fact = math.factorial(i)
            exact_u = fact >> (i - i.bit_count())
            assert U[i] == exact_u % (1 << t)
            assert U[i] % (1 << W) == exact_u % (1 << W)
            assert v[i] == pow(U[i], -1, 1 << t)
            assert V[i] == pow(exact_u, -1, 1 << W)
            assert exact_u.bit_length() <= Bn
        record('factorial_tables', n, h, W, Bn, B, t)


def direct(a, sigma):
    return [sum(math.comb(i, j) * sigma ** (i - j) * a[i]
                for i in range(j, len(a))) for j in range(len(a))]


assert shift([]) == []
record('empty_shift')
for n in range(1, 4):
    for a in itertools.product(range(-2, 3), repeat=n):
        for sigma in (-1, 1):
            out = shift(a, sigma)
            assert out == direct(a, sigma)
            assert shift(out, -sigma) == list(a)
            record('signed_shift_and_inverse', a, sigma, out)
for n in [2, 3, 4, 7, 8, 9, 16, 17, 32]:
    for h in [1, 2, n, 4 * n, 64 * n]:
        for sigma in (-1, 1):
            a = [rng.randrange(-(1 << h) + 1, 1 << h) for _ in range(n)]
            out = shift(a, sigma, h)
            assert out == direct(a, sigma)
            assert shift(out, -sigma) == a
            record('signed_shift_and_inverse', n, h, sigma, out)

for m in [2, 3, 4, 5, 7, 13, 31, 127, 257]:
    p, radix = (1 << m) - 1, 1 << m
    for L in [1, 2, 3, 5, 8]:
        a = [rng.randrange(radix) for _ in range(L)]
        X = sum(z << (i * m) for i, z in enumerate(a))
        c = shift(a, 1, m)
        assert sum(z * p ** i for i, z in enumerate(c)) == X
        assert shift(c, -1) == a
        # Canonical p digits are an oracle-only normalization boundary.
        digits, q = [], X
        while q:
            q, z = divmod(q, p)
            digits.append(z)
        if not digits:
            digits = [0]
        binary_raw = shift(digits, -1)
        assert sum(z << (i * m) for i, z in enumerate(binary_raw)) == X
        record('binary_p_roundtrip', m, L, X)
        for d in [1, 2, 3]:
            for start in range(0, len(digits), d):
                group = digits[start:start + d]
                raw = shift(group, -1)
                assert sum(z << (i * m) for i, z in enumerate(raw)) == sum(z * p ** i for i, z in enumerate(group))
            record('grouped_digit_identity', m, L, d)

# Exact outer multiplication counts, including non-byte-aligned W and W<t.
for W, t in [(1, 8), (7, 8), (8, 8), (9, 8), (65, 16), (4097, 128)]:
    calls = []
    def counted(x, y):
        calls.append((x.bit_length(), y.bit_length()))
        return kmul(x, y)
    u = (1 << (t - 1)) + 1
    v = inverse_odd(u, t)
    stream_div_odd((1 << W) - 1, u, W, t, v, counted)
    assert len(calls) == 2 * ((W + t - 1) // t)
    assert all(a <= t and b <= t for a, b in calls)
    record('exact_division_product_counts', W, t, len(calls))

# Dropping the carry is unsound; this has x=1,u=3,t=8,W=16.
u, x, W, t = 3, 1, 16, 8
v = inverse_odd(u, t)
bad = (x & 255) * v & 255
assert bad != stream_div_odd(x, u, W, t, v)
record('negative_control_drop_carry', bad)
# Dense ordinary convolution does not isolate diagonals at 2*i.
a, u = [1, 2, 4], [1, 1, 1]
assert sum(a[k] * u[2 - k] for k in range(3)) != a[1] * u[1]
record('negative_control_naive_batch')

result = {'status': 'PASS', 'seed': 202610181043, 'counts': counts,
          'digest': digest.hexdigest(), 'timing_claim': False,
          'scope': 'Finite exact controls; proof, not samples, supplies complexity.'}
(ROOT / 'RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
