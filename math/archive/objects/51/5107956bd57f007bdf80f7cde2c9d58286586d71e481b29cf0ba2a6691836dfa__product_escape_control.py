"""Phase 12 negative-control: products of Green sums evade the one-layer minor gate.

This is NOT an exact Fourier factorization. It prevents extending the rank<=2
argument incorrectly to products of two such inexpensive layers.
"""
from __future__ import annotations
import json
import random
from cycle_minor_gate import (linearize_perm,find_rectangle,green_perm_submatrix,
                               permutation_cycles,rank_mod,det_mod,
                               auxiliary_prime_root)


def mm(A,B,q):
    n=len(A);d=len(B);m=len(B[0]);C=[[0]*m for _ in range(n)]
    for i in range(n):
        for k in range(d):
            if not A[i][k]:continue
            aik=A[i][k]
            for j in range(m): C[i][j]=(C[i][j]+aik*B[k][j])%q
    return C


def sample_product_escape(p=29,seed=1202,q=100109):
    rng=random.Random(seed)
    n=p
    stages=[];cycles=[]
    for _ in range(4):
        perm=list(range(n));rng.shuffle(perm)
        weights=[rng.randrange(q) for _ in range(n)]
        for cyc in permutation_cycles(perm):
            product=1
            for i in cyc:product=product*weights[i]%q
            if product==1: weights[cyc[0]]=0
        stages.append((perm,weights));cycles.append(len(permutation_cycles(perm)))
    full=list(range(n))
    mats=[green_perm_submatrix(pi,w,full,full,q) for pi,w in stages]
    T1=[[(mats[0][i][j]+mats[1][i][j])%q for j in range(n)]for i in range(n)]
    T2=[[(mats[2][i][j]+mats[3][i][j])%q for j in range(n)]for i in range(n)]
    T=mm(T1,T2,q)
    order=[linearize_perm(stages[i][0]) for i in [0,1]]
    cert=find_rectangle(order,3)
    R,C=cert['rows'],cert['cols']
    slice_1=[[T1[i][j] for j in C]for i in R]
    slice_product=[[T[i][j]for j in C]for i in R]
    result={'prime':p,'q':q,'seed':seed,'cycles_each':cycles,
            'rows':R,'cols':C,'stage1_crosscut_rank':rank_mod(slice_1,q),
            'product_crosscut_rank':rank_mod(slice_product,q),
            'product_crosscut_det':det_mod(slice_product,q)}
    assert result['stage1_crosscut_rank']<=2
    return result


if __name__=='__main__':
    c=sample_product_escape()
    print(json.dumps(c,indent=2))
