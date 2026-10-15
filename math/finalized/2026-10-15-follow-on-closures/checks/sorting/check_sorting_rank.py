"""Fresh independent small controls for M-SORTING-RANK; no supplier code."""
from itertools import product
from collections import Counter
from math import comb,ceil,log2,exp
from fractions import Fraction
from pathlib import Path
import json

def cycles(p):
 seen=set();c=0
 for j in range(len(p)):
  if j not in seen:
   c+=1
   while j not in seen:seen.add(j);j=p[j]
 return c

def rank(A,p):
 A=[[x%p for x in r] for r in A];k=0
 for j in range(len(A[0])):
  t=next((i for i in range(k,len(A)) if A[i][j]),None)
  if t is None:continue
  A[k],A[t]=A[t],A[k];iv=pow(A[k][j],-1,p);A[k]=[x*iv%p for x in A[k]]
  for i in range(len(A)):
   if i!=k:
    f=A[i][j];A[i]=[(x-f*y)%p for x,y in zip(A[i],A[k])]
  k+=1
 return k
out={};wordcount=strides=matrices=0
for n in range(2,13):
 hist=Counter();zero=0
 for bits in product((0,1),repeat=n):
  order=[j for bit in (0,1) for j,b in enumerate(bits) if b==bit]
  W=[0]*n
  for i,j in enumerate(order):W[j]=order[(i+1)%n]
  T=sum(x!=y for x,y in zip(bits,bits[1:]));r=n-cycles([(x-1)%n for x in W]);s=sum(x!=(j+1)%n for j,x in enumerate(W))
  assert r==2*(T//2);assert s==(0 if T<=1 else r+1)
  hist[r]+=1;zero+=s==0;wordcount+=1
  if n<=8:
   for a in range(1,n):
    z=n-cycles([(x-a)%n for x in W]);m=sum(x==(j+a)%n for j,x in enumerate(W));qa=sum(bits[j]==bits[j+a] and all(bits[j+t]!=bits[j] for t in range(1,a)) for j in range(n-a))
    assert 2*z>=n-m and m<=qa+2;strides+=1
    if n<=5:
     for p in (2,3,5):
      A=[[int(i==W[j])-int(i==(j+a)%n) for j in range(n)] for i in range(n)]
      assert rank(A,p)==z;matrices+=1
 assert sum(hist.values())==2**n and zero==2*n
 assert hist=={2*k:2*comb(n,2*k+1) for k in range((n+1)//2)}
 mean=Fraction(sum(k*v for k,v in hist.items()),2**n);var=Fraction(sum(k*k*v for k,v in hist.items()),2**n)-mean*mean
 if n>=3:assert mean==Fraction(n,2)-1 and var==Fraction(n,4)
 out[n]={'words':2**n,'histogram':dict(hist),'zero_edge_words':zero,'mean':str(mean),'variance':str(var)}
def bound(n):
 A=min(n-1,ceil(3*log2(n)));return max(0,1-exp(-n/32)-A*(A+1)*exp(-n/(16*(A+1)))-n*2**(-A))
result={'status':'PASS','words':wordcount,'all_stride_cases':strides,'direct_matrix_ranks':matrices,'exact_distributions':out,'analytic_bound_examples':{str(n):bound(n) for n in [4096,8192]},'qualification':'These bounded controls supplement the independent analytic proof; no all-N theorem is inferred from enumeration; high rank is not high execution cost.'}
Path(__file__).with_name('SORTING_FRESH_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='exact_distributions'}))
