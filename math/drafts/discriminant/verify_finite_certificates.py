"""Fresh exact check for this manuscript. Only JSON data are read from source packets.
Ring arithmetic, q-Pascal construction and degree-reduced determinants are implemented here.
"""
from pathlib import Path
from itertools import permutations
from math import gcd
from functools import reduce
import json

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'certificates'
REVIEW=ROOT/'certificates'

class Ring:
 def __init__(self,phi):
  self.phi=phi;self.d=len(phi)-1
  self.zero=(0,)*self.d;self.one=(1,)+(0,)*(self.d-1)
 def e(self,a):
  if isinstance(a,int):return (a,)+(0,)*(self.d-1)
  a=list(a)
  for k in range(len(a)-1,self.d-1,-1):
   c=a[k]
   for j in range(self.d):a[k-self.d+j]-=c*self.phi[j]
  return tuple((a+[0]*self.d)[:self.d])
 def add(self,a,b):return tuple(x+y for x,y in zip(a,b))
 def neg(self,a):return tuple(-x for x in a)
 def sub(self,a,b):return self.add(a,self.neg(b))
 def mul(self,a,b):
  c=[0]*(2*self.d-1)
  for i,x in enumerate(a):
   for j,y in enumerate(b):c[i+j]+=x*y
  return self.e(c)
 def scale(self,a,n):return tuple(n*x for x in a)
 def power(self,a,n):
  c=self.one
  while n:
   if n&1:c=self.mul(c,a)
   a=self.mul(a,a);n//=2
  return c
 def eval(self,a,x):
  c=self.zero
  for v in reversed(a):c=self.add(self.mul(c,x),self.e(v) if isinstance(v,int) else v)
  return c

def trim(a,R):
 a=list(a)
 while a and a[-1]==R.zero:a.pop()
 return a

def psub(a,b,R):
 a=a+[R.zero]*max(0,len(b)-len(a));b=b+[R.zero]*max(0,len(a)-len(b))
 return trim([R.sub(x,y) for x,y in zip(a,b)],R)

def pmul(a,b,R):
 c=[R.zero]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=R.add(c[i+j],R.mul(x,y))
 return trim(c,R)

def rem(a,P,R):
 a=trim(a,R);n=len(P)-1
 while len(a)>n:
  c=a[-1];j=len(a)-len(P)
  for k,x in enumerate(P):a[j+k]=R.sub(a[j+k],R.mul(c,x))
  a=trim(a,R)
 return a

def determinant(M,R):
 n=len(M);out=R.zero
 for p in permutations(range(n)):
  sign=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
  v=R.one
  for i in range(n):v=R.mul(v,M[i][p[i]])
  out=R.add(out,R.scale(v,sign))
 return out

def resultant(P,B,R):
 n=len(P)-1
 if n==0:return R.one
 cols=[]
 for j in range(n):
  c=rem([R.zero]*j+B,P,R);cols.append(c+[R.zero]*(n-len(c)))
 return determinant([[cols[j][i] for j in range(n)] for i in range(n)],R)

def disc(P,R):
 n=len(P)-1
 if n<=1:return R.one
 der=[R.scale(P[j],j) for j in range(1,len(P))]
 return R.scale(resultant(P,der,R),(-1)**(n*(n-1)//2))

def cyclo(s):
 # Construct Phi_s recursively, with exact monic integer division.
 polys={}
 for n in range(1,s+1):
  if s%n:continue
  a=[-1]+[0]*(n-1)+[1]
  for d in range(1,n):
   if n%d:continue
   b=polys[d];out=[0]*(len(a)-len(b)+1)
   while len(a)>=len(b):
    k=len(a)-len(b);c=a[-1];out[k]=c
    for j,x in enumerate(b):a[k+j]-=c*x
    while a and a[-1]==0:a.pop()
   assert not a;a=out
  polys[n]=a
 return polys[s]

def run(s):
 R=Ring(cyclo(s));q=R.e([0,1]);b=(s-1)//2;r=(s-3)//4
 row=[R.one]
 for n in range(1,b+1):
  new=[]
  for k in range(n+1):
   a=row[k] if k<n else R.zero
   v=R.mul(R.power(q,n-k),row[k-1]) if k else R.zero
   new.append(R.add(a,v))
  row=new
 # Divide H_b by z+1 from the constant coefficient upwards.
 U=[];prev=R.zero
 for a in row[:-1]:prev=R.sub(a,prev);U.append(prev)
 assert U[-1]==row[-1]==R.one
 assert U==list(reversed(U))
 # Write z^-r U = u_r + sum u_(r+j) S_j(t).
 S=[[R.e(2)],[R.zero,R.one]]
 for j in range(2,r+1):S.append(psub([R.zero]+S[-1],S[-2],R))
 P=[U[r]]
 for j in range(1,r+1):P=psub(P,[R.neg(R.mul(U[r+j],x)) for x in S[j]],R)
 # C_1=1,C_3=t-1 and C_(j+2)=t C_j-C_(j-2).
 C0=[R.one];C1=[R.e(-1),R.one]
 if s==1:C=C0
 else:
  for j in range(3,s,2):C0,C1=C1,psub([R.zero]+C1,C0,R)
  C=C1
 pp=R.eval(P,R.e(2));pm=R.eval(P,R.e(-2));dp=disc(P,R);pc=resultant(P,C,R)
 du=R.mul(R.mul(pp,pm),R.mul(dp,dp))
 res=R.scale(R.mul(pm,R.mul(pc,pc)),(-1)**r)
 gamma=R.mul(du,res);qi=R.power(q,s-1);gi=R.eval(gamma,qi)
 g=R.eval(U,R.e(-1));v=R.one
 for j in range(1,r+1):v=R.mul(v,R.sub(R.one,R.power(q,2*j)))
 for j in range(b):v=R.mul(v,R.sub(R.one,R.power(q,2*j+1)))
 delta=R.sub(R.scale(g,2),v);pair=R.mul(gamma,gi);aug=R.mul(pair,delta)
 own={'U':U,'P':P,'g':g,'v':v,'delta':delta,'disc_U':du,'res_F_U':res,'Gamma':gamma,'Gamma_pair':pair,'augmented':aug}
 src=json.loads((SRC/f'EXACT_CONTENT_S{s}.json').read_text())
 assert src['phi_ascending']==R.phi
 checks={k:json.loads(json.dumps(x))==src[k] for k,x in own.items()}
 assert all(checks.values()),(s,checks)
 reviewer=json.loads((REVIEW/f'INDEPENDENT_EXACT_S{s}.json').read_text())
 content=reduce(gcd,aug);bez=reviewer['augmented_gcd_bezout_coefficients']
 assert sum(x*y for x,y in zip(aug,bez))==content
 assert R.add(R.mul(g,R.eval(v,qi)),R.mul(R.eval(g,qi),v))==R.mul(v,R.eval(v,qi))
 return {'s':s,'all_fields_match':checks,'content':content,'bezout_verified':True,'inverse_identity_verified':True,'method':'fresh q-Pascal; reciprocal degree reduction; permutation determinants of size at most four'}

if __name__=='__main__':
 rows=[run(s) for s in [3,7,11,15,19]]
 (ROOT/'FRESH_FINITE_CHECKS.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(json.dumps(rows,indent=2))
