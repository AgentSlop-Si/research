"""Charged exact first-order factors for the q-orbit correction compiler."""
from collections import Counter
from fixed_kernel import Counted


def counted_power(counter, base, exponent):
    """Nonnegative binary powering with every field multiplication charged."""
    if exponent < 0:
        raise ValueError('nonnegative exponent required')
    out = counter.one
    while exponent:
        if exponent & 1:
            out = counter.mul(out, base)
        exponent >>= 1
        if exponent:
            base = counter.mul(base, base)
    return out


def apply_factor_powers(field, x, factor_powers, q):
    """Apply product_e (I-q^e S)^f[e], modulo the length-N nilpotent shift.

q must have order N=len(x). Positive powers use y_i=x_i-c*x_(i-1).
Negative powers use y_i=x_i+c*y_(i-1); no data-dependent division occurs.
The dictionary is expected to contain a compiled signed flow. This routine
    counts all coefficient generation, copies, reads, writes, and field operations.
    A single deterministic power table uses N-1 multiplications. Every positive
    factor updates in descending order; negative factors update ascending, so
    only the output copy and O(N) coefficient table are materialized.
It does not hide the cost of compiling the input operator graph into that flow.
"""
    n = len(x)
    if n < 1:
        raise ValueError('nonempty vector required')
    canonical = Counter()
    for exponent, multiplicity in factor_powers.items():
        if not isinstance(exponent, int) or not isinstance(multiplicity, int):
            raise ValueError('integer exponents and multiplicities required')
        canonical[exponent % n] += multiplicity
    root_counter, operation_counter = Counted(field), Counted(field)
    traffic = Counter({'initial_copy_reads': n, 'initial_copy_writes': n})
    value = list(x)
    powers = [field.one]
    for _ in range(1, n):
        powers.append(root_counter.mul(powers[-1], q))
    traffic['coefficient_generation_reads'] = n-1
    traffic['coefficient_table_writes'] = n
    applied = distinct = 0
    for exponent, multiplicity in canonical.items():
        if not multiplicity:
            continue
        distinct += 1
        coefficient = powers[exponent]
        for _ in range(abs(multiplicity)):
            indices = range(n-1, 0, -1) if multiplicity > 0 else range(1, n)
            for j in indices:
                term = operation_counter.mul(coefficient, value[j-1])
                value[j] = (operation_counter.sub(value[j], term) if multiplicity > 0
                            else operation_counter.add(value[j], term))
            applied += 1
            traffic['filter_vector_reads'] += 2*(n-1)
            traffic['filter_vector_writes'] += n-1
    traffic['coefficient_lookups'] = distinct
    return value, {'coefficient_preparation': dict(root_counter.count),
        'field_operations': dict(operation_counter.count), 'array_traffic': dict(traffic),
        'filter_passes': applied, 'distinct_coefficients': distinct,
        'canonicalization_entries_read': len(factor_powers)}
