"""Denominator-free polynomial rank gate for arbitrary TWO Green-sum layers.

Stage INPUT has a_j=I-P_j, j=1..r1 and X=sum_j a_j^-1.
Stage OUTPUT has d_k=I-Q_k, k=1..r2 and Y=sum_k d_k^-1.
Target is F_N = Y X (all inputs). Lift to H of size (r1+r2+1)N:

    [ diag(a_j)     0         -stack(I) ]
    [ -stack(I)*sum(I)  diag(d_k)  0     ]
    [ 0              -sum(I)     F_N     ]

When all a_j,d_k invertible,
    rank(H) = (r1+r2)N + rank(F_N - YX).

No matrix inversion appears in H entries. Exact rank= (r1+r2)N is
necessary and sufficient for the proposed Green-sum Fourier factorization.
It is a CHECKER, not a factorization or universal fast FFT.
"""
from __future__ import annotations
from cut_capacity import GreenGraph,exact_green,mat_add,mat_mul,rank_mod,fourier_mod


def sparse_a(g,q):
    n=len(g.pi)
    A=[[int(i==j) for j in range(n)] for i in range(n)]
    for i,j in enumerate(g.pi):A[i][j]=(A[i][j]-g.weights[i])%q
    return A


def block_matrix(input_graphs,output_graphs,F,q=65537):
    n=len(input_graphs[0].pi)
    r=len(input_graphs);s=len(output_graphs)
    size=(r+s+1)*n
    M=[[0]*size for _ in range(size)]
    # Stage 1: A_j u_j - x = 0 for all j.
    for j,g in enumerate(input_graphs):
        A=sparse_a(g,q)
        for i in range(n):
            for k in range(n):M[j*n+i][j*n+k]=A[i][k]
            M[j*n+i][(r+s)*n+i]=q-1
    # Stage 2: D_k v_k - sum_j u_j = 0 for all k.
    for j,g in enumerate(output_graphs):
        A=sparse_a(g,q)
        for i in range(n):
            row=(r+j)*n+i
            for k in range(n):M[row][(r+j)*n+k]=A[i][k]
            for h in range(r):M[row][h*n+i]=q-1
    # Output: F*x - sum_k v_k = 0.
    for i in range(n):
        row=(r+s)*n+i
        for k in range(n):M[row][(r+s)*n+k]=F[i][k]
        for j in range(s):M[row][(r+j)*n+i]=q-1
    return M


def direct_product(input_graphs,output_graphs,q=65537):
    def acc(gs):
        S=None
        for g in gs:
            mat=exact_green(g,q)
            S=mat if S is None else mat_add(S,mat,q)
        return S
    return mat_mul(acc(output_graphs),acc(input_graphs),q)


def rank_identity(input_graphs,output_graphs,q=65537):
    n=len(input_graphs[0].pi)
    F=fourier_mod(n,q)
    H=block_matrix(input_graphs,output_graphs,F,q)
    residual=mat_add(F, [[(-v)%q for v in row]
                             for row in direct_product(input_graphs,output_graphs,q)],q)
    raw=rank_mod(H,q)
    res=rank_mod(residual,q)
    assert raw==(len(input_graphs)+len(output_graphs))*n+res
    return {'N':n,'r_input':len(input_graphs),'r_output':len(output_graphs),
            'lifted_dimension':len(H),'rank_H':raw,
            'rank_residual':res,
            'base_rank':(len(input_graphs)+len(output_graphs))*n,
            'factorization_success':res==0}

if __name__=='__main__':
    import json
    from random import Random
    from cut_capacity import random_green
    for n,r,s in ((4,2,2),(8,2,3),(8,3,2)):
        rng=Random(n*100+r*10+s)
        input_=[random_green(n,rng,zero_prob=.1) for _ in range(r)]
        output=[random_green(n,rng,zero_prob=.1) for _ in range(s)]
        print(json.dumps(rank_identity(input_,output)))
