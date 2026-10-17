"""Fresh exact 2-adic Taylor shift and Mersenne conversion controls.

No historical code is imported. The implementation uses no built-in wide
integer multiplication, division, modular inverse, factorial or binomial.
Python multiplication/division is used only in independent test oracles and
small loop/array-index arithmetic. General products use explicit Karatsuba;
its leaves and short-factor products use binary shift/add multiplication.
"""
from dataclasses import dataclass, field
import hashlib
import itertools
import json
import math
from pathlib import Path
import random


@dataclass
class Ledger:
    collect_recursive_metrics: bool = False
    general_calls: int = 0
    general_argument_width_sum: int = 0
    max_general_width: int = 0
    karatsuba_nodes: int = 0
    karatsuba_width_sum: int = 0
    short_calls: int = 0
    short_width_charge: int = 0
    mersenne_divisions: int = 0
    mersenne_folds: int = 0
    max_folds: int = 0
    mersenne_chunk_steps: int = 0
    max_mersenne_chunks: int = 0
    shifts: list = field(default_factory=list)


def schoolbook(x, y):
    """Nonnegative exact multiplication using shifts and additions."""
    z = 0
    while y:
        if y & 1:
            z += x
        x <<= 1
        y >>= 1
    return z


def kara_nonnegative(x, y, ledger):
    n = max(x.bit_length(), y.bit_length())
    if ledger.collect_recursive_metrics:
        # Optional diagnostics, excluded from the arithmetic-core bit bound.
        # Disabled by default to avoid a growing global counter at every leaf.
        ledger.karatsuba_nodes += 1
        ledger.karatsuba_width_sum += n
    if not x or not y:
        return 0
    if n <= 32:
        return schoolbook(x, y)
    k = (n + 1) // 2
    mask = (1 << k) - 1
    xl, xh = x & mask, x >> k
    yl, yh = y & mask, y >> k
    lo = kara_nonnegative(xl, yl, ledger)
    hi = kara_nonnegative(xh, yh, ledger)
    cross = kara_nonnegative(xl + xh, yl + yh, ledger) - lo - hi
    return lo + (cross << k) + (hi << (k + k))


def mul(x, y, ledger):
    ledger.general_calls += 1
    w = max(abs(x).bit_length(), abs(y).bit_length())
    ledger.general_argument_width_sum += w
    ledger.max_general_width = max(ledger.max_general_width, w)
    z = kara_nonnegative(abs(x), abs(y), ledger)
    return -z if (x < 0) != (y < 0) else z


def mul_short(x, k, ledger):
    assert x >= 0 and k >= 0
    ledger.short_calls += 1
    ledger.short_width_charge += (x.bit_length() + k.bit_length()) * max(1, k.bit_length())
    return schoolbook(x, k)


def inverse_odd(u, width, ledger):
    assert u & 1 and width >= 1
    x, bits = 1, 1
    while bits < width:
        bits = min(bits + bits, width)
        mask = (1 << bits) - 1
        z = mul(u & mask, x, ledger) & mask
        x = mul(x, (2 - z) & mask, ledger) & mask
    return x


def convolution_mod_power_two(a, b, width, ledger):
    """One exact Kronecker product, using fixed byte windows both ways."""
    n = max(len(a), len(b))
    logn = (n - 1).bit_length()
    byte_width = (width + width + logn + 7) // 8
    packed_bits = 8 * byte_width
    aa = int.from_bytes(b''.join(x.to_bytes(byte_width, 'little') for x in a), 'little')
    bb = int.from_bytes(b''.join(x.to_bytes(byte_width, 'little') for x in b), 'little')
    product = mul(aa, bb, ledger)
    count = len(a) + len(b) - 1
    data = product.to_bytes(count * byte_width, 'little')
    mask = (1 << width) - 1
    out = [int.from_bytes(data[i * byte_width:(i + 1) * byte_width], 'little') & mask
           for i in range(count)]
    return out, packed_bits * n


