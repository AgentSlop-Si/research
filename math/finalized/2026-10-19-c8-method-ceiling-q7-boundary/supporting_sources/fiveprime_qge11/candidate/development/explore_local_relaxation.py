from itertools import combinations,product
from scipy.optimize import linprog
from fractions import Fraction
from functools import lru_cache
import json
F={n:set() for n in range(1,6)}
for n in range(2,6):
 for a in combinations(range(1,32),n):
  if all((x&y).bit_count()==1 for x,y in combinations(a,2)):
   c=31;u=0
   for x in a:c&=x;u|=x
   if not c:F[n].add((u.bit_count(),sum(x.bit_count() for x in a)))
print('nonstars',F)
def choices(n):
 if n==1:return [(k,k) for k in range(6)]
 return [(k,n+k-1) for k in range(1,6)]+list(F.get(n,[]))
def parts(n,k,mini=1):
 if k==0:
  if n==0:yield ()
  return
 for a in range(mini,n//k+1):
  for b in parts(n-a,k-1,a):yield(a,)+b
for q in [7,11,13,17,19,23,29,31,37,41,43]:
 out=[]
 for k in range(1,5):
  for ns in parts(q,k):
   patterns=[]
   for cs in product(*[choices(n) for n in ns]):
    if sum(x[0] for x in cs)<=5:patterns.append([x[1] for x in cs])
   # weights lambda local incidence n*d/q; t=d/q variable
   # max t s.t sum lambda=1, avginc n*t
   eq=[[1]*len(patterns)+[0]]
   for i,n in enumerate(ns):eq.append([p[i] for p in patterns]+[-n])
   obj=[0]*len(patterns)+[-1]
   r=linprog(obj,A_eq=eq,b_eq=[1]+[0]*k,bounds=[(0,None)]*(len(patterns)+1),method='highs')
   if r.success:
    excess=q*(r.x[-1]-1)
    if excess>=2.99:out.append({'partition':ns,'tmax':str(Fraction(excess).limit_denominator()),'duals':[str(Fraction(x).limit_denominator()) for x in r.eqlin.marginals]})
 print(q,out)
