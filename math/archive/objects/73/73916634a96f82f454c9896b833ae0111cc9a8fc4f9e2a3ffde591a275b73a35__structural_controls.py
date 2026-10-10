"""Fresh alternate checks: direct ordinary discriminants/resultants.
Read saved output only as data; do not import any research implementation.
"""
import sympy as s
from sympy.polys.rings import ring
from functools import reduce
from math import gcd
from pathlib import Path
from time import perf_counter
import json
q,z,u=s.symbols('q z u'); OUT=Path(__file__).resolve().parent
results=[]
for d in [17,21,25]:
 t=perf_counter();b=(d-1)//2;r=b//2
 K=s.QQ.alg_field_from_poly(s.Poly(s.cyclotomic_poly(d,q),q),'w');w=K.unit
 R,Z=ring('Z',K);U,X=ring('X',K)
 # Gaussian multiplicative definition, rather than recurrence/Pascal.
 row=[K.one]
 for k in range(1,b+1):row.append(row[-1]*(1-w**(b-k+1))/(1-w**k))
 G=sum((row[k]*Z**k for k in range(b+1)),R.zero)
 direct_disc=G.discriminant()
 direct_res=(Z**d+1).resultant(G)
 C=[U(2),X]
 for k in range(2,2*r+1):C.append(X*C[-1]-C[-2])
 P=U(row[r])+sum((row[r+j]*C[j] for j in range(1,r+1)),U.zero)
 # Reciprocal contraction of (Z^d+1)/(Z+1): alternating coefficients.
 Cd=U.one+sum((((-1)**j)*C[j] for j in range(1,2*r+1)),U.zero)
 # Middle coefficient equals 1 because 2r is even.
 hminus=G.evaluate(0,-K.one);hplus=G.evaluate(0,K.one)
 sp=P.discriminant();rp=Cd.resultant(P)
 assert direct_res==hminus*rp**2
 assert direct_disc==P.evaluate(0,K(2))*P.evaluate(0,K(-2))*sp**2
 assert direct_disc*direct_res==(-1)**r*hplus*(hminus*sp*rp)**2
 # Alternating Gaussian sum identity.
 expected=K.one
 for j in range(1,b,2):expected*=1-w**j
 assert hminus==expected
 a=json.loads((OUT/f'base_{d}.json').read_text())
 def coeffs(v):
  a=list(reversed(v.to_list()));assert all(c.denominator==1 for c in a)
  return [int(c) for c in a] or [0]
 assert coeffs(direct_disc)==a['discriminant_coefficients_ascending']
 assert coeffs(direct_res)==a['cluster_resultant_coefficients_ascending']
 assert coeffs(direct_disc*direct_res)==a['B_coefficients_ascending']
 # Smaller non-square obstruction has same non-d prime support.
 small=coeffs(hplus*sp*rp);content=reduce(gcd,map(abs,small))
 entry={'d':d,'checks':'direct discriminant; direct resultant; reciprocal identity; alternating Gaussian identity; saved exact arrays', 'reduced_obstruction_content':str(content),'reduced_obstruction_content_factors':{str(k):v for k,v in s.factorint(content).items()},'elapsed_seconds':perf_counter()-t}
 results.append(entry);print(entry,flush=True)
# Formal local diagonal evaluations, arbitrary j demonstrated symbolically.
t,j=s.symbols('t j')
# Use truncated (1+t)^j via symbolic binomial expansion; coefficients rational polynomials in j.
formal=[]
for r in range(1,6):
 n=2*r;row=[s.Poly(1,q)]
 for a in range(1,n+1):row=[(row[k-1] if k else s.Poly(0,q))+(s.Poly(q**k,q)*row[k] if k<a else s.Poly(0,q)) for k in range(a+1)]
 # H_n(-q^j;q)=sum_k (-1)^k [n k]_q q^(jk).
 truncated=0
 for k,c in enumerate(row):
  for (e,),ce in c.terms():
   truncated+=(-1)**k*ce*sum(s.prod(e+j*k-h for h in range(a))/s.factorial(a)*t**a for a in range(r+1))
 truncated=s.Poly(s.expand(truncated),t)
 assert all(truncated.nth(a)==0 for a in range(r))
 lead=(-1)**r*s.factorial2(2*r-1)
 assert truncated.nth(r)==lead
 formal.append({'r':r,'j':'symbolic integer','order':r,'leading_coefficient':str(lead)})
print('formal local controls passed',formal,flush=True)
(OUT/'STRUCTURAL_CONTROL_RESULTS.json').write_text(json.dumps({'fixed_base_controls':results,'formal_local_controls':formal},indent=2)+'\n')
