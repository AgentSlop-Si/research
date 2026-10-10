"""Compiled integer max-flow oracle for the quasiseparable scan network.

Networkx is used to build the network (once); scipy Dinic handles repeated
small cut queries. Edge capacities are integers, and the result is exact.
"""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
from scan_flow import make_graph


class ScanFlowOracle:
    def __init__(self, n, ranks, shuffles):
        G, big = make_graph(n, ranks, shuffles)
        self.n = n
        self.t = len(ranks)
        self.big = int(big)
        self.nodes = list(G.nodes)
        self.loc = {node: i for i, node in enumerate(self.nodes)}
        self.v = len(self.nodes)
        self.source = self.v
        self.sink = self.v + 1
        ed = [(self.loc[a], self.loc[b], int(attr['capacity'])) for a,b,attr in G.edges(data=True)]
        self.u0 = np.array([u for u,v,w in ed],dtype=np.int32)
        self.v0 = np.array([v for u,v,w in ed],dtype=np.int32)
        self.w0 = np.array([w for u,v,w in ed],dtype=np.int64)
        self.inputs = [self.loc[(0,'x',j,'i')] for j in range(n)]
        self.outputs = [self.loc[(self.t-1,'y',j,'o')] for j in range(n)]
    def bound(self, R, C):
        u=np.concatenate((self.u0,
                          np.full(len(C),self.source,dtype=np.int32),
                          np.array([self.outputs[j] for j in R],dtype=np.int32)))
        v=np.concatenate((self.v0,
                          np.array([self.inputs[j] for j in C],dtype=np.int32),
                          np.full(len(R),self.sink,dtype=np.int32)))
        w=np.concatenate((self.w0,
                          np.full(len(C),self.big,dtype=np.int64),
                          np.full(len(R),self.big,dtype=np.int64)))
        A=csr_matrix((w,(u,v)),shape=(self.v+2,self.v+2))
        return int(maximum_flow(A,self.source,self.sink,method='dinic').flow_value)

if __name__ == '__main__':
    import random
    from scan_flow import mincut_bound
    for n in (8,16,32,64):
        rng=random.Random(n)
        p=list(range(n));rng.shuffle(p)
        q=ScanFlowOracle(n,[2,2],[p]);G,big=make_graph(n,[2,2],[p]);
        for _ in range(16):
            R=rng.sample(range(n),rng.randrange(1,n+1));C=rng.sample(range(n),rng.randrange(1,n+1))
            assert q.bound(R,C)==mincut_bound(G,big,n,2,R,C)[0]
        print('PASS scipy/networkx',n,flush=True)
