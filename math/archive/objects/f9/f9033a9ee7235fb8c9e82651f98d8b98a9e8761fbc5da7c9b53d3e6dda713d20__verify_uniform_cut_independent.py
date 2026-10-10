"""Independent path-disconnection verification of uniform FFT rank-cut certificate.

This verifier constructs the entire directed scalar dependency DAG from scratch.
It does not import or use the old network-flow implementation. The retained
edges are an overapproximation of *any* rank-one quasiseparable stage's
forward/backward generator realization.
"""
from collections import defaultdict,deque
from research_gate import bitrev
from uniform_cut import cut_sets,wire_list

def graph(n,removed):
    perm=bitrev(n)
    adj=defaultdict(list)
    def edge(u,v):adj[u].append(v)
    def channel(s,typ,j):
        if (s,typ,j) not in removed:
            edge((s,typ,j,0),(s,typ,j,1))
    for s in range(3):
        for j in range(n):
            channel(s,'x',j)
            channel(s,'y',j)
            edge((s,'x',j,1),(s,'y',j,0))
        for j in range(1,n):
            channel(s,'f',j)
            edge((s,'x',j-1,1),(s,'f',j,0))
            edge((s,'f',j,1),(s,'y',j,0))
            if j<n-1:
                edge((s,'f',j,1),(s,'f',j+1,0))
        for j in range(n-2,-1,-1):
            channel(s,'b',j)
            edge((s,'x',j+1,1),(s,'b',j,0))
            edge((s,'b',j,1),(s,'y',j,0))
            if j>0:
                edge((s,'b',j,1),(s,'b',j-1,0))
    for s in range(2):
        for j in range(n):
            edge((s,'y',perm[j],1),(s+1,'x',j,0))
    return adj

def has_source_target_path(n,removed):
    a=cut_sets(n)
    adj=graph(n,removed)
    starts=[(0,'x',j,0) for j in sorted(a['sources'])]
    targets={(2,'y',j,1) for j in a['targets']}
    Q=deque(starts);visited=set(starts)
    while Q:
        u=Q.popleft()
        if u in targets:return True
        for v in adj[u]:
            if v not in visited:
                visited.add(v);Q.append(v)
    return False

def verify(n):
    cut=set(wire_list(n))
    assert len(cut)==12*(n//32)+1
    assert has_source_target_path(n,set()),'graph check must have uncensored signal'
    assert not has_source_target_path(n,cut),'PROPOSED CUT FAILED'
    return {'n':n,'cut_channels':len(cut),'disconnected':True}

if __name__=='__main__':
    for n in (32,64,128,256,512):
        print(verify(n),flush=True)
