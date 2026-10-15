"""Fresh exact block composition of canonical Newton-Horner steps.

No full-input native multiplication, polynomial convolution, or external producer
is used. Data products use explicit shift/add; divisions use bit-list long division.
This is an elementary closed algorithm, not a fast multiplication claim.
"""
from dataclasses import dataclass, asdict


@dataclass
class Ledger:
    descriptor_nodes: int = 0
    block_applications: int = 0
    normalization_cells: int = 0
    normal_division_bits: int = 0
    input_division_bits: int = 0
    scalar_bit_steps: int = 0
    scalar_add_bit_work: int = 0
    descriptor_add_bit_work: int = 0
    cell_add_bit_work: int = 0
    output_add_bit_work: int = 0
    input_division_bit_work: int = 0
    normal_division_bit_work: int = 0
    max_descriptor_bits: int = 0
    max_carry_bits: int = 0
    max_raw_bits: int = 0
    full_period_shift_blocks: int = 0


def bits_of(x):
    assert x >= 0
    if not x:
        return []
    raw = x.to_bytes((x.bit_length() + 7) // 8, 'big')
    result = [(byte >> shift) & 1 for byte in raw for shift in range(7, -1, -1)]
    return result[len(result) - x.bit_length():]


def from_bits(bits):
    """Linear bit-list packing, without repeatedly growing a binary quotient."""
    if not bits:
        return 0
    pad = (-len(bits)) % 8
    padded = [0] * pad + bits
    raw = bytearray()
    for i in range(0, len(padded), 8):
        byte = 0
        for bit in padded[i:i+8]:
            byte = (byte << 1) | bit
        raw.append(byte)
    return int.from_bytes(raw, 'big')


def multiply(x, y, ledger=None):
    assert x >= 0 and y >= 0
    if x.bit_length() < y.bit_length():
        x, y = y, x
    value = 0
    for bit in reversed(bits_of(y)):
        if ledger is not None:
            ledger.scalar_bit_steps += 1
            # A conservative abstract bit-operation invoice: read/shift x,
            # then conditionally add it. Does not purport to time CPython.
            ledger.scalar_add_bit_work += x.bit_length() + max(value.bit_length(), x.bit_length()) + 1
        if bit:
            value += x
        x <<= 1
    return value


def divide(x, divisor, ledger=None, kind='normal'):
    assert x >= 0 and divisor > 0
    if x < divisor:
        if ledger is not None:
            if kind == 'input':
                ledger.input_division_bit_work += x.bit_length() + 1
            else:
                ledger.normal_division_bit_work += x.bit_length() + 1
        return 0, x
    quotient = []
    rem = 0
    started = False
    for bit in bits_of(x):
        rem = (rem << 1) | bit
        qb = int(rem >= divisor)
        if qb:
            rem -= divisor
        if started or qb:
            quotient.append(qb)
            started = True
        if ledger is not None:
            if kind == 'input':
                ledger.input_division_bits += 1
                ledger.input_division_bit_work += divisor.bit_length() + 1
            else:
                ledger.normal_division_bits += 1
                ledger.normal_division_bit_work += divisor.bit_length() + 1
    return from_bits(quotient), rem


def bases_for(p, g, r):
    if p < 3 or g <= 0 or r < 1:
        raise ValueError('Require p >= 3, g > 0, r >= 1')
    bases = []
    value = p
    for index in range(r):
        bases.append(value)
        if index + 1 < r:
            value += g
    return bases


def to_digits(x, bases, ledger=None):
    if x < 0:
        raise ValueError('Nonnegative input required')
    digits = []
    while x:
        x, digit = divide(x, bases[len(digits) % len(bases)], ledger, 'input')
        digits.append(digit)
    return digits or [0]


def from_digits(digits, bases, ledger=None):
    value = 0
    for i in range(len(digits) - 1, -1, -1):
        value = multiply(value, bases[i % len(bases)], ledger)
        if ledger is not None:
            ledger.output_add_bit_work += max(value.bit_length(), digits[i].bit_length()) + 1
        value += digits[i]
    return value


def compose(low, high, ledger=None):
    """F_low after F_high: (P_l P_h, H_l + P_l H_h)."""
    pl, hl = low
    ph, hh = high
    p = multiply(pl, ph, ledger)
    h = multiply(pl, hh, ledger)
    if ledger is not None:
        ledger.descriptor_add_bit_work += max(h.bit_length(), hl.bit_length()) + 1
    h += hl
    assert 0 <= h < p
    if ledger is not None:
        ledger.descriptor_nodes += 1
        ledger.max_descriptor_bits = max(ledger.max_descriptor_bits, p.bit_length(), h.bit_length())
    return p, h


def describe(a, bases, lo, hi, ledger=None):
    """Balanced product tree, retaining only O(block bits) live arithmetic data."""
    if hi == lo:
        return 1, 0
    if hi == lo + 1:
        p, h = bases[lo % len(bases)], a[lo]
        assert 0 <= h < p
        if ledger is not None:
            ledger.max_descriptor_bits = max(ledger.max_descriptor_bits, p.bit_length())
        return p, h
    mid = (lo + hi) // 2
    return compose(describe(a, bases, lo, mid, ledger),
                   describe(a, bases, mid, hi, ledger), ledger)


def apply_block(old, beta, descriptor, bases, capacity, ledger=None,
                shift=None):
    """Exact canonical block action. shift optionally exploits P=Q^k."""
    p, h = descriptor
    carry = 0
    output = []
    for i in range(capacity + 1):
        vi = old[i] if i < len(old) else 0
        bi = beta[i] if i < len(beta) else 0
        if shift is None:
            pv = multiply(p, vi, ledger)
        else:
            pv = old[i-shift] if 0 <= i-shift < len(old) else 0
        raw = pv + multiply(h, bi, ledger) + carry
        if ledger is not None:
            ledger.cell_add_bit_work += max(pv.bit_length(), h.bit_length()+bi.bit_length(), carry.bit_length()) + 2
            ledger.normalization_cells += 1
            ledger.max_raw_bits = max(ledger.max_raw_bits, raw.bit_length())
        carry, digit = divide(raw, bases[i % len(bases)], ledger)
        if shift is None:
            assert carry <= p + h - 1
        else:
            # Shifted old digits are canonical, hence act as coefficient 1.
            assert carry <= h
        if ledger is not None:
            ledger.max_carry_bits = max(ledger.max_carry_bits, carry.bit_length())
        output.append(digit)
    assert carry == 0 and output[-1] == 0
    while len(output) > 1 and output[-1] == 0:
        output.pop()
    if ledger is not None:
        ledger.block_applications += 1
        ledger.full_period_shift_blocks += int(shift is not None)
    return output


def multiply_digits(a, b, bases, block_size=1, exploit_period_shift=True, ledger=None):
    if block_size < 1 or not a or not b:
        raise ValueError('Positive block size and nonempty canonical operands required')
    for digits in (a, b):
        if any(not 0 <= digit < bases[i % len(bases)] for i, digit in enumerate(digits)):
            raise ValueError('Noncanonical input digits')
    if len(a) > len(b):
        a, b = b, a
    ledger = ledger or Ledger()
    capacity = len(a) + len(b)
    old = [0]
    # Generate descending intervals without storing O(s/h) growing indices.
    last_lo = ((len(a)-1)//block_size)*block_size
    for lo in range(last_lo, -1, -block_size):
        hi = min(lo+block_size, len(a))
        descriptor = describe(a, bases, lo, hi, ledger)
        # Any complete number of periods contains exactly Q^k as its product.
        shift = hi-lo if exploit_period_shift and (hi-lo) % len(bases) == 0 else None
        old = apply_block(old, b, descriptor, bases, capacity, ledger, shift)
    return old, ledger


def multiply_integer(a, b, p=7, g=4, r=4, block_size=1,
                     exploit_period_shift=True):
    bases = bases_for(p, g, r)
    ledger = Ledger()
    ad, bd = to_digits(a, bases, ledger), to_digits(b, bases, ledger)
    output, ledger = multiply_digits(ad, bd, bases, block_size,
                                     exploit_period_shift, ledger)
    return from_digits(output, bases, ledger), asdict(ledger)
