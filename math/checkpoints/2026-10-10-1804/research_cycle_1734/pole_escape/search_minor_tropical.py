"""Fresh bounded cutting-plane search for entry and 2x2-minor tropical witnesses."""
import json,pathlib,time,collections
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
R=pathlib.Path(__file__).resolve().parent
L=json.loads((R/'topology_11.json').read_text())['layers']
P=collections.defaultdict(list)
for a,(u,j) in enumerate(L[0]):
 for b,(v,uu) in enumerate(L[1]):
  if u!=uu:continue
  for c,(i,vv) in enumerate(L[2]):
   if v==vv:P[i,j].append([a,33+b,66+c])
E=[{'label':['entry',i,j],'target':0,'terms':P[i,j]} for i in range(11) for j in range(11)]
M=[{'label':['minor',*r['rows'],*r['cols']],'target':1,'terms':[f['edges'] for f in r['families']]} for r in json.loads((R/'minor_tropical_full_certificate.json').read_text())]
selected=set(i for i,m in enumerate(M) if len(m['terms'])<=2)
W=3;MAX_ROUNDS=5;TIME_PER_ROUND=90
for rnd in range(1,MAX_ROUNDS+1):
 polys=E+[M[i] for i in sorted(selected)]
 N=99+len(polys)+sum(1+len(p['terms']) for p in polys)
 lo=np.zeros(N);hi=np.ones(N);lo[:99]=-W;hi[:99]=W
 for k,p in enumerate(polys):lo[99+k]=-6*W;hi[99+k]=p['target']
 cost=np.zeros(N);cost[99:220]=1
 rows=[];rl=[];rh=[]
 def add(d,l=-np.inf,h=np.inf):rows.append(d);rl.append(l);rh.append(h)
 y=99+len(polys)
 for k,p in enumerate(polys):
  m=99+k;zs=[];big=12*W+1
  for es,constant in [([],p['target'])]+[(es,0) for es in p['terms']]:
   z=y;y+=1;zs.append(z)
   d={e:es.count(e) for e in es};d[m]=-1
   add(d,l=-constant)
   d=dict(d);d[z]=big;add(d,h=big-constant)
  add({z:1 for z in zs},l=2)
 add({m:1 for m in range(99,220)},h=-1)
 for v in range(11):
  a=next(a for a,(u,j) in enumerate(L[0]) if u==v)
  c=66+next(c for c,(i,u) in enumerate(L[2]) if u==v)
  lo[a]=hi[a]=lo[c]=hi[c]=0
 A=lil_matrix((len(rows),N))
 for k,row in enumerate(rows):
  for j,v in row.items():A[k,j]=v
 t=time.monotonic();res=milp(cost,integrality=np.ones(N),bounds=Bounds(lo,hi),constraints=LinearConstraint(A.tocsr(),rl,rh),options={'time_limit':TIME_PER_ROUND})
 out={'round':rnd,'bounds':W,'time_limit_seconds':TIME_PER_ROUND,'runtime':time.monotonic()-t,'included_minor_indices':sorted(selected),'solver_status':int(res.status),'solver_message':res.message,'objective':None if res.fun is None else float(res.fun)}
 if res.x is not None:
  w=[int(round(x)) for x in res.x[:99]];badE=[];badM=[]
  for family,bad in [(E,badE),(M,badM)]:
   for k,p in enumerate(family):
    vals=[p['target']]+[sum(w[e] for e in es) for es in p['terms']]
    if vals.count(min(vals))<2:bad.append(k)
  assert not badE
  assert not (set(badM)&selected)
  out.update({'weights':w,'failed_entry_indices':badE,'failed_minor_indices':badM,'negative_entries':sum(min(sum(w[e] for e in es) for es in p['terms'])<0 for p in E)})
  selected.update(badM)
 (R/f'minor_search_round{rnd}.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ['weights','included_minor_indices','failed_minor_indices']}),flush=True)
 if res.x is None or not out['failed_minor_indices']:break
