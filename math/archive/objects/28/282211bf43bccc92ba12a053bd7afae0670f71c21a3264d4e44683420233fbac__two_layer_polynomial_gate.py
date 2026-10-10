"""Phase 13 starter: a correct exact algebraic gate for TWO Green-sum layers.

For A,B,C,D invertible weighted-permutation sparse matrices,
(A^-1+B^-1)(C^-1+D^-1)=F iff
A F D = (A+B)(C B)^(-1)(C+D).
Equivalently the 2N x 2N block polynomial matrix
   [ CB      C+D  ]
   [ A+B     AFD  ]
has rank N, provided CB is invertible.

This tests candidate factors, not a universal FFT algorithm. The appearance
of high-rank 3x3 minors in a product does not imply this gate is satisfied.
"""
from __future__ import annotations
import json,random,functools
from cycle_minor_gate import (permutation_cycles,green_perm_submatrix,
                              rank_mod)


def mm(A,B,q):
    n=len(A);k=len(B);m=len(B[0]);ans=[[0]*m for _ in range(n)]
    for i in range(n):
        for t in range(k):
            if A[i][t]:
                for j in range(m):ans[i][j]=(ans[i][j]+A[i][t]*B[t][j])%q
    return ans


def add(A,B,q):
    return [[(x+y)%q for x,y in zip(a,b)]for a,b in zip(A,B)]


def sub(A,B,q):
    return [[(x-y)%q for x,y in zip(a,b)]for a,b in zip(A,B)]


def sparse_inverse(pi,w,q):
    n=len(pi);M=[[int(i==j) for j in range(n)]for i in range(n)]
    for i,j in enumerate(pi):M[i][j]=(M[i][j]-w[i])%q
    return M


def cert(n=8,seed=213,q=65537):
    assert (q-1)%n==0
    root=pow(3,(q-1)//n,q)
    assert pow(root,n,q)==1 and (n<=2 or pow(root,n//2,q)!=1)
    rng=random.Random(seed)
    graph=[];greens=[];sparse=[]
    for _ in range(4):
        pi=list(range(n));rng.shuffle(pi)
        weights=[rng.randrange(q) for _ in range(n)]
        for cyc in permutation_cycles(pi):
            c=functools.reduce(lambda x,i:x*weights[i]%q,cyc,1)
            if c==1:weights[cyc[0]]=0
        graph.append((pi,weights))
        greens.append(green_perm_submatrix(pi,weights,list(range(n)),list(range(n)),q))
        sparse.append(sparse_inverse(pi,weights,q))
    G1,G2,G3,G4=greens
    A,B,C,D=sparse
    X=add(G1,G2,q);Y=add(G3,G4,q)
    F=[[pow(root,i*j,q) for j in range(n)]for i in range(n)]
    direct=sub(mm(X,Y,q),F,q)
    lhs=mm(mm(A,F,q),D,q)
    U=add(A,B,q);V=add(C,D,q)
    K=mm(C,B,q)
    rhs=mm(mm(mm(U,G2,q),G3,q),V,q)
    # A (F - X Y) D = lhs - rhs; the sign reverses direct.
    independent=mm(mm(A,direct,q),D,q)
    assert lhs==add(rhs,[[(-v)%q for v in row]for row in independent],q)
    block=[K[i]+V[i] for i in range(n)]+[U[i]+lhs[i] for i in range(n)]
    rank=rank_mod(block,q)
    mismatch=sum(v!=0 for row in direct for v in row)
    return {'n':n,'q':q,'seed':seed,'primitive_root':root,
            'full_transform_mismatch_count':mismatch,
            'block_polynomial_matrix_rank':rank,
            'factorization_success':mismatch==0,
            'block_rank_gate_passes':rank==n,
            'schur_equivalence_checked':True}

if __name__=='__main__':
    for n in [4,8,16]:print(json.dumps(cert(n),indent=2))
