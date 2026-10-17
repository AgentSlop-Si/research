"""Fresh algebraic verification of classical parity and collision identifications."""
import sympy as s,json
from pathlib import Path
x,y,u,m,t=s.symbols('x y u m t')
checks=[]
for parity in (0,1):
 alpha=s.Rational(2*parity-1,2)
 A=2*m+parity-1;c=A*(t-1)/(2*m)
 zc=(m*c*c+(2*m+alpha)*c+m+alpha)/c
 assert s.cancel(2*zc-t*(A*t+1)/(t-1))==0
 for n in range(1,11):
  H=s.hermite_prob(2*n+parity,x)
  R=s.Poly(H,x).all_terms()
  R=sum(coef*y**((power[0]-parity)//2) for power,coef in R)
  lag=s.assoc_laguerre(n,alpha,y/2)
  assert s.expand(R-(-1)**n*2**n*s.factorial(n)*lag)==0
  H0=s.hermite_prob(2*(n-1)+parity,x)
  R0=sum(coef*y**((power[0]-parity)//2) for power,coef in s.Poly(H0,x).all_terms())
  W=s.expand(s.diff(R,y)*R0-R*s.diff(R0,y))
  L=s.assoc_laguerre(n,alpha,u);L0=s.assoc_laguerre(n-1,alpha,u)
  diag=s.diff(L,u)*L0-L*s.diff(L0,u)
  scalar=-2**(2*n-2)*s.factorial(n)*s.factorial(n-1)
  assert s.expand(W-scalar*diag.subs(u,y/2))==0
  assert s.degree(s.gcd(W,s.diff(W,y)),y)==0
  checks.append({'parity':parity,'m':n,'parity_and_kernel_scalars_match':True,'W_squarefree':True})
# Direct ramified negative control, preserving the exact algebraic field.
a=s.sqrt(-2);tau=(-1+2*a)/3
J=x*s.hermite_prob(3,x)-3*tau*s.hermite_prob(2,x)
assert s.expand(J-(x*x-(1+a))**2)==0
# Three explicit sensitivity controls for sign, shift and field guard.
W2=y*y-2*y+3
assert s.expand(W2.subs(y,1+x))==x*x+2
assert s.expand(W2.subs(y,x))!=x*x+2
assert s.discriminant(J,x)==0
r={'status':'PASS','classical_parity_kernel_cases':len(checks),'all_m_collision_location_symbolic_checks':2,'ramified_nonreal_negative_control':True,'unit_shift_negative_control':True,'rows':checks}
Path(__file__).with_name('ATTRIBUTION_RESULT.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='rows'}))
