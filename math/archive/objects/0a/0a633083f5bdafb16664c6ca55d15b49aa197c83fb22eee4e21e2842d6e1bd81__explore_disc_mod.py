import sympy as s
x,t=s.symbols('x t')
for p in [3,7,11,19,23,31,43]:
 A=(p-1)//2
 j=s.Poly(x*s.hermite_prob(A,x)-A*t*s.hermite_prob(A-1,x),x,t,modulus=p).as_expr()
 di=s.discriminant(j,x)
 print(p,s.factor(di, modulus=p), flush=True)
