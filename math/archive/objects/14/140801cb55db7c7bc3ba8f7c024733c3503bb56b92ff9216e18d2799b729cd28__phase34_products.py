"""Phase 34: exact finite-field audits of low-rank-corrected, noncommuting Green products.
Theorems and complexity limitations are recorded separately in THEOREM.md.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from random import Random
from phase33_two_sided import CyclicGreen, field_rank, inverse_small, root_of_unity, P1, GEN1, make_cycles


def matmul(A, B, p=P1):
    n=len(A);m=len(B[0]);k=len(B)
    out=[[0]*m for _ in range(n)]
    for i in range(n):
        row=out[i]
        for j in range(k):
            a=A[i][j]
            if a:
                for t in range(m):
                    row[t]=(row[t]+a*B[j][t])%p
    return out


def add(A,B,p=P1,sgn=1):
    return [[(x+sgn*y)%p for x,y in zip(row,other)] for row,other in zip(A,B)]


def diag(v,p=P1):
    n=len(v);return [[v[i]%p if i==j else 0 for j in range(n)] for i in range(n)]


def permutation_successor(cycle):
    n=len(cycle);nxt=[0]*n
    for j,now in enumerate(cycle):nxt[now]=cycle[(j+1)%n]
    return nxt


def permutation_rank_difference(s1,s2):
    """rank(P1-P2) = N - cycles(P1^-1 P2), any characteristic."""
    n=len(s1);assert sorted(s1)==sorted(s2)==list(range(n))
    inv=[0]*n
    for i,j in enumerate(s1):inv[j]=i
    nxt=[inv[s2[i]] for i in range(n)]
    visited=[False]*n;count=0
    for k in range(n):
        if visited[k]:continue
        count+=1;i=k
        while not visited[i]:visited[i]=True;i=nxt[i]
    return n-count, count


def swapped_cycle(cycle,a,b):
    assert a!=b
    return [b if x==a else a if x==b else x for x in cycle]


def green_matrix(cycle,alpha,p=P1):
    g=CyclicGreen(list(cycle),alpha,p)
    n=len(cycle)
    return [[g.entry(i,j) for j in range(n)] for i in range(n)]


def denominator_matrix(cycle,alpha,p=P1):
    n=len(cycle);succ=permutation_successor(cycle)
    out=[[0]*n for _ in range(n)]
    for j,i in enumerate(succ):
        out[j][j]=1
        out[i][j]=(out[i][j]-alpha)%p
    return out


def support_max(P):
    return max(sum(x!=0 for x in row) for row in P)


def Fourier(n,p=P1,primitive=GEN1):
    w=root_of_unity(n,p,primitive)
    return [[pow(w,(i*j)%n,p) for j in range(n)] for i in range(n)]


def minimum_rank_certificate_for_sparse_core(n,k,p=P1,primitive=GEN1,P=None):
    """Select consecutive Fourier rows, columns where arbitrary row-k-sparse P vanishes."""
    ell=n//(k+1)
    if ell<=0:return {'N':n,'row_sparsity':k,'guaranteed_rank':0}
    cols=list(range(n))
    if P is not None:
        assert support_max(P)<=k
        bad={j for i in range(ell) for j,x in enumerate(P[i]) if x}
        cols=[j for j in range(n) if j not in bad]
        assert len(cols)>=ell
    cols=cols[:ell]
    w=root_of_unity(n,p,primitive)
    V=[[pow(w,i*j,p) for j in cols] for i in range(ell)]
    got=field_rank(V,p)
    assert got==ell,(n,k,got)
    return {'N':n,'row_sparsity':k,'guaranteed_rank':ell,'witness_columns':cols,
            'witness_rank_mod_p':got}


def experiment(n,seed=340034,p=P1,primitive=GEN1):
    cycles=make_cycles(n,2,seed)
    a0,a1=cycles
    b0=swapped_cycle(a0,1,n//2+1)
    b1=swapped_cycle(a1,2,n//2+2)
    ka,_=permutation_rank_difference(permutation_successor(a0),permutation_successor(b0))
    kb,_=permutation_rank_difference(permutation_successor(a1),permutation_successor(b1))
    assert ka==kb==2,(n,ka,kb)
    alpha,beta=3,5
    GA,GB=green_matrix(a0,alpha,p),green_matrix(b0,alpha,p)
    GC,GD=green_matrix(a1,beta,p),green_matrix(b1,beta,p)
    A=add(GA,GB,p);C=add(GC,GD,p)
    AI,CI=inverse_small(A,p),inverse_small(C,p)
    B0,B1=denominator_matrix(a0,alpha,p),denominator_matrix(a1,beta,p)
    inv2=pow(2,p-2,p)
    sparseA=[[x*inv2%p for x in row] for row in B0]
    sparseC=[[x*inv2%p for x in row] for row in B1]
    rankA=field_rank(add(AI,sparseA,p,-1),p)
    rankC=field_rank(add(CI,sparseC,p,-1),p)
    assert rankA<=2 and rankC<=2,(rankA,rankC)
    rng=Random(seed+n)
    d=[rng.randrange(1,p) for _ in range(n)]
    dinv=[pow(z,p-2,p) for z in d]
    # M = C D A -> M^-1=A^-1 D^-1 C^-1.
    MI=matmul(matmul(AI,diag(dinv,p),p),CI,p)
    P=matmul(matmul(sparseA,diag(dinv,p),p),sparseC,p)
    rank_error=field_rank(add(MI,P,p,-1),p)
    assert rank_error<=4, (n,rank_error)
    assert support_max(P)<=4
    cert=minimum_rank_certificate_for_sparse_core(n,4,p,primitive,P)
    F=Fourier(n,p,primitive)
    # Fourier vs sparse core has provably rank >= ell, regardless of coefficients.
    delta=field_rank(add(F,P,p,-1),p)
    assert delta>=cert['guaranteed_rank']
    disproof=n//5>4
    if disproof:
        assert MI!=F
    # Independent far-ordering control; these cycles have O(N) mismatched edges.
    w0=permutation_successor(a0);w1=permutation_successor(a1)
    far,_=permutation_rank_difference(w0,w1)
    return {'N':n,'near_order_ranks':[ka,kb],
            'inverse_stage_correction_ranks':[rankA,rankC],
            'inverse_product_correction_rank':rank_error,
            'inverse_sparse_core_max_row_nnz':support_max(P),
            'fourier_minus_sparse_core_rank':delta,
            'vandermonde_lower_bound':cert['guaranteed_rank'],
            'fourier_excluded_by_bound':disproof,
            'independent_cycle_difference_rank':far,
            'vandermonde_witness':cert['witness_columns']}


def audit():
    output={'title':'Phase34 low-rank-corrected Green products', 'prime':P1}
    output['examples']=[experiment(n) for n in [8,16,32,64]]
    output['uniform_bounds']=[]
    for t in [2,3,4,5,6,8,10]:
        n=2**(t+5)
        k=2**t
        r=2*t
        output['uniform_bounds'].append({
            'N':n,'stages':t,'row_sparsity':k,'lowrank_budget':r,
            'Fourier_minus_sparse_rank_floor':n//(k+1),
            'exact_fourier_excluded':n//(k+1)>r
        })
    return output

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default='audit.json')
    args=parser.parse_args()
    report=audit()
    Path(args.output).write_text(json.dumps(report,indent=2))
    for e in report['examples']:
        print('N={} near={} inverse residual={} sparse k={} Fourier-rigidity floor={} far-order rank={}'.format(
            e['N'],e['near_order_ranks'],e['inverse_product_correction_rank'],
            e['inverse_sparse_core_max_row_nnz'],e['vandermonde_lower_bound'],
            e['independent_cycle_difference_rank']))
    print('wrote',args.output)
