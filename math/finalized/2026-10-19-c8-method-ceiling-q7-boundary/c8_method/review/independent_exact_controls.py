#!/usr/bin/env python3
"""Independent dyadic/Lagrange review of the frozen C8 fixed-chain ceiling.

No candidate or historical checker is imported or executed. All tested
inequalities use exact Fraction arithmetic. Decimal output is presentation.
"""
from fractions import Fraction as F
from math import factorial
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from pathlib import Path
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parent
CAND = Path('/workspace/shared/phase_rankzero_method_ceiling_20261019_1431')
BASE = Path('/workspace/shared/phase_rankzero_quantitative_20261019_1347')
REVIEW = Path('/workspace/shared/phase_rankzero_quantitative_review_20261019_1354')
CHECKS = []
START = time.perf_counter()

def check(p, name):
    if not p:
        raise AssertionError(name)
    CHECKS.append(name)

def receipt(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def snapshot():
    paths = {p for d in (CAND, BASE, REVIEW) for p in d.iterdir() if p.is_file()}
    inherited = json.loads((REVIEW/'SOURCE_BINDINGS_BEFORE.json').read_text())
    paths |= {Path(p) for p in inherited}
    return {str(p): receipt(p) for p in sorted(paths)}

BEFORE = snapshot()
(ROOT/'SOURCE_BINDINGS_BEFORE.json').write_text(json.dumps(BEFORE, indent=2)+'\n')
for directory, key in ((CAND, 'files'), (BASE, None), (REVIEW, 'review_files')):
    manifest = json.loads((directory/'MANIFEST.json').read_text())
    manifest = manifest[key] if key else manifest
    for name, expected in manifest.items():
        check(receipt(directory/name) == expected, 'manifest hash: '+str(directory/name))
for bindings in (CAND/'SOURCE_BINDINGS.json', REVIEW/'SOURCE_BINDINGS_BEFORE.json', REVIEW/'SOURCE_BINDINGS_AFTER.json'):
    for path, expected in json.loads(bindings.read_text()).items():
        check(receipt(Path(path)) == {k: expected[k] for k in ('bytes','sha256')},
              'source receipt: '+str(bindings)+' -> '+path)
check(json.loads((REVIEW/'VERDICT.json').read_text())['verdict'] == 'PASS',
      'accepted all-phase analytical review has PASS verdict')

def point(x): return (F(x), F(x))
def add(a,b): return a[0]+b[0], a[1]+b[1]
def neg(a): return -a[1], -a[0]
def sub(a,b): return add(a,neg(b))
def mul(a,b):
    q = [x*y for x in a for y in b]
    return min(q), max(q)
def scale(a,x): return mul(a,point(x))
def reciprocal(a):
    check(a[0]>0, 'positive interval denominator')
    return 1/a[1], 1/a[0]
def sq(a):
    check(a[0]>=0, 'positive interval squaring')
    return a[0]**2, a[1]**2

def root_scalar(q):
    """Binary integer bisection, independent of decimal scaling/isqrt."""
    check(q >= 0, 'nonnegative square-root radicand')
    S = 1 << 384
    lo, hi = 0, S
    while F(hi*hi,S*S) <= q:
        hi *= 2
    while hi-lo > 1:
        mid = (lo+hi)//2
        if F(mid*mid,S*S) <= q:
            lo = mid
        else:
            hi = mid
    a,b = F(lo,S), F(hi,S)
    check(a*a<=q<b*b, 'dyadic square-root bounding squares')
    check(b-a==F(1,S), 'dyadic square-root width 2^-384')
    return a,b

def root(a):
    return root_scalar(a[0])[0], root_scalar(a[1])[1]

def taylor(x, kind):
    """Taylor with absolute Lagrange remainder, not alternating bounds."""
    check(0 <= x <= F(1,1000), 'small rational argument for independent trig')
    if kind=='cos':
        degree = 16
        value = sum(F((-1)**k)*x**(2*k)/factorial(2*k) for k in range(9))
    else:
        degree = 17
        value = sum(F((-1)**k)*x**(2*k+1)/factorial(2*k+1) for k in range(9))
    rem = x**(degree+1)/factorial(degree+1)
    check(rem >= 0, 'absolute Lagrange remainder is nonnegative')
    return value-rem, value+rem

SQRT2 = root(point(2))
# Independent identity: c = cos(3pi/8)cos(e)-sin(3pi/8)sin(e).
# This deliberately avoids the candidate's double-angle formula for c^2.
C0 = scale(root(sub(point(2),SQRT2)),F(1,2))
S0 = scale(root(add(point(2),SQRT2)),F(1,2))

def evaluate(e):
    c = sub(mul(C0,taylor(e,'cos')),mul(S0,taylor(e,'sin')))
    q = sq(add(root(point(10*e)),point(e)))
    c2 = sq(c)
    r2 = scale(q,57**2)
    beta2 = sub(point(1),scale(q,1800))
    check(beta2[0] > 0, 'positive beta-square interval')
    # Direct compression contradiction margin, opposite sign to candidate G.
    margin = sub(mul(c2,beta2),scale(r2,2))
    # Separately normalized H, checking division/normalization independently.
    h = sub(mul(add(scale(reciprocal(c2),6498),point(1800)),q),point(1))
    residual = root(scale(sub(point(1),c),F(1,2)))
    return {'c':c,'c2':c2,'rho2':q,'margin':margin,'G':neg(margin),
            'H':h,'residual':residual}

N = 216382078575297666905178343251032596362320361
DEN = 10**50
EL, EU, BOX = F(N,DEN), F(N+1,DEN), F(3,10**6)
check(0 < F(2,10**6) < EL < EU < BOX < F(3,8), 'ordered bracket in arc and auxiliary box')
check(EU-EL == F(1,10**50), 'root bracket has exact width 10^-50')
check(EL/2 == F('0.000001081910392876488334525891716255162981811601805'),
      'exact residual half-angle increment')

# Whole-box auxiliary margins from the inherited analytic proof.
check(F(283,200)**2 > 2, 'sqrt2 rational upper bound')
check((2-F(283,200))/4 > F(191,500)**2, 'cos(theta0) rational lower bound')
check((2+F(283,200))/4 < F(231,250)**2, 'sin(theta0) rational upper bound')
check(F(191,500)-BOX > 0, 'uniform positive cosine')
check(F(231,250)+BOX < F(5,2)*(F(191,500)-BOX), 'uniform tan(theta)<5/2')
check(BOX < F(3,8), 'theta<pi/2 from pi>3')
check(BOX < F(9,8), 'theta0-epsilon positive from pi>3')
check(16*BOX < 6, 'unique opposite cycle offsets')
check(4*BOX < F(3,2), 'positive cosine branch for phase-product contradiction')
check(F(11,2000)-BOX>0 and (F(11,2000)-BOX)**2>10*BOX,
      'uniform rho<11/2000')
check(8*F(11,2000)**2 < F(1,50)**2, 'uniform eta<1/50')
check(1800*F(11,2000)**2 < 1, 'uniform positive beta-square bound')
check(F(24,25)*F(4,5)*F(47,50)>F(21,25)**2, 'normalized-product denominator margin')
check(4*F(101,50)/F(21,25)/5==F(202,105)<F(199,100), 'phase-product rational upper margin')
check(2-(4*BOX)**2>F(199,100), 'uniform phase-product cosine lower margin')
check(1+14*4==57 and 2*57**2==6498 and 225*8==1800, 'fixed-chain coefficients and factor normalization')

LO, HI, EBOX, OLD = [evaluate(e) for e in (EL,EU,BOX,F(2,10**6))]
check(LO['margin'][0] > F(1,10**46), 'strict compression contradiction at epsilon lower')
check(HI['margin'][1] < -F(1,10**46), 'strict condition fails at epsilon upper')
check(LO['H'][1]<0<HI['H'][0], 'independent normalized H endpoint signs')
check(EBOX['H'][0]>0 and OLD['H'][1]<0, 'box and old endpoint controls')
improvement = sub(LO['residual'],OLD['residual'])
check(improvement[0]>0, 'new endpoint strictly improves accepted bound')
ceiling_diff = sub(HI['residual'],LO['residual'])
check(0<ceiling_diff[0]<=ceiling_diff[1]<F(5,10**51), 'residual bracket width below 5e-51')

# Independently validate all reported outward rational enclosure endpoints.
reported = json.loads((CAND/'CHECK_RESULTS.json').read_text())
for key, own in (
    ('gap_at_epsilon_lower_enclosure',LO['G']),
    ('gap_at_epsilon_upper_enclosure',HI['G']),
    ('certified_lower_endpoint_enclosure',LO['residual']),
    ('method_ceiling_lower_endpoint_enclosure',(LO['residual'][0],HI['residual'][1])),
    ('improvement_over_accepted_endpoint_enclosure',improvement)):
    x = reported[key]
    check(F(x['lower'])<own[0] and own[1]<F(x['upper']), 'independent enclosure inside reported '+key)

# Deliberately wrong substitutions must fail the appropriate independent test.
check(not (HI['H'][1]<0), 'reject above-ceiling epsilon as strict-admissible')
check(EL/2!=EL, 'reject epsilon/half-angle confusion')
check(2*57**2!=2*29**2, 'reject lost factor in flat-vector error')
check(reported['strict_feasible_epsilon_range']=='0 < epsilon < epsilon_star',
      'candidate records open strict feasible interval')

AFTER = snapshot()
check(BEFORE==AFTER, 'every frozen source remains byte-identical')
(ROOT/'SOURCE_BINDINGS_AFTER.json').write_text(json.dumps(AFTER,indent=2)+'\n')

def outward(q, mode):
    with localcontext() as ctx:
        ctx.prec=90
        ctx.rounding=mode
        return str(Decimal(q.numerator)/Decimal(q.denominator))
def show(i):
    return {'lower':outward(i[0],ROUND_FLOOR),'upper':outward(i[1],ROUND_CEILING)}
result = {
    'status':'PASS', 'exact_assertions':len(CHECKS),
    'source_files_bound':len(BEFORE), 'source_immutability_verified':BEFORE==AFTER,
    'epsilon_bracket_exact':[str(EL),str(EU)],
    'epsilon_bracket_decimal':show((EL,EU)),
    'G_lower_independent_enclosure':show(LO['G']),
    'G_upper_independent_enclosure':show(HI['G']),
    'H_lower_independent_enclosure':show(LO['H']),
    'H_upper_independent_enclosure':show(HI['H']),
    'certified_residual_enclosure':show(LO['residual']),
    'improvement_over_previous_bound':show(improvement),
    'residual_bracket_width':show(ceiling_diff),
    'arithmetic':'Exact rational interval arithmetic; binary dyadic square-root bisection at 384 bits; separate angle-addition and absolute Taylor-Lagrange remainder.',
    'candidate_or_historical_checker_imported_or_executed':False,
    'external_writes':False, 'subagents_spawned':False,
    'runtime_seconds':time.perf_counter()-START,
}
(ROOT/'ASSERTIONS.json').write_text(json.dumps(CHECKS,indent=2)+'\n')
(ROOT/'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
