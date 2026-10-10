"""Independent exact-field checks and experimental search for Phase 12.

Does not rely on test_phase12 or a numerical FFT library.
Search is NOT a proof of optimality outside the enumerated finite fields.
"""
import json
import random
import time
from collections import Counter
from math import isqrt
from itertools import combinations
from phase12 import (
    primitive_root_of_order, fourier,rank,inverse,matvec,
    stage_correction_network, green_commutator_audit,
    full_spark_audit,lower_rank_budget
)


def green_pair_matrix(n,q,alpha,beta):
    """Closed form for G_S G_T over a splitting finite field."""
    w=primitive_root_of_order(n,q)
    scale=pow((1-pow(alpha,n,q))%q,-1,q)
    return [[pow(alpha,(i-j)%n,q)*scale*pow((1-beta*pow(w,j,q))%q,-1,q)%q
             for j in range(n)] for i in range(n)]


def green_pair_sweep(n,q):
    F=fourier(n,q)
    allowed=[a for a in range(1,q) if pow(a,n,q)!=1]
    hist=Counter();minimum=n;argmin=[]
    for a in allowed:
        for b in allowed:
            C=green_pair_matrix(n,q,a,b)
            d=rank([[(F[i][j]-C[i][j])%q for j in range(n)] for i in range(n)],q)
            hist[d]+=1
            if d<minimum:
                minimum=d;argmin=[[a,b]]
            elif d==minimum and len(argmin)<12:
                argmin.append([a,b])
    return {'n':n,'field_prime':q,'parameter_pairs':len(allowed)**2,
            'min_rank_F_minus_pair':minimum,'rank_histogram':dict(sorted(hist.items())),
            'first_minimizers':argmin,'complex_prime_lower_bound_r':lower_rank_budget(n,2,prime=True)}


def enumerate_k_sparse(n,q,k):
    F=fourier(n,q)
    support_sizes=Counter();num=0
    # Restrict coefficients to all nonzero values for k<=2; finite exhaustive.
    from itertools import product
    for supp in combinations(range(n),k):
        for scalars in product(range(1,q),repeat=k):
            x=[0]*n
            for j,c in zip(supp,scalars):x[j]=c
            b=sum(v!=0 for v in matvec(F,x,q))
            num+=1; support_sizes[b]+=1
            assert k*b>=n,(n,q,k,b)
            if n in (3,5,7):assert k+b>=n+1,(n,q,k,b)
    return {'n':n,'q':q,'input_support':k,'vectors_enumerated':num,
            'min_fourier_support':min(support_sizes),'fourier_support_histogram':dict(sorted(support_sizes.items()))}


def audit():
    t0=time.time()
    spark=[{'n':n,'q':q,**full_spark_audit(n,q)} for n,q in [(3,7),(5,11),(7,29)]]
    pair_search=[green_pair_sweep(n,q) for n,q in [(3,7),(5,11),(7,29),(11,23)]]
    sparse=[enumerate_k_sparse(n,q,k) for n,q in [(5,11),(7,29),(8,17)] for k in (1,2)]
    tel=[stage_correction_network(n,q,L,r_each,seed=12+seed)
         for n,q in [(5,11),(7,29),(8,17),(16,97)]
         for L in [1,2,3] for r_each in [0,1,2] for seed in range(3)]
    assert all(x['rank_telescoping_valid'] and x['sparsity_valid'] for x in tel)
    comm=[green_commutator_audit(n,q,a,a) for n,q in [(3,7),(5,11),(7,29),(8,17),(16,97),(32,97)]
          for a in [next(a for a in range(2,q) if pow(a,n,q)!=1)]]
    assert all(x['commutator_rank']==x['n'] and x['qcommutation_residual'] and x['inverse_identity'] for x in comm)
    bounds=[]
    for n in (127,257,1024,65536,1048576):
        for layers in (1,2,3,4):
            s=2**layers
            lb=lower_rank_budget(n,s,prime=(n in (127,257)))
            if n in (127,257): assert (s+1)*(lb+1)>=n+1
            else: assert s*(lb+1)**2>=n
            bounds.append({'N':n,'L':layers,'inverse_column_sparsity_cap':s,
                           'necessary_rank_correction_at_least':lb,
                           'prime_additive_bound':n in (127,257)})
    elapsed=time.time()-t0
    return {'status':'passed','audit_type':'finite_field_exact_plus_char_zero_theory',
            'full_spark_certificates':spark,'green_pair_exhaustive_small_field':pair_search,
            'sparse_uncertainty_exhaustive_small_field':sparse,
            'perturbed_networks_checked':len(tel),'perturbed_network_examples':tel[:6],
            'max_inverse_rank_correction_budget':max(x['rank_budget'] for x in tel),
            'max_observed_inverse_difference_rank':max(x['inverse_difference_rank'] for x in tel),
            'full_rank_weyl_green_commutators_checked':len(comm),
            'rank_lower_bound_examples':bounds,
            'elapsed_seconds':round(elapsed,3),
            'limitations':[
              'Theoretical uncertainty bounds apply to complex Fourier matrices; finite-field additive inequality is used only after exhaustive full-spark certification for n<=7.',
              'Parameter sweeps certify only the listed small fields and Green-pair ansatz, not global optimality.',
              'An inverse rank bound is not an unrestricted arithmetic lower bound or a universal DFT solution.',
            ]}

if __name__=='__main__':
    out=audit()
    with open('AUDIT_RESULTS.json','w') as f:json.dump(out,f,indent=2)
    print('Status:',out['status'])
    print('Full-spark:',out['full_spark_certificates'])
    print('Green-pair minima:',[(a['n'],a['min_rank_F_minus_pair'],a['complex_prime_lower_bound_r']) for a in out['green_pair_exhaustive_small_field']])
    print('Stage-network samples:',out['perturbed_networks_checked'])
    print('Full-rank Green commutators:',out['full_rank_weyl_green_commutators_checked'])
    print('Sparse input enumerations:',sum(a['vectors_enumerated'] for a in out['sparse_uncertainty_exhaustive_small_field']))
    print('Seconds:',out['elapsed_seconds'])
