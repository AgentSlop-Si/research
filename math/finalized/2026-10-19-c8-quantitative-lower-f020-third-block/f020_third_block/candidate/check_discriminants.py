#!/usr/bin/env python3
"""Compute actual discriminants, then their exact cyclotomic valuations.
This is a fresh supplemental control, independent of the root-distance formula.
"""
from pathlib import Path
import json,hashlib
import sympy as S
X,q,T=S.symbols('X q T')
HERE=Path(__file__).resolve().parent
P=[S.Integer(1),X]
for k in range(1,8):
    P.append(S.Poly(X*P[-1]-(1-q**k)*P[-2],X,q).as_expr())
checks=[]
for b,expected in ((6,27),(7,37),(8,40)):
    D=S.Poly(S.discriminant(P[b],X),q)
    dh=hashlib.sha256(str(D.as_expr()).encode()).hexdigest()
    for s in (2,3):
        e=2*3**(s-1)
        phi=S.Poly(S.cyclotomic_poly(3**s,q),q)
        R=D.rem(phi)
        RT=S.Poly(S.expand(R.as_expr().subs(q,1+T)),T)
        weights=[]
        for (i,),c in RT.terms():
            c=int(c);z=0
            while c%3==0:c//=3;z+=1
            weights.append(dict(T_exponent=int(i),coefficient_v3=z,weight=e*z+int(i)))
        low=min(a['weight'] for a in weights)
        winners=[a for a in weights if a['weight']==low]
        # deg(RT)<e makes the weights distinct modulo e. The unique minimum
        # is therefore the exact valuation after T=q-1, with no cancellation.
        assert RT.degree()<e and len(winners)==1 and low==expected
        checks.append(dict(p=3,s=s,b=b,expected_valuation=expected,actual_valuation=low,
            cyclotomic_degree=e,discriminant_degree_q=D.degree(),
            discriminant_expression_sha256=dh,unique_minimal_term=winners[0],
            passed=True,method='actual symbolic discriminant; remainder modulo Phi_(3^s); exact uniformizer-basis coefficient valuations'))
(HERE/'DISCRIMINANT_CHECKS.json').write_text(json.dumps(dict(all_passed=True,count=len(checks),checks=checks),indent=2)+'\n')
print(f'PASS: {len(checks)} actual discriminant valuations; p=3, b=6,7,8, s=2,3.')
