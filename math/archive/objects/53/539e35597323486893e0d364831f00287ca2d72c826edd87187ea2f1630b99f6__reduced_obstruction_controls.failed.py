"""Fresh controls for removing the two Gaussian-unit cluster factors."""
from sympy import QQ,Poly,cyclotomic_poly,symbols,factorint
from sympy.polys.rings import ring
from pathlib import Path
from math import gcd
from functools import reduce
from time import perf_counter
import json
OUT=Path(__file__).resolve().parent;q=symbols('q');rows=[]
for d in (17,21,25):
 start=perf_counter(); r=(d-1)//4;n=2*r
 K=QQ.alg_field_from_poly(Poly(cyclotomic_poly(d,q),q),'w');w=K.unit
 R,z=ring('z',K);U,u=ring('u',K)
 h0,h1=R.one,z+1
 for k in range(2,n+1):h0,h1=h1,(1+z)*h1+(w**(k-1)-1)*z*h0
 H=h1;S=[U(2),u]
 for j in range(2,2*r+1):S.append(u*S[-1]-S[-2])
 P=U(H[(r,)])+sum((H[(r+j,)]*S[j] for j in range(1,r+1)),U.zero)
 C=U.one+sum((((-1)**j)*S[j] for j in range(1,2*r+1)),U.zero)
 eta1=-w-w**(-1); eta2=-w**(2*r)-w**(-2*r)
 Cstar,rem=C.div((u-eta1)*(u-eta2));assert rem==0
 hm=H.evaluate(0,-K.one)
 assert H.evaluate(0,-w)==hm
 t=-w**(2*r+1);assert t*t==w
 product=K.one
 for j in range(1,n+1):product*=1+t**j
 assert H.evaluate(0,t)==product
 old=P.evaluate(0,K(2))*P.discriminant()*C.resultant(P)
 new=P.evaluate(0,K(2))*P.discriminant()*Cstar.resultant(P)
 assert old==new*P.evaluate(0,eta1)*P.evaluate(0,eta2)
 V=(u-2)*P.diff(u)*Cstar
 determinant=P.resultant(V)
 assert determinant==(-1)**(r+r*(r-1)//2)*new
 a=list(reversed(determinant.to_list()));assert all(x.denominator==1 for x in a)
 coeffs=[int(x) for x in a];ct=reduce(gcd,map(abs,coeffs))
 row={'d':d,'matrix_size':r,'Cstar_degree':2*r-2,'determinant_coefficients_ascending':coeffs,'determinant_content':str(ct),'determinant_content_factorization':{str(p):v for p,v in factorint(ct).items()},'elapsed_seconds':perf_counter()-start}
 rows.append(row);print({k:row[k] for k in ['d','matrix_size','determinant_content','determinant_content_factorization','elapsed_seconds']},flush=True)
(OUT/'REDUCED_OBSTRUCTION_RESULTS.json').write_text(json.dumps(rows,indent=2)+'\n')
