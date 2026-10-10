"""Exact tests of a two-quasiseparable-stage rank obstruction.

A check of necessary matrix rank inequalities; does NOT synthesize an FFT.
All finite-field calculations are exact. Independent of earlier project modules.
"""
from __future__ import annotations
from dataclasses import dataclass
from random import Random

PRIMES = [(998244353, 3), (2013265921, 31)]


def rank(a, p):
    """Matrix rank by modular Gaussian elimination; rows are copied."""
    if not a:
        return 0
    m, n = len(a), len(a[0])
    assert all(len(v) == n for v in a)
    b = [[int(x) % p for x in row] for row in a]
    k = 0
    for col in range(n):
        pivot = next((j for j in range(k, m) if b[j][col]), None)
        if pivot is None: continue
        b[k], b[pivot] = b[pivot], b[k]
        inv = pow(b[k][col], p-2, p)
        b[k] = [v*inv % p for v in b[k]]
        for row in range(k+1, m):
            factor = b[row][col]
            if factor:
                b[row] = [(u-factor*v) % p for u, v in zip(b[row], b[k])]
        k += 1
        if k == m: break
    return k


def fourier(n, p=998244353, primitive_root=3):
    if (p-1) % n:
        raise ValueError('n must divide p-1')
    root = pow(primitive_root, (p-1)//n, p)
    if n > 1 and pow(root, n//2, p) == 1:
        raise ValueError('root not primitive')
    return [[pow(root, i*j, p) for j in range(n)] for i in range(n)]


def permute(a, row_order=None, col_order=None):
    n = len(a)
    row_order = list(range(n)) if row_order is None else row_order
    col_order = list(range(n)) if col_order is None else col_order
    return [[a[i][j] for j in col_order] for i in row_order]


def stage(n, r, p, rng):
    """A strict upper/lower generator stage with qsrank at most r."""
    dl = [rng.randrange(1, p) for _ in range(n)]
    low_i = [[rng.randrange(p) for _ in range(r)] for _ in range(n)]
    low_j = [[rng.randrange(p) for _ in range(r)] for _ in range(n)]
    up_i = [[rng.randrange(p) for _ in range(r)] for _ in range(n)]
    up_j = [[rng.randrange(p) for _ in range(r)] for _ in range(n)]
    return [[(dl[i] if i == j else
              sum(low_i[i][k]*low_j[j][k] for k in range(r)) if i > j else
              sum(up_i[i][k]*up_j[j][k] for k in range(r))) % p
             for j in range(n)] for i in range(n)]


def qsrank(a, p):
    n=len(a)
    return max([0]+[rank([row[c:] for row in a[:c]],p) for c in range(1,n)]+[rank([row[:c] for row in a[c:]],p) for c in range(1,n)])


def matmul(a, b, p):
    n=len(a); out=[[0]*n for _ in range(n)]
    for i in range(n):
        for k, v in enumerate(a[i]):
            if v:
                for j, w in enumerate(b[k]):
                    out[i][j]=(out[i][j]+v*w)%p
    return out


def middle_shuffle(a, order):
    """P A, output row i selected from old row order[i]."""
    return [a[j] for j in order]


def two_stage_bound(f, s1, s2, order, p):
    """For M=S2 P S1, prove both m-block ranks <= routed_capacity+r1+r2.

    Returns the same necessary bounds evaluated on f=actual product M.
    """
    n=len(f); assert n%2==0; m=n//2
    r1=qsrank(s1,p); r2=qsrank(s2,p)
    # S1's first/last m rows are routed into S2's first m columns.
    a=sum(order[i]<m for i in range(m))
    b=m-a
    f0=rank([row[:m] for row in f[:m]],p)
    f1=rank([row[m:] for row in f[:m]],p)
    assert f0<=a+r1+r2, (n,r1,r2,a,f0)
    assert f1<=b+r1+r2, (n,r1,r2,b,f1)
    return {'left_rank':f0,'right_rank':f1,'middle_left_capacity':a,'middle_right_capacity':b,
            'stage1_qsrank':r1,'stage2_qsrank':r2,
            'rank_surplus':f0+f1-m,
            'required_r1_plus_r2':max(0,(f0+f1-m+1)//2)}


def endpoint_certificate(f, p):
    """A generic necessary upper bound for two-stage sum of ranks.

    For arbitrary endpoint orders and cuts s,j, any two-stage factorization
    needs r1+r2 >= (rank(top_s, left_j) + rank(top_s,right_N-j) - s)/2.
    """
    n=len(f); winner=None
    for s in range(1,n):
        for j in range(1,n):
            left=rank([row[:j] for row in f[:s]],p)
            right=rank([row[j:] for row in f[:s]],p)
            score=left+right-s
            if winner is None or score > winner['surplus']:
                winner={'row_cut':s,'col_cut':j,'left_rank':left,'right_rank':right,
                        'surplus':score,'necessary_rank_sum':max(0,(score+1)//2)}
    return winner


def endpoint_patterns(n):
    bits=n.bit_length()-1
    return {
        'natural':list(range(n)),
        'parity':list(range(0,n,2))+list(range(1,n,2)),
        'bit_reversal':[int(f'{i:0{bits}b}'[::-1],2) for i in range(n)],
    }


def run():
    from pathlib import Path
    import json
    rng=Random(20261009)
    result={'theorem':'r1+r2 >= N/4 for F_N (even N), if one endpoint naturally ordered',
            'matrix_ranks':[],'shuffle_checks':[],'endpoint_orders':[]}
    for p,g in PRIMES:
        for n in (8,16,32,64):
            f=fourier(n,p,g); m=n//2
            a=rank([row[:m] for row in f[:m]],p)
            b=rank([row[m:] for row in f[:m]],p)
            assert a==b==m
            perm=list(range(n)); rng.shuffle(perm)
            a_row=rank([f[i][:m] for i in perm[:m]],p)
            b_row=rank([f[i][m:] for i in perm[:m]],p)
            assert a_row==b_row==m
            a_col=rank([[row[j] for j in perm[:m]] for row in f[:m]],p)
            b_col=rank([[row[j] for j in perm[m:]] for row in f[:m]],p)
            assert a_col==b_col==m
            result['matrix_ranks'].append({'p':p,'n':n,'quadrants':[a,b],
                'arbitrary_output_order':[a_row,b_row],'arbitrary_input_order':[a_col,b_col],
                'minimum_rank_sum':n//4,'minimum_equal_channel_rank':(n+7)//8})
            for reps in range(3):
                r1=min(4,1+reps);r2=min(4,1+reps)
                s1=stage(n,r1,p,rng);s2=stage(n,r2,p,rng)
                shuffle=list(range(n));rng.shuffle(shuffle)
                fnew=matmul(s2,middle_shuffle(s1,shuffle),p)
                cert=two_stage_bound(fnew,s1,s2,shuffle,p)
                assert cert['stage1_qsrank']<=r1 and cert['stage2_qsrank']<=r2
                result['shuffle_checks'].append({'p':p,'n':n,'r':r1,'cert':cert})
        for n in (8,16):
            f=fourier(n,p,g); patterns=endpoint_patterns(n)
            for ro in patterns:
                for co in patterns:
                    ff=permute(f,patterns[ro],patterns[co])
                    c=endpoint_certificate(ff,p)
                    result['endpoint_orders'].append({'p':p,'n':n,'rows':ro,'cols':co,'cert':c})
    path=Path(__file__).with_name('results.json');path.write_text(json.dumps(result,indent=2)+'\n')
    print(f"PASS: {len(result['matrix_ranks'])} Fourier/endpoint field certificates")
    print(f"PASS: {len(result['shuffle_checks'])} randomly shuffled generator products")
    print(f"PASS: {len(result['endpoint_orders'])} endpoint-order cut-budget scans")
    for r in result['matrix_ranks']:
        if r['p']==PRIMES[0][0]:print(f"N={r['n']}, r1+r2 >= {r['minimum_rank_sum']} and each channel rank >= {r['minimum_equal_channel_rank']}")
    for r in result['endpoint_orders']:
        if r['p']==PRIMES[0][0] and r['n']==16:
            print('endpoint16',r['rows'],r['cols'],r['cert']['surplus'],r['cert']['necessary_rank_sum'])
    return result

if __name__=='__main__':run()
