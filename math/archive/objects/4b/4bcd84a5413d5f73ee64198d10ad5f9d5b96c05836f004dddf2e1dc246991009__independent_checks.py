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

def prime(p):return p>=2 and all(p%d for d in range(2,int(p**0.5)+1))
def choose_chirp_field(n):
    for k in range(2,1000):
        p=k*n+1
        if prime(p):
            w=root(n,p);h=(n+1)//2;G=sum(pow(w,h*j*j,p) for j in range(n))%p;c=n*G%p
            if (1+c)%p:return p,w
    raise AssertionError('test field not found')
def degree_matrices(mats,p):return rank([[M[i][j] for M in mats] for i in range(len(mats[0])) for j in range(len(mats[0]))],p)

def chirp_case(n,p=None,w=None):
    if p is None:p,w=choose_chirp_field(n)
    h=(n+1)//2;I=ident(n);FF=fourier(n,p,w);FB=fourier(n,p,pow(w,-1,p));ph=[pow(w,h*j*j,p) for j in range(n)];A=diag(ph);AI=inv(A,p);G=sum(ph)%p;Gm=sum(pow(x,-1,p) for x in ph)%p;c=n*G%p
    recurrence=[];a=1;r=pow(w,h,p)
    for j in range(n):recurrence.append(a);a=a*r%p;r=r*w%p
    check(recurrence==ph,'uniform chirp recurrence');check(G*Gm%p==n%p,'Gauss product')
    M=mul(FF,A,p);M2=mul(M,M,p);M3=mul(M2,M,p)
    check(M2==scale(mul(AI,FB,p),G,p) and M3==scale(I,c,p),'positive chirp cube')
    Mm=mul(FF,AI,p);REV=zero(n)
    for j in range(n):REV[(-j)%n][j]=1
    check(mul(mul(Mm,Mm,p),Mm,p)==scale(REV,n*Gm,p),'negative chirp cube')
    md=degree_matrices([I,M,M2],p)
    if n>=5:check(md==3,'M degree exactly three')
    if (1+c)%p==0:
        check(rank(add(I,M,p),p)<n,'explicit resonance singularity')
        return dict(N=n,p=p,root=w,c=c,resonant=True,I_plus_M_rank=rank(add(I,M,p),p))
    B=mul(inv(add(I,M,p),p),FF,p)
    B2=scale(add(sub(FF,mul(mul(FF,A,p),FF,p),p),scale(AI,c,p),p),pow(1+c,-1,p),p)
    B3=scale(add(sub(FF,scale(mul(mul(AI,FB,p),AI,p),G,p),p),scale(AI,c,p),p),pow(1+c,-1,p),p)
    check(B==B2==B3==inv(add(inv(FF,p),A,p),p),'chirp B formulas')
    K=mul(B,A,p);K2=mul(K,K,p);K3=mul(K2,K,p)
    mu=add(sub(scale(K3,1+c,p),scale(K2,3*c,p),p),sub(scale(K,3*c,p),scale(I,c,p),p),p)
    check(mu==zero(n),'cubic loop annihilator')
    inverse_poly=add(add(scale(I,1+c,p),scale(K,1-2*c,p),p),scale(K2,1+c,p),p)
    check(inverse_poly==inv(sub(I,K,p),p),'cubic polynomial inverse')
    check(mul(inverse_poly,B,p)==FF,'exact Fourier output')
    if n>=5:check(degree_matrices([I,K,K2],p)==3,'K degree exactly three')
    corr=sub(B,AI,p);check(rank(corr,p)==n and corr==scale(mul(inv(add(I,M,p),p),AI,p),-1,p),'full rank correction')
    check(sub(I,mul(AI,A,p),p)==zero(n),'dropping correction destroys feedback')
    for j in range(n):
        x=[int(i==j) for i in range(n)];u=vector(B,x,p);v=[(1+c)*t%p for t in u]
        v=vector(B,vector(A,v,p),p);v=[(x+(1-2*c)*y)%p for x,y in zip(v,u)]
        v=vector(B,vector(A,v,p),p);v=[(x+(1+c)*y)%p for x,y in zip(v,u)]
        check(v==vector(FF,x,p),'three-B Horner basis evaluator')
    return dict(N=n,p=p,root=w,G=G,c=c,resonant=False,M_minimal_degree=md,K_minimal_degree=degree_matrices([I,K,K2],p),correction_rank=n,basis_vectors_checked=n,B_is_Fourier_oracle_expression=True)

def main():
    result=dict(status='PASS',chirp_controls=[chirp_case(n) for n in [3,5,7,9,15,21,25,27,35,63]],resonance=chirp_case(3,7,2),uploaded_or_constructor_code_executed=False)
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
