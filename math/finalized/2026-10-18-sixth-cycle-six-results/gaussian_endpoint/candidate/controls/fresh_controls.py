#!/usr/bin/env python3
"""Fresh ALG-036 endpoint controls. No historical code, external writes, or network."""
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import random

import scipy
from scipy.stats import ncx2
import sympy as sp

SEED = 202610182053
rng = random.Random(SEED)
I = sp.I
counts = {
    'coordinate_projectors': 0,
    'dense_complex_projectors': 0,
    'projector_pivots': 0,
    'schur_complement_comparisons': 0,
    'adaptive_paths': 0,
    'adaptive_positive_variance_queries': 0,
    'adaptive_redundant_queries': 0,
    'scalar_disk_cases': 0,
    'coordinate_probability_bound_cases': 0,
}

def simp(A):
    return A.applyfunc(sp.simplify)

def zero(A):
    return all(sp.simplify(z) == 0 for z in A)

def assert_projector(P, d):
    assert zero(P-P.conjugate().T)
    assert zero(P*P-P)
    assert sp.simplify(sp.trace(P)) == d


def check_projector(P, d, schur):
    n = P.rows
    original = P
    selected = []
    assert_projector(P, d)
    for ell in range(d):
        remaining = d-ell
        diagonal = [sp.simplify(P[j,j]) for j in range(n)]
        assert all(v.is_real and v >= 0 for v in diagonal)
        j = max(range(n), key=lambda j: diagonal[j])
        v = diagonal[j]
        assert v >= sp.Rational(remaining,n)
        assert v > 0 and j not in selected
        if ell < (d+1)//2:
            assert v >= sp.Rational(d,2*n)
        col = P[:,j]
        P = simp(P-col*col.conjugate().T/v)
        selected.append(j)
        assert_projector(P, remaining-1)
        assert all(z == 0 for k in selected for z in P[k,:])
        if schur:
            principal = original.extract(selected,selected)
            assert principal.det() != 0
            cross = original.extract(range(n), selected)
            other = original.extract(selected, range(n))
            direct = simp(original-cross*principal.inv()*other)
            assert zero(P-direct)
            counts['schur_complement_comparisons'] += 1
        counts['projector_pivots'] += 1
    assert zero(P)

# Exact exhaustive coordinate projectors through dimension seven.
for n in range(1,8):
    for bits in itertools.product((0,1), repeat=n):
        d = sum(bits)
        if d == 0:
            continue
        check_projector(sp.diag(*bits),d,False)
        counts['coordinate_projectors'] += 1

