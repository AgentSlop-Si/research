import numpy as np,json,time
results=[]
for m in range(2,10):
 n=1<<m; p=np.array([int(f'{j:0{m}b}'[::-1],2) for j in range(n)])
 best=(-10,None)
 for t in range(1,n):
  c=np.r_[0,np.cumsum(p<t)]
  for w in range(1,n):
   z=c[w:]-c[:-w]
   costs=np.full(n-w+1,2);costs[0]=costs[-1]=1
   lo=int(np.argmin(z+costs));hi=int(np.argmax(z-costs))
   # rank deficit to boundary-aware rank cap = maxdiff - (bI+bJ+1)
   deficit=int(z[hi]-z[lo]-costs[hi]-costs[lo]-1)
   if deficit>best[0]: best=(deficit,dict(n=n,t=t,w=w,I=[hi,hi+w],J=[lo,lo+w],delta=int(z[hi]-z[lo]),budgets=[int(costs[hi]),int(costs[lo])]))
 results.append(best);print(m,best,flush=True)
json.dump(results,open('research_round_2156/review_three_stage/LAYOUT_PROBE.json','w'),indent=2)
