"""Full-subset Fourier cut / quasiseparable boundary-rank obstruction.

If B = M C[:,pi], C invertible, upper/lower QS rank ceilings for C/B,
then for any I subset of B-columns, J=pi(I),
    rank(M[I^c,J]) <= budget_B(I) + budget_C(J)
where budget counts transitions of membership in an index set.

Modular rank gives characteristic-zero lower bound (not necessarily equality).
"""
from functools import lru_cache
from itertools import combinations,permutations
from collections import Counter


def boundaries(mask,n):
    # descending membership 1->0 means J to left and J^c to right: lower-rank block
    down=up=0
    for k in range(1,n):
        a=(mask>>(k-1))&1;b=(mask>>k)&1
        if a and not b: down+=1
        if not a and b: up+=1
    return up, down


def budget(mask,n,up=1,down=1):
    a,b=boundaries(mask,n)
    return a*up+b*down


def modrank(arr,p):
    if not arr:return 0
    A=[[x%p for x in row] for row in arr]
    nrows=len(A);ncols=len(A[0])
    pivot=0
    for j in range(ncols):
        k=next((i for i in range(pivot,nrows) if A[i][j]),None)
        if k is None:continue
        A[pivot],A[k]=A[k],A[pivot]
        z=pow(A[pivot][j],-1,p)
        for q in range(j,ncols):A[pivot][q]=(A[pivot][q]*z)%p
        for i in range(pivot+1,nrows):
            f=A[i][j]
            if f:
                for q in range(j,ncols):A[i][q]=(A[i][q]-f*A[pivot][q])%p
        pivot+=1
        if pivot==nrows:break
    return pivot


def primitive_root(n,p):
    assert (p-1)%n==0
    for x in range(2,p):
        z=pow(x,(p-1)//n,p)
        if pow(z,n,p)==1 and (n==1 or pow(z,n//2,p)!=1):return z
    raise RuntimeError('root not found')


def fourier_matrix(n,p=12289,in_order=None,out_order=None):
    z=primitive_root(n,p)
    ai=list(range(n)) if out_order is None else out_order
    bj=list(range(n)) if in_order is None else in_order
    return [[pow(z,ai[i]*bj[j],p) for j in range(n)] for i in range(n)]


def rank_table(M,p=12289):
    n=len(M);size=1<<n
    table={}
    for t in range(1,n):
        masks=[sum(1<<i for i in comb) for comb in combinations(range(n),t)]
        for row_i in masks:
            rows=[i for i in range(n) if not(row_i>>i)&1]
            for col_j in masks:
                cols=[j for j in range(n) if (col_j>>j)&1]
                table[(row_i,col_j)]=modrank([[M[i][j] for j in cols] for i in rows],p)
    return table


def apply_perm_mask(pi,mask):
    return sum(1<<pi[k] for k in range(len(pi)) if (mask>>k)&1)


def subset_violations(pi,table,upC=1,downC=1,upB=1,downB=1):
    n=len(pi);N=1<<n
    costsB=[budget(mask,n,upB,downB) for mask in range(N)]
    costsC=[budget(mask,n,upC,downC) for mask in range(N)]
    for I in range(1,N-1):
        J=apply_perm_mask(pi,I)
        k=table[(I,J)]
        cost=costsB[I]+costsC[J]
        if k>cost:return {'I':I,'J':J,'rank':k,'budget':cost,'type':'subset'}
    return None

if __name__=='__main__':
    from pathlib import Path
    import sys,time,json
    here=Path(__file__).parent
    sys.path.insert(0,str(here.parent/'fft_window_rank_gate_2026-10-09'))
    from window_gate import check_windows
    import pickle
    for n in [8]:
        start=time.time();M=fourier_matrix(n)
        r=rank_table(M)
        print('rank_table',len(r),'seconds',round(time.time()-start,2))
        stats=Counter();witness=None
        for pi in permutations(range(n)):
            old=not check_windows(pi)
            new=subset_violations(pi,r) is None
            stats[(old,new)]+=1
            if old and not new and witness is None:
                witness={'pi':pi,'violation':subset_violations(pi,r)}
        print('counts',dict(stats),'witness',witness,'seconds',round(time.time()-start,2))
