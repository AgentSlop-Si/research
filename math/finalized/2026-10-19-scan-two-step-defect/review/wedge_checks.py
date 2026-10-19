#!/usr/bin/env python3
"""Independent literal check of report equation (2.1) and modular ranks."""
import json
from commutator_checks import compressed,sp


def rankmod(M,p):
    M=[[int(x)%p for x in row] for row in M.tolist()]
    r=0
    for c in range(len(M[0])):
        piv=next((i for i in range(r,len(M)) if M[i][c]),None)
        if piv is None: continue
        M[piv],M[r]=M[r],M[piv]
        scale=pow(M[r][c],-1,p)
        M[r]=[(a*scale)%p for a in M[r]]
        for i in range(r+1,len(M)):
            scale=M[i][c]
            M[i]=[(a-scale*b)%p for a,b in zip(M[i],M[r])]
        r+=1
    return r

results=[]
for m in range(3,18):
    n=1<<m; S,K=compressed(m); ix={x:i for i,x in enumerate(S)}; W=sp.zeros(len(S))
    def wedge(x,y,a=1):
        W[ix[x],ix[y]]+=a; W[ix[y],ix[x]]-=a
    for r in range(1,m-1):
        wedge(2**r-1,n-2**(r+1))
        wedge(2**(r+1)-1,n-2**r,-1)
    for r in range(m-1):
        wedge(2**r,n-1-2**(r+1),-1)
        wedge(2**(r+1),n-1-2**r)
    for x,a in [(1,-1),(2**(m-1)-1,-1),(n-2,1),(n-2**(m-1),1)]: wedge(0,x,a)
    wedge(1,n-1,-1); wedge(n-2**(m-1),n-1)
    assert W==K
    ranks={str(p):rankmod(K,p) for p in [2,3,5,7]}
    expected=4*m-(6 if m%2==0 else 8)
    assert all(r==expected for r in ranks.values())
    assert all(any(K[i,j] in (1,-1) for j in range(len(S))) for i in range(len(S)))
    results.append({'m':m,'literal_report_equation_2_1':'PASS','modular_ranks':ranks})
print(json.dumps({'scope':'Transcription and field controls only; the all-field conclusion follows from the division-free kernel parametrization.','checks':results},indent=2))
