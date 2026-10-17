#!/usr/bin/env python3
"""Exact signed outer convolutions, with all packed operand sizes reported.

This is classical Kronecker substitution, supplied as a prime-free all-size
completion of the outer-convolution interface.  A Python integer product is
an explicitly reported subroutine, not a claimed free operation or a new
sub-NlogN multiplier.  Packing and extraction use bounded byte windows.
"""
from dataclasses import dataclass, field


@dataclass
class PackingCounts:
    coefficient_scans: int = 0
    packing_window_bytes: int = 0
    unpacking_window_bytes: int = 0
    packed_stream_subtractions: int = 0
    output_sign_extensions: int = 0
    output_coefficient_additions: int = 0
    products: list = field(default_factory=list)


def _pack_signed(values, byte_width, counts):
    """Evaluate at Q=256**byte_width by two nonnegative streams."""
    size = len(values) * byte_width
    positive, negative = bytearray(size), bytearray(size)
    for i, value in enumerate(values):
        blob = abs(value).to_bytes(byte_width, 'little')
        start = i * byte_width
        target = negative if value < 0 else positive
        target[start:start + byte_width] = blob
        counts.packing_window_bytes += byte_width
    counts.packed_stream_subtractions += 1
    return int.from_bytes(positive, 'little') - int.from_bytes(negative, 'little')


def _unpack_balanced(value, length, byte_width, bound, counts):
    """Read fixed slots of two's-complement data, propagating a one-bit borrow.

    Unlike repeated division of the entire packed integer, the loop touches
    one bounded slot at a time.  The final borrow records the global sign.
    """
    bits = 8 * byte_width
    Q = 1 << bits
    negative = value < 0
    if negative:
        value += 1 << (bits * length)
        counts.output_sign_extensions += 1
    if not 0 <= value < (1 << (bits * length)):
        raise ArithmeticError('packed product exceeds output allocation')
    stream = value.to_bytes(length * byte_width, 'little')
    carry, result = 0, []
    for i in range(length):
        start = i * byte_width
        slot = int.from_bytes(stream[start:start + byte_width], 'little') + carry
        counts.unpacking_window_bytes += byte_width
        if slot >= Q // 2:
            digit, carry = slot - Q, 1
        else:
            digit, carry = slot, 0
        if abs(digit) > bound:
            raise ArithmeticError('recovered coefficient exceeds prior envelope')
        result.append(digit)
    if carry != int(negative):
        raise ArithmeticError('final signed-slot borrow mismatch')
    return result


def convolution(a, b, counts=None):
    """Return a*b and its prior certificate; exactly one product unless zero.

    The allocated product operand lengths, including guard slots, are the
    relevant recurrence sizes.  Actual lengths are separately observed.
    """
    if counts is None:
        counts = PackingCounts()
    if not a or not b:
        raise ValueError('nonempty coefficient lists required')
    if any(not isinstance(x, int) for x in (*a, *b)):
        raise TypeError('integer coefficients required')
    counts.coefficient_scans += len(a) + len(b)
    maximum_a, maximum_b = max(map(abs, a)), max(map(abs, b))
    overlap = min(len(a), len(b))
    bound = overlap * maximum_a * maximum_b
    output_length = len(a) + len(b) - 1
    if not bound:
        return [0] * output_length, {'bound': 0, 'slot_bits': 0}
    # Strictly 2*bound < 2**bits, so centered recovery is unique.
    byte_width = max(1, ((2 * bound).bit_length() + 7) // 8)
    bits = byte_width * 8
    left = _pack_signed(a, byte_width, counts)
    right = _pack_signed(b, byte_width, counts)
    counts.products.append({
        'allocated_left_bits': len(a) * bits,
        'allocated_right_bits': len(b) * bits,
        'actual_left_bits': abs(left).bit_length(),
        'actual_right_bits': abs(right).bit_length(),
        'slot_bits': bits,
        'output_slots': output_length,
    })
    product = left * right
    return _unpack_balanced(product, output_length, byte_width, bound, counts), {
        'bound': bound, 'slot_bits': bits, 'overlap': overlap,
        'input_maximum_a': maximum_a, 'input_maximum_b': maximum_b,
    }


def jet_products(a, u, c, v, counts=None):
    """p=a*c, e=u*c+a*v; rows are nodes, columns are outer coefficients."""
    if counts is None:
        counts = PackingCounts()
    if not a or not (len(a) == len(u) == len(c) == len(v)):
        raise ValueError('matching nonempty nodal arrays required')
    low, derivative, certificates = [], [], []
    for ar, ur, cr, vr in zip(a, u, c, v):
        if len(ar) != len(ur) or len(cr) != len(vr):
            raise ValueError('jet width mismatch')
        p, cp = convolution(ar, cr, counts)
        e1, ce1 = convolution(ur, cr, counts)
        e2, ce2 = convolution(ar, vr, counts)
        e = [x + y for x, y in zip(e1, e2)]
        counts.output_coefficient_additions += len(e)
        low.append(p)
        derivative.append(e)
        certificates.append({'p': cp, 'e_first': ce1, 'e_second': ce2,
                             'e_bound': ce1['bound'] + ce2['bound']})
    return low, derivative, certificates


def values_products(a, c, counts=None):
    """One ordinary outer convolution at each independently prepared node."""
    if counts is None:
        counts = PackingCounts()
    if not a or len(a) != len(c):
        raise ValueError('matching nonempty nodal arrays required')
    output, certificates = [], []
    for ar, cr in zip(a, c):
        row, certificate = convolution(ar, cr, counts)
        output.append(row)
        certificates.append(certificate)
    return output, certificates
