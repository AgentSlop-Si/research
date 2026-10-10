#!/usr/bin/env python3
"""Fresh independent integer controls; no inherited research code is imported.

Two deliberately separate routes are compared:
  * scores from exact regular-action permutation cycles and subset DP;
  * recursive coset-family recognition and subgroup-lattice counting.
All identity-first permutations are also inspected for groups of size at most 9.
"""
from array import array
from functools import lru_cache
from itertools import permutations, product
from math import factorial
from fractions import Fraction
import json
import random
import sys
import time


def prime(n):
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def predicted(m):
    n, d, w = m, 2, Fraction(0)
    while d <= n:
        while n % d == 0:
            w += Fraction(d - 1, d)
            n //= d
        d += 1
    answer = m * w
    assert answer.denominator == 1
    return int(answer)


def group_tables(moduli):
    elements = list(product(*(range(n) for n in moduli)))
    index = {x: i for i, x in enumerate(elements)}
    add = [[index[tuple((a + b) % n for a, b, n in zip(x, y, moduli))]
            for y in elements] for x in elements]
    inverse = [index[tuple((-a) % n for a, n in zip(x, moduli))]
               for x in elements]
    return elements, add, inverse


def all_stabilizers(add):
    """Generate invariant sets via whole cycles, without testing prefix formulas."""
    n = len(add)
    answer = array('I', [1]) * (1 << n)
    for g in range(1, n):
        unseen = set(range(n))
        cycles = []
        while unseen:
            x = min(unseen)
            cycle = 0
            while x in unseen:
                unseen.remove(x)
                cycle |= 1 << x
                x = add[g][x]
            cycles.append(cycle)
        invariant = [0]
        for cycle in cycles:
            invariant += [s | cycle for s in invariant]
        for s in invariant:
            answer[s] |= 1 << g
    return answer


def subgroups(add):
    """Enumerate subgroup closures in the product group from scratch."""
    n = len(add)
    groups = {frozenset({0})}
    queue = list(groups)
    for h in queue:
        for g in range(n):
            if g in h:
                continue
            result = set(h)
            layer = set(h)
            while True:
                layer = {add[g][x] for x in layer}
                if layer <= result:
                    break
                result |= layer
            subgroup = frozenset(result)
            if subgroup not in groups:
                groups.add(subgroup)
                queue.append(subgroup)
    return sorted(groups, key=lambda h: (len(h), tuple(sorted(h))))


EXPECTED = {
    (4,): (4, 8), (2, 2): (4, 24), (6,): (7, 120),
    (8,): (12, 128), (4, 2): (12, 1408), (2, 2, 2): (12, 8064),
    (9,): (12, 1296), (3, 3): (12, 5184),
    (12,): (20, 31872), (6, 2): (20, 169344),
    (6, 3): (33, 95219712),
}


