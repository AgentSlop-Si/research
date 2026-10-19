#!/usr/bin/env python3
"""Fresh exact controls for the three proper q-multiple endpoints at N=5q.

Standard library only. Exact cyclotomic polynomial reduction, no floating point,
historical checker import/execution, optimization, or arbitrary-mask census.
"""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from math import isqrt
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
COUNT = Counter()


def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')


def poly_remainder(poly, divisor):
    a = list(poly)
    degree = len(divisor) - 1
    assert divisor[-1] == 1
    for j in range(len(a) - 1, degree - 1, -1):
        if a[j]:
            factor = a[j]
            for i, value in enumerate(divisor):
                a[j - degree + i] -= factor * value
    assert not any(a[degree:])
    return tuple(a[:degree])


def exact_monic_quotient(numerator, denominator):
    a = list(numerator)
    deg = len(denominator) - 1
    quotient = [0] * (len(a) - deg)
    for j in range(len(a) - 1, deg - 1, -1):
        factor = a[j]
        quotient[j - deg] = factor
        for i, value in enumerate(denominator):
            a[j - deg + i] -= factor * value
    assert not any(a)
    return tuple(quotient)


def bits(x):
    return [i for i in range(x.bit_length()) if (x >> i) & 1]


class Fourier:
    def __init__(self, q):
        self.q, self.n = q, 5*q
        self.p5 = q * pow(q, -1, 5)
        self.pq = 5 * pow(5, -1, q)
        # Phi_(5q)(x) = Phi_q(x^5) / Phi_q(x), since q != 5.
        top = [int(i % 5 == 0) for i in range(5*(q-1)+1)]
        self.phi = exact_monic_quotient(top, [1]*q)
        assert len(self.phi) == 4*(q-1)+1
        assert not any(poly_remainder([-1]+[0]*(self.n-1)+[1], self.phi))
        assert (self.p5+self.pq) % self.n == 1
        assert self.p5*self.pq % self.n == 0
        assert self.p5*self.p5 % self.n == self.p5 % self.n
        assert self.pq*self.pq % self.n == self.pq % self.n
        for r in range(self.n):
            for c in range(self.n):
                assert (r*c-self.p5*(r%5)*(c%5)-self.pq*(r%q)*(c%q)) % self.n == 0
                COUNT['literal_CRT_phase_products'] += 1

    def idx(self, a, b):
        return (self.p5*a+self.pq*b) % self.n

    @lru_cache(maxsize=None)
    def monomial_sum(self, powers):
        coefficients = [0] * self.n
        for exponent in powers:
            coefficients[exponent % self.n] += 1
        return poly_remainder(coefficients, self.phi)

    def overlap_sum(self, support, delta):
        return self.monomial_sum(tuple(sorted(delta*c % self.n for c in support)))


def full_gram_control(F, rows, d, expected, name):
    n = F.n
    cols = [{r for r in range(n) if c in rows[r]} for c in range(n)]
    assert all(len(s) == d for s in rows+cols)
    record = {'q': F.q, 'degree': d, 'name': name,
              'both_degrees_verified': True, 'expected_equality': expected,
              'gram_summary': {}, 'nonzero_witnesses': {}}
    for orientation, sets in [('row', rows), ('column', cols)]:
        summary = Counter()
        for i in range(n):
            for j in range(n):
                delta = i-j if orientation == 'row' else j-i
                common = sets[i] & sets[j]
                rem = F.overlap_sum(common, delta)
                COUNT['full_original_index_Gram_entries'] += 1
                if i == j:
                    assert rem == (d,)+(0,)*(len(F.phi)-2)
                    summary['correct_diagonal'] += 1
                else:
                    zero = not any(rem)
                    summary['zero_off_diagonal' if zero else 'nonzero_off_diagonal'] += 1
                    if expected:
                        assert zero, (name, orientation, i, j)
                    if not zero and orientation not in record['nonzero_witnesses']:
                        record['nonzero_witnesses'][orientation] = {
                            'original_indices': [i, j], 'difference_mod_N': delta % n,
                            'common_original_support': sorted(common),
                            'remainder_mod_cyclotomic_polynomial': list(rem)}
                    if not expected and orientation == 'row' and i % F.q != j % F.q:
                        assert zero
        if not expected:
            assert summary['nonzero_off_diagonal'] > 0
        record['gram_summary'][orientation] = dict(summary)
    if F.q == 7 and not expected:
        record['literal_original_index_mask'] = [
            ''.join('1' if c in s else '0' for c in range(n)) for s in rows]
    return record


def positive(F, d):
    n, q = F.n, F.q
    if d == 1:
        return [{r} for r in range(n)]
    if d == 5:
        return [{c for c in range(n) if c % q == r % q} for r in range(n)]
    if d == q:
        return [{c for c in range(n) if c % 5 == r % 5} for r in range(n)]
    assert d == n
    return [set(range(n)) for r in range(n)]


