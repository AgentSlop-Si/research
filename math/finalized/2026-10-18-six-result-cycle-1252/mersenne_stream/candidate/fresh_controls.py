"""Fresh deterministic controls. Native arithmetic below is an oracle only."""
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import kernel_stream as core

ROOT = Path(__file__).resolve().parent
rng = random.Random(202610181243)
counts = {}
digest = hashlib.sha256()

def record(label, value):
    counts[label] = counts.get(label, 0) + 1
    digest.update((label + ':' + repr(value)).encode())

def scalar_oracle(a, sigma):
    return [sum(math.comb(i, j) * sigma ** (i - j) * a[i]
                for i in range(j, len(a))) for j in range(len(a))]

# Explicit arithmetic core, signed and leaf/split boundaries.
for width in (0, 1, 8, 15, 16, 17, 31, 32, 33, 63, 127, 257, 1025):
    for _ in range(80):
        x, y = rng.getrandbits(width), rng.getrandbits(width)
        x *= rng.choice((-1, 1)); y *= rng.choice((-1, 1))
        z = core.karatsuba(x, y)
        assert z == x * y
        record('karatsuba', hex(z))

# Exact common denominator, cofactors and all paid microinverses.
for n in list(range(2, 36)) + [48, 64, 97]:
    p = core.parameters(n, max(1, n * 8))
    t = p['t']
    u, f, v, k = core.prepare(n, t)
    for i in range(n):
        fact = math.factorial(i)
        exact_u = fact >> (i - i.bit_count())
        assert u[i] == exact_u
        assert u[i] * f[i] == u[-1]
        assert v[i] == pow(u[i], -1, 1 << t)
        assert k[i] == (u[-1] // u[i]) << i.bit_count()
        assert 0 < k[i] < 1 << t
    record('tables', (n, t, hex(u[-1])))

# Instrument all narrow-convolution carries, coefficient bounds and prefixes.
def check_convolution(a, k, W, t):
    n = len(a); R = 1 << t; mask = (1 << W) - 1
    prefix_c = [0] * n; prefix_out = [0] * n
    calls = []
    def product(x, y):
        calls.append((x.bit_length(), y.bit_length()))
        return core.karatsuba(x, y)
    def trace(slab, coordinate, digits, c, carry, next_carry):
        assert c == sum(digits[i] * k[coordinate - i] for i in range(coordinate + 1))
        assert 0 <= c <= n * (R - 1) ** 2
        assert 0 <= carry <= n * (R - 1)
        assert 0 <= next_carry <= n * (R - 1)
        assert c + carry < n * R * R
        prefix_c[coordinate] += c << (slab * t)
        digit = (c + carry) & (R - 1)
        prefix_out[coordinate] += digit << (slab * t)
        assert prefix_c[coordinate] == prefix_out[coordinate] + (next_carry << ((slab + 1) * t))
    actual = core.narrow_convolution(a, k, W, t, product, trace)
    expected = [sum(a[i] * k[j - i] for i in range(j + 1)) & mask for j in range(n)]
    assert actual == expected
    b = 8 * ((2 * t + (n - 1).bit_length() + 7) // 8)
    assert len(calls) == (W + t - 1) // t
    assert all(x <= n * b and y <= n * b for x, y in calls)
    record('narrow_convolution', (n, W, t, actual))

for a in itertools.product(range(16), repeat=2):
    for k in ([1, 1], [255, 255], [0, 239]):
        check_convolution(a, k, 4, 8)
for n in (1, 2, 3, 5, 8, 11):
    for W in (1, 7, 8, 9, 17, 33, 257, 1025):
        for t in (8, 16, 24):
            a = [rng.getrandbits(W) for _ in range(n)]
            k = [rng.getrandbits(t) for _ in range(n)]
            check_convolution(a, k, W, t)

# Independently instrument local modular divisions and every carry identity.
for W in (1, 7, 8, 9, 17, 65, 257, 1025, 8193):
    for t in (8, 16, 24, 64):
        u = rng.getrandbits(t) | 1
        x = rng.getrandbits(W)
        v = core.odd_inverse(u, t)
        calls = []
        def product(a, b):
            assert a.bit_length() <= t and b.bit_length() <= t
            calls.append(1)
            return core.karatsuba(a, b)
        def trace(a, b, c, nxt, numerator):
            assert 0 <= c < u and 0 <= nxt < u
            assert numerator == u * b + c - a
            assert numerator == nxt << t
        result = core.limb_divide(x, u, W, t, v, product, trace)
        assert result == (x * pow(u, -1, 1 << W)) % (1 << W)
        assert len(calls) == 2 * ((W + t - 1) // t)
        record('modular_division', (W, t, hex(result)))

assert core.shift([], 1) == []
record('empty_shift', True)
for n in range(1, 5):
    for a in itertools.product((-1, 0, 1), repeat=n):
        for sign in (-1, 1):
            actual = core.shift(a, sign)
            assert actual == scalar_oracle(a, sign)
            assert core.shift(actual, -sign) == list(a)
            record('exhaustive_shift_inverse', (a, sign, actual))
for n in (2, 3, 5, 8, 12, 17, 24):
    for h in (1, 9, 65, 513, 2049):
        for sign in (-1, 1):
            a = [rng.getrandbits(h) * rng.choice((-1, 1)) for _ in range(n)]
            calls = []
            def product(x, y):
                calls.append((x.bit_length(), y.bit_length()))
                return core.karatsuba(x, y)
            actual = core.shift(a, sign, h, convolution_product=product)
            assert actual == scalar_oracle(a, sign)
            p = core.parameters(n, h)
            assert len(calls) == p['q']
            assert max(max(pair) for pair in calls) <= p['S']
            assert core.shift(actual, -sign) == a
            record('wide_signed_shift_inverse', (n, h, sign, [hex(v) for v in actual]))

# Exact complete scalar ledger, with preparation separated from packed calls.
for n in (2, 3, 5, 8, 17):
    for h in (1, 9, 513):
        a = [rng.getrandbits(h) for _ in range(n)]
        p = core.parameters(n, h)
        local_calls, packed_calls = [], []
        def local_product(x, y):
            assert max(x.bit_length(), y.bit_length()) <= p['t']
            local_calls.append(1)
            return core.karatsuba(x, y)
        def packed_product(x, y):
            assert max(x.bit_length(), y.bit_length()) <= p['S']
            packed_calls.append(1)
            return core.karatsuba(x, y)
        actual = core.shift(a, 1, h, local_product, packed_product)
        short_bits = 8 * ((max(1, p['g']) + 7) // 8)
        preparation = 3 * (n - 1) * ((p['t'] + short_bits - 1) // short_bits)
        preparation += 2 * (p['t'] - 1).bit_length()
        assert len(local_calls) == preparation + 5 * n * p['q']
        assert len(packed_calls) == p['q']
        assert actual == scalar_oracle(a, 1)
        record('complete_scalar_ledger', (n, h, preparation, len(local_calls), len(packed_calls)))

# Mersenne identities and canonical carry controls. Native division here is an
# independent normalization oracle; the inherited linear carry is not rerun.
for m, L in ((2, 2), (3, 3), (5, 5), (7, 4), (11, 6), (31, 7), (61, 8), (127, 12), (521, 16)):
    p = (1 << m) - 1
    for trial in range(4):
        a = [((1 << m) - 1 if trial == 0 else rng.getrandbits(m)) for _ in range(L)]
        x = sum(a[i] << (m * i) for i in range(L))
        redundant = core.shift(a, 1, m)
        assert sum(v * p ** i for i, v in enumerate(redundant)) == x
        canonical = []
        carry = 0
        for coefficient in redundant:
            carry, digit = divmod(coefficient + carry, p)
            canonical.append(digit)
        while carry:
            carry, digit = divmod(carry, p)
            canonical.append(digit)
        binary = core.shift(canonical, -1)
        assert sum(v << (m * i) for i, v in enumerate(binary)) == x
        record('mersenne_roundtrip', (m, L, trial, hex(x)))
        for d in (1, 2, 3, L + 1):
            groups = [sum(canonical[i + j] * p ** j for j in range(min(d, len(canonical) - i)))
                      for i in range(0, len(canonical), d)]
            assert sum(v * (p ** d) ** i for i, v in enumerate(groups)) == x
            record('grouped_identity', (m, L, trial, d))

# Omitted denominator and omitted inter-slab carries are genuinely incorrect.
a = [1, 2, 3, 4, 5]
p = core.parameters(len(a), 3)
u, f, v, k = core.prepare(len(a), p['t'])
assert u[-1] > 1
assert k[0] != pow(u[0], -1, 1 << p['W'])
modulus = 1 << p['W']
scaled = [(u[i] * a[i] << (p['g'] - i.bit_count())) % modulus for i in range(len(a))]
c = [sum(scaled[len(a) - 1 - i] * k[j - i] for i in range(j + 1)) % modulus
     for j in range(len(a))]
wrong_shift = []
for j in range(len(a)):
    wrong = (c[len(a) - 1 - j] * pow(u[j], -1, modulus) << j.bit_count()) % modulus
    wrong >>= p['g']
    if wrong >= 1 << (p['H'] - 1):
        wrong -= 1 << p['H']
    wrong_shift.append(wrong)
assert wrong_shift != scalar_oracle(a, 1)
record('negative_missing_denominator', wrong_shift)
R = 256
wide = [R - 1 + (R - 1) * R] * 2
kernel = [R - 1] * 2
correct = core.narrow_convolution(wide, kernel, 16, 8)
wrong = [((wide[0] & 255) * 255) & 255,
         (2 * (wide[0] & 255) * 255) & 255]
wrong = [x + (x << 8) for x in wrong]
assert correct != wrong
record('negative_missing_carries', True)

# Three concrete shrinking-call witnesses, without making timing claims.
examples = []
for L, m in ((8, 8192), (16, 32768), (32, 131072)):
    p = core.parameters(L, m)
    old_slot = 8 * ((2 * p['W'] + p['g'] + 7) // 8)
    assert p['S'] < L * m < L * old_slot
    examples.append({'L': L, 'm': m, 'N': L * m, 'old_capacity': L * old_slot,
                     'new_capacity': p['S'], 'slab_products': p['q'],
                     'local_diagonal_products': 5 * L * p['q']})

result = {'status': 'PASS', 'counts': counts, 'sha256': digest.hexdigest(),
          'examples': examples, 'native_oracles': 'Controls only; default production products use explicit Karatsuba.',
          'external_writes': False}
(ROOT / 'RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
