"""Independent max-flow check for the scalar scan-network cut at N=256.

Model: two one-channel directional recurrence wires per QS1 stage, input and
output scalar wires, diagonal connections, and exact interstage permutations.
The minimum source-to-output cut upper-bounds submatrix rank.
"""
from __future__ import annotations
import numpy as np
import networkx as nx
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow


def exact_mincut(n,ranks,shuffles,rows,cols):
    if len(shuffles)!=len(ranks)-1:raise ValueError('incorrect shuffle count')
    big=5*n*(1+sum(ranks))
    G=nx.DiGraph()
    def edge(u,v,cap=big):G.add_edge(u,v,capacity=cap)
    t=len(ranks)
    for s,r in enumerate(ranks):
        for j in range(n):
            edge((s,'x',j,'i'),(s,'x',j,'o'),1)
            edge((s,'y',j,'i'),(s,'y',j,'o'),1)
            edge((s,'x',j,'o'),(s,'y',j,'i'))
        for j in range(1,n):
            edge((s,'f',j,'i'),(s,'f',j,'o'),r)
            edge((s,'x',j-1,'o'),(s,'f',j,'i'))
            edge((s,'f',j,'o'),(s,'y',j,'i'))
            if j<n-1:edge((s,'f',j,'o'),(s,'f',j+1,'i'))
        for j in range(n-2,-1,-1):
            edge((s,'b',j,'i'),(s,'b',j,'o'),r)
            edge((s,'x',j+1,'o'),(s,'b',j,'i'))
            edge((s,'b',j,'o'),(s,'y',j,'i'))
            if j>0:edge((s,'b',j,'o'),(s,'b',j-1,'i'))
    for s,p in enumerate(shuffles):
        for j,source in enumerate(p):
            edge((s,'y',int(source),'o'),(s+1,'x',j,'i'))
    nodes=list(G.nodes()); id_by_name={name:i for i,name in enumerate(nodes)}
    source=len(nodes);sink=source+1
    er=[]
    for a,b,data in G.edges(data=True):er.append((id_by_name[a],id_by_name[b],int(data['capacity'])))
    for c in cols:er.append((source,id_by_name[(0,'x',int(c),'i')],big))
    for r in rows:er.append((id_by_name[(t-1,'y',int(r),'o')],sink,big))
    ii=np.array([e[0] for e in er],dtype=np.int32)
    jj=np.array([e[1] for e in er],dtype=np.int32)
    vv=np.array([e[2] for e in er],dtype=np.int64)
    a=csr_matrix((vv,(ii,jj)),shape=(sink+1,sink+1))
    return int(maximum_flow(a,source,sink,method='dinic').flow_value)
