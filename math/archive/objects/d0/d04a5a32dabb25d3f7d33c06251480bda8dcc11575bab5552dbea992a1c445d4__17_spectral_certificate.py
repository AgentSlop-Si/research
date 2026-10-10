"""Exact integer spectral-gap certificate for a fixed two-path expander sample.

For integer graph Laplacian L and n vertices, positive definiteness of
K=4n L + 4 J - n I guarantees lambda_2(L)>1/4, since the all-ones
vector has eigenvalue 3n for K and an orthogonal vector has eigenvalue
n(4lambda_i(L)-1).

Uses fraction-free symmetric Bareiss elimination with no pivots. Output
includes only positive-pivot bit-lengths and SHA-256 of the pivot list;
any reader can rerun the whole exact integer verification.
"""
from hashlib import sha256
from time import perf_counter
from expander_stage import random_order,path_union_edges


def integer_laplacian(n, paths):
    L=[[0]*n for _ in range(n)]
    for path in paths:
        for i,j in path:
            L[i][i]+=1;L[j][j]+=1
            L[i][j]-=1;L[j][i]-=1
    return L


def exact_ldlt_sylvester(A):
    n=len(A)
    a=[row[:] for row in A]
    prev=1
    pivots=[]
    for k in range(n):
        pivot=a[k][k]
        if pivot<=0:
            raise AssertionError(f'leading principal minor not positive: k={k} value={pivot}')
        pivots.append(pivot)
        if k==n-1: break
        for i in range(k+1,n):
            aik=a[i][k]
            for j in range(i,n):
                numerator=a[i][j]*pivot-aik*a[k][j]
                x,rem=divmod(numerator,prev)
                if rem:
                    raise AssertionError(f'Bareiss division not exact at {i},{j} step {k}')
                a[i][j]=x
                if j>i:a[j][i]=x
        for i in range(k+1,n): a[i][k]=a[k][i]=0
        prev=pivot
    return pivots


def run(n):
    t0=perf_counter()
    order=random_order(n,seed=20261009+n)
    path_edges=path_union_edges(order)
    L=integer_laplacian(n,path_edges)
    K=[[4*n*L[i][j]+4-n*(i==j) for j in range(n)] for i in range(n)]
    pivots=exact_ldlt_sylvester(K)
    evidence=sha256((';'.join(str(x) for x in pivots)).encode()).hexdigest()
    return dict(n=n,positive_leading_principal_minors=len(pivots),
                spectral_gap_strict_gt_one_quarter=True,
                balanced_boundary_strict_gt_n_over_16=True,
                first_pivots=pivots[:3],last_pivot_bit_length=pivots[-1].bit_length(),
                pivot_sequence_sha256=evidence,
                elapsed_seconds=round(perf_counter()-t0,3))

if __name__=='__main__':
    import json
    print(json.dumps([run(n) for n in (32,64,128)],indent=2))
