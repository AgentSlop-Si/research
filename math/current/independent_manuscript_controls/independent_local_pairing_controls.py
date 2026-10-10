"""Fresh exact coefficient/discriminant controls and finite-field pairing checks."""
from pathlib import Path
from math import prod,factorial
import json,time
import sympy as S
ROOT=Path(__file__).resolve().parent
q,z,x,y=S.symbols('q z x y')
def H(n):
 a=S.Poly(1,z,q);b=S.Poly(1+z,z,q)
 if n==0:return a
 for j in range(2,n+1):a,b=b,S.Poly(1+z,z,q)*b+S.Poly((q**(j-1)-1)*z,z,q)*a
 return b

def he(n):return S.hermite_prob(n,y)
local=[]
for d,A,b in [(3,1,0),(3,2,0),(3,1,1),(3,2,1),(3,1,2),(3,2,2),(5,1,1),(5,1,2),(5,1,3)]:
 start=time.time();n=d*A+b;hn=H(n);phi=S.Poly(S.cyclotomic_poly(d,q),q)
 K=S.QQ.alg_field_from_poly(phi,alias='w');w=K.unit
 def evaluate_q(coeff):
  coeff=S.Poly(coeff,q);out=K.zero
  for (e,),v in coeff.terms():out+=K.convert(v)*w**e
  return out
 def poly_specialize(f):
  f=S.Poly(f,z,q);out={}
  for (k,e),v in f.terms():out[(k,)]=out.get((k,),K.zero)+K.convert(v)*w**e
  return S.Poly.from_dict(out,z,domain=K)
 G=poly_specialize(H(b));F=S.Poly(z**d+1,z,domain=K);overlap=b%2==1
 if overlap:
  U,rem=G.div(S.Poly(z+1,z,domain=K));assert rem.is_zero
  g=U.rep.eval(-1);num=K.one;den=K.one
  for j in range(1,b+1):num*=K.one-w**j
  for j in range(1,(b+d)//2+1):den*=K.one-w**(2*j)
  tau=d*num/(den*g)
  J=S.Poly(y*he(A),y,domain=K)-S.Poly(S.diff(he(A),y),y,domain=K).mul_ground(tau)
  assert J.rep.discriminant()!=K.zero
  C=(-1)**(A*((d-1)//2))*d**(d*A*(A+1)//2+A)*prod(j**j for j in range(1,A+1))**(d-1)
  C=K.convert(C)*J.rep.discriminant()*(U.rep.discriminant() if U.degree() else K.one)*F.rep.resultant(U.rep)**(2*A)*g**2
  exponent=d*A*(A-1)//2+A;alpha=-K.one;order=A+1
  # sqrt(d) cancels: use expanded Hermite coefficients in y.
  expected={}
  for (j,),c in J.rep.to_dict().items():
   assert (A-1+j)%2==0
   expected[j]=((-1)**(A+1+j))*d**((A-1+j)//2)*g*c
 else:
  assert (G.degree()==0 or G.rep.discriminant()!=K.zero) and F.rep.resultant(G.rep)!=K.zero
  C=(-1)**(A*((d-1)//2))*d**(d*A*(A+1)//2)*prod(j**j for j in range(1,A+1))**d
  C=K.convert(C)*(G.rep.discriminant() if G.degree() else K.one)*F.rep.resultant(G.rep)**(2*A)
  exponent=d*A*(A-1)//2;alpha=-w;order=A
  galpha=G.rep.eval(alpha);expected={}
  for (j,),c in S.Poly(he(A),y,domain=K).rep.to_dict().items():
   assert (A+j)%2==0
   expected[j]=(-1)**A*d**((A+j)//2)*galpha*c/alpha**j
 # Direct Taylor coefficient from each z^k q^e monomial.
 for level in range(order+1):
  got={}
  for (k,e),c in hn.terms():
   for j in range(min(k,level)+1):
    if (level-j)%2:continue
    value=K.convert(c*S.binomial(k,j)*S.binomial(S.Rational(e,d),(level-j)//2))*alpha**(k-j)*w**e
    got[j]=got.get(j,K.zero)+value
  got={j:c for j,c in got.items() if c!=K.zero}
  assert got==({} if level<order else expected),(d,A,b,level)
 # Global discriminant coefficient via exact cyclotomic division.
 D=S.Poly(S.discriminant(hn.as_expr(),z),q);divisor=phi**exponent
 E,rem=D.div(divisor);assert rem.is_zero
 remainder=E.rem(phi);assert not remainder.is_zero
 Q=S.Poly(q**d-1,q).exquo(phi)
 assert evaluate_q(remainder.as_expr())==evaluate_q(Q.as_expr())**exponent*C,(d,A,b)
 row={'d':d,'A':A,'b':b,'type':'overlap' if overlap else 'separated','leading_polynomial_verified':True,'exact_cyclotomic_order':exponent,'leading_discriminant_coefficient_verified':True,'seconds':round(time.time()-start,3)}
 local.append(row);print(json.dumps(row),flush=True)
pairing=[]
for p in list(S.primerange(3,102)):
 A=(p-1)//2;H0=S.Poly(he(A),y,modulus=p);Hp=H0.diff()
 # Exact Wronskian polynomial identity using V(y)=i^-A H(iy):
 # Every monomial has parity A, hence i^(j-A) = (-1)^((A-j)/2).
 V=S.Poly.from_dict({(j,):c*(-1)**((A-j)//2) for (j,),c in H0.terms()},y,modulus=p)
 W=Hp*V-H0*V.diff()-S.Poly(y,y,modulus=p)*H0*V
 assert W==S.Poly(-y**p,y,modulus=p)
 bad=[]
 for tau in range(2,p):
  other=tau*pow(tau-1,-1,p)%p
  J=S.Poly(y,y,modulus=p)*H0-Hp.mul_ground(tau)
  J2=S.Poly(y,y,modulus=p)*H0-Hp.mul_ground(other)
  fail=J.gcd(J.diff()).degree()>0 and J2.gcd(J2.diff()).degree()>0
  assert fail==(p%4==1 and tau==2),(p,tau)
  if fail:bad.append(tau)
 pairing.append({'p':int(p),'all_prime_field_pairs_checked':p-2,'simultaneous_failures':bad,'wronskian_identity':True})
(ROOT/'independent_local_pairing_results.json').write_text(json.dumps({'local_expansions':local,'finite_characteristic_pairing':pairing},indent=2)+'\n')
