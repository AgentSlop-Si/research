"""Exact finite-field commutator rank witnesses for stationary Green circuits.
Small-N oracle: forms dense matrices ONLY to verify the claimed rank theorem.
The actual Green application uses O(N) tridiagonal solvers.
"""
from __future__ import annotations
from weyl_gate import P, TridiagonalLU,modular_root


def rank_mod(A):
    """Exact field rank O(n^3); offline verifier, not transform executor."""
    if not A:return 0
    a=[[x%P for x in row] for row in A]
    nr=len(a);nc=len(a[0]);pivot=0
    for j in range(nc):
        q=next((i for i in range(pivot,nr) if a[i][j]),None)
        if q is None:continue
        a[q],a[pivot]=a[pivot],a[q]
        inv=pow(a[pivot][j],-1,P)
        a[pivot]=[x*inv%P for x in a[pivot]]
        for i in range(pivot+1,nr):
            z=a[i][j]
            if z:
                a[i]=[(x-z*y)%P for x,y in zip(a[i],a[pivot])]
        pivot+=1
        if pivot==nr:break
    return pivot


def matrix_from_apply(oracle,n):
    cols=[]
    for i in range(n):
        b=[0]*n;b[i]=1
        cols.append(oracle(b))
    return [[cols[j][i] for j in range(n)] for i in range(n)]

def commute_shift(A):
    n=len(A)
    return [[(A[i][(j+1)%n]-A[(i-1)%n][j])%P for j in range(n)] for i in range(n)]

def matmul(A,B):
    n=len(A)
    return [[sum(A[i][k]*B[k][j] for k in range(n))%P for j in range(n)] for i in range(n)]

def one_green(n,a,b,c):
    solver=TridiagonalLU.build([0]+[b]*(n-1),[a]*n,[c]*(n-1)+[0])
    return matrix_from_apply(solver.solve,n)

def sum_stationary(n,q,k):
    S=[[0]*n for _ in range(n)]
    for i in range(q):
        # Near-resonant-sized denominator entries in the finite field; 
        # no numeric condition number is claimed over this field.
        a=2*n + 23*i + 11*k
        b=-(n-1)+3*i
        c=-(n-1)+5*k
        G=one_green(n,a,b,c)
        for r in range(n):
            for v in range(n):S[r][v]=(S[r][v]+G[r][v])%P
    return S

def modular_commutator_audit(n,q=2,t=2):
    stages=[sum_stationary(n,q,j) for j in range(t)]
    S_rank=[rank_mod(commute_shift(S)) for S in stages]
    M=[[int(i==j) for j in range(n)] for i in range(n)]
    for S in stages:M=matmul(S,M)
    rank=rank_mod(commute_shift(M))
    w=modular_root(n)
    DminusZ=[[((pow(w,j,P) if i==j else 0) - (1 if i==(j+1)%n else 0))%P
              for j in range(n)] for i in range(n)]
    Fourier_rank=rank_mod(DminusZ)
    return dict(n=n,q=q,t=t,individual_stage_ranks=S_rank,
                product_rank=rank,upper_bound=2*q*t,
                Fourier_commutator_rank=Fourier_rank)

if __name__=='__main__':
    import json
    print(json.dumps([modular_commutator_audit(n) for n in (8,16,32,64)],indent=2))
