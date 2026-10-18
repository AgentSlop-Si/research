"""Fresh, self-contained bounded controls for streamed short-factor conversion.

No historical source is imported or executed. Represented core multiplication
uses shift/add leaves and explicit Karatsuba. Python wide *, //, %, ** and
math.comb appear only in the independently labelled oracle/control section.
The bit-cost proof does not include optional diagnostic instrumentation.
"""
from pathlib import Path
import hashlib
import json
import math
import random


def leaf_mul(x, y):
    z = 0
    while y:
        if y & 1:
            z += x
        x <<= 1
        y >>= 1
    return z


def kara(x, y):
    """Exact nonnegative product; difference form avoids enlarged children."""
    assert x >= 0 and y >= 0
    t = max(x.bit_length(), y.bit_length())
    if not x or not y:
        return 0
    if t <= 16:
        return leaf_mul(x, y)
    h = (t + 1) // 2
    mask = (1 << h) - 1
    x0, x1 = x & mask, x >> h
    y0, y1 = y & mask, y >> h
    z0 = kara(x0, y0)
    z2 = kara(x1, y1)
    dx, dy = x1 - x0, y1 - y0
    zd = kara(abs(dx), abs(dy))
    if (dx < 0) != (dy < 0):
        zd = -zd
    cross = z0 + z2 - zd
    return z0 + (cross << h) + (z2 << (h + h))


