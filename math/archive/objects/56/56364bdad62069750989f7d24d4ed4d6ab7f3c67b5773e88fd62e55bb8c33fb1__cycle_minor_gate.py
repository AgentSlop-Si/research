"""Phase 12: exact Fourier-minor obstruction for sums of weighted-permutation Green inverses.

Self-contained Python standard library. This does NOT construct a faster FFT.
Represent a weighted-permutation Green inverse as (I-DP)^(-1), where
P is ANY permutation and D is arbitrary diagonal, including zero weights.
It is invertible iff 1-product(weights on each permutation cycle) != 0.

For prime p>=29, any two such resolvents have a 3x3 separated rectangle
on which their sum has rank<=2, while the complex p-DFT's minor is nonzero.
"""
from __future__ import annotations
import bisect
import itertools
import json
import math
import random
import functools
from typing import Sequence


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    k = 3
    while k * k <= n:
        if n % k == 0:
            return False
        k += 2
    return True


def longest_monotone_subsequence_positions(arr: Sequence[int]) -> tuple[list[int], str]:
    """Return indices in arr in longest strict increasing or decreasing subsequence."""
    def lis_indices(seq):
        tails = []
        tails_at = []
        parent = [-1] * len(seq)
        for i, val in enumerate(seq):
            loc = bisect.bisect_left(tails, val)
            if loc == len(tails):
                tails.append(val)
                tails_at.append(i)
            else:
                tails[loc] = val
                tails_at[loc] = i
            if loc > 0:
                parent[i] = tails_at[loc - 1]
        path = []
        if tails_at:
            k = tails_at[-1]
            while k >= 0:
                path.append(k)
                k = parent[k]
        return path[::-1]
    inc = lis_indices(arr)
    dec = lis_indices([-v for v in arr])
    if len(inc) >= len(dec):
        return inc, 'increasing'
    return dec, 'decreasing'


def find_rectangle(cycle_orders: Sequence[Sequence[int]], m: int) -> dict:
    """Extract R,C of size m, separated in all cycle orderings if available.

    Iterated Erdos-Szekeres. For r cycles existence is guaranteed when
    n > (2*m-1)**(2**(r-1)). Returns a proof witness otherwise may fail.
    """
    r = len(cycle_orders)
    if r < 1 or m < 1:
        raise ValueError('need >=1 cycle, m>=1')
    n = len(cycle_orders[0])
    assert all(len(x) == n and set(x) == set(range(n)) for x in cycle_orders)
    pos = [{v: i for i, v in enumerate(order)} for order in cycle_orders]
    subseq = list(cycle_orders[0])
    polarities = ['increasing']
    for k in range(1, r):
        arr = [pos[k][v] for v in subseq]
        idx, orientation = longest_monotone_subsequence_positions(arr)
        subseq = [subseq[i] for i in idx]
        polarities.append(orientation)
    if len(subseq) < 2*m:
        raise ValueError(f'only {len(subseq)} monotone elements; need {2*m}')
    rows = subseq[:m]
    cols = subseq[-m:]
    checks = []
    for j in range(r):
        rp = [pos[j][v] for v in rows]
        cp = [pos[j][v] for v in cols]
        relation = ('rows_before_cols' if max(rp) < min(cp) else
                    'cols_before_rows' if max(cp) < min(rp) else 'NOT_SEPARATED')
        if relation == 'NOT_SEPARATED':
            raise AssertionError('invalid separated rectangle')
        checks.append({'cycle':j, 'orientation':polarities[j],
                       'relation':relation,'row_positions':rp,'col_positions':cp})
    return {'n':n,'number_of_cycles':r,'minor_size':m,
            'subsequence_length':len(subseq),'rows':rows,'cols':cols,
            'checks':checks,
            'guaranteed_if_n_greater_than':(2*m-1)**(2**(r-1))}


