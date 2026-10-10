import importlib.util,json,collections
from pathlib import Path
spec=importlib.util.spec_from_file_location('own_gate',str(Path(__file__).with_name('_projective_gate_helpers.py')));h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h);h.p=241
z=json.loads(Path(__file__).with_name('ORDER_SCREEN_RESULTS.json').read_text());B=z['B'];ident=list(range(5))
def decompose(rel):
 adj=[[]for i in range(5)]
 for e,(i,k,L)in enumerate(rel):
  H=h.H(L);assert h.det(H)
  adj[i].append((k,H,e));adj[k].append((i,h.inv(H),e))
 roots=[];belong=[None]*5;T=[None]*5;members=[]
 for root in range(5):
  if belong[root]is not None:continue
  c=len(roots);roots.append(root);queue=[root];belong[root]=c;T[root]=h.eye(2)
  for i in queue:
   for k,H,e in adj[i]:
    if belong[k]is None:belong[k]=c;T[k]=h.mul(H,T[i]);queue.append(k)
  members.append(queue)
 qs=[[]for x in roots]
 for e,(i,k,L)in enumerate(rel):
  R=h.mul(h.tr(T[k]),h.mul(L,T[i]));q=[R[0][0],(R[0][1]+R[1][0])%h.p,R[1][1]];qs[belong[i]].append((e,q))
 domains=[h.domain(q,False)for q in qs]
 return dict(members=members,T=T,domains=domains)
results=[]
for a,b in z['survivors']:
 rel=h.extract(B,ident,z['cycles'][a]['permutation'],ident,z['cycles'][b]['permutation']);d=decompose(rel)
 results.append(dict(first=a,second=b,**d))
Path(__file__).with_name('SURVIVOR_DOMAINS.json').write_text(json.dumps(results,indent=2)+'\n')
print(collections.Counter(tuple((len(m),x['unrestricted'],len(x['g'])-1,x['infinity'])for m,x in zip(d['members'],d['domains']))for d in results))
print(json.dumps(results[0],indent=2))
