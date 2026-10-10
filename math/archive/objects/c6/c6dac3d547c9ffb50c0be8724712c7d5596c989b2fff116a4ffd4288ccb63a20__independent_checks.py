#!/usr/bin/env python3
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent;p=65537

def mm(A,B):return [[sum(x*y for x,y in zip(r,c))%p for c in zip(*B)] for r in A]
def inverse(A):
 n=len(A);a=[r[:]+[int(i==j) for j in range(n)] for i,r in enumerate(A)]
 for j in range(n):
  k=next(i for i in range(j,n) if a[i][j]);a[k],a[j]=a[j],a[k];v=pow(a[j][j],-1,p);a[j]=[v*t%p for t in a[j]]
  for i in range(n):
   if i!=j and a[i][j]:
    v=a[i][j];a[i]=[(x-v*y)%p for x,y in zip(a[i],a[j])]
 return [r[n:] for r in a]
controls=[]
for n in [4,8,16]:
 q=pow(3,(p-1)//n,p);W=[[pow(q,-i,p) if i==j else 0 for j in range(n)] for i in range(n)];Z=[[int(i==(j+1)%n) for j in range(n)] for i in range(n)]
 for d in range(1,n+1):
  if n%d:continue
  k=n//d;H=[[0]*n for _ in range(n)]
  for b in range(k):
   for r in range(d):
    for a in range(d):H[r*k+b][a*k+b]=pow(q,-k*r*a,p)
  Hi=inverse(H);X=mm(H,mm(Z,Hi));Y=mm(H,mm(W,Hi))
  assert all(sum(v!=0 for v in row)==1 for A in [X,Y] for row in A)
  assert all(sum(A[i][j]!=0 for i in range(n))==1 for A in [X,Y] for j in range(n))
  assert mm(X,Y)==[[q*v%p for v in r] for r in mm(Y,X)]
  assert all(sum(v!=0 for v in row)==d for row in H)
  controls.append({'N':n,'row_support':d,'both_images_monomial':True,'Weyl_sign_checked':True})
geometry=[]
for M in range(2,129):
 n=M*M;counts=[0]*(n+1);areas=[(i//M+1)*(i%M+1) for i in range(n)]
 for a in areas:counts[a]+=1
 pos=[];v=0
 for c in counts:pos.append(v);v+=c
 order=[0]*n
 for i,a in enumerate(areas):order[pos[a]]=i;pos[a]+=1
 sigma=[0]*n
 for r,i in enumerate(order):sigma[i]=order[n-1-r]
 assert sigma[0]==n-1 and sigma[1]==n-2
 # Native row1 cannot receive column M. Routed term has base row N-2
 # and base column rho(M)=N-1-M, whose u-coordinate is M-1.
 assert not (1//M>=M//M and 1%M>=M%M)
 a=sigma[1];b=n-1-M;assert not (a//M>=b//M and a%M>=b%M)
 assert n-M+1<n and n-1>n/2
 geometry.append({'M':M,'N':n,'sigma0':sigma[0],'sigma1':sigma[1],
                  'row0_support_at_least_if_beta_nonzero':n-1,'row1_structural_upper_bound':n-M+1,
                  'row1_missing_column':M})
result={'monomial_intertwiner_controls':controls,'balanced_geometry_controls':geometry,
        'scope':'Exact support/representation gate, not a product-of-sums exclusion; no source inputs or uploaded code.'}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'monomial_controls':len(controls),'geometry_sizes':len(geometry)},indent=2))
