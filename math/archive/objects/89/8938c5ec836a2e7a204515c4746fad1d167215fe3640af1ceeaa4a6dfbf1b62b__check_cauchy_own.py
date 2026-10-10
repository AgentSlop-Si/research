"""Fresh modular controls, independent of uploaded implementation."""
import json,itertools,random
from pathlib import Path

def rank(a,p):
 a=[row[:] for row in a];r=0
 for c in range(len(a[0]) if a else 0):
  t=next((i for i in range(r,len(a)) if a[i][c]%p),None)
  if t is None:continue
  a[r],a[t]=a[t],a[r];q=pow(a[r][c],-1,p);a[r]=[v*q%p for v in a[r]]
  for i in range(r+1,len(a)):
   q=a[i][c];a[i]=[(x-q*y)%p for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r
rng=random.Random(2210);entries=minors=budgets=0
for p in [257,65537]:
 for n in [2,4,8,16,32,64]:
  z=pow(3,(p-1)//n,p)
  if pow(z,n//2,p)==1:
   z=next(pow(g,(p-1)//n,p) for g in range(2,p) if pow(pow(g,(p-1)//n,p),n//2,p)!=1)
  assert pow(z,n,p)==1 and pow(z,n//2,p)!=1
  a=[[sum(k*pow(z,((i-j)*k)%n,p) for k in range(n))*pow(n,-1,p)%p for j in range(n)] for i in range(n)]
  for i in range(n):
   for j in range(n):
    target=(n-1)*pow(2,-1,p)%p if i==j else pow(z,j,p)*pow((pow(z,i,p)-pow(z,j,p))%p,-1,p)%p
    assert a[i][j]==target;entries+=1
  for t in range(1,min(6,n//2)+1):
   for _ in range(5):
    ids=rng.sample(range(n),2*t);assert rank([[a[i][j] for j in ids[t:]] for i in ids[:t]],p)==t;minors+=1
  for s in range(min(4,n)):
   diff=[r[:] for r in a]
   for i in range(n):
    for j in rng.sample(range(n),s):diff[i][j]=(diff[i][j]-rng.randrange(1,p))%p
   r=rank(diff,p);assert n<=(s+2)*(r+1)-1;budgets+=1
out={'fields':[257,65537],'entry_identities':entries,'disjoint_minors':minors,'sparse_rank_controls':budgets,'uploaded_code_executed':False}
Path(__file__).with_name('CAUCHY_OWN_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
