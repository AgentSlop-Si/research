"""Fresh independent controls; no author or predecessor program is imported.

Ranks are exact over Q(zeta_N), not floating-point or finite-field ranks.
Finite checks support, and do not replace, the all-length mathematical proof.
"""
import hashlib
import json
import math
import random
import time
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / 'candidate'
PREVIOUS = HERE.parent / 'dependencies' / 'previous_review'
out = {'status': 'PASS', 'independent': True, 'sympy_version': sp.__version__}
started = time.time()


def verify_manifest(directory):
    payload = json.loads((directory / 'MANIFEST.json').read_text())
    verified = []
    for item in payload['files']:
        data = (directory / item['path']).read_bytes()
        assert len(data) == item['bytes'], item
        assert hashlib.sha256(data).hexdigest() == item['sha256'], item
        verified.append(item)
    return {'manifest_sha256': hashlib.sha256((directory / 'MANIFEST.json').read_bytes()).hexdigest(),
            'verified_files': verified}


def prime_factors(n):
    return [p for p in range(2, n + 1) if n % p == 0 and sp.isprime(p)]


def dominant(n):
    pp = prime_factors(n)
    p = max(pp)
    m = n // p
    return (m, p) if m < p else None


def matrix_data(n):
    # Every algebraic root of Phi_N is primitive. Picking RootOf index 0
    # avoids approximate trigonometry and differs from the author setup.
    x = sp.Symbol('x')
    root = sp.CRootOf(sp.cyclotomic_poly(n, x), 0)
    K = sp.QQ.algebraic_field(root)
    z = K.unit
    powers = [K.one]
    for _ in range(1, n):
        powers.append(powers[-1] * z)
    assert powers[-1] * z == K.one
    assert all(powers[d] != K.one for d in range(1, n) if n % d == 0)
    return K, powers


def rank(K, powers, n, R, C):
    return DomainMatrix([[powers[(-i*j) % n] for j in C] for i in R],
                        (len(R), len(C)), K).rank()


