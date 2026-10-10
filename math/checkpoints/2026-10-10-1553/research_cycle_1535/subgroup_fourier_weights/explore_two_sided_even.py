# Fresh bounded, exact integer-coefficient search; zero tests never use tolerances.
import numpy as np, json
from pathlib import Path
n=6; w=np.array([1,2,2,2,2,2]); Ec=np.zeros((5,n,n),dtype=np.int64)
for i in range(n):
 for j in range(n):
  if not i*j: Ec[0,i,j]=2
  else:
   k=i*j%11;k=min(k,11-k)
   if k==5:Ec[0,i,j]=-1;Ec[1:,i,j]=-2
   else:Ec[k,i,j]=2
Ps={}
for a2 in [0,2,-2,4,-4,1,-1]:
 for mask in range(32):
  P=2*np.eye(n,dtype=np.int64)
  for j in range(1,6):
   if mask>>(j-1)&1:P[j,0]=a2
  for anchor in range(6):
   for mask2 in range(32) if anchor else [0]:
    R=P.copy()
    for j in range(1,6):
     if j!=anchor and mask2>>(j-1)&1:R[j,:]=P[j,:]-P[anchor,:]
    Ps[tuple(R.flatten())]=R
P=np.array(list(Ps.values()));cost=((P!=0)*w).sum(axis=(1,2))
# Inverses proposed in floating point, then VERIFIED EXACTLY before any use.
inv=np.rint(4*np.linalg.inv(P)).astype(np.int64)
assert np.all(np.matmul(P,inv)==4*np.eye(n,dtype=np.int64))
max_inverse_integer=int(np.abs(inv).max())
arithmetic_absolute_bound=72*max_inverse_integer**2
assert arithmetic_absolute_bound < 2**63
T=np.einsum('aij,rjk->raik',Ec,inv)
single=cost+11+np.any(T!=0,axis=1).sum(axis=(1,2))
print('candidates',len(P),'best single',single.min(),'distribution',dict(zip(*np.unique(single,return_counts=True))),flush=True)
idx=np.nonzero(single<=61)[0]
print('selected candidates',len(idx),flush=True)
# Optimize pairings whose single-side cost is at most 61; this is a bounded local family only.
T0=T[idx];cost0=cost[idx]; best=58; arg=None
for count,k in enumerate(idx):
 B=np.einsum('ij,rajk->raik',inv[k].T,T0,optimize=True)
 scores=cost[k]+cost0+np.any(B!=0,axis=1).sum(axis=(1,2))
 j=int(np.argmin(scores));score=int(scores[j])
 if score<best:
  best=score;arg=(int(k),int(idx[j]));print('BEST',best,'Pleft',P[k].tolist(),'Pright',P[idx[j]].tolist(),flush=True)
 if count%1000==0: print('progress',count,'/',len(idx),flush=True)
res=dict(raw_candidate_count=len(P),selected_candidate_count=len(idx),single_side_cutoff=61,best_even_sector_edges=best,odd_sector_edges=45,total_edges=best+45,
         scope='Only the explicitly enumerated rational star-and-difference outer bases; not a global minimum or general obstruction.',
         exact_inverse_and_coefficient_zero_tests=True,
         max_scaled_inverse_integer=max_inverse_integer,arithmetic_absolute_bound=arithmetic_absolute_bound,
         int64_overflow_excluded=True)
if arg:res['scaled_Pleft']=P[arg[0]].tolist();res['scaled_Pright']=P[arg[1]].tolist()
Path(__file__).with_name('F11_BOUNDED_RATIONAL_SEARCH.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res),flush=True)
