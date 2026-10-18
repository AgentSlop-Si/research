"""Precision-targeted Mersenne product interface and two-wide slab schedule.

Inherited arithmetic in dependencies/kernel_stream.py is explicitly pinned.
No native multiplication of represented values in the production functions.
Python native integer arithmetic is used only for small indices/capacities.
This is a reference arithmetic model, not a Python runtime bound.
"""
from dependencies.kernel_stream import (
    karatsuba, parameters, prepare, limb_product, limb_divide, narrow_convolution,
)


def shift_mod(values, sigma, output_bits, product=karatsuba):
    """T_sigma(values) mod 2**output_bits, without a coefficient-height premise."""
    assert sigma in (-1, 1) and output_bits >= 1
    n = len(values)
    out_mask = (1 << output_bits) - 1
    if n < 2:
        return [x & out_mask for x in values]
    guard = (n - 1).bit_length()
    width = output_bits + guard
    t = parameters(n, 0)['t']
    factorial, _, inverses, kernel = prepare(n, t, product)
    mask = (1 << width) - 1
    scaled = []
    for i, value in enumerate(values):
        # Any representative of the input residue is valid.
        x = limb_product(value & out_mask, factorial[i], width, t, product)
        x = (x << (guard - i.bit_count())) & mask
        if sigma < 0 and i & 1:
            x = (-x) & mask
        scaled.append(x)
    convolution = narrow_convolution(scaled[::-1], kernel, width, t, product)
    result = []
    for j in range(n):
        x = limb_divide(convolution[n - 1 - j], factorial[-1], width, t, inverses[-1], product)
        x = limb_divide(x, factorial[j], width, t, inverses[j], product)
        x = (x << j.bit_count()) & mask
        if sigma < 0 and j & 1:
            x = (-x) & mask
        assert x & ((1 << guard) - 1) == 0
        result.append(x >> guard)
    return result


def two_wide_convolution(values, other, width, limb_bits, product=karatsuba, trace=None, stats=None):
    """Ordinary polynomial convolution modulo 2**width, truncated limb pairs.

    Exactly q(q+1)/2 packed products. Each has capacity n*b bits, where
    q=ceil(width/t), b=round8(2*t+ceil(log2(n))), and t=limb_bits.
    Each row has bounded carry; its last carry is discarded modulo 2**width.
    """
    n = len(values)
    assert n >= 1 and len(other) == n
    assert width >= 1 and limb_bits >= 8 and limb_bits % 8 == 0
    assert all(0 <= x < 1 << width for x in values + other)
    g = (n - 1).bit_length()
    slot_bytes = (2 * limb_bits + g + 7) // 8
    slot_bits = 8 * slot_bytes
    limb_bytes = limb_bits // 8
    q = (width + limb_bits - 1) // limb_bits
    count_out = n + n - 1
    sources = [[x.to_bytes(q * limb_bytes, 'little') for x in array] for array in (values, other)]
    outputs = [bytearray(q * limb_bytes) for _ in range(count_out)]
    limb_mask = (1 << limb_bits) - 1
    calls = 0
    for r in range(q):
        rstart = r * limb_bytes
        left = [int.from_bytes(raw[rstart:rstart + limb_bytes], 'little') for raw in sources[0]]
        packed_left = int.from_bytes(b''.join(x.to_bytes(slot_bytes, 'little') for x in left), 'little')
        carries = [0] * count_out
        for s in range(q - r):
            sstart = s * limb_bytes
            right = [int.from_bytes(raw[sstart:sstart + limb_bytes], 'little') for raw in sources[1]]
            packed_right = int.from_bytes(b''.join(x.to_bytes(slot_bytes, 'little') for x in right), 'little')
            packed_result = product(packed_left, packed_right)
            calls += 1
            raw_result = packed_result.to_bytes(2 * n * slot_bytes, 'little')
            out_start = (r + s) * limb_bytes
            for j in range(count_out):
                coefficient = int.from_bytes(raw_result[j * slot_bytes:(j + 1) * slot_bytes], 'little')
                old = int.from_bytes(outputs[j][out_start:out_start + limb_bytes], 'little')
                combined = coefficient + old + carries[j]
                next_carry = combined >> limb_bits
                digit = combined & limb_mask
                if trace is not None:
                    trace(r, s, j, left, right, coefficient, old, carries[j], next_carry, digit)
                outputs[j][out_start:out_start + limb_bytes] = digit.to_bytes(limb_bytes, 'little')
                carries[j] = next_carry
        # All remaining row carries start at radix position q and vanish.
    if stats is not None:
        stats.update(n=n, H=width, t=limb_bits, q=q, b=slot_bits, S=n * slot_bits,
                     packed_calls=calls, expected_calls=q * (q + 1) // 2)
    mask = (1 << width) - 1
    return [int.from_bytes(raw, 'little') & mask for raw in outputs]


def binary_chunks(value, m, length):
    assert value >= 0 and m >= 2 and value.bit_length() <= m * length
    source = value.to_bytes((m * length + 7) // 8, 'little')
    result = []
    mask = (1 << m) - 1
    for i in range(length):
        position = i * m
        start, offset = divmod(position, 8)
        span = (offset + m + 7) // 8
        result.append((int.from_bytes(source[start:start + span], 'little') >> offset) & mask)
    return result


def reconstruct_binary(coefficients, m):
    """Carry into m-bit digits, then assemble via fixed byte output windows."""
    assert m >= 2 and all(c >= 0 for c in coefficients)
    mask, carry, digits = (1 << m) - 1, 0, []
    for coefficient in coefficients:
        combined = coefficient + carry
        digits.append(combined & mask)
        carry = combined >> m
    while carry:
        digits.append(carry & mask)
        carry >>= m
    output = bytearray((len(digits) * m + 7) // 8)
    for i, digit in enumerate(digits):
        start, offset = divmod(i * m, 8)
        span = (m + offset + 7) // 8
        raw = (digit << offset).to_bytes(span, 'little')
        output[start] |= raw[0]
        output[start + 1:start + span] = raw[1:]
    return int.from_bytes(output, 'little')


def multiply_interface(x, y, m, length, limb_bits=None, product=karatsuba, stats=None):
    """Complete correct multiplier; no speedup of general multiplication claimed."""
    assert length >= 1 and m >= 2
    left = binary_chunks(x, m, length)
    right = binary_chunks(y, m, length)
    H = 2 * m + (length - 1).bit_length()
    a = shift_mod(left, 1, H, product)
    b = shift_mod(right, 1, H, product)
    if limb_bits is None:
        limb_bits = parameters(max(2, length), 0)['t']
    ledger = {}
    raw = two_wide_convolution(a, b, H, limb_bits, product, stats=ledger)
    exact_binary_convolution = shift_mod(raw, -1, H, product)
    if stats is not None:
        stats.update(ledger)
        stats['H_final'] = H
        stats['raw_output_length'] = len(raw)
        stats['final_coefficients'] = exact_binary_convolution
    return reconstruct_binary(exact_binary_convolution, m)
