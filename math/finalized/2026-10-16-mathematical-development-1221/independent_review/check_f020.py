import sympy as s,json
q,x,y=s.symbols('q x y')
def mod(f):return s.Poly(f,x,q,modulus=2).as_expr()
def valuation(f):
 if f==0:return None
 g=s.Poly(f,q,modulus=2);v=0
 while g.eval(1)==0:g=g.exquo(s.Poly(q+1,q,modulus=2));v+=1
 return v
P=[s.Integer(1),x+q+q*q];rows=[]
for j in range(2,10):P.append(mod((x+q**(2*j-1)*(1+q))*P[-1]+(1+q**(2*j-1))*(1+q**(2*j-2))*P[-2]))
for m in range(1,10):
 T=s.Poly(mod(P[m].subs(x,x+q+q*q)),x);r=m//2
 assert valuation(P[m].subs(x,0))==m
 residual=[0,0]
 for (i,),coef in T.terms():
  k=m-i;v=valuation(coef);assert v is None or v>=3*((k+1)//2)
  # coefficient of tilde pair: divide by prescribed w power minus substituted Y power.
  target=3*r if m%2==0 or i%2 else 3*(r+1)
  power=target-3*(i//2)
  if power<0:raise AssertionError()
  d=s.Poly(coef,q,modulus=2).exquo(s.Poly((1+q)**power,q,modulus=2))
  residual[i%2]+=int(d.eval(1))%2*y**(i//2)
 if r:
  expected=[(y+1)**r,(r%2)*(y+1)**(r-1)] if m%2==0 else [(r%2)*y*(y+1)**(r-1),(y+1)**r]
  for a,b in zip(residual,expected):assert s.Poly(a-b,y,modulus=2).is_zero
 rows.append({'m':m,'endpoint_valuation':m,'all_weighted_coefficients_and_residuals_pass':True})
print(json.dumps(rows,indent=2))
