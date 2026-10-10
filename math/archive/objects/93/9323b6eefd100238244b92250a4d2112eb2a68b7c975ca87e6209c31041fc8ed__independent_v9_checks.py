#!/usr/bin/env python3
"""Independent v9 checks; Python standard library only; uploaded code is never run.

Run: python independent_v9_checks.py [--source-root PATH] [--output PATH]
Without --source-root, source data are read from ../../source_archives/*v9*.zip
if present. Mathematical checks do not depend on the source being available.
"""
from __future__ import annotations
import argparse
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path
from zipfile import ZipFile


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def mobius(n):
    factors = 0
    p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            factors += 1
            if n % p == 0:
                return 0
        p += 1
    return (-1) ** (factors + (n > 1))


def phi(n):
    return sum(gcd(a, n) == 1 for a in range(n))


def character_average(n, c):
    # Divisor-sum Ramanujan formula, rather than the uploaded quotient formula.
    g = gcd(n, c)
    return F(sum(d * mobius(n // d) for d in divisors(g)), phi(n))


def covariance(n, m):
    ds = [set(range(u - m + 1, u + 1)) - {0} for u in range(m)]
    return [[sum((character_average(n, d * (j - i))
                  for d in ds[i % m] & ds[j % m]), F(0)) / n
             for j in range(n)] for i in range(n)]


def explicit_projector_covariance(n, m):
    k = n // m
    return [[F(m * (i == j) - ((i - j) % k == 0), n)
             for j in range(n)] for i in range(n)]


def valuation(d, p):
    assert d
    d = abs(d)
    v = 0
    while d % p == 0:
        d //= p
        v += 1
    return v


def shell_checks():
    records = []
    positions = 0
    for p in [x for x in range(2, 14) if prime(x)]:
        for ell in range(2, 11):
            for mu in range(1, ell // 2 + 1):
                m = p ** mu
                if m > 10000:
                    continue
                n, k = p ** ell, p ** (ell - mu)
                # Sliding interval explicitly enumerates every displacement once,
                # then checks every local coordinate without floor-count formula.
                counts = Counter(valuation(d, p) for d in range(-m + 1, 0))
                expected = {v: (p - 1) * m // p ** (v + 1) for v in range(mu)}
                for u in range(m):
                    assert counts == expected, (p, ell, mu, u, counts)
                    positions += 1
                    if u + 1 < m:
                        counts[valuation(u - m + 1, p)] -= 1
                        counts[valuation(u + 1, p)] += 1
                ranks = [(p - 1) * k // p ** (v + 1) for v in range(mu)]
                for v, count in expected.items():
                    assert F(count * p ** (v + 1), (p - 1) * n) == F(m, n)
                assert m * sum(ranks) == n - k
                assert F(m * (n - k), n) == m - 1
                records.append({'p': p, 'L': ell, 'mu': mu, 'N': n,
                                'M': m, 'rank': n - k, 'eigenvalue': str(F(m, n))})
    assert len(records) == 141
    return {'cases': len(records), 'local_positions_checked': positions, 'records': records}


def trim(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def poly_div_exact(a, b):
    a = a[:]
    q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1]
        assert b[-1] == 1
        q[i] = c
        for j, v in enumerate(b):
            a[i + j] -= c * v
    assert all(v == 0 for v in a)
    return trim(q)


PHI = {1: [-1, 1]}


def cyclotomic(n):
    if n not in PHI:
        f = [-1] + [0] * (n - 1) + [1]
        for d in divisors(n)[:-1]:
            f = poly_div_exact(f, cyclotomic(d))
        PHI[n] = f
    return PHI[n]


def reduce_poly(a, polynomial):
    a = a[:] + [0] * max(0, len(polynomial) - 1 - len(a))
    for i in range(len(a) - 1, len(polynomial) - 2, -1):
        v = a[i]
        for j, c in enumerate(polynomial):
            a[i - len(polynomial) + 1 + j] -= v * c
    return a[:len(polynomial) - 1]


def exhaustive_cyclotomic_covariance(n, m, output):
    """Direct all-state covariance from S[r,u]/S[r,t], in Q[eta]."""
    order = 2 * n
    units = [a for a in range(n) if gcd(a, n) == 1]
    accum = [[[0] * order for _ in range(n)] for _ in range(n)]
    means = [[0] * order for _ in range(n)]
    for a in units:
        for beta in range(n):
            terms = []
            for i in range(n):
                r, u = divmod(i, m)
                def phase(t):
                    return (2 * (a * t * (t - 1) // 2 + (a * m * r + beta) * t)
                            + (n % 2) * t) % order
                es = [(phase(u) - phase(t) - 2 * output * (r * m + t)) % order
                      for t in range(m) if t != u]
                terms.append(es)
                for e in es:
                    means[i][e] += 1
            for i in range(n):
                for j in range(n):
                    for ei in terms[i]:
                        for ej in terms[j]:
                            accum[i][j][(ej - ei) % order] += 1
    polynomial = cyclotomic(order)
    scale = n * n * len(units)  # Fourier normalization N, then number of states.
    q0 = covariance(n, m)
    for i in range(n):
        assert all(v == 0 for v in reduce_poly(means[i], polynomial))
        for j in range(n):
            expected = [0] * order
            coefficient = q0[i][j] * scale
            assert coefficient.denominator == 1
            expected[(2 * output * (i - j)) % order] = coefficient.numerator
            assert reduce_poly(accum[i][j], polynomial) == reduce_poly(expected, polynomial)
    return {'N': n, 'M': m, 'output': output, 'states': n * len(units),
            'matrix_entries': n * n, 'arithmetic': 'exact integer cyclotomic reduction'}


def field_root(order):
    q = order + 1
    while not prime(q):
        q += order
    for base in range(2, q):
        w = pow(base, (q - 1) // order, q)
        if all(pow(w, order // p, q) != 1 for p in divisors(order) if prime(p)):
            return q, w
    raise AssertionError('root missing')


def modular_decoder(n, m, a, beta):
    """Exact finite-field identity, unnormalized DFT (no square-root choice)."""
    k = n // m
    modulus, eta = field_root(2 * n)
    root = [pow(eta, j, modulus) for j in range(2 * n)]
    e = lambda exponent: root[exponent % (2 * n)]
    x = [(17 * i * i + 9 * i + 11) % modulus for i in range(n)]
    phases = [[2 * (a * t * (t - 1) // 2 + (a * m * r + beta) * t) + n % 2 * t
               for t in range(m)] for r in range(k)]
    d = [sum(e(phases[r][t]) * x[r * m + t] for t in range(m)) % modulus
         for r in range(k)]
    y = [e(-phases[r][t]) * d[r] % modulus for r in range(k) for t in range(m)]
    direct = [sum(y[t] * e(-2 * j * t) for t in range(n)) % modulus for j in range(n)]
    D = [sum(d[r] * e(-2 * m * j * r) for r in range(k)) % modulus for j in range(k)]
    idx = [a * j % n for j in range(n)]
    assert len(set(idx)) == n
    gauge = [e(2 * (a * j * (j - 1) // 2 + beta * j) + n % 2 * j) for j in range(n + 1)]
    assert gauge[-1] == modulus - 1
    terms = []
    for j, mm in enumerate(idx):
        boundary = e(-2 * (m * (mm + beta) + a * m * (m - 1) // 2) - n % 2 * m)
        force = (D[mm % k] - boundary * D[(mm + a * m) % k]) % modulus
        terms.append(force * pow(gauge[j], -1, modulus) % modulus)
    total = sum(terms) % modulus
    seed = total * pow(2, -1, modulus) % modulus
    prefix = 0
    got = [0] * n
    for j, mm in enumerate(idx):
        got[mm] = gauge[j] * (seed - prefix) % modulus
        prefix = (prefix + terms[j]) % modulus
    assert got == direct
    return {'N': n, 'M': m, 'a': a, 'beta': beta, 'field_modulus': modulus}


def matrix_checks():
    pairs = [(4, 1), (4, 2), (8, 2), (9, 3), (16, 2), (16, 4),
             (25, 5), (27, 3), (32, 2), (32, 4), (49, 7),
             (64, 4), (64, 8), (81, 3), (81, 9), (121, 11), (125, 5)]
    records = []
    for n, m in pairs:
        q = covariance(n, m)
        assert q == explicit_projector_covariance(n, m)
        assert sum(q[i][i] for i in range(n)) == m - 1
        # Rank/idempotence then follow exactly from groups of size M.
        records.append({'N': n, 'M': m, 'rank': n - n // m,
                        'operator_norm': str(F(m, n) if m > 1 else F(0))})
    return records


def composite_checks():
    pairs = [(12, 2), (12, 3), (18, 3), (20, 4), (30, 3), (30, 5),
             (36, 6), (42, 6), (45, 5), (60, 5), (60, 6), (72, 8)]
    records = []
    for n, m in pairs:
        q = covariance(n, m)
        assert sum(q[i][i] for i in range(n)) == m - 1
        defect = None
        for i in range(n):
            for j in range(n):
                z = sum((q[i][r] * q[r][j] for r in range(n)), F(0)) - F(m, n) * q[i][j]
                if z:
                    defect = {'i': i, 'j': j, 'Q_squared_minus_M_over_N_Q': str(z)}
                    break
            if defect:
                break
        assert defect is not None
        records.append({'N': n, 'M': m, 'trace': m - 1, 'exact_nonprojector_witness': defect})
    n, m = 12, 2
    q = covariance(n, m)
    v = [0] * n
    for r, value in enumerate([2, 1, -1, -2, -1, 1]):
        v[2 * r] = value
    assert all(sum(q[i][j] * v[j] for j in range(n)) == F(v[i], 4) for i in range(n))
    return {'cases': records, 'exact_norm_lower_bound': {
        'N': n, 'M': m, 'eigenvector': v, 'eigenvalue': '1/4',
        'M_over_N': '1/6', 'ratio': '3/2'}}


def ledger_checks():
    # Exact formulas evaluated at high precision; analytic proof is in the report.
    records = 0
    best = (Decimal(0), None)
    with localcontext() as ctx:
        ctx.prec = 55
        for L in list(range(2, 81)) + [100, 128, 256, 512, 1024, 2048]:
            for lm in sorted({1, max(1, L // 4), L // 2}):
                lk = L - lm
                for factor in [Decimal('0.01'), Decimal('0.001'), Decimal('0.000001'), Decimal('1e-12')]:
                    t = factor / L
                    c = (1 + t) ** 2 - 1
                    e = c + (1 + c) * (c + t * (2 + c))
                    aa = (1 + c) * (1 + t) ** lm - 1
                    b = (1 + e) ** lk - 1
                    h = (1 + aa) * (1 + b) * (1 + c) - 1
                    f = 2 * h + c * (1 + h) + t * (2 + c) * (1 + h)
                    q = (1 + c) * f + 2 * c
                    gamma = (1 + t) ** (2 * L) - 1
                    P = q + gamma * (2 + q)
                    bound = Decimal('1.5') * (1 + c) * (1 + t) * P + 3 * t * (1 + c) + c
                    ratio = bound / (L * t)
                    assert ratio <= 100
                    records += 1
                    if ratio > best[0]:
                        best = ratio, {'L': L, 'log2_M': lm, 'tL': str(factor)}
    return {'cases': records, 'largest_conservative_ledger_ratio': str(best[0]),
            'maximizer': best[1], 'proven_constant': 100,
            'arithmetic': '55-digit Decimal, corroborating analytic bounds'}



def sparse_edge_checks():
    # Exact integer incidence/probability checks for the added restricted corollary.
    records = []
    for n, m in [(16, 2), (16, 4), (27, 3), (64, 4), (81, 3), (81, 9),
                 (125, 5), (256, 8), (729, 9)]:
        k = n // m
        units = [a for a in range(k) if gcd(a, k) == 1]
        worst = F(0)
        for delta in range(k):
            count = sum(any((a*d-delta) % k == 0
                            for d in range(-m+1, m) if d) for a in units)
            probability = F(count, len(units))
            assert probability <= F(2*m, k)
            if delta % m == 0:
                assert probability == 0
            worst = max(worst, probability)
        records.append({'N': n, 'M': m, 'K': k,
                        'maximum_edge_probability': str(worst),
                        'bound': str(F(2*m, k)),
                        'zero_for_differences_divisible_by_M': True})
    return records


def source_data(source_root):
    names = ['RESEARCH.md', 'PROJECTOR_CERTIFICATE.md', 'COMPOSITE_MODULUS_AUDIT.md',
             'projector_certificate_results.json', 'composite_modulus_results.json',
             'native_benchmark_results.csv', 'prototype.py', 'native_benchmark.cpp']
    data = {}
    if source_root:
        for name in names:
            data[name] = (source_root / name).read_bytes()
        origin = 'directory supplied with --source-root'
    else:
        archives = sorted((Path(__file__).resolve().parents[2] / 'source_archives').glob('*v9*.zip'))
        if not archives:
            return {'status': 'not supplied; mathematical checks remain standalone'}
        with ZipFile(archives[0]) as z:
            for name in names:
                matches = [s for s in z.namelist() if s.endswith('/' + name) or s == name]
                assert len(matches) == 1, (name, matches)
                data[name] = z.read(matches[0])
        origin = 'sibling source archive ' + archives[0].name
    saved = json.loads(data['projector_certificate_results.json'])
    assert saved['cases'] == len(saved['records']) == 141
    for rec in saved['records']:
        n, m, k = rec['N'], rec['M'], rec['K']
        assert n == m * k and k >= m
        assert rec['zero_multiplicity'] == k and rec['nonzero_multiplicity'] == n - k
        assert F(rec['nonzero_eigenvalue']) == F(m, n)
        assert F(rec['trace']) == m - 1
    return {'status': 'read as inert data only', 'origin': origin,
            'sha256': {name: hashlib.sha256(blob).hexdigest() for name, blob in data.items()},
            'saved_certificate_records_consistent': len(saved['records'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('independent_v9_results.json'))
    args = parser.parse_args()
    output = {'status': 'PASS', 'uploaded_code_executed': False,
              'scope': 'exact approximation mechanism; no exact sub-N-log-N DFT conclusion'}
    output['source_data'] = source_data(args.source_root)
    output['shell_certificate'] = shell_checks()
    output['rational_covariance_checks'] = matrix_checks()
    output['all_state_cyclotomic_checks'] = [
        exhaustive_cyclotomic_covariance(n, m, out)
        for n, m, outs in [(4, 2, [0, 1]), (8, 2, [0, 1]), (9, 3, [0, 1]),
                           (12, 3, [0]), (16, 4, [0])]
        for out in outs]
    cycles = []
    for n, m in [(4, 1), (4, 2), (6, 2), (8, 2), (9, 3), (12, 3),
                 (16, 4), (25, 5), (27, 3), (35, 5), (49, 7), (64, 8), (81, 9)]:
        units = [a for a in range(n) if gcd(a, n) == 1]
        for a in sorted({units[0], units[len(units) // 2], units[-1]}):
            for beta in sorted({0, 1, n // 2, n - 1}):
                cycles.append(modular_decoder(n, m, a, beta))
    output['finite_field_decoder_checks'] = cycles
    output['composite_exact_counterexamples'] = composite_checks()
    output['precision_ledger_checks'] = ledger_checks()
    output['sparse_fourier_edge_checks'] = sparse_edge_checks()
    output['summary'] = {
        'shell_cases': output['shell_certificate']['cases'],
        'shell_local_positions': output['shell_certificate']['local_positions_checked'],
        'rational_covariance_cases': len(output['rational_covariance_checks']),
        'all_state_cyclotomic_cases': len(output['all_state_cyclotomic_checks']),
        'finite_field_decoder_cases': len(cycles),
        'composite_nonprojector_cases': len(output['composite_exact_counterexamples']['cases']),
        'precision_ledger_cases': output['precision_ledger_checks']['cases'],
        'sparse_fourier_edge_cases': len(output['sparse_fourier_edge_checks'])}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', **output['summary']}, indent=2))


if __name__ == '__main__':
    main()
