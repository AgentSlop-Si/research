"""Exact byte-digit products with paid seeds and verified multi-parent reuse.

Seed multiplication is an explicit black box M(8*n), not one word operation.
All other numerical work uses bounded digit/carry loops. No FFT is imported.
"""
from collections import Counter
from dataclasses import dataclass
from math import comb

BASE = 256
MAX_DEGREE = 3


class Ledger(Counter):
    def word_operations(self):
        return sum(self[k] for k in (
            'word_add', 'word_sub', 'small_mul', 'digit_mul', 'word_divmod'))


@dataclass(frozen=True)
class SeedCache:
    n: int
    # Trusted internal entries (A digits, B digits, canonical product digits).
    entries: tuple


def validate(pairs, c):
    if not pairs or len(pairs[0]) != 2:
        raise ValueError('a nonempty sequence of operand pairs is required')
    n = len(pairs[0][0])
    if n < 1:
        raise ValueError('at least one byte per operand is required')
    for pair in pairs:
        if len(pair) != 2:
            raise ValueError('every query must have two operands')
        for digits in pair:
            if len(digits) != n:
                raise ValueError('all operands must have the same padded length')
            for value in digits:
                c['validation_digit_reads'] += 1
                c['validation_digit_tests'] += 1
                if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value < BASE:
                    raise ValueError('operands must be canonical byte digits')
    return n


def seed_product(pair, n, c):
    a, b = pair
    left = int.from_bytes(bytes(a), 'little')
    right = int.from_bytes(bytes(b), 'little')
    c['seed_input_pack_bytes'] += 2*n
    # Intentionally opaque cost: one multiplication of at most 8n-bit integers.
    product = left*right
    c['seed_multiplications'] += 1
    c['seed_bound_bits_sum'] += 8*n
    out = list(product.to_bytes(2*n, 'little'))
    c['seed_output_conversion_bytes'] += 2*n
    c['seed_canonical_digit_writes'] += 2*n
    return out


def combine(vectors, weights, width, c):
    """Signed linear combination in redundant digits; never creates a bigint."""
    out = [0]*width
    c['coefficient_zero_writes'] += width
    for vector, weight in zip(vectors, weights):
        if len(vector) > width:
            raise ValueError('linear combination exceeds its buffer')
        for j, value in enumerate(vector):
            c['combination_digit_reads'] += 1
            if abs(weight) != 1:
                value *= abs(weight)
                c['small_mul'] += 1
            if weight >= 0:
                out[j] += value
                c['word_add'] += 1
            else:
                out[j] -= value
                c['word_sub'] += 1
            c['combination_accumulator_writes'] += 1
    return out


def carry_pass(coefficients, width, c):
    carry = 0
    out = []
    for j in range(width):
        value = (coefficients[j] if j < len(coefficients) else 0)+carry
        carry, digit = divmod(value, BASE)
        c['word_add'] += 1
        c['word_divmod'] += 1
        c['carry_digit_reads'] += int(j < len(coefficients))
        c['carry_digit_writes'] += 1
        out.append(digit)
    return out, carry


def signed_patch(coefficients, width, c):
    """Canonical signed magnitude, for -256**width < value < 256**width."""
    if len(coefficients) > width:
        raise ValueError('signed coefficients exceed their normalization width')
    digits, carry = carry_pass(coefficients, width, c)
    if carry not in (-1, 0):
        raise ValueError('signed relation exceeds its proven width')
    sign = 1
    if carry == -1:
        sign, carry = -1, 1
        for j, digit in enumerate(digits):
            value = (BASE-1)-digit+carry
            carry, digits[j] = divmod(value, BASE)
            c['word_sub'] += 1
            c['word_add'] += 1
            c['word_divmod'] += 1
            c['signed_magnitude_digit_writes'] += 1
        if carry:
            raise ValueError('negative value at or beyond the signed width boundary')
    patch = []
    for j, digit in enumerate(digits):
        c['patch_zero_tests'] += 1
        if digit:
            # The sign is metadata; applying it uses a counted add/subtract.
            patch.append((j, sign, digit))
            c['numeric_patch_records'] += 1
    return patch


def product_digits(coefficients, n, c):
    # An extra byte checks cancellation of any signed correction overflow.
    digits, carry = carry_pass(coefficients, 2*n+1, c)
    c['product_range_checks'] += 2
    if carry != 0 or digits[-1] != 0:
        raise ValueError('computed product is outside the canonical output range')
    return digits[:-1]


def finite_difference_patch(vectors, order, n, c):
    weights = [(-1)**j*comb(order, j) for j in range(order+1)]
    c['relation_coefficients_prepared'] += order+1
    raw = combine(vectors, weights, n+1, c)
    return signed_patch(raw, n+1, c)


def discover_degree(pairs, operand, max_degree, n, c):
    for degree in range(max_degree+1):
        order = degree+1
        c['degree_candidates_tested'] += 1
        valid = True
        for i in range(order, len(pairs)):
            c['trajectory_relations_tested'] += 1
            vectors = [pairs[i-j][operand] for j in range(order+1)]
            if finite_difference_patch(vectors, order, n, c):
                valid = False
                break
        if valid:
            return degree
    return None


