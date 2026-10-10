"""Fresh review checks; does not load or execute supplied research programs."""
import json
import math
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import numpy as np
import sympy as sp

out = {}
y, tau = sp.symbols('y tau')
hermite = []
boundary_checks = 0
for A in range(1, 13):
    H = sp.hermite_prob(A, y)
    J = y * H - tau * sp.diff(H, y)
    D = sp.factor(sp.discriminant(J, y))
    for t in range(-4, 5):
        z = 1 + sp.Rational(1-t*t, 1+t*t) + sp.I*sp.Rational(2*t, 1+t*t)
        assert sp.simplify(D.subs(tau, z)) != 0
        boundary_checks += 1
    assert (D.subs(tau, 0) == 0) == bool(A % 2)
    if A % 2 == 0:
        assert D.subs(tau, -sp.Rational(1, A)) == 0
        assert sp.Poly(J.subs(tau, -sp.Rational(1, A)), y).coeff_monomial(y**3) != 0
    hermite.append({'A': A, 'discriminant': str(D)})
out['hermite'] = {'exact_boundary_samples': boundary_checks, 'discriminants': hermite}

threshold_checks = 0
for q in range(1, 9):
    for r in range(1, 9):
        a = 3**r
        for diagonal in [False, True]:
            threshold = (4*q*r*a*a + 2*q*(a-1)+2) if diagonal else (q*r*a*a + q*(a-1))
            N = threshold + 1
            m = N//2 if diagonal else N
            for _ in range(r):
                assert m >= 4*q
                m = (m-q+2)//3
            assert m*m > N*q*r
            threshold_checks += 1
out['separator'] = {'threshold_boundary_checks': threshold_checks}

N = 8
L = N//4
U = np.exp(-2j*np.pi*np.outer(np.arange(N),np.arange(N))/N)/math.sqrt(N)
B = Fraction(L) + Fraction(3,4) + Fraction(1,4*L) + Fraction(1,16*L*L)
delta = math.sqrt(1-math.sqrt(float(B/Fraction(L+1))))
minimum = float('inf')
maximum_trace = 0.
count = 0
for R in combinations(range(N),2*L-1):
    I = sorted(set(range(N))-set(R))
    for H in combinations(range(N),2*L+1):
        V = U[np.ix_(R,H)]
        A = U[np.ix_(I,H)].conj().T @ U[np.ix_(I,H)]
        trace = np.trace(A @ A).real
        sv = np.linalg.svd(V,compute_uv=False)[L]
        assert trace <= float(B)+1e-10
        assert sv >= delta-1e-10
        minimum = min(minimum,float(sv))
        maximum_trace = max(maximum_trace,float(trace))
        count += 1
out['dyadic_gap'] = {'N': N, 'submatrices': count, 'delta_bound': delta,
                     'minimum_singular_value': minimum, 'trace_bound': float(B),
                     'maximum_trace': maximum_trace,
                     'arithmetic': 'floating exploratory check, not exact proof'}

carry_checks = 0
for s in range(1, 102, 4):
    for p in list(sp.primerange(5,200)):
        if p % 4 != 1:
            continue
        D = Fraction(s*(p-3),8)
        R = Fraction(s*p,4)
        assert math.floor(D+R)-math.floor(D)-math.floor(R) == int(p%8 == 1)
        carry_checks += 1
out['content_carry'] = {'exact_floor_checks': carry_checks,
                        'note': 'checks arithmetic only, not lower-prime unit hypotheses'}
Path(__file__).with_name('independent_check_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:{a:b for a,b in v.items() if a!='discriminants'} for k,v in out.items()},indent=2))
