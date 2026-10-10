"""Fresh exact audit controls derived from displayed identities; no source imports."""
import json, math, random
from pathlib import Path
rng=random.Random(221310)
counts={"full_jet_entries":0,"interval_jet_entries":0,"reconstructed_bins":0,"confluent_hankel_cases":0,"dense_defect_cases":0}
def inverse(a,p): return pow(a%p,p-2,p)
def rank(a,p):
 a=[r[:] for r in a]; k=0
 for j in range(len(a[0])):
  pivot=next((i for i in range(k,len(a)) if a[i][j]%p),None)
  if pivot is None: continue
  a[k],a[pivot]=a[pivot],a[k]
  z=inverse(a[k][j],p); a[k]=[x*z%p for x in a[k]]
  for i in range(len(a)):
   if i!=k:
    z=a[i][j]; a[i]=[(x-z*y)%p for x,y in zip(a[i],a[k])]
  k+=1
  if k==len(a): break
 return k
for n,p in [(3,7),(5,11),(7,29),(9,19),(11,23),(13,53),(15,31),(17,103),(21,43),(25,101)]:
 eta=next(a for a in range(2,p) if pow(a,2*n,p)==1 and all(pow(a,k,p)!=1 for k in range(1,2*n)))
 q=pow(eta,8,p); h=[]; phi=1
 for t in range(n):
  if t: phi=phi*(1-pow(q,t,p))%p
  h.append(pow(eta,2*t*t,p)*inverse(phi,p)%p)
 for a,b in [(0,n),(0,1),(n-1,n),(1,n),(1,min(n,4))]:
  d=min(4,n-1)
  direct=[[sum(pow(t,j,p)*h[t]*pow(eta,k*t,p) for t in range(a,b))%p for k in range(2*n)] for j in range(d+1)]
  out=[[None]*(2*n) for _ in range(d+1)]
  for j in range(d+1):
   for parity in [0,1]:
    cycle=[(parity+4*i)%(2*n) for i in range(n)]
    out[j][cycle[0]]=direct[j][cycle[0]];out[j][cycle[1]]=direct[j][cycle[1]]
    for i in range(n-2):
     k=cycle[i]; nxt=cycle[i+1];last=cycle[i+2]
     coupling=sum(math.comb(j,l)*out[l][nxt] for l in range(j+1))
     left=(1-pow(q,a,p))*h[a]*pow(a,j,p)*pow(eta,k*a,p)
     right=pow(eta,4*b-2,p)*h[b-1]*pow(b,j,p)*pow(eta,k*b,p)
     out[j][last]=(out[j][k]-pow(eta,k+2,p)*coupling-left+right)%p
  assert out==direct,(n,a,b)
  counts['full_jet_entries' if (a,b)==(0,n) else 'interval_jet_entries']+=(d+1)*2*n
 for _ in range(12):
  R=rng.randrange(1,min(n//2,4)+1)
  orders=[];remaining=R
  while remaining:
   r=rng.randrange(1,remaining+1);orders.append(r);remaining-=r
  ms=rng.sample(range(2*n),len(orders))
  polys=[[rng.randrange(p) for _ in range(r-1)]+[rng.randrange(1,p)] for r in orders]
  vals=[sum(sum(c*pow(t,j,p) for j,c in enumerate(poly))*pow(eta,m*t,p) for m,poly in zip(ms,polys))%p for t in range(n)]
  H=[[vals[i+j] for j in range(R)] for i in range(R)]
  assert rank(H,p)==R
  counts['confluent_hankel_cases']+=1
  x=[h[t]*vals[t]%p for t in range(n)]
  jets=[[sum(pow(t,j,p)*h[t]*pow(eta,k*t,p) for t in range(n))%p for k in range(2*n)] for j in range(R)]
  for k in range(n):
   pred=sum(c*jets[j][(2*k+m)%(2*n)] for m,poly in zip(ms,polys) for j,c in enumerate(poly))%p
   actual=sum(x[t]*pow(eta,2*k*t,p) for t in range(n))%p
   assert pred==actual
   counts['reconstructed_bins']+=1
 x=[t*h[t]%p for t in range(n)]
 defects=[((1-pow(q,t,p))*x[t]-pow(eta,4*t-2,p)*x[t-1])%p for t in range(1,n)]
 assert all(defects);counts['dense_defect_cases']+=1
result={'status':'passed','counts':counts,'seed':221310,'scope':'Fresh displayed-identity, reconstruction, and Hankel controls only; no source executable or source benchmark ledger run.'}
Path(__file__).with_name('RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
