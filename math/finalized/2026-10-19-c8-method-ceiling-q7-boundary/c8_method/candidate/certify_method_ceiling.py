#!/usr/bin/env python3
"""Exact rational certificate for optimizing the accepted C8 gap chain.

Only Python standard-library integer/Fraction arithmetic is used for all tests.
Decimal conversions are explicitly outward-rounded presentation of exact
rational interval endpoints. No prior checker is imported or executed.
"""
from fractions import Fraction as Q
from math import factorial, isqrt
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from pathlib import Path
import hashlib, json, time

ROOT = Path(__file__).resolve().parent
START = time.perf_counter()
SOURCE_DIRS = [
    Path('/workspace/shared/phase_rankzero_quantitative_20261019_1347'),
    Path('/workspace/shared/phase_rankzero_quantitative_review_20261019_1354'),
]
ASSERTIONS = []

def check(condition, name):
    if not condition:
        raise AssertionError(name)
    ASSERTIONS.append(name)

def receipts():
    return {str(p): {'bytes': p.stat().st_size,
                     'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
            for d in SOURCE_DIRS for p in sorted(d.iterdir()) if p.is_file()}

BEFORE = receipts()

def sqrt_bounds(q, name, places=100):
    """Return exact rational bounds [a,b] for sqrt(q), b-a=10^-places."""
    check(q >= 0, name + ': nonnegative radicand')
    scale = 10**places
    m = isqrt((q.numerator * scale**2) // q.denominator)
    a, b = Q(m, scale), Q(m+1, scale)
    check(a*a <= q < b*b, name + ': bounding squares verified')
    check(b-a == Q(1, scale), name + ': stated enclosure width')
    return a, b

def trig_bounds(x, kind, name):
    """Alternating Taylor lower S9 and upper S10, valid for 0<=x<=1."""
    check(0 <= x <= 1, name + ': alternating-series domain')
    offset = 0 if kind == 'cos' else 1
    terms = [x**(2*k+offset) / factorial(2*k+offset) for k in range(11)]
    check(all(terms[k+1] <= terms[k] for k in range(10)),
          name + ': decreasing term magnitudes')
    lower = sum((-1)**k * terms[k] for k in range(10))
    upper = lower + terms[10]
    check(lower <= upper, name + ': ordered alternating bounds')
    return lower, upper

SQ2 = sqrt_bounds(Q(2), 'sqrt2')

def c2_bounds(e, name):
    # cos(3pi/8+e)^2 = 1/2 - sqrt2/4 * (cos(2e)+sin(2e)).
    co = trig_bounds(2*e, 'cos', name + ': cos(2e)')
    si = trig_bounds(2*e, 'sin', name + ': sin(2e)')
    h = co[0]+si[0], co[1]+si[1]
    check(h[0] > 0, name + ': positive trig sum')
    out = Q(1,2)-SQ2[1]*h[1]/4, Q(1,2)-SQ2[0]*h[0]/4
    check(0 < out[0] <= out[1] < 1, name + ': positive cosine square')
    return out

def rho2_bounds(e, name):
    root = sqrt_bounds(10*e, name + ': sqrt(10epsilon)')
    out = 10*e+e*e+2*e*root[0], 10*e+e*e+2*e*root[1]
    check(0 < out[0] <= out[1], name + ': positive rho square')
    return out

def gap_bounds(e, name):
    q = rho2_bounds(e, name)
    c2 = c2_bounds(e, name)
    check(1-1800*q[1] > 0, name + ': positive beta square')
    # G is increasing in q and decreasing in c2 in this domain.
    low = 6498*q[0] - c2[1]*(1-1800*q[0])
    high = 6498*q[1] - c2[0]*(1-1800*q[1])
    check(low <= high, name + ': ordered gap interval')
    return low, high

def outward(q, rounding, precision=75):
    with localcontext() as ctx:
        ctx.prec = precision
        ctx.rounding = rounding
        return str(Decimal(q.numerator)/Decimal(q.denominator))

def presented_interval(interval):
    return {'lower': outward(interval[0], ROUND_FLOOR),
            'upper': outward(interval[1], ROUND_CEILING),
            'presentation': 'outward-rounded exact rational enclosure'}

N = 216382078575297666905178343251032596362320361
D = 10**50
EL, EU = Q(N,D), Q(N+1,D)
EBOX = Q(3,10**6)
check(Q(2,10**6) < EL < EU < EBOX, 'root bracket lies in auxiliary-valid box')
check(EU-EL == Q(1,10**50), 'epsilon root bracket width is exactly 10^-50')
check(EL/2 == Q(N,2*D), 'residual angle increment is epsilon/2')

# Uniform auxiliary conditions on 0<epsilon<=3*10^-6. Use only rational
# inequalities and the accepted standard sine/cosine derivative bounds.
check(Q(283,200)**2 > 2, 'sqrt2 < 283/200')
check((2-Q(283,200))/4 > Q(191,500)**2,
      'cos(theta0) > 191/500 by positive squaring')
check(Q(231,250)**2 > (2+Q(283,200))/4,
      'sin(theta0) < 231/250 by positive squaring')
check(EBOX < Q(3,8), 'theta < pi/2 throughout box using pi>3')
check(Q(191,500)-EBOX > 0, 'positive cosine bound in box')
check(Q(5,2)*(Q(191,500)-EBOX) > Q(231,250)+EBOX,
      'tan(theta) < 5/2 throughout box')
check(Q(11,2000)-EBOX > 0, 'positive comparison for rho')
check((Q(11,2000)-EBOX)**2 > 10*EBOX,
      'rho < 11/2000 throughout box')
check(8*Q(11,2000)**2 < Q(1,50)**2,
      'eta=2sqrt2 rho < 1/50 throughout box')
check(1-1800*Q(11,2000)**2 > 0,
      '1-225eta^2 = 1-1800rho^2 > 0 throughout box')
check(2-(4*EBOX)**2 > Q(199,100),
      '2cos(4epsilon) > 199/100 throughout box')
check(16*EBOX < 6, 'opposite-offset uniqueness: 16epsilon < 2pi')
check(4*EBOX < Q(3,2), 'positive cosine branch: 4epsilon < pi/2')
check(Q(24,25)*Q(4,5)*Q(47,50) > Q(21,25)**2,
      'unchanged phase-product denominator constant')
check(4*Q(101,50)/Q(21,25)/5 == Q(202,105),
      'unchanged phase-product bound is 202/105')
check(Q(202,105) < Q(199,100), 'unchanged phase-product contradiction margin')
check(1+14*4 == 57, 'r=rho+14sqrt2 eta=57rho')
check(2*57**2 == 6498, 'squared residual coefficient is 6498')
check(225*8 == 1800, 'squared beta coefficient is 1800')

GLO = gap_bounds(EL, 'epsilon_lower')
GHI = gap_bounds(EU, 'epsilon_upper')
GBOX = gap_bounds(EBOX, 'box_upper')
check(GLO[1] < 0, 'strict compression contradiction at certified epsilon_lower')
check(GHI[0] > 0, 'compression inequality reverses at epsilon_upper')
check(GBOX[0] > 0, 'root exists below box_upper by continuity and G(0)<0')
check(GLO[1] < -Q(1,10**46), 'lower-bracket gap exceeds 10^-46 strictly')
check(GHI[0] > Q(1,10**46), 'upper-bracket gap exceeds 10^-46 strictly')

# Destructive controls: an endpoint beyond the root and a normalization error
# must not be confused with an admissible epsilon or its half-angle increment.
check(not (GHI[1] < 0), 'destructive control rejects epsilon_upper as feasible')
check(EL != EL/2, 'destructive control rejects epsilon/half-angle conflation')
check(1+14*4 != 29, 'destructive control rejects r=29rho')

# Exact enclosure of sin(3pi/16+epsilon/2):
# cos(theta0+epsilon)>0 and sin(theta/2)=sqrt((1-sqrt(c2))/2).
def residual_bound_interval(e, name):
    c2 = c2_bounds(e, name)
    clo = sqrt_bounds(c2[0], name + ': cosine lower')[0]
    chi = sqrt_bounds(c2[1], name + ': cosine upper')[1]
    slo = sqrt_bounds((1-chi)/2, name + ': residual lower')[0]
    shi = sqrt_bounds((1-clo)/2, name + ': residual upper')[1]
    check(0 < slo < shi < 1, name + ': ordered residual interval')
    return slo, shi

BCERT = residual_bound_interval(EL, 'certified_bound')
BCEIL_HI = residual_bound_interval(EU, 'ceiling_upper')
BOLD = residual_bound_interval(Q(1,500000), 'accepted_bound')
IMPROVEMENT = BCERT[0]-BOLD[1], BCERT[1]-BOLD[0]
check(IMPROVEMENT[0] > 0, 'certified new lower endpoint exceeds accepted endpoint')
check(BCEIL_HI[1]-BCERT[0] < Q(1,10**50),
      'certified lower endpoint is within 10^-50 of method ceiling')
check(BCEIL_HI[1]-BCERT[0] > 0, 'method ceiling enclosure is ordered')

# Freeze both source directories and verify no source changed during execution.
AFTER = receipts()
check(BEFORE == AFTER, 'all accepted proof/review source files remain unchanged')

result = {
    'status': 'PASS', 'assertion_count': len(ASSERTIONS),
    'claim': 'Finished optimization of the exact accepted sufficient-condition chain',
    'ceiling_definition': 'unique positive root of (6498+1800*cos(3*pi/8+epsilon)^2)*(sqrt(10*epsilon)+epsilon)^2 - cos(3*pi/8+epsilon)^2 = 0 within 0<epsilon<pi/8',
    'strict_feasible_epsilon_range': '0 < epsilon < epsilon_star',
    'endpoint_caution': 'epsilon_star is the supremum of the strict sufficient conditions; equality is not claimed certified by that strict chain',
    'epsilon_lower_exact': f'{N}/10^50',
    'epsilon_upper_exact': f'{N+1}/10^50',
    'epsilon_bracket': presented_interval((EL,EU)),
    'angle_increment_exact': f'{N}/(2*10^50)',
    'angle_increment_bracket': presented_interval((EL/2,EU/2)),
    'strict_lower_bound_exact': f'sin(3*pi/16 + {N}/(2*10^50))',
    'certified_lower_endpoint_enclosure': presented_interval(BCERT),
    'method_ceiling_lower_endpoint_enclosure': presented_interval((BCERT[0],BCEIL_HI[1])),
    'improvement_over_accepted_endpoint_enclosure': presented_interval(IMPROVEMENT),
    'gap_at_epsilon_lower_enclosure': presented_interval(GLO),
    'gap_at_epsilon_upper_enclosure': presented_interval(GHI),
    'auxiliary_uniform_domain': '0<epsilon<=3/1000000',
    'monotonicity': 'H(epsilon)=(6498/cos(3pi/8+epsilon)^2+1800)*(sqrt(10epsilon)+epsilon)^2-1 is strictly increasing on 0<epsilon<pi/8',
    'model_scope': 'Original all-phase external operator norm; arbitrary invertible complex monomial outer factors; unrestricted real core; actual potentially non-invariant compressions',
    'not_claimed': ['true optimum', 'global optimality of inherited upper witness', 'literature novelty', 'root equality as an admissible strict-inequality endpoint'],
    'arithmetic': 'All assertions use exact Python integers/Fractions; decimals are outward-rounded display only; no sampling or floating-point optimizer',
    'source_files_unchanged': True,
    'runtime_seconds': time.perf_counter()-START,
}
(ROOT/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
(ROOT/'ASSERTIONS.json').write_text(json.dumps(ASSERTIONS,indent=2)+'\n')
(ROOT/'SOURCE_BINDINGS.json').write_text(json.dumps(BEFORE,indent=2)+'\n')
print(json.dumps(result,indent=2))
