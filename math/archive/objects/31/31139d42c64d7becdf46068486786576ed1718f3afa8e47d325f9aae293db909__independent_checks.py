#!/usr/bin/env python3
"""Own exact Q(w) arithmetic. No source code imported. w^2+w+1=0."""
from fractions import Fraction as Q
from pathlib import Path
import json,sys,cmath
class E:
 def __init__(self,a=0,b=0):
  if isinstance(a,E): self.a,self.b=a.a,a.b
  else:self.a,self.b=Q(a),Q(b)
 def __add__(self,y):
  y=E(y);return E(self.a+y.a,self.b+y.b)
 __radd__=__add__
 def __neg__(self):return E(-self.a,-self.b)
 def __sub__(self,y):return self+-E(y)
 def __rsub__(self,y):return E(y)+-self
 def __mul__(self,y):
  y=E(y);return E(self.a*y.a-self.b*y.b,self.a*y.b+self.b*y.a-self.b*y.b)
 __rmul__=__mul__
 def inverse(self):
  n=self.a*self.a-self.a*self.b+self.b*self.b
  assert n;return E((self.a-self.b)/n,-self.b/n)
 def __truediv__(self,y):return self*E(y).inverse()
 def __pow__(self,n):
  if n<0:return self.inverse()**(-n)
  out=E(1);a=self
  while n:
   if n&1:out=out*a
   a=a*a;n//=2
  return out
 def __eq__(self,y):y=E(y);return self.a==y.a and self.b==y.b
 def encode(self):return [str(self.a),str(self.b)]
def mm(a,b):return [[sum((x*y for x,y in zip(row,col)),E()) for col in zip(*b)] for row in a]
def eye(n):return [[E(i==j) for j in range(n)] for i in range(n)]
def inverse(a):
 n=len(a);z=[row[:]+eye(n)[i] for i,row in enumerate(a)]
 for j in range(n):
  k=next(k for k in range(j,n) if z[k][j]!=0);z[j],z[k]=z[k],z[j];c=z[j][j].inverse();z[j]=[x*c for x in z[j]]
  for k in range(n):
   if k!=j:
    c=z[k][j];z[k]=[x-c*y for x,y in zip(z[k],z[j])]
 return [row[n:] for row in z]
def main():
 w=E(0,1);F=[[w**(i*j) for j in range(3)] for i in range(3)];A=[[w**(2*i*i) if i==j else E() for j in range(3)] for i in range(3)];Fi=inverse(F);X=[[A[i][j]+Fi[i][j] for j in range(3)] for i in range(3)];B=inverse(X)
 den=4+26*w;d=(-17-16*w)/den;e=(1-4*w)/den;b=w*e;a=w*w*d
 target=[[a,b,b],[b,d,e],[b,e,d]];assert B==target
 assert d!=0 and e!=0 and e/d!=1 and e/d!=E(Q(-1,2))
 # Formal quadratic quotient t^2+t=s. Coefficients are in Q(w).
 s=2*e/d
 def mul(x,y):return (x[0]*y[0]+s*x[1]*y[1],x[0]*y[1]+x[1]*y[0]-x[1]*y[1])
 t=(E(),E(1));t2=mul(t,t);t3=mul(t2,t);one_minus=(E(1)-t3[0],-t3[1]);assert (t[0]+t2[0],t[1]+t2[1])==(s,E())
 # Norm of 1-t^3 in the quadratic algebra detects guard for both roots.
 # Conjugation maps t to -1-t.
 conj=(one_minus[0]-one_minus[1],-one_minus[1]);norm=mul(one_minus,conj);assert norm[1]==0 and norm[0]!=0
 # Numerator of each Green inverse is I+tP+t^2P^2; pair has
 # diagonal 2 and off diagonal t+t^2=s. Scaling cancels denominator.
 unscaled=[[d if i==j else e for j in range(3)] for i in range(3)];D=[w,E(1),E(1)];sand=[[D[i]*unscaled[i][j]*D[j] for j in range(3)] for i in range(3)];assert sand==B
 # Numerical supplementary control for BOTH roots and BOTH primitive roots.
 residuals=[]
 for wc in [complex(-.5,3**.5/2),complex(-.5,-3**.5/2)]:
  dc=(-17-16*wc)/(4+26*wc);ec=(1-4*wc)/(4+26*wc);disc=cmath.sqrt(1+8*ec/dc)
  for tc in [(-1+disc)/2,(-1-disc)/2]:
   kc=dc*(1-tc**3)/2;res=abs(kc*(tc+tc**2)/(1-tc**3)-ec);assert abs(1-tc**3)>1e-8 and res<1e-12;residuals.append(res)
 out=dict(status='PASS',field='Q(w), w^2+w+1=0',target_entries=[[v.encode() for v in row] for row in B],d=d.encode(),e=e.encode(),e_over_d=(e/d).encode(),quadratic_s=s.encode(),guard_norm=norm[0].encode(),matrix_entry_checks=9,both_quadratic_roots_covered=True,complex_controls=len(residuals),uploaded_or_constructor_code_executed=False)
 p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
