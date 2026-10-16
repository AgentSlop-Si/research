"""New standalone finite controls. Does not import or execute historical code."""
from itertools import product
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def rank(a, p):
    a = [list(row) for row in a]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        i = next((i for i in range(r, len(a)) if a[i][c] % p), None)
        if i is None:
            continue
        a[r], a[i] = a[i], a[r]
        q = pow(a[r][c] % p, -1, p)
        a[r] = [(v*q) % p for v in a[r]]
        for i in range(len(a)):
            if i != r:
                q = a[i][c]
                a[i] = [(x-q*y) % p for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def inverse(a, p):
    n = len(a)
    b = [[x % p for x in row] + [int(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for c in range(n):
        i = next((i for i in range(c, n) if b[i][c]), None)
        if i is None:
            return None
        b[c], b[i] = b[i], b[c]
        q = pow(b[c][c], -1, p)
        b[c] = [(v*q) % p for v in b[c]]
        for i in range(n):
            if i != c:
                q = b[i][c]
                b[i] = [(x-q*y) % p for x, y in zip(b[i], b[c])]
    return [row[n:] for row in b]


def cut(a, k, reverse=False):
    return ([row[:k] for row in a[k:]] if reverse
            else [row[k:] for row in a[:k]])


def words(t, b):
    return [k for k in range(1 << (t-1), 1 << t)
            if k & 1 and '0'*b not in format(k, f'0{t}b')]


def rev(k, t):
    return int(format(k, f'0{t}b')[::-1], 2)


def avoid_count(length, b):
    counts = [1] + [0]*(b-1)
    for _ in range(length):
        counts = [sum(counts)] + counts[:-1]
    return sum(counts)


def main():
    result = {'historical_code_executed': False, 'all_size_claims':
              'Written proofs; finite checks are corroboration only.'}
    cases = singular = 0
    for bits in product((0, 1), repeat=9):
        a = [list(bits[3*i:3*i+3]) for i in range(3)]
        ai = inverse(a, 2)
        if ai is None:
            continue
        for k in (1, 2):
            for reverse in (False, True):
                assert rank(cut(a, k, reverse), 2) == rank(cut(ai, k, reverse), 2)
                cases += 1
            if rank([row[:k] for row in a[:k]], 2) < k:
                singular += 1
    result['inverse_cut_rank'] = {'invertible_3x3_binary_matrices': cases//4,
                                 'directed_cut_equalities': cases,
                                 'singular_leading_block_cases': singular}
    pair_checks = support_rows = 0
    for b in range(2, 5):
        L = 1 << (b-1)
        d = b+L
        seen = set()
        for t in range(1, L+1):
            for k in words(t, b):
                for q in range(1 << (d-b-t)):
                    i = (1 << (b+t))*q+k
                    assert i not in seen
                    seen.add(i)
                    support_rows += 1
                for tp in range(t+1, L+1):
                    for kp in words(tp, b):
                        assert (rev(kp, tp)-rev(k, t)) % (1 << (b+t)) != 0
                        pair_checks += 1
    result['packet_identity_controls'] = {
        'b_values': [2, 3, 4], 'disjoint_routed_rows': support_rows,
        'cross_age_geometric_sum_zero_conditions': pair_checks}
    # Exact count inequalities can be checked at large d without huge vectors.
    count_checks = 0
    for b in range(7, 11):
        L = 1 << (b-1)
        weights = []
        for t in range(1, L+1):
            count = 1 if t == 1 else avoid_count(t-2, b)
            mt_over_r = Fraction(count, 1 << (b+t))
            if t >= 2:
                assert mt_over_r >= Fraction(1, 16*L)
            weights.append((b+t)*mt_over_r)
            count_checks += 1
        assert sum(weights)/2 >= Fraction(L, 64)
    result['exact_count_controls'] = {'b_values': [7, 8, 9, 10],
                                      'age_counts_checked': count_checks,
                                      'S_over_2r_at_least_L_over_64': True}
    result['negative_controls'] = {
        'signed_alpha_condition': 'alpha=-2, Delta=3, delta=1/2 passes signed test but violates absolute-value test',
        'forbidden_word_collision': None}
    # If marker avoidance is removed, the cross-age zero criterion can fail.
    for b in range(2, 5):
        found = False
        for t in range(1, 5):
            for tp in range(t+b+1, t+b+4):
                for k in words(t, b):
                    for kp in range((1 << (tp-1))+1, 1 << tp, 2):
                        if (rev(kp, tp)-rev(k, t)) % (1 << (b+t)) == 0:
                            assert '0'*b in format(kp, f'0{tp}b')
                            result['negative_controls']['forbidden_word_collision'] = {
                                'b': b, 't': t, 'tp': tp, 'k': k, 'kp': kp}
                            found = True
                            break
                    if found:
                        break
                if found:
                    break
            if found:
                break
        assert found
    result['status'] = 'PASS'
    Path(__file__).with_name('CHECK_RESULTS.json').write_text(
        json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
