"""Phase34 experiments: sparse phase patches, three-stage products, rank-distant controls."""
from phase34_products import (
    add, matmul, diag, permutation_successor, permutation_rank_difference,
    green_matrix, denominator_matrix, swapped_cycle, support_max,
    minimum_rank_certificate_for_sparse_core
)
from phase33_two_sided import (
    make_cycles, CyclicGreen, inverse_small, field_rank, root_of_unity, P1, GEN1
)
from random import Random


def build_patched_stage(cycle,alpha,n,stage_index,p=P1):
    modified=swapped_cycle(cycle,1+stage_index,n//2+1+stage_index)
    rank_cycle,_=permutation_rank_difference(permutation_successor(cycle),permutation_successor(modified))
    assert rank_cycle==2
    GA=green_matrix(cycle,alpha,p)
    GB=green_matrix(modified,alpha,p)
    L=[1]*n; R=[1]*n
    L[(3+stage_index)%n]=7+stage_index
    R[(7+stage_index)%n]=11+stage_index
    GB_patched=[[(L[i]*GB[i][j]*R[j])%p for j in range(n)] for i in range(n)]
    S=add(GA,GB_patched,p)
    Sinv=inverse_small(S,p)
    B=denominator_matrix(cycle,alpha,p)
    inv2=pow(2,p-2,p)
    baseline=[[v*inv2%p for v in row] for row in B]
    r=field_rank(add(Sinv,baseline,p,-1),p)
    assert r<=4
    return Sinv,baseline,r,rank_cycle


def patched_two_stage(n=64,p=P1):
    cycles=make_cycles(n,2,seed=341234)
    a,p0,r0,k0=build_patched_stage(cycles[0],3,n,0,p)
    b,p1,r1,k1=build_patched_stage(cycles[1],5,n,1,p)
    rng=Random(n+54)
    d=[rng.randrange(1,p) for _ in range(n)]
    dinv=diag([pow(z,p-2,p) for z in d],p)
    MI=matmul(matmul(a,dinv,p),b,p)
    P=matmul(matmul(p0,dinv,p),p1,p)
    r=field_rank(add(MI,P,p,-1),p)
    assert r<=r0+r1<=8
    cert=minimum_rank_certificate_for_sparse_core(n,4,p,GEN1,P)
    return {'N':n,'stage_rank_budgets':[r0,r1],
            'inverse_correction_rank':r,'baseline_row_sparsity':support_max(P),
            'Fourier_rigidity_rank_floor':cert['guaranteed_rank'],
            'excluded_exact_fourier': cert['guaranteed_rank']>r0+r1,
            'patched_edges_per_stage': [k0,k1],
            'patched_phase_entries_per_stage':2}


def three_stage(n=64,p=P1):
    cycles=make_cycles(n,3,seed=342234)
    mats=[];sparse=[];ranks=[]
    for s,cyc in enumerate(cycles):
        mod=swapped_cycle(cyc,1+s,n//2+1+s)
        ga=green_matrix(cyc,3+2*s,p);gb=green_matrix(mod,3+2*s,p)
        S=add(ga,gb,p)
        Sinv=inverse_small(S,p)
        B=denominator_matrix(cyc,3+2*s,p)
        baseline=[[v*pow(2,p-2,p)%p for v in row] for row in B]
        r=field_rank(add(Sinv,baseline,p,-1),p)
        assert r<=2
        mats.append(Sinv);sparse.append(baseline);ranks.append(r)
    d1=diag([2+i for i in range(n)],p)
    d2=diag([100+i for i in range(n)],p)
    # inverse product with arbitrary invertible diagonal gauges
    mi=matmul(matmul(matmul(matmul(mats[0],d1,p),mats[1],p),d2,p),mats[2],p)
    core=matmul(matmul(matmul(matmul(sparse[0],d1,p),sparse[1],p),d2,p),sparse[2],p)
    residual=field_rank(add(mi,core,p,-1),p)
    assert residual<=sum(ranks)
    cert=minimum_rank_certificate_for_sparse_core(n,8,p,GEN1,core)
    return {'N':n,'stages':3,'correction_rank':residual,
            'rank_budget':sum(ranks),'sparse_core_row_nnz':support_max(core),
            'Fourier_rigidity_rank_floor':cert['guaranteed_rank'],
            'excluded_exact_fourier':cert['guaranteed_rank']>sum(ranks)}


def _add_vectors(a,b,p=P1):return [(x+y)%p for x,y in zip(a,b)]

def far_cycle_control(n=64,seed=343334,p=P1):
    cycles=make_cycles(n,4,seed=seed)
    ds=[]
    for i in range(2):
        ka,_=permutation_rank_difference(permutation_successor(cycles[2*i]),
                                          permutation_successor(cycles[2*i+1]))
        ds.append(ka)
    greens=[CyclicGreen(cyc,a,p) for i,cyc in enumerate(cycles) for a in [3 if i<2 else 5]]
    w=root_of_unity(n,p,GEN1)
    mid=[pow(w,(i*i)%n,p) for i in range(n)]
    def apply(x):
        z=_add_vectors(greens[0].apply(x),greens[1].apply(x),p)
        y=[z[i]*mid[i]%p for i in range(n)]
        return _add_vectors(greens[2].apply(y),greens[3].apply(y),p)
    rng=Random(113+n);x=[rng.randrange(1,p) for _ in range(n)]
    # Z e_j=e_{j+1}; D[i]=w^i, and FZ=DF
    Zx=[x[(i-1)%n] for i in range(n)]
    Dx=[x[i]*pow(w,i,p)%p for i in range(n)]
    mx=apply(x); mzx=apply(Zx); mdx=apply(Dx)
    first=[(mzx[i]-pow(w,i,p)*mx[i])%p for i in range(n)]
    second=[(mdx[i]-mx[(i+1)%n])%p for i in range(n)]
    assert any(first) and any(second)
    return {'N':n,'independent_order_cycle_deficits':ds,
            'first_Weyl_defect_nonzero':sum(bool(a) for a in first),
            'second_Weyl_defect_nonzero':sum(bool(a) for a in second),
            'online_stage_green_solves':4,'online_arithmetic': 'O(N)'}

if __name__=='__main__':
    import json
    report={'phase_patches':patched_two_stage(64),
            'three_stage':three_stage(64),
            'rank_distant_controls':[far_cycle_control(n) for n in (32,64,256)]}
    print(json.dumps(report,indent=2))
