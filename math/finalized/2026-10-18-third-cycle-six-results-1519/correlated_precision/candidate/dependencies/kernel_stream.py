"""Denominator-cleared, narrow-kernel, slab-streamed Taylor shifts.

A fresh implementation for the accepted sequential-bit/array arithmetic model.
No historical program is imported. Native multiplication of represented values
is confined to optional externally supplied correctness oracles, never defaults.
"""
LEAF_BITS = 16


def karatsuba(x, y):
    """Conventional independently terminating difference-form Karatsuba."""
    if x < 0 or y < 0:
        answer = karatsuba(abs(x), abs(y))
        return -answer if (x < 0) != (y < 0) else answer
    width = max(x.bit_length(), y.bit_length())
    if width <= LEAF_BITS:
        answer = 0
        while y:
            if y & 1:
                answer += x
            x <<= 1
            y >>= 1
        return answer
    split = (width + 1) // 2
    mask = (1 << split) - 1
    xl, xh = x & mask, x >> split
    yl, yh = y & mask, y >> split
    low, high = karatsuba(xl, yl), karatsuba(xh, yh)
    dx, dy = xh - xl, yh - yl
    difference = karatsuba(abs(dx), abs(dy))
    if (dx < 0) != (dy < 0):
        difference = -difference
    middle = low + high - difference
    return low + (middle << split) + (high << (split + split))


def odd_part(i):
    assert i > 0
    return i >> ((i & -i).bit_length() - 1)


def odd_inverse(u, width, product=karatsuba):
    assert u > 0 and u & 1 and width >= 1
    inverse, precision = 1, 1
    while precision < width:
        precision = min(precision + precision, width)
        mask = (1 << precision) - 1
        correction = (2 - (product(u & mask, inverse) & mask)) & mask
        inverse = product(inverse, correction) & mask
    return inverse


def limb_product(value, factor, width, limb_bits, product=karatsuba):
    """value * factor modulo 2**width using short products only."""
    assert width >= 1 and limb_bits >= 8 and limb_bits % 8 == 0
    assert 0 <= value < 1 << width and 0 <= factor < 1 << limb_bits
    count = (width + limb_bits - 1) // limb_bits
    limb_bytes = limb_bits // 8
    raw = value.to_bytes(count * limb_bytes, 'little')
    output = bytearray(len(raw))
    mask, carry = (1 << limb_bits) - 1, 0
    for position in range(0, len(raw), limb_bytes):
        digit = int.from_bytes(raw[position:position + limb_bytes], 'little')
        combined = product(digit, factor) + carry
        output[position:position + limb_bytes] = (combined & mask).to_bytes(limb_bytes, 'little')
        carry = combined >> limb_bits
    return int.from_bytes(output, 'little') & ((1 << width) - 1)


def limb_divide(value, divisor, width, limb_bits, inverse, product=karatsuba, trace=None):
    """value / divisor modulo 2**width; a modular, not ordinary, quotient."""
    assert width >= 1 and limb_bits >= 8 and limb_bits % 8 == 0
    assert 0 <= value < 1 << width and 0 < divisor < 1 << limb_bits and divisor & 1
    count = (width + limb_bits - 1) // limb_bits
    limb_bytes = limb_bits // 8
    raw = value.to_bytes(count * limb_bytes, 'little')
    output = bytearray(len(raw))
    mask, carry = (1 << limb_bits) - 1, 0
    for position in range(0, len(raw), limb_bytes):
        digit = int.from_bytes(raw[position:position + limb_bytes], 'little')
        quotient = product((digit - carry) & mask, inverse) & mask
        numerator = product(divisor, quotient) + carry - digit
        next_carry = numerator >> limb_bits
        if trace is not None:
            trace(digit, quotient, carry, next_carry, numerator)
        carry = next_carry
        output[position:position + limb_bytes] = quotient.to_bytes(limb_bytes, 'little')
    return int.from_bytes(output, 'little') & ((1 << width) - 1)


