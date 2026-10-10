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
 T=inv(G(-1,1,9,2))
 u=[div(sub(ff(a,2),mul(T,G(-1,1,a,2))),G(1,1,a,2)) for a in range(2,9)]
 def solve(A,b):
  M=[row[:]+[v] for row,v in zip(A,b)];size=len(A)
  for j in range(size):
   k=next(k for k in range(j,size) if M[k][j]!=z);M[k],M[j]=M[j],M[k]
   factor=inv(M[j][j]);M[j]=[mul(v,factor) for v in M[j]]
   for k in range(size):
    if k!=j:
     factor=M[k][j];M[k]=[sub(v,mul(factor,w)) for v,w in zip(M[k],M[j])]
  return [row[-1] for row in M]
 A=[s[:4],s[1:5],s[2:6],u[:4]]
 g0=solve(A,[neg(v) for v in [s[6],s[7],s[8],u[6]]])+[z,z,one]
 gl=solve(A,[neg(v) for v in [s[4],s[5],s[6],u[4]]])+[one,z,z]
 gm=solve(A,[neg(v) for v in [s[5],s[6],s[7],u[5]]])+[z,one,z]
 def ev(c,x):
  value=z
  for a in c[::-1]:value=add(mul(value,x),a)
  return value
 B=[[ev(gl,vector(x)),ev(gm,vector(x))] for x in [7,8]]
 lam,mu=solve(B,[neg(ev(g0,vector(x))) for x in [7,8]])
 g=[add(add(v,mul(lam,l)),mul(mu,mv)) for v,l,mv in zip(g0,gl,gm)]
 assert ev(g,vector(7))==ev(g,vector(8))==z
 for r in range(3):
  value=z
  for j,c in enumerate(g):value=add(value,mul(c,s[r+j]))
  assert value==z
 value=z
 for j,c in enumerate(g):value=add(value,mul(c,u[j]))
 assert value==z
 def divide_linear(c,x):
  a=c[:];b=[z]*(len(a)-1)
  for j in range(len(b)-1,-1,-1):b[j]=a[j+1];a[j]=add(a[j],mul(x,b[j]))
  assert a[0]==z
  return b
 quartic=divide_linear(divide_linear(g,vector(7)),vector(8))
 source=Path('research_cycle_1535/basefield_bank_attainment/N11_RATIONAL_ROOT_SPECIALIZATION.json')
 data=json.loads(source.read_text())
 assert vector(data['lambda'])==lam and vector(data['mu'])==mu
 assert [vector(c) for c in data['sextic']]==g
 assert [vector(c) for c in data['residual_quartic']]==quartic
 import hashlib
 return dict(status='PASS',field='Q(q)/(Phi_11)',source_data=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),all_expanded_lambda_mu_coefficients_match=True,all_expanded_sextic_and_quartic_coefficients_match=True,both_forced_root_equations_zero=True,all_four_edge_recurrences_zero=True,sextic_factorization_exact=True)

result=run(11,[],1)
Path(__file__).with_name('N11_INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
