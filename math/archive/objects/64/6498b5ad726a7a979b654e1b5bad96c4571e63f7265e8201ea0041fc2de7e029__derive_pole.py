# Newly authored exploratory computation. Final verifier will not import this file.
import sympy as sy, json
from sympy.polys.rings import ring
from pathlib import Path
z=sy.symbols('z'); K=sy.QQ.algebraic_field(sy.CRootOf(z**4+z**3+z**2+z+1,0)); R,r=ring('r',K); zz=R(K.unit)
a=1+r*zz**2;b=1+r*zz**3;c=zz**2+r*zz**3;e=zz**3+r*zz**2;f=zz**4+r;hh=zz+r
A=c*a*b;B=e*a*b;C=f*b*b;E=hh*a*a
S=A+B;U=2*C-S;L=B*B-C*E;M=-2*A*B+A*C+A*E+B*C+B*E-2*C*E;J=(B-C)**2
RT=L*U*U-M*U*C+J*C*C
N=-2*S*J*U*L-M*(-S*J*C+(C*L-S*M)*U)+2*J*(C*L-S*M)*C
D=L*RT
Guard=a*b*C*(A-B)*(B-C)*(C-S)*L*RT
print('gcd start', flush=True);g=N.gcd(D); n=N.exquo(g); d=D.exquo(g)
print('degrees',N.degree(),D.degree(),g.degree(),n.degree(),d.degree(), flush=True)
# Simultaneously normalize denominator constant to 1.
k=d[(0,)];n=n.quo_ground(k);d=d.quo_ground(k)
print('squarefree start', flush=True); ge=Guard.gcd(Guard.diff(r)); guard=Guard.exquo(ge).monic();print('squarefree guard degree',guard.degree(), flush=True)
def coeffs(p):
  return [[str(x) for x in reversed(p.get((i,),K.zero).to_list())]+['0']*(4-len(p.get((i,),K.zero).to_list())) for i in range(p.degree()+1)]
obj={'numerator':coeffs(n),'denominator':coeffs(d),'squarefree_guard':coeffs(guard),'canceled_gcd':coeffs(g)}
path=Path(__file__).with_name('POLE_RATIONAL_DATA.json');path.write_text(json.dumps(obj,indent=2)+'\n');print(path)
print('n',obj['numerator']);print('d',obj['denominator']);print('e',obj['squarefree_guard'])
