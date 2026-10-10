"""Rigorous all-(lambda,mu) N=4 Green Fourier exclusion via homogeneous Macaulay rank.

For every possible row/column permutation, homogenize the 2x2 projective
cross-ratio constraints to ternary quadrics f_ij(lambda,mu,nu). Every
compatible complex parameter [lambda:mu:nu] is a common projective zero.
If the degree-four multiples of the f_ij span *all* degree-four ternary
polynomials, no projective zero exists. Full modular rank lifts to characteristic
zero by a nonvanishing 15x15 minor. Uses no heuristic or numerical fitting.
"""
from __future__ import annotations
from itertools import permutations
import json
from phase29_two_parameter import build_family,P,SEEDS


def monomials(deg):
    return [(a,b,deg-a-b) for a in range(deg+1) for b in range(deg-a+1)]

DEG2=monomials(2);DEG4=monomials(4)
POS4={m:k for k,m in enumerate(DEG4)}

def product_linear(v,w):
    """Variables x=lambda, y=mu, z=nu in that order."""
    result={}
    for i in range(3):
        for j in range(3):
            e=[0,0,0];e[i]+=1;e[j]+=1;e=tuple(e)
            result[e]=(result.get(e,0)+v[i]*w[j])%P
    return result

def triple(g0,g1,g2,i,j):
    return [g1[i][j],g2[i][j],g0[i][j]]

def quadratic(target,g0,g1,g2,rows,cols,i,j):
    """Necessary cross-ratio Tij*T00*Mi0*M0j - Ti0*T0j*Mij*M00 = 0."""
    r=rows;c=cols
    a=target[i][j]*target[0][0]%P
    b=target[i][0]*target[0][j]%P
    first=product_linear(triple(g0,g1,g2,r[i],c[0]),triple(g0,g1,g2,r[0],c[j]))
    second=product_linear(triple(g0,g1,g2,r[i],c[j]),triple(g0,g1,g2,r[0],c[0]))
    return {e:(a*first.get(e,0)-b*second.get(e,0))%P for e in DEG2}

def coefficient_rows(target,g0,g1,g2,rows,cols):
    n=len(target)
    result=[]
    labels=[]
    for i in range(1,n):
        for j in range(1,n):
            q=quadratic(target,g0,g1,g2,rows,cols,i,j)
            for multiplier in DEG2:
                row=[0]*len(DEG4)
                for e,value in q.items():
                    dest=tuple(e[k]+multiplier[k] for k in range(3))
                    row[POS4[dest]]=value
                result.append(row)
                labels.append((i,j,multiplier))
    return result,labels

def rank_and_pivots(rows):
    """Independent standard Gaussian elimination over F_p; pivot original rows."""
    work=[r[:] for r in rows]
    idx=list(range(len(work)))
    nr=len(work);nc=len(work[0]); rank=0
    selected=[]
    for col in range(nc):
        pivot=next((r for r in range(rank,nr) if work[r][col]),None)
        if pivot is None: continue
        work[rank],work[pivot]=work[pivot],work[rank]
        idx[rank],idx[pivot]=idx[pivot],idx[rank]
        selected.append(idx[rank])
        iv=pow(work[rank][col],-1,P)
        work[rank]=[v*iv%P for v in work[rank]]
        for r in range(rank+1,nr):
            factor=work[r][col]
            if factor:
                work[r]=[(x-factor*y)%P for x,y in zip(work[r],work[rank])]
        rank+=1
        if rank==nc:break
    return rank, selected


def determinant_modp(square):
    """Independent determinant calculation for a 15-by-15 witness."""
    n=len(square)
    if any(len(r)!=n for r in square):raise ValueError('not square')
    a=[r[:] for r in square]
    out=1
    for col in range(n):
        pivot=next((r for r in range(col,n) if a[r][col]),None)
        if pivot is None:return 0
        if pivot!=col:
            a[pivot],a[col]=a[col],a[pivot]
            out=-out%P
        val=a[col][col]
        out=out*val%P
        iv=pow(val,-1,P)
        for r in range(col+1,n):
            if a[r][col]:
                fac=a[r][col]*iv%P
                for j in range(col+1,n):
                    a[r][j]=(a[r][j]-fac*a[col][j])%P
                a[r][col]=0
    return out


def all_permutations_audit(n=4,seed=None,positive=False):
    seed=SEEDS[n] if seed is None else seed
    target,g0,g1,g2=build_family(n,seed)
    if positive:
        # Ensure there is an actual projective zero at [lambda:mu:nu]=[2:3:1]
        target=[[ (g0[i][j]+2*g1[i][j]+3*g2[i][j])%P
                   for j in range(n)] for i in range(n)]
    ranks={};minrank=15;failed=[];pivots={}
    for rows in permutations(range(n)):
        for cols in permutations(range(n)):
            m,_=coefficient_rows(target,g0,g1,g2,rows,cols)
            rank,selected=rank_and_pivots(m)
            minrank=min(minrank,rank)
            key=''.join(str(i) for i in rows)+'/'+''.join(str(j) for j in cols)
            ranks[key]=rank
            if rank<15:failed.append(key)
            elif not positive:
                determinant=determinant_modp([m[idx] for idx in selected])
                assert determinant,('bad pivot witness',key)
                pivots[key]={'selected_rows':selected,'determinant_modp':determinant}
    return {'n':n,'seed':seed,'prime':P,'projective_degree':4,
            'variables':['lambda','mu','nu'],'monomials_degree_four':len(DEG4),
            'total_permutation_pairs':len(ranks),'min_rank':minrank,
            'full_rank_cases':sum(v==15 for v in ranks.values()),
            'failed_pairs':failed,'positive_control':positive,
            'pivot_witnesses':pivots if not positive else {},
            'rank_histogram':{str(r):sum(v==r for v in ranks.values()) for r in set(ranks.values())}}