def parameters(n, h):
    assert n >= 2 and h >= 0
    guard = (n - 1).bit_length()
    output_bits = h + n + 1
    width = output_bits + guard
    factorial_cap = (n - 1) * guard
    limb_bits = 8 * ((factorial_cap + guard + 1 + 7) // 8)
    slot_bits = 8 * ((limb_bits + limb_bits + guard + 7) // 8)
    return {
        'n': n, 'h': h, 'g': guard, 'H': output_bits, 'W': width,
        'factorial_cap': factorial_cap, 't': limb_bits,
        'b': slot_bits, 'S': n * slot_bits,
        'q': (width + limb_bits - 1) // limb_bits,
    }


def prepare(n, limb_bits, product=karatsuba):
    """Exact u_i, exact U/u_i, and every microinverse, all paid."""
    short_bits = 8 * ((max(1, (n - 1).bit_length()) + 7) // 8)
    factorial = [1] * n
    for i in range(1, n):
        factorial[i] = limb_product(factorial[i - 1], odd_part(i), limb_bits, short_bits, product)
    cofactors = [1] * n
    for i in range(n - 1, 0, -1):
        cofactors[i - 1] = limb_product(cofactors[i], odd_part(i), limb_bits, short_bits, product)
    inverses = [0] * n
    inverses[-1] = odd_inverse(factorial[-1], limb_bits, product)
    for i in range(n - 1, 0, -1):
        inverses[i - 1] = limb_product(inverses[i], odd_part(i), limb_bits, short_bits, product)
    kernel = [cofactors[i] << i.bit_count() for i in range(n)]
    return factorial, cofactors, inverses, kernel


def narrow_convolution(values, kernel, width, limb_bits, product=karatsuba, trace=None):
    """Return the first n coefficients modulo 2**width, in fixed windows.

    Both lists have length n. values are wide; kernel entries fit limb_bits.
    Exactly ceil(width/limb_bits) packed multiplications are performed, each
    with argument capacity n * round8(2*limb_bits + ceil(log2(n))).
    """
    n = len(values)
    assert n >= 1 and len(kernel) == n
    assert limb_bits >= 8 and limb_bits % 8 == 0 and width >= 1
    assert all(0 <= value < 1 << width for value in values)
    assert all(0 <= value < 1 << limb_bits for value in kernel)
    guard = (n - 1).bit_length()
    slot_bytes = (limb_bits + limb_bits + guard + 7) // 8
    limb_bytes = limb_bits // 8
    count = (width + limb_bits - 1) // limb_bits
    kernel_raw = b''.join(value.to_bytes(slot_bytes, 'little') for value in kernel)
    packed_kernel = int.from_bytes(kernel_raw, 'little')
    source = [value.to_bytes(count * limb_bytes, 'little') for value in values]
    outputs = [bytearray(count * limb_bytes) for _ in range(n)]
    carries = [0] * n
    mask = (1 << limb_bits) - 1
    for slab in range(count):
        start = slab * limb_bytes
        digits = [int.from_bytes(raw[start:start + limb_bytes], 'little') for raw in source]
        packed = int.from_bytes(b''.join(value.to_bytes(slot_bytes, 'little') for value in digits), 'little')
        result = product(packed, packed_kernel)
        raw_result = result.to_bytes((n + n) * slot_bytes, 'little')
        for k in range(n):
            coefficient = int.from_bytes(raw_result[k * slot_bytes:(k + 1) * slot_bytes], 'little')
            combined = coefficient + carries[k]
            next_carry = combined >> limb_bits
            if trace is not None:
                trace(slab, k, digits, coefficient, carries[k], next_carry)
            carries[k] = next_carry
            outputs[k][start:start + limb_bytes] = (combined & mask).to_bytes(limb_bytes, 'little')
    output_mask = (1 << width) - 1
    return [int.from_bytes(raw, 'little') & output_mask for raw in outputs]


def shift(values, sigma=1, h=None, product=karatsuba, convolution_product=None, trace=None):
    assert sigma in (-1, 1)
    if not values:
        return []
    if h is None:
        h = max(abs(value).bit_length() for value in values)
    assert h >= 0 and all(abs(value) < 1 << h for value in values)
    n = len(values)
    if n == 1:
        return list(values)
    p = parameters(n, h)
    width, t, guard, output_bits = p['W'], p['t'], p['g'], p['H']
    factorial, cofactors, inverses, kernel = prepare(n, t, product)
    mask = (1 << width) - 1
    scaled = []
    for i, value in enumerate(values):
        x = limb_product(value & mask, factorial[i], width, t, product)
        x = (x << (guard - i.bit_count())) & mask
        if sigma < 0 and i & 1:
            x = (-x) & mask
        scaled.append(x)
    convolution = narrow_convolution(scaled[::-1], kernel, width, t,
                                     convolution_product or product, trace)
    output = []
    for j in range(n):
        x = limb_divide(convolution[n - 1 - j], factorial[-1], width, t, inverses[-1], product)
        x = limb_divide(x, factorial[j], width, t, inverses[j], product)
        x = (x << j.bit_count()) & mask
        if sigma < 0 and j & 1:
            x = (-x) & mask
        assert x & ((1 << guard) - 1) == 0
        x >>= guard
        if x >= 1 << (output_bits - 1):
            x -= 1 << output_bits
        output.append(x)
    return output
