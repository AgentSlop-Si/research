"""Create checkable rank-cut + two-prime Fourier minor certificates."""
import json,sys,time
from pathlib import Path
from research_gate import bitrev, root, det_mod, rank_mod
import networkx as nx
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'fft_scan_network_gate_2026-10-09'))
from scan_flow import make_graph,mincut_bound
from fast_mincut import ScanFlowOracle

def encode(node):
    return list(node)

def decode(obj):
    return tuple(obj)

def get_witness(n):
    if n==64:return list(range(38,64)),list(range(26))
    if n==128:return list(range(43)),list(range(85,128))
    raise ValueError

def certificate(n):
    P=bitrev(n);R,C=get_witness(n);G,big=make_graph(n,[1,1,1],[P,P]);source=('SRC',);sink=('SINK',)
    for j in C:G.add_edge(source,(0,'x',j,'i'),capacity=big)
    for j in R:G.add_edge((2,'y',j,'o'),sink,capacity=big)
    val,(source_part,sink_part)=nx.minimum_cut(G,source,sink,capacity='capacity',flow_func=nx.algorithms.flow.preflow_push)
    val=int(val)
    cap=sum(G[u][v]['capacity'] for u,v in G.edges if u in source_part and v in sink_part)
    assert cap==val
    # Independent graph engine and explicit cut-value reconstruction.
    G2,big2=make_graph(n,[1,1,1],[P,P]);assert big2==big
    fast=ScanFlowOracle(n,[1,1,1],[P,P]).bound(R,C)
    assert fast==val,(n,fast,val)
    assert len(R)==len(C)
    detail=[]
    for p in (12289,65537):
        omega=root(n,p)
        M=[[pow(omega,i*j,p) for j in C] for i in R]
        d=det_mod(M,p);r=rank_mod(M,p)
        assert r==len(R) and d!=0,(n,p,r,d)
        detail.append({'prime':p,'primitive_root':omega,'determinant':d,'rank':r})
    # Store a complete source side partition, smaller than edge enumeration.
    obj={'n':n,'ranks':[1,1,1],'perm':'bit_reversal','rows':R,'columns':C,
         'large_capacity':big,'rank_upper_bound':val,'source_partition':[encode(z) for z in sorted(source_part,key=str)],
         'crossing_edges':[{'u':encode(u),'v':encode(v),'capacity':G[u][v]['capacity']}
             for u,v in G.edges if u in source_part and v in sink_part],
         'primes':detail}
    out=HERE/f'NETWORK_CERTIFICATE_N{n}.json'
    out.write_text(json.dumps(obj,indent=2)+'\n')
    print('N',n,'source_part',len(source_part),'cut',val,'rank',len(R),'primes',detail,'cross_edges',len(obj['crossing_edges']),'bytes',out.stat().st_size,flush=True)
    return obj

if __name__=='__main__':
    certificate(64);certificate(128)
