"""Fresh exact symbolic certificate for every primitive 3^s root, s>=3.
The recurrence is rebuilt here. No historical checker or scratch file is read.
"""
import sympy as S
import json
from pathlib import Path
q,x,y=S.symbols('q x y');checks=[]
def check(name,b):
    assert b,name
    checks.append({'check':name,'passed':True})
old=S.Integer(1);P=x
for n in range(1,9):old,P=P,S.expand(x*P-(1-q**n)*old)
Q=sum(c*y**((j[0]-1)//2) for j,c in S.Poly(P,x).terms())
check('Exact identity P9=X Q4(X^2)',S.expand(P-x*Q.subs(y,x*x))==0)
co=S.Poly(Q,y).all_coeffs();check('Q is monic quartic',len(co)==5 and co[0]==1)
_,a,b,c,d=co
disc_formula=256*d**3-192*a*c*d**2-128*b**2*d**2+144*b*c**2*d-27*c**4+144*a**2*b*d**2-6*a**2*c**2*d-80*a*b**2*c*d+18*a*b*c**3+16*b**4*d-4*b**3*c**2-27*a**4*d**2+18*a**3*b*c*d-4*a**3*c**3-4*a**2*b**3*d+a**2*b**2*c**2
disc=S.Poly(S.discriminant(Q,y),q).as_expr()
check('Quartic discriminant matches explicit 16-term formula',S.expand(disc-disc_formula)==0)
R14=[5,11,17,25,32,36,39,39,34,28,22,14,8,4,1]
E52=[400,1200,3484,8140,17353,32979,59408,99345,158657,240592,350885,490963,664623,868696,1102292,1356748,1625307,1893889,2152130,2383469,2577374,2720023,2805073,2825452,2782425,2677227,2518707,2315386,2080597,1826209,1566017,1310706,1070721,852721,661837,499942,367300,261962,181195,121251,78354,48745,29108,16603,9008,4611,2207,978,392,138,41,9,1]
R=sum(v*q**i for i,v in enumerate(R14));E=sum(v*q**i for i,v in enumerate(E52))
phi3=q*q+q+1
check('Exact Q4(0) factorization',S.expand(d-(q-1)**4*phi3*R)==0)
check('Exact quartic discriminant factorization',S.expand(disc-(q-1)**12*(q+1)**6*(q*q+1)**2*phi3**3*E)==0)
phi27=q**18+q**9+1
rem=S.rem(S.Poly(E,q,modulus=2),S.Poly(phi27,q,modulus=2)).as_expr()
expected=q**13+q**12+q**10+q**9+q**6+q**5+q*q+q+1
check('Explicit E52 remainder modulo (2,Phi27)',S.expand(rem-expected)==0)
check('Nonzero remainder certificate',rem!=0)
check('R14 degree below all phi(3^s), s>=3',S.degree(R,q)==14<18 and R14[-1]==1)
check('E52 degree below all phi(3^s), s>=4',S.degree(E,q)==52<54 and E52[-1]==1)
check('Cyclotomic minimum polynomials',S.cyclotomic_poly(27,q)==phi27 and S.degree(S.cyclotomic_poly(81,q),q)==54)
# The general factor identity follows by partitioning roots into 0 and +/-sqrt(y_i).
# Check it symbolically as a second independent resultant calculation.
discP=S.discriminant(P,x)
check('Exact Disc_X P9=256 Q4(0)^3 Disc_Y(Q4)^2',S.expand(discP-256*d**3*disc**2)==0)
cert={'status':'PASS','checks_passed':len(checks),'checks':checks,'recurrence':'P0=1,P1=X,P(n+1)=X*Pn-(1-q^n)*P(n-1)','P9_X_coefficients':{str(j[0]):str(c) for j,c in S.Poly(P,x).terms()},'R14_coefficients_low_first':R14,'E52_coefficients_low_first':E52,'E52_remainder_mod_2_Phi27':str(rem),'Q4_constant_degree':int(S.degree(d,q)),'Q4_discriminant_degree':int(S.degree(disc,q)),'P9_discriminant_degree':int(S.degree(discP,q)),'uniform_scope':'Every primitive 3^s root with s>=3; nonvanishing uses rational cyclotomic minimal-polynomial divisibility and the stated degree bounds.'}
Path(__file__).with_name('P3_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks_passed':len(checks),'P9_discriminant_degree':int(S.degree(discP,q))},indent=2))
