#!/usr/bin/env python3
"""Hero #0 Phase 7: exact rank-adaptive, full-phase Green/polyphase fusion.

Input Q=K*M, K>=M, radix-2 K,M. Chirp-dechirp KxM input matrix and
find a certified exact row-rank factorization V = U@H (mod p).

All M Fourier phase modes may be nonzero. The execution combines r length-K
NTTs and K length-M NTTs (small M), giving O(N*(r+log M)) under log K=O(M).

Mathematical family only: fresh generic inputs almost surely have rank M and
are not accelerated. Mode detector uses zero tests and divisions of input-
dependent quantities; this is a branching algebraic-RAM algorithm and must
NOT be equated with the restricted scalar linear circuit model.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from math import gcd
from typing import Optional
import random
from phase6_exact import P, G, root_of_unity, ntt, independent_full_dft, hankel_rank


@dataclass
class Counter:
    adds: int = 0
    multiplies: int = 0
    inversions: int = 0
    inverse_modular_multiplication_bound: int = 0
    root_multiplications: int = 0
    ntt_butterflies: int = 0
    input_scanned: int = 0
    pivot_comparisons: int = 0
    def basic_field_ops(self):
        return (self.adds + self.multiplies +
                self.inverse_modular_multiplication_bound)
    def to_dict(self): return vars(self).copy()


def mul(a,b,c:Optional[Counter]):
    if c is not None:c.multiplies+=1
    return a*b % P

def add(a,b,c:Optional[Counter]):
    if c is not None:c.adds+=1
    return (a+b)%P

def inv(a,c:Optional[Counter]):
    if a%P==0:raise ZeroDivisionError
    # Exponentiation by squaring can be bounded by 2*bitlength(P).
    if c is not None:
        c.inversions+=1
        c.inverse_modular_multiplication_bound +=2*P.bit_length()
    return pow(a,P-2,P)


def root_table(n:int,omega:int,c:Optional[Counter]):
    t=[1]*n
    for i in range(1,n):
        t[i]=mul(t[i-1],omega,c)
        if c is not None:c.root_multiplications+=1
    return t


def ntt_charged(values:list[int],root:int,c:Optional[Counter]):
    """Radix-2 transform; charged butterflies and powers/preparation."""
    n=len(values)
    if n<1 or n & (n-1):raise ValueError('radix2 required')
    data=values.copy()
    j=0
    for i in range(1,n):
        bit=n>>1
        while j&bit:
            j^=bit;bit>>=1
        j^=bit
        if i<j:data[i],data[j]=data[j],data[i]
    length=2
    while length<=n:
        phase=pow(root,n//length,P)
        # root powers computed by modular exponentiation: <= 2 log p field mults
        if c is not None:c.multiplies += 2*P.bit_length()
        for offset in range(0,n,length):
            w=1
            for j in range(length//2):
                v=mul(data[offset+j+length//2],w,c)
                u=data[offset+j]
                data[offset+j]=add(u,v,c)
                data[offset+j+length//2]=add(u,-v,c)
                w=mul(w,phase,c)
                if c is not None:c.ntt_butterflies+=1
        length*=2
    return data


def chirp_phase(q,m,a,beta,b,t,table):
    return table[(a*(t*(t-1)//2)+(a*m*b+beta)*t)%q]


def dechirp(x,m,a,beta,table,c:Optional[Counter]):
    q=len(x);k=q//m
    for b in range(k):
        row=[]
        for t in range(m):
            row.append(mul(x[b*m+t],chirp_phase(q,m,a,beta,b,t,table),c))
            if c is not None:c.input_scanned+=1
        yield row


def factor_exact(rows,k:int,m:int,rmax:int,c:Optional[Counter]):
    """Incrementally certify KxM rank <=rmax. No pre-supplied factors.

    Returns (U,H) where U is Kxr and H rxM, or (None,None) at first
    witnessed rank>rmax. Each of K rows reduced against <=rmax pivots,
    for total O(rmax*K*M + rmax*M^2) algebraic work. For K>=M,
    rmax<=M, this is O((rmax+1)*K*M).
    """
    if not 0<=rmax<=m:raise ValueError('rank threshold')
    pivots=[];basis=[];coeffs=[]
    for row in rows:
        residual=row[:]
        alpha=[]
        for pivot,h in zip(pivots,basis):
            coeff=residual[pivot]
            alpha.append(coeff)
            if coeff:
                for t in range(m):
                    residual[t]=add(residual[t],-mul(coeff,h[t],c),c)
        new_pivot=next((i for i,z in enumerate(residual) if z),None)
        if c is not None:c.pivot_comparisons+=m
        if new_pivot is not None:
            if len(basis)>=rmax:
                return None,None
            p=residual[new_pivot]
            inv_p=inv(p,c)
            new_h=[mul(z,inv_p,c) for z in residual]
            if new_h[new_pivot]!=1:raise AssertionError('bad normalization')
            for old in coeffs:old.append(0)
            basis.append(new_h)
            pivots.append(new_pivot)
            alpha.append(p)
        coeffs.append(alpha)
    if len(coeffs)!=k:raise AssertionError('bad row stream')
    return coeffs,basis


def exact_green_rank_fused(x:list[int],m:int,rmax:int,a:int=1,beta:int=0,
                           counter:Optional[Counter]=None, return_factors:bool=False,
                           shifts:Optional[list[int]]=None):
    q=len(x)
    if q%m:raise ValueError('invalid length')
    k=q//m
    if q%2 or (k&(k-1)) or (m&(m-1)) or k<m:
        raise ValueError('Q even, K,M radix2, K>=M')
    if gcd(a,q)!=1:raise ValueError('non-unit chirp slope')
    c=counter if counter is not None else Counter()
    w=root_of_unity(q)
    tab=root_table(q,w,c)
    g=[0]*m if shifts is None else [int(v)%k for v in shifts]
    if len(g)!=m:raise ValueError("shift schedule must have M elements")
    # A distinct index translation in each column. This uses exactly N
    # addressed writes, charged to the input scan and O(N) memory.
    shifted=[[0]*m for _ in range(k)]
    for b,row in enumerate(dechirp(x,m,a,beta,tab,c)):
        for t,v in enumerate(row):shifted[(b+g[t])%k][t]=v
    U,H=factor_exact(shifted,k,m,rmax,c)
    if U is None:
        return (None,None,c) if return_factors else (None,c)
    result=fused_core(U,H,k,m,a,beta,g,tab,c)
    if return_factors:return result,(U,H),c
    return result,c


def fused_core(U,H,k,m,a,beta,g,tab,c:Optional[Counter]):
    """Compute F_Qx from verified sheared factor W(q,t)=sum_i U(q,i)H(i,t)."""
    q=k*m
    r=len(H)
    if r==0:return [0]*q
    wk_neg=tab[(-m)%q]
    G_channels=[]
    for i in range(r):
        G_channels.append(ntt_charged([U[b][i] for b in range(k)],wk_neg,c))
    wm_neg=tab[(-k)%q]
    result=[0]*q
    for ell in range(k):
        h=[]
        for t in range(m):
            v=0
            sample=(ell+a*t)%k
            for i in range(r):
                v=add(v,mul(H[i][t],G_channels[i][sample],c),c)
            phase=tab[(-(a*(t*(t-1)//2)+(beta+ell)*t) + m*sample*g[t])%q]
            h.append(mul(phase,v,c))
        z=ntt_charged(h,wm_neg,c)
        for j in range(m):result[ell+j*k]=z[j]
    return result


def sample_dechirped_rank(k:int,m:int,rank:int,seed:int,
                          a:int=1,beta:int=0,dense:bool=True,
                          shifts:Optional[list[int]]=None):
    """Synthesizes fresh full-length vectors with prescribed dechirped rank.

    Generates U @ H, then unchirps; random field factors. Unless rank=0,
    its original input typically has all coordinates and phase modes nonzero.
    """
    if rank>min(k,m):raise ValueError('rank too large')
    rng=random.Random(seed)
    q=k*m;w=root_of_unity(q)
    tab=root_table(q,w,None)
    U=[[rng.randrange(1,P) for _ in range(rank)] for _ in range(k)]
    H=[[rng.randrange(1,P) for _ in range(m)] for _ in range(rank)]
    g=[0]*m if shifts is None else [int(z)%k for z in shifts]
    if len(g)!=m:raise ValueError("shift schedule must have M elements")
    x=[]
    for b in range(k):
        for t in range(m):
            bb=(b+g[t])%k
            v=sum(U[bb][i]*H[i][t] for i in range(rank))%P
            ph=chirp_phase(q,m,a,beta,b,t,tab)
            x.append(v*pow(ph,P-2,P)%P)
    return x,U,H


def count_phase_modes(x:list[int],m:int,a:int=1,beta:int=0):
    q=len(x);k=q//m;tab=root_table(q,root_of_unity(q),None)
    wm=tab[k]
    support=set()
    for row in dechirp(x,m,a,beta,tab,None):
        transformed=ntt(row,wm)
        support.update(i for i,z in enumerate(transformed) if z)
    return len(support)


if __name__=='__main__':
    k,m,r=64,8,2
    x,_,_=sample_dechirped_rank(k,m,r,seed=7)
    y,(U,H),c=exact_green_rank_fused(x,m,r,return_factors=True)
    print('N',len(x),'rank',len(H),'all modes',count_phase_modes(x,m),
          'correct',y==independent_full_dft(x),
          'ops/N',round(c.basic_field_ops()/len(x),3))
