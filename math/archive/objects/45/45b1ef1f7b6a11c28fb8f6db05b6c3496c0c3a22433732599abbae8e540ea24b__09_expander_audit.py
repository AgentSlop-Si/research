"""Independent numeric and exact finite-field checks for random-path stage."""
import json
from random import Random
import numpy as np
from expander_stage import random_order,apply_two_path,path_union_edges,union_bound_failure
from exact_audit import tridiagonal_green,permuted_sum,dense_apply
from linear_inverse import MOD


def laplacian_lambda2(n,paths):
    L=np.zeros((n,n))
    for path in paths:
        for i,j in path:
            L[i,i]+=1;L[j,j]+=1
            L[i,j]-=1;L[j,i]-=1
    e=np.linalg.eigvalsh(L)
    return float(e[1])


def run():
    rng=Random(20261009)
    results=[]
    for n in (32,64,128,256):
        order=random_order(n,seed=20261009+n)
        paths=path_union_edges(order)
        lam=laplacian_lambda2(n,paths)
        exp_cert=lam*n/4
        cut_samples=[]
        for i in range(16):
            S=set(rng.sample(range(n),n//2))
            counts=[sum((u in S)!=(v in S) for u,v in path) for path in paths]
            cut_samples.append(sum(counts))
        assert min(cut_samples)>=n/16
        if n<=64:
            g=tridiagonal_green(n)
            eps=pow(100,-1,MOD)
            M=permuted_sum(g,order,eps)
            for _ in range(3):
                x=[rng.randrange(MOD) for _ in range(n)]
                assert dense_apply(M,x)==apply_two_path(x,order)
        # Prove all balanced cuts via numeric spectral bound for this sample if lambda2>=1/4;
        # otherwise the universal probabilistic theorem still applies, but this sample
        # is NOT treated as certified by this audit.
        results.append(dict(n=n,lambda2=lam,
                            spectral_balanced_edge_bound=exp_cert,
                            meets_spectral_n_over_16=lam>=.25,
                            min_of_16_random_balanced_cuts=min(cut_samples),
                            probability_theorem_failure_upper=union_bound_failure(n),
                            modular_full_vector_tests=(3 if n<=64 else 0)))
    return results

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