def inspect(n, R, C, r):
    a, b = len(R), len(C)
    assert 1 <= r <= min(a, b)
    assert a*b <= n*r
    plaquette_rank_one = all((i-R[0])*(j-C[0]) % n == 0 for i in R for j in C)
    assert (r == 1) == plaquette_rank_one
    for p in prime_factors(n):
        m = n // p
        assert r >= (min(a, b)+m-1)//m
        rr, cc = (R, C) if a <= b else (C, R)
        fiber = max(([i for i in rr if i % m == u] for u in range(m)), key=len)
        reps = {}
        for j in cc:
            reps.setdefault(j % p, j)
        assert len(fiber) >= (min(a, b)+m-1)//m
        assert len(reps) >= (max(a, b)+m-1)//m
        k0 = fiber[0] % m
        assert len({(i-k0)//m for i in fiber}) == len(fiber)
        # Verify the precise column gauge and prime-root exponent identity.
        assert all((i*j-k0*j-m*((i-k0)//m)*(j % p)) % n == 0
                   for i in fiber for j in reps.values())
    domain = dominant(n)
    if domain:
        m, p = domain
        gap = n*r*(a+b)-(m+p)*a*b
        if r >= 2:
            assert gap >= min(m, p-m)*a*b
        else:
            assert gap >= 0
        if gap == 0:
            assert r == 1 and sorted((a,b)) == [m,p]
            g = math.gcd(n, *(i-R[0] for i in R))
            assert set(R) == {(R[0]+j*g) % n for j in range(n//g)}
            assert set(C) == {(C[0]+j*(n//g)) % n for j in range(g)}
    return {'a': a, 'b': b, 'rank': r}


# Final tests run only after the author freezes the artifact manifest.
out['author_manifest'] = verify_manifest(AUTHOR)
out['previous_acceptance_manifest'] = verify_manifest(PREVIOUS)
out['reviewed_report_sha256'] = hashlib.sha256((AUTHOR/'REPORT.md').read_bytes()).hexdigest()

exact = {}
for n in range(2, 8):
    K, powers = matrix_data(n)
    sets = [[i for i in range(n) if mask & (1 << i)] for mask in range(1, 1 << n)]
    counts = {'rectangles': 0, 'rank_one': 0}
    for R in sets:
        for C in sets:
            r = rank(K, powers, n, R, C)
            inspect(n, R, C, r)
            counts['rectangles'] += 1
            counts['rank_one'] += r == 1
    exact[n] = counts
    print('Exact exhaustive', n, counts, flush=True)
out['exact_cyclotomic_exhaustive'] = exact

rng = random.Random(114320261018)
sampled = {}
for n in [8, 9, 10, 12, 15, 18, 20, 21, 25, 27, 33, 35, 39, 55, 57, 77]:
    K, powers = matrix_data(n)
    samples = []
    for _ in range(12):
        R = sorted(rng.sample(range(n), rng.randint(2, min(n, 10))))
        C = sorted(rng.sample(range(n), rng.randint(2, min(n, 12))))
        samples.append(inspect(n, R, C, rank(K, powers, n, R, C)))
    # Deliberately dense subset forces a nontrivial prime-fiber bound,
    # including the repeated-prime/cofactor cases absent from the main theorem.
    R = list(range(n-1 if n <= 27 else 4))
    C = list(range(n))
    r = rank(K, powers, n, R, C)
    assert r == len(R)
    samples.append(inspect(n, R, C, r))
    sampled[n] = samples
    print('Exact samples', n, flush=True)
out['exact_cyclotomic_samples'] = sampled

K, powers = matrix_data(57)
examples = [
    ([0,3,6,9,12,15,18,21,24,27], [0,19,38,1,20,39,2,21,40,3,22], 4),
    ([0,19,38,1,20,39], list(range(0,57,3)), 2),
]
out['N57_examples'] = []
for R, C, expected in examples:
    r = rank(K, powers, 57, R, C)
    assert r == expected
    rec = inspect(57, R, C, r)
    rec.update(rows=R, columns=C, cost=r*(len(R)+len(C)), area=len(R)*len(C))
    out['N57_examples'].append(rec)

scalar_count = rank_one_count = 0
scalar_lengths = []
for n in range(2, 301):
    domain = dominant(n)
    if not domain:
        continue
    m, p = domain
    scalar_lengths.append(n)
    divisors = [d for d in range(1, n+1) if n % d == 0]
    assert [d for d in divisors if d+n//d == min(e+n//e for e in divisors)] == [m,p]
    for a in range(1, n+1):
        for b in range(a, n+1):
            r = max(2, (a+m-1)//m, (a*b+n-1)//n)
            if r <= a:
                assert n*r*(a+b) >= (m+p+min(m,p-m))*a*b
                scalar_count += 1
            if a <= m and a*b <= n:
                gap = n*(a+b)-(m+p)*a*b
                assert gap >= 0
                assert (gap == 0) == ((a,b) == (m,p))
                rank_one_count += 1
out['scalar_shapes'] = {'maximum_N': 300, 'lengths': len(scalar_lengths),
                        'higher_rank_shapes': scalar_count, 'rank_one_shapes': rank_one_count}
print('Scalar shapes', out['scalar_shapes'], flush=True)

newly_covered = []
uncovered = []
for n in range(2, 1001):
    D = min(d+n//d for d in range(1,n+1) if n % d == 0)
    old = (D*D < 8*n or sp.isprime(n) or (n % 2 == 0 and sp.isprime(n//2)))
    new = dominant(n) is not None
    if new and not old:
        newly_covered.append(n)
    if not (old or new):
        uncovered.append(n)
assert len(newly_covered) == 238
assert uncovered == [343, 847]
assert 343*56 == 19208 and 56*56 > 8*343
out['domain_census'] = {'maximum_N': 1000, 'newly_covered_count': len(newly_covered),
                        'newly_covered': newly_covered, 'remaining': uncovered}

tiles = tilings = sharp_rectangles = 0
for n in range(2, 151):
    domain = dominant(n)
    if not domain:
        continue
    m, p = domain
    rows = [[i for i in range(n) if i % p == u] for u in range(p)]
    cols = [[j for j in range(n) if j % m == v] for v in range(m)]
    covered = set()
    cost = 0
    for R in rows:
        for C in cols:
            cells = {(i,j) for i in R for j in C}
            assert not covered.intersection(cells)
            covered.update(cells)
            inspect(n, R, C, 1)
            cost += len(R)+len(C)
            tiles += 1
    assert len(covered) == n*n and cost == n*(m+p)
    tilings += 1
    if p >= 2*m and n <= 100:
        K, powers = matrix_data(n)
        R, C = rows[0]+rows[1], cols[0]
        r = rank(K, powers, n, R, C)
        assert r == 2
        assert n*r*(len(R)+len(C))-(m+p)*len(R)*len(C) == m*len(R)*len(C)
        sharp_rectangles += 1
out['attainment'] = {'maximum_N': 150, 'tilings': tilings, 'tiles': tiles,
                     'exact_sharp_gap_rectangles_through_N100': sharp_rectangles}

# Check that the author freeze has not changed during the run.
assert verify_manifest(AUTHOR) == out['author_manifest']
out['elapsed_seconds'] = round(time.time()-started, 3)
(HERE/'RESULTS.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({'status':'PASS', 'seconds':out['elapsed_seconds'],
                  'exact_exhaustive':sum(v['rectangles'] for v in exact.values()),
                  'exact_samples':sum(len(v) for v in sampled.values()),
                  'new_lengths':len(newly_covered), 'remaining':uncovered,
                  'tilings':tilings, 'sharp_rectangles':sharp_rectangles}), flush=True)
