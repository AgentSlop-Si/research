"""Independent fresh modular controls for multiscale claims. No source imports/data."""
from itertools import combinations_with_replacement
from math import isqrt
from pathlib import Path
import json
O=Path(__file__).resolve().parent
def prime(p):return p>=2 and all(p%d for d in range(2,isqrt(p)+1))
def field(n):
 p=n+1
 while not prime(p):p+=n
 for g in range(2,p):
  w=pow(g,(p-1)//n,p)
  if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n) if n%d==0):return p,w
 raise ValueError(n)
def rank(a,p):
 a=[r[:] for r in a];k=0
 for j in range(len(a[0])):
  s=next((i for i in range(k,len(a)) if a[i][j]%p),None)
  if s is None:continue
  a[k],a[s]=a[s],a[k];iv=pow(a[k][j],-1,p)
  for i in range(k+1,len(a)):
   f=a[i][j]*iv%p
   for h in range(j,len(a[0])):a[i][h]=(a[i][h]-f*a[k][h])%p
  k+=1
  if k==len(a):break
 return k
def cyclic(a,b,p):
 n=len(a);out=[0]*n
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[(i+j)%n]=(out[(i+j)%n]+x*y)%p
 return out
support=[]
for n in range(2,26):
 p,w=field(n)
 if p==2:raise AssertionError
 gauss=[sum(pow(w,(j*j+d*j)%n,p) for j in range(n))%p for d in range(n)]
 count=sum(v!=0 for v in gauss)*n;expected=n*n if n%2 else n*n//2
 assert count==expected
 support.append({'N':n,'field':p,'root':w,'support':count})
chirp=[];inverses=0;reshapes=0;fusion=0
for n in [4,8,16,32]:
 p,z=field(2*n);m=n.bit_length()-1;iv=pow(n,-1,p)
 q=[pow(z,(-t*t)%(2*n),p)*iv%p for t in range(n)]
 c=[pow(z,t*t,p) for t in range(n)]
 assert cyclic(c,q,p)==[1]+[0]*(n-1);inverses+=1
 for a in range(1,m):
  mat=[[q[u+(1<<a)*v] for v in range(n>>a)] for u in range(1<<a)]
  assert rank(mat,p)==1<<min(a,m-a);reshapes+=1
 for alpha in range(min(p,9)):
  if pow(alpha,n,p)==1:continue
  poly=[1]+[0]*(n-1)
  for j in range(m):
   factor=[0]*n;factor[0]=1;factor[1<<j]=pow(alpha,1<<j,p)
   poly=cyclic(poly,factor,p)
  assert poly==[pow(alpha,k,p) for k in range(n)];fusion+=1
 chirp.append({'N':n,'field':p,'primitive2Nroot':z})
subset_total=0;unique=0;parallelograms=0
for n in [4,8,16]:
 m=n.bit_length()-1;p,z=field(2*n)
 for strides in combinations_with_replacement(range(1,n),m):
  subset_total+=1;sums=[0]
  for s in strides:sums +=[(x+s)%n for x in sums]
  if len(set(sums))!=n:continue
  unique+=1
  val=[(x&-x).bit_length()-1 for x in strides]
  assert sorted(val)==list(range(m))
  a=strides[val.index(0)];b=strides[val.index(1)]
  q=lambda t:pow(z,-(t%n)**2%(2*n),p)
  for offset in range(n):
   ratio=q(offset)*q(offset+a+b)*pow(q(offset+a)*q(offset+b)%p,-1,p)%p
   assert ratio==pow(z,(-2*a*b)%(2*n),p) and ratio!=1;parallelograms+=1
assert subset_total==3150
out={'status':'PASS','gauss_support_fields':support,'chirp_fields':chirp,'direct_inverse_convolutions':inverses,'binary_cut_ranks':reshapes,'binomial_fusion_controls':fusion,'stride_multisets':subset_total,'unique_subset_sum_multisets':unique,'translated_parallelogram_controls':parallelograms,'scope':'Only independently written standard-library code; no supplied program or source result data read.'}
(O/'multiscale_check_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
