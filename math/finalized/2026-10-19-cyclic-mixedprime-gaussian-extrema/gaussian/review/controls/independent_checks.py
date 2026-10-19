#!/usr/bin/env python3
"""Fresh controls for the ALG036 equality/gap review. No historical imports or programs."""
import hashlib, json, math, platform
from fractions import Fraction
from pathlib import Path
import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import quad
from scipy.special import i0e
import sympy as s

OUT = Path(__file__).resolve().parent
mp.mp.dps = 70
counts = {}

# Exact scalar derivative and boundary-continuation formulas.
p,a=s.symbols('p a', positive=True)
h=p*s.log(1-s.exp(-a/p))
claimed=-(a/p)**2*s.exp(a/p)/(p*(s.exp(a/p)-1)**2)
assert s.simplify(s.diff(h,p,2)-claimed)==0
assert s.limit(h,p,0,dir='+')==0
counts['symbolic_hessian_and_zero_limit']=2

# Exact nondivisible counterexample, independently represented as a rational projector.
P=s.eye(3)-s.ones(3)/3
assert P==P.conjugate().T and P*P==P and P.rank()==2
assert all(P[j,j]==s.Rational(2,3) for j in range(3))
realP=s.diag(P,P)
J=s.zeros(6)
J[:3,3:]=-s.eye(3); J[3:,:3]=s.eye(3)
assert realP*J==J*realP
union_lower=Fraction(61,64)
rounded=Fraction(15,16)*Fraction(255,256)
rank_upper=Fraction(63,64)**2
assert union_lower-rounded==Fraction(79,4096)
assert rank_upper-union_lower==Fraction(65,4096)
assert rounded<union_lower<rank_upper
counts['rational_counterexample_identities']=8

# Exact phased block matrices, including absent coordinates.
block_cases=[]
for sizes,zeros in [([1],0),([3],2),([2,2],0),([1,2],0),([1,3,2],2),([2,2,2],1),([4,4],0)]:
    N=sum(sizes)+zeros; d=len(sizes); V=s.zeros(N,d); offset=0
    for ell,n in enumerate(sizes):
        for k in range(n): V[offset+k,ell]=s.I**k/s.sqrt(n)
        offset+=n
    Q=s.simplify(V*V.conjugate().T)
    assert s.simplify(V.conjugate().T*V)==s.eye(d)
    assert Q*Q==Q and Q.conjugate().T==Q and s.trace(Q)==d
    diag=[Q[j,j] for j in range(N)]
    assert diag.count(0)==zeros
    positive=[j for j in range(N) if diag[j]>0]
    # Row-space projections are each equal or orthogonal, exact complex arithmetic.
    Es=[]
    for j in positive:
        v=V[j,:]
        E=s.simplify(v.conjugate().T*v/diag[j]); Es.append(E)
        assert E*E==E and s.trace(E)==1
    assert all(E==F or E*F==s.zeros(d) for E in Es for F in Es)
    assert sum((diag[j]*Es[k] for k,j in enumerate(positive)), s.zeros(d))==s.eye(d)
    for radius2 in [mp.mpf('0.125'),mp.mpf(1),mp.log(16),mp.mpf(6)]:
        success=mp.fprod([1-mp.exp(-n*radius2) for n in sizes])
        leverage=mp.exp(sum(mp.mpf(str(q))*mp.log(1-mp.exp(-radius2/mp.mpf(str(q)))) for q in diag if q))
        envelope=(1-mp.exp(-N*radius2/d))**d
        assert mp.almosteq(success,leverage,rel_eps=mp.mpf('1e-65'))
        exact_rank_equal=(zeros==0 and len(set(sizes))==1)
        if exact_rank_equal: assert mp.almosteq(success,envelope,rel_eps=mp.mpf('1e-65'))
        else: assert success<envelope
    block_cases.append({'sizes':sizes,'zero_coordinates':zeros,'rank_bound_equality':zeros==0 and len(set(sizes))==1})
counts['phased_block_cases']=len(block_cases)
counts['phased_block_scalar_checks']=4*len(block_cases)

# Exhaustive small rank-one simplex data, independently evaluating the true probability.
def compositions(total,k,prefix=()):
    if k==1:
        yield prefix+(total,)
    else:
        for t in range(1,total-k+2): yield from compositions(total-t,k-1,prefix+(t,))
rankone=0
for denom in range(1,13):
    for support in range(1,min(denom,5)+1):
        for ns in compositions(denom,support):
            ps=[mp.mpf(n)/denom for n in ns]
            for radius2 in [mp.mpf('0.2'),mp.mpf(1),mp.mpf(3)]:
                actual=1-mp.exp(-radius2/max(ps))
                leverage=mp.exp(sum(q*mp.log(1-mp.exp(-radius2/q)) for q in ps))
                if len(set(ns))==1: assert mp.almosteq(actual,leverage,rel_eps=mp.mpf('1e-65'))
                else: assert actual<leverage
                rankone+=1
counts['rank_one_probability_controls']=rankone

# Direct polar quadrature for translated disks. Stable e^-x I0(x) avoids overflow.
disk_rows=[]
for variance in [.1,.5,1.]:
    for radius in [.2,1.,2.]:
        centered=-math.expm1(-radius*radius/variance)
        for shift in [.1,.5,2.]:
            fn=lambda rho: 2*rho/variance*math.exp(-(rho-shift)**2/variance)*i0e(2*rho*shift/variance)
            shifted,err=quad(fn,0,radius,epsabs=1e-13,epsrel=1e-13)
            assert shifted < centered
            assert shifted<=math.exp(-(max(shift-radius,0))**2) + 1e-12
            disk_rows.append({'variance':variance,'radius':radius,'shift':shift,'centered':centered,'shifted':shifted,'error_bound':err})
counts['translated_disk_quadratures']=len(disk_rows)

# Common-coupling boundary test. This is a direct exact probability counterexample
# to continuity in translations at a zero-leverage coordinate, not to USC.
r=1
boundary_mass=1-math.exp(-r*r)
assert boundary_mass>0
usc_boundary={'P_diagonal':[1,0],'b_limit':[0,1],'r':1,'limit_value':boundary_mass,'approach_from_b2_above_r':0.0,'conclusion':'upper semicontinuous; not continuous'}

# Compactness truncation choices, using explicit block lower bounds.
truncations=[]
for N,d,radius in [(3,2,.2),(3,2,math.sqrt(math.log(16))),(5,2,1.),(7,3,.6),(4,4,1.)]:
    m,k=divmod(N,d)
    L=(1-math.exp(-m*radius**2))**(d-k)*(1-math.exp(-(m+1)*radius**2))**k
    R=radius+math.sqrt(math.log(2/L))
    tail=math.exp(-(R-radius)**2)
    assert abs(tail-L/2)<=max(1e-15,L*1e-13)
    truncations.append({'N':N,'d':d,'r':radius,'explicit_positive_lower':L,'translation_cutoff':R,'outside_upper':tail})
counts['compactness_cutoffs']=len(truncations)

result={'status':'PASS','versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':s.__version__,'mpmath':mp.__version__},'counts':counts,'counterexample':{'P':str(P),'r_squared':'log(16)','union_lower':str(union_lower),'rounded_blocks':str(rounded),'rank_upper':str(rank_upper),'certified_improvement':str(union_lower-rounded)},'phased_blocks':block_cases,'translated_disks':disk_rows,'usc_boundary':usc_boundary,'compactness_truncations':truncations,'scope':'Finite controls support the independently written all-dimension proof. No simulation or finite test establishes the theorem.'}
(OUT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','counts':counts,'counterexample':result['counterexample']},indent=2))
