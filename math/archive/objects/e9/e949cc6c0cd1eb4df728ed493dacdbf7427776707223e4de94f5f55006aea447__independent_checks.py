#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import json,hashlib
HERE=Path(__file__).resolve().parent
SRC=HERE/'source_evidence/HALF_GRID_CUTS.json'
def layout(m):
 n=m*m;counts=[0]*(n+1);areas=[(i//m+1)*(i%m+1) for i in range(n)]
 for a in areas:counts[a]+=1
 pos=[];v=0
 for c in counts:pos.append(v);v+=c
 order=[0]*n
 for i,a in enumerate(areas):order[pos[a]]=i;pos[a]+=1
 sigma=[0]*n
 for k,i in enumerate(order):sigma[i]=order[n-1-k]
 return order,sigma

def propagate(m,sources,cut):
 n=m*m;order,sigma=layout(m);cut=set(cut);assert all(0<=v<7*n for v in cut)
 x=[i in sources and i not in cut for i in range(n)]
 for native,balanced,out in [(1,2,3),(4,5,6)]:
  a=[False]*n;b=[False]*n
  for i in range(n):
   a[i]=(native*n+i not in cut) and (x[i] or (i>=m and a[i-m]) or (i%m>0 and a[i-1]))
   b[i]=(balanced*n+i not in cut) and (x[n-1-i] or (i>=m and b[i-m]) or (i%m>0 and b[i-1]))
  x=[out*n+i not in cut and (a[i] or b[sigma[i]]) for i in range(n)]
 return x
records=[]
for d in json.loads(SRC.read_text()):
 m=d['M']
 if m not in [8,16,32]:continue
 n=m*m;cut=d['cut_state_vertices'];assert len(cut)==len(set(cut))==d['cut_capacity']
 out=propagate(m,set(range(n//2,n)),cut);assert not any(out[:n//2]) and len(cut)<n//2
 records.append({'M':m,'N':n,'cut_vertices':len(cut),'Fourier_rank':n//2,'method':'topological Boolean propagation'})
for m in [64,128]:
 n=m*m;order,sigma=layout(m);A=set(order[:n//2]);B=set(order[n//2:]);rhoB={n-1-j for j in B}
 assert {sigma[i] for i in A}==B
 overlap=B&rhoB
 frontier={i for i in B if (i>=m and i-m in A) or (i%m>0 and i-1 in A)}
 assert len(frontier)<=2*m
 S=overlap|frontier;cut={wire*n+i for wire in [2,5] for i in S};out=propagate(m,B,cut)
 assert not any(out[i] for i in A) and len(cut)<n//4
 records.append({'M':m,'N':n,'h':len(overlap),'frontier':len(frontier),'single_stage_union':len(S),
                 'cut_vertices':len(cut),'Fourier_rank_lower_bound':n//4,'method':'topological Boolean propagation'})
exp_lower=sum(F(7,4)**k/F(factorial(k)) for k in range(6))
assert exp_lower==F(700667,122880) and exp_lower>F(50,9)
assert F(9,50)*(1+F(7,4))==F(99,200)
# Lens upper series coefficient, after factoring sqrt(7).
coefficient=F(2,3)*F(7,125)+F(2,15)*F(49,3125)/(1-F(7,25))
assert coefficient==F(679,16875)
assert 7<F(8,3)**2 and coefficient*F(8,3)<F(27,250)
assert 99*257**2<100*256**2
assert 17*256**2-4216*256-1108==33708>0 and 34*256-4216>0
# Tail expression was independently expanded as exact polynomial coefficients.
assert F(1,4)-F(27,125)==F(17,500)
assert -2*F(27,125)-8==-F(4216,500)
assert -F(27,125)-2==-F(1108,500)
result={'source':str(SRC.relative_to(HERE)),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),
        'finite_cases':records,'rational_tail_constants':{'exponential_lower_sum':str(exp_lower),'lens_coefficient_of_sqrt7':str(coefficient),
        'lens_rational_upper':'27/250','threshold_M':256,'gap_at_threshold':'33708/500','tail_gap_increasing':True},
        'conclusion':'Identity-permutation middle is excluded for every dyadic M>=8, for all component masks/diagonals. No arbitrary-middle or other-route exclusion.',
        'source_programs_executed':False}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
