#!/usr/bin/env python3
"""Independent scalar-network cut certificate using Edmonds-Karp."""
import json,collections,pathlib
ROOT=pathlib.Path(__file__).resolve().parent

def reverse(j,n):return int(format(j,f'0{n.bit_length()-1}b')[::-1],2)
def check(n,depth,w):
 arcs=[];nodes=set()
 def add(a,b,c):nodes.update([a,b]);arcs.append((a,b,c))
 def key(s,kind,i,port):return(s,kind,i,port)
 for s in range(depth):
  for kind,indices in [('x',range(n)),('y',range(n)),('l',range(1,n)),('u',range(n-1))]:
   for i in indices:add(key(s,kind,i,0),key(s,kind,i,1),1)
  def wire(a,b):add(a+(1,),b+(0,),n+1)
  for i in range(n):wire((s,'x',i),(s,'y',i))
  for i in range(1,n):
   wire((s,'x',i-1),(s,'l',i));wire((s,'l',i),(s,'y',i))
   if i<n-1:wire((s,'l',i),(s,'l',i+1))
  for i in range(n-1):
   wire((s,'x',i+1),(s,'u',i));wire((s,'u',i),(s,'y',i))
   if i>0:wire((s,'u',i),(s,'u',i-1))
  if s+1<depth:
   for i in range(n):wire((s,'y',i),(s+1,'x',reverse(i,n)))
 source=(-1,'source',0,0);sink=(depth,'sink',0,0)
 for i in range(n-w,n):add(source,key(0,'x',i,0),1)
 for i in range(w):add(key(depth-1,'y',i,1),sink,1)
 adj={x:set() for x in nodes};cap={}
 for a,b,c in arcs:adj[a].add(b);adj[b].add(a);cap[a,b]=cap.get((a,b),0)+c;cap.setdefault((b,a),0)
 residual=cap.copy();flow=0
 while True:
  pred={source:None};q=collections.deque([source])
  while q and sink not in pred:
   a=q.popleft()
   for b in sorted(adj[a]):
    if b not in pred and residual[a,b]:pred[b]=a;q.append(b)
  if sink not in pred:break
  d=n+1;b=sink
  while b!=source:a=pred[b];d=min(d,residual[a,b]);b=a
  b=sink
  while b!=source:a=pred[b];residual[a,b]-=d;residual[b,a]+=d;b=a
  flow+=d
 reachable=set(pred);cut=[(a,b,c) for a,b,c in arcs if a in reachable and b not in reachable]
 assert sum(c for a,b,c in cut)==flow
 # Independently validate the cut disconnects the original directed graph.
 removed={(a,b) for a,b,c in cut};seen={source};q=collections.deque([source])
 forward=collections.defaultdict(list)
 for a,b,c in arcs:
  if (a,b) not in removed:forward[a].append(b)
 while q:
  for b in forward[q.popleft()]:
   if b not in seen:seen.add(b);q.append(b)
 assert sink not in seen
 return {'N':n,'stages':depth,'I':[0,w],'J':[n-w,n],'capacity':flow,'deficit':w-flow,'cut':cut,'cut_disconnection_verified':True}

out={'method':'Independently rebuilt scalar scan graph; Edmonds-Karp and explicit cut-disconnection check','cases':[check(n,d,w) for n,d,w in [(64,3,21),(128,3,42),(128,3,43),(128,4,42),(128,4,43),(128,4,64)]]}
(ROOT/'INDEPENDENT_NETWORK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps([{k:v for k,v in x.items() if k!='cut'} for x in out['cases']],indent=2))
