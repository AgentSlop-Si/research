#!/usr/bin/env python3
"""Exact adaptive union of r unknown scaled-cyclic-shift column orbits.

For V[b,t]=h[t] f_{cluster[t]}[(b+g[t])%K], no templates, cluster,
scalars, or shifts need be provided. Search r distinct projective cyclic
orbits by support-gap KMP; O(r*N) detection and one batch inversion.
Then r long K-NTTs + K short M-NTTs, combining all r components before
any short transform: O(N*(r+loglog N)) when M=Theta(log N).

This still recognizes a lower-dimensional special family only.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import gcd
from typing import Optional
from phase6_exact import P,root_of_unity
from phase7_rank_fusion import Counter,root_table,dechirp,fused_core,mul
from phase7_hidden_shift_detector import cyclic_projective_shift,invert_many


def infer_orbit_union(v,k:int,m:int,rmax:int,c:Optional[Counter]):
    if rmax<0 or rmax>m:raise ValueError('rank threshold out of bounds')
    templates=[]
    groups=[-1]*m;shifts=[0]*m;anchors=[-1]*m
    for t in range(m):
        column=[v[b][t] for b in range(k)]
        first_nz=next((b for b,z in enumerate(column) if z),None)
        if first_nz is None:continue
        selected=None
        for i,f in enumerate(templates):
            g=cyclic_projective_shift(f,column,c)
            if g is not None:
                selected=i;shifts[t]=g;break
        if selected is None:
            if len(templates)>=rmax:return None
            selected=len(templates)
            templates.append(column)
            shifts[t]=0
        groups[t]=selected;anchors[t]=first_nz
    r=len(templates)
    nonzero=[t for t in range(m) if groups[t]>=0]
    invs=invert_many([templates[groups[t]][(anchors[t]+shifts[t])%k]
                       for t in nonzero],c)
    H=[[0]*m for _ in range(r)]
    for i,t in enumerate(nonzero):
        H[groups[t]][t]=mul(v[anchors[t]][t],invs[i],c)
    for b in range(k):
        for t in range(m):
            expected=(H[groups[t]][t]*templates[groups[t]][(b+shifts[t])%k])%P if groups[t]>=0 else 0
            if expected!=v[b][t]:return None
            if c is not None:c.input_scanned+=1
    U=[[templates[i][b] for i in range(r)] for b in range(k)]
    return U,H,shifts,groups


def orbit_union_transform(x:list[int],m:int,rmax:int,a:int=1,beta:int=0,
                          counter:Optional[Counter]=None,return_certificate:bool=False):
    q=len(x)
    if q%m:raise ValueError('M not divisor')
    k=q//m
    if q%2 or k<m or k&(k-1) or m&(m-1):raise ValueError('power2 K>=M')
    if gcd(a,q)!=1:raise ValueError('a nonunit')
    c=counter if counter is not None else Counter()
    tab=root_table(q,root_of_unity(q),c)
    V=list(dechirp(x,m,a,beta,tab,c))
    factors=infer_orbit_union(V,k,m,rmax,c)
    if factors is None:return (None,None,c) if return_certificate else (None,c)
    U,H,g,groups=factors
    result=fused_core(U,H,k,m,a,beta,g,tab,c)
    return (result,(U,H,g,groups),c) if return_certificate else (result,c)


def sample_orbit_union(k,m,r,seed,a:int=1,beta:int=0,zeros=False):
    """Synthesize arbitrary previously unknown templates, shifts and clusters."""
    import random
    rng=random.Random(seed)
    if r>m:raise ValueError
    q=k*m
    tab=root_table(q,root_of_unity(q),None)
    templates=[]
    for _ in range(r):
        f=[rng.randrange(1,P) for b in range(k)]
        if zeros:
            for b in rng.sample(range(k),k//3):f[b]=0
        templates.append(f)
    group=list(range(r))+[rng.randrange(r) for _ in range(m-r)] if r else [-1]*m
    rng.shuffle(group)
    shifts=[rng.randrange(k) for _ in range(m)]
    h=[rng.randrange(1,P) for _ in range(m)]
    x=[]
    for b in range(k):
        for t in range(m):
            v=h[t]*templates[group[t]][(b+shifts[t])%k]%P if r else 0
            exponent=(a*(t*(t-1)//2)+(a*m*b+beta)*t)%q
            x.append(v*tab[(-exponent)%q]%P)
    return x,templates,group,shifts,h

if __name__=='__main__':
    from phase6_exact import independent_full_dft
    k,m,r=64,8,3
    x,*_=sample_orbit_union(k,m,r,seed=58,a=3,beta=7,zeros=True)
    y,cert,c=orbit_union_transform(x,m,r,a=3,beta=7,return_certificate=True)
    print('PASS exact',y==independent_full_dft(x),'templates',len(cert[1]),
          'ops_per_n',round(c.basic_field_ops()/len(x),2),'inversions',c.inversions)
