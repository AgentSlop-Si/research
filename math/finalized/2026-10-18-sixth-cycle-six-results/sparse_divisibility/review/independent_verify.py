#!/usr/bin/env python3
"""Independent review checks. Standard library only; no packet code imported.

Base-field representation: a+b*sqrt(2)+i*(c+d*sqrt(2)), four rationals.
Family checks: direct exponent histograms reduced modulo independently
constructed cyclotomic polynomials, without relying on the CRT Gram claim.
"""
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = (HERE.parent / 'candidate')
EXPECTED_REPORT = '93be9a7c2c62b7a8c9ba6ff0cfce160b3c0469b03d0373f53fbcbad9e86f5cde'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

assert sha(SOURCE / 'REPORT.md') == EXPECTED_REPORT
manifest = json.loads((SOURCE / 'MANIFEST.json').read_text())
for item in manifest['files']:
    p = SOURCE / item['path']
    assert p.stat().st_size == item['bytes'] and sha(p) == item['sha256'], item
bindings = json.loads((SOURCE / 'SOURCE_BINDINGS.json').read_text())
for item in bindings:
    assert sha(SOURCE / item['copy']) == item['sha256']
    assert sha((SOURCE / item['public_source_path'])) == item['sha256']
for name in ('verify_exact.py', 'RESULTS.json', 'GRAM_CERTIFICATE.json'):
    assert sha(SOURCE / name) == sha(HERE / 'replay' / name), name

# Literal transcription independently specified from REPORT.md, not its checker.
R = [[int(v) for v in row] for row in (
    '00110011', '01010101', '11001100', '10101010',
    '00110011', '10101010', '11001100', '01010101')]
assert json.loads((SOURCE / 'connected_mask.json').read_text())['R'] == R
assert json.loads((SOURCE / 'RESULTS.json').read_text())['binary_mask'] == R

# Exact arithmetic through the quadratic tower Q(sqrt(2))[i].
ZERO = tuple(F(0) for _ in range(4))
ONE = (F(1), F(0), F(0), F(0))
def scal(n):
    return (F(n), F(0), F(0), F(0))
def plus(x, y):
    return tuple(a+b for a, b in zip(x, y))
def minus(x, y):
    return tuple(a-b for a, b in zip(x, y))
def qmul(x, y):
    a, b = x
    c, d = y
    return (a*c+2*b*d, a*d+b*c)
def qadd(x, y):
    return (x[0]+y[0], x[1]+y[1])
def qsub(x, y):
    return (x[0]-y[0], x[1]-y[1])
def product(x, y):
    re = qsub(qmul(x[:2], y[:2]), qmul(x[2:], y[2:]))
    im = qadd(qmul(x[:2], y[2:]), qmul(x[2:], y[:2]))
    return re + im
def reciprocal(x):
    assert x != ZERO
    den = qadd(qmul(x[:2], x[:2]), qmul(x[2:], x[2:]))
    a, b = den
    norm = a*a-2*b*b
    assert norm != 0
    invden = (a/norm, -b/norm)
    re = qmul(x[:2], invden)
    im = qmul((-x[2], -x[3]), invden)
    result = re + im
    assert product(x, result) == ONE
    return result
def conjugate(x):
    return x[:2] + (-x[2], -x[3])
z = (F(0), F(1, 2), F(0), F(-1, 2))
roots = [ONE]
for _ in range(7):
    roots.append(product(roots[-1], z))
assert product(roots[-1], z) == ONE and roots[4] == scal(-1)
def ident(n, scalar=1):
    return [[scal(scalar if i == j else 0) for j in range(n)] for i in range(n)]
def matrix_sum(A, B, sign=1):
    return [[plus(x, y) if sign == 1 else minus(x, y) for x, y in zip(a, b)] for a, b in zip(A, B)]
def multiply(A, B):
    out = []
    for a in A:
        row = []
        for b in zip(*B):
            entry = ZERO
            for x, y in zip(a, b):
                entry = plus(entry, product(x, y))
            row.append(entry)
        out.append(row)
    return out
def adjoint(A):
    return [[conjugate(x) for x in col] for col in zip(*A)]
def invert(A):
    n = len(A)
    aug = [row[:] + eye for row, eye in zip(A, ident(n))]
    for j in range(n):
        pivot = next(k for k in range(j, n) if aug[k][j] != ZERO)
        aug[j], aug[pivot] = aug[pivot], aug[j]
        factor = reciprocal(aug[j][j])
        aug[j] = [product(factor, x) for x in aug[j]]
        for k in range(n):
            if k != j:
                factor = aug[k][j]
                aug[k] = [minus(x, product(factor, y)) for x, y in zip(aug[k], aug[j])]
    assert [row[:n] for row in aug] == ident(n)
    return [row[n:] for row in aug]

H = [[roots[(r*c) % 8] for c in range(8)] for r in range(8)]
D = [[H[r][c] if R[r][c] else ZERO for c in range(8)] for r in range(8)]
assert multiply(adjoint(H), H) == multiply(H, adjoint(H)) == ident(8, 8)
assert multiply(adjoint(D), D) == multiply(D, adjoint(D)) == ident(8, 4)
A = matrix_sum(H, D, -1)
B = [[product(scal(F(1, 4)), x) for x in row] for row in adjoint(A)]
M = invert(B)
assert multiply(M, B) == multiply(B, M) == ident(8)
assert all(sum(x != ZERO for x in row) == 4 for row in B)
assert all(sum(x != ZERO for x in col) == 4 for col in zip(*B))
E = matrix_sum(M, H, -1)
assert multiply(adjoint(E), E) == multiply(E, adjoint(E)) == ident(8, 4)

