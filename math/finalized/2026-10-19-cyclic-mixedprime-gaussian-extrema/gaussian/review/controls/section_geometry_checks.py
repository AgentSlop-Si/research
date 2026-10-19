#!/usr/bin/env python3
"""Original exact controls for the new block counterexamples and simplex reduction."""
import json, math, platform
from pathlib import Path
import sympy as s
import mpmath as mp
mp.mp.dps=80
OUT=Path(__file__).resolve().parent
counts={}

# Parameterized plane volume and covariance: direct exact algebra on the Gram matrix.
al,be=s.symbols('alpha beta', nonnegative=True)
A=s.Matrix([[1,0],[0,1],[-al,-be]])
H=A.T*A
assert s.expand(H.det())==1+al**2+be**2
u=s.Matrix([al,be,1])/s.sqrt(1+al**2+be**2)
assert s.simplify(A*H.inv()*A.T-(s.eye(3)-u*u.T))==s.zeros(3)
# The real four-volume factor is sqrt(det(realification(H)))=det(H).
assert s.factor(s.diag(H,H).det()-H.det()**2)==0
counts['symbolic_gram_projector_identities']=3

simplex=[]
for den in range(1,10):
    for n1 in range(den+1):
        for n2 in range(den-n1+1):
            n3=den-n1-n2
            if n3<max(n1,n2) or n3==0: continue
            q1,q2,q3=[s.Rational(k,den) for k in [n1,n2,n3]]
            aa=s.sqrt(q1/q3); bb=s.sqrt(q2/q3)
            T=A.subs({al:aa,be:bb}); G=T.T*T
            assert s.simplify(G.det()-1/q3)==0
            v=s.Matrix([s.sqrt(q1),s.sqrt(q2),s.sqrt(q3)])
            Q=s.eye(3)-v*v.T
            assert s.simplify(T*G.inv()*T.T-Q)==s.zeros(3)
            assert Q*Q==Q and s.trace(Q)==2
            simplex.append([str(q1),str(q2),str(q3)])
counts['rational_simplex_planes']=len(simplex)

# Direct lens integration, distinct from any candidate checker.
t=s.symbols('t', nonnegative=True)
lens=2*s.acos(t/2)-t*s.sqrt(4-t*t)/2
integral=s.integrate(t*lens,(t,0,1))
assert s.simplify(integral-(s.pi/2-3*s.sqrt(3)/8))==0
C=3-9*s.sqrt(3)/(4*s.pi)
assert s.simplify(6*integral/s.pi-C)==0
# pi<22/7 is classical; the second rational/radical comparison is exact.
assert s.Rational(22,7)**2 < (s.Rational(15,8)*s.sqrt(3))**2
assert s.Rational(97,50)>s.Rational(9,5)
counts['exact_small_radius_relations']=4

# Independently evaluate axis-boundary simplex integral in polar squared radii.
x,y,a=s.symbols('x y a', positive=True)
axis=s.integrate(s.exp(-x),(x,0,a))*s.integrate(s.exp(-y),(y,0,a))
block=2*s.integrate(s.exp(-x),(x,0,a))*s.integrate(s.exp(-2*y),(y,0,a))
assert s.simplify(axis-(1-s.exp(-a))**2)==0
assert s.simplify(block-(1-s.exp(-a))*(1-s.exp(-2*a)))==0
counts['boundary_simplex_integral_identities']=2

# General sufficient threshold, compared in logarithms to avoid 1-epsilon cancellation.
threshold=[]
for N in range(3,31):
    for d in range(2,N):
        if N%d==0: continue
        m=N//d; theta=mp.mpf(N)/d-m
        radius2=mp.log(N)/theta+mp.mpf(1)
        logratio=mp.log(N)-(mp.mpf(N)/d-m)*radius2
        assert logratio<0 and abs(logratio+theta)<mp.mpf('1e-70')
        threshold.append({'N':N,'d':d,'theta':str(theta),'radius_squared':str(radius2),'log_failure_ratio':str(logratio)})
counts['nondivisible_large_radius_thresholds']=len(threshold)

# Enumerate all full-support block-size partitions for moderate dimensions.
def partitions(n,k,lo=1):
    if k==1:
        if n>=lo: yield (n,)
    else:
        for t in range(lo,n//k+1):
            for rest in partitions(n-t,k-1,t): yield (t,)+rest
partition_checks=0
for N in range(1,16):
    for d in range(1,N+1):
        m,k=divmod(N,d); optimal=tuple([m]*(d-k)+[m+1]*k)
        for a in [mp.mpf('.1'),mp.mpf(1),mp.mpf(4)]:
            def prob(ns): return mp.fprod(1-mp.exp(-a*n) for n in ns)
            bound=prob(optimal)
            for sizes in partitions(N,d):
                value=prob(sizes)
                if sizes==optimal: assert value==bound
                else: assert value<bound
                partition_checks+=1
counts['balanced_block_partition_controls']=partition_checks

result={'status':'PASS','counts':counts,'small_section':{'radial_integral':str(integral),'normalized_coefficient':str(C),'coefficient_decimal':str(s.N(C,25)),'test_radius_squared':'1/100','equal_plane_upper_coefficient':'<9/5','blocks_lower_coefficient':'97/50'},'simplex_cases':simplex,'large_radius_cases':threshold,'scope':'Proof diagnostics only; no global numerical optimization or critical-window gap claimed.'}
(OUT/'SECTION_GEOMETRY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','counts':counts,'small_section':result['small_section']},indent=2))
