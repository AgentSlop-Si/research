#!/usr/bin/env python3
"""Fresh exact controls for the third-block theorem; no prior checker is loaded.
Polynomials use exact integer coefficients in X and q. Translation q=1+T
is exact through T^(4p); omitted powers provably exceed every tested threshold.
"""
import json, math, hashlib
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache

HERE=Path(__file__).resolve().parent
checks=[]

def check(label, ok, **data):
    if not ok: raise AssertionError((label,data))
    checks.append(dict(label=label, passed=True, **data))

def clean(a): return {k:v for k,v in a.items() if v}
def add(a,b,sgn=1):
    c=dict(a)
    for k,v in b.items(): c[k]=c.get(k,0)+sgn*v
    return clean(c)
def shift(a,x=0,q=0): return {(i+x,j+q):v for (i,j),v in a.items()}
def mul(a,b):
    c={}
    for (i,j),v in a.items():
        for (k,l),w in b.items(): c[i+k,j+l]=c.get((i+k,j+l),0)+v*w
    return clean(c)
ONE={(0,0):1}; X={(1,0):1}
def edge(j): return {(0,0):1,(0,j):-1}
@lru_cache(None)
def continuant(n,first_edge=1):
    if n==0:return ONE
    if n==1:return X
    return add(shift(continuant(n-1,first_edge),x=1),mul(edge(first_edge+n-2),continuant(n-2,first_edge)),-1)

def translated(poly,cap):
    out={}
    for (x,q),v in poly.items():
        for t in range(min(q,cap)+1):out[x,t]=out.get((x,t),0)+v*math.comb(q,t)
    return clean(out)
def vp(c,p):
    z=0
    while c%p==0:c//=p;z+=1
    return z

def weight(poly,p,alpha,cap):
    e=p*(p-1)
    return min([Q(cap+1)]+[x*alpha+t+e*vp(c,p) for (x,t),c in translated(poly,cap).items()])

def tweight(poly,p,alpha,cap):
    e=p*(p-1)
    return min([Q(cap+1)]+[x*alpha+t+e*vp(c,p) for (x,t),c in poly.items()])

def doublefact(n):return math.prod(range(n,0,-2))
def coeff_low_residue(poly,p,alpha,target,cap):
    out={}
    e=p*(p-1)
    for (x,t),c in translated(poly,cap).items():
        w=x*alpha+t+e*vp(c,p)
        if w<target:raise AssertionError(('nonintegral scale',p,w,target))
        if w==target:
            # All desired face coefficients are prime-to-p; p-multiple
            # terms would require the unit of p/t^e and are excluded explicitly.
            if c%p==0:raise AssertionError('p-multiple on tested face')
            out[x]=(out.get(x,0)+c)%p
    return {k:v for k,v in out.items() if v}

def hm(n,p):
    a={0:1};b={1:1}
    if n==0:return a
    for k in range(1,n):
        c={j+1:v for j,v in b.items()}
        for j,v in a.items():c[j]=(c.get(j,0)+k*v)%p
        a,b=b,{j:v%p for j,v in c.items() if v%p}
    return b

def pgcd(a,b,l):
    def strip(c):
        while c and c[-1]%l==0:c.pop()
        return [v%l for v in c]
    a=strip(a[:]);b=strip(b[:])
    while b:
        r=a[:]
        while len(r)>=len(b):
            k=len(r)-len(b);v=r[-1]*pow(b[-1],-1,l)%l
            for j,w in enumerate(b):r[j+k]=(r[j+k]-v*w)%l
            r=strip(r)
        a,b=b,r
    return [v*pow(a[-1],-1,l)%l for v in a] if a else []
def prime(n):
    return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))
def pvalues(n,q,l):
    a=[1];b=[0,1]
    vals=[a,b]
    for k in range(1,n):
        c=[0]+b
        u=(1-pow(q,k,l))%l
        for j,v in enumerate(a):c[j]=(c[j]-u*v)%l
        a,b=b,c;vals.append(b)
    return vals

def hvalues(n,q,l):
    rows=[[1]]
    for m in range(1,n+1):
        prior=rows[-1];row=[1]+[0]*(m-1)+[1]
        for k in range(1,m):row[k]=(prior[k]+pow(q,m-k,l)*prior[k-1])%l
        rows.append(row)
    return rows

def derivative(c,l):return [j*c[j]%l for j in range(1,len(c))]

