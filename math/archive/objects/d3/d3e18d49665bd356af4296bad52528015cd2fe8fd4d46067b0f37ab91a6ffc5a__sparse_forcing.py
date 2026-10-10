"""Exact full DFT for sparse q-difference forcing; fresh restricted inputs.

Python standard library, prime-field oracle. This is not a general faster FFT.
"""
from collections import Counter
import json
from pathlib import Path
import random


def root(n, p):
    assert n >= 2 and n & (n-1) == 0 and (p-1) % n == 0
    q = pow(3, (p-1)//n, p)
    assert pow(q,n,p) == 1 and pow(q,n//2,p) != 1
    return q


def forcing(x, q, p):
    n = len(x)
    r = [x[-1] % p]
    qp = q
    for j in range(1,n):
        r.append(((qp-1)*x[j]+x[j-1]) % p)
        qp = qp*q % p
    return r


def invert_forcing(r, q, p):
    n = len(r)
    powers = [1]
    for j in range(1,n): powers.append(powers[-1]*q % p)
    x = [0]*n
    x[-1] = r[0] % p
    for j in range(n-1,0,-1):
        x[j-1] = (r[j]-(powers[j]-1)*x[j]) % p
    return x


def transform(x, q, p):
    """Detect forcing and return all N Fourier values with charged arithmetic.

    Scalar operation counts include multiplication by 1. Constant comparisons,
    indexing, and traffic have a separate O(N(s+1)) word bound, not zero cost.
    The exact primitive root q is supplied. No input FFT is called.
    """
    n = len(x)
    assert n >= 2 and n & (n-1) == 0
    count = Counter()
    powers = [1]
    for j in range(1,n):
        powers.append(powers[-1]*q % p); count['mul'] += 1
    r = [x[-1] % p]
    for j in range(1,n):
        r.append(((powers[j]-1)*x[j]+x[j-1]) % p)
        count['sub'] += 1; count['mul'] += 1; count['add'] += 1
    support = [j for j in range(1,n) if r[j]]
    rhs = [r[0]]*n
    for j in support:
        term = r[j]
        for k in range(n):
            rhs[k] = (rhs[k]+term) % p; count['add'] += 1
            if k+1 < n:
                term = term*powers[j] % p; count['mul'] += 1
    out = [0]*n
    out[1] = rhs[0]
    for k in range(1,n):
        out[(k+1)%n] = ((1-powers[k])*out[k]+rhs[k]) % p
        count['sub'] += 1; count['mul'] += 1; count['add'] += 1
    s = len(support)
    assert dict(count) == {'mul':(s+3)*(n-1),'sub':2*(n-1),'add':s*n+2*(n-1)}
    return out, {'n':n,'middle_support':s,'field_operations':dict(count),
                 'root_assumption':'primitive order-N root supplied',
                 'word_work':'O(N(s+1)), including detection/indexing/traffic',
                 'storage':'O(N) field elements and indices'}


def direct(x,q,p):
    return [sum(x[j]*pow(q,k*j,p) for j in range(len(x))) % p
            for k in range(len(x))]


def run():
    rng=random.Random(91702)
    basis=0; special=[]; dense=[]
    for p in (65537,998244353):
        for n in (2,4,8,16,32,64):
            q=root(n,p)
            for j in range(n):
                r=[int(i==j) for i in range(n)]
                x=invert_forcing(r,q,p)
                assert forcing(x,q,p)==r
                result,cost=transform(x,q,p)
                assert result==direct(x,q,p)
                basis+=1
        for n in (64,128,256):
            q=root(n,p)
            for s in (0,1,2,4):
                r=[0]*n; r[0]=rng.randrange(1,p)
                for j in rng.sample(range(1,n),s): r[j]=rng.randrange(1,p)
                x=invert_forcing(r,q,p)
                result,cost=transform(x,q,p)
                assert forcing(x,q,p)==r
                assert result==direct(x,q,p)
                assert cost['middle_support']==s
                special.append({'prime':p,**cost})
            # Invertibility permits every middle forcing coefficient to be nonzero.
            r=[1]*n
            x=invert_forcing(r,q,p)
            result,cost=transform(x,q,p)
            assert result==direct(x,q,p)
            assert cost['middle_support']==n-1
            dense.append({'prime':p,**cost})
    report={'status':'PASS','forcing_basis_vectors':basis,
            'sparse_family_cases':len(special),'dense_forcing_controls':len(dense),
            'sparse_cases':special,'dense_controls':dense,
            'scope':'Fresh full exact DFT for sparse q-forcing; worst-case quadratic for this evaluator.'}
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('sparse_cases','dense_controls')}))


if __name__=='__main__': run()
