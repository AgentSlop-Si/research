#!/usr/bin/env python3
"""Independent, standard-library exact F2[q] checks; imports no supplied research code."""
import json
from pathlib import Path


def degree(a): return a.bit_length()-1

def mul(a,b):
    c=0
    while b:
        if b&1: c^=a
        a<<=1; b>>=1
    return c

def divmod2(a,b):
    assert b
    q=0; db=degree(b)
    while degree(a)>=db:
        s=degree(a)-db; q^=1<<s; a^=b<<s
    return q,a

def exact(a,b):
    q,r=divmod2(a,b)
    assert r==0, (hex(a),hex(b),hex(r))
    return q

def power(a,n):
    b=1
    while n:
        if n&1: b=mul(b,a)
        a=mul(a,a); n//=2
    return b

def valuation(a,f):
    assert a
    v=0
    while True:
        q,r=divmod2(a,f)
        if r: return v
        v+=1; a=q

def trim(p):
    p=p[:]
    while len(p)>1 and not p[-1]: p.pop()
    return p

def padd(a,b):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a): c[i]^=x
    for i,x in enumerate(b): c[i]^=x
    return trim(c)

def pmul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]^=mul(x,y)
    return trim(c)

def pscale(a,s): return trim([mul(x,s) for x in a])

def ppow(a,n):
    b=[1]
    while n:
        if n&1:b=pmul(b,a)
        a=pmul(a,a); n//=2
    return b

def monic_remainder(a,b):
    assert b[-1]==1
    a=trim(a)
    while len(a)>=len(b) and a!=[0]:
        lead=a[-1]; shift=len(a)-len(b)
        for i,v in enumerate(b):a[i+shift]^=mul(lead,v)
        a=trim(a)
    return a

def resultant(a,b):
    a=trim(a); b=trim(b)
    da=len(a)-1; db=len(b)-1
    if da==0:return power(a[0],db)
    if db==0:return power(b[0],da)
    size=da+db
    M=[[0]*size for _ in range(size)]
    for j in range(db):
        for i,x in enumerate(reversed(a)):M[j][i+j]=x
    for j in range(da):
        for i,x in enumerate(reversed(b)):M[db+j][i+j]=x
    prior=1
    for k in range(size-1):
        pivot=next((i for i in range(k,size) if M[i][k]),None)
        if pivot is None:return 0
        M[k],M[pivot]=M[pivot],M[k]
        t=M[k][k]
        for i in range(k+1,size):
            for j in range(k+1,size):
                M[i][j]=exact(mul(t,M[i][j])^mul(M[i][k],M[k][j]),prior)
            M[i][k]=0
        prior=t
    return M[-1][-1]

def cyclotomic(n, cache={1:3}):
    if n not in cache:
        f=(1<<n)|1
        for d in range(1,n):
            if n%d==0:f=exact(f,cyclotomic(d))
        cache[n]=f
    return cache[n]

def trace_recurrence(m):
    prev=[1]; curr=[6,1]
    if m==0:return prev
    for j in range(2,m+1):
        a=(1<<(2*j-1))^(1<<(2*j))
        c=mul(1^(1<<(2*j-1)),1^(1<<(2*j-2)))
        prev,curr=curr,padd(pmul([a,1],curr),pscale(prev,c))
    return curr

def gaussian_h(n):
    row=[1]
    for j in range(1,n+1):
        nxt=[1]*(j+1)
        for k in range(1,j):nxt[k]=row[k]^(row[k-1]<<(j-k))
        row=nxt
    return row

def fold_reciprocal(u):
    """For symmetric degree 2m polynomial U, find P with U=z^m P(z+1/z)."""
    m=(len(u)-1)//2
    assert all(u[i]==u[-1-i] for i in range(len(u)))
    out=[0]*(m+1); work=u[:]
    for j in range(m,-1,-1):
        a=work[m+j]; out[j]=a
        # (z+z^-1)^j has binomial-parity coefficients.
        for k in range(j+1):
            if k&~j==0: work[m+j-2*k]^=a
    assert not any(work)
    return trim(out)

def gaussian_trace(m):
    h=gaussian_h(2*m+1); u=[]; previous=0
    for i in range(2*m+1):
        previous=h[i]^previous; u.append(previous)
    assert u[-1]==h[-1]
    return fold_reciprocal(u)

def cyc_trace(d):
    return fold_reciprocal([1]*d)

def total_extra(m):
    return sum(degree(cyclotomic(d))*(((d+1)//2)*(m//d)+m//(2*d))
               for d in range(3,m+1,2))

def phi(n): return degree(cyclotomic(n))

checks=0
rows=[]
for m in (1,2,3,4,12):
    p=trace_recurrence(m); assert p==gaussian_trace(m); checks+=1
    e=p[0]; r=resultant(p[::2],p[1::2]); q=mul(e,r)
    N=m*(m+1)*(2*m+1)//3; v=(m+1)//2
    kap=m+3*(m*m//4)+2*(m//4)
    assert degree(q)==N and valuation(q,2)==v; checks+=2
    low=1; local=[]
    for d in range(3,m+1,2):
        k=m//d; A=(2*m+1)//d; h=(d-1)//2
        ed=((d+1)//2)*k+k//2; rd=h*k+k//2; ph=cyclotomic(d)
        assert valuation(e,ph)>=k and valuation(r,ph)>=rd; checks+=2
        if m%d==0:assert valuation(e,ph)==k; checks+=1
        low=mul(low,power(ph,ed))
        forced=[0]*k+ppow(cyc_trace(d),A)
        residue=[divmod2(c,ph)[1] for c in monic_remainder(p,forced)]
        assert not any(residue); checks+=1
        local.append({'d':d,'k':k,'forced_E':k,'actual_E':valuation(e,ph),'forced_R':rd,'actual_R':valuation(r,ph),'forced_Q':ed})
    denominator=mul(mul(1<<v,power(3,kap)),low)
    qhat=exact(q,denominator)
    B=N-v-kap; delta=total_extra(m)
    assert degree(qhat)==B-delta; checks+=1
    # Independent negative controls: wrong divisor at sharp endpoint boundary.
    if m>=3:
        ph=cyclotomic(3)
        if m%3==0:assert divmod2(e,power(ph,m//3+1))[1]; checks+=1
    rows.append({'m':m,'N':N,'accepted_B':B,'extra_forced_degree':delta,'new_B':B-delta,'low_orders':local})
# A strict improvement to the inequality at an existing control, not a new support stage.
assert 17>2*3+1 and 13 < phi(17) <=17; checks+=1
result={'checks':checks,'controls':rows,'strict_filter_example':{'m':3,'d':17,'phi':phi(17),'old_B':17,'new_B':13},'scope':'Identity and forced-divisibility controls only; no paired-support census.'}
print(json.dumps(result,indent=2))
Path(__file__).with_name('RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
