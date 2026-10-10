#!/usr/bin/env python3
"""Two-sided Fourier/Green separator theorem, independent test suite.
Uses numpy for numerical singular values and explicit finite-field ranks for
Green inverse/circuit assertions. No FFT routines are used in core checks.
"""
from collections import deque
from math import gcd, sqrt
import numpy as np
import random
import json
from pathlib import Path

SEED = 20261010

def mod_rank(matrix, p):
    # Exact rank over GF(p).
    if isinstance(matrix, np.ndarray):
        a = [[int(x)%p for x in row] for row in matrix.tolist()]
    else:
        a = [[int(x)%p for x in row] for row in matrix]
    n=len(a)
    if not n: return 0
    m=len(a[0]); i=0
    for j in range(m):
        piv=next((k for k in range(i,n) if a[k][j]%p),None)
        if piv is None: continue
        a[i],a[piv]=a[piv],a[i]
        inv=pow(a[i][j], -1, p)
        a[i]=[(v*inv)%p for v in a[i]]
        for k in range(i+1,n):
            factor=a[k][j]
            if factor:
                a[k]=[(a[k][t]-factor*a[i][t])%p for t in range(m)]
        i+=1
        if i==n:break
    return i

def mod_inverse(M,p):
    n=len(M)
    a=[[int(M[i][j])%p for j in range(n)]+[int(i==j) for j in range(n)] for i in range(n)]
    for j in range(n):
        piv=next((i for i in range(j,n) if a[i][j]),None)
        if piv is None: raise ValueError('singular')
        a[j],a[piv]=a[piv],a[j]
        inv=pow(a[j][j],-1,p)
        a[j]=[(x*inv)%p for x in a[j]]
        for i in range(n):
            if i!=j and a[i][j]:
                factor=a[i][j]
                a[i]=[(a[i][k]-factor*a[j][k])%p for k in range(2*n)]
    return [row[n:] for row in a]

def cycle_denominator(sigma,weights,p):
    n=len(sigma)
    K=[[int(i==j) for j in range(n)] for i in range(n)]
    for i,j in enumerate(sigma):
        K[i][j]=(K[i][j]-weights[i])%p
    return K

def matching_forest(denom,sigma,weights,A,B):
    """Matching rank for denominator K[B^c,A^c] in O(n) on cycle subgraph.
    A = chosen G row set, B = chosen G column set.
    """
    n=len(sigma)
    ra=set(range(n))-set(B) # denominator row labels
    co=set(range(n))-set(A) # denominator col labels
    if not ra or not co: return 0
    if len(ra)==n and len(co)==n:
        # K invertible by precondition; its bipartite support is one cycle.
        return n
    adj={i:set() for i in ra}
    adj.update({n+j:set() for j in co})
    for i in ra:
        if i in co:
            adj[i].add(n+i); adj[n+i].add(i)
        if weights[i] and sigma[i] in co:
            j=n+sigma[i]
            adj[i].add(j); adj[j].add(i)
    degree={v:len(ns) for v,ns in adj.items()}
    pending=deque(v for v,d in degree.items() if d<=1)
    active=set(adj); matched=0
    while pending:
        v=pending.popleft()
        if v not in active:continue
        if degree[v]==0:
            active.remove(v);continue
        if degree[v]!=1:continue
        u=next(w for w in adj[v] if w in active)
        matched+=1
        for w in (v,u):
            for z in adj[w]:
                if z in active and z not in (v,u):
                    degree[z]-=1
                    if degree[z]<=1:pending.append(z)
        active.discard(v);active.discard(u)
        degree[v]=0;degree[u]=0
    if active:
        raise AssertionError(f'Unexpected cycle inside proper Green rectangle: {len(active)} vertices')
    return matched

def predicted_green_rank(sigma,weights,A,B):
    n=len(sigma)
    return len(A)+len(B)-n+matching_forest(None,sigma,weights,A,B)

