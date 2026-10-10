"""Fresh exact checks of this assessment's normalization maps, not a research audit."""
import json
from pathlib import Path
import sympy as s
x,t,tau,c=s.symbols('x t tau c')
rows=[]
for A in range(1,10):
 J=s.expand(x*s.hermite_prob(A,x)-A*tau*s.hermite_prob(A-1,x))
 if A%2:
  m=(A+1)//2; alpha=-s.Rational(1,2); cc=s.Rational(A,A+1)*(tau-1)
  P=s.expand((-1)**m*s.factorial(m)*(s.assoc_laguerre(m,alpha,t)+cc*s.assoc_laguerre(m-1,alpha,t)))
  Jmap=s.expand(2**m*P.subs(t,x*x/2))
  dmap=(-1)**m*2**(2*m*m+m)*P.subs(t,0)*s.discriminant(P,t)**2
 else:
  m=A//2; alpha=s.Rational(1,2); cc=tau-1
  P=s.expand((-1)**m*s.factorial(m)*(s.assoc_laguerre(m,alpha,t)+cc*s.assoc_laguerre(m-1,alpha,t)))
  Jmap=s.expand(x*2**m*P.subs(t,x*x/2))
  dmap=(-1)**m*2**(2*m*m+3*m)*P.subs(t,0)**3*s.discriminant(P,t)**2
 assert s.expand(J-Jmap)==0
 assert s.expand(s.discriminant(J,x)-dmap)==0
 rows.append({'check':'J parity and discriminant normalization','A':A,'passed':True})
for m in range(1,6):
 alpha=-s.Rational(1,2)
 f=s.assoc_laguerre(m,alpha,t)+c*s.assoc_laguerre(m-1,alpha,t)
 xi=(m*c*c+(2*m+alpha)*c+m+alpha)/c
 prod=s.prod(s.Integer(k)**(k-2*m+3) for k in range(1,m+1))*s.prod((k+alpha)**(k-1) for k in range(1,m))
 rhs=prod*(-c)**m*f.subs(t,xi)/(m+alpha+c*m)
 assert s.cancel(s.discriminant(f,t)-rhs)==0
 rows.append({'check':'Sawa Uchida Theorem 4.8 normalization','m':m,'passed':True})
for A in range(1,7):
 U=s.hermite_prob(A,x);V=s.expand(s.I**(-A)*s.hermite_prob(A,s.I*x))
 K=s.expand(x*U*V-s.diff(U,x)*V+U*s.diff(V,x))
 ns=list(range(1,A+1))+[2*A+1]
 vand=s.prod(ns[j]-ns[i] for i in range(len(ns)) for j in range(i+1,len(ns)))
 W=s.wronskian([s.hermite_prob(n,x) for n in ns],x)/vand
 assert s.expand(W-K)==0
 rows.append({'check':'hook pseudo Wronskian normalization','A':A,'passed':True})
for p in [3,5,7,11,13,17,19,23,29,31]:
 A=(p-1)//2
 U=s.hermite_prob(A,x);V=s.expand(s.I**(-A)*s.hermite_prob(A,s.I*x))
 K=s.expand(x*U*V-s.diff(U,x)*V+U*s.diff(V,x))
 assert s.Poly(K-x**p,x,modulus=p).is_zero
 rows.append({'check':'hook congruence for odd prime (not paired-good parity claim)','p':p,'passed':True})
Path(__file__).with_name('NORMALIZATION_CHECKS.json').write_text(json.dumps({'checks':rows,'passed':len(rows),'all_passed':True},indent=2)+'\n')
print('All',len(rows),'exact checks passed.')