def determinant_polynomial(p: int, rows: Sequence[int], cols: Sequence[int]) -> dict:
    """P(x)=det(x^(row_i*col_j)), exponents modulo p.

    At complex primitive p-root zeta, P(zeta)!=0 iff its p coefficients
    are not all identical, since Phi_p(x)=1+...+x^(p-1).
    This is an exact integer/cyclotomic certificate, no numerical tolerance.
    """
    assert is_prime(p) and len(rows)==len(cols) and len(set(rows))==len(rows)
    assert len(set(cols))==len(cols)
    n=len(rows)
    accum=[0]*p
    for perm in itertools.permutations(range(n)):
        exp=sum(rows[i]*cols[perm[i]] for i in range(n))%p
        inv=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        accum[exp] += -1 if inv%2 else 1
    nz={str(i):a for i,a in enumerate(accum) if a}
    return {'prime':p,'size':n,'rows':list(rows),'cols':list(cols),
            'terms_expanded': math.factorial(n),
            'nonzero_coefficients':nz,
            'cyclotomic_remainder_nonzero':len(set(accum))!=1,
            'proof':'For prime p, minimal polynomial of zeta_p is Phi_p=1+x+...+x^(p-1). Degree < p vanishes at zeta iff its coefficient vector is constant.'}




def find_sparse_avoiding_rectangle(cycle_orders:Sequence[Sequence[int]], m:int,
                                   row_support:Sequence[Sequence[int]],
                                   max_row_degree:int)->dict:
    """Extract separated m x m Fourier block where row-sparse S vanishes.

    Assumes each row of S has <= max_row_degree nonzeros. Guaranteed if
    n > (m*(max_row_degree+2)-1)**(2**(r-1)), r=#orders.
    """
    r=len(cycle_orders)
    n=len(cycle_orders[0])
    assert len(row_support)==n
    assert all(len(set(x))<=max_row_degree for x in row_support)
    positions=[{v:i for i,v in enumerate(order)} for order in cycle_orders]
    subseq=list(cycle_orders[0]); orientation=['increasing']
    for j in range(1,r):
        idx,sign=longest_monotone_subsequence_positions([positions[j][v] for v in subseq])
        subseq=[subseq[i] for i in idx]
        orientation.append(sign)
    needed=m*(max_row_degree+2)
    if len(subseq)<needed:
        raise ValueError(f'Only {len(subseq)} common monotone elements, need {needed}')
    rows=subseq[:m]
    forbidden=set().union(*(set(row_support[i]) for i in rows))
    choices=subseq[-m*(max_row_degree+1):]
    cols=[x for x in choices if x not in forbidden][:m]
    assert len(cols)==m
    assert all(j not in row_support[i] for i in rows for j in cols)
    checks=[]
    for j in range(r):
        rp=[positions[j][x] for x in rows]
        cp=[positions[j][x] for x in cols]
        relation=('rows_before_cols' if max(rp)<min(cp) else
                  'cols_before_rows' if max(cp)<min(rp) else 'NOT_SEPARATED')
        assert relation!='NOT_SEPARATED'
        checks.append({'cycle':j,'orientation':orientation[j],
                       'relation':relation,'row_positions':rp,'col_positions':cp})
    return {'n':n,'rows':rows,'cols':cols,'minor_size':m,
            'sparse_row_degree':max_row_degree,'subsequence_length':len(subseq),
            'forbidden_columns':sorted(forbidden),'checks':checks,
            'guaranteed_if_n_greater_than':(needed-1)**(2**(r-1))}


def permutation_cycles(pi: Sequence[int]) -> list[list[int]]:
    """Decompose ANY permutation into consistently ordered disjoint cycles."""
    n=len(pi)
    assert set(pi)==set(range(n))
    seen=set();result=[]
    for start in range(n):
        if start in seen: continue
        cur=start;cycle=[]
        while cur not in seen:
            seen.add(cur);cycle.append(cur);cur=pi[cur]
        assert cur==start
        result.append(cycle)
    return result


