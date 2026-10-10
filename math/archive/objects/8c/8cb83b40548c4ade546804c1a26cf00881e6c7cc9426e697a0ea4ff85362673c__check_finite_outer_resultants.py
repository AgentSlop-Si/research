"""Independent compact exact resultant exclusion for finite unequal outer ratios.

Inputs are coefficient data, already independently reconstructed by
check_six_outer_minors.py, and a proposed cubic common divisor. Every
divisibility and reduction used here is checked, not trusted.
"""
from pathlib import Path
import json, hashlib
import sympy as s

HERE=Path(__file__).resolve().parent
a,c=s.symbols('a c')
Q=s.QQ_I
data=json.loads((HERE/'N4_OUTER_RANK_MINORS.json').read_text())
proposal=json.loads((HERE/'EXACT_RESULTANT_DIVISIBILITY.json').read_text())
det=lambda v:(15*v+16)*(10625*v**3+30500*v**2+29920*v+9984)
P=[]
for entry in data['minors']:
    f=s.Poly.from_dict({tuple(mon):s.Rational(re)+s.I*s.Rational(im)for mon,re,im in entry['terms']},(a,c),domain=Q)
    if entry['i']==3:
        f=f.exquo(s.Poly(det(a)*det(c),a,c,domain=Q))
    P.append(f)
F=P[2]
assert (F.degree(a),F.degree(c))==(8,8)
q=s.Poly(10625*a**3+30500*a**2+29920*a+9984,a,domain=Q).monic()
h=s.Poly(a+s.Rational(16,15),a,domain=Q)
a0=-s.Rational(16,15)
assert q.is_irreducible and q.gcd(q.diff()).degree()==0 and q.eval(a0)!=0
prime,ii=29,12
assert (ii*ii+1)%prime==0

def reduce_coeff(z):
    re,im=s.expand(z).as_real_imag()
    re,im=s.Rational(re),s.Rational(im)
    assert int(re.q)%prime and int(im.q)%prime
    return (int(re.p)*pow(int(re.q),-1,prime)+ii*int(im.p)*pow(int(im.q),-1,prime))%prime
def modpoly(poly,gens):
    return s.Poly.from_dict({mon:reduce_coeff(co)for mon,co in poly.terms()},gens,modulus=prime)

records=[];modular_quotients=[]
for trial,weights in enumerate([[1]*5,[1,2,3,4,5]]):
    G=sum((w*P[j]for w,j in zip(weights,[0,1,3,4,5])),s.Poly(0,a,c,domain=Q))
    assert (G.degree(a),G.degree(c))==(12,12)
    f0=s.Poly(F.as_expr().subs(a,a0),c,domain=Q)
    g0=s.Poly(G.as_expr().subs(a,a0),c,domain=Q)
    assert (f0.degree(),g0.degree())==(7,10)
    common=f0.gcd(g0)
    assert common.degree()==3
    # The generic Sylvester matrix acts on deg(u)<12, deg(v)<8.
    # These four independent vectors are its entire specialized kernel.
    u0=g0.exquo(common);v0=-f0.exquo(common)
    f1=s.Poly(F.diff(a).as_expr().subs(a,a0),c,domain=Q)
    g1=s.Poly(G.diff(a).as_expr().subs(a,a0),c,domain=Q)
    assert g1.degree()<=11
    kernel_checks=[]
    for j in range(4):
        u=u0*s.Poly(c**j,c,domain=Q);v=v0*s.Poly(c**j,c,domain=Q)
        assert u.degree()<12 and v.degree()<8
        assert (f0*u+g0*v).is_zero
        assert (f1*u+g1*v).nth(19)==0
        kernel_checks.append({'power':j,'u_degree':u.degree(),'v_degree':v.degree(),'derivative_c19_zero':True})
    # The nonzero left functional "coefficient of c^19" annihilates S0
    # and S1 on its full right kernel. Hence corank4 has order at least5.

    prop=proposal['resultants'][trial]['factors'][1]
    assert prop['factor']=='cubic'
    divisor=s.Poly(s.sympify(prop['finite_gcd_monic']),c,a,domain=Q)
    assert divisor.degree(c)==3
    coeff3=s.Poly(divisor.as_expr(),c,domain=Q.poly_ring(a)).nth(3)
    assert coeff3==1
    # Leading monomials c^3 and a^3 are coprime. Exact division by this
    # monic triangular pair checks divisibility in Q(i)[a]/(q)[c].
    cubic_checks=[]
    for name,poly in [('F',F),('G',G)]:
        _,rem=s.reduced(poly.as_expr(),[divisor.as_expr(),q.as_expr()],c,a,domain=Q)
        assert rem==0
        cubic_checks.append(name)

    Fp=modpoly(F,(a,c));Gp=modpoly(G,(a,c))
    ring=s.GF(prime).poly_ring(a)
    resultant=s.Poly(s.Poly(Fp.as_expr(),c,domain=ring).resultant(s.Poly(Gp.as_expr(),c,domain=ring)),a,modulus=prime)
    assert resultant.degree()==192
    exact_factor=h**5*q**3
    factor_mod=modpoly(exact_factor,(a,))
    reduced=resultant.exquo(factor_mod)
    assert reduced.degree()==178
    modular_quotients.append(reduced)
    records.append({'weights':weights,'F_bidegree':[8,8],'G_bidegree':[12,12],
        'charzero_resultant_degree_upper_bound':192,
        'linear_specialization_degrees':[7,10],'linear_gcd':str(common.as_expr()),
        'linear_sylvester_corank':4,'linear_order_at_least':5,'kernel_checks':kernel_checks,
        'cubic_irreducible':True,'cubic_common_monic_divisor':str(divisor.as_expr()),
        'cubic_exact_divisions_checked':cubic_checks,'cubic_order_at_least':3,
        'modular_resultant_degree':192,'modular_resultant_coefficients':[int(z)%prime for z in resultant.all_coeffs()],
        'modular_quotient_degree':178,'modular_quotient_coefficients':[int(z)%prime for z in reduced.all_coeffs()]})
    print('Independent exact divisibility and modular resultant verified for',weights,flush=True)

u,v,g=s.gcdex(modular_quotients[0],modular_quotients[1])
assert g.degree()==0
u=u.mul_ground(s.invert(g.LC(),prime));v=v.mul_ground(s.invert(g.LC(),prime))
assert (u*modular_quotients[0]+v*modular_quotients[1]).is_one
out={'verified':True,'field':'Q(i)','good_reduction':{'prime':prime,'image_i':ii,'every_coefficient_denominator_checked':True},
    'input_minors_sha256':hashlib.sha256((HERE/'N4_OUTER_RANK_MINORS.json').read_bytes()).hexdigest(),
    'exact_forced_resultant_factor':str((h**5*q**3).as_expr()),'resultants':records,
    'modular_quotients_coprime':True,'bezout_U':[int(z)%prime for z in u.all_coeffs()],
    'bezout_V':[int(z)%prime for z in v.all_coeffs()],
    'conclusion':'No regular finite unequal-outer point for the fixed-pole N4 family; all projective middle ratios are covered on the regular support chart. Earlier exact zero-support and infinite-outer checks complete the full projective family.',
    'limits':'This is a degree-preserving resultant lift after exact characteristic-zero factor divisibility, not finite-field point enumeration.'}
(HERE/'FINITE_OUTER_RESULTANT_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n')
print('FULL FINITE UNEQUAL-OUTER REGULAR EXCLUSION VERIFIED',flush=True)