def taylor_shift(coefficients, sigma, ledger):
    """Return coefficients of f(X+sigma), sigma in {-1,+1}, exactly."""
    assert sigma in (-1, 1)
    n = len(coefficients)
    if not n:
        return []
    a = max(1, max(abs(x).bit_length() for x in coefficients))
    height = a + n + 1
    guard = (n - 1).bit_length()
    width = height + guard
    mask = (1 << width) - 1
    odd = [1] * n
    u = [1] * n
    for i in range(1, n):
        odd[i] = i >> ((i & -i).bit_length() - 1)
        u[i] = mul_short(u[i - 1], odd[i], ledger) & mask
    v = [0] * n
    v[-1] = inverse_odd(u[-1], width, ledger)
    for i in range(n - 1, 0, -1):
        v[i - 1] = mul_short(v[i], odd[i], ledger) & mask
    g = [(v[i] << i.bit_count()) & mask for i in range(n)]
    aa = [((mul(u[i], coefficients[i] & mask, ledger) & mask)
           << (guard - i.bit_count())) & mask for i in range(n)]
    kernel = [((-g[i]) & mask) if sigma < 0 and i & 1 else g[i] for i in range(n)]
    convolution, packed_capacity = convolution_mod_power_two(aa[::-1], kernel, width, ledger)
    out = []
    sign_bit = 1 << (height - 1)
    modulus = 1 << height
    for j in range(n):
        residue = mul(g[j], convolution[n - 1 - j], ledger) & mask
        assert residue & ((1 << guard) - 1) == 0
        residue >>= guard
        out.append(residue - modulus if residue >= sign_bit else residue)
    ledger.shifts.append({'length': n, 'input_height': a, 'reconstruction_bits': height,
                         'guard_bits': guard, 'working_bits': width,
                         'packed_argument_capacity': packed_capacity,
                         'output_height': max(abs(x).bit_length() for x in out)})
    return out