def short_mod(x, k, width, bound):
    """Return x*k modulo 2**width, with k<bound and 0<=x<2**width.

    Each byte-aligned limb has t>=bit_length(bound-1) bits. Input and output
    are converted to/from byte windows once. There is no repeated full-input
    right shift, no growing shifted accumulation, and no W-by-t core product.
    """
    assert width >= 1 and bound >= 2
    assert 0 <= k < bound and 0 <= x < (1 << width)
    limb_bytes = max(1, ((bound - 1).bit_length() + 7) // 8)
    t = limb_bytes << 3
    count = (width + t - 1) // t
    total_bytes = count * limb_bytes
    src = x.to_bytes(total_bytes, 'little')
    dst = bytearray(total_bytes)
    carry = 0
    mask = (1 << t) - 1
    for off in range(0, total_bytes, limb_bytes):
        a = int.from_bytes(src[off:off + limb_bytes], 'little')
        z = kara(a, k) + carry
        b, carry = z & mask, z >> t
        assert 0 <= carry < max(1, k)
        dst[off:off + limb_bytes] = b.to_bytes(limb_bytes, 'little')
    return int.from_bytes(dst, 'little') & ((1 << width) - 1)


def odd_inverse(u, width):
    assert u & 1 and width >= 1
    v, q = 1, 1
    while q < width:
        q = min(q + q, width)
        mask = (1 << q) - 1
        v = kara(v, (2 - (kara(u & mask, v) & mask)) & mask) & mask
    return v


def odd_tables(n, width):
    assert n >= 1 and width >= 1
    bound = max(2, n)
    odd = [1]
    for i in range(1, n):
        z = i
        while not z & 1:
            z >>= 1
        odd.append(z)
    u = [1]
    for i in range(1, n):
        u.append(short_mod(u[-1], odd[i], width, bound))
    inv = [0] * n
    inv[-1] = odd_inverse(u[-1], width)
    for i in range(n - 1, 0, -1):
        inv[i - 1] = short_mod(inv[i], odd[i], width, bound)
    return u, inv


def packed_convolution(a, b, width):
    assert len(a) == len(b) and a
    n = len(a)
    logn = (n - 1).bit_length()
    slot_bytes = (width + width + logn + 7) // 8
    size = n * slot_bytes
    aa, bb = bytearray(size), bytearray(size)
    for i, (x, y) in enumerate(zip(a, b)):
        off = i * slot_bytes
        aa[off:off + slot_bytes] = x.to_bytes(slot_bytes, 'little')
        bb[off:off + slot_bytes] = y.to_bytes(slot_bytes, 'little')
    prod = kara(int.from_bytes(aa, 'little'), int.from_bytes(bb, 'little'))
    raw = prod.to_bytes(size + size, 'little')
    mask = (1 << width) - 1
    return [int.from_bytes(raw[i * slot_bytes:(i + 1) * slot_bytes], 'little') & mask
            for i in range(n + n - 1)]


def taylor(a, sign):
    assert sign in (-1, 1)
    if not a:
        return []
    n = len(a)
    h = max(1, max(abs(x).bit_length() for x in a))
    H = h + n + 1
    guard = (n - 1).bit_length()
    W = H + guard
    mask = (1 << W) - 1
    u, inv = odd_tables(n, W)
    A, G, J = [], [], []
    for i in range(n):
        pop = i.bit_count()
        A.append((kara(u[i], a[i] & mask) << (guard - pop)) & mask)
        gi = (inv[i] << pop) & mask
        G.append(gi)
        J.append((-gi if sign == -1 and i & 1 else gi) & mask)
    D = packed_convolution(A[::-1], J, W)
    result = []
    for j in range(n):
        r = kara(G[j], D[n - 1 - j]) & mask
        assert r & ((1 << guard) - 1) == 0
        r >>= guard
        if r >= (1 << (H - 1)):
            r -= 1 << H
        result.append(r)
    return result


def div_mersenne(x, m):
    """Local quotient-limb division; only bounded m-bit steps."""
    assert x >= 0 and m >= 2
    if x == 0:
        return 0, 0
    # Use byte-aligned windows around exact m-bit chunks. The small reference
    # controls below use direct bounded shifts on x only in the independent
    # positional oracle; this local quotient routine uses bit-by-bit bytes.
    p = (1 << m) - 1
    bits = x.bit_length()
    count = (bits + m - 1) // m
    src = x.to_bytes((bits + 7) // 8, 'little')
    qbytes = bytearray((count * m + 7) // 8)
    rem = 0
    for j in range(count - 1, -1, -1):
        start = j * m
        lo = start // 8
        hi = (start + m + 7) // 8
        a = (int.from_bytes(src[lo:hi], 'little') >> (start & 7)) & p
        s = rem + a
        delta = int(s >= p)
        qlimb, rem = rem + delta, s - (p if delta else 0)
        # Only the O(m)-bit output window is read/modified, with overlap <8 bits.
        old = int.from_bytes(qbytes[lo:hi], 'little')
        old |= qlimb << (start & 7)
        qbytes[lo:hi] = old.to_bytes(hi - lo, 'little')
    return int.from_bytes(qbytes, 'little'), rem


def canonical_p(a, m):
    p = (1 << m) - 1
    out, carry = [], 0
    for x in a:
        z = x + carry
        if z >= 0:
            carry, digit = div_mersenne(z, m)
        else:
            q, r = div_mersenne(-z, m)
            carry, digit = (-q, 0) if r == 0 else (-q - 1, p - r)
        out.append(digit)
    assert carry >= 0
    while carry:
        carry, digit = div_mersenne(carry, m)
        out.append(digit)
    while out and out[-1] == 0:
        out.pop()
    return out


# Everything below this line is a correctness oracle or small control ledger.
# Its native Python arithmetic is deliberately excluded from core cost claims.
def controls():
    rng = random.Random(20261018000230)
    counts = {'karatsuba': 0, 'short_mod': 0, 'odd_tables': 0,
              'taylor': 0, 'conversion': 0, 'grouped_pipeline': 0,
              'mersenne_division': 0, 'negative_controls': 0}
    digest = hashlib.sha256()
    def record(key, value):
        counts[key] += 1
        digest.update(repr((key, value)).encode())
    for t in (1, 2, 7, 8, 15, 16, 17, 31, 32, 63, 64, 129, 257):
        for _ in range(20):
            x, y = rng.getrandbits(t), rng.getrandbits(t)
            got = kara(x, y)
            assert got == x * y
            record('karatsuba', got)
    for W in range(1, 9):
        for x in range(1 << W):
            for k in range(32):
                got = short_mod(x, k, W, 32)
                assert got == (x * k) % (1 << W)
                record('short_mod', got)
    for n in (2, 3, 7, 16, 31, 128, 256, 257, 512, 1025, 65537):
        for W in (1, 7, 8, 9, 15, 16, 17, 63, 64, 65, 257, 1024, 8193):
            for _ in range(8):
                x, k = rng.getrandbits(W), rng.randrange(n)
                got = short_mod(x, k, W, n)
                assert got == (x * k) % (1 << W)
                record('short_mod', got)
    for n in (1, 2, 3, 7, 16, 31, 64, 129):
        for W in (1, 7, 31, n + 17, 2 * n + 19):
            u, v = odd_tables(n, W)
            fact = 1
            for i in range(n):
                if i:
                    fact *= i
                odd = fact // (fact & -fact)
                assert u[i] == odd % (1 << W)
                assert (u[i] * v[i]) % (1 << W) == 1
            record('odd_tables', (n, W, u[-1]))
    for n in (1, 2, 3, 5, 8, 13, 20, 33):
        for h in (1, 3, 11, 37):
            for _ in range(2):
                a = [rng.randrange(-(1 << h) + 1, 1 << h) for _ in range(n)]
                for sign in (-1, 1):
                    got = taylor(a, sign)
                    want = [sum(math.comb(i, j) * sign ** (i - j) * a[i]
                                for i in range(j, n)) for j in range(n)]
                    assert got == want
                    assert taylor(got, -sign) == a
                    record('taylor', got)
    for m in (2, 3, 4, 5, 7, 8, 13, 31, 61, 127):
        p = (1 << m) - 1
        for width in (1, m - 1, m, m + 1, 3 * m + 1):
            for _ in range(8):
                x = rng.getrandbits(width)
                got = div_mersenne(x, m)
                assert got == divmod(x, p)
                record('mersenne_division', got)
        for n in (1, 2, 5, 11):
            a = [rng.randrange(1 << m) for _ in range(n)]
            shifted = taylor(a, 1)
            x = sum(ai << (i * m) for i, ai in enumerate(a))
            assert sum(ci * p ** i for i, ci in enumerate(shifted)) == x
            canon = canonical_p(shifted, m)
            assert sum(ci * p ** i for i, ci in enumerate(canon)) == x
            back = taylor(canon, -1)
            assert sum(ci << (i * m) for i, ci in enumerate(back)) == x
            record('conversion', (m, n, canon))
            for d in (1, 2, 4):
                b = [rng.randrange(1 << m) for _ in range(n)]
                y = sum(bi << (i * m) for i, bi in enumerate(b))
                bc = canonical_p(taylor(b, 1), m)
                A = [sum(canon[i + j] * p ** j for j in range(min(d, len(canon) - i)))
                     for i in range(0, len(canon), d)]
                B = [sum(bc[i + j] * p ** j for j in range(min(d, len(bc) - i)))
                     for i in range(0, len(bc), d)]
                C = [0] * max(0, len(A) + len(B) - 1)
                for i, aa in enumerate(A):
                    for j, bb in enumerate(B):
                        C[i + j] += aa * bb
                # Direct oracle expansion of raw grouped coefficients. Converter
                # is independently checked above; this is only positional identity.
                assert sum(cc * p ** (d * i) for i, cc in enumerate(C)) == x * y
                record('grouped_pipeline', (m, n, d, C))
    # Removing inter-limb carry is unsound even before modular truncation.
    W, n, x, k = 17, 257, 65535, 256
    t = 16
    wrong = ((x & ((1 << t) - 1)) * k & ((1 << t) - 1))
    assert wrong != (x * k) % (1 << W)
    record('negative_controls', 'dropped_inter_limb_carry_detected')
    return {'status': 'PASS', 'counts': counts, 'result_digest': digest.hexdigest(),
            'seed': 20261018000230,
            'scope': 'Finite exactness controls; no timing or asymptotic inference.',
            'prime_assumption': 'None; m=4 and m=8 include composite positional controls.'}


if __name__ == '__main__':
    result = controls()
    dest = Path(__file__).with_name('CONTROL_RESULTS.json')
    dest.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
