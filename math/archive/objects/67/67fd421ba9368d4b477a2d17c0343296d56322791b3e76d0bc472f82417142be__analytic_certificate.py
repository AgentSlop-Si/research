"""Independent exact structural certificates for rank-one bidirectional stages.

In characteristic zero the simple induction in RESEARCH.md proves that a
polynomial supported on <=3 powers has at most N/2 zeros at Nth roots of
unity, for N a power of 2. This file independently checks its N=8
consequence using two finite fields, and verifies the tight upper witness
by determinants in the exact cyclotomic ring Z[z]/(z^4+1).
"""
from __future__ import annotations
from itertools import combinations, permutations
from collections import Counter
import json


def rank_mod(a, prime):
    if not a: return 0
    v=[[z%prime for z in row] for row in a]
    n=len(v);m=len(v[0]);r=0
    for j in range(m):
        pivot=next((i for i in range(r,n) if v[i][j]),None)
        if pivot is None: continue
        v[pivot],v[r]=v[r],v[pivot]
        inv=pow(v[r][j],prime-2,prime)
        for k in range(j,m):v[r][k]=v[r][k]*inv%prime
        for i in range(r+1,n):
            scale=v[i][j]
            if scale:
                for k in range(j,m):v[i][k]=(v[i][k]-scale*v[r][k])%prime
        r+=1
        if r==n:break
    return r


def root8(p,g):
    assert (p-1)%8==0
    w=pow(g,(p-1)//8,p)
    assert pow(w,4,p)==p-1
    return w


def det_over_cyclotomic_8(row_indices,col_indices):
    """Returns exact coefficient vector in Z[z]/(z^4+1), NOT floats."""
    r=len(row_indices)
    assert r==len(col_indices)
    accum=[0,0,0,0]
    for perm in permutations(range(r)):
        inversions=sum(perm[i]>perm[j] for i in range(r) for j in range(i+1,r))
        sign=(-1)**inversions
        exp=sum(row_indices[i]*col_indices[perm[i]] for i in range(r))%8
        sign*= -1 if exp>=4 else 1
        accum[exp%4]+=sign
    return tuple(accum)


def run():
    report={'primes':[],'complex_balanced_determinants':{},'dyadic_3_term_example_n':[]}
    for p,g in ((998244353,3),(2013265921,31)):
        w=root8(p,g)
        f=[[pow(w,(i*j)%8,p) for j in range(8)] for i in range(8)]
        c=Counter()
        for rows in combinations(range(8),3):
            for cols in combinations(range(8),5):
                r=rank_mod([[f[i][j] for j in cols] for i in rows],p)
                c[r]+=1
        assert c==Counter({3:56*56}),c
        order=(0,2,4,6,1,3,5,7)
        for cut in range(1,8):
            up=rank_mod([[f[i][j] for j in order[cut:]] for i in order[:cut]],p)
            down=rank_mod([[f[i][j] for j in order[:cut]] for i in order[cut:]],p)
            assert up<=3 and down<=3
            if cut==3:assert (up,down)==(3,3)
        report['primes'].append({'modulus':p,'root8':w,'rank3_3x5_matrices':c[3],
                                  'parity_qsep_order':3})
    order=(0,2,4,6,1,3,5,7)
    detup=det_over_cyclotomic_8(order[:4],order[4:])
    detdown=det_over_cyclotomic_8(order[4:],order[:4])
    assert detup==(0,0,0,0) and detdown==(0,0,0,0)
    report['complex_balanced_determinants']={'upper':detup,'lower':detdown}
    # Explicit induction sanity checks on trinomials with small coefficients.
    for n,p,g in ((2,998244353,3),(4,998244353,3),(8,998244353,3),
                  (16,998244353,3),(32,998244353,3)):
        w=pow(g,(p-1)//n,p)
        tested=0
        for positions in combinations(range(n),min(3,n)):
            if n>16 and tested>=100:break
            for signs in ((1,1,1),(1,-1,1),(-1,1,1)) if len(positions)==3 else ((1,1),):
                coeffs=list(zip(positions,signs))
                vals=[sum(a*pow(w,(j*k)%n,p) for j,a in coeffs)%p for k in range(n)]
                assert sum(z!=0 for z in vals)>=n//2,(n,positions,signs)
                tested+=1
        report['dyadic_3_term_example_n'].append({'n':n,'tested':tested})
    return report

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
