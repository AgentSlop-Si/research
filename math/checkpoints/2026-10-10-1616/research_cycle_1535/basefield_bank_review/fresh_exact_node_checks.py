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
 fixed=qp[1:N-3];P=[one]
 for y in fixed:
  new=[z]*(len(P)+1)
  for j,c in enumerate(P):new[j]=sub(new[j],mul(y,c));new[j+1]=add(new[j+1],c)
  P=new
 D=z;U=z
 for j,c in enumerate(P):D=add(D,mul(c,s[j]));U=add(U,mul(c,s[j+1]))
 x=div(U,D)
 expected=vector([F(a,denom) for a in coefficients])
 assert x==expected and x!=z and x not in fixed
 nodes=fixed+[x]
 # Construct the split polynomial independently and check its moment functional.
 g=[one]
 for y in nodes:
  new=[z]*(len(g)+1)
  for j,c in enumerate(g):new[j]=sub(new[j],mul(y,c));new[j+1]=add(new[j+1],c)
  g=new
 recurrence=z
 for j,c in enumerate(g):recurrence=add(recurrence,mul(c,s[j]))
 assert recurrence==z
 # Each fixed node and each last node has a legal beta=1 guard.
 guards=[neg(pw(y,N)) for y in nodes]
 assert all(v!=z for v in guards)
 return dict(N=N,field=f'Q(q)/(Phi_{N})',fixed_exponents=list(range(1,N-3)),last_node=[str(v) for v in x],D=[str(v) for v in D],U=[str(v) for v in U],edge_moments=[[str(v) for v in a] for a in s],split_polynomial_coefficients=[[str(v) for v in a] for a in g],recurrence_zero=True,all_nodes_distinct_nonzero=True,all_guards_nonzero=True,status='PASS')

rows=[run(7,[3,-1,-1,0,0,1],2),run(11,[19,41,81,68,13,-18,3,60,80,39],23)]
(OUT/'INDEPENDENT_EXACT_NODE_RESULTS.json').write_text(json.dumps({'status':'PASS','scope':'Exact characteristic-zero nodes, edge moments, split recurrence, and guards; literal matrix controls are separately finite-field.','results':rows},indent=2)+'\n')
print(json.dumps([dict(N=r['N'],last_node=r['last_node'],status=r['status']) for r in rows],indent=2))
