"""A *fully charged linear-work stage* evading the single-order cut-rank gate.

Uses two differently ordered Green solves, plus an optional rational Householder.
It is NOT an FFT factorization. Fields are F_998244353 for exact audit.
"""
from math import isqrt
from random import Random
from minor_certificate import MOD, rank_mod
from green_sum_audit import tridiagonal_solve


def parity_order(n):
    assert n%2==0
    return list(range(0,n,2)) + list(range(1,n,2))


def green_matrix(n, p=MOD):
    cols=[]
    for j in range(n):
        b=[int(j==i) for i in range(n)]
        cols.append(tridiagonal_solve(3,b,p=p))
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def mixed_matrix(n, p=MOD):
    """(P G P^T) + (1/20) G, P's ordering is even then odd."""
    G=green_matrix(n,p)
    order=parity_order(n)
    eps=pow(20,-1,p)
    return [[(G[order[i]][order[j]]+eps*G[i][j])%p for j in range(n)]
            for i in range(n)]


def rational_householder_components(n,p=MOD):
    z=isqrt(n-1)
    if z*z<n-1:z+=1
    u=[z]+[1]*(n-1)
    d=(z*z+n-1)%p
    assert d
    return u,2*pow(d,-1,p)%p


def householder_apply_mod(x, p=MOD):
    u,lam=rational_householder_components(len(x),p)
    inner=sum((a*b) for a,b in zip(u,x))%p
    factor=lam*inner%p
    return [(val-factor*a)%p for val,a in zip(x,u)]


def phase_diagonals(n,p=MOD):
    """Prepare w^(i*i) and w^i in O(n) modular multiplications."""
    assert (p-1)%n==0
    w=pow(3,(p-1)//n,p)
    right=[1]*n
    left=[1]*n
    ratio=w
    step=w*w%p
    for i in range(n-1):
        right[i+1]=right[i]*w%p
        left[i+1]=left[i]*ratio%p
        ratio=ratio*step%p
    return left,right


def apply_mixed(x,p=MOD,reflect=True,phases=False):
    """O(N) field arithmetic and O(N) memory, no dense matrix creation.

    We define S0[i,j]=G[order[i],order[j]]+G[i,j]/20.
    A vector x is first scattered from new coordinates to old ones;
    the output is gathered back after an O(N) tridiagonal solve.
    """
    n=len(x)
    if phases:
        left,right=phase_diagonals(n,p)
        x=[a*b%p for a,b in zip(x,right)]
    order=parity_order(n)
    v=[0]*n
    for i,old in enumerate(order):v[old]=x[i]
    transformed=tridiagonal_solve(3,v,p=p)
    term1=[transformed[old] for old in order]
    term2=tridiagonal_solve(3,x,p=p)
    eps=pow(20,-1,p)
    combined=[(a+eps*b)%p for a,b in zip(term1,term2)]
    out=householder_apply_mod(combined,p) if reflect else combined
    if phases: out=[a*b%p for a,b in zip(out,left)]
    return out


def left_apply_householder(M,p=MOD):
    n=len(M)
    cols=[[M[i][j] for i in range(n)] for j in range(n)]
    trans=[householder_apply_mod(v,p) for v in cols]
    return [[trans[j][i] for j in range(n)] for i in range(n)]


def inverse_mod(A,p=MOD):
    n=len(A)
    a=[[x%p for x in row]+[int(i==j) for j in range(n)]
       for i,row in enumerate(A)]
    for j in range(n):
        k=next((i for i in range(j,n) if a[i][j]),None)
        if k is None: raise ValueError('singular')
        a[j],a[k]=a[k],a[j]
        v=pow(a[j][j],p-2,p)
        a[j]=[v*x%p for x in a[j]]
        for i in range(n):
            if i==j:continue
            coeff=a[i][j]
            if coeff:
                a[i]=[(a[i][h]-coeff*a[j][h])%p for h in range(2*n)]
    return [row[n:] for row in a]


def audit(n,seed=123, inverse=True):
    p=MOD
    m=n//2
    order=parity_order(n)
    G=green_matrix(n,p)
    E=order[:m]; O=order[m:]
    parity_cross=rank_mod([[G[i][j] for j in O] for i in E])
    assert parity_cross==m
    M=mixed_matrix(n,p)
    M_cross=rank_mod([row[m:] for row in M[:m]])
    assert M_cross>=m-1
    S=left_apply_householder(M,p)
    S_cross=rank_mod([row[m:] for row in S[:m]])
    assert S_cross>=m-2
    L,R=phase_diagonals(n,p)
    S_phase=[[S[i][j]*L[i]*R[j]%p for j in range(n)] for i in range(n)]
    assert rank_mod([row[m:] for row in S_phase[:m]])==S_cross
    rng=Random(seed)
    for _ in range(4):
        x=[rng.randrange(p) for i in range(n)]
        full=[sum(S[i][j]*x[j] for j in range(n))%p for i in range(n)]
        fast=apply_mixed(x,p,reflect=True)
        assert fast==full
        full_phase=[sum(S_phase[i][j]*x[j] for j in range(n))%p for i in range(n)]
        fast_phase=apply_mixed(x,p,reflect=True,phases=True)
        assert fast_phase==full_phase
    info=dict(n=n,parity_green_half_rank=parity_cross,
              mixed_half_rank=M_cross,reflected_half_rank=S_cross,
              mixed_nonzeros=sum(bool(v) for row in M for v in row),
              reflected_nonzeros=sum(bool(v) for row in S for v in row),
              exact_new_vector_checks=4,exact_complex_phase_vector_checks=4)
    if inverse:
        Mi=inverse_mod(M,p)
        Si=inverse_mod(S,p)
        info['mixed_inverse_nonzeros']=sum(bool(v) for row in Mi for v in row)
        info['reflected_inverse_nonzeros']=sum(bool(v) for row in Si for v in row)
    return info


if __name__=='__main__':
    import json
    print(json.dumps([audit(n) for n in (8,16,32,64)],indent=2))
