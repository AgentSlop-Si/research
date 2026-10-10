"""Independent exact cyclotomic-field checks of displayed small-order nodes."""
import json
from fractions import Fraction as F
from pathlib import Path
import sympy as sp
OUT=Path(__file__).resolve().parent

def run(N,coefficients,denom):
 n=N-1;t=sp.Symbol('t');phi=sp.Poly(sum(t**j for j in range(N)),t,domain=sp.QQ)
 def vector(v):
  if isinstance(v,(int,F)):return (F(v),)+(F(0),)*(n-1)
  return tuple(F(x) for x in v)+(F(0),)*(n-len(v))
 z=vector(0);one=vector(1);q=vector([0,1])
 def add(a,b):return tuple(x+y for x,y in zip(a,b))
 def neg(a):return tuple(-x for x in a)
 def sub(a,b):return add(a,neg(b))
 def mul(a,b):
  c=[F(0)]*(2*n-1)
  for i,x in enumerate(a):
   for j,y in enumerate(b):c[i+j]+=x*y
  for k in range(2*n-2,n-1,-1):
   v=c[k]
   for j in range(n):c[k-n+j]-=v
  return tuple(c[:n])
 memo={}
 def inv(a):
  if a not in memo:
   pol=sp.Poly(sum(sp.Rational(v.numerator,v.denominator)*t**j for j,v in enumerate(a)),t,domain=sp.QQ)
   ip=sp.invert(pol,phi)
   memo[a]=tuple(F(ip.nth(j)) for j in range(n))
  return memo[a]
 def div(a,b):return mul(a,inv(b))
 def pw(a,k):
  c=one
  for j in range(k):c=mul(c,a)
  return c
 qp=[pw(q,j) for j in range(N)]
 def G(e,dd,a,b):
  r=e*a%N;ell=dd*b%N
  if r+ell>N-1:return z
  value=one
  for j in range(1,ell+1):value=mul(value,div(sub(one,qp[e*dd*(r+j)%N]),sub(one,qp[e*dd*j%N])))
  return value
 h=pow(4,-1,N);H=div(q,add(one,q))
 def ff(a,b):return qp[h*(a+b)**2%N]
 s=[div(sub(div(ff(a,1),H),G(-1,1,a,1)),G(1,1,a,1)) for a in range(1,N-1)]
 assert s[0]==one and s[2]==q
 A=vector([F(v,29) for v in [-31,-5,5,20,-1,-18]])
 B=vector([F(v,29) for v in [-9,-37,-21,3,10,6]])
 g=[neg(mul(q,B)),sub(B,mul(q,A)),sub(A,q),one]
 expected=[[6,15,43,27,3,-4],[-27,-24,-34,-20,-28,-11],[-31,-34,5,20,-1,-18]]
 assert g[:3]==[vector([F(v,29) for v in c]) for c in expected]
 for r in [0,1]:
  recurrence=z
  for j,c in enumerate(g):recurrence=add(recurrence,mul(c,s[j+r]))
  assert recurrence==z
 disc=sub(mul(A,A),mul(vector(4),B))
 assert disc==vector([F(v,841) for v in [1215,3313,1617,-1884,-1843,60]])
 assert B!=z and add(add(pw(q,2),mul(A,q)),B)!=z and disc!=z
 return dict(N=N,exact_field='Q(q)/(Phi_7)',cubic_ascending=[[str(v) for v in c] for c in g],quadratic_ascending=[[str(v) for v in c] for c in [B,A,one]],discriminant=[str(v) for v in disc],both_exact_recurrences_zero=True,constant_nonzero=True,quadratic_discriminant_nonzero=True,forced_root_not_quadratic_root=True,status='PASS')

result=run(7,[],1)
Path(__file__).with_name('N7_INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['cubic_ascending','quadratic_ascending','discriminant']},indent=2))
