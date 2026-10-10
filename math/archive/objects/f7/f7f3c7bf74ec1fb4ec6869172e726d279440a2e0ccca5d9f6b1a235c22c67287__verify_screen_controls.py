"""Independent complete-basis positive control and rank-screen validation."""
from pathlib import Path
import json, random
import numpy as np
from endpoint_rank_screen import PRIME, fourier, rank_tables, reject, pcount

p=PRIME
n=16
w=pow(3,(p-1)//n,p); ii=pow(w,4,p)
leaf=np.array([[1,1,1,1],[-1,-1,1,1],[ii,-ii,1,-1],[-ii,ii,1,-1]],dtype=np.int64)%p
h=np.zeros((n,n),dtype=np.int64)
for b in range(0,n,4):h[b:b+4,b:b+4]=leaf
rev=[(t%4)*4+t//4 for t in range(n)]
g1=[b+r for b in range(0,n,4) for r in [1,3,0,2]]
s1=[b+r for b in range(0,n,4) for r in [0,2,1,3]]
g2=[j+4*r for j in range(4) for r in [1,3,0,2]]
s2=[j+4*r for j in range(4) for r in [0,2,1,3]]
tw=[pow(w,j*r,p) for j in range(4) for r in [1,3,0,2]]
inv_s1=[s1.index(t) for t in range(n)]
row_to_col=[inv_s1[g] for g in g2]
perm=[row_to_col.index(j) for j in range(n)]
P=np.zeros((n,n),dtype=np.int64)
for j,i in enumerate(perm):P[i,j]=1
r=s2;c=[rev[g] for g in g1]
target=fourier(n)[np.ix_(r,c)]
actual=h@np.diag(tw)@P@h%p
assert np.array_equal(actual,target)
tables=rank_tables(target)
assert reject(perm,tables) is None
# Independent brute Gaussian ranks versus incremental tables on 200 random rectangles.
def rank(a):
 a=a.tolist(); rows=len(a); cols=len(a[0]) if rows else 0; k=0
 for j in range(cols):
  pivot=next((i for i in range(k,rows) if a[i][j]%p),None)
  if pivot is None:continue
  a[k],a[pivot]=a[pivot],a[k]; inv=pow(a[k][j]%p,-1,p)
  a[k]=[v*inv%p for v in a[k]]
  for i in range(k+1,rows):
   c=a[i][j]%p
   a[i]=[(x-c*y)%p for x,y in zip(a[i],a[k])]
  k+=1
 return k
rng=random.Random(260109)
for _ in range(200):
 k=rng.randrange(n+1);l=rng.randrange(n+1)
 assert int(tables[0][k,l])==rank(target[:k,:l])
q=pcount(perm)
assert all(int(q[k,l])==sum(i<k for i in perm[:l]) for k in range(n+1) for l in range(n+1))
result=dict(status='passed',prime=p,n=n,positive_control='Explicit two-stage radix-4 complete matrix equality',basis_columns_checked=n,independent_rectangle_ranks=200,row_order=r,column_order=c,middle_input_to_output_permutation=perm,screen_passed=True)
Path(__file__).with_name('control_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
