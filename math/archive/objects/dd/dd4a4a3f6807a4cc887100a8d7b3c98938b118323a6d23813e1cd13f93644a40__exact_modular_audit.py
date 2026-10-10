"""Independent exact arithmetic audit of the sum-product/Taylor-jet identity.
All calculations are in the TIME DOMAIN over Z/97Z, independent of scipy.fft.
"""
from __future__ import annotations
import itertools
from collections import defaultdict
import numpy as np
from algebra_fft import AlgebraFFT

MOD=97

def conv(a,b):
    n=len(a)
    out=[0]*n
    for j in range(n):
        for k in range(n):
            out[(j+k)%n]=(out[(j+k)%n]+a[j]*b[k])%MOD
    return out

def delta(n,index=0,coeff=1):
    arr=[0]*n
    arr[index%n]=coeff%MOD
    return arr

def add(*arrays):
    if not arrays:return []
    n=len(arrays[0]);return [sum(a[j] for a in arrays)%MOD for j in range(n)]

def scale(a,c):return [(x*int(c))%MOD for x in a]

def direct(engine,root,overrides):
    memo={}; n=engine.n
    for uid in engine._topological(root):
        nd=engine.nodes[uid]
        if nd.op=='seed':v=overrides.get(uid,list(map(int,engine._seeds[uid])))
        elif nd.op=='const':v=delta(n,coeff=int(nd.scalar))
        elif nd.op=='impulse':v=delta(n,nd.index,int(nd.scalar))
        elif nd.op=='scale':v=scale(memo[nd.args[0]],nd.scalar)
        elif nd.op=='sum':v=add(*(scale(memo[u],w) for u,w in zip(nd.args,nd.weights)))
        else:
            v=delta(n,coeff=int(nd.scalar))
            for ch in nd.args:v=conv(v,memo[ch])
        memo[uid]=v
    return memo[root]

def jet(engine,root,target):
    memo={};n=engine.n
    for uid in engine._topological(root):
        nd=engine.nodes[uid]
        if nd.op=='seed':
            v=list(map(int,engine._seeds[uid]))
            memo[uid]=[v,delta(n)] if uid==target else [v]
        elif nd.op=='const':memo[uid]=[delta(n,coeff=int(nd.scalar))]
        elif nd.op=='impulse':memo[uid]=[delta(n,nd.index,int(nd.scalar))]
        elif nd.op=='scale':memo[uid]=[scale(a,nd.scalar) for a in memo[nd.args[0]]]
        elif nd.op=='sum':
            dim=max(len(memo[u]) for u in nd.args)
            v=[delta(n,coeff=0) for _ in range(dim)]
            for u,w in zip(nd.args,nd.weights):
                for j,a in enumerate(memo[u]):v[j]=add(v[j],scale(a,w))
            memo[uid]=v
        else:
            v=[delta(n,coeff=int(nd.scalar))]
            for u in nd.args:
                nxt=[delta(n,coeff=0) for _ in range(len(v)+len(memo[u])-1)]
                for j,a in enumerate(v):
                    for k,b in enumerate(memo[u]):nxt[j+k]=add(nxt[j+k],conv(a,b))
                v=nxt
            memo[uid]=v
    return memo[root]

def check(seed=20261009, trials=240):
    rng=np.random.default_rng(seed)
    n=8
    engine=AlgebraFFT(n)
    A=engine.signal(rng.integers(0,10,n),'A')
    B=engine.signal(rng.integers(0,10,n),'B')
    C=engine.signal(rng.integers(0,10,n),'C')
    D=engine.signal(rng.integers(0,10,n),'D')
    # Many repeated variables and DAG subexpressions.
    shared=engine.add(engine.mul(A,B),engine.mul(C,D))
    formulas=[engine.add(shared,engine.mul(A,A),engine.mul(A,B,C)),
              engine.mul(engine.add(A,B),engine.add(A,C)),
              engine.add(engine.mul(A,A,A),engine.mul(shared,shared),engine.scale(A,-2)),
              engine.add(engine.mul(A,B),engine.mul(A,B),engine.mul(C,D))]
    counted=0
    for root in formulas:
        jets=jet(engine,root,A)
        assert len(jets)==engine.degree_in(root,A)+1
        original=direct(engine,root,{})
        assert jets[0]==original
        for _ in range(trials//len(formulas)):
            t=int(rng.integers(0,n)); dv=int(rng.integers(-8,9))
            a=list(map(int,engine._seeds[A]));a[t]=(a[t]+dv)%MOD
            expected=direct(engine,root,{A:a})
            updated=original[:]
            for h in range(1,len(jets)):
                correction=scale(jets[h],dv**h)
                updated=add(updated,correction[-(h*t)%n:]+correction[:-(h*t)%n] if (h*t)%n else correction)
            assert updated==expected, f'single-edited mismatch {root=} {t=} {dv=}'
            # Multi-edit corrections, including all nonlinear cross terms.
            edits={int(rng.integers(0,n)):int(rng.integers(-3,4)) for _ in range(3)}
            edited=list(map(int,engine._seeds[A]));u=delta(n,coeff=0)
            for pos,value in edits.items():
                edited[pos]=(edited[pos]+value)%MOD
                u[pos]=value%MOD
            expected=direct(engine,root,{A:edited})
            correction=delta(n,coeff=1)
            total=jets[0][:]
            for h in range(1,len(jets)):
                correction=conv(correction,u)
                total=add(total,conv(jets[h],correction))
            assert total==expected, f'multi-edited mismatch {root=}'
            counted+=2
    print(f'EXACT MODULAR AUDIT PASSED: {counted} independent update comparisons over F_{MOD}; 4 expressions; degrees 1–4')
    return counted

if __name__=='__main__':check()
