"""Independent checks; does not import or execute the author/source checker.

Exact ranks use Q(zeta_N), not floating singular values or finite fields.
Finite controls supplement the proof; they are not a theorem over all N.
"""
import hashlib
import json
import math
import random
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'candidate'
out = {'status': 'PASS', 'independence': 'New code, no source checker imported or executed',
       'sympy_version': sp.__version__}

def divisors(n):
    return [d for d in range(1,n+1) if n % d == 0]

def optimum_pair(n):
    d = max(d for d in divisors(n) if d*d <= n)
    return d, n//d

def exact_matrix(n):
    K = sp.QQ.algebraic_field(sp.exp(2*sp.pi*sp.I/n))
    z = K.from_sympy(sp.exp(2*sp.pi*sp.I/n))
    powers = [K.one]
    for j in range(1,n):
        powers.append(powers[-1]*z)
    assert powers[-1]*z == K.one
    assert all(powers[d] != K.one for d in divisors(n) if d < n)
    return K, [[powers[(-j*k)%n] for j in range(n)] for k in range(n)]

def rectangle_rank(K,F,R,C):
    return DomainMatrix([[F[i][j] for j in C] for i in R],(len(R),len(C)),K).rank()

def check_rectangle(n,R,C,r):
    a,b = len(R),len(C)
    d,e = optimum_pair(n)
    D = d+e
    assert 1 <= r <= min(a,b)
    assert a*b <= n*r
    plaquettes = all(((i-R[0])*(j-C[0])) % n == 0 for i in R for j in C)
    assert (r == 1) == plaquettes
    if D*D < 8*n or (n%2 == 0 and sp.isprime(n//2)):
        gap = n*r*(a+b) - D*a*b
        assert gap >= 0
        if r >= 2:
            assert gap > 0
        if gap == 0:
            assert r == 1 and a*b == n and a+b == D
            g = math.gcd(n,*(i-R[0] for i in R))
            H = {(R[0]+j*g)%n for j in range(n//g)}
            A = {(C[0]+j*(n//g))%n for j in range(g)}
            assert set(R) == H and set(C) == A
    if n%2 == 0 and sp.isprime(n//2) and n//2 != 2:
        assert r >= (min(a,b)+1)//2

exhaustive = {}
for n in range(2,7):
    K,F = exact_matrix(n)
    sets = [[j for j in range(n) if mask>>j & 1] for mask in range(1,1<<n)]
    counts = {'rectangles': 0, 'rank_one': 0, 'local_equalities': 0}
    d,e = optimum_pair(n)
    for R in sets:
        for C in sets:
            r = rectangle_rank(K,F,R,C)
            check_rectangle(n,R,C,r)
            counts['rectangles'] += 1
            counts['rank_one'] += (r == 1)
            counts['local_equalities'] += (n*r*(len(R)+len(C)) == (d+e)*len(R)*len(C))
    exhaustive[n] = counts
    print('exact exhaustive',n,counts,flush=True)
out['exact_cyclotomic_exhaustive'] = exhaustive

rng = random.Random(202610181053)
samples = {}
for n in [8,10,12,14,18,22,26,30,34]:
    K,F = exact_matrix(n)
    tested = []
    for _ in range(8):
        a = rng.randrange(2,min(6,n)+1)
        b = rng.randrange(2,min(8,n)+1)
        R,C = sorted(rng.sample(range(n),a)), sorted(rng.sample(range(n),b))
        r = rectangle_rank(K,F,R,C)
        check_rectangle(n,R,C,r)
        tested.append({'a':a,'b':b,'rank':r})
    # The twice-prime scalar equality escape is actually full row rank.
    R,C = list(range(4)), list(range(n))
    r = rectangle_rank(K,F,R,C)
    assert r == 4
    check_rectangle(n,R,C,r)
    samples[n] = {'sampled':tested,'full_column_candidate_rank':r}
    print('exact samples',n,flush=True)
out['exact_cyclotomic_samples'] = samples

balanced_count = 0
balanced_N = []
for n in range(2,301):
    d,e = optimum_pair(n)
    D = d+e
    if D*D >= 8*n:
        continue
    balanced_N.append(n)
    for a in range(2,n+1):
        for b in range(a,n+1):
            r = max(2,(a*b+n-1)//n)
            if r <= a:
                assert n*r*(a+b) > D*a*b
                balanced_count += 1
out['balanced_scalar_shapes'] = {'maximum_N':300,'lengths':len(balanced_N),'shapes':balanced_count}

twice_count = 0
excluded = []
for p in list(sp.primerange(3,258)):
    n = 2*p
    for a in range(2,n+1):
        for b in range(a,n+1):
            r = max(2,(a+1)//2)
            gap = n*r*(a+b) - (p+2)*a*b
            assert gap >= 0
            if gap == 0:
                assert (a,b,r) == (4,n,2)
                excluded.append([p,a,b,r])
            twice_count += 1
out['twice_prime_scalar_shapes'] = {'prime_limit':257,'shapes':twice_count,'only_excluded_equality_candidates':excluded}

tiling_count = tile_count = 0
for n in range(2,101):
    d,e = optimum_pair(n)
    for d in divisors(n):
        e = n//d
        # Independent representation by residue classes, rather than source loops.
        row_classes = [[x for x in range(n) if x % e == u] for u in range(e)]
        col_classes = [[x for x in range(n) if x % d == v] for v in range(d)]
        covered = set()
        cost = 0
        for R in row_classes:
            for C in col_classes:
                assert all((i-R[0])*(j-C[0])%n == 0 for i in R for j in C)
                entries = {(i,j) for i in R for j in C}
                assert not covered.intersection(entries)
                covered |= entries
                cost += len(R)+len(C)
                tile_count += 1
        assert len(covered) == n*n
        assert cost == n*(d+e)
        tiling_count += 1
out['coset_tilings'] = {'maximum_N':100,'tilings':tiling_count,'tiles':tile_count}

assert 10*11 <= 57*2 and 57*2*(10+11) < 22*10*11
out['relaxed_counterexample'] = {'N':57,'a':10,'b':11,'r':2,'stable_rank_slack':4,'density_gap_numerator':-26,
    'meaning':'Only a relaxed-premise counterexample; no actual Fourier rectangle supplied'}
# Deliberate field-boundary control: full spark fails over a splitting finite field.
p,q,z = 11,23,2
R,C = [0,1,3],[0,2,7]
assert pow(z,p,q) == 1 and z != 1
M = [[pow(z,(-i*j)%p,q) for j in C] for i in R]
finite_rank = DomainMatrix([[sp.GF(q)(x) for x in row] for row in M],(3,3),sp.GF(q)).rank()
K,F = exact_matrix(p)
complex_rank = rectangle_rank(K,F,R,C)
assert (finite_rank,complex_rank) == (2,3)
out['finite_field_negative_control'] = {'N':p,'field_prime':q,'primitive_root':z,'rows':R,'columns':C,
    'matrix_mod_q':M,'finite_field_rank':finite_rank,'characteristic_zero_rank':complex_rank,
    'meaning':'Characteristic-zero Chebotarev cannot be replaced by finite-field full spark'}
out['candidate_manifest_verified'] = []
for item in json.loads((SOURCE/'MANIFEST.json').read_text())['files']:
    data = (SOURCE/item['path']).read_bytes()
    assert len(data) == item['bytes']
    assert hashlib.sha256(data).hexdigest() == item['sha256']
    out['candidate_manifest_verified'].append(item['path'])
fresh = (HERE/'PHASE7_FRESH.md').read_bytes()
assert fresh == (SOURCE/'SOURCE_PHASE7_AUDIT.md').read_bytes()
out['source_hashes'] = {'sha256':hashlib.sha256(fresh).hexdigest(),
    'git_blob':hashlib.sha1(b'blob '+str(len(fresh)).encode()+b'\0'+fresh).hexdigest()}
assert out['source_hashes']['git_blob'] == '58be131bc82c3ccc7dfb15b435d01bd9edd17942'
(HERE/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','balanced':out['balanced_scalar_shapes'],'twice_prime_shapes':twice_count,
    'exact_exhaustive_rectangles':sum(x['rectangles'] for x in exhaustive.values()),
    'tilings':tiling_count,'tiles':tile_count}),flush=True)
