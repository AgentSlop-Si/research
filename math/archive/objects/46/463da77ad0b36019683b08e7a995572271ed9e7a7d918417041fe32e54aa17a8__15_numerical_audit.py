"""Optional floating-point sanity check; exact claims are in the paper/proof."""
import json
from random import Random
import numpy as np
from scipy.linalg import solve_banded
from grid_stage import transpose_order,grid_edges,crossing_count


def build_G(n):
    band=np.zeros((3,n))
    band[0,1:]=-1
    band[1,:]=3
    band[2,:-1]=-1
    return solve_banded((1,1),band,np.eye(n))


def run(Ls=(4,8,16), seed=8426):
    rng=Random(seed)
    results=[]
    for L in Ls:
        n=L*L
        perm=transpose_order(L)
        G=build_G(n)
        M=G+.01*G[np.ix_(perm,perm)]
        eigen=np.linalg.eigvalsh(M)
        cuts=[]
        cases={
          'top-half-rows':set(range(n//2)),
          'left-half-columns':{r*L+c for r in range(L) for c in range(L//2)},
          'checkerboard':{r*L+c for r in range(L) for c in range(L) if (r+c)%2==0},
          'random1':set(rng.sample(range(n),n//2)),
          'random2':set(rng.sample(range(n),n//2)),
        }
        for name,S in cases.items():
            I=np.array(sorted(S))
            J=np.array(sorted(set(range(n))-S))
            s=np.linalg.svd(M[np.ix_(I,J)],compute_uv=False)
            k=int(np.count_nonzero(s>=1/2500 - 1e-12))
            assert k >= L//15, (L,name,k)
            cuts.append(dict(cut=name,grid_edge_boundary=crossing_count(grid_edges(L),S),
                             singular_values_ge_1_over_2500=k,
                             sigma_max=float(s[0]),
                             sigma_smallest=float(s[-1])))
        results.append(dict(L=L,N=n,kappa2=float(eigen[-1]/eigen[0]),
                            cuts=cuts,meets_theorem=True))
    return results

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
