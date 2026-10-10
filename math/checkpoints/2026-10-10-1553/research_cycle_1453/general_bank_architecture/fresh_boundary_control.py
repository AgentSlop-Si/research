"""New standalone control of inverse-shift construction and one-bank curve.
No author or predecessor research module is imported or executed.
"""
from pathlib import Path
import json

def isprime(p): return p>=2 and all(p%d for d in range(2,int(p**.5)+1))
def inv(A,p):
    n=len(A);R=[[x%p for x in row]+[int(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        k=next(i for i in range(j,n) if R[i][j]);R[j],R[k]=R[k],R[j]
        z=pow(R[j][j],-1,p);R[j]=[z*x%p for x in R[j]]
        for i in range(n):
            if i!=j:
                z=R[i][j];R[i]=[(a-z*b)%p for a,b in zip(R[i],R[j])]
    return [row[n:] for row in R]
def mm(A,B,p):
    return [[sum(a*b for a,b in zip(row,col))%p for col in zip(*B)] for row in A]
def primitive(order,p):
    return next(z for z in range(2,p) if pow(z,order,p)==1 and all(pow(z,d,p)!=1 for d in range(1,order)))
def bank(N,p,q,e,alpha,weight):
    I=[[int(k==t) for t in range(N)] for k in range(N)];R=[[0]*N for _ in range(N)]
    for j in range(N):
        H=[row[:] for row in I]
        for t in range(N):
            H[(t+e)%N][t]=(H[(t+e)%N][t]-alpha)%p
            H[t][t]=(H[t][t]-pow(q,(e*j+t)%N,p))%p
        V=inv(H,p)
        assert mm(H,V,p)==I and mm(V,H,p)==I
        for k in range(N):
            for t in range(N):R[k][t]=(R[k][t]+weight*pow(N,-1,p)*V[k][t])%p
    return R
results=[]
for N in (3,5,7,9,11,15):
    M=N-1;p=N*M+1
    while not isprime(p):p+=N*M
    q=primitive(N,p);z=primitive(M,p);xs=[pow(z,k,p) for k in range(M)]
    assert len(set(xs))==M
    acc=[[0]*N for _ in range(N)]
    for x in xs:
        assert (-pow(x,N,p))%p==(-x)%p
        B=bank(N,p,q,-1,x,(-pow(M,-1,p))%p)
        for k in range(N):
            for t in range(N):acc[k][t]=(acc[k][t]+B[k][t])%p
    target=[[int(k==(t-1)%N) for t in range(N)] for k in range(N)]
    assert acc==target
    for t in (2,3):
        alpha=pow(t,-1,p);B=bank(N,p,q,1,alpha,-alpha)
        curve=[[pow(t,N-1-((k-j)%N),p) for j in range(N)] for k in range(N)]
        assert B==curve
    results.append({'N':N,'p':p,'q':q,'root_order':M,'branches_checked':N*(M+2),'matrix_equalities_checked':3,'status':'PASS'})
out={'status':'PASS','scope':'Finite-field literal matrix controls of exact roots-of-unity identity and two nonzero points of the boundary curve; symbolic proof establishes characteristic-zero theorem.','results':results}
path=Path(__file__).resolve().parent
(path/'BOUNDARY_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