# A different degree-preserving negative control from the original checker.
bad = [row[:] for row in R]
for r, c in ((0, 1), (0, 2), (1, 1), (1, 2)):
    bad[r][c] = 1-bad[r][c]
assert all(sum(row) == 4 for row in bad)
assert all(sum(col) == 4 for col in zip(*bad))
badD = [[H[r][c] if bad[r][c] else ZERO for c in range(8)] for r in range(8)]
assert multiply(adjoint(badD), badD) != ident(8, 4)

# Integer-polynomial arithmetic, low-degree coefficient first.
def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p
def divmod_poly(a, b):
    a, b = trim(a), trim(b)
    assert b[-1] == 1
    q = [0] * max(1, len(a)-len(b)+1)
    while len(a) >= len(b) and a != [0]:
        k, c = len(a)-len(b), a[-1]
        q[k] = c
        for j, v in enumerate(b):
            a[k+j] -= c*v
        a = trim(a)
    return trim(q), a
@lru_cache(None)
def cyclotomic(n):
    p = [-1] + [0]*(n-1) + [1]
    for d in range(1, n):
        if n % d == 0:
            p, rem = divmod_poly(p, cyclotomic(d))
            assert rem == [0]
    return tuple(p)
assert cyclotomic(8) == (1, 0, 0, 0, 1)

def connected(mask):
    n = len(mask)
    adjacency = [set() for _ in range(2*n)]
    for r in range(n):
        for c in range(n):
            if mask[r][c]:
                adjacency[r].add(n+c)
                adjacency[n+c].add(r)
    visited, frontier = set(), {0}
    while frontier:
        visited |= frontier
        frontier = set.union(*(adjacency[v] for v in frontier)) - visited
    return len(visited)

family_results = []
for m in (1, 3, 5, 7, 9, 11, 15):
    n, degree = 8*m, 4*m
    u = pow(m, -1, 8)
    mask = [[R[(u*r) % 8][c % 8] for c in range(n)] for r in range(n)]
    assert all(sum(row) == degree for row in mask)
    assert all(sum(col) == degree for col in zip(*mask))
    assert connected(mask) == 2*n
    phi = cyclotomic(n)
    for order in ('columns', 'rows'):
        for j in range(n):
            for k in range(n):
                histogram = [0]*n
                for t in range(n):
                    if order == 'columns':
                        present = mask[t][j] and mask[t][k]
                        exponent = t*(k-j)
                    else:
                        present = mask[j][t] and mask[k][t]
                        exponent = t*(j-k)
                    if present:
                        histogram[exponent % n] += 1
                remainder = divmod_poly(histogram, phi)[1]
                assert remainder == [degree if j == k else 0], (m, order, j, k, remainder)
    if m > 1:
        v = pow(8, -1, m)
        for r in range(n):
            for c in range(n):
                assert (r*c-m*u*(r % 8)*(c % 8)-8*v*(r % m)*(c % m)) % n == 0
    family_results.append({'m': m, 'N': n, 'd': degree, 'gram_entries': 2*n*n, 'connected_vertices': 2*n, 'cyclotomic_coefficients': phi, 'status': 'PASS'})

# The two time-limit records are checked as nonterminal, never infeasibility.
for name in ('search_12_5.json', 'search_strong_12_5.json'):
    log = json.loads((SOURCE / name).read_text())
    assert log['N'] == 12 and log['d'] == 5 and log['status'] == 1
    assert 'Time limit reached' in log['message']

result = {
    'status': 'PASS',
    'report_sha256': EXPECTED_REPORT,
    'packet_manifest_entries_verified': len(manifest['files']),
    'copied_and_original_source_bindings_verified': len(bindings),
    'isolated_replay_outputs_byte_identical': ['RESULTS.json', 'GRAM_CERTIFICATE.json'],
    'base_field': 'Q(sqrt(2))[i], rational four-coordinate tuples',
    'base_gram_entries_checked': 128,
    'both_inverse_products': True,
    'every_inverse_row_and_column_nonzeros': 4,
    'both_unnormalized_error_grams': '4 I_8',
    'normalized_squared_spectral_error': '1/2',
    'independent_degree_preserving_negative_control_rejected': True,
    'family_direct_gram_checks': family_results,
    'family_total_direct_gram_entries': sum(x['gram_entries'] for x in family_results),
    'family_all_odd_m_proof': 'Separately reviewed exact CRT tensor argument; finite checks are controls only',
    'uniform_divisibility_status': 'UNRESOLVED',
    'nondivisor_counterexample_found_or_claimed': False,
    'search_timeouts_have_no_existence_or_nonexistence_consequence': True,
    'historical_programs_executed': False,
    'external_writes': False
}
(HERE / 'INDEPENDENT_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
witness = {'basis': ['1', 'sqrt(2)', 'i', 'i*sqrt(2)'], 'M_tilde': M, 'B_tilde': B, 'error_M_tilde_minus_H': E}
(HERE / 'INDEPENDENT_WITNESS.json').write_text(json.dumps(witness, default=str, indent=2)+'\n')
print(json.dumps({'status': 'PASS', 'independent_family_gram_entries': result['family_total_direct_gram_entries'], 'manifest_entries': len(manifest['files'])}))