def check_group(moduli):
    start = time.monotonic()
    elements, add, inverse = group_tables(moduli)
    n = len(elements)
    stabs = all_stabilizers(add)
    groups = subgroups(add)
    total = frozenset(range(n))

    @lru_cache(None)
    def maximal(h):
        return tuple(k for k in groups if k < h and prime(len(h) // len(k))
                     and len(h) % len(k) == 0)

    @lru_cache(None)
    def family_count(h):
        if len(h) == 1:
            return 1
        return sum(factorial(len(h) // len(k)) * family_count(k) ** (len(h) // len(k))
                   for k in maximal(h))

    # Independent exact maximum over all identity-first maximal Boolean chains.
    size = 1 << (n - 1)
    best = array('h', [0]) * size
    counts = [0] * size
    counts[0] = 1
    for s in range(1, size):
        weight = stabs[(s << 1) | 1].bit_count() - 1
        remaining = s
        optimum, ways = -1, 0
        while remaining:
            bit = remaining & -remaining
            predecessor = s ^ bit
            value = best[predecessor]
            if value > optimum:
                optimum, ways = value, counts[predecessor]
            elif value == optimum:
                ways += counts[predecessor]
            remaining ^= bit
        best[s], counts[s] = optimum + weight, ways
    observed = (best[-1], counts[-1] * n)
    assert observed == (predicted(n), family_count(total)), (moduli, observed)
    if moduli in EXPECTED:
        assert observed == EXPECTED[moduli]

    enumerated = 0
    exhaustive_optima = 0
    if n <= 9:
        @lru_cache(None)
        def hierarchy_tops(order, h):
            if len(h) == 1:
                return (h,)
            valid = []
            for k in maximal(h):
                width = len(k)
                blocks = [order[i:i + width] for i in range(0, len(order), width)]
                local = [tuple(add[inverse[b[0]]][x] for x in b) for b in blocks]
                if all(frozenset(b) == k for b in local):
                    if all(hierarchy_tops(b, k) for b in local):
                        valid.append(k)
            return tuple(valid)

        for tail in permutations(range(1, n)):
            order = (0,) + tail
            score = 0
            mask = 0
            generated = {0}
            for j, x in enumerate(order):
                mask |= 1 << x
                hbits = stabs[mask]
                # Audit the cycle route against literal translation on every prefix.
                direct = sum(1 << g for g in range(n)
                             if {add[g][y] for y in order[:j + 1]} == set(order[:j + 1]))
                assert hbits == direct
                score += hbits.bit_count() - 1
                h = [g for g in range(n) if (hbits >> g) & 1]
                generated = {add[a][b] for a in generated for b in h}
                assert all((mask >> x) & 1 for x in generated)
            tops = hierarchy_tops(order, total)
            optimal = score == observed[0]
            assert optimal == bool(tops), (moduli, order, score, tops)
            if optimal:
                assert len(tops) == 1
                exhaustive_optima += 1
            enumerated += 1
        assert enumerated == factorial(n - 1)
        assert exhaustive_optima * n == observed[1]

    return {
        'moduli': moduli, 'order': n, 'maximum': observed[0],
        'maximizing_labeled_orders': observed[1],
        'identity_first_dp_states': size,
        'identity_first_permutations_enumerated': enumerated,
        'subgroups_enumerated': len(groups),
        'checks': 'maximum, count recurrence, supplied examples; plus full optimizer characterization and accumulated-coset lemma when order <= 9',
        'elapsed_seconds': round(time.monotonic() - start, 4),
    }


def primitive_root(p):
    for g in range(2, p):
        if len({pow(g, j, p) for j in range(p - 1)}) == p - 1:
            return g
    raise AssertionError(p)


def cyclic_hierarchy(n):
    if n == 1:
        return [0]
    q = next(q for q in range(2, n + 1) if n % q == 0 and prime(q))
    internal = cyclic_hierarchy(n // q)
    return [q * x + a for a in range(q) for x in internal]


def check_fourier(p):
    """Use exact integer cyclotomic coefficient vectors, never floating zeros."""
    n = p - 1
    generator = primitive_root(p)
    optimal = [pow(generator, e, p) for e in cyclic_hierarchy(n)]
    if p <= 7:
        orders = list(permutations(range(1, p)))
    else:
        rng = random.Random(1753000 + p)
        orders = [tuple(optimal), tuple(range(1, p)), tuple(range(p - 1, 0, -1))]
        for _ in range(97):
            shuffled = list(range(1, p))
            rng.shuffle(shuffled)
            orders.append(tuple(shuffled))
    optimum_seen = -1
    for order in orders:
        coefficient_vectors = [[0] * p for _ in range(p)]
        prefix = set()
        total_zeros = 0
        for x in order:
            prefix.add(x)
            # Expand beta_(x-1) * zeta^((x-1)t) directly in Z[zeta].
            for t, coeffs in enumerate(coefficient_vectors):
                coeffs[((x - 1) * t + x) % p] += 1
                coeffs[((x - 1) * t - x) % p] -= 1
            zero_columns = {t for t, c in enumerate(coefficient_vectors)
                            if len(set(c)) == 1}
            stabilizer = {a for a in range(1, p)
                          if {a * x % p for x in prefix} == prefix}
            assert len(zero_columns) == len(stabilizer) - 1
            assert not ({1, p - 1} & zero_columns)
            total_zeros += len(zero_columns)
        assert total_zeros <= predicted(n)
        optimum_seen = max(optimum_seen, total_zeros)
    assert optimum_seen == predicted(n)
    return {'prime': p, 'orders_checked': len(orders),
            'maximum_zeros_seen': optimum_seen,
            'minimum_nnz_R': p * p - optimum_seen,
            'minimum_total_E': 2 * p * p + 2 * p - 2 - optimum_seen,
            'scope': 'all orders' if p <= 7 else 'deterministic hierarchy and fixed-seed samples'}


def main():
    result = {'method': 'fresh standard-library-only exact controls',
              'group_results': [], 'fourier_results': []}
    specs = [(), (2,), (3,), (4,), (2, 2), (5,), (6,), (7,), (8,),
             (4, 2), (2, 2, 2), (9,), (3, 3), (10,), (11,), (12,),
             (6, 2), (16,), (4, 4), (8, 2), (4, 2, 2), (2, 2, 2, 2),
             (18,), (6, 3)]
    for spec in specs:
        row = check_group(spec)
        result['group_results'].append(row)
        print(json.dumps(row), flush=True)
    for p in (5, 7, 11, 13, 17, 19, 31):
        row = check_fourier(p)
        result['fourier_results'].append(row)
        print(json.dumps(row), flush=True)
    result['all_assertions_passed'] = True
    with open(sys.argv[1], 'w', encoding='utf-8') as output:
        json.dump(result, output, indent=2)
        output.write('\n')


if __name__ == '__main__':
    main()
