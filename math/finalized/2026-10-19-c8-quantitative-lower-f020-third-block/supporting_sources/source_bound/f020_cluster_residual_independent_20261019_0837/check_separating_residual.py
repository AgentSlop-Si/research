"""Fresh local transcription checks for the independent degree-2p residual note."""
import json
from fractions import Fraction
from pathlib import Path
import sympy as s

T,X=s.symbols('T X')
results=[]
for p in (3,5,7,11):
    q=1+T
    P=[s.Integer(1),X]
    for n in range(1,2*p):
        P.append(s.Poly(X*P[-1]-(1-q**n)*P[-2],X,T).as_expr())
    lam=s.Poly(P[p],X).coeff_monomial(X)
    c=(-1)**((p+1)//2)
    C=s.prod(1-q**(2*j-1) for j in range(1,p+1))
    assert s.expand(P[2*p].subs(X,0)+C)==0
    threshold=Fraction(4*p-1,2)
    variants=[]
    for label,a1 in [('exact_linear_coefficient',lam),('leading_linear_coefficient',c*T**(p-1))]:
        A=X**p+a1*X
        E=s.Poly(P[2*p]-A*A+C,X,T,modulus=p)
        weights=[Fraction(tdeg)+Fraction(2*p-1,2*p)*xdeg for (xdeg,tdeg),coef in E.terms() if coef]
        val=min(weights) if weights else None
        assert val is None or val>threshold
        assert p*(p-1)>threshold
        variants.append({'variant':label,'error_min_weight_mod_p':str(val),'threshold':str(threshold)})
    Z=s.symbols('Z')
    resid=s.Poly(Z**p+c*Z,Z,modulus=p)
    assert s.gcd(resid,resid.diff()).degree()==0
    assert Fraction(2*p*(p-1))+2*p*p*Fraction(2*p-1,2*p)==p*(4*p-3)
    results.append({'p':p,'c':c,'minimum_e':p*(p-1),'residual_squarefree':True,'variants':variants})
output={'status':'PASS','role':'Finite transcription controls only; the written proof supplies the uniform theorem.','results':results}
Path(__file__).with_name('CHECKS.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
