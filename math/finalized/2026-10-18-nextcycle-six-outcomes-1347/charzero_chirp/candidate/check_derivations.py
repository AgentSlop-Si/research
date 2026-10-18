#!/usr/bin/env python3
"""Bind certificate input polynomials back to the displayed necessary equations."""
import json,sympy as s
from pathlib import Path
D,E=s.symbols('D E');a=6;b=4;p=17
cs=json.loads((Path(__file__).parent/'CERTIFICATES.json').read_text())
def num(e):return s.Poly(s.cancel(e).as_numer_denom()[0],D,E,modulus=p)
def fromdata(v):return s.Poly(sum(c*D**m[0]*E**m[1] for m,c in v),D,E,modulus=p)
def compare(name,eqs):
 expected=[fromdata(v) for v in cs[name]['inputs']]
 actual=[num(e) for e in eqs]
 assert actual==expected,name
h=D/(D+a*E);A=a*h/E;B=-a*h/D;C=(b*h-E)/D;F=E*(s.Rational(b,a)+1/D)
compare('330',[A+C*E+F-a*h,C+D+B*F+a*h,A*D+C*F-h])
R=1-E**2-D**2*E;A=D**3/R;C=-D-A*E;B=E-D**2-A*D*E
u=A*D;v=B;r=-B*D;t=-A*E
ls=[(v-b*u,u-b*v),(r+t,r-t),(r-a*u,-t-a*v)]
compare('312',[1+B*E-A*D]+[ls[i][0]*ls[j][1]-ls[i][1]*ls[j][0] for i,j in [(0,1),(0,2),(1,2)]])
compare('510',[a*D**2-D+a,b*D**4+a*D**3+D**2+a*D+b])
EE=b+a*D+a/D;h=D/(D+a*EE)
compare('420',[EE-D**2-h*(a*D+b),a/EE-a*EE-D*EE/h-a])
B=-2*D**2/(1+D**4);A=2*D**3/(1+D**4);H=D*(D**4-1)/(1+D**4);e=(b-B)/(1-b*B)
compare('411',[A+H+(A-H)*e,A-H*e-a*(1+B*e)])
print('PASS: all five stored polynomial lists match the exact rational necessary equations.')
