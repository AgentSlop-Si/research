import json, random, sys
from sympy import isprime,primitive_root
from probe_constraints import rref

def setup(n,p,q):
 h=pow(4,-1,n)
 def G(a,b,e,d):
  r=e*a%n;l=d*b%n
  if r+l>=n:return 0
  z=pow(q,e*d%(n),p);v=1
  for j in range(1,l+1):v=v*(1-pow(z,r+j,p))*pow(1-pow(z,j,p),-1,p)%p
  return v
 def f(a,b):return pow(q,h*(a+b)**2%n,p)
 seq=[]
 for b in range(1,(n+1)//2):
  T=pow(G(n-b,b,-1,1),-1,p)
  seq.append([(f(a,b)-T*G(a,b,-1,1))*pow(G(a,b,1,1),-1,p)%p for a in range(1,n-b)])
 return seq,G,f

def rempow(n,c,p):
 m=len(c)-1;P=[]
 for k in range(n):
  if k<m:v=[int(j==k) for j in range(m)]
  else:v=[-sum(c[j]*P[k-m+j][i] for j in range(m))%p for i in range(m)]
  P.append(v)
 return P

def good(n,c,p):
 from sympy import Poly, symbols
 t=symbols('t');g=Poly(sum(c[j]*t**j for j in range(len(c))),t,modulus=p)
 if not c[0] or g.gcd(g.diff()).degree():return False,None
 P=rempow(n,c,p);m=len(c)-1
 axis=[P[a]+[1]+P[-a%n] for a in range(n)]
 _,piv=rref(axis,p)
 return len(piv)==n,piv

def probe(n):
 p=n+1
 while not isprime(p):p+=n
 q=pow(int(primitive_root(p)),(p-1)//n,p)
 seq,G,f=setup(n,p,q);out=[];rng=random.Random(n)
 for m in range((n-1)//2,n-1):
  rows=[s[r:r+m+1] for s in seq for r in range(len(s)-m)]
  R,piv=rref(rows,p)
  if m in piv:
   out.append([m,len(rows),len(piv),False]);continue
  free=[j for j in range(m) if j not in piv]
  success=None
  for trial in range(40):
   c=[0]*m+[1]
   for j in free:c[j]=rng.randrange(p) if trial else 0
   for i,j in enumerate(piv):c[j]=-sum(R[i][k]*c[k] for k in free+[m])%p
   ok,cols=good(n,c,p)
   if ok:success={'coefficients':c,'axis_columns':cols,'trial':trial};break
  out.append([m,len(rows),len(piv),bool(success)])
  if success:
   return {'N':n,'p':p,'q':q,'probes':out,'witness':success,'bank_count':2*m+2,'m':m,'pivot_columns':piv,'pivot_rows':None}
 return {'N':n,'p':p,'q':q,'probes':out}
if __name__=='__main__':
 out=[]
 for n in list(range(7,66,2))+[71,79,89,101,113,127,151]:
  d=probe(n);out.append(d);print(n,d.get('m'),d.get('bank_count'),d['probes'][-3:],flush=True)
  with open('research_cycle_1735/common_annihilator_barrier/FULL_LEFT_RESULTS.json','w') as f:json.dump(out,f,indent=2)