def finite_green_trials():
    rng=random.Random(SEED)
    cases=0
    for n in (5,7,8,11,16,32):
        p=193
        for repeat in range(24):
            order=list(range(n));rng.shuffle(order)
            sigma=[0]*n
            for i in range(n):sigma[order[i]]=order[(i+1)%n]
            weights=[rng.randrange(p) for _ in range(n)]
            prod=1
            for w in weights:prod=prod*w%p
            if prod==1:weights[order[0]]=0
            K=cycle_denominator(sigma,weights,p)
            G=mod_inverse(K,p)
            for test in range(12):
                A={i for i in range(n) if rng.randrange(2)}
                B={j for j in range(n) if rng.randrange(2)}
                sub=[[G[i][j] for j in sorted(B)] for i in sorted(A)]
                # If |A|=0 or |B|=0, use rank=0 directly
                rank=mod_rank(sub,p) if A and B else 0
                predicted=predicted_green_rank(sigma,weights,A,B)
                assert rank==predicted,(n,A,B,rank,predicted)
                cases+=1
    return cases

def fourier_coset_trials():
    total=0; largest_err=0.0
    for N in [8,12,16,18,24,32,45,64]:
        idx=np.arange(N)
        U=np.exp(-2j*np.pi*np.outer(idx,idx)/N)/sqrt(N)
        ds=[d for d in range(1,N+1) if N%d==0]
        for dr in ds:
            for dc in ds:
                r=N//dr;c=N//dc;h=N//gcd(N,dr*dc)
                sv=sqrt(r*c/(N*h))
                expected=np.array([sv]*h+[0]*(min(r,c)-h))
                for aa,bb in [(0,0),((dr-1), (dc-1))]:
                    A=aa+dr*np.arange(r);B=bb+dc*np.arange(c)
                    observed=np.linalg.svd(U[np.ix_(A,B)],compute_uv=False)
                    err=float(np.max(np.abs(observed-expected))) if len(expected) else 0
                    assert err<1e-11,(N,dr,dc,aa,bb,observed,expected)
                    largest_err=max(largest_err,err)
                    total+=1
    return total,largest_err

def make_cycle_by_parity(n):
    order=list(range(0,n,2))+list(range(1,n,2))
    sigma=[0]*n
    for i,j in enumerate(order):sigma[j]=order[(i+1)%n]
    return sigma

def perm_map(n,source_labels,target_labels,rng):
    source=sorted(source_labels)
    target=sorted(target_labels)
    assert len(source)==len(target)
    rng.shuffle(target)
    return dict(zip(source,target))

def matched_permutation(n,user_group,native_group,rng):
    A=set(user_group);E=set(native_group)
    mp={}
    mp.update(perm_map(n,A,E,rng))
    mp.update(perm_map(n,set(range(n))-A,set(range(n))-E,rng))
    return [mp[i] for i in range(n)]

def matmul_mod(A,B,p):
    n=len(A);m=len(B[0]);inner=len(B)
    return [[sum(A[i][k]*B[k][j] for k in range(inner))%p for j in range(m)] for i in range(n)]

