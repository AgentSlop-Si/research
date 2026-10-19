#!/usr/bin/env python3
"""Fresh exact controls for the order-5q middle-interval proof.

Standard-library integer arithmetic only. This verifies controls and finite
lemmas; it is not an exhaustive search over square masks.
"""
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COUNTS = {'crt_pairs': 0, 'full_gram_entries': 0, 'primitive_overlap_cases': 0,
          'union_support_cases': 0, 'degree_values': 0, 'partner_selections': 0}


def save(name, obj):
    (ROOT / name).write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def crt_data(q):
    n = 5*q
    e5 = q*pow(q, -1, 5)
    eq = 5*pow(5, -1, q)
    assert (e5+eq) % n == 1
    assert (e5*eq) % n == 0
    assert (e5*e5-e5) % n == (eq*eq-eq) % n == 0
    def index(a, b):
        return (e5*a+eq*b) % n
    assert len({index(a,b) for a in range(5) for b in range(q)}) == n
    for r in range(n):
        for c in range(n):
            assert (r*c-e5*(r%5)*(c%5)-eq*(r%q)*(c%q)) % n == 0
            COUNTS['crt_pairs'] += 1
    return n, e5, eq, index


def reduced_hist(hist, q):
    """Exact coefficients in alpha^a beta^b, a<4,b<q-1.

    hist[k] is the coefficient of the original zeta^(k). Since zeta^k
    = alpha^(k mod5) beta^(k modq), this retains original phases.
    """
    grid = [[0]*q for _ in range(5)]
    for k, coefficient in enumerate(hist):
        grid[k%5][k%q] += coefficient
    return tuple(grid[a][b]-grid[a][q-1]-grid[4][b]+grid[4][q-1]
                 for a in range(4) for b in range(q-1))


def gram_remainder(support, difference, q):
    n = 5*q
    hist = [0]*n
    for c in bits(support):
        hist[(difference*c)%n] += 1
    return reduced_hist(hist, q)


def transpose(rows, n):
    columns = [0]*n
    for r, mask in enumerate(rows):
        for c in bits(mask):
            columns[c] |= 1 << r
    return columns


def order_type(difference, q):
    if difference % 5 == 0:
        return 'order_q'
    if difference % q == 0:
        return 'order_5'
    return 'primitive'


def gram_check(rows, q, degree, expected_valid):
    n = 5*q
    columns = transpose(rows, n)
    assert all(row.bit_count() == degree for row in rows)
    assert all(col.bit_count() == degree for col in columns)
    result = {'N': n, 'q': q, 'degree': degree, 'row_regular': True,
              'column_regular': True, 'expected_equality_mask': expected_valid,
              'orders': {}, 'first_nonzero': {}}
    for orientation, supports in [('rows', rows), ('columns', columns)]:
        tally = {kind: {'zero': 0, 'nonzero': 0} for kind in
                 ['order_q', 'order_5', 'primitive']}
        for i in range(n):
            for j in range(n):
                difference = i-j if orientation == 'rows' else j-i
                rem = gram_remainder(supports[i] & supports[j], difference, q)
                COUNTS['full_gram_entries'] += 1
                if i == j:
                    assert rem == (degree,) + (0,)*(4*(q-1)-1)
                    continue
                kind = order_type(difference, q)
                zero = not any(rem)
                tally[kind]['zero' if zero else 'nonzero'] += 1
                if not zero and orientation not in result['first_nonzero']:
                    result['first_nonzero'][orientation] = {
                        'indices': [i,j], 'difference_mod_N': difference%n,
                        'type': kind, 'common_original_indices': list(bits(supports[i]&supports[j])),
                        'basis_remainder': list(rem)}
                if expected_valid:
                    assert zero, (q, degree, orientation, i, j, rem)
        if not expected_valid:
            assert tally['primitive']['nonzero'] > 0
            if orientation == 'rows':
                assert tally['order_q']['nonzero'] == 0
        result['orders'][orientation] = tally
    return result


