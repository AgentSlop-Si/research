"""Exact small-coefficient lift and streaming boundary evaluation.

This checks a proposed representation, not a faster asymptotic algorithm.
It imports only the fresh companion experiment, never historical source.
"""
from random import Random
from math import isqrt
import json
from lazy_fermat import Plan, transform


def lift(x, w, d):
    mask = (1 << w) - 1
    raw = x.to_bytes((w * d + 7) // 8, 'little')
    view = memoryview(raw)
    out = []
    byte = offset = 0
    step_bytes, step_bits = divmod(w, 8)
    for _ in range(d):
        stop = byte + (w + offset + 7) // 8
        out.append((int.from_bytes(view[byte:stop], 'little') >> offset) & mask)
        byte += step_bytes
        offset += step_bits
        if offset >= 8:
            offset -= 8
            byte += 1
    return out


def signed_rotate(a, exponent):
    d = len(a)
    exponent %= 2 * d
    sign = -1 if exponent >= d else 1
    s = exponent % d
    out = [0] * d
    for j, x in enumerate(a):
        target = j + s
        out[target % d] = sign * (-x if target >= d else x)
    return out


def stream_evaluate(coefficients, w, k):
    """Bounded-width carry propagation and byte packing; no growing Horner."""
    mask = (1 << w) - 1
    out = bytearray()
    carry = buffer = used = 0
    for c in coefficients:
        t = c + carry
        digit, carry = t & mask, t >> w
        assert abs(carry) <= k
        buffer |= digit << used
        used += w
        whole = used // 8
        if whole:
            bits = 8 * whole
            out.extend((buffer & ((1 << bits) - 1)).to_bytes(whole, 'little'))
            buffer >>= bits
            used -= bits
    if used:
        out.append(buffer)
    q = (1 << (w * len(coefficients))) + 1
    value = int.from_bytes(out, 'little') - carry
    if value < 0:
        value += q
    elif value >= q:
        value -= q
    assert 0 <= value < q
    return value


def lifted_transform(values, inverse, p):
    k, d = p.k, p.k // 2
    w = p.r // d
    B = 1 << w
    assert p.r == w * d
    # The canonical exceptional value 2**r represents -1, not d zero digits.
    arrays = [([-1] + [0] * (d - 1)) if x == p.q - 1 else lift(x, w, d)
              for x in values]
    length = 2 if inverse else k
    stage = 0
    while (length <= k if inverse else length >= 2):
        half = length // 2
        step = k // length
        for start in range(0, k, length):
            for j in range(half):
                u, v = arrays[start + j], arrays[start + j + half]
                if inverse and j:
                    v = signed_rotate(v, -j * step)
                x = [a + b for a, b in zip(u, v)]
                y = [a - b for a, b in zip(u, v)]
                if not inverse and j:
                    y = signed_rotate(y, j * step)
                arrays[start + j], arrays[start + j + half] = x, y
        stage += 1
        assert all(abs(c) <= (1 << stage) * (B - 1)
                   for a in arrays for c in a)
        length = length * 2 if inverse else length // 2
    evaluated = [stream_evaluate(a, w, k) for a in arrays]
    if inverse:
        # Boundary normalization only; this validation does not claim it free.
        scale = pow(k, -1, p.q)
        evaluated = [x * scale % p.q for x in evaluated]
    return evaluated


def validate():
    rng = Random(202610171738)
    tests = 0
    carry_tests = 0
    for k in (2, 4, 8, 16, 32, 64):
        for w in (1, 2, 3, 7, 8, 15, 16, 31):
            p = Plan(k, w * k // 2)
            for sample in range(8):
                values = [rng.randrange(p.q) for _ in range(k)]
                if sample == 0:
                    values = [p.q - 1] * k
                elif sample == 1:
                    values = [0 if j & 1 else p.q - 1 for j in range(k)]
                for inverse in (False, True):
                    expected = transform(values, inverse, p, False)
                    actual = lifted_transform(values, inverse, p)
                    assert actual == expected
                    tests += 1
                bound = k * ((1 << w) - 1)
                coefficients = [rng.randint(-bound, bound) for _ in range(k // 2)]
                direct = sum(c << (j * w) for j, c in enumerate(coefficients)) % p.q
                assert stream_evaluate(coefficients, w, k) == direct
                carry_tests += 1
    return {'lifted_transform_cases': tests, 'streaming_signed_carry_cases': carry_tests}


def parameter_rows():
    rows = []
    for ell in (8, 16, 24, 32, 64, 128, 256, 512):
        n = 1 << ell
        target = n * ell
        m = isqrt(target)
        if m * m < target:
            m += 1
        # 2**m-1 >= 2**(m-1), so this safely bounds Mersenne digit count too.
        L = (n + m - 2) // (m - 1)
        k = 1 << (2 * L - 2).bit_length()
        d = k // 2
        # Certified coefficient-bit upper bound, without constructing 2**m.
        b = 2 * m + (L - 1).bit_length() + 1
        r = ((b + d - 1) // d) * d
        w = r // d
        guard_width = w + k.bit_length()  # sign and stage envelope
        rows.append({'log2_N': ell, 'm': m, 'K': k, 'r': r, 'w': w,
                     'guard_width': guard_width,
                     'final_storage_bits_over_N': (k * d * guard_width) / n,
                     'ring_storage_bits_over_N': k * r / n})
    return rows


if __name__ == '__main__':
    print(json.dumps({'validation': validate(), 'parameter_rows': parameter_rows()}, indent=2))
