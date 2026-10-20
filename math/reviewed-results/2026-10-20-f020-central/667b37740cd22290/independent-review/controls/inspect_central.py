from math import comb
from fractions import Fraction
import json, time
from pathlib import Path
class Field:
 def __init__(self,p,s):
  self.p=p; self.s=s; self.qorder=p**s; self.gap=p**(s-1);self.e=(p-1)*self.gap
  self.zero=[0]*self.e;self.one=[1]+[0]*(self.e-1)
 def shiftq(self,a,k):
  out=[0]*self.e
  for j,c in enumerate(a):
   if not c:continue
   u=(j+k)%self.qorder
   if u<self.e: out[u]+=c
   else:
    for h in range(self.p-1):out[u-self.e+h*self.gap]-=c
  return out
 def add(self,a,b,sgn=1):return [x+sgn*y for x,y in zip(a,b)]
 def tpower(self,a,k):
  out=[0]*self.e
  for h in range(k+1):
   c=comb(k,h)*(-1)**(k-h);sh=self.shiftq(a,h)
   out=[x+c*y for x,y in zip(out,sh)]
  return out
 def vu(self,a):
  # independent explicit binomial q=1+t transform
  b=[sum(a[j]*comb(j,i) for j in range(i,self.e)) for i in range(self.e)]
  opts=[]
  for i,x in enumerate(b):
   if x:
    k=0
    while x%self.p==0:x//=self.p;k+=1
    opts.append((i+k*self.e, x*(-1)**k%self.p))
  return min(opts) if opts else None
 def odd(self,m):
  A=[self.one];B=[self.one]
  for i in range(1,m+1):
   U_B=[self.zero]+B
   A=[self.add(U_B[j],self.add(self.shiftq(A[j],2*i-1),A[j],-1)) if j<len(A) else U_B[j] for j in range(i+1)]
   B=[self.add(A[j],self.add(self.shiftq(B[j],2*i),B[j],-1)) if j<len(B) else A[j] for j in range(i+1)]
  return B
 def central_shift(self,coeff):
  c=[self.zero]
  for a in reversed(coeff):
   tc=[self.tpower(x,self.p) for x in c]
   new=[[0]*self.e for _ in range(len(c)+1)]
   for i,x in enumerate(tc):new[i]=self.add(new[i],x,-1);new[i+1]=self.add(new[i+1],x)
   new[0]=self.add(new[0],a);c=new
  return c[:-1]
if __name__=='__main__':
 import sys
 pairs=[tuple(map(int,x.split(','))) for x in sys.argv[1:]] or [(3,3),(3,4),(5,3),(7,3)]
 rows=[]
 for p,s in pairs:
  st=time.time();K=Field(p,s);f=K.odd(p*p);c=K.central_shift(f);wv=3*p*p-2*p
  tab=[dict(j=j,valuation=v[0]-wv,unit=v[1]) for j,a in enumerate(c) if (v:=K.vu(a)) is not None]
  delta=Fraction(tab[0]['valuation'],p)
  base=tab[0]['valuation']
  assert [r['j'] for r in tab if r['valuation']+r['j']*delta==base]==[0,p]
  assert all(r['valuation']+r['j']*delta>=base for r in tab)
  dt=[]
  for r in tab:
   j=r['j']
   if not j: continue
   z=j;v=0
   while z%p==0:z//=p;v+=1
   dt.append((Fraction(r['valuation'])+v*K.e+(j-1)*delta,j))
  dm=min(x[0] for x in dt); piv=[j for x,j in dt if x==dm]
  assert piv==([2] if p==3 else [1])
  assert dm==(Fraction(13,3) if p==3 else Fraction(p*(p-1),2)+1)
  if p>=5:
   assert tab[1]['unit']==pow(8,-1,p)
   assert tab[1]['unit']!=(-pow(8,-1,p))%p
  derivative=dict(root_V_weight=str(delta),ordinary_derivative_weight=str(dm),unique_pivot=piv,original_P_derivative_weight=str(wv+dm))
  print(p,s,'seconds',time.time()-st,'rows',tab,flush=True);rows.append(dict(p=p,s=s,e=K.e,table=tab,derivative=derivative))
 Path(__file__).with_name('independent_centered_coefficients.json').write_text(json.dumps(rows,indent=2)+'\n')
