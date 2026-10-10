import sympy as s
x,t,q=s.symbols('x t q')
for A in range(1,9):
 j=s.expand(x*s.hermite_prob(A,x)-A*t*s.hermite_prob(A-1,x))
 disc=s.factor(s.discriminant(j,x))
 rr=s.rem(disc.subs(t,1-q),q*q+q+1,q)
 print(A,disc,'=>',s.factor(rr), 'content',s.Poly(rr,q).content(), flush=True)
