"""Independent exact difference-constraint controls and tropical witness audit.
No source or other author's program is imported or executed.
"""
from pathlib import Path
import json, itertools, random, hashlib
P=Path(__file__).resolve().parent
SOURCE=Path('research_cycle_1635/v34_independent_audit/source/extracted/fft_cyclotomic_zero_forcing_v34/topology_11.json')

def check_graph(sizes, weighted_edges):
    # Edges (layer, source, destination, integer valuation); None means zero.
    vertices=[(l,i) for l,n in enumerate(sizes) for i in range(n)]
    edges=[((l,u),(l+1,v),w) for l,u,v,w in weighted_edges if w is not None]
    boundary={v for v in vertices if v[0] in (0,len(sizes)-1)}
    # Forward enumerate all surviving boundary-to-boundary paths.
    minimum=[]
    for s in range(sizes[0]):
        paths={(0,s):[0]}
        for l in range(len(sizes)-1):
            for u,v,w in edges:
                if u[0]==l:
                    paths.setdefault(v,[]).extend(x+w for x in paths.get(u,[]))
        for t in range(sizes[-1]):
            minimum.extend(paths.get((len(sizes)-1,t),[]))
    path_feasible=all(x>=0 for x in minimum)
    # A different implementation: impose all boundary h=0 by contraction,
    # then use Bellman-Ford with a zero initial distance at EVERY vertex.
    q=lambda v: 'boundary' if v in boundary else v
    quotient=set(map(q,vertices));d={v:0 for v in quotient}
    es=[(q(u),q(v),w) for u,v,w in edges]
    negative=False
    for k in range(len(quotient)):
        changed=False
        for u,v,w in es:
            if d[v]>d[u]+w:
                d[v]=d[u]+w;changed=True
        if not changed:break
    else:
        negative=changed
    assert path_feasible == (not negative)
    if not negative:
        h={v:d[q(v)]-d['boundary'] for v in vertices}
        assert all(h[b]==0 for b in boundary)
        assert all(w+h[u]-h[v]>=0 for u,v,w in edges)
    return {'path_feasible':path_feasible,'surviving_paths':len(minimum),'minimum_path':min(minimum,default=None)}

cases=0; feasible=0; no_paths=0
# Exhaust every deletion/valuation pattern on a two-branch diamond.
for vals in itertools.product([None,-1,0,1],repeat=4):
    result=check_graph([1,2,1],[(0,0,0,vals[0]),(0,0,1,vals[1]),(1,0,0,vals[2]),(1,1,0,vals[3])])
    cases+=1;feasible+=result['path_feasible'];no_paths+=not result['surviving_paths']
# Includes isolated vertices, dead ends, source-unreachable/sink-reachable
# branches, and completely boundary-disconnected internal components.
rng=random.Random(873450)
for unused in range(2000):
    sizes=[2,3,3,2]
    edges=[(l,u,v,rng.choice([None,None,-3,-2,-1,0,1,2,3])) for l in range(3) for u in range(sizes[l]) for v in range(sizes[l+1])]
    result=check_graph(sizes,edges)
    cases+=1;feasible+=result['path_feasible'];no_paths+=not result['surviving_paths']

out={'status':'PASS','exact_integer_gauge_control_cases':cases,'feasible_cases':feasible,'no_surviving_path_cases':no_paths,'source_programs_executed_or_imported':False}
T=json.loads(SOURCE.read_text());L=T['layers'];n=T['n']
paths={}
# Build adjacency once, then independently walk from inputs to outputs.
adj=[]
for layer in L:
    a={i:[] for i in range(n)}
    for k,(v,u) in enumerate(layer):a[u].append((v,k))
    adj.append(a)
for j in range(n):
    for u,a in adj[0][j]:
        for v,b in adj[1][u]:
            for i,c in adj[2][v]:paths.setdefault((i,j),[]).append((a,33+b,66+c))
assert len(paths)==121 and sum(map(len,paths.values()))==297
out.update({'topology_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'entry_count':len(paths),'path_count':sum(map(len,paths.values())),'unique_entries':sum(len(ps)==1 for ps in paths.values())})
WITNESS=Path('research_cycle_1734/pole_escape/tropical_search_W2.json')
if WITNESS.exists():
    data=json.loads(WITNESS.read_text())
    if 'weights' in data:
        w=data['weights'];assert len(w)==99 and all(type(x) is int for x in w)
        entries=[]; violations=[]
        for (i,j),ps in sorted(paths.items()):
            vals=[sum(w[e] for e in path) for path in ps]
            m=min([0]+vals); count=sum(x==m for x in [0]+vals)
            if count<2:violations.append([i,j,vals])
            entries.append({'output':i,'input':j,'path_values':vals,'minimum':m,'minimum_count_including_target':count,'paths':ps})
        negative=[x for x in entries if x['minimum']<0]
        assert not violations and negative
        out.update({'tropical_witness_status':'PASS','witness_sha256':hashlib.sha256(WITNESS.read_bytes()).hexdigest(),'negative_entries':len(negative),'minimum_path_weight':min(e['minimum'] for e in entries),'exact_tropical_entries':entries,'weights':w})
    else:out['tropical_witness_status']='No candidate in search receipt; not a no-go proof.'
else:out['tropical_witness_status']='Awaiting witness data.'
(P/'REVIEW_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['exact_tropical_entries','weights']},indent=2))
