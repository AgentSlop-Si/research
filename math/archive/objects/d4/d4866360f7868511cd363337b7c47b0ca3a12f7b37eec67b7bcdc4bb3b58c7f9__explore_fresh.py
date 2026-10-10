import sympy as s
q,z=s.symbols('q z')
def mod(e):return s.Poly(e,q,z,modulus=2).as_expr()
h0,h1=1,z+1
for n in range(2,13):
 h0,h1=h1,mod((z+1)*h1+(1+q**(n-1))*z*h0)
 if n%2==0:
  d=s.Poly(s.resultant(h1,s.diff(h1,z),z),q,modulus=2)
  print(n,s.factor_list(d),flush=True)
