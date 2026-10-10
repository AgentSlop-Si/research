"""Independent small exact controls for the Phase 22 second mathematical review.
No uploaded program and no first-review program is imported or executed.
"""
from pathlib import Path
import hashlib
import json
from math import comb
from random import Random

RNG = Random(221336)
COUNTS = dict(polynomial_coefficient_checks=0, spectral_identity_checks=0,
              recognized_structured_inputs=0, rejected_prefix_spoofs=0,
              rejected_offgrid_modes=0, reconstructed_n_bins=0,
              finite_field_union_count_checks=0)

def solve(A, b, p):
    n = len(b)
    A = [[v % p for v in row] + [b[i] % p] for i, row in enumerate(A)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if A[i][j]), None)
        if pivot is None:
            return None
        A[j], A[pivot] = A[pivot], A[j]
        inv = pow(A[j][j], -1, p)
        A[j] = [v * inv % p for v in A[j]]
        for i in range(n):
            if i != j:
                scale = A[i][j]
                A[i] = [(x - scale * y) % p for x, y in zip(A[i], A[j])]
    return [row[-1] for row in A]

def bm(s, p):
    # C[i] is the coefficient of s[n-i].
    C, B, L, gap, last = [1], [1], 0, 1, 1
    for n in range(len(s)):
        delta = (s[n] + sum(C[i] * s[n-i] for i in range(1, L+1))) % p
        if delta == 0:
            gap += 1
            continue
        old = C[:]
        scale = delta * pow(last, -1, p) % p
        if len(C) < len(B) + gap:
            C += [0] * (len(B) + gap - len(C))
        for j in range(len(B)):
            C[j+gap] = (C[j+gap] - scale*B[j]) % p
        if 2*L <= n:
            L, B, last, gap = n+1-L, old, delta, 1
        else:
            gap += 1
    return L, C[:L+1]

def eval_low(poly, z, p):
    acc = 0
    for c in reversed(poly):
        acc = (acc*z+c) % p
    return acc

def divide_linear(poly, u, p):
    d = len(poly)-1
    out = [0]*d
    out[-1] = poly[-1]
    for k in range(d-1, 0, -1):
        out[k-1] = (poly[k]+u*out[k]) % p
    assert (poly[0]+u*out[0]) % p == 0
    return out

def recognize(raw, h, eta, p, cap):
    n = len(raw)
    b = [v*pow(w, -1, p) % p for v, w in zip(raw, h)]
    order, C = bm(b[:2*cap], p)
    if order > cap:
        return None
    if order == 0:
        return [] if all(v == 0 for v in b) else None
    poly = list(reversed(C))
    modes = []
    for m in range(2*n):
        u = pow(eta, m, p)
        multiplicity = 0
        while len(poly) > 1 and eval_low(poly, u, p) == 0:
            poly = divide_linear(poly, u, p)
            multiplicity += 1
        if multiplicity:
            modes.append((m, multiplicity))
    if len(poly) != 1:
        return None
    cols = [(m, j) for m, r in modes for j in range(r)]
    amplitudes = solve([[pow(t,j,p)*pow(eta,m*t,p) % p for m,j in cols]
                        for t in range(order)], b[:order], p)
    if amplitudes is None:
        return None
    result = [(m,j,c) for (m,j),c in zip(cols,amplitudes)]
    predicted = [sum(c*pow(t,j,p)*pow(eta,m*t,p) for m,j,c in result) % p
                 for t in range(n)]
    return result if predicted == b else None

