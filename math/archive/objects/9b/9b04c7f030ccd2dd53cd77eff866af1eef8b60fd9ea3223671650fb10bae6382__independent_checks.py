#!/usr/bin/env python3
"""Independent exact controls; standard library only; no submitted code imported."""
import itertools, json, random, sys
from pathlib import Path

def ident(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def zero(n,m=None): return [[0]*(n if m is None else m) for _ in range(n)]
def mul(a,b,p):
    out=zero(len(a),len(b[0]))
    for i,row in enumerate(a):
        for k,x in enumerate(row):
            if x:
                for j,y in enumerate(b[k]): out[i][j]=(out[i][j]+x*y)%p
    return out
def scale(a,c,p): return [[x*c%p for x in row] for row in a]
def add(a,b,p): return [[(x+y)%p for x,y in zip(r,s)] for r,s in zip(a,b)]
def sub(a,b,p): return add(a,scale(b,-1,p),p)
def trans(a): return list(map(list,zip(*a)))
def inv(a,p):
    n=len(a); u=[[(x%p) for x in a[i]]+ident(n)[i] for i in range(n)]
    for j in range(n):
        k=next(k for k in range(j,n) if u[k][j]); u[j],u[k]=u[k],u[j]
        u[j]=[x*pow(u[j][j],-1,p)%p for x in u[j]]
        for k in range(n):
            if k!=j:
                c=u[k][j]; u[k]=[(x-c*y)%p for x,y in zip(u[k],u[j])]
    return [r[n:] for r in u]
def powmat(a,n,p):
    z=ident(len(a))
    while n:
        if n&1:z=mul(z,a,p)
        a=mul(a,a,p);n//=2
    return z
def root(n,p):
    return next(w for w in range(1,p) if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n) if n%d==0))
def fourier(n,p,w=None):
    w=root(n,p) if w is None else w
    return [[pow(w,i*j,p) for j in range(n)] for i in range(n)]
def shift(n):
    z=zero(n)
    for j in range(n): z[(j+1)%n][j]=1
    return z
def diag(v): return [[x if i==j else 0 for j in range(len(v))] for i,x in enumerate(v)]
def blockdiag(blocks):
    n=sum(map(len,blocks)); z=zero(n); offset=0
    for b in blocks:
        for i,row in enumerate(b):z[offset+i][offset:offset+len(b)]=row
        offset+=len(b)
    return z
def kron(a,b): return [[x*y for x in ar for y in br] for ar in a for br in b]
def stat(a):
    rows=[sum(x!=0 for x in r) for r in a]; cols=[sum(x!=0 for x in r) for r in trans(a)]
    return dict(nnz=sum(rows),max_row=max(rows),max_column=max(cols))
def check(x,msg):
    if not x: raise AssertionError(msg)

def vector(a,v,p): return [sum(x*y for x,y in zip(row,v))%p for row in a]
def rank(a,p):
    z=[row[:] for row in a];r=0
    for j in range(len(z[0])):
        candidates=[i for i in range(r,len(z)) if z[i][j]%p]
        if not candidates:continue
        k=candidates[0];z[r],z[k]=z[k],z[r];c=pow(z[r][j],-1,p);z[r]=[x*c%p for x in z[r]]
        for i in range(len(z)):
            if i!=r:
                c=z[i][j];z[i]=[(x-c*y)%p for x,y in zip(z[i],z[r])]
        r+=1
        if r==len(z):break
    return r

def det(a,p):
    z=[r[:] for r in a];out=1;n=len(a)
    for j in range(n):
        ks=[k for k in range(j,n) if z[k][j]%p]
        if not ks:return 0
        k=ks[0]
        if k!=j:z[j],z[k]=z[k],z[j];out=-out
        c=z[j][j];out=out*c%p;ci=pow(c,-1,p)
        for k in range(j+1,n):
            t=z[k][j]*ci%p;z[k]=[(x-t*y)%p for x,y in zip(z[k],z[j])]
    return out%p

def spectral_minor():
    n=4;p=65537;I=ident(n);FF=fourier(n,p,65281);P=trans(shift(n));sigma=[0,2,1,3];T=zero(n)
    for i,j in enumerate(sigma):T[i][j]=1
    Q=mul(mul(T,P,p),T,p);check(mul(P,Q,p)!=mul(Q,P,p),'N4 orders noncommute')
    G=inv(sub(I,scale(P,3,p),p),p);H=inv(sub(I,scale(Q,5,p),p),p);U=mul(FF,G,p);V=mul(FF,H,p)
    coeff=[mul(U,U,p),add(mul(U,V,p),mul(V,U,p),p),mul(V,V,p),scale(U,2,p),scale(V,2,p),I]
    positions=[(0,j) for j in range(4)]+[(1,0),(1,1)]
    minor=[[C[i][j] for C in coeff] for i,j in positions]
    expected=[[11469,50056,38545,65536,32768,1],[34407,11112,46107,65536,32768,0],[37684,11070,61651,65536,32768,0],[47515,58837,33924,65536,32768,0],[3593,9440,44544,39476,27744,0],[10779,54667,28467,52379,37708,1]]
    check(minor==expected,'displayed minor entries');dd=det(minor,p);check(dd==19255,'displayed determinant')
    return dict(N=n,p=p,root=65281,minor=minor,determinant=dd,complex_independence_certified_by_valid_reduction=True)

def spectral_case(n,p,r):
    FF=fourier(n,p);FI=inv(FF,p);I=ident(n);lam=2;dp=lam*pow(1-lam,-1,p)%p;dm=-lam*pow(1+lam,-1,p)%p;ss=(dp+dm)%p;pp=dp*dm%p
    Delta=diag([dp]*r+[dm]*(n-r));C=ident(n)
    for i in range(n):
        for j in range(i+1,n):C[i][j]=(3*i+j+1)%p
    M=mul(mul(C,Delta,p),inv(C,p),p);A=mul(FI,M,p)
    check(add(sub(mul(M,M,p),scale(M,ss,p),p),scale(I,pp,p),p)==zero(n),'spectral equation')
    Pi=scale(sub(M,scale(I,dm,p),p),pow(dp-dm,-1,p),p)
    check(mul(Pi,Pi,p)==Pi and rank(Pi,p)==r,'integer rank multiplicity')
    check(add(sub(mul(mul(A,FF,p),A,p),scale(A,ss,p),p),scale(FI,pp,p),p)==zero(n),'Riccati equation')
    K=sub(scale(M,1-lam*lam,p),scale(I,lam*lam,p),p)
    B=inv(add(FI,A,p),p);B2=sub(scale(FF,1-lam*lam,p),scale(inv(A,p),lam*lam,p),p)
    B3=add(scale(FF,1+lam*lam,p),scale(mul(mul(FF,A,p),FF,p),lam*lam-1,p),p)
    check(B==B2==B3,'three forced B formulas');check(mul(B,A,p)==K and mul(K,K,p)==scale(I,lam*lam,p),'forced loop')
    check(mul(inv(sub(I,K,p),p),B,p)==FF,'oracle-control Fourier feedback')
    return dict(N=n,p=p,plus_multiplicity=r,oracle_constructed_A=True,all_identities=True)

def main():
    result=dict(status='PASS',spectral_minor=spectral_minor(),spectral_oracle_controls=[spectral_case(n,241,r) for n in [3,4,5,8,12,16] for r in [1,n-1]],uploaded_or_constructor_code_executed=False)
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