def cached_prefix(cache, pairs, n, maximum, c):
    if cache is None:
        return []
    if not isinstance(cache, SeedCache) or cache.n != n or len(cache.entries) > maximum:
        raise ValueError('cache width or prefix length does not match this schedule')
    products = []
    for i, entry in enumerate(cache.entries):
        if len(entry) != 3:
            raise ValueError('invalid cache entry')
        a, b, product = entry
        for old, current in ((a, pairs[i][0]), (b, pairs[i][1])):
            if len(old) != n:
                raise ValueError('invalid cached operand width')
            for u, v in zip(old, current):
                c['cache_key_digit_comparisons'] += 1
                if u != v:
                    raise ValueError('stale cache operands')
        if len(product) != 2*n:
            raise ValueError('invalid cached product width')
        for digit in product:
            c['cache_product_digit_tests'] += 1
            if not isinstance(digit, int) or isinstance(digit, bool) or not 0 <= digit < BASE:
                raise ValueError('invalid cached product digit')
        products.append(list(product))
        c['cache_product_copy_bytes'] += 2*n
    return products


def finish(products, c, schedule, **details):
    outputs = [list(value) for value in products]
    c['full_output_digit_writes'] += sum(map(len, outputs))
    return dict(outputs=outputs, counts=dict(c), word_operations=c.word_operations(),
                schedule=schedule, **details)


def make_seed_cache(pairs, count):
    c = Ledger()
    n = validate(pairs, c)
    if not isinstance(count, int) or isinstance(count, bool) or not 0 <= count <= len(pairs):
        raise ValueError('invalid cache prefix count')
    entries = []
    for pair in pairs[:count]:
        product = seed_product(pair, n, c)
        entries.append((tuple(pair[0]), tuple(pair[1]), tuple(product)))
        c['cache_key_copy_bytes'] += 2*n
        c['cache_product_copy_bytes'] += 2*n
    return SeedCache(n, tuple(entries)), dict(counts=dict(c), word_operations=c.word_operations())


def baseline_batch(pairs, cache=None):
    c = Ledger()
    n = validate(pairs, c)
    products = cached_prefix(cache, pairs, n, len(pairs), c)
    schedule = ['cached']*len(products)
    for pair in pairs[len(products):]:
        products.append(seed_product(pair, n, c))
        schedule.append('fresh')
    return finish(products, c, schedule)


def secant_batch(pairs, max_patch=2, cache=None):
    """Fixed verified 2-parent schedule; dense residuals fall back to paid seeds."""
    c = Ledger()
    n = validate(pairs, c)
    if not isinstance(max_patch, int) or isinstance(max_patch, bool) or max_patch < 0:
        raise ValueError('max_patch must be a nonnegative integer')
    for pair in pairs[1:]:
        for u, v in zip(pairs[0][1], pair[1]):
            c['same_b_digit_comparisons'] += 1
            if u != v:
                raise ValueError('secant mode requires the same B in every query')
    products = cached_prefix(cache, pairs, n, min(2, len(pairs)), c)
    schedule = ['cached']*len(products)
    residual_supports = []
    for i in range(len(products), len(pairs)):
        if i < 2:
            products.append(seed_product(pairs[i], n, c))
            schedule.append('fresh')
            continue
        c['secant_relations_tested'] += 1
        raw = combine([pairs[i][0], pairs[i-1][0], pairs[i-2][0]], [1,-2,1], n+1, c)
        numeric = signed_patch(raw, n+1, c)
        coordinate = []
        for j, value in enumerate(raw):
            c['coordinate_patch_zero_tests'] += 1
            if value:
                coordinate.append((j, 1 if value > 0 else -1, abs(value)))
                c['coordinate_patch_records'] += 1
        patch = numeric if len(numeric) < len(coordinate) else coordinate
        residual_supports.append(len(patch))
        if len(patch) > max_patch:
            products.append(seed_product(pairs[i], n, c))
            schedule.append('fresh_dense_residual')
            continue
        coefficients = combine([products[i-1], products[i-2]], [2,-1], 2*n+1, c)
        for j, sign, digit in patch:
            for k, value in enumerate(pairs[i][1]):
                term = digit*value
                c['digit_mul'] += 1
                if sign > 0:
                    coefficients[j+k] += term
                    c['word_add'] += 1
                else:
                    coefficients[j+k] -= term
                    c['word_sub'] += 1
                c['residual_convolution_updates'] += 1
        products.append(product_digits(coefficients, n, c))
        schedule.append('secant')
    return finish(products, c, schedule, residual_supports=residual_supports)


def polynomial_batch(pairs, max_degree=MAX_DEGREE, cache=None):
    """Verify each operand trajectory, then use their product-degree recurrence."""
    c = Ledger()
    n = validate(pairs, c)
    if (not isinstance(max_degree, int) or isinstance(max_degree, bool)
            or not 0 <= max_degree <= MAX_DEGREE):
        raise ValueError('supported discovery degree is 0 through 3')
    degrees = [discover_degree(pairs, j, max_degree, n, c) for j in (0,1)]
    if None in degrees:
        products = cached_prefix(cache, pairs, n, len(pairs), c)
        schedule = ['cached']*len(products)
        for pair in pairs[len(products):]:
            products.append(seed_product(pair, n, c))
            schedule.append('fresh_unstructured')
        return finish(products, c, schedule, degrees=degrees, verified=False)
    order = sum(degrees)+1
    products = cached_prefix(cache, pairs, n, min(order, len(pairs)), c)
    schedule = ['cached']*len(products)
    weights = [(-1)**(j+1)*comb(order,j) for j in range(1,order+1)]
    c['recurrence_coefficients_prepared'] += order
    for i in range(len(products), len(pairs)):
        if i < order:
            products.append(seed_product(pairs[i], n, c))
            schedule.append('fresh')
        else:
            previous = [products[i-j] for j in range(1, order+1)]
            coefficients = combine(previous, weights, 2*n+1, c)
            products.append(product_digits(coefficients, n, c))
            schedule.append('polynomial')
    return finish(products, c, schedule, degrees=degrees, verified=True)
