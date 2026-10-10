#!/usr/bin/env python3
"""Hero #0 Phase7+: UNKNOWN column-wise cyclic shifts detected in O(N).

A dense KxM dechirped matrix of the form V[b,t]=h[t]*f[(b+g[t])%K]
can have ordinary rank M and all M nonzero Green modes, yet needs only ONE
length-K FFT and K length-M FFTs. The shifts g[t] and scalar h[t] are NOT
provided; they are recognized via cyclic support-gap/projective-ratio KMP
in O(KM), EVEN WHEN f HAS ZEROS.

The detector uses field operations, equality tests and one input-dependent
inversion via batch inversion. This is a branching algebraic-RAM model,
not a scalar linear-arithmetic circuit.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import gcd
from typing import Optional
from phase6_exact import P,root_of_unity
from phase7_rank_fusion import Counter,root_table,dechirp,fused_core,mul,inv


def ratio_eq(u,v,c:Optional[Counter]):
    """Projective ratio equality: a/b=c/d iff a*d=c*b (nonzero b,d)."""
    return mul(u[0],v[1],c)==mul(v[0],u[1],c)


def cyclic_ratio_shift(reference,query,c:Optional[Counter]):
    """Find a shift g with query[b]=lambda*reference[(b+g)%K].

    All entries nonzero. Apply KMP to cyclic adjacent-ratio tokens without
    computing ANY individual field inverses. KMP equality is cross product.
    Returns g in 0..K-1, or None if no proportional rotation exists.
    """
    k=len(reference)
    if k!=len(query):raise ValueError('unequal column sizes')
    if not k:return None
    if any(z==0 for z in reference) or any(z==0 for z in query):return None
    rt=[(reference[(j+1)%k],reference[j]) for j in range(k)]
    qt=[(query[(j+1)%k],query[j]) for j in range(k)]
    prefix=[0]*k
    t=0
    for i in range(1,k):
        while t>0 and not ratio_eq(qt[i],qt[t],c):t=prefix[t-1]
        if ratio_eq(qt[i],qt[t],c):t+=1
        prefix[i]=t
    t=0
    for i in range(2*k-1):
        z=rt[i%k]
        while t>0 and not ratio_eq(z,qt[t],c):t=prefix[t-1]
        if ratio_eq(z,qt[t],c):t+=1
        if t==k:
            g=i-k+1
            # guard important: equal ratios imply proportionality, but explicitly
            # verify an input equality certificate rather than just trust KMP.
            if all(mul(query[j],reference[g%k],c)==
                   mul(query[0],reference[(j+g)%k],c) for j in range(k)):
                return g
            t=prefix[t-1]
    return None


def cyclic_projective_shift(reference,query,c:Optional[Counter]):
    """Recognize a cyclic shift AND a nonzero global scalar, including zeros.

    Nonzero support sites form a cyclic graph. Label each successive support
    edge by (cyclic gap, next_value/current_value). These labels are invariant
    under global scale and transform by cyclic rotation under column shifts.
    Compare ratios WITHOUT division, using cross products. KMP on the
    nonzero-edge necklace runs in O(K) worst-case time including support scan.
    Returns a shift g with query[b]=h*reference[(b+g)%K], or None.

    A matching full necklace forces ONE scalar on every nonzero site, because
    successive ratios telescope. Gap labels also match the exact zero pattern.
    This fixes the obstruction of using adjacent ratios when there are zeros.
    """
    k=len(reference)
    if len(query)!=k:raise ValueError('length mismatch')
    pos_ref=[j for j,z in enumerate(reference) if z]
    pos_query=[j for j,z in enumerate(query) if z]
    if not pos_ref or len(pos_ref)!=len(pos_query):return None
    nr=len(pos_ref)
    def tokens(v,positions):
        n=len(positions)
        result=[]
        for j,i in enumerate(positions):
            nxt=positions[(j+1)%n]
            gap=(nxt-i)%k if n>1 else k
            result.append((gap,v[nxt],v[i]))
        return result
    text=tokens(reference,pos_ref)
    pattern=tokens(query,pos_query)
    def eq(u,v):
        return u[0]==v[0] and mul(u[1],v[2],c)==mul(v[1],u[2],c)
    prefix=[0]*nr
    t=0
    for j in range(1,nr):
        while t and not eq(pattern[j],pattern[t]):t=prefix[t-1]
        if eq(pattern[j],pattern[t]):t+=1
        prefix[j]=t
    t=0
    for j in range(2*nr-1):
        v=text[j%nr]
        while t and not eq(v,pattern[t]):t=prefix[t-1]
        if eq(v,pattern[t]):t+=1
        if t==nr:
            offset=j-nr+1
            shift=(pos_ref[offset]-pos_query[0])%k
            # Global proportionality follows from equal gap-and-ratio cycles;
            # independently certify via a single nonzero anchor.
            jq=pos_query[0]
            rf=reference[(jq+shift)%k]
            qv=query[jq]
            if all(mul(query[b],rf,c)==mul(qv,reference[(b+shift)%k],c)
                   for b in range(k)):
                return shift
            t=prefix[t-1]
    return None


def invert_many(values:list[int],c:Optional[Counter]):
    """One field inversion, O(M) multiplications (Montgomery trick)."""
    n=len(values)
    if not n:return []
    if any(z==0 for z in values):raise ZeroDivisionError
    prefix=[1]*(n+1)
    for i,z in enumerate(values):prefix[i+1]=mul(prefix[i],z,c)
    suffix_inv=inv(prefix[-1],c)
    result=[0]*n
    for i in range(n-1,-1,-1):
        result[i]=mul(prefix[i],suffix_inv,c)
        suffix_inv=mul(suffix_inv,values[i],c)
    return result


def infer_shift_rank1(v,k:int,m:int,c:Optional[Counter]):
    """Discover f,h,g for ANY rank1 shifted columns, zeros allowed.

    Find first nonzero column as projective reference. Each other column is
    a scaled cyclic shift; support gaps and neighboring nonzero ratios encode
    that entire orbit without divisions. Detect via KMP in O(KM), then recover
    every nonzero column scale with one total batch inversion.
    """
    anchor=next((t for t in range(m) if any(v[b][t] for b in range(k))),None)
    if anchor is None:return [],[0]*m,[0]*m
    f=[v[b][anchor] for b in range(k)]
    shifts=[0]*m
    active=[];anchors=[]
    for t in range(m):
        col=[v[b][t] for b in range(k)]
        if not any(col):continue
        g=cyclic_projective_shift(f,col,c)
        if g is None:return None
        shifts[t]=g
        active.append(t)
        anchors.append(next(b for b,z in enumerate(col) if z))
    inv_denoms=invert_many([f[(anchors[i]+shifts[t])%k]
                             for i,t in enumerate(active)],c)
    h=[0]*m
    for i,t in enumerate(active):h[t]=mul(v[anchors[i]][t],inv_denoms[i],c)
    for b in range(k):
        for t in range(m):
            if v[b][t]!=mul(h[t],f[(b+shifts[t])%k],c):return None
            if c is not None:c.input_scanned+=1
    return f,h,shifts


def unknown_shift_rank1_transform(x:list[int],m:int,a:int=1,beta:int=0,
                                   counter:Optional[Counter]=None,return_params=False):
    q=len(x)
    if q%m:raise ValueError('m must divide Q')
    k=q//m
    if q%2 or k<m or k&(k-1) or m&(m-1):raise ValueError('radix2; K>=M')
    if gcd(a,q)!=1:raise ValueError('nonunit chirp slope')
    c=counter if counter is not None else Counter()
    tab=root_table(q,root_of_unity(q),c)
    v=list(dechirp(x,m,a,beta,tab,c))
    certificate=infer_shift_rank1(v,k,m,c)
    if certificate is None:
        return (None,None,c) if return_params else (None,c)
    f,h,g=certificate
    if not f:
        result=[0]*q
    else:
        U=[[f[b]] for b in range(k)];H=[h]
        result=fused_core(U,H,k,m,a,beta,g,tab,c)
    return (result,(f,h,g),c) if return_params else (result,c)


if __name__=='__main__':
    from phase7_rank_fusion import sample_dechirped_rank,count_phase_modes
    from phase6_exact import independent_full_dft
    k,m=64,8
    g=[(3*t*t+5*t)%k for t in range(m)]
    x,_,_=sample_dechirped_rank(k,m,1,77,3,5,shifts=g)
    got,params,c=unknown_shift_rank1_transform(x,m,3,5,return_params=True)
    print('success',got is not None,'exact',got==independent_full_dft(x),
          'full-mode',count_phase_modes(x,m,3,5),
          'recovered g',params[2],
          'ops/N',round(c.basic_field_ops()/len(x),2),
          'inversions',c.inversions)
