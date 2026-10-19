#!/usr/bin/env python3
"""Exact controls for the classical Woodbury application; no Jacobian rank."""
import json
import sympy as sp
from checks import anchor
from commutator_checks import support, compressed

results=[]
for n in (8,16,32):
    m=n.bit_length()-1
    t,p,j,h=anchor(n)
    T,P,J=map(lambda x:sp.Matrix(x.tolist()),(t,p,j))
    A=T*P; B=A*A; Binv=P*J*P*J/(h*h)
    assert B*Binv==sp.eye(n)
    S,Ks=compressed(m)
    E=sp.zeros(n,len(S))
    for k,x in enumerate(S): E[x,k]=1
    assert B-B.T==E*Ks*E.T
    G=E.T*Binv*E; M=sp.eye(len(S))-Ks*G
    determinant=M.det(method='domain-ge')
    assert determinant==1
    Minv=M.inv(method='DM')
    corrected=Binv+Binv*E*Minv*Ks*E.T*Binv
    assert B.T*corrected==sp.eye(n)
    assert corrected==Binv.T
    W=sp.Matrix(n,n,lambda i,j:(i+1)*(j+2)+(i==j))
    D2=Binv.T*W*B
    assert D2==Binv*W*B+Binv*E*Minv*Ks*E.T*Binv*W*B
    results.append({'N':n,'core_size':len(S),'det_core':str(determinant),'full_inverse_identity':'PASS','dual_squared_identity':'PASS','rank_H_computed':False})
print(json.dumps({'scope':'Finite transcription checks of an independently proved all-size classical identity; not endpoint-rank evidence.','results':results},indent=2))