def endpoint_near_mask(F, k, varying):
    rows = [None] * F.n
    line_sets = []
    for a in range(5):
        seen = set()
        for b in range(F.q):
            shift = (b*b+b) % 5 if varying else 0
            A = frozenset((a+shift+t) % 5 for t in range(k))
            seen.add(A)
            rows[F.idx(a, b)] = {F.idx(u, v) for u in A for v in range(F.q)}
        line_sets.append(seen)
    if varying:
        assert all(len(s) > 1 for s in line_sets)
    return rows


def degree_controls():
    primes = [q for q in range(7, 1001)
              if all(q % t for t in range(2, isqrt(q)+1))]
    sample = []
    for q in primes:
        for k in (2, 3, 4):
            assert k*q > q+4
            solutions = [(ell, f) for ell in range(k+1) for f in range(q+1)
                         if ell*q+(5-ell)*f == k*q]
            assert solutions == [(k, 0)]
            COUNT['endpoint_degree_equations'] += 1
            sample.append({'q': q, 'k': k, 'all_integer_solutions': solutions})
    return sample


def canonical_support_controls(F):
    q = F.q
    found = Counter()
    for A_bits in range(31):  # A cannot be all five for a proper-degree row.
        A = set(bits(A_bits))
        for B_bits in range((1 << q)-1):  # B cannot be all q either.
            B = set(bits(B_bits))
            support = {(u, v) for u in range(5) for v in range(q) if u in A or v in B}
            actual_A = {u for u in range(5) if all((u, v) in support for v in range(q))}
            actual_B = {v for v in range(q) if all((u, v) in support for u in range(5))}
            assert actual_A == A and actual_B == B
            d = len(support)
            assert d == len(A)*q+(5-len(A))*len(B)
            if d in (2*q, 3*q, 4*q):
                assert not B and len(A) == d//q
                found[d//q] += 1
            COUNT['canonical_cycle_union_supports'] += 1
    assert dict(found) == {2: 10, 3: 10, 4: 5}
    for r in range(F.n):
        exceptions = {s for s in range(F.n) if s % 5 == r % 5 or s % q == r % q}
        assert r in exceptions and len(exceptions) == q+4
        COUNT['coverage_exception_sets'] += 1
    return {'q': q, 'endpoint_supports': dict(found)}


def arbitrary_five_rows(F):
    records = []
    for k in (2, 3, 4):
        choices = [frozenset(s) for s in combinations(range(5), k)]
        compatibility = {}
        for a, a2 in combinations(range(5), 2):
            for x, A in enumerate(choices):
                for y, C in enumerate(choices):
                    support = {F.idx(u, v) for u in A & C for v in range(F.q)}
                    delta = F.idx(a, 0)-F.idx(a2, 0)
                    zero = not any(F.overlap_sum(support, delta))
                    assert zero == (not (A & C))
                    compatibility[a, a2, x, y] = zero
                    COUNT['exact_order5_overlap_cases'] += 1
        candidates = 0
        witness_histogram = Counter()
        for selections in product(range(len(choices)), repeat=5):
            bad = next(((a, a2) for a, a2 in combinations(range(5), 2)
                        if not compatibility[a, a2, selections[a], selections[a2]]), None)
            assert bad is not None
            candidates += 1
            witness_histogram[str(bad)] += 1
            COUNT['arbitrary_five_row_line_set_tuples'] += 1
        records.append({'q': F.q, 'k': k, 'tuples_checked': candidates,
                        'zero_Gram_tuples': 0, 'first_bad_pair_histogram': dict(witness_histogram)})
    return records


def source_controls():
    bindings = json.loads((HERE/'SOURCE_BINDINGS.json').read_text())
    for item in bindings:
        assert sha256((HERE/item['frozen_copy']).read_bytes()).hexdigest() == item['sha256']
        COUNT['frozen_source_hashes'] += 1


def main():
    save('DEGREE_CONTROLS.json', degree_controls())
    positives, negatives, supports, arbitrary = [], [], [], []
    for q in (7, 11, 13):
        F = Fourier(q)
        for d in (1, 5, q, 5*q):
            positives.append(full_gram_control(F, positive(F, d), d, True, 'divisor_positive'))
        for k in (2, 3, 4):
            for varying in (False, True):
                label = 'row_dependent_lines' if varying else 'group_constant_lines'
                negatives.append(full_gram_control(F, endpoint_near_mask(F, k, varying),
                                                    k*q, False, label))
        if q in (7, 11):
            supports.append(canonical_support_controls(F))
            arbitrary.extend(arbitrary_five_rows(F))
    source_controls()
    save('POSITIVE_CONTROLS.json', positives)
    save('NEGATIVE_CONTROLS.json', negatives)
    save('SUPPORT_CONTROLS.json', supports)
    save('ARBITRARY_LINE_SET_CONTROLS.json', arbitrary)
    result = {'status': 'PASS', 'counts': dict(COUNT),
              'arithmetic': 'exact integer polynomial remainders modulo Phi_(5q)',
              'scope': 'd=2q,3q,4q only; prime q>5',
              'historical_scripts_imported_or_executed': False,
              'exhaustive_arbitrary_square_mask_claim': False}
    save('RESULTS.json', result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