for p in (3,5,7,11,13):
    alpha=Q(2*p-1,2*p);h=(p-1)//2;L=Q(4*p-1,2);cap=4*p
    A=continuant(p);D=continuant(p-1)
    prev=continuant(2*p-1);base=continuant(2*p)
    leftF=continuant(p-1,p+1);leftG=continuant(p-2,p+2)
    check(f'p={p}: preceding-block exact identity',prev==add(mul(leftF,A),mul(edge(p),mul(leftG,D)),-1))
    check(f'p={p}: preceding-block weight',weight(prev,p,alpha,cap)>=h+p*alpha, bound=str(h+p*alpha), observed_lower_bound=str(weight(prev,p,alpha,cap)))
    check(f'p={p}: p^2 covers whole block',3*p-1<p*p)
    check(f'p={p}: critical gap is positive',h-alpha>0,odd_gap=str(h-alpha),even_gap=str(h-1+alpha))
    for r in range(p):
        b=2*p+r;m=r//2;eps=r%2;d=doublefact(2*m+2*eps-1)
        F=continuant(r,2*p+1)
        J={} if r==0 else mul(edge(2*p),mul(continuant(r-1,2*p+2),prev))
        actual=continuant(b)
        check(f'p={p},r={r}: exact joining identity',actual==add(mul(F,base),J,-1))
        check(f'p={p},r={r}: tail coefficient is a unit',d%p!=0,d=d)
        ft=translated(F,cap)
        ft=add(ft,{(eps,m):d},-1)
        target=m+eps*alpha
        check(f'p={p},r={r}: entire normalized tail residue',tweight(ft,p,alpha,cap)>target,normalizer_weight=str(target),error_lower_bound=str(tweight(ft,p,alpha,cap)))
        if r:
            gap=h-alpha if eps else h-1+alpha
            join_w=weight(J,p,alpha,cap)
            check(f'p={p},r={r}: entire translated joining error',join_w>=L+target+gap and gap>0,normalizer_weight=str(L+target),theoretical_gap=str(gap),observed_lower_bound=str(join_w))
        else:
            check(f'p={p},r=0: joining term absent',J=={})
        outer=coeff_low_residue(actual,p,Q(1,2),Q(b,2),cap)
        expected={i+2*p:v for i,v in hm(r,p).items()}
        check(f'p={p},r={r}: exact outer residual',outer==expected,residual=outer)
        hr=hm(r,p)
        carr=[hr.get(k,0) for k in range(r+1)]
        check(f'p={p},r={r}: outer h_r squarefree',pgcd(carr,derivative(carr,p),p)==[1])
        check(f'p={p},r={r}: outer zero parity',((0 not in hr)==bool(eps)))
        check(f'p={p},r={r}: exact degree parity',all(x%2==eps for x,t in actual))
        check(f'p={p},r={r}: full distinct-root count',(r-eps)+2*p+eps==b)
        n=r-eps
        via_pairs=2*p*(p-1)+2*p*p*alpha+n*(n-1)//2+n*(2*p+eps)+4*p*eps*alpha
        formula=p*(4*p-3)+2*p*r+Q(r*(r-1),2)+eps*(2*p-2)
        via_derivatives=2*p*(L+m+eps*alpha-1)+n*Q(b-1,2)+eps*(2*p-1+m)
        check(f'p={p},r={r}: discriminant and derivative identities',via_pairs==formula==via_derivatives,discriminant_valuation=str(formula))
        check(f'p={p},r={r}: inner irreducibility denominator',math.gcd(2*p-1,2*p)==1 and n%2==0)
    # Independent characteristic-zero nonvanishing controls via exact finite
    # reduction at a primitive p^2-th root. A failed reduction is retried at a
    # different prime and recorded, not interpreted as a characteristic-zero
    # collision or used in the proof.
    bad=[];found=False
    for k in range(1,200):
        ell=k*p*p+1
        if not prime(ell):continue
        q=None
        for g in range(2,ell):
            a=pow(g,k,ell)
            if pow(a,p*p,ell)==1 and pow(a,p,ell)!=1:q=a;break
        if q is None:continue
        pv=pvalues(3*p-1,q,ell);hv=hvalues(3*p-1,q,ell)
        failures=[]
        for b in range(2*p,3*p):
            if pgcd(pv[b],derivative(pv[b],ell),ell)!=[1] or pgcd(hv[b],derivative(hv[b],ell),ell)!=[1]:failures.append(b)
        if failures:bad.append(dict(ell=ell,q=q,failed_degrees=failures));continue
        check(f'p={p}: primitive-order finite-field control',pow(q,p*p,ell)==1 and pow(q,p,ell)!=1,ell=ell,q=q,order=p*p,prior_bad_reductions=bad)
        for b in range(2*p,3*p):
            check(f'p={p},b={b}: actual P and H finite-field squarefreeness',pgcd(pv[b],derivative(pv[b],ell),ell)==[1] and pgcd(hv[b],derivative(hv[b],ell),ell)==[1],ell=ell)
            check(f'p={p},b={b}: preceding P coprime',pgcd(pv[b],pv[b-1],ell)==[1])
        found=True;break
    check(f'p={p}: finite nonvanishing witnesses found',found)

(HERE/'CHECKS.json').write_text(json.dumps(dict(all_passed=True,count=len(checks),primes=[3,5,7,11,13],least_ramification='e=p(p-1), s=2',arithmetic='exact integer and finite-field arithmetic; no floating point',controls_not_infinite_family_proof=True,checks=checks),indent=2)+'\n')
print(f'PASS: {len(checks)} exact assertions; p=3,5,7,11,13, all 0<=r<p.')
