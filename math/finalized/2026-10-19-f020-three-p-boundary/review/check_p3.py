import json, hashlib, sympy as S
from pathlib import Path
q,x,y=S.symbols('q x y')
P0=S.Poly(1,x); P1=S.Poly(x,x)
for n in range(1,9):
    P0,P1=P1,S.Poly(S.expand(x*P1.as_expr()+(q**n-1)*P0.as_expr()),x)
P9=P1.as_expr()
Q=S.Poly(sum(c*y**((j[0]-1)//2) for j,c in P1.terms()),y)
assert S.expand(x*Q.as_expr().subs(y,x*x)-P9)==0
D=S.Poly(Q.eval(0),q)
Delta=S.Poly(S.discriminant(Q.as_expr(),y),q)
checks={}
for s in [3,4]:
    phi=S.Poly(S.cyclotomic_poly(3**s,q),q)
    checks[str(s)]={}
    for label,F in [('D',D),('Delta',Delta)]:
        rem=F.rem(phi); gcd=S.gcd(F,phi)
        assert not rem.is_zero and gcd.degree()==0
        checks[str(s)][label]={'phi_degree':phi.degree(),'gcd_degree':gcd.degree(),'remainder_low_first':[int(c) for c in reversed(rem.all_coeffs())]}
assert 2*3**4>max(D.degree(),Delta.degree())
checks['s_at_least_5']={'phi_degree_at_least':2*3**4,'D_degree':D.degree(),'Delta_degree':Delta.degree(),'reason':'A nonzero polynomial of smaller degree cannot be divisible by the minimal cyclotomic polynomial.'}
checks['Q_coefficients_high_first']=[str(S.expand(c)) for c in Q.all_coeffs()]
checks['D_factorization']=str(S.factor(D.as_expr()))
checks['Delta_factorization']=str(S.factor(Delta.as_expr()))
# Compare candidate's stated exact factor vectors to independently reconstructed polynomials.
source=Path(__file__).with_name('CANDIDATE_P3_CERTIFICATE.json')
candidate=json.loads(source.read_text())
R=S.Poly(sum(v*q**j for j,v in enumerate(candidate['R14_coefficients_low_first'])),q)
E=S.Poly(sum(v*q**j for j,v in enumerate(candidate['E52_coefficients_low_first'])),q)
assert D==S.Poly((q-1)**4*(q*q+q+1)*R.as_expr(),q)
assert Delta==S.Poly((q-1)**12*(q+1)**6*(q*q+1)**2*(q*q+q+1)**3*E.as_expr(),q)
rem2=S.Poly(E,q,modulus=2).rem(S.Poly(q**18+q**9+1,q,modulus=2))
assert rem2==S.Poly(q**13+q**12+q**10+q**9+q**6+q**5+q*q+q+1,q,modulus=2)
assert S.Poly(S.discriminant(P9,x),q)==256*D**3*Delta**2
checks['candidate_factor_vectors_match']=True
checks['candidate_mod2_remainder_matches']=True
checks['degree9_discriminant_identity']=True
checks['status']='PASS: P9=XQ4(X^2); D and quartic discriminant nonzero at every primitive 3^s-th root for s>=3.'
Path(__file__).with_name('P3_CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
print(checks['status'])
