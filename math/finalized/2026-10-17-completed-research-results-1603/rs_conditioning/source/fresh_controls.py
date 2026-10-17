#!/usr/bin/env python3
"""Fresh controls for the compact-pencil conditioning obstruction.
No historical executable or author script is imported or run.
Exact arithmetic verifies identities; numerical spectra are sanity checks only.
"""
import cmath, hashlib, json, math
from fractions import Fraction
from pathlib import Path
import numpy as np
import sympy as sp

OUT = Path(__file__).resolve().parent
X = sp.Symbol('q')

def shift(v, k):
    n = len(v); k %= n
    return v[-k:] + v[:-k] if k else v[:]
def add(a,b): return [x+y for x,y in zip(a,b)]
def scale(a,c): return [c*x for x in a]
def mul(a,b):
    n=len(a); ans=[0]*n
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y: ans[(i+j)%n]+=x*y
    return ans

def zero_mod_cyclotomic(a,n):
    p=sp.Poly.from_list(a[::-1],X,domain=sp.QQ)
    return p.rem(sp.Poly(sp.cyclotomic_poly(n,X),X)).is_zero

def p_from_definition(n,deg):
    one=[1]+[0]*(n-1); zero=[0]*n
    # R_deg(z)=product_{k=0}^{deg-1}(z-q^k), in Q[q]/(q^n-1).
    r=[one]
    for k in range(deg):
        s=[zero[:] for _ in range(len(r)+1)]
        for j,coef in enumerate(r):
            s[j]=add(s[j],scale(shift(coef,k),-1))
            s[j+1]=add(s[j+1],coef)
        r=s
    tri=lambda j:j*(j-1)//2
    return [shift(v,tri(deg)-tri(j)) for j,v in enumerate(r)]

exact=[]; negative=[]; grid_cases=0
for n in range(4,130,2):
    h=n//2; m=h+1
    p=p_from_definition(n,h)
    one=[1]+[0]*(n-1); qm3=shift(one,-3)
    # Monic B_t has top coefficients b_(m-1)=P_h[h-1],
    # b_(m-2)=P_h[h-2]+t. The formal t terms cancel identically below.
    trace2_at_zero=add(mul(p[h-1],p[h-1]),scale(p[h-2],-2))
    residual=add(add(trace2_at_zero,scale(shift(trace2_at_zero,1),-1)),scale(qm3,4))
    assert zero_mod_cyclotomic(residual,n)
    # The top coefficient formula is separately checked after clearing (1-q).
    e1=scale(p[h-1],-1)
    e1_residual=add(add(e1,scale(shift(e1,1),-1)),scale(shift(one,-1),2))
    assert zero_mod_cyclotomic(e1_residual,n)
    # e2=2*q^-3/(1-q)^2.
    e2_residual=add(add(add(p[h-2],scale(shift(p[h-2],1),-2)),shift(p[h-2],2)),scale(qm3,-2))
    assert zero_mod_cyclotomic(e2_residual,n)
    # Every accepted-grid t has 0<t<=1; algebra in t is formal.
    vals=[Fraction(k,2*n) for k in range(1,2*n+1)]
    assert len(set(vals))==2*n and all(0<t<=1 for t in vals)
    grid_cases += len(vals)
    # Wrong phase q^-2 is not accidentally accepted.
    wrong=add(add(trace2_at_zero,scale(shift(trace2_at_zero,1),-1)),scale(shift(one,-2),4))
    assert not zero_mod_cyclotomic(wrong,n)
    # Omitting -2t leaves -2t(1-q), which is nonzero, tested at t=1.
    omitted=add(scale(one,-2),scale(shift(one,1),2))
    assert not zero_mod_cyclotomic(omitted,n)
    exact.append({'N':n,'degree':m,'root_power_sum_identity':'PASS','e1_identity':'PASS','e2_identity':'PASS','grid_parameters':len(vals)})
    negative.append({'N':n,'wrong_phase_rejected':True,'omitted_parameter_term_rejected':True})

# The uniform N>=44 bound uses pi<22/7, so this is entirely rational.
constant_checks=[]
for n in range(44,10002,2):
    left=Fraction(7*n,11)-2
    right=Fraction(9,8)*(Fraction(n,2)+1)
    assert left>=right
    constant_checks.append(n)
assert Fraction(13*44,176)-Fraction(25,8)==Fraction(1,8)
# Show the selected rational comparison does not certify N=42.
assert Fraction(7*42,11)-2 < Fraction(9,8)*(Fraction(42,2)+1)

numerical=[]
for n in [4,6,8,16,24,32,44,64,128]:
    h=n//2; m=h+1; q=cmath.exp(2j*math.pi/n)
    for label,t in [('zero',0),('first_grid',1/(2*n)),('unit',1),('minus_unit',-1),('imaginary_unit',1j),('outside_disk',2)]:
        # Three-term matrix is used only as a separate numeric root proposal.
        a=[q**(k-1)*((1+q)*q**k-1) for k in range(h)]
        b=[q**(3*k-3)*(q**k-1) for k in range(1,h)]+[-t]
        J=np.diag(a+[0])+np.diag(np.ones(h),1)+np.diag(b,-1)
        roots=np.linalg.eigvals(J)
        actual=sum(roots**2)
        expected=-4*q**-3/(1-q)-2*t
        rel=abs(actual-expected)/max(1,abs(expected))
        assert rel<1e-10
        rho=float(max(abs(roots)))
        bound=((max(0,2/math.sin(math.pi/n)-2*abs(t))/m))**0.5
        assert rho+1e-10>=bound
        # Double precision condition numbers are reported only at modest sizes.
        cond=None
        if n<=24:
            V=np.vander(roots,m,increasing=True).T
            cond=float(np.linalg.cond(V))
            lower=rho**h/math.sqrt(m)
            assert cond+1e-7>=lower
        numerical.append({'N':n,'parameter':label,'abs_t':float(abs(t)),'trace2_relative_residual':float(rel),'max_root_modulus':rho,'radius_lower_bound':bound,'kappa2_double_sanity_only':cond})

result={'status':'PASS','exact_identity_cases':len(exact),'accepted_grid_members_domain_checked':grid_cases,'exact_cases':exact,'negative_controls':negative,'rational_uniform_threshold_checks':{'first_N':44,'last_N':10000,'count':len(constant_checks),'N44_rational_margin':'1/8','N42_does_not_meet_this_sufficient_comparison':True},'numerical_sanity_cases':numerical,'limits':['The all-N statement is proved in PROOF.md; finite checks do not extrapolate it.','Numerical eigensolves and condition numbers are sanity checks, not certified root or condition enclosures.','No historical program was executed.','These controls do not test a production bank evaluator or certify practical preparation.']}
(OUT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'exact_identity_cases':len(exact),'grid_members':grid_cases,'numerical_cases':len(numerical),'rational_threshold_cases':len(constant_checks)},indent=2))
