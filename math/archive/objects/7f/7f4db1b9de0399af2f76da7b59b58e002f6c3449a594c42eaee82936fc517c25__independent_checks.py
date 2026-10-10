#!/usr/bin/env python3
"""Independent, standard-library exact checks for the spliced MGG bank.

This file is authored for the review. It does not import or execute any
constructor or uploaded code. The external MGG spectral theorem is a stated
premise; the checker verifies finite structural controls and exact thresholds.
"""
import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path


LABELS = [(axis, offset, sign) for axis in ('H', 'V')
          for offset in (0, 1) for sign in (1, -1)]


def permutation(a, b, label):
    axis, offset, sign = label
    p = []
    for y in range(b):
        for x in range(a):
            if axis == 'H':
                p.append(y * a + (x + sign * (2*y + offset)) % a)
            else:
                p.append(((y + sign * (2*x + offset)) % b) * a + x)
    return p


def cycles(p):
    seen = bytearray(len(p))
    reps = []
    for v in range(len(p)):
        if seen[v]:
            continue
        reps.append(v)
        w = v
        while not seen[w]:
            seen[w] = 1
            w = p[w]
        assert w == v
    return reps


def splice(p, reps):
    q = p.copy()
    if len(reps) > 1:
        for j, v in enumerate(reps):
            q[v] = p[reps[(j+1) % len(reps)]]
    return q


def predicted_counts(r, rectangular):
    m = 1 << r
    if rectangular:
        base = {('H', 0): m*(r+2), ('H', 1): m,
                ('V', 0): 2*m*(r+1), ('V', 1): 2*m}
    else:
        base = {('H', 0): m*(r+1), ('H', 1): m,
                ('V', 0): m*(r+1), ('V', 1): m}
    return [base[(axis, offset)] for axis, offset, _ in LABELS]


def incoming(p, selected):
    return sum((v not in selected and p[v] in selected)
               for v in range(len(p)))


def exact_threshold(k):
    r = k // 2
    m = 1 << r
    n = 1 << k
    rectangular = bool(k % 2)
    loss = m*(3*r+7) if rectangular else 2*m*(r+2)
    # 3*((8-5*sqrt(2))*n/4-loss) > n/2.
    left = 22*n - 12*loss
    strict = left > 0 and left*left > 450*n*n
    rational_margin = Fraction(3*n, 16) - 3*loss
    return {'k': k, 'N': n, 'm': m, 'shape': 'rectangle' if rectangular else 'square',
            'total_cycle_count': 2*loss, 'splice_loss_bound': loss,
            'strict_capacity_bound': strict,
            'rational_margin_3N_over_16_minus_3loss': str(rational_margin),
            'exact_squared_comparison_margin': left*left - 450*n*n}


def check_enumeration(max_k):
    rows = []
    for k in range(2, max_k+1):
        r = k//2
        m = 1 << r
        a, b = (2*m, m) if k % 2 else (m, m)
        expected = predicted_counts(r, bool(k % 2))
        counts, changed, digests = [], [], []
        for label, count in zip(LABELS, expected):
            p = permutation(a, b, label)
            assert sorted(p) == list(range(a*b))
            reps = cycles(p)
            assert len(reps) == count, (k, label, len(reps), count)
            q = splice(p, reps)
            assert sorted(q) == list(range(a*b))
            assert len(cycles(q)) == 1
            ch = sum(x != y for x, y in zip(p, q))
            assert ch == (count if count > 1 else 0)
            counts.append(count)
            changed.append(ch)
            digests.append(hashlib.sha256(','.join(map(str, q)).encode()).hexdigest())
        if k >= 6:
            assert len(set(digests)) == 8
        rows.append({'k': k, 'N': a*b, 'counts_by_label': counts,
                     'changed_edges_by_label': changed,
                     'spliced_permutation_sha256': digests})
    return rows