def divisor_mask(n, degree):
    m = n//degree
    assert degree*m == n
    return [sum(1 << c for c in range(n) if c % m == r//degree) for r in range(n)]


def near_mask(q, index):
    rows = [0]*(5*q)
    for a in range(5):
        baseline = {a,(a+1)%5}
        for b in range(q):
            rows[index(a,b)] = sum(1 << index(u,v) for u in range(5)
                                  for v in range(q) if u in baseline or v == b)
    return rows


def overlap_support(A, C, v, w, q, index):
    return sum(1 << index(u,t) for u in range(5) for t in range(q)
               if (u in A or t == v) and (u in C or t == w))


def primitive_sweep(q, index):
    pairs = [frozenset(A) for A in itertools.combinations(range(5), 2)]
    count = 0
    first = None
    for A in pairs:
        for C in pairs:
            if A == C:
                continue
            h = len(A & C)
            assert h in (0,1)
            for v in range(q):
                for w in range(q):
                    if v == w:
                        continue
                    support = overlap_support(A,C,v,w,q,index)
                    fiber_counts = [sum((support >> index(u,t)) & 1 for u in range(5))
                                    for t in range(q)]
                    assert fiber_counts[v] == fiber_counts[w] == 2
                    assert all(fiber_counts[t] == h for t in range(q) if t not in (v,w))
                    assert not all(x in (0,5) for x in fiber_counts)
                    assert len(set(fiber_counts)) == 2
                    for da in range(1,5):
                        for db in range(1,q):
                            difference = index(da,db)
                            rem = gram_remainder(support,difference,q)
                            assert any(rem)
                            count += 1
                            if first is None:
                                first = {'A': sorted(A), 'C': sorted(C), 'v': v, 'w': w,
                                         'difference_original': difference,
                                         'common_original_columns': list(bits(support)),
                                         'basis_remainder': list(rem)}
    COUNTS['primitive_overlap_cases'] += count
    return {'q': q, 'cases': count, 'all_nonzero_exact': True, 'first_certificate': first}


def reduction_controls(q, index):
    # Enumerate all cycle-union supports with <=2 full q-lines. This does not
    # assert that all arbitrary supports were enumerated; the proof derives
    # the cycle-union form from column degree.
    rowtypes = {}
    for ell in range(3):
        for A in itertools.combinations(range(5),ell):
            for Bmask in range((1<<q)-1):
                B = frozenset(bits(Bmask))
                support = sum(1<<index(u,v) for u in range(5) for v in range(q)
                              if u in A or v in B)
                degree = support.bit_count()
                assert degree == ell*q+(5-ell)*len(B)
                COUNTS['union_support_cases'] += 1
                if 2*q < degree < 3*q:
                    assert B
                    rowtypes.setdefault(str(degree), set()).add((ell,len(B)))
    for degree in range(2*q+1,3*q):
        singleton_solutions = [ell for ell in range(3) if 5+ell*(q-1) == degree]
        assert singleton_solutions == ([2] if degree == 2*q+3 else [])
        COUNTS['degree_values'] += 1
    # All affine permutation controls, every b, all special fibers. The
    # symbolic proof permits arbitrary permutations; this is a count control.
    for multiplier in range(1,q):
        for shift in range(q):
            perm = [(multiplier*b+shift)%q for b in range(q)]
            assert len(set(perm)) == q
            for b in range(q):
                for special in range(q):
                    choices = [bp for bp in range(q) if bp != b and perm[bp] != special]
                    assert len(choices) >= q-2 > 0
                    COUNTS['partner_selections'] += 1
    return {'q': q, 'cycle_union_types_in_interval':
            {d: [list(t) for t in sorted(types)] for d,types in sorted(rowtypes.items(), key=lambda p:int(p[0]))},
            'singleton_fiber_only_degree': 2*q+3,
            'minimum_primitive_different_fiber_partners': q-2}


def main():
    bound = json.loads((ROOT/'SOURCE_BINDINGS.json').read_text())
    for source in bound:
        data = (ROOT/source['copy']).read_bytes()
        assert len(data) == source['bytes']
        assert hashlib.sha256(data).hexdigest() == source['sha256']
    positives, negatives, reductions, sweeps = [],[],[],[]
    for q in [7,11,13,17,19,23]:
        n,e5,eq,index = crt_data(q)
        if q in [7,11,13,17]:
            for degree in [1,5,q,n]:
                positives.append(gram_check(divisor_mask(n,degree),q,degree,True))
            rows = near_mask(q,index)
            negative = gram_check(rows,q,2*q+3,False)
            if q == 7:
                negative['literal_original_index_rows'] = [format(row,f'0{n}b')[::-1] for row in rows]
            negatives.append(negative)
        if q in [7,11]:
            sweeps.append(primitive_sweep(q,index))
            reductions.append(reduction_controls(q,index))
    save('POSITIVE_CONTROLS.json', positives)
    save('NEGATIVE_CONTROLS.json', negatives)
    save('PRIMITIVE_OVERLAP_CERTIFICATES.json', sweeps)
    save('REDUCTION_CONTROLS.json', reductions)
    result = {'status':'PASS','counts':COUNTS,'source_bindings_checked':len(bound),
              'positive_mask_parameters':[[x['N'],x['degree']] for x in positives],
              'negative_mask_parameters':[[x['N'],x['degree']] for x in negatives],
              'arithmetic':'Exact integer reduction in the original cyclotomic rational basis',
              'scope':'Symbolic theorem supplemented by exact finite controls; no square-mask census',
              'external_writes':False,'floating_point_used':False}
    save('RESULTS.json',result)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
