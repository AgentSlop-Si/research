"""Independent capped-count DP for all one-family circuit minors.
Reads topology JSON as data; executes no supplied source program.
"""
from pathlib import Path
from itertools import combinations
import json,collections,time
import numpy as np
import sympy as sp
P=Path(__file__).resolve().parent
T=json.loads(Path('research_cycle_1635/v34_independent_audit/source/extracted/fft_cyclotomic_zero_forcing_v34/topology_11.json').read_text());layers=T['layers'];n=T['n']
adj=[]
for layer in layers:
 d={j:[] for j in range(n)}
 for k,(i,j) in enumerate(layer):d[j].append((i,k))
 adj.append(d)
certs=[];stats=[];start=time.monotonic()
for k in range(1,n+1):
 subsets=list(combinations(range(n),k));masks=[sum(1<<i for i in sub) for sub in subsets];index={m:i for i,m in enumerate(masks)};d=len(subsets)
 matrices=[];matchings=[]
 for ell in range(3):
  mat=np.zeros((d,d),dtype=np.int64); mm={}
  for j,inputs in enumerate(subsets):
   # Track count and unique edge-mask for each output vertex mask.
   states={0:(1,0)}
   for u in inputs:
    nex={}
    for mask,(count,em) in states.items():
     for v,e in adj[ell][u]:
      bit=1<<v
      if mask&bit:continue
      new=mask|bit;old=nex.get(new,(0,0));nc=min(2,old[0]+count)
      nex[new]=(nc,(em|(1<<e)) if nc==1 else 0)
    states=nex
   for mask,(cnt,em) in states.items():
    i=index[mask];mat[i,j]=cnt
    if cnt==1:mm[i,j]=em
  matrices.append(mat);matchings.append(mm)
 A,B,C=matrices
 BA=np.minimum(B@A,2);H=np.minimum(C@BA,2)
 spots=np.argwhere(H==1)
 for i,j in spots:
  i=int(i);j=int(j)
  ks=np.flatnonzero((C[i,:]>0)&(BA[:,j]>0));assert len(ks)==1;l=int(ks[0])
  hs=np.flatnonzero((B[l,:]>0)&(A[:,j]>0));assert len(hs)==1;h=int(hs[0])
  assert C[i,l]==B[l,h]==A[h,j]==1
  edges=[]
  for ell,key in [(0,(h,j)),(1,(l,h)),(2,(i,l))]:
   em=matchings[ell][key];assert em.bit_count()==k
   edges.extend(33*ell+e for e in range(33) if (em>>e)&1)
  certs.append({'order':k,'rows':subsets[i],'cols':subsets[j],'internal_first':subsets[h],'internal_second':subsets[l],'edges':edges,'required_valuation':k*(k-1)//2})
 stats.append({'order':k,'minors':d*d,'one_family_minors':len(spots),'unreachable_minors':int(np.sum(H==0))})
 print(json.dumps(stats[-1]),flush=True)
rows=[];rhs=[]
for c in certs:
 r=[0]*99
 for e in c['edges']:r[e]+=1
 rows.append(r);rhs.append(c['required_valuation'])
M=sp.Matrix(rows);aug=M.row_join(sp.Matrix(rhs));rank=M.rank();aug_rank=aug.rank()
relations=[]
if aug_rank>rank:
 for v in M.T.nullspace():
  res=sum(a*b for a,b in zip(v,rhs))
  if res:
   den=sp.ilcm(*[x.q for x in v]);ivec=[int(x*den) for x in v]
   relations.append({'coefficients':ivec,'rhs_sum':str(res*den)})
   break
out={'status':'PASS','runtime_seconds':time.monotonic()-start,'all_minor_count':sum(s['minors'] for s in stats),'statistics':stats,'one_family_minor_count':len(certs),'incidence_rank_Q':rank,'augmented_rank_Q':aug_rank,'inconsistent_relation':relations,'certificates':certs,'scope':'Only one-family minors yield these necessary exact linear valuation equations. Consistency is not Fourier feasibility.'}
(P/'ALL_MONOMIAL_MINORS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['certificates','statistics']},indent=2),flush=True)
