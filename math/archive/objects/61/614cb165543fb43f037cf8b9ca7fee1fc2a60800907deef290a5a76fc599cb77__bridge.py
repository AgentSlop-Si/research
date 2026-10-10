#!/usr/bin/env python3
"""Exact finite-field tests of the two-additive-stage sparse-bridge identity.
The algebraic equality is valid over any field if A,B,C,D and CB invertible.
No claim any tested product equals the Fourier transform.
"""
import json, random
from verify import make_cycle, weights_non_singular, product_sparse

Q=998244353

def sparse_to_dense(rows):
 n=len(rows)
 return [[rows[i].get(j,0)%Q for j in range(n)] for i in range(n)]

def mm(a,b):
 n=len(a);out=[[0]*n for _ in range(n)]
 for i in range(n):
  for k in range(n):
   x=a[i][k]
   if x:
    for j in range(n):out[i][j]=(out[i][j]+x*b[k][j])%Q
 return out

def plus(a,b):
 return [[(x+y)%Q for x,y in zip(ra,rb)] for ra,rb in zip(a,b)]

def inv(a):
 n=len(a);m=[row[:]+[int(j==i) for j in range(n)] for i,row in enumerate(a)]
 for i in range(n):
  piv=next((j for j in range(i,n) if m[j][i]%Q),None)
  if piv is None:raise ValueError('singular')
  m[piv],m[i]=m[i],m[piv]
  div=pow(m[i][i],-1,Q)
  m[i]=[(v*div)%Q for v in m[i]]
  for j in range(n):
   if j!=i and m[j][i]:
    z=m[j][i];m[j]=[(v-z*w)%Q for v,w in zip(m[j],m[i])]
 return [row[n:] for row in m]

def denom(n,rng):
 suc,_=make_cycle(n,rng)
 w=weights_non_singular(n,Q,rng,zeros=True)
 return sparse_to_dense([{i:1,suc[i]:(-w[i])%Q} for i in range(n)])

def run():
 ans=[]
 for n in [5,7,8,11,13]:
  for trial in range(4):
   rng=random.Random(1000*n+trial)
   a,b,c,d=[denom(n,rng) for _ in range(4)]
   ai,bi,ci,di=[inv(z) for z in (a,b,c,d)]
   m=mm(plus(ai,bi),plus(ci,di))
   x=plus(a,b);y=plus(c,d);k=mm(c,b)
   bridge=mm(mm(x,inv(k)),y)
   sand=mm(mm(a,m),d)
   assert bridge==sand
   assert m==mm(mm(mm(ai,bridge),di),[[int(i==j) for j in range(n)] for i in range(n)])
   # Deliberately wrong noncommutative bridge orientation must be rejected.
   wrong=mm(mm(x,inv(mm(b,c))),y)
   assert wrong!=bridge
   ans.append({'n':n,'trial':trial,'bridge_equal':True,'wrong_BC_order_rejected':True})
 print('Bridge tests:',len(ans),'PASS')
 with open('BRIDGE_RESULTS.json','w') as f:json.dump({'tests':len(ans),'cases':ans},f,indent=2)
if __name__=='__main__':run()
