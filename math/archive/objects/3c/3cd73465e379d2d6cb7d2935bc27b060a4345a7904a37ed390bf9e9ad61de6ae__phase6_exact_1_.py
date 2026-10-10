#!/usr/bin/env python3
"""Hero #0 Phase 6: adaptive exact sparse global Green-phase support over NTT fields.

This is NOT an arbitrary-input sub-NlogN FFT. The O(rN) path certifies the
special class of inputs with at most r GLOBAL chirp-demodulated block modes.
Every field-operation including input inspection and support discovery counts.

Test fields: prime 2013265921, generator 31, Q | p-1, Q even, K and M powers of two.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import gcd
from typing import Optional

P=2013265921
G=31
INV2=(P+1)//2

@dataclass
class OpCounter:
    mult:int=0
    add:int=0
    roots:int=0
    ntt_butterflies:int=0
    input_checked:int=0
    full_block_dfts:int=0
    def as_dict(self): return vars(self).copy()


def pmul(a:int,b:int,c:Optional[OpCounter]=None)->int:
    if c is not None:c.mult+=1
    return (a*b)%P

def padd(a:int,b:int,c:Optional[OpCounter]=None)->int:
    if c is not None:c.add+=1
    return (a+b)%P


def root_of_unity(n:int):
    assert (P-1)%n==0
    w=pow(G,(P-1)//n,P)
    assert pow(w,n,P)==1
    remaining=n
    prime_factors=[]
    d=2
    while d*d<=remaining:
        if remaining%d==0:
            prime_factors.append(d)
            while remaining%d==0:remaining//=d
        d+=1
    if remaining>1:prime_factors.append(remaining)
    assert all(pow(w,n//d,P)!=1 for d in prime_factors)
    return w


def ntt(a:list[int],root:int,c:Optional[OpCounter]=None)->list[int]:
    n=len(a)
    if n<1 or n&(n-1):raise ValueError('radix 2 only')
    ar=a.copy()
    j=0
    for i in range(1,n):
        bit=n>>1
        while j&bit:
            j^=bit;bit>>=1
        j^=bit
        if i<j: ar[i],ar[j]=ar[j],ar[i]
    length=2
    while length<=n:
        wr=pow(root,n//length,P)
        if c is not None:c.roots+=1
        for b in range(0,n,length):
            w=1
            for j in range(length//2):
                u=ar[b+j];v=pmul(ar[b+j+length//2],w,c)
                ar[b+j]=padd(u,v,c)
                ar[b+j+length//2]=padd(u,-v,c)
                w=pmul(w,wr,c)
                if c is not None:c.ntt_butterflies+=1
        length*=2
    return ar


def root_power_table(q:int,w:int,c:Optional[OpCounter]=None)->list[int]:
    """Input-independent constants generated and CHARGED afresh in O(Q) field products."""
    tab=[1]*q
    for j in range(1,q):tab[j]=pmul(tab[j-1],w,c)
    return tab


def chirp_block_base(q:int,m:int,a:int,beta:int,w:int,b:int,
                     power_table:list[int]|None=None)->list[int]:
    tab=power_table
    return [(tab[(a*(t*(t-1)//2)+(a*m*b+beta)*t)%q]
             if tab is not None else pow(w,(a*(t*(t-1)//2)+(a*m*b+beta)*t)%q,P))
             for t in range(m)]


def full_local_modes(v:list[int],m:int,w_m:int,c:Optional[OpCounter]=None)->list[int]:
    """D_r=sum_t v_t*w_m^(r*t), i.e. positive-exponent transform."""
    if c is not None:c.full_block_dfts+=1
    return ntt(v,w_m,c)


def local_coefficients(v:list[int],chosen:list[int],w_m:int,c:Optional[OpCounter]=None,
                       power_table:list[int]|None=None, k:int|None=None,
                       inv_m:int|None=None)->tuple[list[int],bool]:
    """Compute the selected exact modes, then independently certify reconstruction.

    Orthogonality makes the certificate exact over finite fields.
    """
    m=len(v)
    if inv_m is None:inv_m=pow(m,P-2,P)
    wtab=[[(power_table[(k*r*t)%(k*m)] if power_table is not None else pow(w_m,r*t,P))
           for t in range(m)] for r in chosen]
    d=[]
    for row in wtab:
        acc=0
        for z,phase in zip(v,row):acc=padd(acc,pmul(z,phase,c),c)
        d.append(acc)
    for t in range(m):
        acc=0
        for ii,r in enumerate(chosen):
            ph=power_table[(k*(-r*t))%(k*m)] if power_table is not None else pow(w_m,(-r*t)%m,P)
            acc=padd(acc,pmul(d[ii],ph,c),c)
        got=pmul(acc,inv_m,c)
        if c is not None:c.input_checked+=1
        if got!=v[t]:return d,False
    return d,True


def green_decode_unnormalized(d:list[int],q:int,m:int,a:int,beta:int,w:int,
                               c:Optional[OpCounter]=None, power_table:list[int]|None=None)->list[int]:
    """One K-point NTT plus Q-length gauge/scan, no Q-point NTT.

    This follows the exact Green-cycle decoder in Phase 2, without sqrt(Q).
    """
    k=q//m
    if gcd(a,q)!=1 or q!=len(d)*m or q%2:raise ValueError('dimension/unit parity')
    tab=power_table if power_table is not None else root_power_table(q,w,c)
    w_k_inverse=tab[-m]
    dfft=ntt(d,w_k_inverse,c)
    tri_m=m*(m-1)//2
    indices=[];gauge=[];terms=[]
    for j in range(q):
        idx=(a*j)%q
        gj_exp=(a*(j*(j-1)//2)+beta*j)%q
        gj=tab[gj_exp]
        bexp=(-(m*(idx+beta)+a*tri_m))%q
        boundary=tab[bexp]
        forcing=padd(dfft[idx%k],-pmul(boundary,dfft[(idx+a*m)%k],c),c)
        term=pmul(forcing,tab[(-gj_exp)%q],c)
        indices.append(idx);gauge.append(gj);terms.append(term)
    seed=pmul(sum(terms)%P,INV2,c)
    prefix=0
    out=[0]*q
    for idx,gj,term in zip(indices,gauge,terms):
        out[idx]=pmul(gj,padd(seed,-prefix,c),c)
        prefix=padd(prefix,term,c)
    return out


def adaptive_green_sparse(x:list[int],m:int,rmax:int,a:int=1,beta:int=0,
                          counter:Optional[OpCounter]=None):
    """Exact detector + executor.

    On success returns exact *unnormalized* Q-DFT, global mode set, counter;
    on failure returns None, partial mode set, counter. No hidden fallback.
    """
    q=len(x);k=q//m
    if q%2 or q%m or k<m or (k&(k-1)) or (m&(m-1)):
        raise ValueError('Q even, K,M powers of two, K>=M required')
    if gcd(a,q)!=1:raise ValueError('a must be invertible mod Q')
    if rmax<0 or rmax>m:raise ValueError('0<=rmax<=M')
    c=counter or OpCounter()
    w=root_of_unity(q)
    tab=root_power_table(q,w,c)
    w_m=tab[k]
    inv_m=pow(m,P-2,P)
    support=[]
    d_by_r:dict[int,list[int]]={}
    for b in range(k):
        s0=chirp_block_base(q,m,a,beta,w,b,tab)
        v=[pmul(x[b*m+t],s0[t],c) for t in range(m)]
        d,ok=local_coefficients(v,support,w_m,c,tab,k,inv_m)
        if not ok:
            all_modes=full_local_modes(v,m,w_m,c)
            new=[r for r in range(m) if all_modes[r]!=0 and r not in support]
            if len(support)+len(new)>rmax:
                return None,support+new,c
            for r in new:d_by_r[r]=[0]*k
            support.extend(new)
            # complete exact modes obtained from the full small transform
            for r in support:d_by_r[r][b]=all_modes[r]
        else:
            for r,dr in zip(support,d): d_by_r[r][b]=dr
    if not support:
        return [0]*q,[],c
    output=[0]*q
    for r in support:
        row=green_decode_unnormalized(d_by_r[r],q,m,a,(beta+r*k)%q,w,c,tab)
        for j in range(q):output[j]=padd(output[j],row[j],c)
    return [pmul(z,inv_m,c) for z in output],support,c


def independent_full_dft(x:list[int]):
    q=len(x)
    return ntt(x,pow(root_of_unity(q),P-2,P))


def synth_sparse(k:int,m:int,support:list[int],seed:int,a:int=1,beta:int=0):
    import random
    rng=random.Random(seed)
    q=k*m;w=root_of_unity(q);wm=pow(w,k,P)
    arr=[]
    inv_m=pow(m,P-2,P)
    for b in range(k):
        s0=chirp_block_base(q,m,a,beta,w,b)
        ds={r:rng.randrange(1,P) for r in support}
        for t in range(m):
            v=sum(ds[r]*pow(wm,(-r*t)%m,P) for r in support)%P
            arr.append((v*inv_m*pow(s0[t],P-2,P))%P)
    return arr


def hankel_rank(x:list[int],height:int|None=None):
    n=len(x);rows=height or n//2;cols=n-rows+1
    mat=[[x[i+j] for j in range(cols)] for i in range(rows)]
    rank=0
    for j in range(cols):
        pivot=next((i for i in range(rank,rows) if mat[i][j]),None)
        if pivot is None:continue
        mat[rank],mat[pivot]=mat[pivot],mat[rank]
        inv=pow(mat[rank][j],P-2,P)
        for jj in range(j,cols):mat[rank][jj]=mat[rank][jj]*inv%P
        for ii in range(rank+1,rows):
            factor=mat[ii][j]
            if factor:
                for jj in range(j,cols):mat[ii][jj]=(mat[ii][jj]-factor*mat[rank][jj])%P
        rank+=1
        if rank==rows:break
    return rank

if __name__=='__main__':
    x=synth_sparse(32,8,[1,5],seed=1)
    y,found,c=adaptive_green_sparse(x,8,2)
    print('success',found,'correct',y==independent_full_dft(x),'ops',c.as_dict())
