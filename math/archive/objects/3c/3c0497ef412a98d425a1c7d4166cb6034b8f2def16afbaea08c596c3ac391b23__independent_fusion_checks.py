"""Independent checks for the audit-derived rational mixer and scalar branches."""
from fractions import Fraction as Q
from math import factorial,comb
import random,json,pathlib
B=pathlib.Path(__file__).resolve().parent

def rank(a):
 a=[[Q(x) for x in r] for r in a];n=len(a);k=0
 for j in range(len(a[0])):
  i=next((i for i in range(k,n) if a[i][j]),None)
  if i is None:continue
  a[k],a[i]=a[i],a[k];c=a[k][j];a[k]=[x/c for x in a[k]]
  for i in range(k+1,n):
   c=a[i][j];a[i]=[x-c*y for x,y in zip(a[i],a[k])]
  k+=1
  if k==n:break
 return k

def green(s,a):
 n=len(s);G=[[Q(0)]*n for _ in range(n)]
 for j in range(n):
  i=j
  for d in range(n):G[i][j]=a**d/(1-a**n);i=s[i]
 return G

def mv(H,x,p):return [sum(a*b for a,b in zip(row,x))%p for row in H]
def hom(n,a,b,d,p):return [[(a if i>j else b if i<j else d)%p for j in range(n)] for i in range(n)]
def inter(n,a,b,d,p):
 f=b%p!=0;s=b if f else a;o=a if f else b;K=[[0]*n for _ in range(n)]
 for i in range(n):K[i][(i+1)%n if f else (i-1)%n]=s if (i<n-1 if f else i>0) else o
 BB=[[(K[i][j]-s*int(i==j))%p for j in range(n)] for i in range(n)]
 AA=[[((d-s)*K[i][j]+s*(o-d)*int(i==j))%p for j in range(n)] for i in range(n)]
 return AA,BB,f

out={'rational_mixer':[]};rng=random.Random(270)
from itertools import combinations
for n in [4,6,8,10]:
 order=list(range(n));rng.shuffle(order);w=[0]*n
 for i in range(n):w[order[i]]=order[(i+1)%n]
 z=[(j+1)%n for j in range(n)];G=green(z,Q(1,4));H=green(w,Q(1,5));m=n//2;lam=factorial(m)*(2*20**n)**m+2
 S=[[a+lam*b for a,b in zip(r,s)] for r,s in zip(G,H)];mini=n
 for I in combinations(range(n),m):
  J=[j for j in range(n) if j not in I];rr=rank([[S[i][j] for j in J] for i in I]);mini=min(mini,rr)
  assert rr>=max(sum(z[j] in I for j in J),sum(w[j] in I for j in J))
 out['rational_mixer'].append({'n':n,'lambda_bits':lam.bit_length(),'all_balanced_cuts':comb(n,m),'minimum_exact_rational_rank':mini})

cnt=0
for p,g in [(12289,11),(65537,3)]:
 for n in [16,32,64]:
  omega=pow(g,(p-1)//n,p)
  for t in range(40):
   a,b,d=[rng.randrange(1,p) for _ in range(3)]
   if t%3==0:a=0
   if t%3==1:b=0
   A,Bb,f=inter(n,a,b,d,p);H=hom(n,*[rng.randrange(p) for _ in range(3)],p)
   # Scalar first: choose the column that becomes frequency one after right permutation.
   lhs=mv(Bb,[pow(omega,i,p) for i in range(n)],p);j=rng.randrange(n);v=[r[j] for r in H];rng.shuffle(v);rhs=mv(A,v,p)
   idx=range(n-1) if f else range(1,n)
   assert len({lhs[i] for i in idx})==n-1 and len({rhs[i] for i in idx})<=9
   # Scalar last: row permutation leaves number of distinct values unchanged.
   j=1 if f else 0;x=[r[j] for r in Bb]
   lhs=[sum(x[k]*pow(omega,i*k,p) for k in range(n))%p for i in range(n)]
   v=[r[j] for r in A];rng.shuffle(v);rhs=mv(H,v,p)
   assert len(set(lhs))==n and len(set(rhs))<=5
   cnt+=2
out['scalar_endpoint_witness_checks']=cnt
(B/'FUSION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
