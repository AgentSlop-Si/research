#!/usr/bin/env python3
"""Independent Phase 6 algebra/recognition checks. No source imports or execution.

This reference deliberately uses direct small DFTs, not the uploaded NTT,
and does not benchmark the claimed fast implementation.
"""
from pathlib import Path
import hashlib
import itertools
import json
import math
import random
import zipfile
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'extracted' / 'fft_hero0_phase6_sparse_phase_support_2026-10-10'
RNG = random.Random(62151009)


def factors(n):
    out = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def prime(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n)+1))


def field(q):
    p = q+1
    while not prime(p):
        p += q
    for w in range(2, p):
        if pow(w, q, p) == 1 and all(pow(w, q//d, p) != 1 for d in factors(q)):
            return p, w
    raise AssertionError('No primitive root found')


def transform(v, w, p):
    n = len(v)
    table = [pow(w, i, p) for i in range(n)]
    return [sum(v[t]*table[(t*r) % n] for t in range(n)) % p for r in range(n)]


def chirp(q, m, a, beta, p, w):
    return [[pow(w, (a*t*(t-1)//2 + (a*m*b+beta)*t) % q, p)
             for t in range(m)] for b in range(q//m)]


def analysis(x, m, a, beta, p, w):
    q = len(x)
    s = chirp(q, m, a, beta, p, w)
    return [transform([s[b][t]*x[b*m+t] % p for t in range(m)], pow(w, q//m, p), p)
            for b in range(q//m)]


def synthesis(ds, m, a, beta, p, w):
    q = len(ds)*m
    s = chirp(q, m, a, beta, p, w)
    im = pow(m, -1, p)
    out = []
    for b, d in enumerate(ds):
        v = transform(d, pow(w, -(q//m), p), p)
        out.extend(v[t]*im*pow(s[b][t], -1, p) % p for t in range(m))
    return out


def recognize(x, m, a, beta, cap, p, w):
    """Derive selected modes, certify full block, discover only upon failure."""
    q = len(x)
    s = chirp(q, m, a, beta, p, w)
    active = set()
    stored = []
    discovery = 0
    for b in range(q//m):
        v = [s[b][t]*x[b*m+t] % p for t in range(m)]
        d = {r: sum(v[t]*pow(w, (q//m)*r*t, p) for t in range(m)) % p for r in active}
        recon = [sum(d[r]*pow(w, -(q//m)*r*t, p) for r in active)*pow(m, -1, p) % p
                 for t in range(m)]
        if recon != v:
            discovery += 1
            full = transform(v, pow(w, q//m, p), p)
            nonzero = {r for r, value in enumerate(full) if value}
            assert nonzero-active
            active |= nonzero
            if len(active) > cap:
                assert discovery <= cap+1
                return None, sorted(active), discovery
            d = {r: full[r] for r in active}
        stored.append(d)
    assert discovery <= len(active)
    return [[row.get(r, 0) for r in range(m)] for row in stored], sorted(active), discovery


def green_row(d, q, m, a, beta, p, w):
    """Solve y[k]-w^(-k-beta)y[k+a]=forcing[k] around one cycle."""
    k = q//m
    bhat = transform(d, pow(w, -m, p), p)
    forcing = [(bhat[j % k] - pow(w, -(m*(j+beta)+a*m*(m-1)//2), p)
               *bhat[(j+a*m) % k]) % p for j in range(q)]
    order = [(a*j) % q for j in range(q)]
    gauges = [pow(w, a*j*(j-1)//2+beta*j, p) for j in range(q+1)]
    assert gauges[-1] == p-1
    increments = [forcing[order[j]]*pow(gauges[j], -1, p) % p for j in range(q)]
    initial = sum(increments)*pow(2, -1, p) % p
    value = initial
    y = [0]*q
    for j in range(q):
        y[order[j]] = gauges[j]*value % p
        value = (value-increments[j]) % p
    assert gauges[-1]*value % p == initial
    assert all((y[j]-pow(w, -j-beta, p)*y[(j+a) % q]-forcing[j]) % p == 0 for j in range(q))
    return y


def decode(ds, m, a, beta, p, w):
    q = len(ds)*m
    y = [0]*q
    for r in range(m):
        d = [row[r] for row in ds]
        if any(d):
            z = green_row(d, q, m, a, (beta+r*(q//m)) % q, p, w)
            y = [(u+v) % p for u, v in zip(y, z)]
    return [v*pow(m, -1, p) % p for v in y]


def det_mod(mat, p):
    arr = [row[:] for row in mat]
    result = 1
    for j in range(len(arr)):
        pivot = next((i for i in range(j, len(arr)) if arr[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            arr[j], arr[pivot] = arr[pivot], arr[j]
            result = -result
        value = arr[j][j]
        result = result*value % p
        for i in range(j+1, len(arr)):
            mult = arr[i][j]*pow(value, -1, p) % p
            for k in range(j, len(arr)):
                arr[i][k] = (arr[i][k]-mult*arr[j][k]) % p
    return result % p


def check_case(x, m, a, beta, cap, p, w):
    oracle = analysis(x, m, a, beta, p, w)
    support = [r for r in range(m) if any(row[r] for row in oracle)]
    ds, found, discoveries = recognize(x, m, a, beta, cap, p, w)
    assert (ds is not None) == (len(support) <= cap)
    if ds is not None:
        assert ds == oracle and found == support
        assert synthesis(ds, m, a, beta, p, w) == x
        y = decode(ds, m, a, beta, p, w)
        assert y == transform(x, pow(w, -1, p), p)
        return True, len(x), discoveries
    return False, 0, discoveries


def main():
    out = {}
    source_manifest = json.loads((SOURCE/'SHA256SUMS.json').read_text())
    for name, item in source_manifest.items():
        data = (SOURCE/name).read_bytes()
        assert len(data) == item['bytes'] and hashlib.sha256(data).hexdigest() == item['sha256']
    prior = SOURCE/'prior_phase5_bundle.zip'
    assert hashlib.sha256(prior.read_bytes()).hexdigest() == '25e1d0329da56504d8e3ff855ce11a63c2dcef0a41e69a6879f7e17a06130878'
    with zipfile.ZipFile(prior) as z:
        out['prior_phase5_members'] = len(z.infolist())
    out['source_manifest_entries_verified'] = len(source_manifest)

    exhaustive = {'cases': 0, 'accepted': 0, 'rejected': 0, 'exact_output_entries': 0}
    for x in itertools.product(range(5), repeat=4):
        for a, beta, cap in itertools.product([1, 3], range(4), range(3)):
            accepted, entries, _ = check_case(list(x), 2, a, beta, cap, 5, 2)
            exhaustive['cases'] += 1
            exhaustive['accepted' if accepted else 'rejected'] += 1
            exhaustive['exact_output_entries'] += entries
    out['exhaustive_F5_Q4'] = exhaustive

    shapes = [(8,2),(12,3),(18,3),(24,4),(30,5),(32,4),(48,6),(64,8),(128,8)]
    sampled = {'cases': 0, 'accepted': 0, 'rejected': 0, 'exact_output_entries': 0,
               'field_shapes': [], 'maximum_discovery_count': 0}
    hankel = []
    for q, m in shapes:
        p, w = field(q)
        k = q//m
        sampled['field_shapes'].append({'q':q,'m':m,'p':p,'root':w})
        units = [a for a in range(1,q) if math.gcd(a,q)==1]
        for a, beta in itertools.product(sorted(set(units[:2]+units[-1:])), [0,q-1]):
            for r in sorted(set([0,1,min(2,m),m-1,m])):
                selected = list(range(r))
                for kind in ['shared','staggered','late']:
                    ds = [[0]*m for _ in range(k)]
                    for b in range(k):
                        for j in selected:
                            live = kind=='shared' or (kind=='staggered' and b==j) or (kind=='late' and b==k-1-j)
                            if live:
                                ds[b][j] = RNG.randrange(1,p)
                    x = synthesis(ds,m,a,beta,p,w)
                    for cap in sorted(set([r,max(0,r-1)])):
                        accepted, entries, discoveries = check_case(x,m,a,beta,cap,p,w)
                        sampled['cases'] += 1
                        sampled['accepted' if accepted else 'rejected'] += 1
                        sampled['exact_output_entries'] += entries
                        sampled['maximum_discovery_count'] = max(sampled['maximum_discovery_count'],discoveries)
            x = [RNG.randrange(p) for _ in range(q)]
            for cap in [0,1,m]:
                accepted, entries, discoveries = check_case(x,m,a,beta,cap,p,w)
                sampled['cases'] += 1
                sampled['accepted' if accepted else 'rejected'] += 1
                sampled['exact_output_entries'] += entries
            if k % 2 == 0:
                for r in [0,m-1]:
                    ds = [[0]*m for _ in range(k)]
                    ds[k//2-1][r] = 1
                    x = synthesis(ds,m,a,beta,p,w)
                    h=q//2
                    expected = pow(-1,h*(h-1)//2,p)*pow(x[h-1],h,p) % p
                    actual = det_mod([[x[i+j] for j in range(h)] for i in range(h)],p)
                    assert actual == expected and actual != 0
                    hankel.append({'q':q,'m':m,'a':a,'beta':beta,'r':r,'determinant':actual})
    out['varied_even_composite_cases'] = sampled
    out['hankel_witnesses_checked'] = len(hankel)
    out['hankel_witnesses'] = hankel

    constant_cases=0
    for q,m in [(4,2),(16,4),(32,4),(64,8)]:
        p,w=field(q)
        assert (q//m)%m == 0
        for a in range(1,q):
            if math.gcd(a,q)!=1:
                continue
            for beta in range(q):
                ds=analysis([1]*q,m,a,beta,p,w)
                assert all(any(row[r] for row in ds) for r in range(m))
                constant_cases+=1
    out['constant_input_full_support_all_chirps_cases']=constant_cases

    # A small explicit one-mode witness outside every one-character common
    # quadratic chirp: enumerate that finite model after fixing x[0]=c.
    q,m=16,4
    p,w=field(q)
    ds=[[0]*m for _ in range(q//m)]
    for b,value in enumerate([1,2,3,5]):
        ds[b][0]=value
    x=synthesis(ds,m,1,0,p,w)
    matches=[]
    for a,b in itertools.product(range(q),repeat=2):
        if all(x[j] == x[0]*pow(w,a*j*j+b*j,p)%p for j in range(q)):
            matches.append([a,b])
    assert not matches
    out['common_chirp_rank_one_separation_witness']={'q':q,'m':m,'p':p,'root':w,
        'phase6_modes':[0],'phase6_a':1,'phase6_beta':0,'D_column':[1,2,3,5],
        'raw_x':x,'quadratic_linear_pairs_checked':q*q,'matches':matches}

    q,m,r,p = 256,16,2,2013265921
    k=q//m
    phi=sum(math.gcd(a,q)==1 for a in range(q))
    terms=[math.log10(math.comb(m,j))-k*(m-j)*math.log10(p) for j in range(r+1)]
    largest=max(terms)
    source_bound=math.log10(q*phi)+largest+math.log10(sum(10**(t-largest) for t in terms))
    tightened=math.log10(k*phi*math.comb(m,r))-k*(m-r)*math.log10(p)
    assert source_bound < -2077
    out['coverage_log10']={'source_bound':source_bound,'shift_quotient_and_maximal_support_bound':tightened}

    # Analytic threshold counterexample, evaluated independently.
    atol=1e-9
    delta=atol/2
    assert delta <= atol*(1+delta)
    out['floating_exactness_counterexample']={'q':64,'m':8,'x':'(atol/2)*e_0','atol':atol,
        'tolerance_detector_returns_zero':True,'true_global_mode_count':8,
        'normalized_all_bin_error':delta/math.sqrt(64)}

    rng=np.random.default_rng(6215)
    entropy_checks=0
    max_change=0.0
    for n in [4,8,16,32]:
        f=np.exp(-2j*np.pi*np.outer(np.arange(n),np.arange(n))/n)/math.sqrt(n)
        probs=abs(f)**2
        entropy=float(-np.sum(probs*np.log2(probs)))
        assert abs(entropy-n*math.log2(n)) < 1e-10
        for _ in range(25):
            z=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
            u=np.linalg.qr(z)[0]
            z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
            g=np.linalg.qr(z)[0]
            p0=abs(u)**2
            before=float(-np.sum(p0*np.log2(p0)))
            u[:2]=g@u[:2]
            p1=abs(u)**2
            after=float(-np.sum(p1*np.log2(p1)))
            change=abs(after-before)
            max_change=max(max_change,change)
            assert change <= 2+1e-10
            entropy_checks+=1
    out['unitary_entropy_diagnostics']={'random_mixers':entropy_checks,'maximum_absolute_change':max_change,
        'proved_sharp_gate_change':2,'fourier_sizes':[4,8,16,32]}

    # The shipped counter's plain sum is outside padd: at least Q-1 omitted
    # additions per executed mode. This corrects only that visible omission.
    counter=[]
    for row in json.loads((SOURCE/'scale_audit.json').read_text()):
        omitted=row['modes']*(row['q']-1)
        counter.append({'q':row['q'],'reported':row['counted_modular_add_mult'],
            'unmetered_seed_additions_at_least':omitted,
            'reported_plus_seed_additions_per_input':(row['counted_modular_add_mult']+omitted)/row['q']})
    out['source_counter_partial_correction']=counter
    target=Path(__file__).with_name('CHECK_RESULTS.json')
    target.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['hankel_witnesses','source_counter_partial_correction']},indent=2))


if __name__=='__main__':
    main()
