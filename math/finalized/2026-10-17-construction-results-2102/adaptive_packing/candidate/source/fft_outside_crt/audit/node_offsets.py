#!/usr/bin/env python3
"""Dimension-only minimax shift for 2r-1 consecutive integer value nodes.

The objective is the maximum unweighted absolute row norm of evaluation of
the first r falling-binomial basis functions.  This is an exact finite
optimization, not an assertion that this offset minimizes measured runtime
or input-dependent CRT width.
"""
from dataclasses import dataclass, asdict
from time import perf_counter


@dataclass
class OffsetCounts:
    norm_evaluations: int = 0
    integer_products: int = 0
    exact_divisions: int = 0
    integer_additions: int = 0
    integer_comparisons: int = 0
    peak_integer_bits: int = 0

    def see(self, *values):
        self.peak_integer_bits = max(self.peak_integer_bits,
                                     *(abs(v).bit_length() for v in values))


def _next_binomial(value, numerator, denominator, counts):
    product = value * numerator
    quotient, remainder = divmod(product, denominator)
    counts.integer_products += 1
    counts.exact_divisions += 1
    counts.see(value, product, quotient)
    if remainder:
        raise ArithmeticError('binomial coefficient recurrence is not exact')
    return quotient


def endpoint_norms(r, left_magnitude, counts=None):
    """Return exact endpoint row l1 norms at -a and 2r-2-a."""
    if type(r) is not int or r < 2 or not 0 <= left_magnitude <= r - 1:
        raise ValueError('require r>=2 and 0<=left_magnitude<=r-1')
    counts = OffsetCounts() if counts is None else counts
    counts.norm_evaluations += 1
    a = left_magnitude
    negative = 1
    if a:
        # Sum_j binom(a+j-1,j) = binom(a+r-1,r-1).
        for j in range(1, r):
            negative = _next_binomial(negative, a+j, j, counts)
    endpoint = 2*r - 2 - a
    term = positive = 1
    for j in range(1, r):
        term = _next_binomial(term, endpoint-j+1, j, counts)
        positive += term
        counts.integer_additions += 1
        counts.see(positive)
    return negative, positive


def choose_offset(r):
    """Return offset and a reproducible fully counted setup report.

    Endpoint norms are monotone in opposite directions.  The minimum of
    their maximum occurs at one of the two integers around their crossing.
    """
    if type(r) is not int or r < 2:
        raise ValueError('rank must be an integer at least two')
    started = perf_counter()
    counts = OffsetCounts()
    cache = {}

    def norms(a):
        if a not in cache:
            cache[a] = endpoint_norms(r, a, counts)
        return cache[a]

    low, high = 0, r-1
    while low < high:
        middle = (low+high)//2
        negative, positive = norms(middle)
        counts.integer_comparisons += 1
        if negative >= positive:
            high = middle
        else:
            low = middle+1
    candidates = sorted({max(0, low-1), low})
    best = min(candidates, key=lambda a: (max(norms(a)), a))
    counts.integer_comparisons += max(0, len(candidates)-1)
    left, right = norms(best)
    return -best, {
        'rank': r, 'node_count': 2*r-1, 'node_offset': -best,
        'nodes_last': 2*r-2-best,
        'left_endpoint_absolute_row_norm': left,
        'right_endpoint_absolute_row_norm': right,
        'maximum_absolute_row_norm': max(left, right),
        'objective': 'exact minimax unweighted absolute falling-binomial evaluation row sum',
        'selection': 'dimension-only monotone crossing; lower magnitude wins ties',
        'counts': asdict(counts),
        'setup_seconds': perf_counter()-started,
    }


if __name__ == '__main__':
    import json
    from math import comb
    records = []
    for rank in range(2, 130):
        offset, report = choose_offset(rank)
        exhaustive = []
        for a in range(rank):
            negative = 1 if a == 0 else comb(a+rank-1, rank-1)
            positive = sum(comb(2*rank-2-a, j) for j in range(rank))
            exhaustive.append((max(negative, positive), a))
        expected, a = min(exhaustive)
        if offset != -a or report['maximum_absolute_row_norm'] != expected:
            raise ArithmeticError(('minimax offset mismatch', rank, offset, a))
        records.append({k: report[k] for k in ('rank','node_offset','maximum_absolute_row_norm')})
    print(json.dumps({'status': 'passed', 'exhaustive_dimension_controls': len(records),
                      'selected': [row for row in records if row['rank'] in (8,16,32,64,128)]}, indent=2))