def check_quotient():
    rows = []
    for r in range(1, 7):
        m = 1 << r
        big_a = 2*m
        checked = 0
        for label in LABELS:
            big = permutation(big_a, big_a, label)
            small = permutation(big_a, m, label)
            def project(v):
                return (v//big_a % m)*big_a + v%big_a
            for v, pv in enumerate(big):
                assert project(pv) == small[project(v)]
                checked += 1
            axis, offset, sign = label
            inverse = permutation(big_a, m, (axis, offset, -sign))
            assert all(inverse[small[v]] == v for v in range(len(small)))
        rows.append({'m': m, 'checked_labeled_vertices': checked})
    return rows


def check_all_small_half_cuts():
    rows = []
    for a, b in [(2, 1), (2, 2), (4, 2), (4, 4)]:
        n = a*b
        ps = [permutation(a, b, label) for label in LABELS]
        cs = [cycles(p) for p in ps]
        qs = [splice(p, c) for p, c in zip(ps, cs)]
        losses = [(len(c)//2 if len(c)>1 else 0) for c in cs]
        min_pre = 8*n
        min_post = 8*n
        max_losses = [-8*n]*8
        tested = 0
        for subset in itertools.combinations(range(n), n//2):
            selected = set(subset)
            old = [incoming(p, selected) for p in ps]
            new = [incoming(q, selected) for q in qs]
            assert all(x-y <= bound for x, y, bound in zip(old, new, losses))
            min_pre = min(min_pre, sum(old))
            min_post = min(min_post, sum(new))
            max_losses = [max(z, x-y) for z, x, y in zip(max_losses, old, new)]
            # Exact finite control for e >= (8-5*sqrt(2))*N/4.
            # If 8N-4e <= 0 it is automatic; otherwise square positive sides.
            lhs = 8*n - 4*sum(old)
            assert lhs <= 0 or lhs*lhs <= 50*n*n
            tested += 1
        rows.append({'a': a, 'b': b, 'half_cuts_tested': tested,
                     'min_original_incoming': min_pre, 'min_spliced_incoming': min_post,
                     'max_observed_incoming_loss_by_label': max_losses,
                     'permutation_splice_loss_bounds': losses})
    return rows


def check_abstract_splice_loss():
    # Every pair of size-a source and size-b target subsets has overlap
    # in [max(0,a+b-c), min(a,b)]. This is exhaustive integer verification
    # of the extremal expression, supplemental to the report's proof.
    checked = 0
    for c in range(1, 257):
        for a in range(c+1):
            for b in range(c+1):
                spread = min(a, b) - max(0, a+b-c)
                assert spread == min(a, b, c-a, c-b)
                assert spread <= c//2
                checked += 1
    return checked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-k', type=int, default=18)
    parser.add_argument('--output', default='VERIFIED_RESULTS.json')
    args = parser.parse_args()
    assert args.max_k >= 4
    thresholds = [exact_threshold(k) for k in range(2, 129)]
    assert [row['k'] for row in thresholds if row['strict_capacity_bound']][0] == 17
    assert all(row['strict_capacity_bound'] == (row['k'] >= 17) for row in thresholds)
    assert Fraction(17, 12)**2 > 2
    assert Fraction(31, 512) < Fraction(1, 16)
    assert Fraction(22, 512) < Fraction(1, 16)
    result = {
        'status': 'PASS',
        'external_premise': 'MGG unnormalized mean-zero numerical radius <= 5*sqrt(2), cited in report; Isabelle not executed.',
        'labels': LABELS,
        'enumeration': check_enumeration(args.max_k),
        'quotient': check_quotient(),
        'exhaustive_small_half_cuts': check_all_small_half_cuts(),
        'abstract_splice_integer_cases': check_abstract_splice_loss(),
        'thresholds': thresholds,
        'all_k_ge_17_proof': 'rational bound sqrt(2)<17/12 and monotonic loss/N, in report',
        'scope': 'All balanced-cut aggregate incoming-edge capacities; not attained ranks or Fourier coefficients.'
    }
    path = Path(args.output)
    path.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': 'PASS', 'output': str(path),
                      'enumeration_max_k': args.max_k,
                      'threshold_first_k': 17,
                      'small_half_cuts': sum(row['half_cuts_tested'] for row in result['exhaustive_small_half_cuts']),
                      'abstract_splice_integer_cases': result['abstract_splice_integer_cases']}, sort_keys=True))


if __name__ == '__main__':
    main()
