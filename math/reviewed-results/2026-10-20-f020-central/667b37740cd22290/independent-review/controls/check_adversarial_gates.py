"""Independent direct-sum term enumeration and finite grouped-product controls."""
from pathlib import Path
from fractions import Fraction as Q
import json

def power(p,j):
 out=1
 while j%p==0:out*=p;j//=p
 return out

def mul(a,b,p):
 out=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):out[i+j]=(out[i+j]+x*y)%p
 return out

def gaps(p):
 N=p*p;W=[0]
 for j in range(1,2*N+1):W.append(W[-1]+power(p,j))
 T2=[0]
 for j in range(2*N):T2.append(T2[-1]+(p if j%p==0 else 2))
 delta2=[T2[j]-W[j] for j in range(2*N+1)]
 assert [j for j,v in enumerate(delta2) if v==0]==[0,N,2*N]
 assert min(v for v in delta2 if v)>=(p-1)
 E2=N+4*p*(p-1);D2=3*N+4*p*(p-1)-2*p;Wn=W[N]
 mg=[];hg=[];dg=[];mp=[];dp=[]
 for k in range(1,2*N,2):
  score=2*(W[2*N-1]-W[k]-W[(2*N-1-k)//2])+T2[k]-E2
  if score==0:mp.append(k)
  else:mg.append(score)
 for k in range(0,2*N+1,2):
  score=2*(W[2*N]-W[k]-W[(2*N-k)//2])+T2[k]-2*Wn
  if k not in [0,2*N]:hg.append(score)
  else:assert score==0
  for m in range(k):
   score=2*(W[2*N]-W[(2*N-k)//2]-W[m]-power(p,k-m))+T2[m]-D2
   if score==0:dp.append([k,m])
   else:dg.append(score)
 assert mp==[N] and dp==[[2*N,N]]
 assert min(mg)>=p-1 and min(dg)>=p-1 and min(hg)>=p*p-1
 return dict(p=p,neighbor_pivots=mp,derivative_pivots=dp,neighbor_gap=str(Q(min(mg),2)),H_gap=str(Q(min(hg),2)),derivative_gap=str(Q(min(dg),2)),p3_first_order_gap_mutant_rejected=(p==3 and min(dg)<=2))

def block(p):
 # Coefficients of product(Z+(1+h)^a); A is recovered homogeneously.
 from math import comb
 e=[[1]]
 for a in range(p):
  r=[comb(a,k)%p for k in range(a+1)];new=[[0] for _ in range(len(e)+1)]
  for k,c in enumerate(e):
   z=mul(c,r,p)
   if len(new[k])<len(z):new[k]+=[0]*(len(z)-len(new[k]))
   for h,v in enumerate(z):new[k][h]=(new[k][h]+v)%p
   if len(new[k+1])<len(c):new[k+1]+=[0]*(len(c)-len(new[k+1]))
   for h,v in enumerate(c):new[k+1][h]=(new[k+1][h]+v)%p
  e=new
 orders=[]
 for k,c in enumerate(e):
  c=c[:]
  if k in [0,p]:c[0]=(c[0]-1)%p
  inds=[h for h,v in enumerate(c) if v]
  order=min(inds) if inds else None
  assert order is None or order>=p-1
  orders.append(order)
 return dict(p=p,error_coefficient_orders=orders)

if __name__=='__main__':
 out={'direct_sum_gaps':[gaps(p) for p in [3,5,7,11,13,17,19]],'grouped_product':[block(p) for p in [3,5,7,11]],'role':'Finite falsification controls only; uniform argument audited separately.'}
 Path(__file__).with_name('ADVERSARIAL_GATES.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