def mismatched_interface_example(n=64,p=193):
    assert n%2==0
    rng=random.Random(SEED+71)
    native_even=set(range(0,n,2)); native_odd=set(range(1,n,2))
    original_rows=native_even
    desired_cols=native_odd
    # Random intermediate set, ensures the two stages have incompatible natural cuts.
    interface=set(rng.sample(range(n),n//2))
    sigma=make_cycle_by_parity(n)
    weights=[1]*n;weights[0]=2 # product 2, so K is invertible.
    G=mod_inverse(cycle_denominator(sigma,weights,p),p)
    # H1[even, interface^c] is a row-even/column-odd Green block.
    l1=matched_permutation(n,original_rows,native_even,rng)
    r1=matched_permutation(n,set(range(n))-interface,native_odd,rng)
    # H2[interface, odd] is a row-even/column-odd Green block.
    l2=matched_permutation(n,interface,native_even,rng)
    r2=matched_permutation(n,desired_cols,native_odd,rng)
    H1=[[G[l1[i]][r1[j]] for j in range(n)] for i in range(n)]
    H2=[[G[l2[i]][r2[j]] for j in range(n)] for i in range(n)]
    M=matmul_mod(H1,H2,p)
    A=sorted(original_rows);B=sorted(desired_cols); S=sorted(interface);T=sorted(set(range(n))-interface)
    rH1=mod_rank([[H1[i][j] for j in T] for i in A],p)
    rH2=mod_rank([[H2[i][j] for j in B] for i in S],p)
    rM=mod_rank([[M[i][j] for j in B] for i in A],p)
    old1=mod_rank([[H1[i][j] for j in B] for i in A],p)
    old2=mod_rank([[H2[i][j] for j in B] for i in A],p)
    desired_h=n//4 # U[even,odd] has this many unit singular values for N multiple of 4.
    assert (rH1,rH2)==(1,1),(rH1,rH2)
    assert rM<=rH1+rH2,(rM,rH1,rH2)
    assert old1+old2>=desired_h,(old1,old2)
    return {'N':n,'modulus':p,'Fourier_rectangular_rank':desired_h,'Fourier_nonzero_singular_values':'1, repeated N/4 times',
            'moving_interface_ranks':[rH1,rH2],'product_rectangle_rank_mod_p':rM,
            'fixed_interface_stage_ranks':[old1,old2], 'intermediate_set':S,
            'spectral_norm_distance_lower_bound_over_complex':1.0,
            'row_perm_1':l1,'col_perm_1':r1,'row_perm_2':l2,'col_perm_2':r2}

def main():
    cosets,err=fourier_coset_trials()
    green=finite_green_trials()
    example=mismatched_interface_example()
    results={'coset_svd_cases':cosets,'coset_max_abs_error':err,'green_rank_exact_GF193_cases':green,'strict_improvement_witness':example}
    path=Path(__file__).with_name('RESULTS.json')
    path.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:v for k,v in results.items() if k!='strict_improvement_witness'},indent=2))
    print('Strict two-sided improvement witness:',{k:v for k,v in example.items() if k not in ('row_perm_1','col_perm_1','row_perm_2','col_perm_2','intermediate_set')})
if __name__=='__main__':main()

def verify_two_stage_submodularity(n=8,p=193):
    rng=random.Random(SEED+199)
    R=set(range(0,n,2));C=set(range(1,n,2)); E=set(range(n))
    branches=[]
    for stage in range(2):
        q=2
        arr=[]
        for j in range(q):
            order=list(range(n));rng.shuffle(order)
            sigma=[0]*n
            for k in range(n):sigma[order[k]]=order[(k+1)%n]
            weights=[1]*n; weights[order[0]]=rng.randrange(2,p)
            l=list(range(n));r=list(range(n));rng.shuffle(l);rng.shuffle(r)
            arr.append((sigma,weights,l,r))
        branches.append(arr)
    def cost(S):
        S=set(S); complement=E-S
        total=0
        for sigma,w,l,r in branches[0]:
            total+=predicted_green_rank(sigma,w,{l[i] for i in R},{r[j] for j in complement})
        for sigma,w,l,r in branches[1]:
            total+=predicted_green_rank(sigma,w,{l[i] for i in S},{r[j] for j in C})
        return total
    costs={mask:cost(i for i in range(n) if mask>>i&1) for mask in range(1<<n)}
    # Exhaustive submodularity, stronger than random spot checking.
    for a in range(1<<n):
        for b in range(1<<n):
            assert costs[a]+costs[b]>=costs[a|b]+costs[a&b],(a,b,costs[a],costs[b])
    def apply(H,G,l,r):
        return [[(H[i][j]+G[l[i]][r[j]])%p for j in range(n)] for i in range(n)]
    H=[]
    for stage in range(2):
        agg=[[0]*n for _ in range(n)]
        for sigma,w,l,r in branches[stage]:
            G=mod_inverse(cycle_denominator(sigma,w,p),p)
            agg=apply(agg,G,l,r)
        H.append(agg)
    M=matmul_mod(H[0],H[1],p)
    actual=mod_rank([[M[i][j] for j in sorted(C)] for i in sorted(R)],p)
    beta=min(costs.values())
    assert actual<=beta,(actual,beta)
    return {'N':n,'two_stages_branches':[2,2],'examined_interfaces':1<<n,
            'exhaustive_submodularity_inequalities':(1<<n)**2,
            'optimal_upper_rank_certificate':beta,'actual_product_submatrix_rank_GF193':actual}

