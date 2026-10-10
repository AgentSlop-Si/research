import sympy as s
q,z=s.symbols('q z')
def H(n):
 a=s.Integer(1);b=1+z
 if n==0:return a
 for k in range(2,n+1):a,b=b,s.expand((1+z)*b+(q**(k-1)-1)*z*a)
 return b
for d in [3,7,11,15,19]:
 b=(d-1)//2;m=(b+d)//2;ph=s.cyclotomic_poly(d,q)
 def R(x):return s.rem(x,ph,q)
 def prod(seq):
  r=1
  for e in seq:r=R(r*(1-q**(e%d)))
  return r
 h=H(b);g=R(s.diff(h,z).subs(z,-1));u=s.div(h,z+1,z)[0]
 w=R(prod(range(1,b+1))*s.invert(prod([2*i for i in range(1,m+1)]),ph,q));v=R(d*w)
 gi=R(g.subs(q,q**(d-1)));vi=R(v.subs(q,q**(d-1)))
 identity=R(g*vi+gi*v-v*vi)
 print('d',d,'g',g,'v',v,'identity=',identity,flush=True)
