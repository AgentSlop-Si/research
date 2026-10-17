"""Fresh exact controls; does not import or execute supplied archive code.

The candidate kernel uses bit shifts/adds and recursively native Fermat-ring
products. Schoolbook shift/add is the only multiplication leaf. Python '*' is
used in independent test oracles, scalar indices, and finite parameter reports.
This is a correctness prototype, not an optimized implementation/bit benchmark.
"""
from collections import Counter
from math import isqrt
import json
import random
from pathlib import Path

LEDGER = Counter()


def shift_residue(x, e, r):
    q = (1 << r) + 1
    e %= 2 * r
    if e >= r:
        x = 0 if x == 0 else q - x
        e -= r
    if e:
        x = ((x << e) & ((1 << r) - 1)) - (x >> (r - e))
        if x < 0:
            x += q
    assert 0 <= x < q
    return x


def school_native(x, y, n):
    """Explicit schoolbook leaf. No hidden native integer product."""
    z = 0
    while y:
        if y & 1:
            z += x
        x <<= 1
        y >>= 1
    q = (1 << n) + 1
    z = (z & ((1 << n) - 1)) - (z >> n)
    if z < 0:
        z += q
    assert 0 <= z < q
    return z


def fft(a, r, inverse=False):
    """Independent radix-2 transform; roots are literal powers of two."""
    k = len(a)
    if k == 1:
        return list(a)
    even = fft(a[::2], r, inverse)
    odd = fft(a[1::2], r, inverse)
    q = (1 << r) + 1
    out = [0] * k
    step = (2 * r // k) * (-1 if inverse else 1)
    for j in range(k // 2):
        t = shift_residue(odd[j], step * j, r)
        u, v = even[j] + t, even[j] - t
        out[j] = u - q if u >= q else u
        out[j + k // 2] = v + q if v < 0 else v
    return out


def width(n, k):
    m = n // k
    # D = K (2^m-1)^2, computed without a wide integer product.
    digit_sq = (1 << (2 * m)) - (1 << (m + 1)) + 1
    d = digit_sq << (k.bit_length() - 1)
    r = k * ((d.bit_length() + k - 1) // k)
    return m, r


def choose(n):
    """Small-instance choice only; the report gives the asymptotic rule."""
    k = 1 << (isqrt(n).bit_length() - 1)
    while k >= 4:
        if n % k == 0:
            m, r = width(n, k)
            if r < n:
                return k, m, r
        k //= 2
    return None


def pack_digits(digits, m):
    raw = bytearray()
    buf = used = 0
    for digit in digits:
        buf |= digit << used
        used += m
        count = used // 8
        if count:
            bits = 8 * count
            raw.extend((buf & ((1 << bits) - 1)).to_bytes(count, "little"))
            buf >>= bits
            used -= bits
    if used:
        raw.append(buf)
    return int.from_bytes(raw, "little")


def combine_signed(coefficients, m):
    """Signed carry, followed by the exact B^K == -1 fold."""
    k = len(coefficients)
    n = k * m
    mask = (1 << m) - 1
    carry = 0
    digits = []
    for c in coefficients:
        v = c + carry
        digits.append(v & mask)
        carry = v >> m
    value = pack_digits(digits, m) - carry
    q = (1 << n) + 1
    if value < 0:
        value += q
    if value >= q:
        value -= q
    assert 0 <= value < q
    return value


def negacyclic_coefficients(a, b, digit_max, r, recurse=True):
    """Compute exact signed coefficients, with asymmetric interval recovery."""
    k = len(a)
    assert len(b) == k and r % k == 0
    q = (1 << r) + 1
    theta_step = r // k
    fa = fft([shift_residue(x, j * theta_step, r) for j, x in enumerate(a)], r)
    fb = fft([shift_residue(x, j * theta_step, r) for j, x in enumerate(b)], r)
    leaf = native if recurse else school_native
    point = [leaf(x, y, r) for x, y in zip(fa, fb)]
    raw = fft(point, r, True)
    base = digit_max + 1
    if base & (base - 1) == 0:
        m = base.bit_length() - 1
        square = (1 << (2 * m)) - (1 << (m + 1)) + 1
    else:
        # Only tiny arbitrary-base coefficient controls take this branch.
        square = school_native(digit_max, digit_max, 2 * digit_max.bit_length() + 1)
    upper = 0
    out = []
    logk = k.bit_length() - 1
    for j, u in enumerate(raw):
        u = shift_residue(u, -logk - j * theta_step, r)
        upper += square
        c = u if u <= upper else u - q
        lower = -(k - 1 - j) * square
        assert lower <= c <= upper
        out.append(c)
    return out


def native(x, y, n):
    """Canonical x*y modulo 2^n+1; native modular recursion throughout."""
    q = (1 << n) + 1
    assert 0 <= x < q and 0 <= y < q
    LEDGER["native_calls"] += 1
    if x == q - 1:
        return 0 if y == 0 else q - y
    if y == q - 1:
        return 0 if x == 0 else q - x
    plan = choose(n) if n > 24 else None
    if plan is None:
        LEDGER["school_leaves"] += 1
        return school_native(x, y, n)
    k, m, r = plan
    LEDGER["fft_nodes"] += 1
    LEDGER["pointwise_calls"] += k
    LEDGER["parent_bits_at_fft_nodes"] += n
    LEDGER["child_bits_at_fft_nodes"] += k * r
    mask = (1 << m) - 1
    def chunks(value):
        raw = memoryview(value.to_bytes((n + 7) // 8, "little"))
        out = []
        for j in range(k):
            start = j * m
            byte = start // 8
            end = (start + m + 7) // 8
            out.append((int.from_bytes(raw[byte:end], "little") >> (start % 8)) & mask)
        return out
    a, b = chunks(x), chunks(y)
    c = negacyclic_coefficients(a, b, mask, r)
    return combine_signed(c, m)


def full(x, y):
    needed = max(1, x.bit_length() + y.bit_length())
    n = 4 * ((needed + 3) // 4)
    return native(x, y, n)


def direct_negacyclic(a, b):
    k = len(a)
    out = [0] * k
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[(i + j) % k] += x * y * (1 if i + j < k else -1)
    return out


def odd_radix_controls(rng, counts):
    """Small independent algebra controls for Q_s=(p^s+1)/2.

    Direct dense DFTs/native arithmetic here are test oracles, not a proposed
    fast implementation or a source of asymptotic multiplication cost.
    """
    for p in [3, 7, 31, 15]:  # first three prime; primality is unnecessary here
        for k in [2, 4, 8]:
            for d in [1, 2, 4]:
                base = p ** d
                bound = k * (base - 1) ** 2
                child_s = k
                while (p ** child_s + 1) // 2 <= bound:
                    child_s += k
                q = (p ** child_s + 1) // 2
                theta = pow(p, child_s // k, q)
                omega = theta * theta % q
                assert q & 1
                assert pow(theta, k, q) == q - 1
                for ell in range(1, k):
                    assert sum(pow(omega, ell * j, q) for j in range(k)) % q == 0
                # The modulus's radix-p representation is explicit.
                digits_q = [(p + 1) // 2] + [(p - 1) // 2] * (child_s - 1)
                assert sum(v * p ** j for j, v in enumerate(digits_q)) == q
                for _ in range(6):
                    a = [rng.randrange(base) for _ in range(k)]
                    b = [rng.randrange(base) for _ in range(k)]
                    def transform(values, inverse=False):
                        return [sum(values[j] * pow(omega, (-1 if inverse else 1) * i * j, q)
                                    for j in range(k)) % q for i in range(k)]
                    fa = transform([a[j] * pow(theta, j, q) % q for j in range(k)])
                    fb = transform([b[j] * pow(theta, j, q) % q for j in range(k)])
                    raw = transform([x * y % q for x, y in zip(fa, fb)], True)
                    out = []
                    for j, u in enumerate(raw):
                        for _ in range(k.bit_length() - 1):
                            if u & 1:
                                u += q
                            u //= 2
                        u = u * pow(theta, -j, q) % q
                        upper = (j + 1) * (base - 1) ** 2
                        out.append(u if u <= upper else u - q)
                    assert out == direct_negacyclic(a, b)
                    parent_q = (p ** (k * d) + 1) // 2
                    av = sum(v * base ** j for j, v in enumerate(a))
                    bv = sum(v * base ** j for j, v in enumerate(b))
                    cv = sum(v * base ** j for j, v in enumerate(out))
                    assert (av * bv - cv) % parent_q == 0
                    counts["odd_radix_native_identity_cases"] += 1


def run():
    rng = random.Random(202610171728)
    counts = Counter()
    for n in range(1, 7):
        q = (1 << n) + 1
        for x in range(q):
            for y in range(q):
                assert native(x, y, n) == x * y % q
                counts["exhaustive_leaf_products"] += 1
    for n in [32, 40, 48, 64, 80, 96, 128, 192, 256, 384]:
        q = (1 << n) + 1
        values = [0, 1, 2, q - 3, q - 2, q - 1]
        for x in values:
            for y in values:
                assert native(x, y, n) == x * y % q
                counts["boundary_native_products"] += 1
        for _ in range(25):
            x, y = rng.randrange(q), rng.randrange(q)
            assert native(x, y, n) == x * y % q
            counts["random_native_products"] += 1
    for bits in [1, 7, 15, 31, 63, 100, 127, 191]:
        for _ in range(20):
            x, y = rng.getrandbits(bits), rng.getrandbits(bits)
            assert full(x, y) == x * y
            counts["full_products"] += 1
    for base in [2, 3, 4, 7, 8, 31, 32, 63, 127]:
        for k in [2, 4, 8, 16]:
            d = k * (base - 1) ** 2
            r = k * ((d.bit_length() + k - 1) // k)
            for _ in range(12):
                a = [rng.randrange(base) for _ in range(k)]
                b = [rng.randrange(base) for _ in range(k)]
                got = negacyclic_coefficients(a, b, base - 1, r)
                want = direct_negacyclic(a, b)
                assert got == want
                # Positional evaluation wraps modulo base^K+1, exactly.
                av = sum(x * base ** j for j, x in enumerate(a))
                bv = sum(x * base ** j for j, x in enumerate(b))
                cv = sum(x * base ** j for j, x in enumerate(got))
                assert (av * bv - cv) % (base ** k + 1) == 0
                counts["signed_negacyclic_cases"] += 1
    # An exact counterexample to substituting 2^(mK)+1 for p^K+1.
    p, m, k = 3, 2, 2
    a = b = [0, 1]
    coeff = direct_negacyclic(a, b)
    assert coeff == [-1, 0]
    assert (p * p - (-1)) % (p ** k + 1) == 0
    assert (p * p - (-1)) % ((1 << (m * k)) + 1) != 0
    counts["wrong_modulus_negative_controls"] += 1
    odd_radix_controls(rng, counts)
    report = {"status": "PASS", "counts": dict(counts), "ledger": dict(LEDGER),
              "scope": "Exact identities and small independent controls only; no timings or asymptotic success claim.",
              "supplied_code_executed": False}
    Path(__file__).with_name("CONTROL_RESULTS.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run()
