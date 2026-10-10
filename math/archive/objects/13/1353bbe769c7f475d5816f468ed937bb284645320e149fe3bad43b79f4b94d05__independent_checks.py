#!/usr/bin/env python3
"""Independent finite controls for the common-parity-cut theorem."""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import random


def parity(x):
    return x.bit_count() & 1


def null_vector(rows, k):
    echelon = {}
    for row in rows:
        while row:
            pivot = row.bit_length()-1
            if pivot in echelon:
                row ^= echelon[pivot]
            else:
                echelon[pivot] = row
                break
    free = next(i for i in range(k) if i not in echelon)
    f = 1 << free
    for pivot in sorted(echelon):
        if parity(f & echelon[pivot]):
            f ^= 1 << pivot
    assert f and all(parity(f & row) == 0 for row in rows)
    return f, len(echelon)


def invertible_columns(k, rng):
    columns = [1 << i for i in range(k)]
    for _ in range(5*k+1):
        a, b = rng.sample(range(k), 2)
        columns = [col ^ ((1 << a) if col & (1 << b) else 0)
                   for col in columns]
    return columns


def linear_apply(columns, x):
    value = 0
    for i, col in enumerate(columns):
        if x & (1 << i):
            value ^= col
    return value


def formula_crossings(g, k):
    numerator = sum((1 << (k-h))*parity(g & ((1 << h)-1))
                    for h in range(1, k+1))
    numerator += parity(g & ((1 << k)-1))
    assert numerator % 2 == 0
    return numerator//2


def direct_crossings(values):
    return sum(a == 1 and b == 0
               for a, b in zip(values, values[1:]+values[:1]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='VERIFIED_RESULTS.json')
    args = parser.parse_args()
    formula_rows = []
    for k in range(1, 11):
        n = 1 << k
        for g in range(1, n):
            value = formula_crossings(g, k)
            assert value == direct_crossings([parity(g & x) for x in range(n)])
            low_zeros = (g & -g).bit_length()-1
            assert value <= n//(1 << (low_zeros+1))
        formula_rows.append({'k': k, 'masks_checked': n-1})
    rng = random.Random(90218431)
    banks = []
    for k in range(2, 11):
        n = 1 << k
        r = k//2
        for d in (1, 2, 3, 4, 8):
            u = (k-r-1)//d
            for trial in range(4):
                columns = [invertible_columns(k, rng) for _ in range(d)]
                shifts = [rng.randrange(n) for _ in range(d)]
                rows = [1 << i for i in range(r)]
                rows += [col for matrix in columns for col in matrix[:u]]
                f, rank = null_vector(rows, k)
                assert rank <= r+d*u <= k-1
                assert sum(parity(f & x) == 0 for x in range(n)) == n//2
                assert all(parity(f & x) == parity(f & (x//(1<<r)*(1<<r)))
                           for x in range(n))
                counts, masks = [], []
                for matrix, shift in zip(columns, shifts):
                    sigma = [linear_apply(matrix, x)^shift for x in range(n)]
                    assert len(set(sigma)) == n
                    values = [parity(f & v) for v in sigma]
                    g = sum(parity(f & col) << i for i, col in enumerate(matrix))
                    assert g and g & ((1 << u)-1) == 0
                    assert all(values[x] == (parity(g & x)^parity(f & shift))
                               for x in range(n))
                    actual = direct_crossings(values)
                    assert actual == formula_crossings(g, k)
                    assert actual <= n//(1 << (u+1))
                    counts.append(actual)
                    masks.append(g)
                # The rank comparison is M*N/2^(u+1) >= N/4.
                # Multiplicity M is distinct from the number d of orders.
                min_M = Fraction(1 << u, 2)
                assert min_M*Fraction(n, 1 << (u+1)) == Fraction(n, 4)
                banks.append({'k':k,'d':d,'trial':trial,'r':r,'u':u,
                              'constraint_rank':rank,'chosen_parity_mask':f,
                              'pullback_masks':masks,'incoming_counts':counts,
                              'necessary_total_terms_lower_bound':str(min_M)})
    result = {'status':'PASS','exhaustive_formula_controls':formula_rows,
              'formula_masks_total':sum(x['masks_checked'] for x in formula_rows),
              'banks_checked':len(banks),'banks':banks,
              'scope':'Necessary total Green occurrences M, not number of allowed orders d; characteristic-zero target rank proof is analytic.'}
    Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','formula_masks_total':result['formula_masks_total'],
                      'banks_checked':len(banks),'maps_checked':sum(b['d'] for b in banks)},sort_keys=True))


if __name__ == '__main__':
    main()
