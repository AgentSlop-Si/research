"""Independent exhaustive endpoint-order certificate for one r=2 stage.
No uploaded code is imported or executed. A mod-p nonzero minor witnesses
nonzero complex cyclotomic minor, so modular impossibility lifts to C.
"""
from itertools import combinations
from pathlib import Path
import json
p=998244353;n=8;w=pow(3,(p-1)//n,p)
assert pow(w,8,p)==1 and pow(w,4,p)==p-1
f=[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
def rank(a):
 a=[r[:] for r in a];k=0
 for j in range(len(a[0]) if a else 0):
  pos=next((i for i in range(k,len(a)) if a[i][j]),None)
  if pos is None:continue
  a[k],a[pos]=a[pos],a[k]
  u=pow(a[k][j],-1,p);a[k]=[v*u%p for v in a[k]]
  for i in range(k+1,len(a)):
   u=a[i][j];a[i]=[(v-u*x)%p for v,x in zip(a[i],a[k])]
  k+=1
  if k==len(a):break
 return k
allmask=(1<<n)-1
reach={(0,0)};report=[]
for s in range(1,n+1):
 candidates=set()
 for a,b in reach:
  for i in range(n):
   if a>>i&1:continue
   for j in range(n):
    if b>>j&1:continue
    candidates.add((a|1<<i,b|1<<j))
 nxt=set()
 for a,b in candidates:
  rows=[i for i in range(n) if a>>i&1];nr=[i for i in range(n) if not(a>>i&1)]
  cols=[i for i in range(n) if b>>i&1];nc=[i for i in range(n) if not(b>>i&1)]
  if rank([[f[i][j] for j in nc] for i in rows])<=2 and rank([[f[i][j] for j in cols] for i in nr])<=2:
   nxt.add((a,b))
 report.append({'cut':s,'candidate_prefix_pairs':len(candidates),'reachable_prefix_pairs':len(nxt)})
 reach=nxt
assert (allmask,allmask) not in reach
out={'n':n,'channel_rank':2,'prime':p,'root':w,'arbitrary_independent_endpoint_orders_impossible':True,'frontiers':report}
print(json.dumps(out,indent=2))
(Path(__file__).resolve().parent/'f8_endpoint_order_results.json').write_text(json.dumps(out,indent=2)+'\n')
