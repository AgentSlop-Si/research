"""Fresh fixed-precision / guarded-sharing interface controls.

The imported arithmetic is pinned accepted Karatsuba and modular Taylor shifts.
No general represented-value multiplication is used outside that backend.
Bounded bitstream reads/writes, rather than growing wide quotient shifts, are
used by the new odd-division implementation. This is an arithmetic model;
Python object/address overhead is not a claimed implementation timing.
"""
from dependencies.kernel_stream import karatsuba
from dependencies.accepted_product_interface import shift_mod, binary_chunks, reconstruct_binary


def mul_small(value, small, width):
    """Shift/add multiplication by a nonnegative small integer modulo 2**width."""
    assert small >= 0 and width >= 1
    mask, out = (1 << width) - 1, 0
    value &= mask
    while small:
        if small & 1:
            out = (out + value) & mask
        value = (value << 1) & mask
        small >>= 1
    return out


def odd_divide_bits(value, odd, width, trace=None):
    """Return value / odd modulo 2**width with width bounded bit operations.

    Carry invariant: 0 <= carry < odd. Each step touches O(bitlength(odd))
    carry bits and one source/output bit. Full-width buffers are prepared once.
    """
    assert width >= 1 and odd > 0 and odd & 1
    mask = (1 << width) - 1
    source = (value & mask).to_bytes((width + 7) // 8, 'little')
    output = bytearray(len(source))
    carry = 0
    for bit in range(width):
        digit = (source[bit // 8] >> (bit % 8)) & 1
        quotient = (digit - carry) & 1
        numerator = carry + (odd if quotient else 0) - digit
        assert numerator & 1 == 0
        next_carry = numerator >> 1
        assert 0 <= next_carry < odd
        if trace is not None:
            trace(bit, digit, quotient, carry, next_carry)
        output[bit // 8] |= quotient << (bit % 8)
        carry = next_carry
    return int.from_bytes(output, 'little')


def horner_mod(coefficients, point, width):
    assert point >= 0
    mask, value = (1 << width) - 1, 0
    for coefficient in reversed(coefficients):
        value = (mul_small(value, point, width) + coefficient) & mask
    return value


def guard_for_degree(degree):
    assert degree >= 0
    return degree - degree.bit_count()


def interpolate_consecutive(values, output_bits, stats=None):
    """Integer-coefficient polynomial from samples at 0,...,n-1.

    Input samples are canonical residues modulo 2**(output_bits+Gamma), where
    Gamma=v2((n-1)!). The promise is that these are samples of an integer
    polynomial of degree < n. Returns its monomial coefficients mod 2**H.
    """
    n = len(values)
    assert n >= 1 and output_bits >= 1
    gamma = guard_for_degree(n - 1)
    width = output_bits + gamma
    mask = (1 << width) - 1
    assert all(0 <= value <= mask for value in values)
    differences = list(values)
    odd, valuation, newton = 1, 0, []
    odd_steps = 0
    max_odd_bits = 1
    for k in range(n):
        if k:
            v = (k & -k).bit_length() - 1
            valuation += v
            factor = k >> v
            # Full exact odd factorial fits the declared n*ceil(log2(n+1)) cap.
            cap = max(1, (n - 1) * max(1, (n - 1).bit_length()) + 1)
            odd = mul_small(odd, factor, cap)
        value = differences[0]
        assert value & ((1 << valuation) - 1) == 0
        quotient = odd_divide_bits(value >> valuation, odd, output_bits)
        newton.append(quotient)
        odd_steps += output_bits
        max_odd_bits = max(max_odd_bits, odd.bit_length())
        differences = [(differences[j+1] - differences[j]) & mask
                       for j in range(len(differences)-1)]
    out_mask = (1 << output_bits) - 1
    polynomial = [newton[-1]]
    small_actions = 0
    for k in range(n-2, -1, -1):
        following = [0] + polynomial
        for j, coefficient in enumerate(polynomial):
            following[j] = (following[j] - mul_small(coefficient, k, output_bits)) & out_mask
            small_actions += 1
        following[0] = (following[0] + newton[k]) & out_mask
        polynomial = following
    if stats is not None:
        stats.update(samples=n, degree=n-1, H=output_bits, Gamma=gamma, W=width,
                     difference_subtractions=n*(n-1)//2,
                     odd_division_steps=odd_steps,
                     max_odd_bits=max_odd_bits, basis_small_actions=small_actions)
    return polynomial


def guarded_convolution(left, right, output_bits, product=karatsuba, stats=None):
    """All linear product coefficients using 2L-1 guarded evaluation products.

    Inputs may be any canonical W-bit lifts, W=H+v2((2L-2)!). Their reduction
    modulo 2**H defines the required output. Every sample product is charged.
    """
    length = len(left)
    assert length >= 1 and len(right) == length and output_bits >= 1
    count = 2*length-1
    gamma = guard_for_degree(count-1)
    width, samples = output_bits+gamma, []
    mask = (1 << width) - 1
    assert all(0 <= value <= mask for value in left+right)
    actual_max = 0
    for point in range(count):
        a = horner_mod(left, point, width)
        b = horner_mod(right, point, width)
        actual_max = max(actual_max, a.bit_length(), b.bit_length())
        samples.append(product(a, b) & mask)
    ledger = {}
    result = interpolate_consecutive(samples, output_bits, ledger)
    if stats is not None:
        stats.update(ledger)
        stats.update(evaluation_products=count, maximum_sample_bits=actual_max,
                     horner_small_actions=2*count*length)
    return result


def six_product_three(left, right, width, product=karatsuba, stats=None):
    """Optimal six-product, division-free ring-bilinear length-three control."""
    assert len(left) == len(right) == 3 and width >= 1
    mask = (1 << width)-1
    a, b = [x & mask for x in left], [x & mask for x in right]
    u = [product(a[i], b[i]) & mask for i in range(3)]
    v01 = product((a[0]+a[1]) & mask, (b[0]+b[1]) & mask) & mask
    v02 = product((a[0]+a[2]) & mask, (b[0]+b[2]) & mask) & mask
    v12 = product((a[1]+a[2]) & mask, (b[1]+b[2]) & mask) & mask
    if stats is not None:
        stats.update(scalar_products=6, H=width)
    return [u[0], (v01-u[0]-u[1]) & mask,
            (v02-u[0]-u[2]+u[1]) & mask,
            (v12-u[1]-u[2]) & mask, u[2]]


def multiply_guarded_interface(x, y, m, length, product=karatsuba, stats=None):
    """Accepted Mersenne Taylor route, with guarded interpolation as a control.

    This explicitly realizes a familiar interpolation mechanism. No new
    asymptotic multiplication improvement or prior-art claim is made.
    """
    assert length >= 1 and m >= 2
    a, b = binary_chunks(x,m,length), binary_chunks(y,m,length)
    H = 2*m+(length-1).bit_length()
    gamma = guard_for_degree(2*length-2)
    W = H+gamma
    c, d = shift_mod(a,1,W,product), shift_mod(b,1,W,product)
    ledger = {}
    raw = guarded_convolution(c,d,H,product,ledger)
    coefficients = shift_mod(raw,-1,H,product)
    result = reconstruct_binary(coefficients,m)
    if length == 1:
        h = m
    else:
        h = min(W, m+(length-1).bit_length()
                +(length-1)*(2*length-2).bit_length())
    assert ledger['maximum_sample_bits'] <= h
    if stats is not None:
        stats.update(ledger)
        stats.update(m=m,L=length,H_final=H,W_forward=W,
                     sample_capacity=h, final_coefficients=coefficients,
                     output_coefficients=len(coefficients))
    return result