# Exact dense proper complex projectors with a guaranteed independent basis.
for n in range(2,10):
    for d in sorted(set((1,n//2,n-1,n))):
        B = sp.zeros(n,d)
        for i in range(d):
            B[i,i]=1
        for i in range(d,n):
            for j in range(d):
                B[i,j]=rng.randint(-2,2)+I*rng.randint(-2,2)
        P = simp(B*(B.conjugate().T*B).inv()*B.conjugate().T)
        check_projector(P,d,True)
        counts['dense_complex_projectors'] += 1

# Explicit adaptive choices, response-based stopping, and a redundant query.
# These checks validate algebra on every branch; they do not estimate posterior laws.
n=8
first_values = [sp.Rational(0), sp.Rational(1,2), -sp.Rational(1,2),
                sp.Integer(2), sp.Integer(-2), 1+2*I, -1+2*I]
branch_counts={'early_stop':0, 'positive_branch':0, 'negative_branch':0}
for x0 in first_values:
    x=sp.Matrix([x0]+[sp.Integer(k-3)+I*sp.Integer(k%3-1) for k in range(1,n)])
    P=sp.eye(n)
    m=sp.zeros(n,1)
    rows=[]
    e0=sp.eye(n)[:,0]
    queries=[e0]
    query_index=0
    while query_index < len(queries):
        a=queries[query_index]
        y=(a.conjugate().T*x)[0]
        v=sp.simplify((a.conjugate().T*P*a)[0])
        rows.append(a.conjugate().T)
        if v == 0:
            assert sp.simplify(y-(a.conjugate().T*m)[0])==0
            counts['adaptive_redundant_queries'] += 1
        else:
            innovation=sp.simplify(y-(a.conjugate().T*m)[0])
            m=simp(m+P*a*innovation/v)
            P=simp(P-P*a*a.conjugate().T*P/v)
            counts['adaptive_positive_variance_queries'] += 1
        if query_index==0:
            if sp.simplify(y*sp.conjugate(y)) <= 1:
                branch_counts['early_stop'] += 1
            else:
                if sp.re(y) >= 0:
                    a2=sp.eye(n)[:,1]+I*sp.eye(n)[:,2]
                    branch_counts['positive_branch'] += 1
                else:
                    a2=sp.eye(n)[:,3]-I*sp.eye(n)[:,4]
                    branch_counts['negative_branch'] += 1
                queries.extend((a2,e0+a2))
        query_index+=1
    A=sp.Matrix.vstack(*rows)
    rank=A.rank()
    independent_rows=list(A.T.rref()[1])
    A0=A.extract(independent_rows,range(n))
    exact_m=simp(A0.conjugate().T*(A0*A0.conjugate().T).inv()*A0*x)
    assert zero(m-exact_m)
    exact_P=simp(sp.eye(n)-A0.conjugate().T*(A0*A0.conjugate().T).inv()*A0)
    assert zero(P-exact_P)
    assert zero(A*(x-m)) and zero(A*P)
    assert rank in (1,2) and n-rank >= sp.Rational(3,4)*n
    assert_projector(P,n-rank)
    # Rotate posterior by an exact unitary: two normalized 4-point DFT blocks.
    F4=sp.Matrix([[I**(-j*k)/2 for k in range(4)] for j in range(4)])
    U=sp.diag(F4,F4)
    assert zero(U*U.conjugate().T-sp.eye(n))
    Q=simp(U*P*U.conjugate().T)
    check_projector(Q,n-rank,True)
    counts['adaptive_paths'] += 1
assert all(branch_counts.values())

# Numerical scalar-disk check: 2|W-b|^2/v is noncentral chi-square(2).
max_disk_excess=0.0
max_centered_error=0.0
for v in (0.05,0.2,0.5,1.0,3.0):
    for r in (0.0,0.1,0.5,1.0,2.0,5.0):
        bound=-math.expm1(-r*r/v)
        for distance in (0.0,0.01,0.25,1.0,4.0,20.0):
            prob=float(ncx2.cdf(2*r*r/v,2,2*distance*distance/v))
            excess=prob-bound
            max_disk_excess=max(max_disk_excess,excess)
            assert excess <= 2e-14
            if distance==0:
                max_centered_error=max(max_centered_error,abs(prob-bound))
                assert abs(prob-bound) <= 2e-14
            counts['scalar_disk_cases'] += 1

# For coordinate projectors and a centered cube, exact probability is (1-e^-r^2)^d.
# Check formula (4), formula (5), and the weakened rank-fraction formula (6).
max_probability_bound_excess=0.0
for n in (1,2,3,8,32,128):
    for d in sorted(set((1,max(1,n//4),max(1,n//2),n))):
        for r in (0.05,0.2,0.5,1.0,2.0,4.0):
            actual=(-math.expm1(-r*r))**d
            product=math.prod(-math.expm1(-n*r*r/q) for q in range(1,d+1))
            half=(-math.expm1(-2*n*r*r/d))**((d+1)//2)
            exponential=math.exp(-d/2*math.exp(-2*n*r*r/d))
            delta=d/(2*n)
            weakened=math.exp(-delta*n/2*math.exp(-2*r*r/delta))
            values=(actual,product,half,exponential,weakened)
            for a,b in zip(values,values[1:]):
                max_probability_bound_excess=max(max_probability_bound_excess,a-b)
                assert a <= b+2e-14
            counts['coordinate_probability_bound_cases'] += 1

result={
    'status':'PASS',
    'purpose':'Fresh finite transcription controls; all-N proof is in REPORT.md.',
    'seed':SEED,
    'python':platform.python_version(),
    'sympy':sp.__version__,
    'scipy':scipy.__version__,
    'counts':counts,
    'adaptive_branch_counts':branch_counts,
    'numerical_diagnostics':{
        'max_scalar_disk_probability_minus_bound':max_disk_excess,
        'max_centered_scalar_disk_absolute_error':max_centered_error,
        'max_probability_chain_order_violation':max_probability_bound_excess,
    },
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'historical_programs_executed':False,
    'network_requests':False,
}
print(json.dumps(result,indent=2,sort_keys=True))
