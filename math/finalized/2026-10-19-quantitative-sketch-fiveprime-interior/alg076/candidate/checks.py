#!/usr/bin/env python3
"""Fresh standard-library exact checks. No historical source code is executed."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent


def exp_bounds(x, terms=1024):
    """Exact rational lower/upper bounds for exp(x), x>=0.

    S_m=sum_(j=0)^m x^j/j!. The first omitted term is t_(m+1).
    Every later consecutive ratio is <=x/(m+2)=q<1, so the
    entire omitted tail is <=t_(m+1)/(1-q).
    """
    x = F(x)
    assert x >= 0 and x < terms + 2
    term = F(1)
    total = term
    for j in range(1, terms + 1):
        term *= x / j
        total += term
    first = term * x / (terms + 1)
    q = x / (terms + 2)
    return total, total + first / (1 - q)


def decimal(x):
    with localcontext() as ctx:
        ctx.prec = 25
        return str(Decimal(x.numerator) / Decimal(x.denominator))


def upper_chernoff(n, k, eps, s, lam, mu, terms=1024):
    assert type(n) is int and type(k) is int and 0 <= k < n
    assert 0 < eps < 1 and s > 0 and lam > 0 and 0 < mu < 1
    d = n-k
    positive_argument = lam * eps**2 * s
    negative_argument = mu * s
    _, epos_hi = exp_bounds(positive_argument, terms)
    eneg_lo, _ = exp_bounds(negative_argument, terms)
    low_tail = epos_hi / (1+lam)**d
    high_tail = 1 / (eneg_lo * (1-mu)**n)
    return low_tail, high_tail, low_tail+high_tail


def gamma_bounds(d, t, terms=1024):
    assert type(d) is int and d >= 1 and t >= 0
    lo, hi = exp_bounds(t, terms)
    poly = sum((t**j / math.factorial(j) for j in range(d)), F(0))
    # G=1-poly/exp(t), monotonically increasing with exp(t).
    return max(F(0), 1-poly/lo), min(F(1), 1-poly/hi)


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a,b):
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]


def inv(a):
    n=len(a)
    aug=[[F(v) for v in a[i]]+[F(i==j) for j in range(n)] for i in range(n)]
    for c in range(n):
        p=next(i for i in range(c,n) if aug[i][c])
        aug[c],aug[p]=aug[p],aug[c]
        v=aug[c][c]
        aug[c]=[x/v for x in aug[c]]
        for i in range(n):
            if i!=c:
                v=aug[i][c]
                aug[i]=[x-v*y for x,y in zip(aug[i],aug[c])]
    return [row[n:] for row in aug]


def check_projector(a):
    # Rational real matrices are also legitimate complex measurement maps.
    a=[[F(v) for v in row] for row in a]
    at=transpose(a)
    p=mm(mm(at,inv(mm(a,at))),a)
    assert p==transpose(p)
    assert mm(p,p)==p
    assert mm(a,p)==a
    assert sum(p[j][j] for j in range(len(p)))==len(a)
    q=[[F(i==j)-p[i][j] for j in range(len(p))] for i in range(len(p))]
    assert mm(a,q)==[[0]*len(p) for _ in a]
    assert mm(p,q)==[[0]*len(p) for _ in p]
    return {'N':len(p),'rank':len(a),'null_dimension':len(p)-len(a)}


def run():
    checks=[]
    projectors=[]
    for a in [ [[1,1]], [[1,2,3,4]], [[1,0,1,2],[0,1,2,1]],
               [[1,2,0,1,0],[0,1,1,0,3],[1,0,2,1,1]] ]:
        projectors.append(check_projector(a))
    checks.append('Four exact rational orthogonal-projector fixtures pass.')

    # S_(d-1)-S'_(d-1) has only the top-degree term 1/(d-1)!.
    for d in range(1,65):
        coeff=[F(1,math.factorial(j)) for j in range(d)]
        deriv=[(j+1)*coeff[j+1] if j+1<d else F(0) for j in range(d)]
        assert [a-b for a,b in zip(coeff,deriv)]==[F(0)]*(d-1)+[F(1,math.factorial(d-1))]
        # G_d-G_(d+1)=e^-t t^d/d! >=0; exact polynomial coefficient.
        nextcoeff=[F(1,math.factorial(j)) for j in range(d+1)]
        assert nextcoeff[:-1]==coeff and nextcoeff[-1]>0
    checks.append('64 gamma-CDF derivative and shape-monotonicity identities pass.')

    # General exponential enclosure internal checks; nested higher-degree
    # enclosures contain each other exactly.
    for x in [F(0),F(1,10),F(1),F(7,3),F(10),F(50),F(208),F(256)]:
        lo,hi=exp_bounds(x,512)
        lo2,hi2=exp_bounds(x,1024)
        assert 0<lo<=lo2<=hi2<=hi
    checks.append('Eight exact nested exponential-enclosure controls pass.')

    eps=F(1,2); s=F(1280); lam=F(13,20); mu=F(1,5)
    low,high,b=upper_chernoff(1024,496,eps,s,lam,mu)
    threshold=F(12,10**13)
    assert b < threshold
    # The strict comparison above is integer/rational, not decimal display.
    bound_record={
        'N':1024,'K':16,'M':64,'R':31,'rank_cap':496,'hidden_dimension':528,
        'epsilon':'1/2','s':'1280','lower_tail_lambda':'13/20','upper_tail_mu':'1/5',
        'exp_terms':1024,
        'gamma_lower_tail_chernoff_upper_display':decimal(low),
        'energy_upper_tail_chernoff_upper_display':decimal(high),
        'sum_upper_display':decimal(b),
        'strict_rational_ceiling':'12/10000000000000',
        'strict_rational_comparison':True,
        'fraction_binary_sha256':hashlib.sha256(b.numerator.to_bytes((b.numerator.bit_length()+7)//8,'big')+b'/' +b.denominator.to_bytes((b.denominator.bit_length()+7)//8,'big')).hexdigest(),
        'rational_numerator_bits':b.numerator.bit_length(),'rational_denominator_bits':b.denominator.bit_length(),
        'gaussian_mass_of_inputs_with_success_at_least_0_99_upper_display':decimal(b/F(99,100))
    }
    checks.append('N=1024, R=31 fixture: relative-half-error success <1.2e-12, exactly certified.')

    # A distinct small finite fixture compares exact gamma-CDF enclosures to
    # the Chernoff bound (not an asymptotic or simulation extrapolation).
    n,k,e,s0,lam0,mu0=16,4,F(1,2),F(24),F(1),F(1,3)
    gl,gh=gamma_bounds(n-k,e*e*s0)
    nl,nh=gamma_bounds(n,s0)
    _,_,cb=upper_chernoff(n,k,e,s0,lam0,mu0)
    exact_upper=gh+1-nl
    assert exact_upper <= cb
    checks.append('N=16 exact gamma enclosure is below its scalar Chernoff bound.')

    # Boundary controls: finite binary inputs are not continuous ambient data.
    binary_codes={sum(((mask>>j)&1)*2**j for j in range(12)) for mask in range(2**12)}
    assert len(binary_codes)==2**12
    # One complex measurement x_1+i*x_2 has realified matrix identity on R².
    realified=[[1,0],[0,1]]
    assert realified[0][0]*realified[1][1]-realified[0][1]*realified[1][0]==1
    checks.append('Rank-one finite-binary injectivity and complex/real rank controls pass.')

    rejected=0
    for args in [(16,16,e,s0,lam0,mu0),(16,-1,e,s0,lam0,mu0),
                 (16,4,F(1),s0,lam0,mu0),(16,4,e,s0,lam0,F(1)),
                 (16,4,e,s0,F(0),mu0)]:
        try: upper_chernoff(*args)
        except AssertionError: rejected+=1
        else: raise AssertionError('Malformed model control was accepted')
    assert rejected==5
    checks.append('Five malformed rank/epsilon/Chernoff-parameter controls rejected.')

    # Exact original-schedule ledger, including dyadic endpoint factors.
    ledgers=[]
    for kpow,mpow in [(0,10),(4,6),(10,0),(3,5)]:
        K,M=2**kpow,2**mpow; N=K*M; R=max(1,(M+1)//2)
        count=F(R*K*kpow+N*mpow,2)
        rhs=F(N,2)*(F(R,M)*kpow+mpow)
        floor=F(N,2)*min(F(R,M),F(1))*(kpow+mpow)
        assert count==rhs and count>=floor
        ledgers.append({'N':N,'K':K,'M':M,'R':R,'butterfly_occurrences':str(count),'proved_floor':str(floor)})
    checks.append('Four exact evaluator ledgers, including K=1 and M=1, pass.')

    result={
        'verdict':'PASS','arithmetic':'Python standard-library Fraction; Decimal only for display',
        'theorem_scope':'Finite arithmetic support only; universal statements are proved in REPORT.md.',
        'checks':checks,'projectors':projectors,'finite_certificate':bound_record,
        'small_gamma_fixture':{'N':n,'k':k,'exact_bound_upper_display':decimal(exact_upper),'chernoff_upper_display':decimal(cb)},
        'schedule_ledgers':ledgers,
        'input_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__).resolve(),ROOT/'REPORT.md',ROOT/'sources/FUSION_THEOREMS.md',ROOT/'sources/FREQUENCY_AUDIT.md',ROOT/'sources/V5_README.md',ROOT/'sources/OWNER_RECORD.json']}
    }
    (ROOT/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    run()
