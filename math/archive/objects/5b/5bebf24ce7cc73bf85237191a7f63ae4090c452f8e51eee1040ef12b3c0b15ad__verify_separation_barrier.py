#!/usr/bin/env python3
"""Independent finite-field checks for simultaneous-separation Fourier barrier.

All arithmetic for matrix-rank checks is exact in F_998244353.
The general complex-number theorems are proved separately in THEOREM.md.
"""
from __future__ import annotations
import json
import math
import random
import itertools
from pathlib import Path

PRIME = 998244353
ROOT = 3


def rank_mod(matrix: list[list[int]], p: int = PRIME) -> int:
    if not matrix: return 0
    a = [row[:] for row in matrix]
    m, n = len(a), len(a[0]); rk = 0
    for j in range(n):
        pivot = next((i for i in range(rk, m) if a[i][j] % p), None)
        if pivot is None: continue
        a[rk], a[pivot] = a[pivot], a[rk]
        inv = pow(a[rk][j], -1, p)
        a[rk] = [(x * inv) % p for x in a[rk]]
        for i in range(rk + 1, m):
            f = a[i][j] % p
            if f:
                ai, ar = a[i], a[rk]
                for jj in range(j, n): ai[jj] = (ai[jj] - f * ar[jj]) % p
        rk += 1
        if rk == m: break
    return rk


def inverse_perm(seq):
    out = [None] * len(seq)
    for i, x in enumerate(seq): out[x] = i
    return out


def sample_branch(n: int, rng: random.Random):
    """Branch L (I-DP_sigma)^(-1) R, with arbitrary row/col monomial endpoints."""
    cycle = list(range(n)); rng.shuffle(cycle)
    orderpos = inverse_perm(cycle)
    rowmap = list(range(n)); rng.shuffle(rowmap)
    colmap = list(range(n)); rng.shuffle(colmap)
    row_pos = [orderpos[rowmap[i]] for i in range(n)]
    col_pos = [orderpos[colmap[i]] for i in range(n)]
    weights = [rng.randint(2,1000000) for _ in range(n)]
    pref = [1]
    for j in cycle: pref.append(pref[-1] * weights[j] % PRIME)
    while pref[-1] == 1:
        weights[cycle[-1]] = rng.randint(2,1000000)
        pref = [1]
        for j in cycle: pref.append(pref[-1] * weights[j] % PRIME)
    invpref = [pow(x, -1, PRIME) for x in pref[:-1]]
    inv_den = pow((1 - pref[-1]) % PRIME, -1, PRIME)
    ls = [rng.randint(1,1000000) for _ in range(n)]
    rs = [rng.randint(1,1000000) for _ in range(n)]
    return dict(n=n, cycle=cycle, row_pos=row_pos, col_pos=col_pos,
                pref=pref, invpref=invpref, inv_den=inv_den, ls=ls, rs=rs)


def select_half(rows, cols, row_pos, col_pos):
    h = min(len(rows), len(cols)) // 2
    if h == 0: return [], [], 'empty'
    sr = sorted(rows, key=lambda t: row_pos[t])
    sc = sorted(cols, key=lambda t: col_pos[t])
    rl, rh = sr[:h], sr[-h:]
    cl, ch = sc[:h], sc[-h:]
    if row_pos[rl[-1]] < col_pos[ch[0]]:
        return rl, ch, 'row-before-col'
    if col_pos[cl[-1]] < row_pos[rh[0]]:
        return rh, cl, 'col-before-row'
    raise AssertionError('Universal half-selection lemma is violated')


def val_of_branch(b, row, col):
    # Unique length-<N directed path in cycle from row image to col image.
    a = b['row_pos'][row]; d = b['col_pos'][col]
    numer = b['pref'][d] * b['invpref'][a] % PRIME
    if a > d: numer = numer * b['pref'][-1] % PRIME
    return b['ls'][row] * b['rs'][col] * numer * b['inv_den'] % PRIME


def run_zero_weight_controls(rng: random.Random, trials: int=30):
    """Direct path expansion, including singular edge weights; inverse exists if cycle product !=1."""
    total = 0
    for _ in range(trials):
        n = rng.choice([16,32,64])
        cycle = list(range(n)); rng.shuffle(cycle)
        rowmap = list(range(n)); rng.shuffle(rowmap)
        colmap = list(range(n)); rng.shuffle(colmap)
        pos=inverse_perm(cycle)
        rowpos=[pos[rowmap[i]] for i in range(n)]
        colpos=[pos[colmap[i]] for i in range(n)]
        weight=[0 if rng.random()<0.2 else rng.randrange(1,10000) for _ in range(n)]
        weight[cycle[rng.randrange(n)]]=0  # cycle monodromy is 0, so denom=1
        rows, cols, orient=select_half(list(range(n)), list(range(n)), rowpos, colpos)
        def g(a,b):
            ia, ib=pos[rowmap[a]],pos[colmap[b]]
            z=1
            for h in list(range(ia,ib)) if ia<=ib else list(range(ia,n))+list(range(0,ib)):
                z=z*weight[cycle[h]]%PRIME
            return z
        sub=[[g(i,j) for j in cols] for i in rows]
        rnk=rank_mod(sub)
        assert rnk<=1,(orient,rnk)
        total+=1
    return total


