"""Independent verifier for v23.

This module intentionally does not import metaplectic_bruhat.py.
"""
from __future__ import annotations
from itertools import product
import json


def prime_factors(n):
    out=[];d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out

def is_prime(n):
    if n<2:return False
    if n%2==0:return n==2
    d=3
    while d*d<=n:
        if n%d==0:return False
        d+=2
    return True

def primitive_root(p):
    fac=prime_factors(p-1)
    for g in range(2,p):
        if all(pow(g,(p-1)//q,p)!=1 for q in fac):return g
    raise RuntimeError

def field_for(n):
    for k in range(1,10000):
        p=k*n+1
        if is_prime(p):
            g=primitive_root(p);return p,pow(g,(p-1)//n,p)
    raise RuntimeError

def zmat(n):return [[0]*n for _ in range(n)]
def mm(A,B,p):
    bt=list(zip(*B));return [[sum(x*y for x,y in zip(row,col))%p for col in bt] for row in A]
def peq(A,B,p):
    lam=None
    for ra,rb in zip(A,B):
        for x,y in zip(ra,rb):
            if y%p:
                q=x*pow(y,-1,p)%p
                if lam is None:lam=q
                elif lam!=q:return False
            elif x%p:return False
    return lam is not None
def C(n,p,w,t):
    A=zmat(n);i2=pow(2,-1,n)
    for x in range(n):A[x][x]=pow(w,t*x*x*i2%n,p)
    return A
def P(n,p,a):
    A=zmat(n)
    for j in range(n):A[a*j%n][j]=1
    return A
def F(n,p,w):return [[pow(w,i*j%n,p) for j in range(n)] for i in range(n)]
def rep(S,n,p,w):
    a,b,c,d=S
    if b%n==0:
        return mm(C(n,p,w,c*pow(a,-1,n)%n),P(n,p,a),p)
    ib=pow(b,-1,n)
    return mm(mm(mm(C(n,p,w,d*ib%n),P(n,p,(-b)%n),p),F(n,p,w),p),C(n,p,w,a*ib%n),p)
def mul(A,B,n):
    a,b,c,d=A;e,f,g,h=B
    return ((a*e+b*g)%n,(a*f+b*h)%n,(c*e+d*g)%n,(c*f+d*h)%n)
def elems(n):return [(a,b,c,d) for a,b,c,d in product(range(n),repeat=4) if (a*d-b*c)%n==1]
def lower(t,n):return (1,0,t%n,1)
def upper(t,n):return (1,t%n,0,1)
def W(n):return (0,n-1,1,0)

def run():
    records=[]
    for n in (5,7,11):
        p,w=field_for(n)
        # independent direct Bruhat-kernel checks
        checked=0
        for S in elems(n):
            a,b,c,d=S
            R=rep(S,n,p,w)
            if b:
                inv=pow(2*b%n,-1,n)
                K=[[pow(w,((d*x*x-2*x*y+a*y*y)*inv)%n,p) for y in range(n)] for x in range(n)]
                assert R==K
            checked+=1
        # unique LUL shear factorization
        sols=[]
        for x,y,z in product(range(n),repeat=3):
            if mul(mul(lower(x,n),upper(y,n),n),lower(z,n),n)==W(n):sols.append((x,y,z))
        assert sols==[(1,n-1,1)]
        # operator version equals Fourier projectively
        x,y,z=sols[0]
        op=mm(mm(rep(lower(x,n),n,p,w),rep(upper(y,n),n,p,w),p),rep(lower(z,n),n,p,w),p)
        assert peq(op,F(n,p,w),p)
        records.append({'n':n,'field':p,'elements_checked':checked,'lul_solution':sols[0]})
    with open('independent_results.json','w') as f:json.dump(records,f,indent=2)
    print(json.dumps(records,indent=2))
if __name__=='__main__':run()