def binary_chunks(x, m):
    assert x >= 0 and m >= 2
    count = max(1, (x.bit_length() + m - 1) // m)
    data = x.to_bytes(max(1, (x.bit_length() + 7) // 8), 'little')
    mask = (1 << m) - 1
    out = []
    for i in range(count):
        start, off = divmod(i * m, 8)
        size = (off + m + 7) // 8
        out.append((int.from_bytes(data[start:start + size], 'little') >> off) & mask)
    return out


def binary_assemble(digits, m):
    """Write bounded windows; never grow a whole-number Horner accumulator."""
    out = bytearray((len(digits) * m + 7) // 8)
    for i, digit in enumerate(digits):
        assert 0 <= digit < (1 << m)
        start, off = divmod(i * m, 8)
        chunk = (digit << off).to_bytes((m + off + 7) // 8, 'little')
        for j, value in enumerate(chunk):
            if start + j < len(out):
                out[start + j] |= value
            else:
                assert value == 0
    return int.from_bytes(out, 'little')


def normalize_binary(coefficients, m):
    mask = (1 << m) - 1
    carry, digits = 0, []
    for coefficient in coefficients:
        value = coefficient + carry
        digits.append(value & mask)
        carry = value >> m
    if carry < 0:
        raise ValueError('The represented integer is negative.')
    if carry:
        digits.extend(binary_chunks(carry, m))
    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()
    return digits


def mersenne_fold_divmod(value, m, ledger):
    p = (1 << m) - 1
    quotient, folds = 0, 0
    while value < 0 or value > p:
        high, low = value >> m, value & p
        quotient += high
        value = high + low
        folds += 1
    if value == p:
        quotient += 1
        value = 0
    ledger.mersenne_divisions += 1
    ledger.mersenne_folds += folds
    ledger.max_folds = max(ledger.max_folds, folds)
    return quotient, value


def mersenne_divmod(value, m, ledger):
    """Exact signed division by 2^m-1, with O(width) local chunk work.

    If old remainder r<p and a is the next B-digit, r*B+a =
    (r+delta)*p + (r+a-delta*p), delta=[r+a>=p].
    """
    negative = value < 0
    chunks = binary_chunks(abs(value), m)
    p = (1 << m) - 1
    quotient = [0] * len(chunks)
    remainder = 0
    for i in range(len(chunks) - 1, -1, -1):
        total = remainder + chunks[i]
        delta = int(total >= p)
        quotient[i] = remainder + delta
        remainder = total - p if delta else total
        assert 0 <= quotient[i] < (1 << m) and 0 <= remainder < p
    q = binary_assemble(quotient, m)
    ledger.mersenne_divisions += 1
    ledger.mersenne_chunk_steps += len(chunks)
    ledger.max_mersenne_chunks = max(ledger.max_mersenne_chunks, len(chunks))
    if negative:
        return (-q - 1, p - remainder) if remainder else (-q, 0)
    return q, remainder


def normalize_mersenne(coefficients, m, ledger):
    carry, digits = 0, []
    for coefficient in coefficients:
        carry, digit = mersenne_divmod(coefficient + carry, m, ledger)
        digits.append(digit)
    if carry < 0:
        raise ValueError('The represented integer is negative.')
    while carry:
        carry, digit = mersenne_divmod(carry, m, ledger)
        digits.append(digit)
    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()
    return digits


def binary_to_p(x, m, ledger, canonical=True):
    redundant = taylor_shift(binary_chunks(x, m), 1, ledger)
    return normalize_mersenne(redundant, m, ledger) if canonical else redundant


def p_to_binary(coefficients, m, ledger):
    shifted = taylor_shift(coefficients, -1, ledger)
    return binary_assemble(normalize_binary(shifted, m), m)


def binary_to_grouped(x, m, d, ledger):
    assert d >= 1
    coefficients = binary_to_p(x, m, ledger)
    return [p_to_binary(coefficients[i:i + d], m, ledger)
            for i in range(0, len(coefficients), d)]


def grouped_to_binary(groups, m, d, ledger):
    assert d >= 1
    if len(groups) == 1:
        # Validate the canonical promise using the actual input width, then
        # return the existing integer. Never allocate d leading zero positions.
        digits = binary_to_p(groups[0], m, ledger)
        if len(digits) > d:
            raise ValueError('Noncanonical grouped digit.')
        return groups[0]
    coefficients = []
    for group in groups:
        digits = binary_to_p(group, m, ledger)
        if len(digits) > d:
            raise ValueError('Noncanonical grouped digit.')
        coefficients.extend(digits + [0] * (d - len(digits)))
    return p_to_binary(coefficients, m, ledger)


def grouped_raw_to_binary(groups, m, d, ledger):
    """Read raw signed p^d coefficients without repeated division by p^d."""
    coefficients = []
    for j, group in enumerate(groups):
        digits = binary_to_p(abs(group), m, ledger)
        needed = j * d + len(digits)
        coefficients.extend([0] * max(0, needed - len(coefficients)))
        for k, digit in enumerate(digits):
            coefficients[j * d + k] += -digit if group < 0 else digit
    return p_to_binary(coefficients, m, ledger)


def ordinary_convolution(a, b, ledger):
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += mul(ai, bj, ledger)
    return out


def oracle_shift(a, sigma):
    return [sum(math.comb(i, j) * a[i] * (sigma ** (i - j))
                for i in range(j, len(a))) for j in range(len(a))]


def oracle_p_digits(x, p):
    out = []
    while x:
        x, r = divmod(x, p)
        out.append(r)
    return out or [0]


def run_controls():
    rng = random.Random(202610171728)
    ledger = Ledger()
    counts = {'karatsuba_oracles': 0, 'odd_inverses': 0, 'exact_shifts': 0,
              'binary_roundtrips': 0, 'grouped_roundtrips': 0,
              'signed_mersenne_divisions': 0, 'lazy_products': 0,
              'raw_p_products': 0, 'raw_grouped_products': 0,
              'local_division_transitions': 0, 'single_group_edges': 0,
              'negative_controls': 0}
    for n in [0, 1, 2, 31, 32, 33, 127, 512, 1024, 4097]:
        for _ in range(4):
            a, b = rng.getrandbits(n), rng.getrandbits(n)
            assert mul(a, b, ledger) == a * b
            counts['karatsuba_oracles'] += 1
    for width in [1, 2, 7, 16, 31, 64, 127, 513]:
        for _ in range(4):
            u = rng.getrandbits(width) | 1
            inverse = inverse_odd(u, width, ledger)
            assert (u * inverse) & ((1 << width) - 1) == 1
            counts['odd_inverses'] += 1
    for n in range(1, 33):
        for width in [1, 7, 33]:
            a = [rng.randrange(-(1 << width), 1 << width) for _ in range(n)]
            for sigma in [-1, 1]:
                assert taylor_shift(a, sigma, ledger) == oracle_shift(a, sigma)
                counts['exact_shifts'] += 1
    for n, width in [(64, 64), (65, 192), (128, 256)]:
        a = [rng.getrandbits(width) for _ in range(n)]
        b = taylor_shift(a, 1, ledger)
        assert b == oracle_shift(a, 1)
        assert taylor_shift(b, -1, ledger) == a
        counts['exact_shifts'] += 2
    for m in [2, 3, 5, 8, 17, 32, 64, 127]:
        p = (1 << m) - 1
        for bits in [1, m - 1, m, m + 1, 3 * m, 8 * m]:
            for x in [0, (1 << bits) - 1, rng.getrandbits(bits)]:
                digits = binary_to_p(x, m, ledger)
                assert digits == oracle_p_digits(x, p)
                assert p_to_binary(digits, m, ledger) == x
                counts['binary_roundtrips'] += 1
        for d in [1, 2, 3, 7]:
            x = rng.getrandbits(7 * m + 1)
            groups = binary_to_grouped(x, m, d, ledger)
            assert groups == oracle_p_digits(x, p ** d)
            assert grouped_to_binary(groups, m, d, ledger) == x
            counts['grouped_roundtrips'] += 1
        for width in [m, 2 * m, 3 * m + 7]:
            for _ in range(5):
                x = rng.randrange(-(1 << width), 1 << width)
                assert mersenne_divmod(x, m, ledger) == divmod(x, p)
                assert mersenne_fold_divmod(x, m, ledger) == divmod(x, p)
                counts['signed_mersenne_divisions'] += 1
        for n in [1, 2, 5, 12]:
            x, y = rng.getrandbits(m * n), rng.getrandbits(m * n)
            bx, by = binary_chunks(x, m), binary_chunks(y, m)
            px = taylor_shift(bx, 1, ledger)
            py = taylor_shift(by, 1, ledger)
            product = ordinary_convolution(px, py, ledger)
            back = taylor_shift(product, -1, ledger)
            assert back == ordinary_convolution(bx, by, ledger)
            assert binary_assemble(normalize_binary(back, m), m) == x * y
            counts['lazy_products'] += 1
            ax, ay = binary_to_p(x, m, ledger), binary_to_p(y, m, ledger)
            raw = ordinary_convolution(ax, ay, ledger)
            assert p_to_binary(raw, m, ledger) == x * y
            counts['raw_p_products'] += 1
    for m in [2, 3, 5]:
        p = (1 << m) - 1
        for r in range(p):
            for a in range(1 << m):
                delta = int(r + a >= p)
                assert divmod((r << m) + a, p) == (r + delta, r + a - delta * p)
                assert 0 <= r + delta < 1 << m
                counts['local_division_transitions'] += 1
    for m in [3, 8, 32, 64]:
        for d in [1, 2, 3, 7]:
            x, y = rng.getrandbits(m * d * 3), rng.getrandbits(m * d * 3)
            xx = binary_to_grouped(x, m, d, ledger)
            yy = binary_to_grouped(y, m, d, ledger)
            raw = ordinary_convolution(xx, yy, ledger)
            assert grouped_raw_to_binary(raw, m, d, ledger) == x * y
            counts['raw_grouped_products'] += 1
    for m, x in [(2, 0), (5, (1 << 123) - 1), (17, rng.getrandbits(257))]:
        actual_digits = len(oracle_p_digits(x, (1 << m) - 1))
        for d in [actual_digits + 1, 1_000_000]:
            local = Ledger()
            assert grouped_to_binary([x], m, d, local) == x
            # Validation performs one shift on the actual binary chunk count;
            # d does not enter any shift or padded array size.
            assert len(local.shifts) == 1
            assert local.shifts[0]['length'] == len(binary_chunks(x, m))
            counts['single_group_edges'] += 1
        p = (1 << m) - 1
        try:
            grouped_to_binary([p ** 3], m, 3, Ledger())
        except ValueError:
            counts['single_group_edges'] += 1
        else:
            raise AssertionError('Invalid single grouped digit accepted.')
    # Negative controls detect dropped quotient, wrong sign and factorial guard.
    assert mersenne_divmod(36, 3, ledger)[1] != 36
    counts['negative_controls'] += 1
    assert p_to_binary([1, 2, 3], 3, ledger) != binary_assemble([1, 2, 3], 3)
    counts['negative_controls'] += 1
    # 2^K*c mod 2^H alone loses the top K bits of c on division by 2^K.
    c, height, guard = 7, 3, 2
    assert ((c << guard) & ((1 << height) - 1)) >> guard != c
    counts['negative_controls'] += 1
    selected = []
    for n, m in [(8, 8), (16, 32), (32, 64), (64, 192), (128, 256)]:
        local = Ledger()
        x = (1 << (n * m)) - 1
        p = binary_to_p(x, m, local)
        assert p_to_binary(p, m, local) == x
        selected.append({'input_bits': n * m, 'm': m, 'binary_digit_count': n,
                         'canonical_p_digit_count': len(p),
                         'max_mersenne_chunk_steps_per_digit': local.max_mersenne_chunks,
                         'general_multiplication_calls': local.general_calls,
                         'max_general_argument_bits': local.max_general_width,
                         'shifts': local.shifts})
    return {'status': 'all_passed', 'seed': 202610171728, 'counts': counts,
            'algorithm_native_wide_multiplication_calls': 0,
            'algorithm_native_wide_division_calls': 0,
            'algorithm_native_modular_inverse_calls': 0,
            'selected_exact_metadata': selected,
            'aggregate_ledger': {k: v for k, v in ledger.__dict__.items()
                                 if k not in ('shifts', 'karatsuba_nodes', 'karatsuba_width_sum')},
            'interpretation': 'Correctness and exact operation metadata only; no speed or asymptotic claim inferred from tests.'}


if __name__ == '__main__':
    results = run_controls()
    path = Path(__file__).with_name('CONTROL_RESULTS.json')
    path.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))
