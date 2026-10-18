"""Fresh exact controls for the dominant-prime Fourier rectangle theorem.

No previous source or review checker is imported or executed. Exact cyclotomic
rank tests are characteristic zero; finite controls supplement the proof.
"""
import hashlib
import json
import math
import random
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / 'dependencies' / 'previous_candidate'
REVIEW = HERE.parent / 'dependencies' / 'previous_review'
OUT = {'status': 'PASS', 'sympy_version': sp.__version__,
       'independence': 'Fresh extension checker; no previous checker imported or executed.'}


def factor_pair(n):
    d = max(k for k in range(1, math.isqrt(n)+1) if n % k == 0)
    return d, n//d


def dominant_pair(n):
    p = max(sp.factorint(n))
    m = n//p
    return (m, p) if m < p else None


scalar_counts = {'maximum_N': 400, 'lengths': 0, 'shapes': 0,
                 'rank_at_least_two_shapes': 0, 'rank_one_equalities': 0}
for n in range(2, scalar_counts['maximum_N']+1):
    pair = dominant_pair(n)
    if pair is None:
        continue
    m, p = pair
    assert factor_pair(n) == pair
    scalar_counts['lengths'] += 1
    delta_numerator = min(m, p-m)  # delta = delta_numerator / N
    equalities = []
    for a in range(1, n+1):
        for b in range(a, n+1):
            rmin = max(1, (a+m-1)//m, (a*b+n-1)//n)
            assert rmin <= a
            gap = n*rmin*(a+b) - (m+p)*a*b
            assert gap >= 0
            if gap == 0:
                assert (a, b, rmin) == (m, p, 1)
                equalities.append((a, b, rmin))
                scalar_counts['rank_one_equalities'] += 1
            rhigh = max(2, rmin)
            if rhigh <= a:
                high_gap = n*rhigh*(a+b) - (m+p)*a*b
                assert high_gap >= delta_numerator*a*b > 0
                if m*rhigh <= p:
                    assert high_gap >= m*(rhigh-1)*a*b
                else:
                    assert high_gap >= (p-m)*a*b
                scalar_counts['rank_at_least_two_shapes'] += 1
            scalar_counts['shapes'] += 1
    assert equalities == [(m, p, 1)]
OUT['scalar_shape_controls'] = scalar_counts
print('scalar controls', scalar_counts, flush=True)


class CyclotomicFourier:
    def __init__(self, n):
        self.n = n
        self.K = sp.QQ.cyclotomic_field(n)
        z = self.K.from_sympy(self.K.ext)
        self.powers = [self.K.one]
        for _ in range(1, n):
            self.powers.append(self.powers[-1]*z)
        assert self.powers[-1]*z == self.K.one
        assert all(self.powers[n//q] != self.K.one for q in sp.factorint(n))

    def rank(self, R, C):
        matrix = [[self.powers[(-i*j) % self.n] for j in C] for i in R]
        return int(DomainMatrix(matrix, (len(R), len(C)), self.K).rank())


def check_actual(F, R, C, expected_rank=None):
    n = F.n
    r = F.rank(R, C)
    if expected_rank is not None:
        assert r == expected_rank
    a, b = sorted([len(R), len(C)])
    assert 1 <= r <= a and a*b <= n*r
    for p in sp.factorint(n):
        m = n//p
        assert r >= (a+m-1)//m
    plaquette = all((i-R[0])*(j-C[0]) % n == 0 for i in R for j in C)
    assert (r == 1) == plaquette
    pair = dominant_pair(n)
    density_gap = None
    if pair:
        m, p = pair
        density_gap = n*r*(a+b) - (m+p)*a*b
        assert density_gap >= 0
        if r >= 2:
            assert density_gap >= min(m, p-m)*a*b > 0
        if density_gap == 0:
            assert (a, b, r) == (m, p, 1)
            g = math.gcd(n, *(i-R[0] for i in R))
            H_coset = {(R[0]+k*g) % n for k in range(n//g)}
            annihilator_coset = {(C[0]+k*(n//g)) % n for k in range(g)}
            assert set(R) == H_coset and set(C) == annihilator_coset
    return {'rows': R, 'columns': C, 'rank': r,
            'shape': [len(R), len(C)], 'density_gap_numerator': density_gap}


# Independent exhaustive small controls include both nontrivial prime fibers
# and characteristic-zero nonvanishing minors.
exhaustive = {}
for n in [2, 3, 5, 6]:
    F = CyclotomicFourier(n)
    subsets = [[j for j in range(n) if mask & (1 << j)] for mask in range(1, 1 << n)]
    count = 0
    for R in subsets:
        for C in subsets:
            check_actual(F, R, C)
            count += 1
    exhaustive[n] = count
    print('exact exhaustive', n, count, flush=True)
OUT['exact_cyclotomic_exhaustive'] = exhaustive

rng = random.Random(202610181140)
samples = {}
for n in [9, 15, 21, 27, 35, 49, 57, 69, 116]:
    F = CyclotomicFourier(n)
    tests = []
    for _ in range(5):
        a, b = rng.randint(2, min(6, n)), rng.randint(2, min(8, n))
        R = sorted(rng.sample(range(n), a))
        C = sorted(rng.sample(range(n), b))
        tests.append(check_actual(F, R, C))
    pair = dominant_pair(n)
    if pair:
        m, p = pair
        # Full coset equality and sharp r=2 local gap, when 2m<=p.
        tests.append(check_actual(F, list(range(0, n, p)), list(range(0, n, m)), 1))
        if 2*m <= p:
            R = [u+k*p for u in range(2) for k in range(m)]
            C = list(range(0, n, m))
            result = check_actual(F, R, C, 2)
            assert result['density_gap_numerator'] == m*len(R)*len(C)
            tests.append(result)
    samples[n] = tests
    print('exact samples', n, len(tests), flush=True)
OUT['exact_cyclotomic_samples'] = samples

F57 = CyclotomicFourier(57)
R = list(range(0, 30, 3))
C = [0, 19, 38, 1, 20, 39, 2, 21, 40, 3, 22]
former_shape = check_actual(F57, R, C, 4)
assert 2 < (10+2)//3 == 4
former_shape['universal_rank_lower_bound_for_shape'] = 4
former_shape['old_rank_two_relaxation_is_not_a_fourier_rectangle'] = True
OUT['N57_actual_ten_by_eleven'] = former_shape

# A deliberate field-boundary control, independently recomputed here.
R, C = [0, 1, 3], [0, 2, 7]
q, z = 23, 2
assert pow(z, 11, q) == 1 and z != 1
Kq = sp.GF(q)
matrix = [[Kq(pow(z, (-i*j) % 11, q)) for j in C] for i in R]
finite_rank = int(DomainMatrix(matrix, (3, 3), Kq).rank())
complex_rank = CyclotomicFourier(11).rank(R, C)
assert (finite_rank, complex_rank) == (2, 3)
OUT['finite_field_negative_control'] = {
    'N': 11, 'field_prime': q, 'primitive_root': z, 'rows': R, 'columns': C,
    'finite_field_rank': finite_rank, 'complex_rank': complex_rank,
    'meaning': 'Do not substitute finite-field full spark for Chebotarev over C.'}

tilings = {'maximum_N': 200, 'lengths': 0, 'tiles': 0, 'entries': 0}
for n in range(2, tilings['maximum_N']+1):
    pair = dominant_pair(n)
    if pair is None:
        continue
    m, p = pair
    rows = [[i for i in range(n) if i % p == u] for u in range(p)]
    cols = [[j for j in range(n) if j % m == v] for v in range(m)]
    covered = bytearray(n*n)
    cost = 0
    for R in rows:
        for C in cols:
            assert len(R) == m and len(C) == p
            assert all((i-R[0])*(j-C[0]) % n == 0 for i in R for j in C)
            for i in R:
                for j in C:
                    pos = i*n+j
                    assert covered[pos] == 0
                    covered[pos] = 1
            tilings['tiles'] += 1
            cost += len(R)+len(C)
    assert all(covered) and cost == n*(m+p)
    tilings['lengths'] += 1
    tilings['entries'] += n*n
OUT['exact_coset_partitions'] = tilings
print('coset partitions', tilings, flush=True)

new, residual = [], []
for n in range(2, 1001):
    d, e = factor_pair(n)
    previous = ((d+e)**2 < 8*n or sp.isprime(n)
                or (n % 2 == 0 and sp.isprime(n//2)))
    if not previous:
        (new if dominant_pair(n) else residual).append(n)
assert len(new) == 238 and residual == [343, 847]
OUT['domain_census'] = {'maximum_N': 1000, 'newly_covered_count': len(new),
                        'newly_covered_lengths': new, 'outside_union': residual}
OUT['boundary_examples'] = {
    'N57': {'pair': [3, 19], 'optimum': 1254, 'higher_rank_penalty': '1/19'},
    'N343': {'pair': [7, 49], 'D': 56, 'D_squared': 3136, 'eight_N': 2744,
             'upper_bound': 19208, 'lower_bound': '686 sqrt(686)',
             'status': 'Outside both established domains; general optimum not settled.'},
    'N847': {'pair': [11, 77], 'D': 88, 'D_squared': 7744, 'eight_N': 6776,
             'status': 'Outside both established domains; general optimum not settled.'}}

source_paths = {
    'accepted_candidate': PREVIOUS/'REPORT.md',
    'independent_acceptance': REVIEW/'REVIEW.md',
    'phase7_source': PREVIOUS/'SOURCE_PHASE7_AUDIT.md'}
hashes = {}
for label, path in source_paths.items():
    data = path.read_bytes()
    hashes[label] = {'path': str(path), 'bytes': len(data),
                     'sha256': hashlib.sha256(data).hexdigest()}
assert hashes['accepted_candidate']['sha256'] == '9a1100fe1b98f187aa27f9377f665f31a4b673f1278cc7579ed6fdba9e4624aa'
assert hashes['phase7_source']['sha256'] == 'ed3a259cc88ecb2cf12092f612aabaeb917885fe84147cf2feb99802d1fd32c4'
OUT['source_hashes'] = hashes
(HERE/'RESULTS.json').write_text(json.dumps(OUT, indent=2)+'\n')
sources = json.loads((PREVIOUS/'SOURCES.json').read_text())
sources['scope'] = 'Dominant-prime extension N=mp, p prime, m<p; no external writes.'
sources['accepted_local_dependencies'] = hashes
sources['prime_minor_primary_source']['read_utc'] = '2026-10-18T11:41:04Z'
sources['prime_minor_primary_source']['role'] = ('Prime-length complex Fourier full-spark input for the general '
                                               'prime-fiber rank lemma and dominant-prime extension; no novelty claim')
(HERE/'SOURCES.json').write_text(json.dumps(sources, indent=2)+'\n')
manifest = {'files': []}
for path in sorted(HERE.iterdir()):
    if path.is_file() and path.name not in ['MANIFEST.json', 'controls.stdout.txt']:
        data = path.read_bytes()
        manifest['files'].append({'path': path.name, 'bytes': len(data),
                                  'sha256': hashlib.sha256(data).hexdigest()})
(HERE/'MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(json.dumps({'status': 'PASS', 'scalar_controls': scalar_counts,
                  'exhaustive_actual_rectangles': sum(exhaustive.values()),
                  'additional_actual_rectangles': sum(map(len, samples.values()))+1,
                  'newly_covered_through_1000': len(new), 'residual': residual}), flush=True)
