#!/usr/bin/env python3
"""Independent integer transcription checks; no Jacobian rank computation."""
import json
import numpy as np


def ident(n):
    return np.eye(n,dtype=object)


def anchor(n):
    T=3*ident(n); T[0,0]=4
    for i in range(n-1): T[i,i+1]=T[i+1,i]=1
    m=n.bit_length()-1
    assert 1<<m==n
    perm=[int(format(i,f'0{m}b')[::-1],2) for i in range(n)]
    P=np.zeros((n,n),dtype=object)
    for i,j in enumerate(perm): P[j,i]=1
    theta=[1,4]; eta=[1,3]
    for k in range(2,n+1):
        theta.append(3*theta[-1]-theta[-2]); eta.append(3*eta[-1]-eta[-2])
    adj=np.zeros((n,n),dtype=object)
    for i in range(n):
        for j in range(i,n):
            adj[i,j]=adj[j,i]=(-1)**(i+j)*theta[i]*eta[n-1-j]
    assert np.array_equal(T@adj,theta[n]*ident(n))
    assert np.array_equal(P@P,ident(n)) and np.array_equal(P,P.T)
    return T,P,adj,theta[n]


def band(X):
    n=len(X)
    return tuple(X[i,j] for i in range(n) for j in range(n) if abs(i-j)<=2)


def powmat(A,k):
    r=ident(len(A))
    for _ in range(k): r=r@A
    return r


def eq(X,Y):
    assert np.array_equal(X,Y)


def run(n):
    T,P,J,h=anchor(n); A=T@P; C=P@T; d=n//8
    E=lambda W:J@P@W@A
    F=lambda W:C@W@P@J
    Q=lambda W:E(W)+F(W)
    R=lambda W:E(W)-F(W)
    Ap=[powmat(A,k) for k in range(2*d+1)]
    Cp=[powmat(C,k) for k in range(2*d+1)]
    original_checks=0
    for i in range(n):
        for j in range(n):
            Z=np.zeros((n,n),dtype=object); Z[i,j]=1
            W=Cp[d]@Z.T@Ap[d]
            eq(E(F(W)),h*h*W); eq(F(E(W)),h*h*W)
            eq(R(R(W)),Q(Q(W))-4*h*h*W)
            U=V=W.copy()
            for ell in range(d+1):
                eq(U,h**ell*(Cp[d-ell]@Z.T@Ap[d+ell]))
                eq(V,h**ell*(Cp[d+ell]@Z.T@Ap[d-ell]))
                assert band(U)==band(h**ell*(Cp[d-ell]@Z.T@Ap[d+ell]))
                original_checks+=2
                U=E(U); V=F(V)
    sectors={}
    for eps in (1,-1):
        count=0
        for i in range(n):
            for j in range(i if eps==1 else i+1,n):
                W=np.zeros((n,n),dtype=object)
                W[i,j]=1
                if i!=j: W[j,i]=eps
                eq(E(W).T,eps*F(W))
                eq(Q(W).T,eps*Q(W))
                eq(R(W).T,-eps*R(W))
                U=V=W.copy(); sp=2*W; sm=0*W
                sp_prev=sm_prev=None
                for ell in range(1,d+2):
                    U=E(U); V=F(V)
                    if ell==1: sp_new=Q(W); sm_new=R(W)
                    else:
                        sp_new=Q(sp)-h*h*sp_prev
                        sm_new=Q(sm)-h*h*sm_prev
                    eq(U+V,sp_new); eq(U-V,sm_new)
                    sp_prev,sp=sp,sp_new
                    sm_prev,sm=sm,sm_new
                count+=1
        sectors[str(eps)]=count
    # A deterministic weighted self-adjointness control, unrelated to rank.
    U=np.array([[(i+1)*(j+2)+(i==j) for j in range(n)] for i in range(n)],dtype=object)
    V=np.array([[(-1)**(i+j)*(2*i-j+1) for j in range(n)] for i in range(n)],dtype=object)
    inner=lambda X,Y:sum((X.T@T@Y@T)[i,i] for i in range(n))
    assert inner(E(U),V)==inner(U,E(V))
    assert inner(F(U),V)==inner(U,F(V))
    assert inner(Q(U),V)==inner(U,Q(V))
    assert inner(R(U),V)==inner(U,R(V))
    return {'N':n,'theta':str(h),'d':d,'original_centered_full_basis_checks':original_checks,'symmetric_basis_count':sectors['1'],'skew_basis_count':sectors['-1'],'checks':'PASS','rank_computed':False}

if __name__=='__main__':
    print(json.dumps({'scope':'Transcription controls of exact identities, not an all-size rank certificate.','results':[run(8),run(16)]},indent=2))
