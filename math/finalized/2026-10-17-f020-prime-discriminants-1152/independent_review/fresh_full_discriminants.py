"""Second reviewer: direct Z[q] ordinary discriminants, no reciprocal reduction.
Only SymPy and the standard library are imported; submitted code stays inert.
"""
import sympy as s, json, time, hashlib
from pathlib import Path
q,z,x,t=s.symbols('q z x t')
ROOT=Path(__file__).resolve().parent
MAX_N=10
rows=[[s.Poly(1,q,domain=s.ZZ)]]
H=[s.Integer(1)]
for n in range(1,MAX_N+1):
 old=rows[-1];row=[]
 for k in range(n+1):
  row.append((old[k-1] if k else s.Poly(0,q))+(old[k].mul(s.Poly(q**k,q)) if k<n else s.Poly(0,q)))
 rows.append(row);H.append(sum(a.as_expr()*z**k for k,a in enumerate(row)))
D=[s.Poly(1,q),s.Poly(1,q)]
for n in range(2,MAX_N+1):
 start=time.time();dis=s.Poly(s.discriminant(H[n],z),q,domain=s.ZZ);D.append(dis)
 print(json.dumps({'n':n,'discriminant_q_degree':dis.degree(),'seconds':round(time.time()-start,3)}),flush=True)
 (ROOT/f'DISC_N{n}.json').write_text(json.dumps({'n':n,'coefficients_descending':[int(c) for c in dis.all_coeffs()]})+'\n')
checks=[]
for d,p in [(3,3),(5,5),(7,7),(9,3)]:
 phi=s.Poly(s.cyclotomic_poly(d,q),q,domain=s.QQ)
 def red(a): return s.Poly(a,q,domain=s.QQ).rem(phi)
 def mul(a,b):return (a*b).rem(phi)
 def powr(a,n):
  out=red(1)
  while n:
   if n&1:out=mul(out,a)
   a=mul(a,a);n//=2
  return out
 def inv(a):return s.invert(a,phi)
 def ratio(a,b):return mul(a,inv(b))
 for n in range(MAX_N+1):
  A,b=divmod(n,d)
  if b>=p:continue
  expected=d*A*(A-1)//2+A*(b%2)
  work=D[n].set_domain(s.QQ);order=0
  while work.rem(phi).is_zero:
   work=work.exquo(phi);order+=1
  assert order==expected,(d,n,order,expected)
  if b%2:
   U=s.Poly(H[b],z).exquo(s.Poly(z+1,z)).as_expr()
   g=red(U.subs(z,-1));assert not g.is_zero
   discU=ratio(red(D[b].as_expr()),powr(g,2))
   res=red(1)
   for j in range(d):res=mul(res,red(U.subs(z,-q**j)))
   numerator=red(1);denominator=red(1)
   for j in range(1,b+1):numerator=mul(numerator,red(1-q**j))
   for j in range(1,(d+b)//2+1):denominator=mul(denominator,red(1-q**(2*j)))
   tau=ratio(mul(red(d),numerator),mul(g,denominator))
   if A:
    hh=[s.Integer(1),x]
    for j in range(1,A):hh.append(s.expand(x*hh[-1]-j*hh[-2]))
    J=s.expand(x*hh[A]-A*t*hh[A-1]);discJ=s.Poly(s.discriminant(J,x),t)
    dj=red(0)
    for c in discJ.all_coeffs():dj=mul(dj,tau)+red(c);dj=dj.rem(phi)
   else:dj=red(1)
   PA=s.prod(j**j for j in range(1,A+1))
   scalar=(-1)**(A*((d-1)//2))*d**(d*A*(A+1)//2+A)*PA**(d-1)
   C=mul(red(scalar),mul(dj,mul(discU,mul(powr(res,2*A),powr(g,2)))))
  else:
   res=red(1)
   for j in range(d):res=mul(res,red(H[b].subs(z,-q**j)))
   PA=s.prod(j**j for j in range(1,A+1))
   scalar=(-1)**(A*((d-1)//2))*d**(d*A*(A+1)//2)*PA**d
   C=mul(red(scalar),mul(red(D[b].as_expr()),powr(res,2*A)))
  quotient=mul(C,powr(red(q**(d//p)-1),expected))
  actual=work.rem(phi)
  assert not C.is_zero and actual==quotient,(d,n,C,actual,quotient)
  checks.append({'d':d,'p':p,'n':n,'A':A,'b':b,'order':order,'full_cyclotomic_quotient_match':True,'quotient_coefficients_descending':[str(c) for c in actual.all_coeffs()]})
result={'status':'PASS','method':'Fresh direct ordinary z-discriminants over Z[q] of Gaussian polynomials; exact cyclotomic multiplicity and quotient comparison with separately assembled cluster formula. No reciprocal reduction or source code import.','max_n':MAX_N,'cases':len(checks),'rows':checks}
(ROOT/'FULL_DISCRIMINANT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
