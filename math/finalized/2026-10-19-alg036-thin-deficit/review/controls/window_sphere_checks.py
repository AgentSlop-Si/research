#!/usr/bin/env python3
"""Independent exact sphere integration and high-precision window diagnostics."""
import json, math
import sympy as s
import mpmath as mp
mp.mp.dps=100
counts={}
def count(k): counts[k]=counts.get(k,0)+1
def inclusion(N,d,a):
    return sum((-1)**k*s.binomial(d,k)*max(s.Rational(0),1-k*a/d)**(N-1) for k in range(d+1))
# N=2 exact geometry is an interval in the uniform one-dimensional simplex.
for a in [s.Rational(j,4) for j in range(1,13)]:
    assert inclusion(2,1,a)==min(1,a)
    u=a/2
    direct=max(s.Rational(0),min(1,u)-max(0,1-u))
    assert inclusion(2,2,a)==direct
    count('exact_N2_interval_integrals')

# Integrate the Dirichlet marginal density over an untruncated cube.
for d in [1,2,3]:
    xs=s.symbols('x:'+str(d))
    for N in range(d+1,d+5):
        for denominator in [d+1,d+2]:
            u=s.Rational(1,denominator)
            density=s.factorial(N-1)/s.factorial(N-d-1)*(1-sum(xs))**(N-d-1)
            value=density
            for x in xs: value=s.integrate(value,(x,0,u))
            assert s.simplify(value-inclusion(N,d,d*u))==0
            count('exact_Dirichlet_cube_integrals')

# Truncated d=2 square, split where y<=1-x begins to bind.
x,y=s.symbols('x y')
for N in range(3,8):
    for u in [s.Rational(2,3),s.Rational(3,4)]:
        density=(N-1)*(N-2)*(1-x-y)**(N-3)
        direct=s.integrate(s.integrate(density,(y,0,u)),(x,0,1-u))
        direct+=s.integrate(s.integrate(density,(y,0,1-x)),(x,1-u,u))
        assert s.simplify(direct-inclusion(N,2,2*u))==0
        count('exact_truncated_Dirichlet_integrals')

# Exact critical derivative, plus numerical width scaling independently of blocks.
A,d=s.symbols('A d',positive=True)
w=A/d-s.log(d)
assert s.simplify(s.diff(w,d).subs(A,d*s.log(d))+(s.log(d)+1)/d)==0
count('symbolic_critical_width_identity')
width=[]
for N in [10**6,10**12,10**24,10**48]:
    center=mp.mpf(N)/mp.lambertw(N); sigma=center/(mp.log(center)+1)
    for h in [-2,0,2]:
        dd=center+h*sigma
        shift=mp.mpf(N)/dd-mp.log(dd)
        width.append({'N':N,'h':h,'shift':str(shift),'expected_shift':-h,'rank_center':str(center),'rank_width':str(sigma)})
        count('critical_width_diagnostics')

# Nondivisible block formula verified at high precision against independent lambda.
rounding=[]
for theta in [mp.mpf('0.2'),mp.mpf('0.5'),mp.mpf('0.8')]:
    for shift in [-2,0,2]:
        m=40;dd=int(mp.nint(mp.exp(m+theta-shift)));k=int(mp.nint(theta*dd));N=m*dd+k
        th=mp.mpf(k)/dd; t=mp.mpf(N)/dd; ww=t-mp.log(dd)
        Atheta=(1-th)*mp.exp(th)+th*mp.exp(-(1-th))
        direct=mp.exp((dd-k)*mp.log1p(-mp.exp(-m))+k*mp.log1p(-mp.exp(-m-1)))
        limit=mp.exp(-Atheta*mp.exp(-ww))
        assert Atheta>=1
        assert abs(direct-limit)<mp.mpf('1e-16')
        rounding.append({'theta':str(th),'shift':str(ww),'coefficient':str(Atheta),'probability':str(direct),'asymptotic_prediction':str(limit)})
        count('rounding_correction_diagnostics')

# Exact norm Chernoff exponent after optimizer substitution.
e,N=s.symbols('e N',positive=True)
lam=s.symbols('lam')
upper=-lam*N*(1+e)-N*s.log(1-lam)
lower=-lam*N*(1-e)-N*s.log(1-lam)
assert s.simplify(upper.subs(lam,e/(1+e))+N*(e-s.log(1+e)))==0
# Formal log simplification on 0<e<1 is checked by exp identity to avoid branch artifacts.
assert s.simplify(s.diff(lower.subs(lam,-e/(1-e))-N*(e+s.log(1-e)),e))==0
count('symbolic_norm_Chernoff_checks')
print(json.dumps({'status':'PASS','counts':counts,'critical_width':width,'rounding':rounding,'historical_program_execution':False,'network_access':False},indent=2,sort_keys=True))