def linearize_perm(pi: Sequence[int]) -> list[int]:
    """Concatenate the disjoint cycles. The resolvent has off-cut rank <=1."""
    return [v for cycle in permutation_cycles(pi) for v in cycle]


def green_perm_submatrix(pi:Sequence[int], weights:Sequence[int], rows, cols, q:int):
    """Green inverse of I-diag(weights)*Permutation(pi) on chosen rows/cols.

    Distinct permutation cycles do not couple. Each nonzero entry equals
    a directed path product divided by 1 minus that cycle's total product.
    """
    cycles=permutation_cycles(pi)
    lookups={v:(cycle,index) for cycle in cycles for index,v in enumerate(cycle)}
    den={cycle[0]:(1-functools.reduce(lambda val,i:(val*weights[i])%q, cycle, 1))%q
         for cycle in cycles}
    if 0 in den.values():
        raise ValueError('singular Green inverse: some cycle product is 1')
    ret=[]
    for i in rows:
        cycle,k=lookups[i]
        first=cycle[0]
        inverse=pow(den[first],-1,q)
        row=[]
        for j in cols:
            other, jj=lookups[j]
            if other is not cycle:
                row.append(0);continue
            val=1;idx=k
            while idx != jj:
                val=val*weights[cycle[idx]]%q
                idx=(idx+1)%len(cycle)
            row.append(val*inverse%q)
        ret.append(row)
    return ret


def check_multi_green_inverse(pi, weights, q):
    n=len(pi)
    G=green_perm_submatrix(pi,weights,list(range(n)),list(range(n)),q)
    return all((G[i][j]-weights[i]*G[pi[i]][j])%q==int(i==j)
               for i in range(n) for j in range(n))


def permutation_from_ordered_cycles(cycles:Sequence[Sequence[int]])->list[int]:
    n=sum(len(c) for c in cycles)
    pi=[None]*n
    assert set(v for c in cycles for v in c)==set(range(n))
    for c in cycles:
        for k,v in enumerate(c):pi[v]=c[(k+1)%len(c)]
    return pi



