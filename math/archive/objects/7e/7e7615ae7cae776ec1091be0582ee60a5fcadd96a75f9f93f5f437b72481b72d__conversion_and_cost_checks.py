"""Algebra/recurrence checks for arbitrary log-domain size m.

Large Python integers here represent packed strings; their run time is not
used as evidence for any bounded-word RAM claim.
"""
import json
import math
import random
from functools import lru_cache
from independent_extension_checks import to_novel_reference, from_novel_reference


def binary_long_division(numerator, denominator):
    quotient = 0
    while numerator.bit_length() >= denominator.bit_length():
        shift = numerator.bit_length() - denominator.bit_length()
        quotient ^= 1 << shift
        numerator ^= denominator << shift
    return quotient, numerator


def change_variable(packed, exponent, split, width, inverse=False):
    if exponent == split:
        return packed
    half = 1 << (exponent - 1)
    small = half >> split
    boundary = half * width
    mask = (1 << boundary) - 1
    first, second = packed & mask, packed >> boundary
    if inverse:
        remainder = change_variable(first, exponent - 1, split, width, True)
        quotient = change_variable(second, exponent - 1, split, width, True)
        high = quotient ^ (quotient >> ((half - small) * width))
        low = remainder ^ ((quotient << (small * width)) & mask)
        return low | (high << boundary)
    quotient = second ^ (second >> ((half - small) * width))
    remainder = first ^ ((quotient << (small * width)) & mask)
    low = change_variable(remainder, exponent - 1, split, width)
    high = change_variable(quotient, exponent - 1, split, width)
    return low | (high << boundary)


def convert(packed, exponent, width, inverse=False):
    if exponent <= 1:
        return packed
    split = 1 << ((exponent - 1).bit_length() - 1)
    other = exponent - split
    block_width = width << split
    block_mask = (1 << block_width) - 1
    if inverse:
        lower = 0
        for i in range(1 << other):
            block = (packed >> (i * block_width)) & block_mask
            lower |= convert(block, split, width, True) << (i * block_width)
        upper = convert(lower, other, block_width, True)
        return change_variable(upper, exponent, split, width, True)
    intermediate = change_variable(packed, exponent, split, width)
    upper = convert(intermediate, other, block_width)
    output = 0
    for i in range(1 << other):
        block = (upper >> (i * block_width)) & block_mask
        output |= convert(block, split, width) << (i * block_width)
    return output


@lru_cache(None)
def cost(exponent):
    if exponent <= 1:
        return 0, 1
    split = 1 << ((exponent - 1).bit_length() - 1)
    other = exponent - split
    lower_volume, lower_pieces = cost(split)
    upper_volume, upper_pieces = cost(other)
    return (lower_volume + upper_volume + other,
            (1 << other) * lower_pieces + upper_pieces + (1 << other))


rng = random.Random(20002027)
division_cases = 0
for half in [2, 4, 8, 16, 32, 64]:
    for small in [1 << j for j in range(half.bit_length() - 1)]:
        for _ in range(80):
            numerator = rng.getrandbits(2 * half)
            high, low = numerator >> half, numerator & ((1 << half) - 1)
            quotient = high ^ (high >> (half - small))
            remainder = low ^ ((quotient << small) & ((1 << half) - 1))
            assert (quotient, remainder) == binary_long_division(
                numerator, (1 << half) ^ (1 << small))
            division_cases += 1

conversion_cases = 0
for exponent in range(11):
    for width in [1, 3, 9]:
        for _ in range(6):
            coefficients = [rng.getrandbits(width) for _ in range(1 << exponent)]
            packed = sum(value << (width * i) for i, value in enumerate(coefficients))
            transformed = convert(packed, exponent, width)
            decoded = [(transformed >> (width * i)) & ((1 << width) - 1)
                       for i in range(1 << exponent)]
            assert decoded == to_novel_reference(coefficients)
            assert convert(transformed, exponent, width, True) == packed
            assert from_novel_reference(decoded) == coefficients
            conversion_cases += 1

scaling = []
for exponent in [3, 5, 7, 9, 15, 17, 31, 33, 63, 65, 127, 129, 255, 257, 511, 513, 1023, 1024]:
    volume, pieces = cost(exponent)
    scaling.append({"m": exponent,
                    "V_over_m_log2_m": volume / (exponent * math.log2(exponent)),
                    "J_over_2powm": pieces / (1 << exponent)})
print(json.dumps({"division_cases": division_cases,
                  "arbitrary_m_vector_conversion_and_inverse_cases": conversion_cases,
                  "symbolic_recurrence_scaling": scaling,
                  "status": "all passed"}, indent=2))