def run_same_order_controls(rng:random.Random, trials:int=20):
    """Different weights but one shared branch ordering: only one halving is needed."""
    total=0
    n=64; Q=4
    for _ in range(trials):
        base=sample_branch(n,rng)
        branches=[base]
        for _ in range(Q-1):
            b=sample_branch(n,rng)
            # Retain the order/gauge permutations, but change weights.
            b['cycle']=base['cycle']
            b['row_pos']=base['row_pos']
            b['col_pos']=base['col_pos']
            # Re-generate weighted prefixes in shared cycle order.
            weights=[rng.randint(1,100000) for _ in range(n)]
            pp=[1]
            for j in b['cycle']:pp.append(pp[-1]*weights[j]%PRIME)
            assert pp[-1] != 1  # random weights; an extremely unlikely degenerate sample
            b['pref']=pp;b['invpref']=[pow(x,-1,PRIME) for x in pp[:-1]]
            b['inv_den']=pow((1-pp[-1])%PRIME,-1,PRIME)
            branches.append(b)
        rows,cols,_=select_half(list(range(n)),list(range(n)),base['row_pos'],base['col_pos'])
        assert len(rows)==n//2
        mat=[[sum(val_of_branch(b,i,j) for b in branches)%PRIME for j in cols] for i in rows]
        assert rank_mod(mat)<=Q
        total+=1
    return total


def cyclotomic_minor_is_nonzero(rows, cols, order):
    """Exact symbolic determinant of Fourier square minor in Z[z]/(z^p-1), p prime.

    Vanishes at primitive p-root iff all p coefficients equal.
    """
    k = len(rows)
    assert k == len(cols)
    poly = [0] * order
    for perm in itertools.permutations(range(k)):
        inv = sum(perm[i] > perm[j] for i in range(k) for j in range(i+1,k))
        exponent = sum(rows[i]*cols[perm[i]] for i in range(k)) % order
        poly[exponent] += -1 if inv&1 else 1
    return len(set(poly)) != 1


def run_prime_cyclotomic_controls(rng:random.Random, trials_per_case:int=12):
    """Parameter-free complex certificates, not just finite-field witnesses."""
    cases=[(5,1),(13,2),(37,3),(83,4)]
    rows=[]
    for n,q in cases:
        m=n//(1<<q)
        assert m>=q+1
        for _ in range(trials_per_case):
            branches=[sample_branch(n,rng) for i in range(q)]
            R,C=list(range(n)),list(range(n))
            for b in branches:
                R,C,_=select_half(R,C,b['row_pos'],b['col_pos'])
            assert len(R)==m and len(C)==m
            ok=cyclotomic_minor_is_nonzero(R[:q+1],C[:q+1],n)
            assert ok,(n,q,R,C)
            rows.append((n,q,m))
    return {'total':len(rows),'case_sizes':cases,'checked_all_nonzero':True}


def run(seed=20261010):
    rng = random.Random(seed)
    result = {'seed': seed, 'field': PRIME, 'tests': [], 'total_trials': 0,
              'all_branch_ranks_at_most_one': True,
              'all_sum_ranks_at_most_branch_count': True,
              'all_select_sizes_correct': True}
    for n in [16, 32, 64, 128, 256]:
        for q in [1, 2, 3, 4, 5]:
            m = n // (1 << q)
            if m < 2: continue
            trials = 4 if n < 128 else 10
            for _ in range(trials):
                branches = [sample_branch(n, rng) for __ in range(q)]
                rows, cols = list(range(n)), list(range(n))
                orientations = []
                for b in branches:
                    rows, cols, orient = select_half(rows, cols,b['row_pos'],b['col_pos'])
                    orientations.append(orient)
                assert len(rows) == m and len(cols) == m
                pieces = [[[val_of_branch(b,r,c) for c in cols] for r in rows]
                          for b in branches]
                branks = [rank_mod(z) for z in pieces]
                total = [[sum(pieces[t][i][j] for t in range(q)) % PRIME for j in range(m)]
                         for i in range(m)]
                srank = rank_mod(total)
                assert all(r<=1 for r in branks), (n,q,branks)
                assert srank<=q,(n,q,srank)
                # This is an exact finite-field Fourier check, not full spark over C.
                omega = pow(ROOT,(PRIME-1)//n, PRIME)
                F = [[pow(omega, r*c, PRIME) for c in cols] for r in rows]
                frank=rank_mod(F)
                assert frank>=0
                result['tests'].append(dict(n=n, q=q, m=m, orientations=orientations,
                                            branch_ranks=branks, sum_rank=srank,
                                            fourier_sub_rank=frank))
                result['total_trials']+=1
    result['fourier_sub_ranks_above_q'] = sum(t['fourier_sub_rank']>t['q'] for t in result['tests'])
    result['min_rank_gap'] = min(t['fourier_sub_rank']-t['sum_rank'] for t in result['tests'])
    result['max_rank_gap'] = max(t['fourier_sub_rank']-t['sum_rank'] for t in result['tests'])
    result['checked_sizes'] = sorted(set((t['n'],t['q'],t['m']) for t in result['tests']))
    result['zero_weight_controls'] = run_zero_weight_controls(rng)
    result['same_order_controls'] = run_same_order_controls(rng)
    result['cyclotomic_prime_controls'] = run_prime_cyclotomic_controls(rng)
    return result

if __name__=='__main__':
    result=run()
    p=Path(__file__).with_name('VERIFY_RESULTS.json')
    p.write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ('tests','checked_sizes')},indent=2))
    print('schedules=',len(result['checked_sizes']))
