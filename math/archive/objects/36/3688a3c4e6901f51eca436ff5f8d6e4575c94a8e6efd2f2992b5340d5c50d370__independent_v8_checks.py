#!/usr/bin/env python3
"""Independent exact finite-instance checks. Imports no uploaded implementation.

Run from any directory. The script uses only the Python standard library and
writes its JSON result next to itself. No source-bundle files are needed.
"""
from itertools import product
from pathlib import Path
import json
import math
import random
import time

P = 998244353
G = 3


def dft(v, root):
    n = len(v)
    return [sum(v[j] * pow(root, (-m*j) % n, P) for j in range(n)) % P
            for m in range(n)]


def exclusive_scan(v):
    """Own balanced integer scan, used modulo P and for exact sums."""
    a = list(v)
    n = len(a)
    stride = 2
    while stride <= n:
        for right in range(stride-1, n, stride):
            a[right] += a[right-stride//2]
        stride *= 2
    a[-1] = 0
    stride = n
    while stride >= 2:
        for right in range(stride-1, n, stride):
            left = right-stride//2
            saved = a[left]
            a[left] = a[right]
            a[right] += saved
        stride //= 2
    return a


def modular_row(n, m, a, beta):
    k = n//m
    z = pow(G, (P-1)//n, P)
    x = [(j*j*19+23*j+71) % P for j in range(n)]
    phase = [[pow(z, (a*t*t+(2*a*m*r+beta)*t) % n, P)
              for t in range(m)] for r in range(k)]
    d = [sum(phase[r][t]*x[r*m+t] for t in range(m)) % P
         for r in range(k)]
    projected = [(d[r]*pow(phase[r][t], P-2, P)) % P
                 for r in range(k) for t in range(m)]
    target = dft(projected, z)
    D = dft(d, pow(z, m, P))
    out = [None]*n
    # This is the unnormalized exact recurrence; omit common 1/sqrt(N).
    for seed in (0, 1):
        ids = [(seed+2*a*j) % n for j in range(n//2)]
        gauges = [pow(z, (a*j*j+(beta+seed)*j) % n, P)
                  for j in range(n//2)]
        for j in range(len(ids)-1):
            assert gauges[j+1] == (gauges[j]*pow(z,(a+beta+ids[j]) % n,P)) % P
        forcings = [(D[idx % k]-pow(z,(-a*m*m-idx*m-beta*m) % n,P)
                     *D[(idx+2*a*m) % k]) % P for idx in ids]
        q = [(f*pow(gauge,P-2,P)) % P for f,gauge in zip(forcings,gauges)]
        prefixes = exclusive_scan(q)
        seed_value = sum(d[r]*pow(z,(-a*t*t-(2*a*m*r+beta+seed)*t-seed*m*r)%n,P)
                         for r in range(k) for t in range(m)) % P
        assert seed_value == target[seed]
        for idx, gauge, pref in zip(ids,gauges,prefixes):
            out[idx] = gauge*(seed_value-pref) % P
    assert out == target
    return {'N':n,'M':m,'a':a,'beta':beta,'all_outputs_exact':True}


def grid_estimate_twice(word):
    """tau=3, W=21, offsets 0,7,14. Return twice the center median."""
    centers2 = []
    for k in range(3):
        cand = 0
        count = 0
        for z in word:
            cell = (z-7*k)//21  # Python // is signed floor, exactly.
            if count == 0:
                cand, count = cell, 1
            elif cell == cand:
                count += 1
            else:
                count -= 1
        centers2.append(42*cand+14*k+21)
    return sorted(centers2)[1]


def ledger_ratio(L, Lm, t):
    c = math.expm1(2*math.log1p(t))
    e = c+(1+c)*(c+t*(2+c))
    a = math.expm1(math.log1p(c)+Lm*math.log1p(t))
    b = math.expm1((L-Lm)*math.log1p(e))
    h = math.expm1(math.log1p(a)+math.log1p(b)+math.log1p(c))
    s = math.expm1(math.log1p(a)+2*math.log1p(c)+L*math.log1p(t))
    f = 2*h+c*(1+h)+t*(2+c)*(1+h)
    q = (1+c)*f+2*c
    gamma = math.expm1(2*L*math.log1p(t))
    pref = q+gamma*(2+q)
    M_over_sqrtNM = 2.0**((Lm-L)/2)
    coefficient = (1+c)*(1+t)*(M_over_sqrtNM*s+pref)+(3*t*(1+c)+c)*M_over_sqrtNM
    return coefficient/(L*t)


def run():
    started = time.time()
    exact = []
    for n,m in [(8,2),(16,2),(32,4),(64,4),(128,8),(256,8)]:
        for a,beta in [(1,0),(3,1),(n-1,n-1)]:
            exact.append(modular_row(n,m,a,beta))
    scan_cases = 0
    for ell in range(1,10):
        word = [((j*71)%103)-51 for j in range(2**ell)]
        actual = exclusive_scan(word)
        acc = 0
        for value, result in zip(word, actual):
            assert result == acc
            acc += value
        scan_cases += 1
    grid_all = grid_majority = endpoint_majority = 0
    for mu in range(21):
        alphabet = [mu-30,mu-3,mu-2,mu,mu+2,mu+3,mu+30]
        for length in (1,3,5):
            for word in product(alphabet,repeat=length):
                grid_all += 1
                good = sum(abs(z-mu)<=3 for z in word)
                if 2*good > length:
                    grid_majority += 1
                    endpoint_majority += any(abs(z-mu)==3 for z in word)
                    assert abs(grid_estimate_twice(word)-2*mu) <= 15
    rng = random.Random(813257)
    random_cases = 3000
    for _ in range(random_cases):
        mu = rng.randrange(-500,501)
        length = rng.choice([7,11,21,51,101])
        good_count = rng.randrange(length//2+1,length+1)
        word = [mu+rng.randrange(-3,4) for _ in range(good_count)]
        word += [mu+rng.choice([-1,1])*rng.randrange(4,10**6) for _ in range(length-good_count)]
        rng.shuffle(word)
        assert abs(grid_estimate_twice(word)-2*mu) <= 15
    largest = (0,None)
    ledger_cases = 0
    for L in list(range(3,257))+[512,1024,4096,10000,100000,1000000]:
        for Lm in sorted(set([1,max(1,(L-1)//4),max(1,(L-1)//2)])):
            assert 2*Lm+1 <= L
            for frac in [1e-12,1e-9,1e-6,0.001,0.01,0.1,0.5,1.0]:
                t = .01*frac/L
                ratio = ledger_ratio(L,Lm,t)
                assert ratio < 100
                ledger_cases += 1
                if ratio > largest[0]:
                    largest = (ratio, {'L':L,'log2_M':Lm,'t':t})
    return {
        'status':'all independent checks passed',
        'uploaded_code_executed':False,
        'exact_modular_gauge_cases':exact,
        'exact_balanced_scan_cases':scan_cases,
        'exact_grid_words_tested':grid_all,
        'exact_grid_strict_majority_words':grid_majority,
        'majority_words_containing_interval_endpoints':endpoint_majority,
        'random_adversarial_grid_cases':random_cases,
        'finite_precision_ledger_cases':ledger_cases,
        'maximum_ledger_ratio_to_sqrtNM_L_t':largest,
        'caveat':'Finite tests supplement the written proofs. They do not certify NumPy/IEEE phase generation or establish general numerical bounds by experiment.',
        'elapsed_seconds':time.time()-started,
    }

if __name__ == '__main__':
    result = run()
    target = Path(__file__).resolve().with_name('independent_v8_results.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='exact_modular_gauge_cases'},indent=2))
