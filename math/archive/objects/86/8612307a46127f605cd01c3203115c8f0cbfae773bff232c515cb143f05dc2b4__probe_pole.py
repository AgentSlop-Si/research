# Newly authored exploratory symbolic polynomial computation.
import sympy as s
r,z=s.symbols('r z')
p=241; zz=91
P=lambda f:s.Poly(f,r,modulus=p)
a=P(1+r*pow(zz,2,p));b=P(1+r*pow(zz,3,p))
c=P(pow(zz,2,p)+r*pow(zz,3,p));e=P(pow(zz,3,p)+r*pow(zz,2,p))
f=P(pow(zz,4,p)+r);hh=P(zz+r)
A=c*a*b;B=e*a*b;C=f*b*b;E=hh*a*a
S=A+B;U=2*C-S;L=B*B-C*E;M=-2*A*B+A*C+A*E+B*C+B*E-2*C*E;J=(B-C)**2
RT=L*U*U-M*U*C+J*C*C
Num=-2*S*J*U*L-M*(-S*J*C+(C*L-S*M)*U)+2*J*(C*L-S*M)*C
Den=L*RT
Guard=a*b*C*(A-B)*(B-C)*(C-S)*L*RT
print('degrees',Num.degree(),Den.degree(),Guard.degree())
g=s.gcd(Num,Den);n=s.exquo(Num,g);d=s.exquo(Den,g)
print('gcd',s.factor(g.as_expr(), modulus=p));print('NUM',n.as_expr());print('DEN',d.as_expr());print('REDUCED',n.degree(),d.degree()); print('GUARD FACTOR',s.factor(Guard.as_expr(),modulus=p))
print('samples',[(x, int(n.eval(x))*pow(int(d.eval(x))%p,-1,p)%p) for x in [0,1,2,3] if d.eval(x)%p])
