"""Auditor-authored verifier. Reads uploaded files as data; imports/runs none.

All matrix construction and algebra below are independent implementations.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json
import math
import random

OPTIONS = argparse.ArgumentParser(description=__doc__)
OPTIONS.add_argument('--source-dir', type=Path, help='Optional original archive directory for checksum and reported-number comparisons.')
ARGS = OPTIONS.parse_args()
SRC = ARGS.source_dir
OUT = Path(__file__).resolve().parent
P = 998244353

def ident(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]

def mm(a, b, p=None):
    v = [[sum(a[i][k] * b[k][j] for k in range(len(b)))
          for j in range(len(b[0]))] for i in range(len(a))]
    return [[x % p for x in row] for row in v] if p else v

def inv(a, p=None):
    n = len(a)
    z = [[(v % p if p else Q(v)) for v in row] + ident(n)[i]
         for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if z[i][j])
        z[j], z[pivot] = z[pivot], z[j]
        f = pow(z[j][j], -1, p) if p else 1 / z[j][j]
        z[j] = [(v * f % p if p else v * f) for v in z[j]]
        for i in range(n):
            if i == j:
                continue
            f = z[i][j]
            z[i] = [((v - f * w) % p if p else v - f * w)
                    for v, w in zip(z[i], z[j])]
    return [row[n:] for row in z]

def rk(a, p):
    z = [[v % p for v in row] for row in a]
    row = 0
    for col in range(len(z[0])):
        ix = next((i for i in range(row, len(z)) if z[i][col]), None)
        if ix is None:
            continue
        z[row], z[ix] = z[ix], z[row]
        s = pow(z[row][col], -1, p)
        z[row] = [v * s % p for v in z[row]]
        for i in range(row + 1, len(z)):
            s = z[i][col]
            z[i] = [(v - s * w) % p for v, w in zip(z[i], z[row])]
        row += 1
        if row == len(z):
            break
    return row

def tri(n, d, b):
    return [[d if i == j else b if abs(i-j) == 1 else 0
             for j in range(n)] for i in range(n)]

def dets(n, d, b):
    v = [1, d]
    for k in range(2, n + 1):
        v.append(d * v[-1] - b * b * v[-2])
    return v

def green_closed(n, d, b):
    v = dets(n, d, b)
    return [[Q((-b)**abs(i-j) * v[min(i,j)] * v[n-1-max(i,j)], v[n])
             for j in range(n)] for i in range(n)]

def add(a, b):
    return [[v+w for v, w in zip(x,y)] for x,y in zip(a,b)]

def norm1(a):
    return max(sum(abs(a[i][j]) for i in range(len(a)))
               for j in range(len(a[0])))

def modq(a):
    return [[v.numerator * pow(v.denominator, -1, P) % P for v in row]
            for row in a]

def nz(a):
    return sum(bool(v) for row in a for v in row)

def cuts(a):
    n = len(a)
    return max(max(rk([row[s:] for row in a[:s]], P),
                   rk([row[:s] for row in a[s:]], P)) for s in range(1,n))

def bitrev(i, bits):
    return sum(((i >> k) & 1) << (bits-1-k) for k in range(bits))

def butterfly(n, span, w):
    a = [[0] * n for _ in range(n)]
    half = span // 2
    for base in range(0,n,span):
        for j in range(half):
            x,y = base+j,base+j+half
            t = pow(w, j*(n//span), P)
            a[x][x] = a[y][x] = 1
            a[x][y],a[y][y] = t,(-t)%P
    return a

def do_check():
    report = {'method':'No uploaded Python imported, compiled, or executed.',
              'sha256':[], 'rational_green':[], 'modular_green':[],
              'gauge':[], 'stage_bounds':[]}
    for line in ((SRC/'SHA256SUMS.txt').read_text().splitlines() if SRC else []):
        h, name = line.split('  ')
        good = hashlib.sha256((SRC/name).read_bytes()).hexdigest() == h
        assert good, name
        report['sha256'].append({'file':name,'matches':good})
    expected = json.loads((SRC/'norm_results.json').read_text()) if SRC else None
    for n in (2,4,8,16,32):
        t = tri(n,3,-1)
        a,b,v = green_closed(n,3,-1),green_closed(n,4,-1),green_closed(n,7,-2)
        s = add(a,b)
        si = [[Q(t[i][j],2) + Q(i==j,4) - v[i][j]/4
               for j in range(n)] for i in range(n)]
        assert mm(t,a) == ident(n)
        assert mm(s,si) == ident(n)
        assert all(x>0 for row in s for x in row)
        assert all(si[i][j] < 0 for i in range(n) for j in range(n) if i!=j)
        assert all(si[i][i] > 0 for i in range(n))
        ns,ni = norm1(s),norm1(si)
        assert ns < Q(3,2) and ni < Q(17,6) and ns*ni < Q(17,4)
        if expected:
            supplied = next(x for x in expected['exact_real_column_norm'] if x['n']==n)
            assert ns == Q(supplied['norm1_num'],supplied['norm1_den'])
            supplied = next(x for x in expected['exact_condition1'] if x['n']==n)
            assert ns*ni == Q(supplied['kappa_1_numerator'],supplied['kappa_1_denominator'])
        det_s = Q(dets(n,7,-2)[n],dets(n,3,-1)[n]*dets(n,4,-1)[n])
        assert 0 < det_s < Q(11,20)**(n//2)*Q(7,12)**(n%2) < 1
        report['rational_green'].append({'n':n,'norm1':str(ns),'inverse_norm1':str(ni),
            'kappa1':str(ns*ni),'kappa1_float':float(ns*ni),'det_S':str(det_s),
            'identities_and_signs':True})
        if n>=4:
            sm,sim = modq(s),modq(si)
            assert inv(sm,P)==sim
            assert nz(sm)==n*n and nz(sim)==n*n
            assert cuts(sm)<=2 and cuts(sim)<=2
            report['modular_green'].append({'n':n,'S_nonzeros':nz(sm),
                'inverse_nonzeros':nz(sim),'S_cut_order':cuts(sm),'inverse_cut_order':cuts(sim)})
    for n in (4,8,16,32):
        L = n.bit_length()-1
        w = pow(3,(P-1)//n,P)
        u,v = list(range(1,n+1)),[3*i+1 for i in range(n)]
        beta = 7 * pow(1+7*sum(x*y for x,y in zip(u,v)),-1,P) % P
        h = [[(int(i==j)+7*u[i]*v[j])%P for j in range(n)] for i in range(n)]
        hi = [[(int(i==j)-beta*u[i]*v[j])%P for j in range(n)] for i in range(n)]
        assert mm(h,hi,P)==ident(n)
        base = [butterfly(n,1<<(i+1),w) for i in range(L)]
        dressed = []
        for i,B in enumerate(base):
            G = mm(h,B,P) if i==0 else mm(B,hi,P) if i==L-1 else mm(mm(h,B,P),hi,P)
            assert nz(G)==n*n
            dressed.append(G)
        recovered = mm(dressed[0],inv(base[0],P),P)
        assert recovered==h
        assert rk([[(h[i][j]-int(i==j))%P for j in range(n)] for i in range(n)],P)==1
        m = ident(n)
        for G in dressed:
            m = mm(G,m,P)
        m = [[m[i][bitrev(j,L)] for j in range(n)] for i in range(n)]
        f = [[pow(w,i*j,P) for j in range(n)] for i in range(n)]
        assert m==f
        rand = random.Random(20261009+n)
        for rep in range(12):
            x = [rand.randrange(P) for j in range(n)]
            via_m = mm(m,[[v] for v in x],P)
            direct = [[sum(x[j]*pow(w,k*j,P) for j in range(n))%P] for k in range(n)]
            assert via_m==direct
        report['gauge'].append({'n':n,'dense_stages':L,'full_fourier_equality':True,
            'rank_one_recovered':True,'fresh_vectors':12})
    for n in (16,64,256,1024,4096,65536,1048576):
        tf=tk=0
        while 9**tf < n*4**tf:tf+=1
        while 17**tk < n*4**tk:tk+=1
        report['stage_bounds'].append({'n':n,'forward_norm':tf,'condition1':tk})
    if SRC:
        report['test_methods_in_uploaded_suite'] = (SRC/'tests/test_green_gauge.py').read_text().count('    def test_')
    report['gauge_singular_supported_powers'] = [k for k in range(1,24)
        if (1+7*((1<<k)*((1<<k)+1)*(2*(1<<k)-1)//2))%P==0]
    report['determinant_refinement'] = 'Paired eigenvalues lambda,6-lambda give s(lambda)s(6-lambda) <= 11/20; any unscaled S-chain has determinant magnitude below one.'
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'independent_check_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('sha256','rational_green')},indent=2))

if __name__=='__main__':
    do_check()
