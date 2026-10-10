#!/usr/bin/env python3
"""Boundary controls. Imports only this reviewer's independently authored module."""
import json
from pathlib import Path
import sympy as S
from independent_exact_review import CyclotomicRing, content
OUT=Path(__file__).resolve().parent
q,y,z=S.symbols('q y z')

def expr(a,var=q):return sum(int(c)*var**i for i,c in enumerate(a))
def vec(a,p=None):
    a=S.Poly(a,q,modulus=p) if p else S.Poly(a,q)
    return [int(a.nth(i))%(p or (10**10000)) if p else int(a.nth(i)) for i in range(a.degree()+1)]
def data(s):return json.loads((OUT/f'INDEPENDENT_EXACT_S{s}.json').read_text())['independently_reconstructed']

def convolution(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,w in enumerate(b):c[i+j]+=x*w
    return c

C={}
# Standard symbolic resultant/discriminant cross-check over Z[q], followed by
# cyclotomic reduction, independent of the multiplication-matrix algorithm.
for s in [7,11]:
    d=data(s);R=CyclotomicRing(s);U=sum(expr(c)*z**i for i,c in enumerate(d['U']))
    disc=S.Poly(S.discriminant(U,z),q)
    res=S.Poly(S.resultant(z**s+1,U,z),q)
    dv=R.reduced([int(disc.nth(i)) for i in range(disc.degree()+1)])
    rv=R.reduced([int(res.nth(i)) for i in range(res.degree()+1)])
    assert list(dv)==d['disc_U'] and list(rv)==d['res_F_U']
    C[f's{s}_symbolic_resultants']={'disc_matches':True,'res_matches':True}
# Show why reduced coordinates are mandatory: multiplication can introduce
# extra rational content when the result is reduced in the cyclotomic basis.
raw={}
for s in [3,7,11,15,19]:
    d=data(s);R=CyclotomicRing(s)
    pre=convolution(convolution(d['Gamma'],R.conj(d['Gamma'])),d['delta'])
    raw[str(s)]={'unreduced_product_content':content(pre),'reduced_coordinate_content':content(R.reduced(pre))}
assert raw['19']['unreduced_product_content']==19**10
assert raw['19']['reduced_coordinate_content']==19**11
C['reduction_control']=raw
# Norm-versus-content adverse component, s=7,p=13.
s=7;p=13;d=data(s);R=CyclotomicRing(s)
phi=S.Poly(expr(R.phi),q,modulus=p)
delta=S.Poly(expr(d['delta']),q,modulus=p)
pair=S.Poly(expr(d['Gamma_pair']),q,modulus=p)
aug=S.Poly(expr(d['augmented']),q,modulus=p)
factors=S.factor_list(phi)[1]
assert len(factors)==3
assert S.gcd(phi,pair).degree()==0
bad=S.gcd(phi,delta).monic();assert bad==S.Poly(q*q+6*q+1,q,modulus=13)
assert S.gcd(phi,aug).monic()==bad
norm=int(S.resultant(expr(R.phi),expr(d['delta']),q));assert norm==1183
H0=S.Integer(1);H1=y
for j in range(1,6):H0,H1=H1,S.expand(y*H1-j*H0)
J=S.Poly(y*H1-2*S.diff(H1,y),y,modulus=13)
assert J.nth(0)==J.nth(1)==J.nth(2)==0 and J.nth(3)!=0
Jgcd=S.gcd(J,J.diff()).monic();assert Jgcd==S.Poly(y**2,y,modulus=13)
C['s7_p13_exception']={'irreducible_factors_ascending':[vec(f,p) for f,m in factors],
 'bad_delta_factor_ascending':vec(bad,p),'pair_coprime_to_phi':True,
 'norm_delta':norm,'delta_content':content(d['delta']),'augmented_content':content(d['augmented']),
 'J_tau2_ascending':[int(J.nth(i))%13 for i in range(J.degree()+1)],
 'J_derivative_gcd':'y^2','zero_multiplicity':3}
# Unramified component selection controls, not a census or theorem substitute.
rows=[]
for s in [15,19]:
    R=CyclotomicRing(s);d=data(s)
    for p in [5,13,17,29]:
        phi=S.Poly(expr(R.phi),q,modulus=p)
        aug=S.Poly(expr(d['augmented']),q,modulus=p)
        sf=S.gcd(phi,phi.diff()).degree()==0
        remainder=aug.rem(phi)
        covered=s%p!=0
        if covered:assert sf and not remainder.is_zero
        else:assert not sf and remainder.is_zero
        rows.append({'s':s,'p':p,'p_not_dividing_s':covered,
         'phi_squarefree':sf,'augmented_nonzero_in_quotient':not remainder.is_zero,
         'good_irreducible_factors':sum(1 for f,m in S.factor_list(phi)[1] if not aug.rem(f).is_zero),
         'factor_count':len(S.factor_list(phi)[1])})
C['residue_components']=rows
# The repeated-prime boundary is structural: Phi_15 mod 5=Phi_3^4.
assert S.Poly(expr(CyclotomicRing(15).phi),q,modulus=5)==S.Poly((q*q+q+1)**4,q,modulus=5)
C['repeated_prime_boundary']={'s':15,'p':5,'Phi15_mod5':'Phi3^4',
 'augmented_remainder_zero':True,'theorem_does_not_cover_d75':True}
(OUT/'INDEPENDENT_BOUNDARY_CONTROLS.json').write_text(json.dumps(C,indent=2)+'\n')
print(json.dumps(C,indent=2))
