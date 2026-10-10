#!/usr/bin/env python3
"""Fresh finite-characteristic controls for the uniform symbolic proof."""
import sympy as s,json
from pathlib import Path
x,t=s.symbols('x t');out=[]
def Hp(n):
    a=s.Integer(1);b=x
    if n==0:return a
    for j in range(1,n):a,b=b,s.expand(x*b-j*a)
    return b
for p in (3,7,11,19,23):
    A=(p-1)//2;U=Hp(A)
    # i^(-A) H_A(i*x): term x^(A-2j) is multiplied by (-1)^j.
    V=s.expand(sum(c*(-1)**((A-k[0])//2)*x**k[0] for k,c in s.Poly(U,x).terms()))
    W=s.Poly(s.diff(U,x)*V-U*s.diff(V,x)-x*U*V,x,modulus=p)
    assert W==s.Poly(-x**p,x,modulus=p)
    J=s.expand(x*U-t*s.diff(U,x))
    Dj=s.Poly(s.discriminant(J,x),t,modulus=p)
    m=Dj.degree()
    pulled=s.Poly(s.expand(sum(c*t**k[0]*(t-1)**(m-k[0]) for k,c in Dj.terms())),t,modulus=p)
    common=s.gcd(Dj,pulled).monic()
    bad=common
    zero_mult=0
    while bad.degree()>0 and bad.eval(0)==0:
        bad,rem=s.div(bad,s.Poly(t,t,modulus=p));assert rem.is_zero;zero_mult+=1
    assert bad.degree()==0
    out.append(dict(p=p,A=A,wronskian_is_minus_x_to_p=True,disc_J_mod_p=str(Dj.as_expr()),reciprocal_pullback_gcd=str(common.as_expr()),only_common_parameter_zero=True,zero_multiplicity=zero_mult))
    print('PASS',p,'gcd',common.as_expr(),flush=True)
Path(__file__).with_name('CHARACTERISTIC_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
