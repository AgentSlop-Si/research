"""Fresh independent finite-field rank and full-vector certificates."""
import json
from itertools import combinations
from random import Random
from linear_inverse import MOD,ParityGreenInverse,apply_parity_mixed_fast,interleave_order
from grid_stage import apply_grid,transpose_order,grid_balanced_check,grid_edges,two_path_edges
from green_solver_standalone import tri_solve


def rank_mod(mat,p=MOD):
    if not mat:return 0
    a=[[x%p for x in row] for row in mat]
    n=len(a); m=len(a[0]); r=0
    for c in range(m):
        piv=next((i for i in range(r,n) if a[i][c]),None)
        if piv is None:continue
        a[r],a[piv]=a[piv],a[r]
        z=pow(a[r][c],-1,p)
        a[r]=[v*z%p for v in a[r]]
        for j in range(r+1,n):
            if a[j][c]:
                fac=a[j][c]
                a[j]=[(v-fac*w)%p for v,w in zip(a[j],a[r])]
        r+=1
        if r==n: break
    return r


def tridiagonal_green(n):
    cols=[tri_solve([int(i==j) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def permuted_sum(G,perm,eps):
    n=len(G)
    return [[(G[i][j]+eps*G[perm[i]][perm[j]])%MOD
             for j in range(n)] for i in range(n)]


def dense_apply(M,x):
    return [sum(v*a for v,a in zip(row,x))%MOD for row in M]


def verify_hidden_order(n):
    m=n//2
    sigma=list(range(0,n,2))+list(range(1,n,2))
    tau=interleave_order(n)
    G=tridiagonal_green(n)
    eps=pow(20,-1,MOD)
    M=[[ (G[sigma[i]][sigma[j]]+eps*G[i][j])%MOD
         for j in range(n)] for i in range(n)]
    QMQ=[[M[i][j] for j in tau] for i in tau]
    cuts=[rank_mod([row[k:] for row in QMQ[:k]]) for k in range(1,n)]
    assert max(cuts)<=4,(n,cuts)
    w=pow(3,(MOD-1)//n,MOD)
    F=[[pow(w,(i*j)%n,MOD) for j in tau] for i in tau]
    left=rank_mod([row[:m] for row in F[:m]])
    right=rank_mod([row[m:] for row in F[:m]])
    assert left==m and right==m,(n,left,right)
    return dict(n=n,hidden_max_cut_rank=max(cuts),hidden_mid_cut_rank=cuts[m-1],
                fourier_hidden_LL_rank=left,fourier_hidden_LR_rank=right)


def verify_inverse(n,rng):
    inverse=ParityGreenInverse(n)
    for _ in range(6):
        x=[rng.randrange(MOD) for j in range(n)]
        forward=apply_parity_mixed_fast(x)
        assert inverse.apply(forward)==x
        assert apply_parity_mixed_fast(inverse.apply(x))==x
    return dict(n=n, full_vectors_each_direction=6,exact=True)


def verify_grid(side,rng):
    n=side*side
    G=tridiagonal_green(n)
    perm=transpose_order(side)
    eps=pow(100,-1,MOD)
    M=permuted_sum(G,perm,eps)
    for _ in range(5):
        x=[rng.randrange(MOD) for _ in range(n)]
        assert dense_apply(M,x)==apply_grid(x,side)
    cuts=[]
    row_half=set(range(n//2))
    col_half={r*side+c for r in range(side) for c in range(side//2)}
    checker={r*side+c for r in range(side) for c in range(side) if (r+c)%2==0}
    for S in (row_half,col_half,checker,*[set(rng.sample(range(n),n//2)) for _ in range(4)]):
        check=grid_balanced_check(side,S)
        I=sorted(S)
        J=sorted(set(range(n))-S)
        check['cut_rank_mod']=rank_mod([[M[i][j] for j in J] for i in I])
        cuts.append(check)
    return dict(side=side,N=n,dense_executor_full_vector_tests=5,
                sampled_balanced_cuts=cuts)


def exhaustive_grid4():
    side=4;n=16
    hist={}
    minimal=10000
    for subset in combinations(range(n),n//2):
        x=grid_balanced_check(side,subset)
        k=x['grid_boundary']
        hist[k]=hist.get(k,0)+1
        minimal=min(minimal,k)
    assert minimal==side
    return dict(side=4, balanced_subsets=sum(hist.values()),min_grid_boundary=minimal,
                histogram={str(k):v for k,v in sorted(hist.items())})


def audit():
    rng=Random(20261009)
    data={'hidden_order':[verify_hidden_order(n) for n in (8,16,32,64)],
          'linear_inverse':[verify_inverse(n,rng) for n in (4,8,16,32,64,128,256)],
          'grid_stages':[verify_grid(side,rng) for side in (4,6,8)],
          'grid4_exhaustive':exhaustive_grid4()}
    return data

if __name__=='__main__':
    print(json.dumps(audit(),indent=2))
