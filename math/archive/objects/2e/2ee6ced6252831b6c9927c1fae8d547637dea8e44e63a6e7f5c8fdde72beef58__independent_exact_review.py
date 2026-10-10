#!/usr/bin/env python3
"""Independent exact review: subset Gaussian coefficients and multiplication determinants.
No author program is executed, imported, compiled or parsed. Certificate JSON is
read only AFTER independently reconstructing every mathematical value.
"""
from itertools import combinations
from math import gcd, comb
from functools import reduce
from pathlib import Path
import json, hashlib, time

BASE=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent

def trim(a):
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def exact_poly_quot(a,b):
    a=a[:]; q=[0]*max(1,len(a)-len(b)+1)
    while len(a)>=len(b) and any(a):
        e=len(a)-len(b); assert a[-1]%b[-1]==0
        v=a[-1]//b[-1]; q[e]=v
        for j,x in enumerate(b):a[e+j]-=v*x
        trim(a)
    assert not any(a)
    return trim(q)

PHI={}
def cyclotomic(s):
    if s not in PHI:
        a=[-1]+[0]*(s-1)+[1]
        for d in range(1,s):
            if s%d==0:a=exact_poly_quot(a,cyclotomic(d))
        PHI[s]=a
    return PHI[s]

class CyclotomicRing:
    def __init__(self,s):
        self.s=s;self.phi=cyclotomic(s);self.n=len(self.phi)-1
        self.zero=(0,)*self.n;self.one=(1,)+(0,)*(self.n-1)
        self.q=self.reduced([0,1]);self.powers=[self.one]
        for _ in range(s):self.powers.append(self.mul(self.powers[-1],self.q))
        assert self.powers[s]==self.one
    def reduced(self,a):
        a=list(a)
        for k in range(len(a)-1,self.n-1,-1):
            v=a[k]
            if v:
                for j,x in enumerate(self.phi[:-1]):a[k-self.n+j]-=v*x
        return tuple((a+[0]*self.n)[:self.n])
    def add(self,a,b):return tuple(x+y for x,y in zip(a,b))
    def neg(self,a):return tuple(-x for x in a)
    def sub(self,a,b):return tuple(x-y for x,y in zip(a,b))
    def scale(self,a,k):return tuple(x*k for x in a)
    def mul(self,a,b):
        c=[0]*(2*self.n-1)
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):
                    if y:c[i+j]+=x*y
        return self.reduced(c)
    def conj(self,a):
        c=self.zero
        for i,x in enumerate(a):
            if x:c=self.add(c,self.scale(self.powers[(-i)%self.s],x))
        return c
    def exactdiv(self,a,k):
        assert all(x%k==0 for x in a), (a,k)
        return tuple(x//k for x in a)

# Polynomials in z over the integral cyclotomic ring, in ascending order.
def zmul(a,b,R):
    c=[R.zero]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=R.add(c[i+j],R.mul(x,y))
    return c

def zmod(a,U,R):
    a=list(a);n=len(U)-1
    assert U[-1]==R.one
    for k in range(len(a)-1,n-1,-1):
        x=a[k]
        for j in range(n):a[k-n+j]=R.sub(a[k-n+j],R.mul(x,U[j]))
    return (a+[R.zero]*n)[:n]

def multiplication_matrix(a,U,R):
    n=len(U)-1
    cols=[zmod([R.zero]*j+a,U,R) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]

def determinant(M,R):
    """Faddeev-LeVerrier, with exact integral divisions only; no field inverse."""
    n=len(M)
    if n==0:return R.one
    B=[[R.one if i==j else R.zero for j in range(n)] for i in range(n)]
    for k in range(1,n+1):
        C=[[R.zero for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                x=R.zero
                for h in range(n):x=R.add(x,R.mul(M[i][h],B[h][j]))
                C[i][j]=x
        tr=R.zero
        for i in range(n):tr=R.add(tr,C[i][i])
        coefficient=R.exactdiv(R.neg(tr),k)
        for i in range(n):C[i][i]=R.add(C[i][i],coefficient)
        B=C
    # Cayley-Hamilton identity is an internal exact check.
    assert all(x==R.zero for row in B for x in row)
    return R.scale(coefficient,(-1)**n)

def result_at_U(a,U,R):
    return determinant(multiplication_matrix(a,U,R),R)

def content(a):return reduce(gcd,(abs(x) for x in a),0)

def gaussian_subset(n,k,R):
    # Enumerating k-subsets of {0,...,n-1}: q^(sum indices-k(k-1)/2).
    a=[0]*(k*(n-k)+1)
    for inds in combinations(range(n),k):a[sum(inds)-k*(k-1)//2]+=1
    assert sum(a)==comb(n,k)
    return R.reduced(a)

def compute(s):
    started=time.time();R=CyclotomicRing(s);b=(s-1)//2;r=(s-3)//4
    H=[gaussian_subset(b,k,R) for k in range(b+1)]
    U=[]
    for k in range(b):U.append(R.sub(H[k],U[-1] if k else R.zero))
    assert U[-1]==H[-1]==R.one and U==U[::-1]
    assert zmul(U,[R.one,R.one],R)==H
    g=R.zero
    for k,c in enumerate(U):g=R.add(g,R.scale(c,(-1)**k))
    v=R.one
    for e in list(range(2,2*r+1,2))+list(range(1,2*b,2)):
        v=R.mul(v,R.sub(R.one,R.powers[e]))
    delta=R.sub(R.scale(g,2),v)
    der=[R.scale(U[k],k) for k in range(1,len(U))]
    n=len(U)-1
    disc=R.scale(result_at_U(der,U,R),(-1)**(n*(n-1)//2))
    F=[R.one]+[R.zero]*(s-1)+[R.one]
    res=R.scale(result_at_U(F,U,R),(-1)**(s*n))
    Gamma=R.mul(disc,res);pair=R.mul(Gamma,R.conj(Gamma));aug=R.mul(pair,delta)
    fields=dict(U=U,g=g,v=v,delta=delta,disc_U=disc,res_F_U=res,Gamma=Gamma,Gamma_pair=pair,augmented=aug)
    assert R.add(R.mul(g,R.conj(v)),R.mul(R.conj(g),v))==R.mul(v,R.conj(v))
    # Independent coefficient-gcd witness: extended Bezout across all coordinates.
    def egcd(a,b):
        if b==0:return a,1,0
        g,x,y=egcd(b,a%b);return g,y,x-(a//b)*y
    coeffs=[0]*R.n;d=0
    for i,x in enumerate(aug):
        gg,aa,bb=egcd(d,x)
        coeffs=[aa*y for y in coeffs];coeffs[i]+=bb;d=gg
    if d<0:d=-d;coeffs=[-x for x in coeffs]
    assert sum(x*y for x,y in zip(coeffs,aug))==d==content(aug)
    # Certificate comparison starts only now; no JSON drives the reconstruction.
    path=OUT/'source'/f'EXACT_CONTENT_S{s}.json'
    if not path.exists():path=BASE/'augmented_content_followup'/f'EXACT_CONTENT_S{s}.json'
    source=json.loads(path.read_text())
    comparisons={k:json.loads(json.dumps(v))==source[k] for k,v in fields.items()}
    comparisons['phi_ascending']=R.phi==source['phi_ascending']
    contents={k:content(v) for k,v in fields.items() if k!='U'}
    comparisons['all_claimed_contents']=all(contents[k]==v for k,v in source['contents'].items())
    # Verify the supplied auxiliary P by expanding z^r P(z+z^-1),
    # without relying on that lower-degree representation for any determinant.
    recovered=[R.zero]*(2*r+1)
    for j,c in enumerate(source['P']):
        for h in range(j+1):
            e=r+j-2*h
            recovered[e]=R.add(recovered[e],R.scale(tuple(c),comb(j,h)))
    comparisons['P_expansion']=recovered==U
    assert all(comparisons.values()),comparisons
    expected={3:1,7:7**2,11:11**5,15:3**12*5**9,19:19**11}
    assert d==expected[s]
    result=dict(s=s,b=b,r=r,method='Subset Gaussian coefficients; direct degree-(b-1) multiplication matrices; Faddeev-LeVerrier determinants',
                elapsed_seconds=round(time.time()-started,4),phi_ascending=R.phi,
                independently_reconstructed=fields,contents=contents,
                augmented_gcd_bezout_coefficients=coeffs,
                augmented_content=d,certificate_comparison=comparisons,
                source_json_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                inverse_identity_verified=True,cayley_hamilton_checked=True)
    out=OUT/f'INDEPENDENT_EXACT_S{s}.json';out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'s':s,'augmented_content':d,'matches':all(comparisons.values()),'seconds':result['elapsed_seconds']}),flush=True)
    return result

if __name__=='__main__':
    import sys
    for s in map(int,sys.argv[1:] or ['3','7','11','15','19']):compute(s)
