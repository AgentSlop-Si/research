"""Phase 17 quantitative operator-norm separation from every q-path Green sum.

The bound is proved without numerical computation; these numerical SVDs only
verify that its constants are conservative on explicit sampled partitions.
"""
import json
import math
import random
import numpy as np
from green_sum_cert import balanced_separation_witness


def universal_error_lower_bound(n:int,q:int,half_bandwidth:int=1)->float:
    m=n//(2**q)
    W=q*half_bandwidth
    if m<=W or m*m<=W*n:
        return 0.0
    return math.sqrt((m*m/n-W)/(m-W))


def instance_gap(n:int,q:int,seed:int):
    rng=random.Random(seed)
    orders=[list(range(n))]
    for _ in range(q-1):
        o=list(range(n));rng.shuffle(o);orders.append(o)
    rows,cols=balanced_separation_witness(orders)
    m=len(rows)
    W=q
    assert m>W and m*m>W*n
    # NOTE: the modular certificates and the analytic theorem do not depend
    # on these floating-point SVD checks.
    F=np.exp(-2j*np.pi*np.outer(rows,cols)/n)/math.sqrt(n)
    singular=np.linalg.svd(F,compute_uv=False)
    derived=math.sqrt((m*m/n-W)/(m-W))
    guaranteed=universal_error_lower_bound(n,q)
    actual=float(singular[W])
    assert derived<=actual+1e-10 and guaranteed<=derived+1e-10
    return {
        'n':n,'number_of_paths':q,'rectangle_dimension':m,
        'universal_analytic_error_lower_bound':guaranteed,
        'instance_analytic_error_lower_bound':derived,
        'actual_best_rank_q_spectral_approximation_error':actual,
        'F_submatrix_frobenius_sq':float(np.linalg.norm(F,'fro')**2),
        'fourier_submatrix_operator_norm':float(singular[0])
    }


def demo():
    result=[instance_gap(n,q,1709+n+q) for n,q in ((64,2),(128,2),(256,2),(256,3),(512,3))]
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':demo()
