"""Directed-signal graph cut bound for products of quasiseparable matrices.

Each quasiseparable stage with upper/lower rank at most r is represented as
an input scalar, a diagonal scalar path, and two directional r-register
recurrences.  A minimum s-t cut's capacity upper-bounds the rank of the
specified output-input submatrix, for *every possible* choice of generator
coefficients.  All endpoint orderings and intermediate permutations are
explicit. Only proves necessary constraints, not existence/circuit cost.
"""
from __future__ import annotations
import networkx as nx


def make_graph(n, ranks, shuffles=()):
    t=len(ranks)
    if len(shuffles)!=t-1: raise ValueError('Need t-1 middle permutations')
    big=5*n*(1+sum(ranks))
    G=nx.DiGraph()
    def wire(u,v,cap=big):
        G.add_edge(u,v,capacity=cap)
    for s,r in enumerate(ranks):
        for j in range(n):
            wire((s,'x',j,'i'),(s,'x',j,'o'),1)
            wire((s,'y',j,'i'),(s,'y',j,'o'),1)
            wire((s,'x',j,'o'),(s,'y',j,'i'))
        if r:
            for j in range(1,n):
                wire((s,'f',j,'i'),(s,'f',j,'o'),r)
                wire((s,'x',j-1,'o'),(s,'f',j,'i'))
                wire((s,'f',j,'o'),(s,'y',j,'i'))
                if j<n-1:
                    wire((s,'f',j,'o'),(s,'f',j+1,'i'))
            for j in range(n-2,-1,-1):
                wire((s,'b',j,'i'),(s,'b',j,'o'),r)
                wire((s,'x',j+1,'o'),(s,'b',j,'i'))
                wire((s,'b',j,'o'),(s,'y',j,'i'))
                if j>0:
                    wire((s,'b',j,'o'),(s,'b',j-1,'i'))
    for s,perm in enumerate(shuffles):
        if sorted(perm)!=list(range(n)):raise ValueError('Invalid permutation')
        # perm[j] gives stage-s OUTPUT coordinate which is fed into
        # stage-(s+1) INPUT coordinate j.
        for j,from_j in enumerate(perm):
            wire((s,'y',from_j,'o'),(s+1,'x',j,'i'))
    return G,big


def mincut_bound(G,big,n,t,R,C,flow_func=nx.algorithms.flow.preflow_push):
    g=G.copy();src=('SRC',);sink=('SINK',)
    for j in C: g.add_edge(src,(0,'x',j,'i'),capacity=big)
    for j in R: g.add_edge((t-1,'y',j,'o'),sink,capacity=big)
    v,parts=nx.minimum_cut(g,src,sink,capacity='capacity',flow_func=flow_func)
    return round(v),parts

if __name__=='__main__':
    from two_stage_ct import TwoStage,modular_rank,root,P
    from cut_rank_gate import rank_np
    import random
    for a,b in ((2,2),(4,4),(4,8)):
        ct=TwoStage(a,b);n=ct.n
        graph,inf=make_graph(n,ct.channel_ceiling,[ct.shuffle])
        z=root(n);powers=[pow(z,i,P) for i in range(n)]
        rng=random.Random(n)
        for _ in range(30):
            R=rng.sample(range(n),rng.randrange(1,n+1));C=rng.sample(range(n),rng.randrange(1,n+1))
            actual=rank_np([ct.output_order[j] for j in R],[ct.input_order[j] for j in C],powers)
            upper,_=mincut_bound(graph,inf,n,2,R,C)
            assert upper>=actual,(n,R,C,actual,upper)
        print('PASS',n,'CT rank certificate over 30 random subsets',flush=True)
