"""Fresh bounded integer tropical-feasibility search; does not import source code."""
import json, pathlib, sys, time
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix
ROOT=pathlib.Path(__file__).resolve().parent
T=json.loads((ROOT/'topology_11.json').read_text())
L=T['layers']; n=T['n']
paths={}
for i in range(n):
 for j in range(n):
  paths[i,j]=[(a,33+b,66+c) for a,(r,s) in enumerate(L[0]) if s==j for b,(t,u) in enumerate(L[1]) if u==r for c,(v,w) in enumerate(L[2]) if w==t and v==i]
assert sum(map(len,paths.values()))==297
W=int(sys.argv[1]) if len(sys.argv)>1 else 2
LIMIT=float(sys.argv[2]) if len(sys.argv)>2 else 90
# Integer edge weights, one minimum per equation, binary equal-min indicators.
N=99+121+sum(len(p)+1 for p in paths.values())
lb=np.zeros(N); ub=np.ones(N); lb[:99]=-W; ub[:99]=W
lb[99:220]=-3*W; ub[99:220]=0
c=np.zeros(N); c[99:220]=1
rows=[]; lows=[]; highs=[]
def row(d,lo=-np.inf,hi=np.inf): rows.append(d); lows.append(lo); highs.append(hi)
y=220
for k,((i,j),ps) in enumerate(paths.items()):
 m=99+k; ys=[]
 # Candidate constant zero plus all path valuations.
 for p in [()]+ps:
  z=y; y+=1; ys.append(z)
  d={e:1 for e in p}; d[m]=-1
  row(d,0,np.inf)
  d=dict(d); d[z]=6*W
  row(d,-np.inf,6*W)
 row({z:1 for z in ys},2,np.inf)
row({m:1 for m in range(99,220)},-np.inf,-1)
# Fix gauge by using first incoming edge of each first internal vertex,
# and first outgoing edge of each second internal vertex.
for v in range(n):
 a=next(a for a,(r,s) in enumerate(L[0]) if r==v)
 cidx=66+next(c for c,(r,s) in enumerate(L[2]) if s==v)
 lb[a]=ub[a]=lb[cidx]=ub[cidx]=0
A=lil_matrix((len(rows),N),dtype=float)
for r,d in enumerate(rows):
 for k,v in d.items():A[r,k]=v
start=time.monotonic()
r=milp(c,integrality=np.ones(N),bounds=Bounds(lb,ub),constraints=LinearConstraint(A.tocsr(),lows,highs),options={'time_limit':LIMIT,'mip_rel_gap':0.01})
out={'bounds':W,'time_limit':LIMIT,'runtime_seconds':time.monotonic()-start,'status':int(r.status),'message':r.message,'objective':None if r.fun is None else float(r.fun)}
if r.x is not None:
 w=[int(round(x)) for x in r.x[:99]]
 violations=[]; entries=[]
 for (i,j),ps in paths.items():
  vals=[sum(w[e] for e in p) for p in ps]; m=min([0]+vals); count=([0]+vals).count(m)
  if count<2:violations.append([i,j,vals])
  entries.append({'output':i,'input':j,'path_values':vals,'minimum':m,'minimum_count_including_target':count})
 out.update({'weights':w,'entries':entries,'violations':violations,'negative_entries':sum(e['minimum']<0 for e in entries)})
p=(ROOT/f'tropical_search_W{W}.json');p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['weights','entries']},indent=2),flush=True)