fields = [(3,7),(5,11),(7,29),(9,19),(11,23),(13,53),(15,31),(17,103),(21,43)]
for n,p in fields:
    eta = next(a for a in range(2,p)
               if pow(a,2*n,p)==1 and all(pow(a,j,p)!=1 for j in range(1,2*n)))
    q = pow(eta,8,p)
    h = []
    denominator = 1
    for t in range(n):
        if t:
            denominator = denominator*(1-pow(q,t,p)) % p
        h.append(pow(eta,2*t*t,p)*pow(denominator,-1,p) % p)
    cap = min(4,n//2)
    # Coefficientwise polynomial identities, including all interval locations.
    for a in range(n):
        for b in range(a+1,n+1):
            for j in range(4):
                coeff = [0]*(n+1)
                for t in range(a,b):
                    coeff[t] += pow(t,j,p)*h[t]*(1-pow(q,t,p))
                    coeff[t+1] -= pow(eta,2+4*t,p)*h[t]*pow(t+1,j,p)
                coeff[a] -= (1-pow(q,a,p))*h[a]*pow(a,j,p)
                coeff[b] += pow(eta,4*b-2,p)*h[b-1]*pow(b,j,p)
                assert all(c % p == 0 for c in coeff)
                COUNTS['polynomial_coefficient_checks'] += len(coeff)
            # Independent direct sums verify every coupling, no recurrence fill.
            jets = [[sum(pow(t,j,p)*h[t]*pow(eta,k*t,p) for t in range(a,b)) % p
                     for k in range(2*n)] for j in range(4)]
            for j in range(4):
                for k in range(2*n):
                    rhs = (jets[j][k] - pow(eta,k+2,p)*sum(comb(j,l)*jets[l][(k+4)%(2*n)]
                           for l in range(j+1)) - (1-pow(q,a,p))*h[a]*pow(a,j,p)*pow(eta,k*a,p)
                           + pow(eta,4*b-2,p)*h[b-1]*pow(b,j,p)*pow(eta,k*b,p)) % p
                    assert jets[j][(k+8)%(2*n)] == rhs
                    COUNTS['spectral_identity_checks'] += 1
    for _ in range(45):
        total = RNG.randint(1,cap)
        remaining = total
        orders = []
        while remaining:
            r = RNG.randint(1,remaining)
            orders.append(r)
            remaining -= r
        ms = RNG.sample(range(2*n),len(orders))
        expected = []
        for m,r in zip(ms,orders):
            cs = [RNG.randrange(p) for _ in range(r-1)] + [RNG.randrange(1,p)]
            expected.extend((m,j,c) for j,c in enumerate(cs))
        normalized = [sum(c*pow(t,j,p)*pow(eta,m*t,p) for m,j,c in expected) % p
                      for t in range(n)]
        raw = [b*w % p for b,w in zip(normalized,h)]
        got = recognize(raw,h,eta,p,cap)
        assert got is not None
        assert sorted(got) == sorted(expected)
        COUNTS['recognized_structured_inputs'] += 1
        for k in range(n):
            shifted = sum(c*sum(pow(t,j,p)*h[t]*pow(eta,(2*k+m)*t,p) for t in range(n))
                          for m,j,c in got) % p
            direct = sum(raw[t]*pow(eta,2*k*t,p) for t in range(n)) % p
            assert shifted == direct
            COUNTS['reconstructed_n_bins'] += 1
        spoof = raw[:]
        spoof[-1] = (spoof[-1]+1) % p
        assert recognize(spoof,h,eta,p,cap) is None
        COUNTS['rejected_prefix_spoofs'] += 1
    outside = next((u for u in range(1,p) if pow(u,2*n,p)!=1),None)
    if outside is not None:
        raw = [h[t]*pow(outside,t,p) % p for t in range(n)]
        assert recognize(raw,h,eta,p,cap) is None
        COUNTS['rejected_offgrid_modes'] += 1

# A concrete short-piece rejection in the specified greedy recognition design.
n,p,eta = 7,29,4
assert pow(eta,14,p)==1 and all(pow(eta,k,p)!=1 for k in range(1,14))
assert pow(2,14,p)==28
short_piece = dict(n=n, p=p, eta=eta, normalized_data=[1]+[2]*6,
                  interval_partition=[[0,1],[1,7]], per_piece_order=1,
                  first_two_sample_ratio=2,
                  ratio_is_on_grid=False,
                  result='The first two-sample order-one fit is off-grid, so the described greedy recognizer rejects.')

# Small exact union enumerations, coefficients optional order <=1.
from itertools import product
n,p,eta = 3,7,3
single = {tuple([0]*n)}
for m in range(2*n):
    for c in range(p):
        single.add(tuple(c*pow(eta,m*t,p) % p for t in range(n)))
bound_single = comb(2*n+1,1)*p
assert len(single) <= bound_single
COUNTS['finite_field_union_count_checks'] += 1
piecewise = set(single)
for cut in range(1,n):
    for m1,m2,c1,c2 in product(range(2*n),range(2*n),range(p),range(p)):
        piecewise.add(tuple((c1*pow(eta,m1*t,p) if t<cut else c2*pow(eta,m2*t,p)) % p
                            for t in range(n)))
bound_piecewise = sum(comb(n-1,j-1)*comb(2*n+1,1)**j*p**j for j in (1,2))
assert len(piecewise) <= bound_piecewise
COUNTS['finite_field_union_count_checks'] += 1

output = dict(status='passed', seed=221336, counts=COUNTS, fields=fields,
              short_piece_counterexample=short_piece,
              small_union_enumeration=dict(single_cardinality=len(single),
                                           single_unclipped_bound=bound_single,
                                           piecewise_cardinality=len(piecewise),
                                           piecewise_unclipped_bound=bound_piecewise),
              scope='Independent coefficient, direct-sum, BM/root-factor/amplitude/full-verification controls. No uploaded or first-review programs executed; no benchmark ledger reproduced.')
Path(__file__).with_name('SECOND_REVIEW_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
