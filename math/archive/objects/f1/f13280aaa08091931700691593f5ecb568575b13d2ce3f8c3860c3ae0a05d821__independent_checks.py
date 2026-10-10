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

def prime(p):return p>=2 and all(p%d for d in range(2,int(p**0.5)+1))
def field(n):return next(p for p in range(n+1,10000,n) if prime(p))
def data(q,m,p):
    n=q*m;w=root(n,p);fm=fourier(m,p,pow(w,q,p));fq=fourier(q,p,pow(w,m,p));L=kron(fq,ident(m));Delta=diag([pow(w,b*t,p) for b in range(q) for t in range(m)]);R=zero(n)
    for b in range(q):
        for s in range(m):R[b*m+s][b+q*s]=1
    return n,w,fm,fq,L,Delta,R

def bank(active,q,m,fm):return blockdiag([fm if b in active else ident(m) for b in range(q)])
def selector(active,q,m):return diag([int(b in active) for b in range(q) for _ in range(m)])
def original_conversion(m,r):
    q=r*m;n=m*q;p=field(n);n,w,fm,fq,L,D,R0=data(q,m,p);wq=pow(w,m,p);wr=pow(wq,m,p);I=ident(n);pack=zero(n);post=zero(n)
    for g in range(m):
        for h in range(r):
            for s in range(m):pack[(h+r*s)*m+g][(g*r+h)*m+s]=1
            for t in range(m):
                for u in range(r):post[(g*r+h)*m+t][(t+m*u)*m+g]=pow(r,-1,p)*pow(wq,(-t*h)%q,p)*pow(wr,(-h*u)%r,p)%p
    check(stat(pack)['max_row']==stat(pack)['max_column']==1,'packing is permutation')
    full=blockdiag([fm]*q);converted=mul(mul(post,L,p),pack,p);check(converted==full,'unchanged short bank conversion')
    check(scale(converted,r,p)!=full,'inverse radix normalization indispensable')
    selections=[(0,0),(q,0),(q//2,0),(q//2,q-2)];cases=[]
    for j,start in selections:
        active={(start+k)%q for k in range(j)};C=bank(set(range(q))-active,q,m,fm);B=bank(active,q,m,fm);P=mul(mul(L,D,p),C,p)
        if j:
            k=(q+j-1)//j;rep=zero(n)
            for ell in range(k):
                aa=(start-ell*j)%q
                for b in range(ell*j,min((ell+1)*j,q)):
                    dest=(b+aa)%q;check(dest in active,'routed active support')
                    for s in range(m):
                        col=b*m+s;shifted=dest*m+s;tw=pow(D[shifted][shifted],-1,p)
                        for u in range(q):
                            phase=pow(wq,(-aa*u)%q,p)
                            for t in range(m):rep[u*m+t][col]=(rep[u*m+t][col]+phase*P[u*m+t][shifted]*tw)%p
            check(rep==L,'support-cover L recovered with fixed original bank')
            recovered_full=mul(mul(post,rep,p),pack,p);E=selector(active,q,m);recovered_B=add(mul(E,recovered_full,p),sub(I,E,p),p)
            check(recovered_B==B,'active selector preserves original bank')
            F_recovered=mul(mul(P,recovered_B,p),R0,p);calls=k+1
        else:F_recovered=mul(P,R0,p);calls=1
        check(F_recovered==fourier(n,p,w),'original-orientation full Fourier reconstruction')
        cases.append(dict(active_size=j,interval_start=start,P_calls=calls))
    return dict(m=m,q=q,r=r,N=n,p=p,inverse_small_radix_transforms=n//r,conversion=True,inverse_normalization_required=True,full_Fourier_cases=cases)

def main():
    cases=[original_conversion(m,r) for m,r in [(2,2),(3,2),(4,2),(8,2),(2,3),(2,4),(3,4)]]
    result=dict(status='PASS',cases=cases,bank_conversion_cases=len(cases),full_Fourier_reconstructions=sum(len(x['full_Fourier_cases']) for x in cases),uploaded_or_constructor_code_executed=False)
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
