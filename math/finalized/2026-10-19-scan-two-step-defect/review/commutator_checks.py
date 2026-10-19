#!/usr/bin/env python3
"""Fresh sparse check of the two-step defect; never constructs H_N."""
from collections import defaultdict
import sympy as sp
import json

def rev(x,m): return int(format(x,f'0{m}b')[::-1],2)
def applyT(v,n):
    w=defaultdict(int)
    for x,a in v.items():
        w[x]+=(4 if x==0 else 3)*a
        if x: w[x-1]+=a
        if x+1<n: w[x+1]+=a
    return {x:a for x,a in w.items() if a}
def applyP(v,m): return {rev(x,m):a for x,a in v.items()}
def applyV(v,m): return applyP(applyT(applyP(v,m),1<<m),m)
def defect(x,m):
    n=1<<m
    v=applyT(applyV({x:1},m),n)
    w=applyV(applyT({x:1},n),m)
    for y,a in w.items(): v[y]=v.get(y,0)-a
    return {y:a for y,a in v.items() if a}
def support(m):
    n=1<<m
    return sorted({2**r-1 for r in range(m+1)}|{n-2**r for r in range(m+1)}|{2**r for r in range(m)}|{n-1-2**r for r in range(m)})
def compressed(m):
    S=support(m); ix={x:i for i,x in enumerate(S)}; M=sp.zeros(len(S))
    for x in S:
        for y,a in defect(x,m).items():
            assert y in ix
            M[ix[y],ix[x]]=a
    assert M==-M.T
    return S,M

if __name__=='__main__':
    result=[]
    for m in range(3,16):
        S,M=compressed(m)
        if m<=11:
            assert all(not defect(x,m) for x in range(1<<m) if x not in S)
        r=M.rank(); expected=4*m-(6 if m%2==0 else 8)
        assert len(S)==4*m-4
        assert r==expected,(m,r,expected)
        result.append({'m':m,'N':1<<m,'support_size':len(S),'rank_Q':r,'full_complement_checked':m<=11})
    print(json.dumps({'scope':'New two-step commutator only; these finite checks do not prove the rank formula or any Jacobian rank.','results':result},indent=2))
