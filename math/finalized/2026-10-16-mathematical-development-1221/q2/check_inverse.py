#!/usr/bin/env python3
"""Fresh exact checker for Q2's new paid inverse. No project code imports.
All matrix oracles below are intentionally expensive and excluded from executor cost.
"""
from fractions import Fraction
import json, hashlib, pathlib

class F:
    def __init__(self,p): self.p=p;self.ops=0
    def a(self,x,y):self.ops+=1;return (x+y)%self.p
    def s(self,x,y):self.ops+=1;return (x-y)%self.p
    def m(self,x,y):self.ops+=1;return x*y%self.p
    def d(self,x,y):
        assert y%self.p
        self.ops+=1;return x*pow(y,-1,self.p)%self.p

def factors(n):
    z=[];d=2
    while d*d<=n:
        if n%d==0:
            z.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:z.append(n)
    return z

def prime(p):return p>=2 and all(p%d for d in range(2,int(p**.5)+1))
def root(m,p):
    for g in range(2,p):
        q=pow(g,(p-1)//m,p)
        if pow(q,m,p)==1 and all(pow(q,m//r,p)!=1 for r in factors(m)):return q
    raise AssertionError('root absent')

def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def matvec(M,x,p):return [sum(a*b for a,b in zip(row,x))%p for row in M]
def mm(A,B,p):
    bt=list(zip(*B))
    return [[sum(a*b for a,b in zip(row,col))%p for col in bt]for row in A]
def inv(A,p):
    n=len(A);R=[row[:]+unit for row,unit in zip(A,eye(n))]
    for j in range(n):
        k=next((k for k in range(j,n) if R[k][j]%p),None)
        assert k is not None,'singular'
        R[j],R[k]=R[k],R[j];s=pow(R[j][j],-1,p);R[j]=[v*s%p for v in R[j]]
        for i in range(n):
            if i!=j:
                s=R[i][j];R[i]=[(a-s*b)%p for a,b in zip(R[i],R[j])]
    assert [row[:n]for row in R]==eye(n)
    return [row[n:]for row in R]

class PaidInverse:
    def __init__(self,m,p):
        self.m=m;self.p=p;self.f=F(p);f=self.f;self.omega=root(m*m,p);self.q=pow(self.omega,m,p)
        assert pow(self.q,m,p)==1 and all(pow(self.q,m//r,p)!=1 for r in factors(m))
        self.pow=[pow(self.q,a,p)for a in range(m)]
        self.Lexp=4+m*((2*m-1).bit_length());self.lam=pow(pow(2,self.Lexp,p),-1,p)
        self.s=f.a(1,self.lam);self.is_=f.d(1,self.s);self.quarter=f.d(1,4)
        self.t=f.m(f.m(self.lam,self.quarter),self.is_)
        self.denom=f.s(1,pow(self.t,m,p));assert self.denom
        self.idenom=f.d(1,self.denom)
        self.rowt=[f.m(self.t,qa) for qa in self.pow]
        self.negpow=[self.pow[(-c)%m]for c in range(m)]
        prep=self.f.ops
        E=[[0]*m for _ in range(m)]
        for j in range(m):
            b=[int(c==j)for c in range(m)]
            for a in range(m):b=self.dsolve(a,self.R(b))
            for i in range(m):E[i][j]=b[i]
        self.E=E
        Fm=[[f.s(int(i==j),E[i][j])for j in range(m)]for i in range(m)]
        # Exact factorization with deterministic pivoting, saved for warm solves.
        LU=[row[:]for row in Fm];perm=list(range(m))
        for j in range(m):
            k=next((k for k in range(j,m)if LU[k][j]),None);assert k is not None
            LU[j],LU[k]=LU[k],LU[j];perm[j],perm[k]=perm[k],perm[j]
            for i in range(j+1,m):
                LU[i][j]=f.d(LU[i][j],LU[j][j])
                for k in range(j+1,m):LU[i][k]=f.s(LU[i][k],f.m(LU[i][j],LU[j][k]))
        self.LU=LU;self.perm=perm;self.setup_ops=self.f.ops;self.initial_prep_ops=prep
    def R(self,v):
        f=self.f;m=self.m
        return [f.m(self.quarter,f.a(f.a(v[(c+1)%m],f.m(self.negpow[c],v[c])),f.m(self.lam,v[c])))for c in range(m)]
    def dsolve(self,a,v):
        # Solve (s I - lambda q^a U/4) z=v with cyclic row boundary.
        f=self.f;t=self.rowt[a];h=[f.m(self.is_,x)for x in v]
        z=0
        for x in h:z=f.a(x,f.m(t,z))
        b=f.m(z,self.idenom);out=[]
        for x in h:b=f.a(x,f.m(t,b));out.append(b)
        return out
    def lapply(self,v):
        f=self.f;m=self.m
        return [f.s(v[a*m+c],f.m(self.quarter,f.a(v[((a-1)%m)*m+c],f.m(self.pow[a],v[a*m+(c-1)%m]))))for a in range(m)for c in range(m)]
    def mapply(self,v):
        f=self.f;m=self.m
        return [f.s(v[a*m+c],f.m(self.quarter,f.a(v[((a-1)%m)*m+(c+1)%m],f.m(self.negpow[c],v[((a-1)%m)*m+c]))))for a in range(m)for c in range(m)]
    def sweep(self,g,b):
        f=self.f;m=self.m;out=[]
        for a in range(m):
            r=self.R(b);b=self.dsolve(a,[f.a(g[a*m+c],r[c])for c in range(m)])
            out.extend(b)
        return out,b
    def bsolve(self,p):
        f=self.f;m=self.m;A=self.LU;b=[p[i]for i in self.perm]
        for i in range(m):
            for j in range(i):b[i]=f.s(b[i],f.m(A[i][j],b[j]))
        for i in range(m-1,-1,-1):
            for j in range(i+1,m):b[i]=f.s(b[i],f.m(A[i][j],b[j]))
            b[i]=f.d(b[i],A[i][i])
        return b
    def solve(self,v):
        n=self.f.ops;g=self.lapply(v);_,p=self.sweep(g,[0]*self.m);b=self.bsolve(p)
        y,end=self.sweep(g,b);assert end==b
        x=self.mapply(y);return x,self.f.ops-n

def dense_source(m,p,q,lam):
    n=m*m;L=eye(n);quarter=pow(4,-1,p)
    for a in range(m):
        for c in range(m):
            i=a*m+c;L[i][((a-1)%m)*m+c]=(L[i][((a-1)%m)*m+c]-quarter)%p
            L[i][a*m+(c-1)%m]=(L[i][a*m+(c-1)%m]-quarter*pow(q,a,p))%p
    # Independent explicit permutation conjugation, not row formula.
    phi=[((-c)%m)*m+(a+c)%m for a in range(m)for c in range(m)]
    M=[[L[phi[i]][phi[j]]for j in range(n)]for i in range(n)]
    Gi=inv(L,p);Hi=inv(M,p)
    S=[[(Gi[i][j]+lam*Hi[i][j])%p for j in range(n)]for i in range(n)]
    return L,M,S

def fraction_m2():
    t=Fraction(1,256);s=1+t;q=-1
    def prod(A,B):return [[sum(A[i][k]*B[k][j]for k in range(2))for j in range(2)]for i in range(2)]
    R=[[Fraction(1,4)*(1+t),Fraction(1,4)],[Fraction(1,4),Fraction(1,4)*(-1+t)]]
    def dinv(a):
        r=t*q**a/4;z=s*s-r*r
        return [[s/z,r/z],[r/z,s/z]]
    E=prod(prod(prod(dinv(1),R),dinv(0)),R)
    assert E[0][1]!=0
    return {'m':2,'lambda':str(t),'E':[[str(x)for x in row]for row in E],
      'nonzero_offdiagonal':str(E[0][1]),'conclusion':'The actual fixed schedule does not have a scalar row monodromy, already at m=2.'}

out={'kind':'Fresh exact finite-field controls plus exact rational noncollapse','cases':[]}
for m in [2,3,4,5,6,8]:
    p=14401;assert prime(p) and (p-1)%(m*m)==0
    e=PaidInverse(m,p);L,M,S=dense_source(m,p,e.q,e.lam);n=m*m
    denseInv=inv(S,p);cols=[];costs=[]
    for j in range(n):
        basis=[int(i==j)for i in range(n)];x,cost=e.solve(basis);costs.append(cost);cols.append(x)
        assert matvec(S,x,p)==basis
        assert x==[denseInv[i][j]for i in range(n)]
    # Independent factor-order identity and sparse orientation check.
    K=[[(M[i][j]+e.lam*L[i][j])%p for j in range(n)]for i in range(n)]
    assert mm(mm(M,inv(K,p),p),L,p)==denseInv
    for j in range(n):
        b=[int(i==j)for i in range(n)]
        assert e.mapply(b)==[M[i][j]for i in range(n)]
    assert max(costs)==min(costs)
    scalar=all(e.E[i][j]==(e.E[0][0] if i==j else 0)for i in range(m)for j in range(m))
    out['cases'].append({'m':m,'N':n,'p':p,'omega_N':e.omega,'q':e.q,'omega_to_q_verified':pow(e.omega,m,p)==e.q,'lambda_mod_p':e.lam,'Lexp':e.Lexp,'basis_solves':n,'all_basis_residuals_zero':True,'matches_independent_dense_inverse':True,'orientation_formula_verified':True,'exact_factor_order_verified':True,'monodromy_scalar':scalar,'setup_count_excluding_pow_and_root_search':e.setup_ops,'warm_scalar_ops':costs[0],'warm_ops_per_N':costs[0]/n})
out['rational_noncollapse']=fraction_m2()
out['scope']='Controls support the general algebraic proof; neither all-m proof nor floating-point validation follows from the finite tests. pow/root construction is explicitly excluded from instrument counts and charged in the written setup ledger.'
p=pathlib.Path(__file__).with_name('EXACT_RESULTS.json');p.write_text(json.dumps(out,indent=2)+'\n');print(p.read_text())
