"""Independent finite-field checks; intentionally does not import the main module."""
from __future__ import annotations
import json
from itertools import product


def factor(n):
    out=[];d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out


def prime(n):
    if n<2:return False
    for d in range(2,int(n**0.5)+1):
        if n%d==0:return False
    return True


def field_root(n):
    m=1
    while True:
        p=m*n+1
        if prime(p):
            for g in range(2,p):
                if all(pow(g,(p-1)//r,p)!=1 for r in factor(p-1)):
                    z=pow(g,(p-1)//n,p)
                    if all(pow(z,n//r,p)!=1 for r in factor(n)):
                        return p,z
        m+=1


def mm(a,b,p):
    out=[[0]*len(b[0]) for _ in a]
    for i in range(len(a)):
        for k in range(len(b)):
            if a[i][k]:
                for j in range(len(b[0])):
                    out[i][j]=(out[i][j]+a[i][k]*b[k][j])%p
    return out


def inv(a,p):
    n=len(a);x=[[(v%p) for v in row]+[1 if i==j else 0 for j in range(n)] for i,row in enumerate(a)]
    for c in range(n):
        s=next(i for i in range(c,n) if x[i][c]);x[c],x[s]=x[s],x[c]
        z=pow(x[c][c],-1,p);x[c]=[v*z%p for v in x[c]]
        for i in range(n):
            if i!=c and x[i][c]:
                z=x[i][c];x[i]=[(u-z*v)%p for u,v in zip(x[i],x[c])]
    return [r[n:] for r in x]


def kron(a,b,p):
    return [[a[i//len(b)][j//len(b[0])]*b[i%len(b)][j%len(b[0])]%p for j in range(len(a[0])*len(b[0]))] for i in range(len(a)*len(b))]


def check(n,m):
    p,z=field_root(n)
    X=[[0]*n for _ in range(n)]
    for j in range(n):X[(j+1)%n][j]=1
    Z=[[pow(z,j,p) if i==j else 0 for j in range(n)] for i in range(n)]
    F=[[pow(z,i*j,p) for j in range(n)] for i in range(n)]
    I=[[1 if i==j else 0 for j in range(m)] for i in range(m)]
    Xb=kron(X,I,p);Zb=kron(Z,I,p);J=kron(F,I,p);Ji=inv(J,p)
    lhs=mm(mm(J,Xb,p),Ji,p)
    lhs2=mm(mm(J,Zb,p),Ji,p)
    return {"n":n,"m":m,"first":lhs==Zb,"second":lhs2==kron(inv(X,p),I,p)}


def embedding(q):
    # Nilpotent spectators for q=p^2.
    p=next(r for r in factor(q) if r*r==q)
    rows=[(i,p*((2*i+1)%p)%q) for i in range(q)]
    cols=[(j,p*((3*j+2)%p)%q) for j in range(q)]
    ok=True
    for i in range(q):
        for j in range(q):
            e=(rows[i][0]*cols[j][0]+rows[i][1]*cols[j][1])%q
            ok &= e==(i*j)%q
    return {"q":q,"exact":ok,"nontrivial":any(x[1] for x in rows) and any(y[1] for y in cols)}


def main():
    out={"covariance":[check(3,2),check(5,2),check(9,2)],"embeddings":[embedding(9),embedding(25)]}
    with open("independent_results.json","w") as f:json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps(out,indent=2,sort_keys=True))
    assert all(x["first"] and x["second"] for x in out["covariance"])
    assert all(x["exact"] and x["nontrivial"] for x in out["embeddings"])

if __name__=="__main__":main()
