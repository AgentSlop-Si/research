#!/usr/bin/env python3
"""Independent Q(zeta_5) check of the new globally summed bank."""
from fractions import Fraction as Q
from pathlib import Path
import json

class K:
    def __init__(self,a=0):
        self.a=tuple(Q(x) for x in (a.a if isinstance(a,K) else ([a,0,0,0] if isinstance(a,(int,Q)) else a)))
        assert len(self.a)==4
    def __add__(self,b):
        b=K(b); return K([x+y for x,y in zip(self.a,b.a)])
    __radd__=__add__
    def __neg__(self): return K([-x for x in self.a])
    def __sub__(self,b): return self+-K(b)
    def __rsub__(self,b): return K(b)+-self
    def __mul__(self,b):
        b=K(b); a=[Q(0)]*7
        for i,x in enumerate(self.a):
            for j,y in enumerate(b.a): a[i+j]+=x*y
        for i in range(6,3,-1):
            for j in range(4): a[i-4+j]-=a[i]
        return K(a[:4])
    __rmul__=__mul__
    def __eq__(self,b): return self.a==K(b).a
    def __bool__(self): return any(self.a)
    def inverse(self):
        assert self
        cols=[(self*K([int(i==j) for i in range(4)])).a for j in range(4)]
        return K(linsolve([[cols[j][i] for j in range(4)] for i in range(4)],[Q(1),Q(0),Q(0),Q(0)]))
    def __truediv__(self,b): return self*K(b).inverse()
    def __pow__(self,n):
        if n<0: return self.inverse()**(-n)
        out=K(1); a=self
        while n:
            if n&1: out=out*a
            a=a*a; n//=2
        return out
    def serial(self): return [str(x) for x in self.a]

def linsolve(M,b):
    n=len(b); a=[list(M[i])+[b[i]] for i in range(n)]
    for j in range(n):
        k=next(k for k in range(j,n) if a[k][j]); a[j],a[k]=a[k],a[j]
        iv=1/a[j][j] if isinstance(a[j][j],Q) else a[j][j].inverse()
        a[j]=[v*iv for v in a[j]]
        for i in range(n):
            if i!=j:
                t=a[i][j]; a[i]=[x-t*y for x,y in zip(a[i],a[j])]
    return [a[i][-1] for i in range(n)]

def trim(a):
    a=list(a)
    while len(a)>1 and not a[-1]: a.pop()
    return a

def add(a,b):
    c=[K(0)]*max(len(a),len(b))
    for i,x in enumerate(a): c[i]=c[i]+x
    for i,x in enumerate(b): c[i]=c[i]+x
    return trim(c)
def scale(a,b): return trim([x*b for x in a])
def sub(a,b): return add(a,scale(b,-1))
def mul(a,b):
    c=[K(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]=c[i+j]+x*y
    return trim(c)
def divmodp(a,b):
    a=trim(a); b=trim(b); assert b!=[K(0)]
    if len(a)<len(b): return [K(0)],a
    q=[K(0)]*(len(a)-len(b)+1); iv=b[-1].inverse()
    while a!=[K(0)] and len(a)>=len(b):
        k=len(a)-len(b); c=a[-1]*iv; q[k]=c
        for j,x in enumerate(b): a[j+k]=a[j+k]-c*x
        a=trim(a)
    return trim(q),a

def rem(a,b): return divmodp(a,b)[1]
def gcd(a,b):
    while b!=[K(0)]: a,b=b,rem(a,b)
    return scale(a,a[-1].inverse())
def invmod(a,m):
    r0,r1=m,rem(a,m); s0,s1=[K(0)],[K(1)]
    while r1!=[K(0)]:
        q,r=divmodp(r0,r1); r0,r1=r1,r; s0,s1=s1,sub(s0,mul(q,s1))
    assert len(r0)==1 and r0[0]
    return rem(scale(s0,r0[0].inverse()),m)
def xmul(a,m):
    r=len(m)-1; a=a+[K(0)]*(r-len(a)); c=a[-1]
    return [((a[i-1] if i else K(0))-c*m[i]) for i in range(r)]
def orthopoly(j,f):
    if not j: return [K(1)]
    return linsolve([[f[i+k] for k in range(j)] for i in range(j)],[-f[i+j] for i in range(j)])+[K(1)]
def trace(v,s): return sum((x*y for x,y in zip(v,s)),K(0))

def bank(sign):
    N=5; r=3; w=K([0,1,0,0]); f=[w**((sign*3*k*k)%5) for k in range(6)]
    P=orthopoly(r,f); R=orthopoly(r-1,f); assert gcd(P,R)==[K(1)]
    for tau in range(11):
        p=add(P,scale(R,tau)); dp=[p[j]*j for j in range(1,len(p))]
        if p[0] and gcd(p,dp)==[K(1)] and gcd(p,[K(-1),K(0),K(0),K(0),K(0),K(1)])==[K(1)]: break
    else: raise AssertionError('No legal parameter')
    q=[sum((p[j+1+l]*f[l] for l in range(r-j)),K(0)) for j in range(r)]
    b=rem(mul(q,invmod(dp,p)),p); assert gcd(b,p)==[K(1)]
    powers=[K(r)]
    for k in range(1,r): powers.append(-k*p[r-k]-sum((p[r-j]*powers[k-j] for j in range(1,k)),K(0)))
    bz=b; moments=[]
    for _ in range(N): moments.append(trace(bz,powers)); bz=xmul(bz,p)
    assert moments==f[:N]
    return {'sign':sign,'tau':tau,'polynomial':[x.serial() for x in p],'numerator':[x.serial() for x in q],'moment_checks':N},moments

def mm(A,B): return [[sum((x*y for x,y in zip(row,col)),K(0)) for col in zip(*B)] for row in A]
def main():
    bm,cm=bank(-1); bp,cp=bank(1); N=5; w=K([0,1,0,0]); G=sum((w**(3*i*i%5) for i in range(5)),K(0)); c=N*G
    A=[w**(3*i*i%5) for i in range(5)]; D=[a.inverse() for a in A]
    F=[[w**(i*j%5) for j in range(5)] for i in range(5)]
    H=[[w**(-3*(i+j)**2%5) for j in range(5)] for i in range(5)]
    B=[[(F[i][j]-G*H[i][j]+(c*D[i] if i==j else K(0)))/(1+c) for j in range(5)] for i in range(5)]
    for i in range(5):
        for j in range(5): assert B[i][j]==(A[i]*cm[(j-i)%5]*A[j]-G*D[i]**2*cp[(j-i)%5]*D[j]**2+(c*D[i] if i==j else K(0)))/(1+c)
    M=[[(w**(-i*j%5))/5+(A[i] if i==j else K(0)) for j in range(5)] for i in range(5)]
    I=[[K(int(i==j)) for j in range(5)] for i in range(5)]
    assert mm(M,B)==I and mm(B,M)==I
    out={'status':'PASS','field':'Q(eta), eta^4+eta^3+eta^2+eta+1=0','N':5,'full_bank_entry_checks':25,'inverse_product_entry_checks':50,'banks':[bm,bp],'scope':'Fresh standard-library characteristic-zero check; no predecessor code imported.'}
    Path(__file__).with_name('CHARACTERISTIC_ZERO_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS Q(zeta_5): 25 bank entries, 50 inverse entries, both squarefree nonresonant bank guards')
if __name__=='__main__': main()
