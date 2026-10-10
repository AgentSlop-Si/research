"""Independent test of Fourier rectangle optimization.

For n <= 6 enumerate ALL row/column subset rectangles, impose rank-1 by
modular 2x2 minors (not using phase7.rank_one_rectangle), solve exact-cover
MILP and compare to predicted n min_{d|n}(d+n/d). In addition run independent
field-arithmetic full transforms using direct reference for a broad list n.
"""
from __future__ import annotations
import json
import random
import time
from pathlib import Path
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix
from phase7 import test_field, divisors, optimal_tile_cost, one_pass_tiled_dft, shared_two_axis_dft


def independent_rankone(I,J,n):
    # Integer modulus identity is equivalent to a vanishing 2x2 Fourier minor.
    for a in I:
        for b in I:
            for c in J:
                for d in J:
                    if ((a-b)*(c-d))%n:
                        return False
    return True


def exact_cover_optimum(n):
    subsets=[tuple(k for k in range(n) if mask>>k&1) for mask in range(1,1<<n)]
    options=[]
    for I in subsets:
        for J in subsets:
            if independent_rankone(I,J,n):
                options.append((I,J))
    obj=[len(I)+len(J) for I,J in options]
    M=lil_matrix((n*n,len(options)),dtype=float)
    for idx,(I,J) in enumerate(options):
        for k in I:
            for j in J:
                M[k*n+j,idx]=1
    lin=LinearConstraint(M.tocsr(),[1]*(n*n),[1]*(n*n))
    result=milp(c=obj,integrality=[1]*len(options),bounds=Bounds(0,1),constraints=lin,
                options={'time_limit':80,'mip_rel_gap':0.0})
    if result.status != 0 or result.mip_gap > 1e-9:
        raise AssertionError((n,'not certified optimal',result.status,result.message, result.mip_gap))
    active=[idx for idx,v in enumerate(result.x) if v>=0.5]
    chosen=[options[idx] for idx in active]
    cost=round(result.fun)
    assert sum(len(I)+len(J) for I,J in chosen)==cost
    assert cost == optimal_tile_cost(n), (n,cost,optimal_tile_cost(n))
    assert len(active)>=n
    return {'n':n,'candidate_rectangles':len(options),'optimal_cost':cost,
            'analytical_cost':optimal_tile_cost(n),'selected_blocks':len(active),
            'solver_status':'global optimum (MILP optimality certificate)'}


def independent_direct(x,w,p):
    n=len(x); y=[]
    for k in range(n):
        a=0
        for j in range(n):
            a=(a+x[j]*pow(w,(-k*j)%n,p))%p
        y.append(a)
    return y


def audit():
    t0=time.monotonic()
    results={'exact_cover':[], 'independent_dft':[], 'two_axis':[],
             'status':'passed','description':'independent exhaustive rank-one exact cover and exact field DFT'}
    for n in range(2,7):
        results['exact_cover'].append(exact_cover_optimum(n))
    rng=random.Random(170017)
    coefficients=0
    for n in (2,3,4,5,6,7,8,9,10,12,15,16,18,20,21,24,25,27,28,30,32,36,40,48,49,60,63,64,72,81,96,100,120,128,144,180,196,225,256):
        p,w=test_field(n)
        passes=0
        for trial in range(2 if n <= 100 else 1):
            x=[rng.randrange(p) for _ in range(n)]
            actual,ledger=one_pass_tiled_dft(x,p,w)
            reference=independent_direct(x,w,p)
            assert actual==reference, (n,trial)
            assert ledger.muls==n*min(d+n//d for d in divisors(n))
            assert ledger.adds==ledger.muls-n
            passes+=1
            coefficients+=n
        results['independent_dft'].append({'n':n,'prime_field':p,'runs':passes,'multiplications':ledger.muls})
    for n in (4,8,16,32,64,128,256,512):
        p,w=test_field(n)
        x=[rng.randrange(p) for _ in range(n)]
        out,ledger=shared_two_axis_dft(x,p,w)
        assert out == independent_direct(x,w,p)
        assert ledger.butterflies==n*(n.bit_length()-1)//2
        results['two_axis'].append({'n':n,'butterflies':ledger.butterflies,
                                    'scalar_muls':ledger.muls,'root_muls':ledger.root_muls})
        coefficients+=n
    results['coefficients_independently_checked']=coefficients
    results['elapsed_seconds']=round(time.monotonic()-t0,3)
    return results


if __name__=='__main__':
    result=audit()
    path=Path(__file__).with_name('AUDIT_RESULTS.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:(len(v) if isinstance(v,list) else v) for k,v in result.items()}, indent=2))
    print('small-n MILP optima:',result['exact_cover'])
