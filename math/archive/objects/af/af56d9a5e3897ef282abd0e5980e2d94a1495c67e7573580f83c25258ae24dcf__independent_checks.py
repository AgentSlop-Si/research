#!/usr/bin/env python3
from pathlib import Path
import json,random
HERE=Path(__file__).resolve().parent;p=97;rng=random.Random(72251)
def zero(m,n=None):return [[0]*(m if n is None else n) for _ in range(m)]
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def add(A,B):return [[(a+b)%p for a,b in zip(r,s)] for r,s in zip(A,B)]
def scale(A,c):return [[c*v%p for v in row] for row in A]
def mm(A,B):
    C=zero(len(A),len(B[0]))
    for i,row in enumerate(A):
        for k,a in enumerate(row):
            if a:
                for j,b in enumerate(B[k]):
                    if b:C[i][j]=(C[i][j]+a*b)%p
    return C

def inv(A):
    n=len(A);a=[r[:]+e for r,e in zip(A,eye(n))]
    for j in range(n):
        k=next((i for i in range(j,n) if a[i][j]),None)
        assert k is not None
        a[j],a[k]=a[k],a[j];v=pow(a[j][j],-1,p);a[j]=[v*t%p for t in a[j]]
        for i in range(n):
            if i!=j and a[i][j]:
                v=a[i][j];a[i]=[(u-v*t)%p for u,t in zip(a[i],a[j])]
    return [r[n:] for r in a]

def det(A):
    a=[r[:] for r in A];d=1;n=len(a)
    for j in range(n):
        k=next((i for i in range(j,n) if a[i][j]),None)
        if k is None:return 0
        if k!=j:a[k],a[j]=a[j],a[k];d=-d
        v=a[j][j];d=d*v%p;vi=pow(v,-1,p)
        for i in range(j+1,n):
            if a[i][j]:
                q=a[i][j]*vi%p
                for c in range(j+1,n):a[i][c]=(a[i][c]-q*a[j][c])%p
                a[i][j]=0
    return d%p

def den(m):
    n=m*m;A=eye(n)
    for i in range(n):
        if i//m:A[i][i-m]=-rng.randrange(p)%p
        if i%m:A[i][i-1]=-rng.randrange(p)%p
    return A

def monomial(n):
    perm=list(range(n));rng.shuffle(perm);A=zero(n)
    for i,j in enumerate(perm):A[i][j]=rng.randrange(1,p)
    return A

def diagonal(n):
    A=zero(n)
    for i in range(n):A[i][i]=rng.randrange(1,p)
    return A

def blockput(K,A,r,c):
    n=len(A)
    for i in range(n):
        for j in range(n):K[r*n+i][c*n+j]=A[i][j]%p

def support(A):
    return {'max_row':max(sum(v!=0 for v in row) for row in A),
            'max_column':max(sum(A[i][j]!=0 for i in range(len(A))) for j in range(len(A[0])))}

cases=[];pathchecks=[];weyl=[];transport=[]
for m,q in [(2,22),(4,8)]:
    n=m*m;I=eye(n);minusI=scale(I,-1)
    U1=den(m);U2=den(m)
    V1=mm(monomial(n),mm(den(m),monomial(n)))
    V2=mm(monomial(n),mm(den(m),monomial(n)))
    Ui1,Ui2,Vi1,Vi2=[inv(A) for A in [U1,U2,V1,V2]]
    M=monomial(n);E=diagonal(n);D=diagonal(n)
    expected_det=det(U1)*det(V1)*det(U2)*det(V2)%p
    for a,b,g,d in [(1,1,1,2),(0,1,1,2),(1,0,2,1),(1,-1,1,-1),(1,1,0,1),(1,1,1,0),(0,0,1,1),(1,1,0,0)]:
        K=zero(7*n)
        for i,A in enumerate([I,U1,V1,I,U2,V2,I]):blockput(K,A,i,i)
        for r,c,A in [(1,0,minusI),(2,0,minusI),(3,1,scale(I,-a)),(3,2,scale(I,-b)),
                      (4,3,scale(M,-1)),(5,3,scale(M,-1)),(6,4,scale(I,-g)),(6,5,scale(I,-d))]:blockput(K,A,r,c)
        B=E+zero(6*n,n);C=[([0]*(6*n))+row[:] for row in D]
        x=E;y11=mm(Ui1,x);y12=mm(Vi1,x);z1=add(scale(y11,a),scale(y12,b))
        y21=mm(Ui2,mm(M,z1));y22=mm(Vi2,mm(M,z1));z2=add(scale(y21,g),scale(y22,d))
        states=x+y11+y12+z1+y21+y22+z2
        assert mm(K,states)==B
        T=mm(D,z2);assert mm(C,states)==T
        assert det(K)==expected_det!=0
        degrees=support(K);assert degrees['max_row']<=4 and degrees['max_column']<=4
        cases.append({'N':n,'couplings':[a,b,g,d],'K_determinant':expected_det,'K_support':degrees,
                      'state_equations_exact':True,'transfer_exact':True,'T_zero':not any(any(row) for row in T)})
    # Every individual component path is invertible and has <=9 inverse support.
    for ua in [U1,V1]:
        for ub in [U2,V2]:
            P=mm(D,mm(inv(ub),mm(M,mm(inv(ua),E))))
            Pi=mm(inv(E),mm(ua,mm(inv(M),mm(ub,inv(D)))))
            assert mm(P,Pi)==I and support(Pi)['max_row']<=9
            pathchecks.append({'N':n,'inverse_max_row_support':support(Pi)['max_row']})
    F=[[pow(q,-i*j,p) for j in range(n)] for i in range(n)]
    Z=zero(n)
    for j in range(n):Z[(j+1)%n][j]=1
    W=zero(n)
    for i in range(n):W[i][i]=pow(q,-i,p)
    Zi=inv(Z)
    assert mm(F,Z)==mm(W,F) and mm(F,W)==mm(Zi,F)
    assert support(inv(F))['max_row']==n
    assert mm(F,Z)!=mm(inv(W),F) if n>2 else True
    weyl.append({'N':n,'negative_sign_pairs_verified':True,'inverse_fourier_row_support':n,
                 'nonzero_scale_not_fixed':scale(F,2)!=F})
    # Abstract transport positive control with singular R,S on unused state space.
    K=eye(7*n);B=I+zero(6*n,n);C=[row+[0]*(6*n) for row in F]
    for label,X,Y in [('shift',Z,W),('phase',W,Zi)]:
        R=zero(7*n);S=zero(7*n);blockput(R,X,0,0);blockput(S,X,0,0)
        assert mm(K,S)==mm(R,K)
        assert mm(R,B)==mm(B,X) and mm(C,S)==mm(Y,C)
        assert mm(mm(C,B),X)==mm(Y,mm(C,B))
        transport.append({'N':n,'pair':label,'abstract_identity_verified':True,'R_and_S_singular':True,
                          'note':'Abstract lemma control; not a seven-wire Green Fourier realization.'})
result={'field':'F97','literal_seven_wire_controls':cases,'individual_path_inverse_controls':pathchecks,
        'weyl_controls':weyl,'abstract_transport_controls':transport,
        'scope':'State realization, transport implications, signs, and branch accounting verified; no bounded-degree Fourier transport witness constructed.'}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
