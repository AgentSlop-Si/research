#!/usr/bin/env python3
"""Fresh exact quotient-ring controls, authored 2026-10-10.
No project scripts imported. Coefficients are ascending in q, then z.
"""
from math import gcd
from functools import reduce
from pathlib import Path
import json, sys, time
import sympy as sp

class Cyclotomic:
    def __init__(self,s):
        self.s=s
        x=sp.Symbol('x')
        self.mod=list(reversed([int(a) for a in sp.Poly(sp.cyclotomic_poly(s,x),x).all_coeffs()]))
        self.d=len(self.mod)-1
        self.zero=(0,)*self.d
        self.one=self.elem([1])
        self.q=self.elem([0,1])
    def elem(self,a):
        a=list(a)
        for k in range(len(a)-1,self.d-1,-1):
            c=a[k]
            if c:
                for j in range(self.d): a[k-self.d+j]-=c*self.mod[j]
        return tuple((a+[0]*self.d)[:self.d])
    def add(self,a,b): return tuple(x+y for x,y in zip(a,b))
    def neg(self,a): return tuple(-x for x in a)
    def sub(self,a,b): return self.add(a,self.neg(b))
    def scale(self,a,k): return tuple(k*x for x in a)
    def mul(self,a,b):
        c=[0]*(2*self.d-1)
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):
                    if y:c[i+j]+=x*y
        return self.elem(c)
    def power(self,a,n):
        out=self.one
        while n:
            if n&1:out=self.mul(out,a)
            a=self.mul(a,a);n//=2
        return out
    def inv_conj(self,a):
        out=self.zero
        for i,c in enumerate(a): out=self.add(out,self.scale(self.power(self.q,(-i)%self.s),c))
        return out
    def content(self,a): return reduce(gcd,a,0)

# Determinant by independent-permutation dynamic programming. No divisions.
def det(K,M):
    n=len(M);D={0:K.one}
    for i in range(n):
        E={}
        for mask,a in D.items():
            for j in range(n):
                if mask>>j&1:continue
                b=K.mul(a,M[i][j])
                if (mask>>(j+1)).bit_count()&1:b=K.neg(b)
                mm=mask|1<<j
                E[mm]=K.add(E.get(mm,K.zero),b)
        D=E
    return D[(1<<n)-1]

def padd(K,a,b):
    a=a+[K.zero]*max(0,len(b)-len(a));b=b+[K.zero]*max(0,len(a)-len(b))
    return [K.add(x,y) for x,y in zip(a,b)]
def pmul(K,a,b):
    out=[K.zero]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]=K.add(out[i+j],K.mul(x,y))
    return out
def rem(K,a,f):
    assert f[-1]==K.one
    a=list(a);n=len(f)-1
    for i in range(len(a)-1,n-1,-1):
        c=a[i]
        if c!=K.zero:
            for j in range(n):a[i-n+j]=K.sub(a[i-n+j],K.mul(c,f[j]))
    return (a+[K.zero]*n)[:n]
def res(K,f,h):
    """Res(f,h), f monic, via multiplication by h on K[z]/f."""
    n=len(f)-1
    if n==0:return K.one
    cols=[rem(K,[K.zero]*i+h,f) for i in range(n)]
    return det(K,[[cols[j][i] for j in range(n)] for i in range(n)])
def disc(K,f):
    n=len(f)-1
    if n<=1:return K.one
    return K.scale(res(K,f,[K.scale(f[i],i) for i in range(1,n+1)]),(-1)**(n*(n-1)//2))

def get_h(K,b):
    a=[K.one];c=[K.one,K.one]
    if b==0:return a
    for n in range(2,b+1):
        t=K.sub(K.power(K.q,n-1),K.one)
        a,c=c,padd(K,padd(K,c,[K.zero]+c),[K.zero]+[K.mul(t,x) for x in a])
    return c

def product(K,exponents):
    out=K.one
    for e in exponents:out=K.mul(out,K.sub(K.one,K.power(K.q,e)))
    return out

def palindromic_transform(K,U):
    """Recover unique monic P with U(z)=z^r P(z+z^-1)."""
    r=(len(U)-1)//2;P=[K.zero]*(r+1);remain=U[:]
    from math import comb
    for j in range(r,-1,-1):
        c=remain[r+j];P[j]=c
        for k in range(j+1):remain[r+j-2*k]=K.sub(remain[r+j-2*k],K.scale(c,comb(j,k)))
    assert all(x==K.zero for x in remain)
    return P

def peval(K,f,t):
    a=K.zero
    for c in f[::-1]:a=K.add(K.mul(a,t),c)
    return a

def run(s):
    K=Cyclotomic(s);r=(s-3)//4;b=(s-1)//2
    H=get_h(K,b)
    U=[H[0]]
    for k in range(1,b):U.append(K.sub(H[k],U[-1]))
    assert U[-1]==H[-1] and U==U[::-1]
    g=peval(K,U,K.neg(K.one))
    v=product(K,list(range(2,2*r+1,2))+list(range(1,2*b,2)))
    delta=K.sub(K.scale(g,2),v)
    D=disc(K,U)
    R=res(K,U,[K.one]+[K.zero]*(s-1)+[K.one])
    Gamma=K.mul(D,R)
    pair=K.mul(Gamma,K.inv_conj(Gamma))
    aug=K.mul(pair,delta)
    identity=K.sub(K.add(K.mul(g,K.inv_conj(v)),K.mul(K.inv_conj(g),v)),K.mul(v,K.inv_conj(v)))
    assert identity==K.zero
    # A different, smaller determinant identity independently checks D and R.
    P=palindromic_transform(K,U)
    dp=disc(K,P);p2=peval(K,P,K.scale(K.one,2));pm2=peval(K,P,K.scale(K.one,-2))
    D2=K.mul(K.mul(p2,pm2),K.mul(dp,dp));assert D2==D
    # S_s(t)=z^s+z^-s.  S_s+2=(t+2) C_s(t)^2.  Instead of
    # taking the square root, evaluate the monic degree-s polynomial directly.
    T0=[K.scale(K.one,2)];T1=[K.zero,K.one]
    for n in range(2,s+1):T0,T1=T1,padd(K,[K.zero]+T1,[K.neg(c) for c in T0])
    Ts=padd(K,T1,[K.scale(K.one,2)])
    R2=res(K,P,Ts);assert R2==R
    data={'s':s,'b':b,'r':r,'phi_ascending':K.mod,'coefficient_order':'ascending q; U and P outer lists ascending z or t','U':U,'P':P,'g':g,'v':v,'delta':delta,'disc_U':D,'res_F_U':R,'Gamma':Gamma,'Gamma_pair':pair,'augmented':aug,'contents':{name:K.content(a) for name,a in [('disc_U',D),('res_F_U',R),('Gamma',Gamma),('Gamma_pair',pair),('delta',delta),('augmented',aug)]},'inverse_identity':True,'palindromic_disc_check':True,'palindromic_resultant_check':True}
    data['content_factorizations']={key:{str(p):int(e) for p,e in sp.factorint(c).items()} for key,c in data['contents'].items()}
    out=Path(__file__).with_name(f'EXACT_CONTENT_S{s}.json');out.write_text(json.dumps(data,indent=2)+'\n')
    print(s,data['contents'],data['content_factorizations'],flush=True)
    return data
if __name__=='__main__':
    for s in map(int,sys.argv[1:] or ['3','7','11','15','19']):
        start=time.monotonic();run(s);print('elapsed',time.monotonic()-start,flush=True)
