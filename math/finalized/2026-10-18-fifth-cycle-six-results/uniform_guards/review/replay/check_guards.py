"""Fresh transcription controls for F020 uniform guard proof; no downloaded code."""
import sympy as S
import json, sys, platform
from pathlib import Path
q,z,x,t=S.symbols('q z x t')
ROOT=Path(__file__).resolve().parent
checks=[]
def ck(name,condition,extra=None):
 assert condition,name
 checks.append({'name':name,'passed':True,**(extra or {})})
def H(n):
 row=[S.Integer(1)]
 for m in range(1,n+1):
  row=[S.expand((row[k] if k<m else 0)+(q**(m-k)*row[k-1] if k else 0)) for k in range(m+1)]
 return S.Poly(sum(c*z**k for k,c in enumerate(row)),z).as_expr()
for b in range(7):
 h=H(b)
 ck(f'q_difference_b{b}',S.expand(h.subs(z,q*z)-(1-z)*h-q**b*z*h.subs(z,z/q))==0)
 ck(f'reciprocity_b{b}',S.expand(z**b*h.subs(z,1/z)-h)==0)
 ck(f'half_lattice_product_b{b}',S.expand(h.subs({q:t*t,z:t},simultaneous=True)-S.prod(1+t**k for k in range(1,b+1)))==0)
 if b%2==0:
  e=S.prod(1-q**(2*k-1) for k in range(1,b//2+1))
  ck(f'even_initial_b{b}',S.expand(h.subs(z,-1)-e)==0 and S.expand(h.subs(z,-q)-e)==0)
 else:
  e=S.prod(1-q**(2*k-1) for k in range(1,(b+1)//2+1))
  ck(f'odd_initial_b{b}',h.subs(z,-1)==0 and S.expand(h.subs(z,-q)-e)==0)
 if b>=2:
  D=S.Poly(S.discriminant(h,z),q)
  N=b*(b-1)//2
  V,rem=S.div(D,S.Poly((q-1)**N,q))
  ck(f'discriminant_monic_b{b}',D.LC()==1 and D.degree()==b*(b*b-1)//3)
  ck(f'deflation_monic_b{b}',rem.is_zero and V.LC()==1 and V.degree()==b*(b-1)*(2*b-1)//6)
# Exact old failure of the proposed strict bound, not a characteristic-zero obstruction.
h4=H(4);D4=S.discriminant(h4,z);V4=S.cancel(D4/(q-1)**6)
v3=S.Poly(V4.subs(q,1+t),t,modulus=3)
valuation=min(m[0] for m,c in v3.terms())
ck('finite_t_strict_bound_fails_b4_p3_d9',valuation==8 and valuation>=S.totient(9),{'t':valuation,'phi':int(S.totient(9)),'V4':str(S.factor(V4)),'V4_mod3_shifted':str(v3.as_expr())})
# One already-covered actual-family case checked independently in the exact number field.
K=S.QQ.alg_field_from_poly(S.Poly(S.cyclotomic_poly(9,q),q),'w')
w=K.unit
R=K.poly_ring(z);zz=R.gens[0]
row=[K.one]
for m in range(1,5):
 row=[(row[k] if k<m else K.zero)+(w**(m-k)*row[k-1] if k else K.zero) for k in range(m+1)]
h=R.zero
for k,c in enumerate(row):h+=c*zz**k
ck('b4_d9_charzero_squarefree_despite_t_failure',h.gcd(h.diff(0)).degree()==0)
# Independent CD and H-to-P transformations.
P=[S.Integer(1),x]
for n in range(1,6):P.append(S.expand(x*P[-1]-(1-q**n)*P[-2]))
for b in range(1,7):
 ck(f'hermite_transform_b{b}',S.expand(t**b*P[b].subs(x,t+1/t)-H(b).subs(z,t*t))==0)
 rhs=S.diff(P[b],x)*P[b-1]-P[b]*S.diff(P[b-1],x)
 lhs=sum(P[k]**2*S.prod(1-q**j for j in range(k+1,b)) for k in range(b))
 ck(f'cd_diagonal_b{b}',S.expand(lhs-rhs)==0)
# Rotation bookkeeping without numerical complex powers: put q=t^16.
for b in (0,1,4):
 lam=2*t**(-4*(2*b+1))
 for j in (S.Rational(1,2),S.Integer(1),S.Rational(3,2),S.Integer(2)):
  c=lambda a:8*b*a+4*a*a
  coefficient1=S.expand((1+t**(16*j))*t**(c(j)-c(j+1)))
  coefficient2=S.expand(t**(16*(b+j)+c(j-1)-c(j+1)))
  ck(f'rotation_b{b}_j{j}',S.expand(coefficient1-lam*(t**(8*j)+t**(-8*j))/2)==0 and coefficient2==1)
# Selected already-covered root orders, both parities and endpoint b=d-1.
for d,b in ((3,1),(5,4),(9,4),(9,5),(9,8)):
 K=S.QQ.alg_field_from_poly(S.Poly(S.cyclotomic_poly(d,q),q),'w')
 w=K.unit
 phi=S.Poly(S.cyclotomic_poly(d,q),q)
 ck(f'field_definition_d{d}_b{b}',sum((K.convert(c)*w**k for (k,),c in phi.terms()),K.zero)==K.zero)
 R=K.poly_ring(z);zz=R.gens[0]
 row=[K.one]
 for m in range(1,b+1):
  row=[(row[k] if k<m else K.zero)+(w**(m-k)*row[k-1] if k else K.zero) for k in range(m+1)]
 hb=R.zero
 for k,c in enumerate(row):hb+=c*zz**k
 ub=hb.exquo(zz+1) if b%2 else hb
 ck(f'negative_nodes_d{d}_b{b}',ub.gcd(zz**d+1).degree()==0)
 ck(f'positive_nodes_d{d}_b{b}',hb.gcd(zz**d-1).degree()==0)
 if b%2:ck(f'forced_derivative_d{d}_b{b}',hb.diff(0).evaluate(0,-K.one)!=K.zero)

# Positivity-style shortcut fails even for a nondegenerate ordered-phase recurrence.
u=[(3-4*S.I)/5,S.Rational(4,5),(3+4*S.I)/5]
poly=[S.Integer(1),x]
for a in u:poly.append(S.expand(x*poly[-1]-a*poly[-2]))
ck('nondegenerate_complex_jacobi_can_repeat',S.expand(poly[-1]-(x*x-1)**2)==0)
result={'status':'PASS','assertions':len(checks),'python':sys.version,'sympy':S.__version__,'scope':'Small transcription controls, no order extension or finite census. Theorems use the proofs.','checks':checks}
(ROOT/'CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','assertions':len(checks),'output':'CHECKS.json'},indent=2))
