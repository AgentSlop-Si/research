"""Phase 27: exact affine-reference rank gap for Hamiltonian Green cycles.

Fully independent of FFT numerical approximations. A successor list p represents
P e_j=e_{p(j)}. Algorithms run in O(N * #affine_refs) for exact certification.
No general-FFT complexity claim.
"""
from __future__ import annotations
import math
import random
from dataclasses import dataclass

MOD=998244353


def successor(order:list[int])->list[int]:
    n=len(order)
    if sorted(order)!=list(range(n)):
        raise ValueError('not a permutation')
    succ=[0]*n
    for t,j in enumerate(order):succ[j]=order[(t+1)%n]
    return succ


def cycle_count(p:list[int])->int:
    n=len(p)
    if sorted(p)!=list(range(n)):raise ValueError('not permutation')
    seen=bytearray(n);count=0
    for j in range(n):
        if not seen[j]:
            count+=1
            k=j
            while not seen[k]:
                seen[k]=1;k=p[k]
    return count


def permutation_rank_difference(p:list[int],q:list[int])->int:
    """Rank(P-Q)=n-cycles(Q^-1 P), in any characteristic."""
    n=len(p)
    if len(q)!=n:raise ValueError('size mismatch')
    inv=[0]*n
    for j,k in enumerate(q):inv[k]=j
    rel=[inv[k] for k in p]
    return n-cycle_count(rel)


def shift_successor(n:int)->list[int]:
    return [(j+1)%n for j in range(n)]


def conjugate_by_transposition(n:int,a:int,b:int)->list[int]:
    """W=tau Z tau^-1; an N-cycle that can be non-affine but rank-close."""
    if not(0<=a<b<n):raise ValueError('invalid swap')
    tau=list(range(n));tau[a],tau[b]=tau[b],tau[a]
    z=shift_successor(n)
    return [tau[z[tau[j]]] for j in range(n)]


def random_hamiltonian(n:int,seed:int)->list[int]:
    rng=random.Random(seed)
    order=list(range(n));rng.shuffle(order)
    p=[0]*n
    for j,k in enumerate(order):p[k]=order[(j+1)%n]
    return p


def affine_rank_audit(p:list[int],limit:int|None=None)->dict:
    """Exact minimum rank against all affine maps j -> u*j+b mod n.

    For power-of-two n, units are odd. Optional limit is only for debugging,
    never to claim all-affine coverage.
    """
    n=len(p)
    if n<4 or n&(n-1):raise ValueError('power of two n >= 4 needed')
    best=n+1;witness=None;considered=0
    for u in range(1,n,2):
        inverse=pow(u,-1,n)
        for b in range(n):
            # calculate cycle count without constructing P or dense matrices
            seen=bytearray(n)
            cycles=0
            for j in range(n):
                if not seen[j]:
                    cycles+=1
                    k=j
                    while not seen[k]:
                        seen[k]=1
                        k=inverse*(p[k]-b)%n
            rank=n-cycles
            considered+=1
            if rank<best:
                best=rank;witness=(u,b,cycles)
            if limit is not None and considered>=limit:
                return {'n':n,'min_rank':best,'closest_affine':witness,'checked':considered,
                        'exhaustive':False}
    return {'n':n,'min_rank':best,'closest_affine':witness,'checked':considered,
            'exhaustive':True}


def high_probability_threshold(n:int)->dict:
    """Uniform random N-cycle: failure at most n*|AGL|*(n+1)*2^-t.
    Take t=6 log_2 n (integer for power-of-two sizes): failure <= 1/n^2.
    """
    if n<4 or n&(n-1):raise ValueError('power of two n >= 4 needed')
    lg=n.bit_length()-1
    t=6*lg
    affine_count=n*n//2
    numerator=n*affine_count*(n+1)
    denominator=2**t
    assert numerator*n*n<=denominator or t>=n
    return {'t':t,'rank_at_least':max(0,n-t),
            'failure_bound_numerator':numerator,
            'failure_bound_denominator':denominator,
            'affine_count':affine_count}


def mod_rank(a:list[list[int]],p:int=MOD)->int:
    if not a:return 0
    mat=[row.copy() for row in a]
    nr=len(mat);nc=len(mat[0]);rank=0
    for col in range(nc):
        pivot=next((i for i in range(rank,nr) if mat[i][col]%p),None)
        if pivot is None:continue
        mat[rank],mat[pivot]=mat[pivot],mat[rank]
        inv=pow(mat[rank][col]%p,-1,p)
        for j in range(col,nc):mat[rank][j]=mat[rank][j]*inv%p
        for i in range(rank+1,nr):
            v=mat[i][col]%p
            if v:
                for j in range(col,nc):mat[i][j]=(mat[i][j]-v*mat[rank][j])%p
        rank+=1
        if rank==nr:break
    return rank


def direct_green(succ:list[int],alpha:int,p:int=MOD)->list[list[int]]:
    """Exact rational cyclic Green resolvent entries over prime field."""
    n=len(succ);alpha%=p
    den=1-pow(alpha,n,p)
    if den%p==0:raise ZeroDivisionError('resonant')
    invden=pow(den%p,-1,p)
    matrix=[[0]*n for _ in range(n)]
    # (I-alpha W)^-1= (I+alpha W+...+alpha^{n-1}W^{n-1})/(1-alpha^n)
    for col in range(n):
        j=col;a=invden
        for _ in range(n):
            matrix[j][col]=a
            j=succ[j]
            a=a*alpha%p
    return matrix


def mod_difference_rank_green(succ:list[int],affine:list[int],alpha:int,p:int=MOD)->int:
    G1=direct_green(succ,alpha,p)
    G2=direct_green(affine,alpha,p)
    return mod_rank([[(a-b)%p for a,b in zip(r1,r2)] for r1,r2 in zip(G1,G2)],p)


def conjugate_zero_by_histogram(p:list[int],a:int,b:int)->bool:
    """Exactly decide whether (F P F^-1)[a,b] = 0 over complex field.

    For N=2^m, Phi_N(z) = z^(N/2)+1, so a root sum vanishes
    exactly when the two halves of the exponent histogram coincide.
    """
    n=len(p)
    if n<4 or n&(n-1):raise ValueError('power of two n>=4')
    counts=[0]*n
    for j,k in enumerate(p):
        counts[(a*k-b*j)%n]+=1
    return all(counts[r]==counts[r+n//2] for r in range(n//2))


def cyclotomic_zero_density(p:list[int])->dict:
    n=len(p)
    zeros=0
    for a in range(n):
        for b in range(n):
            zeros+=conjugate_zero_by_histogram(p,a,b)
    return {'n':n,'zeros':zeros,'nonzeros':n*n-zeros,
            'fraction_nonzero':(n*n-zeros)/(n*n)}


if __name__=='__main__':
    for n in (32,64,128,256):
        w=random_hamiltonian(n,seed=2700+n)
        print('random',affine_rank_audit(w),'high_prob',high_probability_threshold(n)['rank_at_least'])
        close=conjugate_by_transposition(n,0,n//4+1)
        print('near_affine',n,permutation_rank_difference(close,shift_successor(n)))
    for n in (16,32,64):
        w=random_hamiltonian(n,seed=2700+n)
        print('Fourier conjugation zeros',cyclotomic_zero_density(w))