if __name__=='__main__':
    import time
    start=time.time()
    a=all_permutations_audit()
    print('negative',time.time()-start,{k:v for k,v in a.items() if k not in ('pivot_witnesses','failed_pairs')})
    b=all_permutations_audit(positive=True)
    print('positive',time.time()-start,{k:v for k,v in b.items() if k not in ('pivot_witnesses','failed_pairs')})
    if a['full_rank_cases']==a['total_permutation_pairs']:
       with open(f'certificates/degree4_all_permutations_N4_p{P}.json','w') as f:json.dump(a,f,indent=1)


def verify_saved_audit(cert):
    assert cert['prime']==P and cert['n']==4 and cert['full_rank_cases']==576
    target,g0,g1,g2=build_family(4,cert['seed'])
    for key, witness in cert['pivot_witnesses'].items():
        rs,cs=key.split('/')
        rows,cols=tuple(map(int,rs)),tuple(map(int,cs))
        m,_=coefficient_rows(target,g0,g1,g2,rows,cols)
        minor=[m[k] for k in witness['selected_rows']]
        d=determinant_modp(minor)
        assert d==witness['determinant_modp'] and d!=0
    return True


def partial_anchor_rows(target,g0,g1,g2,source_rows,source_cols,target_rows=(0,1,2),target_cols=(0,1,2)):
    """Degree-four certificate for a 3x3 anchored submatrix.

    source_rows/source_cols are distinct triples, not necessarily completions
    to full permutations; each full monomial equivalence induces one such map.
    """
    result=[]
    for i in (1,2):
        for j in (1,2):
            # Cross ratio uses the selected target rows/cols, while the source
            # indices can be in an arbitrary order.
            a=target[target_rows[i]][target_cols[j]]*target[target_rows[0]][target_cols[0]]%P
            b=target[target_rows[i]][target_cols[0]]*target[target_rows[0]][target_cols[j]]%P
            one=product_linear(triple(g0,g1,g2,source_rows[i],source_cols[0]),
                               triple(g0,g1,g2,source_rows[0],source_cols[j]))
            two=product_linear(triple(g0,g1,g2,source_rows[i],source_cols[j]),
                               triple(g0,g1,g2,source_rows[0],source_cols[0]))
            q={e:(a*one.get(e,0)-b*two.get(e,0))%P for e in DEG2}
            for mul in DEG2:
                row=[0]*len(DEG4)
                for e,val in q.items():
                    row[POS4[tuple(e[t]+mul[t] for t in range(3))]]=val
                result.append(row)
    return result

def random_partial_trial(n=8,samples=1000,seed=12345):
    from random import Random
    rng=Random(seed)
    t,g0,g1,g2=build_family(n,SEEDS[n])
    rank_hist={}
    for k in range(samples):
        rs=tuple(rng.sample(range(n),3));cs=tuple(rng.sample(range(n),3))
        rank,_=rank_and_pivots(partial_anchor_rows(t,g0,g1,g2,rs,cs))
        rank_hist[rank]=rank_hist.get(rank,0)+1
    return rank_hist


def exhaustive_anchor_audit(n=8,seed=None,save_witnesses=32):
    import hashlib
    seed=SEEDS[n] if seed is None else seed
    t,g0,g1,g2=build_family(n,seed)
    triples=list(permutations(range(n),3))
    hist={};failures=[];total=0;h=hashlib.sha256();sample=[]
    for r in triples:
        for c in triples:
            rows=partial_anchor_rows(t,g0,g1,g2,r,c)
            rank,pivot=rank_and_pivots(rows)
            hist[rank]=hist.get(rank,0)+1
            total+=1
            if rank!=15:
                failures.append({'source_rows':list(r),'source_cols':list(c),'rank':rank})
            else:
                if total<=save_witnesses:
                    det=determinant_modp([rows[k] for k in pivot])
                    assert det
                    sample.append({'source_rows':list(r),'source_cols':list(c),
                                   'selected_rows':pivot,'determinant_modp':det})
            h.update(bytes((rank,)))
    return {'n':n,'seed':seed,'prime':P,'anchored_target_rows':[0,1,2],
            'anchored_target_cols':[0,1,2],
            'source_ordered_triples_each_axis':len(triples),
            'tested_partial_mapping_pairs':total,'degree_four_basis_dim':15,
            'rank_histogram':{str(k):v for k,v in sorted(hist.items())},
            'failures':failures,'rank_stream_sha256':h.hexdigest(),
            'sample_nonzero_minors':sample}
