#!/usr/bin/env python3
"""Fresh component test in finite fields. Does not import other research code.
Uses q-Pascal coefficients and polynomial Euclid, not discriminant determinants.
"""
from pathlib import Path
import json,sys,time
import sympy as sp

def trim(a):
    while a and a[-1]==0:a.pop()
    return a

def divmodp(a,b,p):
    a=trim(a[:]);b=trim(b[:]);q=[0]*max(0,len(a)-len(b)+1)
    il=pow(b[-1],-1,p)
    while len(a)>=len(b):
        i=len(a)-len(b);c=a[-1]*il%p;q[i]=c
        for j,x in enumerate(b):a[i+j]=(a[i+j]-c*x)%p
        trim(a)
    return trim(q),a

def psub(a,b,p):return trim([((a[i] if i<len(a) else 0)-(b[i] if i<len(b) else 0))%p for i in range(max(len(a),len(b)))])
def pmul(a,b,p):
    c=[0]*max(0,len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
    return trim(c)
class Field:
    def __init__(self,p,f):
        self.p=p;self.f=f;self.d=len(f)-1;self.zero=(0,)*self.d;self.one=self.e([1]);self.q=self.e([0,1])
    def e(self,a):
        a=list(a)
        for i in range(len(a)-1,self.d-1,-1):
            c=a[i]%self.p
            if c:
                for j in range(self.d):a[i-self.d+j]-=c*self.f[j]
        return tuple(x%self.p for x in (a+[0]*self.d)[:self.d])
    def add(self,a,b):return tuple((x+y)%self.p for x,y in zip(a,b))
    def sub(self,a,b):return tuple((x-y)%self.p for x,y in zip(a,b))
    def sc(self,a,n):return tuple(x*n%self.p for x in a)
    def mul(self,a,b):return self.e(pmul(a,b,self.p))
    def inv(self,a):
        oldr=self.f[:];r=trim(list(a));oldt=[];t=[1]
        while r:
            quo,newr=divmodp(oldr,r,self.p)
            oldr,r=r,newr;oldt,t=t,psub(oldt,pmul(quo,t,self.p),self.p)
        assert len(oldr)==1
        return self.e([x*pow(oldr[0],-1,self.p)%self.p for x in oldt])
    def power(self,a,n):
        out=self.one
        while n:
            if n&1:out=self.mul(out,a)
            a=self.mul(a,a);n//=2
        return out

def ztrim(F,a):
    while a and a[-1]==F.zero:a.pop()
    return a
def zmod(F,a,b):
    a=ztrim(F,a[:]);b=ztrim(F,b[:]);il=F.inv(b[-1])
    while len(a)>=len(b):
        i=len(a)-len(b);c=F.mul(a[-1],il)
        for j,x in enumerate(b):a[i+j]=F.sub(a[i+j],F.mul(c,x))
        ztrim(F,a)
    return a
def zgcd(F,a,b):
    a=ztrim(F,a[:]);b=ztrim(F,b[:])
    while b:a,b=b,zmod(F,a,b)
    return a

def construct(F,s,q):
    b=(s-1)//2;row=[F.one]
    powers=[F.power(q,i) for i in range(s)]
    for n in range(1,b+1):
        row=[F.one]+[F.add(row[k],F.mul(powers[n-k],row[k-1])) for k in range(1,n)]+[F.one]
    U=[row[0]]
    for k in range(1,b):U.append(F.sub(row[k],U[-1]))
    assert U[-1]==row[-1]
    g=F.zero
    for i,a in enumerate(U):g=F.add(g,F.sc(a,(-1)**i))
    v=F.one;r=(s-3)//4
    for e in list(range(2,2*r+1,2))+list(range(1,2*b,2)):v=F.mul(v,F.sub(F.one,powers[e]))
    delta=F.sub(F.sc(g,2),v)
    return U,delta

def guard(F,s,U):
    deriv=[F.sc(U[i],i) for i in range(1,len(U))]
    dd=len(zgcd(F,U,deriv))-1
    rr=len(zgcd(F,U,[F.one]+[F.zero]*(s-1)+[F.one]))-1
    return dd,rr

def test(s,p):
    x=sp.Symbol('x');phi=sp.Poly(sp.cyclotomic_poly(s,x),x,modulus=p)
    fs=sp.factor_list(phi)[1];rows=[]
    for f,e in fs:
        assert e==1
        co=[int(c)%p for c in reversed(f.all_coeffs())];F=Field(p,co)
        U,d=construct(F,s,F.q)
        dg=d==F.zero
        a=guard(F,s,U)
        V,di=construct(F,s,F.power(F.q,s-1));ai=guard(F,s,V)
        ok=not dg and a==(0,0) and ai==(0,0)
        rows.append({'factor_ascending':co,'degree':F.d,'delta_zero':dg,'gcd_U_derivative_degree':a[0],'gcd_U_F_degree':a[1],'inverse_gcd_U_derivative_degree':ai[0],'inverse_gcd_U_F_degree':ai[1],'augmented_nonzero':ok})
        if ok:break
    return {'s':s,'p':p,'number_components':len(fs),'tested_components':rows,'all_components_tested':len(rows)==len(fs),'obstruction':not any(r['augmented_nonzero'] for r in rows)}
if __name__=='__main__':
    pairs=[tuple(map(int,a.split(':'))) for a in sys.argv[1:]]
    if not pairs:pairs=[(s,p) for s in [3,7,11,15,19,23,27,31,35,39,43,47,51,55,59,63] for p in [5,13,17] if s%p]
    out=[]
    for s,p in pairs:
        t=time.monotonic();r=test(s,p);out.append(r)
        Path(__file__).with_name('MODULAR_COMPONENT_TESTS.json').write_text(json.dumps(out,indent=2)+'\n')
        print(s,p,'OBSTRUCTION' if r['obstruction'] else 'good component',len(r['tested_components']),'/',r['number_components'],'time',round(time.monotonic()-t,3),flush=True)
        if r['obstruction']:break
