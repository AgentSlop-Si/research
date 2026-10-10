"""Phase 19 exact fixed-parameter Green-sum product rejection tests.

Dense inversions are offline finite-field oracles. Each sampled Green summand
is nevertheless the inverse of a permuted tridiagonal linear system; its actual
forward application is a tridiagonal solve, NOT a dense multiplication.
"""
from __future__ import annotations
import random
from field_core import P,root_n,inverse,monomial,matmul
from joint_gate import audit_outer


def green_summand(n,rng,w):
    B=[[0]*n for _ in range(n)]
    for i in range(n):
        B[i][i]=(9+pow(w,rng.randrange(n),P))%P
        if i+1<n:
            B[i][i+1]=(1+pow(w,rng.randrange(n),P))%P
            B[i+1][i]=(1+pow(w,rng.randrange(n),P))%P
    G=inverse(B)
    p=list(range(n));rng.shuffle(p)
    l=[pow(w,rng.randrange(n),P) for _ in range(n)]
    r=[pow(w,rng.randrange(n),P) for _ in range(n)]
    # In the common outer indexing, entry p[i],p[j] equals l[i]G[i,j]r[j].
    out=[[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):out[p[i]][p[j]]=l[i]*G[i][j]*r[j]%P
    return out


def green_sum(n,rng,w,q=2):
    S=[[0]*n for _ in range(n)]
    for _ in range(q):
        G=green_summand(n,rng,w)
        for i in range(n):
            for j in range(n):S[i][j]=(S[i][j]+G[i][j])%P
    return S


def reject_fixed_green_product(n,seed=0):
    rng=random.Random(190000+n*37+seed);w=root_n(n)
    A=green_sum(n,rng,w)
    B=green_sum(n,rng,w)
    out=audit_outer(A,B)
    assert out['status']=='impossible',out
    return {'n':n,'seed':seed,'two_independently_permuted_green_terms_per_stage':True,
            'all_middle_monomials_excluded_for_fixed_stages':True,
            'joint_gate_reason':out['reason']}

if __name__=='__main__':
    import json
    print(json.dumps([reject_fixed_green_product(n,seed) for n in (8,16,32,64)
                      for seed in (0,1,2)],indent=2))
