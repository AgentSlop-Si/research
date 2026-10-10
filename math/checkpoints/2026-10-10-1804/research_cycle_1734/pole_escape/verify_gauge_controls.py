"""Fresh exhaustive tests of the valuation-gauge criterion, including zero edges."""
from itertools import product
import json, pathlib, hashlib
root=pathlib.Path(__file__).resolve().parent
# Sources0,1; internal2,3; sinks4,5. Complete adjacent bipartite layers.
edges=[(s,v) for s in (0,1) for v in (2,3)]+[(v,t) for v in (2,3) for t in (4,5)]
checked=integral=0; hashes=hashlib.sha256()
for weights in product((None,-1,0,1),repeat=8):
 finite=[(u,v,w) for (u,v),w in zip(edges,weights) if w is not None]
 sums=[wa+wb for u,v,wa in finite for x,t,wb in finite if v==x]
 expected=all(s>=0 for s in sums)
 # Quotient all four boundary nodes to vertex0. Vertex1,2 are internal.
 q=lambda v: v-1 if v in (2,3) else 0
 qe=[(q(u),q(v),w) for u,v,w in finite]
 d=[0]*3
 for _ in range(2):
  for u,v,w in qe:d[v]=min(d[v],d[u]+w)
 feasible=all(d[v]<=d[u]+w for u,v,w in qe)
 assert feasible==expected
 if feasible:
  h=[x-d[0] for x in d]
  assert h[0]==0
  assert all(w+h[u]-h[v]>=0 for u,v,w in qe)
 # Independent direct enumeration of the two internal integer gauges.
 brute=any(all(w+(a if u==2 else b if u==3 else 0)-(a if v==2 else b if v==3 else 0)>=0 for u,v,w in finite) for a,b in product(range(-2,3),repeat=2))
 assert brute==expected
 checked+=1;integral+=feasible
 hashes.update(bytes(3 if w is None else w+1 for w in weights)+bytes([expected]))
out={'checked_patterns':checked,'integralizable':integral,'nonintegralizable':checked-integral,'zero_edges_included':True,'brute_force_gauge_range':[-2,2],'mismatches':0,'checksum':hashes.hexdigest()}
(root/'gauge_controls_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
