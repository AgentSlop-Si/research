#!/usr/bin/env python3
"""Fresh bounded exact control; imports no source/research program.
Check p=5 single unit-bidiagonal chain with arbitrary complex nonzero links,
consecutive Fourier indices. Vanishing equations are linear in prefix coefficients.
"""
from itertools import combinations, permutations
from collections import Counter
import json, time
from pathlib import Path

P=5
ORDER=tuple(range(P))
PERMS={k:[(q,(-1)**sum(q[i]>q[j] for i in range(k) for j in range(i+1,k))) for q in permutations(range(k))] for k in range(1,P+1)}
def det(rows,cols):
    k=len(rows); v=[0]*P
    for q,sg in PERMS[k]:
        if all(cols[q[h]]<=rows[h][0] for h in range(k)):
            exp=sum(ORDER[cols[q[h]]]*rows[h][1] for h in range(k))%P
            v[exp]+=sg
    # Phi_5 is the only relation among 1,zeta,...,zeta^4 over Q.
    return tuple(v[i]-v[-1] for i in range(P-1))
def nz(a): return any(a)
def classify_kernel(rows):
    # Return rank and indices of coordinates identically zero on the kernel.
    for k in range(P-1,0,-1):
        for ri in combinations(range(P),k):
            rr=[rows[h] for h in ri]
            cs=list(combinations(range(P),k))
            vals={cc:det(rr,cc) for cc in cs}
            if not any(nz(v) for v in vals.values()): continue
            # rr has k independent rows. Other rows might increase rank;
            # outer decreasing loop already excluded larger rank.
            forced=[]
            for c in range(P):
                if not any(nz(v) for cc,v in vals.items() if c not in cc):
                    forced.append(c)
            return k,forced
    return 0,[]
def run_order():
    t=time.time(); cases=[]; stat=Counter()
    eqs=[(j,t) for j in range(1,P) for t in range(P)]
    for rows in combinations(eqs,P):
        stat['all_five_constraint_masks']+=1
        counts=Counter(j for j,t in rows)
        if any(counts[j]>j for j in range(1,P)):
            stat['excluded_by_degree']+=1; continue
        ss=set(rows)
        if any((j+1,t) in ss for j,t in rows):
            stat['excluded_by_nonzero_adjacent_coefficient']+=1; continue
        stat['admissible_masks_checked']+=1
        if nz(det(rows,tuple(range(P)))):
            stat['full_rank']+=1; continue
        rank,forced=classify_kernel(rows)
        stat['singular_rank_'+str(rank)]+=1
        if forced:
            stat['singular_forces_zero_coefficient']+=1
        else:
            stat['potential_nonzero_coefficient_kernel']+=1
            cases.append({'rows':rows,'rank':rank})
    out={'scope':'p=5, arbitrary-index single nonzero unit lower-bidiagonal chain; exact rational cyclotomic determinants', 'order':ORDER,'counts':dict(stat),'feasible_candidates':cases,'seconds':time.time()-t}
    return out
if __name__=='__main__':
    results=[]
    for tail in permutations(range(2,P)):
        ORDER=(0,1)+tail
        results.append(run_order())
    out={'affine_normalized_order_results':results}
    Path(__file__).with_name('FRESH_ALL_ORDERS_SEARCH.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
