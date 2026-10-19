from itertools import combinations_with_replacement, product
from functools import lru_cache
import json
import numpy as np
from scipy.optimize import linprog
BASE='/workspace/shared/fiveprime_q7_boundary_20261019_1430/'
@lru_cache(None)
def types(n):
 if n==1:return [(k,k) for k in range(6)]
 out={(k,n+k-1) for k in range(1,6)}
 if n<=5:
  for ss in combinations_with_replacement(range(1,32),n):
   if any((a&b).bit_count()!=1 for a,b in __import__('itertools').combinations(ss,2)):continue
   u=0
   for a in ss:u|=a
   out.add((u.bit_count(),sum(a.bit_count() for a in ss)))
 return sorted(out)
for n in range(1,8):print(n,types(n))
for h in range(1,5):
 for part in combinations_with_replacement(range(1,8),h):
  if sum(part)!=7:continue
  pats=sorted(set(tuple(p[1] for p in pp) for pp in product(*(types(n) for n in part)) if sum(p[0] for p in pp)<=5))
  A=np.array([[p[i] for p in pats]+[-part[i]] for i in range(h)]+[[1]*len(pats)+[0]])
  B=[0]*h+[1]
  sol=linprog([0]*len(pats)+[-1],A_eq=A,b_eq=B,bounds=(0,None),method='highs')
  print(part,'maxdegree',-sol.fun*7,'duals',sol.eqlin.marginals.tolist(), 'active',[(p,round(x,4)) for p,x in zip(pats,sol.x) if x>1e-7])
