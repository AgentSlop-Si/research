"""Fresh formula-only checks; no archival module is imported or executed.

Ledger checks compare independently summed mathematical formulas. They are
not measurements of the historical evaluator or fallback executions.
"""
from collections import Counter
from fractions import Fraction
import json
from math import gcd
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parent
counts = Counter()
rng = random.Random(12017)
p = 257

def ramanujan_dyadic(q, n):
    if q == 1:
        return 1
    n %= q
    return q//2 if n == 0 else (-q//2 if n == q//2 else 0)

def alias_difference(x,q):
    m = q//2
    return [sum(x[j+t*q]-x[j+m+t*q] for t in range(len(x)//q)) for j in range(m)]

def coefficient_defect(r):
    """Direct signed-substitution formula, independent of archived code."""
    m = len(r)
    result = [-a for a in r]
    for j,a in enumerate(r):
        quotient,remainder = divmod(5*j,m)
        result[remainder] += (-1)**quotient*a
    return [a%p for a in result]

for d in range(1,8):
    n = 2**d
    root = pow(3,256//n,p)
    assert pow(root,n,p)==1 and pow(root,n//2,p)!=1
    inputs = [[rng.randrange(p) for _ in range(n)] for _ in range(3)]
    if n <= 16:
        inputs += [[int(j==i) for j in range(n)] for i in range(n)]
    for x in inputs:
        reconstructed = [Fraction(sum(x),n) for _ in range(n)]
        direct = [sum(a*pow(root,j*k,p) for j,a in enumerate(x))%p for k in range(n)]
        covered = {0}
        orbit_sum,hybrid_sum,T,nu = 0,0,0,0
        for a in range(1,d+1):
            q = 2**a
            r = alias_difference(x,q)
            m = q//2
            beta = [Fraction(a,n) for a in r]
            projected = [sum(beta[j]*ramanujan_dyadic(q,t-j) for j in range(m)) for t in range(n)]
            anti = [Fraction(q,2*n)*r[t%q] if t%q<m else -Fraction(q,2*n)*r[t%q-m] for t in range(n)]
            assert projected == anti
            reconstructed = [a+b for a,b in zip(reconstructed,projected)]
            counts['exact_rational_projection_maps'] += 1
            z = pow(root,n//q,p)
            for k in range(1,q,2):
                target = k*n//q
                assert target not in covered
                covered.add(target)
                value = sum(a*pow(z,j*k,p) for j,a in enumerate(r))%p
                assert value == direct[target]
                counts['exact_conductor_output_maps'] += 1
            modproj = [(a.numerator*pow(a.denominator,-1,p))%p for a in projected]
            for k in range(n):
                value = sum(a*pow(root,j*k,p) for j,a in enumerate(modproj))%p
                member = k > 0 and n//gcd(n,k) == q
                assert value == (direct[k] if member else 0)
                counts['exact_projection_spectral_checks'] += 1
            if q >= 4:
                delta = coefficient_defect(r)
                s = sum(v != 0 for v in delta)
                nu += sum((5*j//m)%2 for j in range(m))
                T += m*s
                anchor_formula = 2*2*m
                defect_formula = 2*m*s
                edge_formula = 2*(q//4-1)
                local_orbit = anchor_formula+defect_formula+edge_formula
                assert local_orbit == 5*m+2*m*s-2
                local_fft = m+3*m*(a-1)//2
                orbit_sum += local_orbit
                hybrid_sum += min(local_orbit,local_fft)
                counts['local_cost_formula_checks'] += 1
        assert len(covered)==n and reconstructed==[Fraction(a) for a in x]
        counts['exact_full_reconstructions'] += 1
        preparation_formula = n+2*d
        discovery_formula = 2*(n-1)+(n-2)+nu
        assert preparation_formula+discovery_formula+orbit_sum == 9*n-12+2*T+nu
        counts['global_ledger_formula_checks'] += 1
        comparator_formula = n+2*d+3*n*d//2
        assert preparation_formula+discovery_formula+hybrid_sum <= comparator_formula+n-3+nu
        counts['hybrid_formula_bound_checks'] += 1

result = {'status':'PASS','evidence_kind':'fresh formula-only controls; no historical imports or evaluator executions',
          'domain':'exact rationals and prime field F_257','N_values':[2,4,8,16,32,64,128],
          'seed':12017,'counts':dict(counts),
          'excluded_evidence':'An earlier checker executed the archived evaluator; those outcomes are preserved separately and excluded from accepted evidence.',
          'scope_limit':'Finite exact checks supplement the algebraic proof. Ledger and hybrid tests compare formulas; no actual evaluator/fallback replay, performance benchmark or arbitrary-input sub-N-log-N claim.'}
(ROOT/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
