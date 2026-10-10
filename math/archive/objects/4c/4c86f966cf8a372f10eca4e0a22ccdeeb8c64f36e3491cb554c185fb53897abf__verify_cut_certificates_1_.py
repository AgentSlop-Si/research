"""Independent, standard-library-only verification of exact four-stage cuts.

Does not call a maxflow package. Builds stage dependency edges separately from
research's optimization graph, deletes specified scalar wires, and checks
source-to-target nonreachability plus finite-field Fourier determinants.
"""
import collections
import json
from pathlib import Path
from central_partition import bitrev,partition,modular_fft_minor,primitive_root_of_unity

HERE=Path(__file__).resolve().parent

def independent_graph(n,t,shuffles):
    out=collections.defaultdict(list)
    cap={}
    def edge(u,v,c):
        assert (u,v) not in cap
        cap[(u,v)]=c;out[u].append(v)
    for s in range(t):
        for j in range(n):
            edge((s,'x',j,'i'),(s,'x',j,'o'),1)
            edge((s,'y',j,'i'),(s,'y',j,'o'),1)
            edge((s,'x',j,'o'),(s,'y',j,'i'),None)
        for j in range(1,n):
            edge((s,'f',j,'i'),(s,'f',j,'o'),1)
            edge((s,'x',j-1,'o'),(s,'f',j,'i'),None)
            edge((s,'f',j,'o'),(s,'y',j,'i'),None)
            if j<n-1:edge((s,'f',j,'o'),(s,'f',j+1,'i'),None)
        for j in range(n-2,-1,-1):
            edge((s,'b',j,'i'),(s,'b',j,'o'),1)
            edge((s,'x',j+1,'o'),(s,'b',j,'i'),None)
            edge((s,'b',j,'o'),(s,'y',j,'i'),None)
            if j>0:edge((s,'b',j,'o'),(s,'b',j-1,'i'),None)
    for s,p in enumerate(shuffles):
        for j in range(n):edge((s,'y',p[j],'o'),(s+1,'x',j,'i'),None)
    return out,cap

def verify_one(n,kind='all_bitrev'):
    path=HERE/f'EXACT_NETWORK_CERTIFICATE_N{n}_{kind}.json'
    obj=json.loads(path.read_text());assert obj['n']==n
    A,B,d,_=partition(n)
    # Verify the recorded permutations are exactly the advertised bit operations.
    k=n.bit_length()-1;m=k//2;P=bitrev(n)
    if kind=='all_bitrev': perm=[P]*3
    elif kind=='middle_rotate':perm=[P,[((P[j]<<1)&(n-1))|(P[j]>>(k-1)) for j in range(n)],P]
    elif kind=='middle_xor':perm=[P,[P[j]^(((P[j]>>(m-1))&1)<<m) for j in range(n)],P]
    else:raise ValueError(kind)
    assert obj['shuffles']==perm
    graph,caps=independent_graph(n,4,perm)
    forbidden=set()
    for e in obj['cut_edges']:
        a=tuple(e['from']);b=tuple(e['to'])
        assert (a,b) in caps and caps[(a,b)]==e['capacity']==1
        assert (a,b) not in forbidden
        forbidden.add((a,b))
    assert len(forbidden)==obj['upper_rank']
    if kind=='all_bitrev':assert obj['upper_rank']==4*d
    seen=set((0,'x',i,'i') for i in B)
    q=collections.deque(seen)
    while q:
        node=q.popleft()
        for nex in graph.get(node,()):
            if (node,nex) not in forbidden and nex not in seen:
                seen.add(nex);q.append(nex)
    bad=[i for i in A if (3,'y',i,'o') in seen]
    assert not bad,bad
    assert obj['fourier_rank']==n//2
    for entry in obj['modular_determinants']:
        p=entry['prime'];w=entry['omega']
        assert w==primitive_root_of_unity(n,p)
        assert modular_fft_minor(n,p)==entry['determinant']!=0
    print('VERIFIED n',n,kind,'cut edges',len(forbidden),'unreachable outputs',len(A),
          'Fourier rank',n//2,'two determinants valid',flush=True)

if __name__=='__main__':
 for n in (128,256):verify_one(n)
 for kind in ('middle_rotate','middle_xor'):verify_one(256,kind)