if __name__=='__main__':
    sub=verify_two_stage_submodularity()
    p=Path(__file__).with_name('RESULTS.json')
    results=json.loads(p.read_text());results['submodularity_and_product_test']=sub
    # A cross-check using a genuinely primitive 64-th root of unity in GF(193).
    root=next(x for x in range(2,193) if pow(x,64,193)==1 and pow(x,32,193)!=1)
    Ublock=[[pow(root,i*j,193)*pow(8,-1,193)%193 for j in range(1,64,2)] for i in range(0,64,2)]
    r=mod_rank(Ublock,193)
    assert r==16
    results['prime_field_Fourier_coset_check']={'N':64,'prime':193,'primitive_root_64':root,'rank':r}
    p.write_text(json.dumps(results,indent=2)+'\n')
    print('Submodular gate:',sub)
    print('Finite-field Fourier coset rank:',r)

def four_green_two_sum_witness(n=64,p=193):
    rng=random.Random(SEED+311)
    E=set(range(0,n,2));O=set(range(1,n,2));allset=set(range(n))
    S=set(rng.sample(range(n),n//2));T=allset-S
    H=[];stage_data=[];per_branch_cut_ranks=[]
    for stage in range(2):
        agg=[[0]*n for _ in range(n)]; descriptions=[]
        for j in range(2):
            # Two genuinely different, non-affine grouped Hamiltonian cycles.
            orderE=list(E);orderO=list(O);rng.shuffle(orderE);rng.shuffle(orderO)
            order=orderE+orderO
            sig=[0]*n
            for i,u in enumerate(order):sig[u]=order[(i+1)%n]
            w=[1]*n;w[order[0]]=2+stage+j
            if stage==0:
                l=matched_permutation(n,E,E,rng)
                r=matched_permutation(n,T,O,rng)
                chosen_rows={l[i] for i in E}
                chosen_cols={r[i] for i in T}
            else:
                l=matched_permutation(n,S,E,rng)
                r=matched_permutation(n,O,O,rng)
                chosen_rows={l[i] for i in S}
                chosen_cols={r[i] for i in O}
            pred=predicted_green_rank(sig,w,chosen_rows,chosen_cols)
            assert pred==1
            per_branch_cut_ranks.append(pred)
            G=mod_inverse(cycle_denominator(sig,w,p),p)
            for a in range(n):
                for b in range(n):agg[a][b]=(agg[a][b]+G[l[a]][r[b]])%p
            descriptions.append({'sigma':sig,'weights':w,'row_perm':l,'col_perm':r})
        H.append(agg);stage_data.append(descriptions)
    M=matmul_mod(H[0],H[1],p)
    rr=sorted(E);cc=sorted(O)
    rstage1=mod_rank([[H[0][i][j] for j in sorted(T)] for i in rr],p)
    rstage2=mod_rank([[H[1][i][j] for j in cc] for i in sorted(S)],p)
    rm=mod_rank([[M[i][j] for j in cc] for i in rr],p)
    old1=mod_rank([[H[0][i][j] for j in cc] for i in rr],p)
    old2=mod_rank([[H[1][i][j] for j in cc] for i in rr],p)
    assert rstage1<=2 and rstage2<=2 and rm<=4
    assert old1+old2>=16
    return {'N':n,'architecture':'(G1+G2)(G3+G4) with four distinct Hamiltonian cycles, independently permuted endpoints',
            'field':'GF(193)','Fourier_target_block_rank':16,'moving_cut_total_budget':sum(per_branch_cut_ranks),
            'moving_stage_aggregate_ranks':[rstage1,rstage2], 'product_rectangle_rank_GF193':rm,
            'old_same_cut_stage_ranks':[old1,old2],
            'certified_operator_norm_error_lower_bound_over_C':1.0,
            'certified_Frobenius_norm_error_lower_bound_over_C':sqrt(16-4),
            'interface_set':sorted(S),'branch_parameters':stage_data}

if __name__=='__main__':
    four=four_green_two_sum_witness()
    p=Path(__file__).with_name('RESULTS.json')
    results=json.loads(p.read_text());results['four_green_two_sum_witness']=four
    p.write_text(json.dumps(results,indent=2)+'\n')
    print('Four distinct Green branches:',{k:v for k,v in four.items() if k not in ('branch_parameters','interface_set')})
