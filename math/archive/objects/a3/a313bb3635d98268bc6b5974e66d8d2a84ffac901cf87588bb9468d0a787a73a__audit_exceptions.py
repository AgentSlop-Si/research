#!/usr/bin/env python3
"""Fresh standard-library verification of isolated certificate data."""
import json,math
from pathlib import Path
D=Path(__file__).parent
src=json.load(open('overlap_cluster_extension_0406/EXCEPTION_CERTIFICATES.json'))
original=json.load(open('diagonal_chirp_classification_0246/MODULAR_CERTIFICATES.json'))
if isinstance(original,dict):
    print('original keys',list(original))
    original=original.get('certificates',original.get('results',[]))
byN={a['N']:a for a in original}
def trim(a):
    while a and a[-1]==0:a.pop()
    return a
def add(a,b,p):return trim([((a[j] if j<len(a) else 0)+(b[j] if j<len(b) else 0))%p for j in range(max(len(a),len(b)))])
def mul(a,b,p):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
    return trim(c)
def remainder(a,b,p):
    a=trim(a[:]);ib=pow(b[-1],-1,p)
    while len(a)>=len(b):
        j=len(a)-len(b);c=a[-1]*ib%p
        for k,v in enumerate(b):a[j+k]=(a[j+k]-c*v)%p
        trim(a)
    return a
def gcd(a,b,p):
    while b:a,b=b,remainder(a,b,p)
    return [(v*pow(a[-1],-1,p))%p for v in a]
def ev(a,x,p):
    out=0
    for c in reversed(a):out=(out*x+c)%p
    return out
results=[]
for c in src:
    N=c['N'];p=c['prime_p'];q=c['primitive_q'];n=(N-1)//2
    assert all(p%i for i in range(2,math.isqrt(p)+1))
    order=1;t=q%p
    while t!=1:t=t*q%p;order+=1;assert order<=p-1
    assert order==N
    a=[1]
    for k in range(1,n+1):a=[1]+[(a[j]+pow(q,k-j,p)*a[j-1])%p for j in range(1,k)]+[1]
    T=[v*(-1)**(n+j)%p for j,v in enumerate(a)]
    assert T==c['T']
    deriv=[(j*T[j])%p for j in range(1,len(T))]
    bez=add(mul(c['squarefree_bezout_u'],T,p),mul(c['squarefree_bezout_v'],deriv,p),p)
    assert bez==[1]
    assert gcd(T,deriv,p)==[1]
    assert all(ev(T,pow(q,j,p),p) for j in range(N))
    assert c==byN[N]
    results.append(dict(N=N,degree=n,field_prime=p,root=q,prime_verified=True,exact_order_verified=True,coefficients_rebuilt=True,full_bezout_verified=True,derivative_gcd_one=True,all_cycle_nodes_nonzero=True,equals_original_certificate=True))
    print('PASS',N,flush=True)
(D/'EXCEPTION_CHECKS.json').write_text(json.dumps(results,indent=2)+'\n')
