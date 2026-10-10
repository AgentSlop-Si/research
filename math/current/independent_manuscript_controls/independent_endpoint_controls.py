"""Independent fresh endpoint controls. No manuscript/source program imports."""
from pathlib import Path
from itertools import product, combinations
from fractions import Fraction
import json, random
import numpy as np
ROOT=Path(__file__).resolve().parent
random.seed(27419)
def rankmod(A,p):
 A=[list(map(lambda x:int(x)%p,row)) for row in A]
 if not A:return 0
 k=0
 for j in range(len(A[0])):
  a=next((a for a in range(k,len(A)) if A[a][j]),None)
  if a is None:continue
  A[k],A[a]=A[a],A[k];v=pow(A[k][j],-1,p);A[k]=[(x*v)%p for x in A[k]]
  for a in range(k+1,len(A)):
   v=A[a][j]
   if v:A[a]=[(x-v*y)%p for x,y in zip(A[a],A[k])]
  k+=1
  if k==len(A):break
 return k
def bitrev(i,n):return int(format(i,f'0{n}b')[::-1],2) if n else 0
cut_rows=[]
for prime,gen in [(998244353,3),(2013265921,31)]:
 counts={1:[0,0],2:[0,1,0]}
 for n in [4,8,16,32,64]:
  m=n.bit_length()-1;z=pow(gen,(prime-1)//n,prime);assert pow(z,n//2,prime)==prime-1
  order=[bitrev(i,m) for i in range(n)]
  Q=[[pow(z,a*b,prime) for b in order] for a in order]
  rr=[rankmod([row[k:] for row in Q[:k]],prime) for k in range(n+1)]
  for k in range(n//2+1):assert rr[k]==(k+1)//2+counts[n//4][k//2]
  assert rr==rr[::-1]
  assert max(rr)==(1 if n==4 else n//4+1)
  counts[n]=rr;cut_rows.append({'N':n,'prime':prime,'ranks':rr,'recurrence_reflection_and_max':True})
# Exhaust all critical rectangles in all abelian groups of order eight.
critical=[]
for factors in [(8,),(4,2),(2,2,2)]:
 pts=list(product(*(range(d) for d in factors)));n=len(pts);p=97
 roots=[pow(5,(p-1)//d,p) for d in factors]
 F=[[int(np.prod([pow(rt,a*b,p) for rt,a,b in zip(roots,x,y)]))%p for y in pts] for x in pts]
 minimum=9;count=0
 for R in combinations(range(n),3):
  for H in combinations(range(n),5):
   rk=rankmod([[F[i][j] for j in H] for i in R],p);assert rk>=3
   minimum=min(minimum,rk);count+=1
 critical.append({'factors':factors,'rectangles':count,'minimum_modular_rank':minimum,'prime':p})
# General deficit moment and every permitted singular-value lower bound.
moment=[]
for factors in [(4,),(7,),(8,),(4,2),(2,2,2),(9,),(3,3),(16,),(4,4),(27,)]:
 pts=list(product(*(range(d) for d in factors)));n=len(pts);lookup={x:i for i,x in enumerate(pts)}
 U=np.array([[np.exp(2j*np.pi*sum(a*b/d for a,b,d in zip(x,y,factors))) for y in pts] for x in pts])/np.sqrt(n)
 worst=0.0;tests=0;gaps=0
 for case in range(180):
  r=random.randrange(1,n+1);h=random.randrange(1,n+1)
  R=sorted(random.sample(range(n),r));H=sorted(random.sample(range(n),h));Hs={pts[j] for j in H}
  cmax=max(sum(tuple((x[k]+s[k])%factors[k] for k in range(len(factors))) in Hs for x in Hs) for s in pts[1:])
  deficit=h-cmax;B=Fraction(h*(n-r),n)-Fraction(deficit*r*(n-r),n*n);K=Fraction(h)-B
  I=[i for i in range(n) if i not in R];A=U[np.ix_(I,H)].conj().T@U[np.ix_(I,H)]
  actual=float(np.trace(A@A).real);worst=max(worst,actual-float(B));assert actual<=float(B)+1e-10
  sv=np.linalg.svd(U[np.ix_(R,H)],compute_uv=False)
  assert sum(sv>1e-9)>=-(-K.numerator//K.denominator)
  for t in range(min(r,h)):
   if t<K:
    bound=np.sqrt(max(0,1-np.sqrt(float(B/Fraction(h-t)))))
    assert sv[t]+1e-9>=bound;gaps+=1
  tests+=1
 moment.append({'factors':factors,'rectangles':tests,'gap_checks':gaps,'largest_moment_excess_from_roundoff':worst})
out={'cut_recurrences':cut_rows,'exhaustive_critical_rectangles':critical,'randomized_complex_moments_and_gaps':moment,'interpretation':'Exact modular cut and finite critical checks; floating-point analytic controls are regression evidence, not proofs.'}
(ROOT/'independent_endpoint_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:len(v) for k,v in out.items() if isinstance(v,list)}))
