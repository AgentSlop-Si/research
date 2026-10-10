#!/usr/bin/env python3
"""Independent standard-library audit of the supplied bounded-chirp-rank note.

Written from the mathematical claims on 2026-10-09. No uploaded code is loaded
or executed. Small finite-field tests are exact; they are not speed benchmarks.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import time


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def field_for(n):
    p = n + 1
    while not is_prime(p):
        p += n
    for z in range(1, p):
        powers = [1]
        for _ in range(1, n):
            powers.append(powers[-1] * z % p)
        if powers[-1] * z % p == 1 and len(set(powers)) == n:
            return p, z, powers
    raise AssertionError('no root')


def make_signal(n, p, powers, a, frequencies, coefficients):
    return [powers[a*j*j % n] * sum(c*powers[b*j % n]
            for b, c in zip(frequencies, coefficients)) % p for j in range(n)]


def direct_dft(x, p, powers):
    n = len(x)
    return [sum(x[j]*powers[-j*k % n] for j in range(n)) % p
            for k in range(n)]


def poly_eval(coeffs, t, p):
    value = 0
    for c in reversed(coeffs):
        value = (value*t + c) % p
    return value


def eliminant(x, r, start, p):
    degree = math.comb(r + 2, 3)
    minimum = (r + 1)*r*(r - 1)//2
    coeffs = [0]*(degree + 1)
    for perm in itertools.permutations(range(r + 1)):
        inversions = sum(perm[i] > perm[j] for i in range(r + 1)
                         for j in range(i + 1, r + 1))
        value = -1 if inversions % 2 else 1
        exponent = -minimum
        for i, j in enumerate(perm):
            k = i + j
            exponent += k*(k - 1)//2
            value = value*x[start + k] % p
        assert 0 <= exponent <= degree
        coeffs[exponent] = (coeffs[exponent] + value) % p
    return coeffs


def determinant(matrix, p):
    a = [row[:] for row in matrix]
    det = 1
    for k in range(len(a)):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            det = -det
        det = det*a[k][k] % p
        inverse = pow(a[k][k], -1, p)
        for i in range(k + 1, len(a)):
            factor = a[i][k]*inverse % p
            for j in range(k + 1, len(a)):
                a[i][j] = (a[i][j] - factor*a[k][j]) % p
    return det % p


def bounded_bm(y, r, p):
    """C[0]=1, sum_i C[i] y[n-i]=0. Abort before an update exceeding r."""
    c, b = [1], [1]
    order, delay, inverse_baseline, inversions = 0, 1, 1, 0
    for n, sample in enumerate(y):
        discrepancy = (sample + sum(c[i]*y[n-i]
                         for i in range(1, order + 1))) % p
        if discrepancy == 0:
            delay += 1
            continue
        increases = 2*order <= n
        new_order = n + 1 - order if increases else order
        if new_order > r:
            return None, {'inversions': inversions, 'abort_at': n}
        old = c[:]
        factor = discrepancy*inverse_baseline % p
        needed = max(len(c), len(b) + delay)
        c += [0]*(needed - len(c))
        for j, value in enumerate(b):
            c[j + delay] = (c[j + delay] - factor*value) % p
        if increases:
            order, b = new_order, old
            inverse_baseline = pow(discrepancy, -1, p)
            inversions += 1
            delay = 1
        else:
            delay += 1
        assert len(c) <= order + 1
        c += [0]*(order + 1 - len(c))
    assert inversions <= r
    return c, {'inversions': inversions, 'order': order}


def solve(matrix, rhs, p):
    a = [row[:] + [value] for row, value in zip(matrix, rhs)]
    n = len(a)
    for j in range(n):
        k = next(i for i in range(j, n) if a[i][j])
        a[j], a[k] = a[k], a[j]
        inv = pow(a[j][j], -1, p)
        a[j] = [v*inv % p for v in a[j]]
        for i in range(n):
            if i != j:
                factor = a[i][j]
                a[i] = [(v - factor*w) % p for v, w in zip(a[i], a[j])]
    return [row[-1] for row in a]


def gauss_row(n, p, powers, a):
    """Return S_a(c) for all c, sharing one base sum across all modes."""
    d = math.gcd(a, n)
    m, reduced_a = n//d, a//d
    out = [0]*n
    if m == 1:
        out[0] = n % p
        return out
    if m % 2:
        base = sum(powers[d*reduced_a*j*j % n] for j in range(m)) % p
        inverse = pow(4*reduced_a, -1, m)
        for v in range(m):
            out[d*v] = d*base*powers[d*(-v*v*inverse % m)] % p
    else:
        q = m//2
        v0 = q % 2
        base = sum(powers[d*(reduced_a*j*j + v0*j) % n]
                   for j in range(m)) % p
        inverse = pow(reduced_a, -1, q) if q > 1 else 0
        for v in range(v0, m, 2):
            t = ((v - v0)//2*inverse) % q if q > 1 else 0
            out[d*v] = d*base*powers[d*((-reduced_a*t*t - v0*t) % m)] % p
    return out


def transform_representation(n, p, powers, a, frequencies, coefficients):
    row = gauss_row(n, p, powers, a)
    return [sum(c*row[(b-k) % n] for b, c in zip(frequencies, coefficients)) % p
            for k in range(n)]


def recognize(x, p, powers, r):
    n = len(x)
    assert n >= 3*r and r >= 1 and len(powers) == n
    if not any(x):
        return {'a': 0, 'frequencies': [], 'coefficients': [], 'output': [0]*n,
                'candidates': 0, 'bm_inversions': 0}
    center = next((j for j in range(r, n-r) if x[j]), None)
    if center is None:
        return None
    polynomial = eliminant(x, r, center-r, p)
    candidates = [a for a in range(n//math.gcd(2, n))
                  if poly_eval(polynomial, powers[-2*a % n], p) == 0]
    assert len(candidates) <= math.comb(r + 2, 3)
    for a in candidates:
        y = [value*powers[-a*j*j % n] % p for j, value in enumerate(x)]
        recurrence, info = bounded_bm(y, r, p)
        if recurrence is None:
            continue
        s = len(recurrence) - 1
        frequencies = [b for b, z in enumerate(powers)
                       if poly_eval(list(reversed(recurrence)), z, p) == 0]
        if len(frequencies) != s:
            continue
        nodes = [powers[b] for b in frequencies]
        coefficients = solve([[pow(z, j, p) for z in nodes] for j in range(s)],
                             y[:s], p)
        if any(c == 0 for c in coefficients):
            continue
        values = coefficients[:]
        valid = True
        for target in y:
            if sum(values) % p != target:
                valid = False
                break
            values = [v*z % p for v, z in zip(values, nodes)]
        if valid:
            return {'a': a, 'frequencies': frequencies, 'coefficients': coefficients,
                    'output': transform_representation(n, p, powers, a,
                                                       frequencies, coefficients),
                    'candidates': len(candidates), 'bm_inversions': info['inversions']}
    return None


def rank(matrix, p):
    a = [row[:] for row in matrix]
    h = 0
    for j in range(len(a[0])):
        k = next((i for i in range(h, len(a)) if a[i][j]), None)
        if k is None:
            continue
        a[h], a[k] = a[k], a[h]
        inv = pow(a[h][j], -1, p)
        for i in range(h+1, len(a)):
            factor = a[i][j]*inv % p
            for col in range(j, len(a[0])):
                a[i][col] = (a[i][col] - factor*a[h][col]) % p
        h += 1
        if h == len(a):
            break
    return h


def audit(output_dir):
    started = time.time()
    rng = random.Random(202610091908)
    result = {'status': 'running', 'seed': 202610091908,
              'source_library_file_id': '[private-id]',
              'source_sha256': hashlib.sha256((output_dir/'source/RESEARCH (2).md').read_bytes()).hexdigest(),
              'independent_code': True, 'uploaded_code_executed': False}
    gauss_cases = gauss_bins = 0
    for n in range(1, 81):
        p, omega, powers = field_for(n)
        for a in range(n):
            got = gauss_row(n, p, powers, a)
            expected = [sum(powers[(a*j*j + c*j) % n] for j in range(n)) % p
                        for c in range(n)]
            assert got == expected, ('gauss', n, p, a)
            gauss_cases += 1
            gauss_bins += n
    result['all_gauss_phases'] = {'lengths': [1, 80], 'rows': gauss_cases, 'bins': gauss_bins}
    print('Gauss rows checked:', gauss_cases, gauss_bins, flush=True)

    determinant_evaluations = 0
    for r in range(1, 7):
        n = 3*r + 1
        p, _, _ = field_for(n)
        for case in range(12):
            x = [rng.randrange(p) for _ in range(n)]
            x[r] = rng.randrange(1, p)
            coeffs = eliminant(x, r, 0, p)
            assert coeffs[0] == (-1)**(r*(r+1)//2)*pow(x[r], r+1, p) % p
            assert coeffs[-1] == math.prod(x[2*i] for i in range(r+1)) % p
            for t in range(1, min(p, 12)):
                matrix = [[x[i+j]*pow(t, (i+j)*(i+j-1)//2, p) % p
                           for j in range(r+1)] for i in range(r+1)]
                minimum = (r+1)*r*(r-1)//2
                assert poly_eval(coeffs, t, p)*pow(t, minimum, p) % p == determinant(matrix, p)
                determinant_evaluations += 1
    result['determinants'] = {'ranks': [1, 6], 'polynomials': 72,
                              'independent_gaussian_evaluations': determinant_evaluations}
    print('Determinants checked:', determinant_evaluations, flush=True)

    structured_runs = structured_bins = 0
    max_candidates = {}
    for r in range(1, 7):
        lengths = sorted(set([3*r, 3*r+1, 3*r+2, 32, 45, 64, 97]))
        for n in lengths:
            if n < 3*r:
                continue
            p, _, powers = field_for(n)
            phases = sorted(set([0, 1, n//2, n-1] + [rng.randrange(n) for _ in range(3)]))
            for a in phases:
                s = rng.randrange(1, r+1)
                frequencies = rng.sample(range(n), s)
                coefficients = [rng.randrange(1, p) for _ in range(s)]
                x = make_signal(n, p, powers, a, frequencies, coefficients)
                recognized = recognize(x, p, powers, r)
                assert recognized is not None, ('structured rejection', n, r, a)
                assert recognized['output'] == direct_dft(x, p, powers)
                assert recognized['a'] < n//math.gcd(2, n)
                structured_runs += 1
                structured_bins += n
                max_candidates[str(r)] = max(max_candidates.get(str(r), 0), recognized['candidates'])
    result['structured'] = {'runs': structured_runs, 'full_dft_bins': structured_bins,
                            'maximum_candidates_seen_by_rank': max_candidates}
    print('Structured runs checked:', structured_runs, structured_bins, flush=True)

    exhaustive = []
    for n, p, r in [(3, 7, 1), (4, 5, 1), (6, 7, 2)]:
        _, _, powers = field_for(n)
        assert field_for(n)[0] == p
        family = {(0,)*n}
        for a in range(n//math.gcd(2, n)):
            for s in range(1, r+1):
                for frequencies in itertools.combinations(range(n), s):
                    for coefficients in itertools.product(range(1, p), repeat=s):
                        family.add(tuple(make_signal(n, p, powers, a, frequencies, coefficients)))
        accepted = 0
        for x in itertools.product(range(p), repeat=n):
            recognized = recognize(x, p, powers, r)
            assert (recognized is not None) == (x in family), ('membership', n, r, x)
            if recognized is not None:
                assert recognized['output'] == direct_dft(x, p, powers)
                accepted += 1
        exhaustive.append({'n': n, 'p': p, 'r': r, 'vectors': p**n,
                           'family_size': len(family), 'accepted': accepted})
        print('Exhaustive space checked:', n, p, r, p**n, accepted, flush=True)
    result['exhaustive_membership'] = exhaustive

    dense_runs = dense_accepted = 0
    for n in [9, 12, 17, 18, 31, 32, 33, 63, 64]:
        p, _, powers = field_for(n)
        for r in range(1, 4):
            for _ in range(30):
                x = [rng.randrange(p) for _ in range(n)]
                recognized = recognize(x, p, powers, r)
                if recognized is not None:
                    dense_accepted += 1
                    assert recognized['output'] == direct_dft(x, p, powers)
                dense_runs += 1
    result['dense_random'] = {'runs': dense_runs, 'accepted_and_verified': dense_accepted,
                              'rejected': dense_runs-dense_accepted}

    cancellation_runs = 0
    for r in range(1, 7):
        n = 3*r
        p, _, powers = field_for(n)
        nodes = [powers[b] for b in range(r)]
        # Force precisely r-1 consecutive zero samples at the start of the
        # scanned interior. A nonsingular r-row system makes the next sample 1.
        coefficients = solve([[pow(z, r+j, p) for z in nodes] for j in range(r)],
                             [0]*(r-1)+[1], p)
        assert all(coefficients)
        for a in [0, 1, n//2, n-1]:
            x = make_signal(n, p, powers, a, list(range(r)), coefficients)
            assert x[r:2*r-1] == [0]*(r-1) and x[2*r-1] != 0
            got = recognize(x, p, powers, r)
            assert got is not None and got['output'] == direct_dft(x, p, powers)
            cancellation_runs += 1
        zero = recognize([0]*n, p, powers, r)
        assert zero is not None and zero['frequencies'] == []
        # A nonzero endpoint-only vector has r consecutive interior zeroes.
        endpoint = [0]*n
        endpoint[0] = 1
        assert recognize(endpoint, p, powers, r) is None
    result['boundary_and_cancellation'] = {'forced_cancellation_runs': cancellation_runs,
                                          'zero_rank_tests': 6, 'no_witness_rejections': 6}

    ranks = []
    for n in [7, 17, 31, 63, 119, 127]:
        p, _, powers = field_for(n)
        x = make_signal(n, p, powers, 1, [0], [1])
        m = n//2
        got = rank([[x[i+j] for j in range(m)] for i in range(m)], p)
        assert got == m
        ranks.append({'n': n, 'p': p, 'rank': got})
    result['ordinary_hankel_ranks'] = ranks
    result['status'] = 'pass'
    result['elapsed_seconds'] = round(time.time()-started, 3)
    result['checker_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (output_dir/'independent_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    audit(args.output_dir)
