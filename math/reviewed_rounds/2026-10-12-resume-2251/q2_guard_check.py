#!/usr/bin/env python3
"""Self-authored exact rational checks; no supplied programs are imported."""
from fractions import Fraction as F
from pathlib import Path
import json

def matmul(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def det(a):
 a=[list(map(F,r)) for r in a];v=F(1);n=len(a)
 for i in range(n):
  k=next((k for k in range(i,n) if a[k][i]),None)
  if k is None:return F(0)
  if k!=i:a[k],a[i]=a[i],a[k];v=-v
  pivot=a[i][i];v*=pivot
  for j in range(i+1,n):
   ratio=a[j][i]/pivot
   for t in range(i,n):a[j][t]-=ratio*a[i][t]
 return v
I=eye(4)
A=[[F(0) for _ in range(4)] for _ in range(4)]
B=[[F(0) for _ in range(4)] for _ in range(4)]
for a in range(2):
 for c in range(2):
  i=2*a+c;A[i][2*((a-1)%2)+c]=1;B[i][2*a+(c-1)%2]=(-1)**a
C=[[A[i][j]+B[i][j] for j in range(4)] for i in range(4)]
L=[[I[i][j]-C[i][j] for j in range(4)] for i in range(4)]
G=[[-I[i][j]-C[i][j] for j in range(4)] for i in range(4)]
assert matmul(C,C)==[[2*x for x in r] for r in I]
assert matmul(L,G)==I and matmul(G,L)==I
assert det(L)==1
blocks=[[[1,-1],[-1,1]],[[1,1],[1,1]]]
assert all(det(x)==0 for x in blocks)
y=[row[0] for row in G]
assert y==[-1,-1,-1,0]
# The published small coefficient schedule is always guarded for integer m>=2.
# These rational controls supplement the immediate inequalities 0<4^-m<1
# and 0<2*4^-m<=1/8<1; they do not replace that all-m proof.
controls=[]
for m in range(2,65):
 b=F(1,4)**m;delta=1-2*b
 assert b!=1 and delta>0
 controls.append({'m':m,'beta_power':str(b),'full_denominator':str(delta)})
r={'status':'PASS','m':2,'q':-1,'alpha':1,'beta':1,'full_operator_determinant':str(det(L)),
   'full_operator':[[int(x) for x in r] for r in L],
   'inverse':[[int(x) for x in r] for r in G],
   'row_block_determinants':[str(det(x)) for x in blocks],
   'solution_for_e0':[int(x) for x in y],
   'guarded_fixed_schedule_controls':controls,
   'scope':'Counterexample only to extending the stated row-inverse elimination beyond beta^m!=1. Supplied code and prior theorem already guard it; no supplied program executed.'}
Path(__file__).with_name('q2_guard_results.json').write_text(json.dumps(r,indent=2)+'\n')
print('PASS: full L determinant 1, both row blocks singular; exact inverse verified; 63 fixed-schedule rational controls')
