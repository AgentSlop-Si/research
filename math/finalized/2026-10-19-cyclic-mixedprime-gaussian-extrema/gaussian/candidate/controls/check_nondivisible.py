#!/usr/bin/env python3
"""Fresh finite controls for the accompanying proof; not an optimizer certificate.
No network calls and no imports or execution of inherited/historical programs.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import math
import sympy as s

HERE = Path(__file__).resolve().parent
counts = {}

# Exact derivative in the inherited Jensen step, checked independently.
p, a = s.symbols('p a', positive=True)
h = p * s.log(1-s.exp(-a/p))
expected = -a*a*s.exp(a/p)/(p**3*(s.exp(a/p)-1)**2)
assert s.simplify(s.diff(h,p,2)-expected) == 0
counts['symbolic_concavity_identity'] = 1

# Exact projector control, including non-block equal-diagonal geometry.
Pe = s.eye(3) - s.ones(3)/3
Pb = s.Matrix([[s.Rational(1,2),s.Rational(1,2),0],
               [s.Rational(1,2),s.Rational(1,2),0],[0,0,1]])
for P in (Pe,Pb):
    assert P == P.conjugate().T and P*P == P
    assert s.trace(P) == 2 and P.rank() == 2
assert list(Pe.diagonal()) == [s.Rational(2,3)]*3
counts['exact_rank_two_projectors'] = 2

# All ordered positive compositions, generated afresh.
def compositions(total, length):
    if length == 1:
        if total >= 1:
            yield (total,)
        return
    for first in range(1,total-length+2):
        for rest in compositions(total-first,length-1):
            yield (first,)+rest

phases = (1,s.I,-1,-s.I)
checked = 0
for N in range(1,8):
    for d in range(1,N+1):
        for sizes in compositions(N,d):
            # Include one unused zero coordinate to check deterministic-row support.
            P = s.zeros(N+1)
            offset = 0
            for n in sizes:
                for j in range(n):
                    for k in range(n):
                        P[offset+j,offset+k] = phases[j%4]*s.conjugate(phases[k%4])/n
                offset += n
            assert P == P.conjugate().T and P*P == P
            assert s.trace(P) == d and P[N,N] == 0
            # Aggregate leverage exponents within each block are exactly one.
            assert all(n*s.Rational(1,n) == 1 for n in sizes)
            checked += 1
counts['exact_phase_block_projectors_with_zero_row'] = checked

# All finite block products at a=log 2; compare exact rational values.
block_count = 0
for N in range(1,11):
    for d in range(1,N+1):
        m,k = divmod(N,d)
        balanced = (m,)*(d-k)+(m+1,)*k
        target = math.prod(Fraction(2**n-1,2**n) for n in balanced)
        for sizes in compositions(N,d):
            value = math.prod(Fraction(2**n-1,2**n) for n in sizes)
            assert value <= target
            block_count += 1
counts['exact_balanced_block_comparisons'] = block_count

# The counterexample uses rational marginal tails, no quadrature or Monte Carlo.
lower_equal = Fraction(1)-3*Fraction(1,64)
block = (1-Fraction(1,16))*(1-Fraction(1,256))
upper = (1-Fraction(1,64))**2
assert lower_equal-block == Fraction(79,4096)
assert lower_equal == Fraction(3904,4096)
assert block == Fraction(3825,4096)
assert upper == Fraction(3969,4096)
assert block < lower_equal < upper
counts['exact_large_radius_counterexample'] = 1

# Exact polydisc coefficient from overlap area integration.
x = s.symbols('x', real=True)
I = s.integrate(x*(2*s.acos(x/2)-x*s.sqrt(4-x*x)/2),(x,0,1))
C = 3 - 9*s.sqrt(3)/(4*s.pi)
assert s.simplify(6*I/s.pi-C) == 0
# pi<22/7 and 22/7<15 sqrt(3)/8 imply C<9/5.
assert s.Rational(22,7)**2 < (s.Rational(15,8)**2)*3
small_a = Fraction(1,100)
small_lower_coefficient = 2*(1-3*small_a)
assert small_lower_coefficient == Fraction(97,50) > Fraction(9,5)
counts['exact_section_integral'] = 1
counts['exact_small_radius_comparison'] = 1

# Hyperplane Jacobian and inverse marginal covariance for the simplex formula.
alpha,beta = s.symbols('alpha beta', nonnegative=True)
A = s.Matrix([[1,0],[0,1],[-alpha,-beta]])
assert s.expand((A.T*A).det()) == 1+alpha**2+beta**2
q1,q2 = s.symbols('q1 q2', nonnegative=True)
q3 = 1-q1-q2
assert s.simplify((1+q1/q3+q2/q3)-1/q3) == 0
Sigma = s.Matrix([[1-q1,-s.sqrt(q1*q2)],[-s.sqrt(q1*q2),1-q2]])
assert s.simplify(Sigma.det()-q3) == 0
assert s.simplify(Sigma.inv()[0,0]-(1-q2)/q3) == 0
assert s.simplify(Sigma.inv()[1,1]-(1-q1)/q3) == 0
counts['symbolic_hyperplane_parameterization_checks'] = 5

# Log-scale numerical diagnostics avoid probability cancellation/underflow.
threshold_checks = 0
minimum_log_advantage = math.inf
for N in range(3,61):
    for d in range(2,N):
        m,k = divmod(N,d)
        if not k:
            continue
        gap = N/d-m
        radius_squared = math.log(N)/gap + 1
        log_equal_failure_bound = math.log(N)-(N/d)*radius_squared
        log_block_failure_lower = -m*radius_squared
        advantage = log_block_failure_lower-log_equal_failure_bound
        assert advantage > 0
        assert abs(advantage-gap) < 1e-10
        minimum_log_advantage = min(minimum_log_advantage,advantage)
        threshold_checks += 1
counts['all_dimension_threshold_diagnostics'] = threshold_checks

result = {
    'status':'PASS',
    'counts':counts,
    'exact_rank2_N3':{
        'r_squared':'log(16)',
        'rounded_block_probability':str(block),
        'equal_diagonal_union_lower_bound':str(lower_equal),
        'improvement_at_least':str(lower_equal-block),
        'ambient_upper_bound':str(upper),
        'strictness_of_global_upper':'proved by equality classification and compactness, not by this finite checker'
    },
    'small_radius':{
        'r_squared':'1/100',
        'equal_diagonal_coefficient_exact':'3 - 9*sqrt(3)/(4*pi)',
        'equal_diagonal_coefficient_decimal':float(C),
        'equal_diagonal_coefficient_upper':'9/5',
        'block_lower_coefficient':'97/50'
    },
    'threshold_minimum_log_advantage':minimum_log_advantage,
    'not_certified_by_controls':['general Brascamp-Lieb equality theorem','compactness theorem','global nondivisible optimizer','explicit global strict-gap size'],
    'historical_programs_executed':False,
    'network_calls':False,
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
}
(HERE/'RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