def fourier_prime_factor_grid(n:int, p:int)->dict:
    """Find a p x p principal submatrix of F_n with primitive p- or p^2-root entries.

    For N=m*p^v, gcd(m,p)=1:
      v odd: a=m*p^((v-1)//2), F_N[ia,ja]=zeta_p^(mij)
      v even: a=m*p^(v//2-1), F_N[ia,ja]=zeta_(p^2)^(mij)
    for 0<=i,j<p. In both cases, all 3x3 minors are nonzero over C
    when p>=7 (proved by 6-term cyclotomic support).
    """
    assert is_prime(p) and n%p==0
    v=0;m=n
    while m%p==0:
        v+=1;m//=p
    if v%2:
        a=m*p**((v-1)//2)
        order=p
    else:
        a=m*p**(v//2-1)
        order=p*p
    S=[i*a for i in range(p)]
    assert len(set(S))==p and max(S)<n
    assert ((a*a*order)//n)==m and (a*a*order)%n==0
    return {'length':n, 'prime_factor':p,'valuation':v,'coprime_factor':m,
            'spacing':a, 'root_order':order,'frequency_multiplier':m,
            'indices':S}


def prime_power_three_minor(n:int, p:int, row_indices, col_indices)->dict:
    """Exact Z[primitive p or p^2 root] nonzero 3x3 determinant check."""
    grid=fourier_prime_factor_grid(n,p)
    assert len(row_indices)==len(col_indices)==3
    assert len(set(row_indices))==len(set(col_indices))==3
    assert all(0<=i<p for i in list(row_indices)+list(col_indices))
    root_order=grid['root_order'];m=grid['frequency_multiplier']
    coeff=[0]*root_order
    for perm in itertools.permutations(range(3)):
        e=sum(row_indices[i]*col_indices[perm[i]]*m for i in range(3))%root_order
        parity=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
        coeff[e] += (-1 if parity%2 else 1)
    if root_order==p:
        zero_at_root=len(set(coeff))==1
    else:
        assert root_order==p*p
        # If Q(zeta_(p^2))=0, Q(x)=R(x)*Phi_(p^2)(x),
        # deg R<p, so each residue class mod p has constant coefficients.
        zero_at_root=all(len({coeff[r+k*p] for k in range(p)})==1 for r in range(p))
    return {'length':n,'prime_factor':p,'root_order':root_order,
            'row_labels':list(row_indices),'col_labels':list(col_indices),
            'nonzero_coefficients':{str(i):v for i,v in enumerate(coeff) if v},
            'determinant_nonzero_over_complex':not zero_at_root,
            'proof':'Coefficient-pattern test against Phi_p or Phi_(p^2) in characteristic zero.'}


def composite_two_green_certificate(n:int, p:int, seed:int=0)->dict:
    """Certificate that two independently ordered weighted-permutation inverses
    cannot reproduce F_N when p>=29 is any prime divisor of N.
    No N x N matrix is allocated or needed.
    """
    if not is_prime(p) or p<29 or n%p!=0:
        raise ValueError('requires p>=29 prime dividing length n')
    rng=random.Random(seed)
    grid=fourier_prime_factor_grid(n,p)
    perms=[];orders=[]
    for _ in range(2):
        pi=list(range(n));rng.shuffle(pi)
        perms.append(pi)
        order=linearize_perm(pi)
        selected=set(grid['indices'])
        orders.append([i for i in order if i in selected])
    # Relabel the p chosen indices as 0..p-1 to reuse ES extractor.
    inv={val:i for i,val in enumerate(grid['indices'])}
    renumbered=[[inv[v] for v in order] for order in orders]
    rect=find_rectangle(renumbered,3)
    dft_minor=prime_power_three_minor(n,p,rect['rows'],rect['cols'])
    assert dft_minor['determinant_nonzero_over_complex']
    # Candidate resolvent ranks are structural and independent of the weights;
    # optional random exact-field witnesses can be checked separately.
    return {'theorem':'two weighted-permutation resolvents cannot equal F_N',
            'seed':seed,'grid':grid,'cycle_count_each':[len(permutation_cycles(pi)) for pi in perms],
            'relative_cycle_orders':renumbered,'rectangle':rect,
            'original_rows':[grid['indices'][i] for i in rect['rows']],
            'original_cols':[grid['indices'][j] for j in rect['cols']],
            'exact_fourier_minor':dft_minor,
            'notes':'Parametric obstruction applies to arbitrary weights, including zero weights, when both inverses exist.'}


def product_weights_except_wrap(order: Sequence[int], weights: Sequence[int], row: int, col: int, q: int) -> int:
    pos={v:i for i,v in enumerate(order)}
    i,j=pos[row],pos[col]
    value=1
    while i != j:
        value=value*weights[order[i]]%q
        i=(i+1)%len(order)
    return value


def green_submatrix(order,weights,rows,cols,q):
    c=functools.reduce(lambda v,w: (v*w)%q,weights,1)
    if c == 1:
        raise ValueError('singular Green inverse, product weights = 1')
    den=pow((1-c)%q,-1,q)
    return [[product_weights_except_wrap(order,weights,i,j,q)*den%q for j in cols] for i in rows]


def green_full_matrix(order,weights,q):
    return green_submatrix(order,weights,list(range(len(order))),list(range(len(order))),q)


def check_green_inverse(order,weights,q):
    n=len(order)
    pos={v:i for i,v in enumerate(order)}
    nxt={v:order[(pos[v]+1)%n] for v in order}
    G=green_full_matrix(order,weights,q)
    for i in range(n):
        for j in range(n):
            entry=(G[i][j]-weights[i]*G[nxt[i]][j])%q
            if entry != int(i==j):
                return False
    return True


def det_mod(A,q):
    a=[list(row) for row in A]
    n=len(a)
    assert all(len(row)==n for row in a)
    det=1
    for i in range(n):
        pivot=next((k for k in range(i,n) if a[k][i]%q),None)
        if pivot is None:
            return 0
        if pivot!=i:
            a[i],a[pivot]=a[pivot],a[i]
            det=-det
        x=a[i][i]%q
        det=det*x%q
        inv=pow(x,-1,q)
        for k in range(i+1,n):
            f=a[k][i]*inv%q
            if f:
                for j in range(i+1,n):
                    a[k][j]=(a[k][j]-f*a[i][j])%q
                a[k][i]=0
    return det%q


def rank_mod(A,q):
    a=[list(row) for row in A]
    if not a:return 0
    nr,nc=len(a),len(a[0]); ri=0
    for j in range(nc):
        i=next((i for i in range(ri,nr) if a[i][j]%q),None)
        if i is None:continue
        a[ri],a[i]=a[i],a[ri]
        inv=pow(a[ri][j]%q,-1,q)
        for ii in range(ri+1,nr):
            f=a[ii][j]*inv%q
            for jj in range(j,nc):
                a[ii][jj]=(a[ii][jj]-f*a[ri][jj])%q
        ri+=1
        if ri==nr:break
    return ri


def auxiliary_prime_root(p:int, rows,cols, minimum:int=100000):
    """Find an independently checked prime q, primitive p-root mod q,
    and nonzero modular Fourier determinant of the selected minor.
    We only use this to validate a sample; complex proof is cyclotomic.
    """
    assert is_prime(p)
    k= max(1,minimum//p)
    for _ in range(20000):
        q=k*p+1
        k+=1
        if not is_prime(q):continue
        root=next((pow(a,(q-1)//p,q) for a in range(2,30)
                   if pow(a,(q-1)//p,q)!=1),None)
        if root is None:continue
        f=[[pow(root,i*j,q) for j in cols] for i in rows]
        minor=det_mod(f,q)
        if minor!=0:
            return q,root,minor
    raise RuntimeError('could not find a suitable finite-field certificate')



def composite_field_witness(n:int,p:int,seed:int=0,minimum:int=100000)->dict:
    """Independent modular sample of composite-Fourier 3x3 minor versus
    two arbitrary invertible permutation Green inverses. This is an example,
    whereas the proof rules out EVERY choice of weights.
    """
    cert=composite_two_green_certificate(n,p,seed)
    rng=random.Random(seed)
    pi=[]
    for _ in range(2):
        perm=list(range(n));rng.shuffle(perm);pi.append(perm)
    grid=cert['grid']
    rows=cert['rectangle']['rows'];cols=cert['rectangle']['cols']
    order=grid['root_order'];m=grid['frequency_multiplier']
    threshold=max(minimum,order*10)
    q=None;root=None;dft_det=None
    k=max(1,threshold//order)
    for _ in range(20000):
        q_candidate=k*order+1;k+=1
        if not is_prime(q_candidate):continue
        z=next((v for a in range(2,40)
                 if (v:=pow(a,(q_candidate-1)//order,q_candidate))!=1
                 and (order==p or pow(v,p,q_candidate)!=1)),None)
        if z is None:continue
        F=[[pow(z,m*i*j,q_candidate) for j in cols] for i in rows]
        det=det_mod(F,q_candidate)
        if det:
            q=q_candidate;root=z;dft_det=det;break
    if q is None:raise RuntimeError('No finite field witness found')
    spatial_rows=cert['original_rows'];spatial_cols=cert['original_cols']
    mats=[];rank=[]
    for perm in pi:
        weights=[rng.randrange(q) for _ in range(n)]
        for cyc in permutation_cycles(perm):
            prod=functools.reduce(lambda v,i:(v*weights[i])%q,cyc,1)
            if prod==1:weights[cyc[0]]=0
        G=green_perm_submatrix(perm,weights,spatial_rows,spatial_cols,q)
        mats.append(G);rank.append(rank_mod(G,q))
    joined=[[(a+b)%q for a,b in zip(ra,rb)] for ra,rb in zip(mats[0],mats[1])]
    assert max(rank)<=1 and rank_mod(joined,q)<=2 and dft_det!=0
    cert['modular_sample']={
        'q':q,'root_order':order,'root':root,'prime_field_primitive_root_verified':
        pow(root,order,q)==1 and (order==p or pow(root,p,q)!=1),
        'dft_minor_det':dft_det,'green_block_ranks':rank,
        'sum_green_block_rank':rank_mod(joined,q),
        'green_blocks':mats,
        'semiseparability_check':'Each block has rank <=1 under independent random weights, independently permuted cycles; all Fourier outputs exact on the selected block.'}
    return cert


def generate_certificate(p:int, r:int=2, correction_rank:int=0, seed:int=0, test_green:bool=True):
    assert is_prime(p) and r>=2 and correction_rank>=0
    rng=random.Random(seed)
    orders=[]
    for _ in range(r):
        perm=list(range(p));rng.shuffle(perm)
        orders.append(perm)
    rect=find_rectangle(orders,r+correction_rank+1)
    rows,cols=rect['rows'],rect['cols']
    poly=determinant_polynomial(p,rows,cols)
    assert poly['cyclotomic_remainder_nonzero']
    q,root,dft_det=auxiliary_prime_root(p,rows,cols)
    data={'theorem':'single-layer sum of full-cycle weighted Green inverses',
          'prime_length':p,'summands':r,'allowed_extra_global_rank':correction_rank,
          'seed':seed,'cycle_orders':orders, 'rectangle':rect,
          'fourier_minor_cyclotomic':poly,
          'finite_field_sample':{'field_prime':q,'primitive_p_root':root,
                                 'dft_minor_det_nonzero':dft_det}}
    if test_green:
        green_samples=[];sum_matrix=[[0]*len(cols) for _ in rows]
        for order in orders:
            weights=[rng.randrange(q) for _ in range(p)]
            while functools.reduce(lambda v,w: (v*w)%q,weights,1)==1:
                weights=[rng.randrange(q) for _ in range(p)]
            gm=green_submatrix(order,weights,rows,cols,q)
            rank=rank_mod(gm,q)
            assert rank<=1, 'Green cross-cut should be rank<=1'
            for i in range(len(rows)):
                for j in range(len(cols)):
                    sum_matrix[i][j]=(sum_matrix[i][j]+gm[i][j])%q
            sample={'weights':weights, 'separated_block':gm,'rank':rank,
                    'full_inverse_identity_checked':p<=43 and check_green_inverse(order,weights,q)}
            green_samples.append(sample)
        actual_rank=rank_mod(sum_matrix,q)
        assert actual_rank<=r
        data['finite_field_sample'].update({'green_samples':green_samples,
                 'sum_block_rank':actual_rank, 'rank_upper_bound':r,
                 'dft_block_rank':len(rows)})
    return data


if __name__=='__main__':
    import argparse
    pa=argparse.ArgumentParser()
    pa.add_argument('--prime',type=int,default=29)
    pa.add_argument('--summands',type=int,default=2)
    pa.add_argument('--correction-rank',type=int,default=0)
    pa.add_argument('--seed',type=int,default=2026)
    pa.add_argument('--output',default='certificate.json')
    args=pa.parse_args()
    obj=generate_certificate(args.prime,args.summands,args.correction_rank,args.seed)
    with open(args.output,'w') as f:json.dump(obj,f,indent=2)
    print('Verified',obj['prime_length'],'rows=',obj['rectangle']['rows'],
          'cols=',obj['rectangle']['cols'],'sample rank=',
          obj['finite_field_sample'].get('sum_block_rank'),
          'Fourier determinant=',obj['finite_field_sample']['dft_minor_det_nonzero'])
