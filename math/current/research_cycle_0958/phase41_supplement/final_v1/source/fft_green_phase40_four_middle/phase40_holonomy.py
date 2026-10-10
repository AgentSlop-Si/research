"""Phase 40: simultaneous graph-gauge normal form for independently ordered
weighted cyclic Green operators, with disjoint-set spanning-tree selection.

All phase arithmetic is exact in F_p.  The graph-gauge construction is a
standard cycle-space/coboundary principle; its use here is project-specific.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
import random

@dataclass(frozen=True)
class Edge:
    cycle:int
    target:int
    source:int
    weight:int

class DSU:
    def __init__(self,n):
        self.p=list(range(n));self.sz=[1]*n
    def find(self,x):
        while x!=self.p[x]:
            self.p[x]=self.p[self.p[x]]
            x=self.p[x]
        return x
    def union(self,a,b):
        a=self.find(a);b=self.find(b)
        if a==b:return False
        if self.sz[a]<self.sz[b]:a,b=b,a
        self.p[b]=a;self.sz[a]+=self.sz[b]
        return True

def cycle_edges(cycle,weights,cycle_id=0):
    n=len(cycle)
    assert set(cycle)==set(range(n)) and len(weights)==n
    return [Edge(cycle_id,cycle[j],cycle[j-1],int(weights[j])) for j in range(n)]

def normalize_gauge(n,cycles,weights,p):
    """Return D and canonical edge weights with all spanning-tree weights 1.

    Conjugation: W_original = diag(D) W_canonical diag(D)^(-1).
    Every edge outside the union-find spanning tree is a gauge invariant.
    """
    assert len(cycles)==len(weights)>=1
    E=[edge for s,(c,w) in enumerate(zip(cycles,weights))
       for edge in cycle_edges(c,w,s)]
    uf=DSU(n);tree=[];chord=[]
    for i,e in enumerate(E):
        assert e.weight%p!=0
        (tree if uf.union(e.source,e.target) else chord).append(i)
    assert len(tree)==n-1 and len(chord)==len(E)-n+1
    adj=[[] for _ in range(n)]
    for k in tree:
        e=E[k];v,u=e.target,e.source
        adj[u].append((v,e.weight%p))
        adj[v].append((u,pow(e.weight,p-2,p)))
    potential=[0]*n;potential[0]=1;Q=deque([0]);seen=1
    while Q:
        u=Q.popleft()
        for v,ratio in adj[u]:
            if potential[v]!=0:continue
            potential[v]=potential[u]*ratio%p
            seen+=1;Q.append(v)
    assert seen==n
    normalized=[e.weight%p*potential[e.source]%p*pow(potential[e.target],p-2,p)%p for e in E]
    assert all(normalized[i]==1 for i in tree)
    return dict(potential=potential,edge_weights=normalized,
                tree=tree,chord=chord,edges=E,holonomies=[normalized[i] for i in chord],
                independent_phase_count=len(chord))

def weighted_green_apply(cycle,weights,x,p):
    """O(N) arithmetic solve (I-W)x_out=x for one weighted cyclic shift.

    weights[j] labels directed edge cycle[j-1] -> cycle[j].
    """
    n=len(cycle)
    xs=[int(x[j])%p for j in cycle]
    h=0;pref=1
    for j in range(n-1,-1,-1):
        h=(h+pref*xs[j])%p
        pref=pref*int(weights[j])%p
    if pref==1:raise ValueError('Singular Green denominator (cycle holonomy is 1)')
    last=h*pow((1-pref)%p,p-2,p)%p
    prev=last;out=[0]*n
    for j in range(n):
        prev=(xs[j]+int(weights[j])*prev)%p
        out[cycle[j]]=prev
    assert prev==last
    return out

def double_green_apply(cycles,weights,x,p):
    out=[0]*len(x)
    for cy,ws in zip(cycles,weights):
        q=weighted_green_apply(cy,ws,x,p)
        out=[(u+v)%p for u,v in zip(out,q)]
    return out

def random_problem(n,p,seed=40040):
    rng=random.Random(seed+n)
    c0=list(range(n));c1=list(range(n));rng.shuffle(c1)
    weights_rng=random.Random(seed+7919+n)
    if n>=5:
        assert c0!=c1
    cycles=[c0,c1]
    weights=[]
    for cy in cycles:
        w=[weights_rng.randrange(2,100000) for _ in range(n)]
        prod=1
        for v in w:prod=prod*v%p
        if prod==1:w[0]=2*w[0]%p
        weights.append(w)
    return cycles,weights


def verify_problem(n,p,seed=40040):
    cycles,weights=random_problem(n,p,seed)
    canon=normalize_gauge(n,cycles,weights,p)
    D=canon['potential'];nws=[canon['edge_weights'][k*n:(k+1)*n]
         for k in range(len(cycles))]
    rng=random.Random(seed+2*n+p)
    x=[rng.randrange(p) for _ in range(n)]
    lhs=double_green_apply(cycles,weights,x,p)
    dx=[v*pow(d,p-2,p)%p for v,d in zip(x,D)]
    rhs=[v*d%p for v,d in zip(double_green_apply(cycles,nws,dx,p),D)]
    assert lhs==rhs
    # Independent vertex gauge: canonically normalized chord weights unchanged.
    K=[rng.randrange(1,p) for _ in range(n)]
    gauged=[[w[j]*K[cy[j]]%p*pow(K[cy[j-1]],p-2,p)%p
             for j in range(n)] for cy,w in zip(cycles,weights)]
    canon2=normalize_gauge(n,cycles,gauged,p)
    assert canon2['holonomies']==canon['holonomies']
    assert len(canon['holonomies'])==n+1
    return {'N':n,'prime':p,'edges':2*n,'tree_edges':n-1,
            'independent_phase_invariants':n+1,
            'simultaneous_conjugacy_exact':True,
            'arbitrary_vertex_gauge_invariant':True,
            'matrix_free_round_trip':True}

if __name__=='__main__':
    import json
    for p in (998244353,2013265921):
        for n in (8,16,64,256):
            print(json.dumps(verify_problem(n,p)))
