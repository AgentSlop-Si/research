from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog

def partitions(n,lo=1):
 if n==0:yield ()
 for k in range(lo,n+1):
  for p in partitions(n-k,k):yield (k,)+p

def pats(labels, comps):
 choices=[[m for m in range(1,32) if m>>l&1] for l in labels]
 out=[]
 def rec(ss):
  j=len(ss)
  if j==7:
   out.append(tuple(ss));return
  for m in choices[j]:
   if all((m&s).bit_count()==int(comps[i]==comps[j]) for i,s in enumerate(ss)):rec(ss+[m])
 rec([])
 return out
for aa in partitions(3):
 for bb in partitions(4):
  if len(aa)+len(bb)>5:continue
  labels=[]
  for i,n in enumerate(aa+bb):labels +=[i]*n
  pp=pats(labels,[0]*3+[1]*4)
  ww=sorted(set(tuple(m.bit_count() for m in p) for p in pp))
  A=np.array([[p[i] for p in ww]+[-1] for i in range(7)]+[[1]*len(ww)+[0]])
  sol=linprog([0]*len(ww)+[-1],A_eq=A,b_eq=[0]*7+[1],bounds=(0,None),method='highs')
  print(aa,bb,'patterns',len(pp),'weighttypes',len(ww),'maxd',None if sol.fun is None else -sol.fun*7,'duals',sol.eqlin.marginals,flush=True)
