from math import comb
from pathlib import Path
import json

# Sparse exact integer polynomials in X,q, independently reconstructed.
def add(A,B,s=1):
    C=A.copy()
    for key,v in B.items():
        C[key]=C.get(key,0)+s*v
        if not C[key]:del C[key]
    return C

def mul(A,B):
    C={}
    for (j,k),a in A.items():
        for (l,m),b in B.items():C[(j+l,k+m)]=C.get((j+l,k+m),0)+a*b
    return {key:v for key,v in C.items() if v}

def diff(A):return {(j-1,k):j*a for (j,k),a in A.items() if j}
def u(n):return {(0,0):1,(0,n):-1}
def block(lo,hi):
    A={(0,0):1}
    if hi<lo:return A
    B={(1,0):1}
    for n in range(lo,hi):A,B=B,add({(j+1,k):a for (j,k),a in B.items()},mul(u(n),A),-1)
    return B

def product(*polys):
    R={(0,0):1}
    for P in polys:R=mul(R,P)
    return R

def gaussian(n):
    R={(0,0):1}
    for m in range(1,n+1):
        S=R.copy()
        for (k,j),a in R.items():
            key=(k+1,j+m-k-1)
            S[key]=S.get(key,0)+a
        R=S
    return R

results=[]
for p in [3,5,7]:
    n=3*p
    A=block(1,p);B=block(p+1,2*p);C=block(2*p+1,3*p)
    D=block(1,p-1);E=block(p+2,2*p);G=block(p+1,2*p-1);J=block(2*p+2,3*p);M=block(p+2,2*p-1)
    assembled=add(add(add(product(A,B,C),product(u(p),D,E,C),-1),product(u(2*p),A,G,J),-1),product(u(p),u(2*p),D,M,J))
    P=block(1,n);assert assembled==P
    transformed={}
    for (j,k),a in P.items():
        for r in range(j+1):
            assert (n+j-2*r)%2==0
            key=((n+j-2*r)//2,k)
            transformed[key]=transformed.get(key,0)+a*comb(j,r)
    transformed={key:v for key,v in transformed.items() if v}
    H=gaussian(n);assert transformed==H
    assert H.get((0,0))==1 and not any(k==0 and j for (k,j) in H)
    Q=block(1,n-1);R=block(1,n-2)
    F=add(mul(diff(P),Q),mul(P,diff(Q)),-1)
    Fprev=add(mul(diff(Q),R),mul(Q,diff(R)),-1)
    assert add(add(F,mul(Q,Q),-1),mul(u(n-1),Fprev),-1)=={}
    results.append({'p':p,'degree':n,'actual_terms':len(P),'exact_triple_block_identity':True,'exact_original_gaussian_H_identity':True,'exact_CD_telescope':True,'H_constant_one':True,'status':'PASS'})
    print('PASS exact identities p=',p,flush=True)
Path(__file__).with_name('EXACT_IDENTITY_CHECKS.json').write_text(json.dumps(results,indent=2)+'\n')
