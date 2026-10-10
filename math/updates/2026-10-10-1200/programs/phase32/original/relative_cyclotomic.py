"""Hero #1 Phase 32: relative cyclotomic Fourier cut-rank certificates.

Mathematics: E=Q(zeta_d) <= K=Q(zeta_n), H=Gal(K/E).
A trace-zero E-linear functional L_b(t)=Tr_{K/E}(bt) is applied to
F_n[j,k]=zeta_n^(jk). Generic relative rank is n-c_H; c_H counts
H-orbits on the indices. A modular nonzero minor gives a rigorous
characteristic-zero LOWER bound. The orbit argument is the UPPER bound.

Exact finite-field checks use a homomorphism Z[zeta_n] -> F_p,
zeta_n |-> primitive nth root. They are not a proof of novel priority.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import product
from math import gcd,isqrt,prod
import hashlib,json,random
import numpy as np

P1,GEN1=2013265921,31
P2,GEN2=754974721,11
FIELDS=((P1,GEN1),(P2,GEN2))

def factor(n):
    if n<1: raise ValueError('positive integer required')
    q=n; out=[]
    for p in range(2,isqrt(q)+1):
        if p*p>q:break
        if q%p:continue
        a=0
        while q%p==0:q//=p;a+=1
        out.append((p,a))
    if q>1:out.append((q,1))
    return out

def divisors(n):
    ds=[1]
    for p,a in factor(n):
        ds=[d*(p**j) for d in ds for j in range(a+1)]
    return sorted(ds)

def phi(n):
    k=n
    for p,a in factor(n): k=k//p*(p-1)
    return k

def unit_subgroup(n,d):
    if n<1 or d<1 or n%d:raise ValueError('d must divide n')
    if n==1:return [0]
    return [a for a in range(n) if gcd(a,n)==1 and (a-1)%d==0]

def H_orbits(n,H):
    remaining=set(range(n));result=[]
    while remaining:
        k=min(remaining)
        orb=sorted({(k*a)%n for a in H}) if n>1 else [0]
        assert set(orb)<=remaining
        remaining.difference_update(orb)
        result.append(orb)
    return result

def orbit_count_closed(n,d):
    """c_d(n) = sum_{m|n} phi(gcd(m,d))."""
    return sum(phi(gcd(m,d)) for m in divisors(n))

def orbit_count_burnside(n,H):
    return sum(gcd((a-1)%n,n) for a in H)//len(H) if n>1 else 1

def order_root(n,p,gen):
    if (p-1)%n:raise ValueError('n must divide p-1')
    z=pow(gen,(p-1)//n,p)
    assert pow(z,n,p)==1
    assert all(pow(z,n//q,p)!=1 for q,a in factor(n))
    return z

def root_powers(n,p,gen):
    w=order_root(n,p,gen)
    out=[1]*n
    for i in range(1,n):out[i]=out[i-1]*w%p
    return out

def rank_pivots(matrix,p):
    """Return modular rank and original pivot row/column ids; no numerical rank guess."""
    a=np.asarray(matrix,dtype=np.int64).copy()%p
    m,n=a.shape
    row_ids=list(range(m));p_rows=[];p_cols=[];r=0
    for col in range(n):
        if r==m:break
        nz=np.flatnonzero(a[r:,col])
        if not len(nz):continue
        j=r+int(nz[0])
        if j!=r:
            a[[r,j]]=a[[j,r]]
            row_ids[r],row_ids[j]=row_ids[j],row_ids[r]
        inv=pow(int(a[r,col]),-1,p)
        a[r,col:]=(a[r,col:]*inv)%p
        nz=np.flatnonzero(a[r+1:,col])+r+1
        if len(nz):
            a[nz,col:]=(a[nz,col:]-a[nz,col,None]*a[r,col:])%p
        p_rows.append(row_ids[r]);p_cols.append(col)
        r+=1
    return r,p_rows,p_cols

def det_mod(matrix,p):
    a=np.asarray(matrix,dtype=np.int64).copy()%p
    n=len(a)
    if a.shape!=(n,n):raise ValueError('minor must be square')
    det=1
    for col in range(n):
        nz=np.flatnonzero(a[col:,col])
        if not len(nz):return 0
        j=col+int(nz[0]);
        if col!=j:
            a[[col,j]]=a[[j,col]]
            det=-det
        pivot=int(a[col,col])
        det=det*pivot%p
        if col+1<n:
            inv=pow(pivot,-1,p)
            mul=(a[col+1:,col]*inv)%p
            a[col+1:,col:]=(a[col+1:,col:]-mul[:,None]*a[col,col:])%p
    return int(det%p)

def polynomial_coeffs(n,d,attempt):
    seed=3200000+101*n+13*d+7919*attempt
    rng=random.Random(seed)
    return seed, [rng.randrange(-7,8) for _ in range(n)]

def relative_trace_samples(n,d,p,gen,coeffs):
    H=unit_subgroup(n,d)
    roots=root_powers(n,p,gen)
    if len(H)==1:return [0]*n
    za=[sum(c*roots[(a*t)%n] for t,c in enumerate(coeffs))%p for a in H]
    trace=sum(za)%p
    ba=[(len(H)*z-trace)%p for z in za]
    vals=[sum(b*roots[(a*k)%n] for a,b in zip(H,ba))%p for k in range(n)]
    assert vals[0]==0
    # E-invariant phases must be annihilated, regardless of the witness.
    assert all(vals[k]==0 for k in range(n) if all(((a-1)*k)%n==0 for a in H))
    return vals

def projected_matrix(n,vals,orders=None):
    """Cyclic matrix, or A=product C_ni with exponent n*sum(ki*xi/ni)."""
    if orders is None:
        return np.array([[vals[(i*j)%n] for j in range(n)] for i in range(n)],dtype=np.int64)
    points=list(product(*(range(v) for v in orders)))
    assert all(n%v==0 for v in orders)
    return np.array([[vals[sum((n//m)*a*b for m,a,b in zip(orders,i,j))%n]
                      for j in points] for i in points],dtype=np.int64)

def group_orbits(orders,H,n):
    points=set(product(*(range(v) for v in orders)));answer=[]
    while points:
        t=min(points)
        orbit=sorted({tuple((a*x)%m for x,m in zip(t,orders)) for a in H})
        assert set(orbit)<=points
        points.difference_update(orbit);answer.append(orbit)
    return answer

def sharp_witness(n,d,orders=None,attempt_limit=10):
    H=unit_subgroup(n,d)
    c=(len(H_orbits(n,H)) if orders is None else len(group_orbits(orders,H,n)))
    size=n if orders is None else prod(orders)
    need=size-c
    for attempt in range(attempt_limit):
        seed,coeffs=polynomial_coeffs(n,d,attempt)
        matrices=[];pivots=[];ranks=[]
        for p,gen in FIELDS:
            samples=relative_trace_samples(n,d,p,gen,coeffs)
            M=projected_matrix(n,samples,orders)
            rank,rows,cols=rank_pivots(M,p)
            ranks.append(rank);matrices.append(M);pivots.append((rows,cols))
        if all(rank==need for rank in ranks):
            rows,cols=pivots[0]
            minors=[]
            for (p,gen),M in zip(FIELDS,matrices):
                minors.append(det_mod(M[np.ix_(rows,cols)],p))
            if not all(minors):continue
            return dict(n=n,d=d,group=orders or [n],h_size=len(H),orbit_count=c,
                        predicted_rank=need,modular_ranks=ranks,pivot_minor_dets=minors,
                        pivot_rows=rows,pivot_cols=cols,coefficient_seed=seed,
                        witness_attempt=attempt,
                        polynomial_sha256=hashlib.sha256(json.dumps(coeffs,separators=(',',':')).encode()).hexdigest(),
                        fields=[p for p,gen in FIELDS],
                        note='minor nonzero mod both primes => rank >= predicted over characteristic 0; H-orbit proof gives upper bound')
    raise RuntimeError(f'No sufficient trace witness n={n} d={d} group={orders}')

def twiddle_relative_width(h,d):
    n=8*h
    assert n%d==0 and h>0 and (h&(h-1))==0
    H=unit_subgroup(n,d)
    live=[(u,q) for u in range(8) for q in range(h)
          if not all((a-1)*u*q%n==0 for a in H)]
    return 15*len(live),live
