"""Exact, reproducible finite-N expansion certificates for random-cycle Green orders.

If the integer matrix K=4*n*L + 4*J - n*I is positive definite,
then lambda_2(L)>1/4 and every balanced cut has >n/16 undirected
crossing edges. K>0 is verified with exact fraction-free Bareiss pivots.
This certifies individual finite instances, NOT a uniform expander family.
"""
from __future__ import annotations
from hashlib import sha256
from time import perf_counter
from phase27_affine_gap import random_hamiltonian,shift_successor


def combined_laplacian(n:int,seed:int)->list[list[int]]:
    L=[[0]*n for _ in range(n)]
    for succ in (shift_successor(n),random_hamiltonian(n,seed)):
        for j,k in enumerate(succ):
            L[j][j]+=1;L[k][k]+=1
            L[j][k]-=1;L[k][j]-=1
    return L


def exact_positive_definite_pivots(mat:list[list[int]])->list[int]:
    n=len(mat)
    a=[r.copy() for r in mat]
    previous=1;pivots=[]
    for k in range(n):
        pivot=a[k][k]
        if pivot<=0:raise AssertionError(f'nonpositive exact pivot at {k}')
        pivots.append(pivot)
        if k==n-1:break
        for i in range(k+1,n):
            aik=a[i][k]
            for j in range(i,n):
                numerator=a[i][j]*pivot-aik*a[k][j]
                nextv,rem=divmod(numerator,previous)
                if rem:raise AssertionError(f'nonexact Bareiss division at {k},{i},{j}')
                a[i][j]=nextv
                if i!=j:a[j][i]=nextv
        for i in range(k+1,n):a[i][k]=a[k][i]=0
        previous=pivot
    return pivots


def certify(n:int,seed:int,delta_den:int=4)->dict:
    if n<8 or n&(n-1):raise ValueError('size power of 2 >= 8')
    if delta_den<1:raise ValueError('positive delta denominator')
    t=perf_counter()
    L=combined_laplacian(n,seed)
    # delta=1/delta_den, K=delta_den*n*L + delta_den*J - n*I
    # on 1^perp: n*(delta_den*lambda-1), on 1: delta_den*n-n
    K=[[delta_den*n*L[i][j] + delta_den - (n if i==j else 0)
        for j in range(n)] for i in range(n)]
    pivots=exact_positive_definite_pivots(K)
    digest=sha256((';'.join(map(str,pivots))).encode()).hexdigest()
    return {'n':n,'seed':seed,'delta_fraction':f'1/{delta_den}',
            'lambda2_strictly_greater':1/delta_den,
            'every_balanced_cut_edges_strictly_greater':n/(4*delta_den),
            'exact_positive_pivots':len(pivots),
            'pivot_digest_sha256':digest,
            'first_pivots':pivots[:3],
            'last_pivot_bits':pivots[-1].bit_length(),
            'seconds':round(perf_counter()-t,3)}

if __name__=='__main__':
    import json
    for n in (32,64,128):
        print(json.dumps(certify(n,2700+n),indent=2),flush=True)
