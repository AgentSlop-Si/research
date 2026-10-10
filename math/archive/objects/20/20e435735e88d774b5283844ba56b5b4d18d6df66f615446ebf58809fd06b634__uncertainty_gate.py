"""Permutation-endpoint independent DFT subspace uncertainty gate.
For H of length h and spectral output I of t positions, the intersection
E_H intersect F^{-1}(E_I) has dimension d <= floor(h*t/n), by trace of
orthogonal projection products for normalized complex DFT.
Hence t-floor(ht/n) <= relevant QS rank budget.
"""
from itertools import permutations
from collections import Counter

def uncertainty_violations(pi,cup=1,cdown=1,bup=1,bdown=1):
 n=len(pi); fail=[]
 for u in range(n):
  a=n;b=-1
  for v in range(u,n):
   t=v-u+1
   a=min(a,pi[v]);b=max(b,pi[v]); h=b-a+1
   bcost=(u>0)*bup+(v<n-1)*bdown
   budget=bcost+(a>0)*cup+(b<n-1)*cdown
   necessary=t-(h*t)//n
   if necessary>budget:fail.append((u,v,a,b,t,h,necessary,budget))
 return fail

if __name__=='__main__':
 from prior_window_gate import check_windows
 count=Counter(); witness={}
 for perm in permutations(range(8)):
  a=not check_windows(perm)
  b=not uncertainty_violations(perm)
  count[a,b]+=1
 print(dict(count))
 for n,pi in [(16,[0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15]),(32,list(range(32)))]:
  print(n,pi,'uncertainty violations',len(uncertainty_violations(pi)), 'first',uncertainty_violations(pi)[:2])
