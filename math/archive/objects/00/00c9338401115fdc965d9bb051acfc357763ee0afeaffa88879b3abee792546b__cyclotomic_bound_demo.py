"""Toy exact cyclotomic coefficient-bound demonstration.

For a fixed root of unity zeta_D, #130-style prepared coefficients live in a
cyclotomic field.  This script demonstrates an effective crude bound:
reduce a rational function to a polynomial representative modulo Phi_D and
bound its chosen complex embedding by the l1 norm of rational coefficients.

This is an effectivity demo, not extraction of the full #130 coefficient list.
"""
from fractions import Fraction
import json
from pathlib import Path
import sympy as sp

z=sp.symbols('z')


def rational_l1_bound(poly_expr):
    p=sp.Poly(sp.expand(poly_expr),z,domain=sp.QQ)
    return sum(abs(sp.Rational(c)) for c in p.all_coeffs())


def reduce_fraction_mod_cyclotomic(num,den,D):
    phi=sp.Poly(sp.cyclotomic_poly(D,z),z,domain=sp.QQ)
    n=sp.Poly(num,z,domain=sp.QQ).rem(phi)
    d=sp.Poly(den,z,domain=sp.QQ).rem(phi)
    inv=sp.invert(d,phi)
    rep=(n*inv).rem(phi)
    return phi,rep


def main():
    cases=[
        (8, 1+z, 1-z),
        (16, 1+2*z+z**3, 1-z**2),
        (32, 3-z+2*z**5, 2+z+z**2),
    ]
    rows=[]
    for D,num,den in cases:
        phi,rep=reduce_fraction_mod_cyclotomic(num,den,D)
        bound=rational_l1_bound(rep.as_expr())
        zv=sp.exp(2*sp.pi*sp.I/D)
        exact=complex(sp.N(rep.as_expr().subs(z,zv),60))
        rows.append({
            'D':D,
            'phi':str(phi.as_expr()),
            'representative':str(rep.as_expr()),
            'l1_bound':str(bound),
            'numeric_abs':abs(exact),
            'bound_valid':abs(exact) <= float(bound)+1e-12,
        })
    p=Path(__file__).with_name('cyclotomic_bound_demo.json')
    p.write_text(json.dumps(rows,indent=2))
    for r in rows: print(r)
    print('wrote',p)

if __name__=='__main__': main()
