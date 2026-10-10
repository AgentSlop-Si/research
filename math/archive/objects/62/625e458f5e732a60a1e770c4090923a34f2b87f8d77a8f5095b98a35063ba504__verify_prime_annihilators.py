"""Exact integer residue-count checks; no floating point or external code."""
from itertools import combinations
from math import comb
import json
from pathlib import Path

def coefficients(p, support):
    # Each coefficient is an integer combination of 1,zeta,...,zeta^(p-1).
    out = [[1]+[0]*(p-1)]
    for j in support:
        nxt = [[0]*p for _ in range(len(out)+1)]
        for degree, c in enumerate(out):
            for r, value in enumerate(c):
                nxt[degree][r] += value
                nxt[degree+1][(r+j)%p] -= value
        out = nxt
    return out

def is_zero(c):
    # For prime p, a degree < p integer polynomial vanishes at zeta_p
    # iff all p coefficients are equal (multiple of Phi_p).
    return len(set(c)) == 1

counts=[]
for p in [2,3,5,7,11,13]:
    sets=checks=0
    for k in range(1,p):
        assert all(comb(k,t)%p for t in range(k+1))
        for support in combinations(range(p),k):
            q=coefficients(p,support)
            assert not any(is_zero(c) for c in q)
            # The complement is independently among the subsets enumerated.
            sets += 1
            checks += len(q)
    counts.append(dict(prime=p,support_sets=sets,nonzero_coefficients=checks))
result={'arithmetic':'exact Python integers and prime cyclotomic relation',
        'scope':'All nonempty proper root subsets at the listed prime lengths; not a runtime lower bound.',
        'counts':counts,'total_support_sets':sum(r['support_sets'] for r in counts),
        'total_coefficients':sum(r['nonzero_coefficients'] for r in counts)}
Path(__file__).with_name('prime_annihilator_checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
