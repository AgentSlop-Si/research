"""Independent finite-field verifier; intentionally does not import two_line_weyl."""
from __future__ import annotations
import json
from pathlib import Path


def is_prime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    d=3
    while d*d<=n:
        if n%d==0:return False
        d+=2
    return True

def factors(n):
    out=[];d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1 if d==2 else 2
    if n>1:out.append(n)
    return out

def proot(p):
    fs=factors(p-1)
    for g in range(2,p):
        if all(pow(g,(p-1)//q,p)!=1 for q in fs):return g
    raise RuntimeError

def field(n):
    for k in range(1,10000):
        p=k*n+1
        if is_prime(p):
            g=proot(p);w=pow(g,(p-1)//n,p)
            return p,w
    raise RuntimeError

def rank(A,p):
    A=[r[:] for r in A];r=0
    for c in range(len(A[0])):
        z=next((i for i in range(r,len(A)) if A[i][c]%p),None)
        if z is None:continue
        A[r],A[z]=A[z],A[r]
        iv=pow(A[r][c],-1,p);A[r]=[x*iv%p for x in A[r]]
        for i in range(len(A)):
            if i!=r and A[i][c]:
                q=A[i][c];A[i]=[(x-q*y)%p for x,y in zip(A[i],A[r])]
        r+=1
    return r

def mm(A,B,p):
    Bt=list(zip(*B));return [[sum(x*y for x,y in zip(row,col))%p for col in Bt] for row in A]
def D(n,p,w,a,b):
    h=pow(2,-1,n);M=[[0]*n for _ in range(n)]
    for j in range(n):M[(j+a)%n][j]=pow(w,(a*b*h+b*j)%n,p)
    return M
def F(n,p,w):return [[pow(w,i*j%n,p) for j in range(n)] for i in range(n)]
def L(n,p,w,u):
    h4=pow(4,-1,n);q=(u[0]*u[0]+u[1]*u[1])%n;M=[[0]*n for _ in range(n)]
    for m in range(n):
        c=pow(w,(-q*m*m*h4)%n,p);T=D(n,p,w,m*u[0]%n,m*u[1]%n)
        for i in range(n):
            for j in range(n):M[i][j]=(M[i][j]+c*T[i][j])%p
    return M
def gauss(n,p,w):return pow(n,-1,p)*sum(pow(w,j*j%n,p) for j in range(n))%p


def main():
    rows=[]
    for n,u in [(7,(1,0)),(11,(1,2)),(13,(2,2)),(17,(0,1))]:
        p,w=field(n);a,b=u;v=((a-b)%n,(a+b)%n)
        A=L(n,p,w,u);B=[[gauss(n,p,w)*x%p for x in r] for r in L(n,p,w,v)]
        ok=mm(A,B,p)==F(n,p,w)
        rows.append({'N':n,'p':p,'u':u,'v':v,'factorization':ok,'rank_A':rank(A,p),'rank_B':rank(B,p)})
        assert ok and rank(A,p)==n and rank(B,p)==n
    out={'independent_cases':rows,'passed':True}
    path=Path(__file__).with_name('independent_results.json')
    path.write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
