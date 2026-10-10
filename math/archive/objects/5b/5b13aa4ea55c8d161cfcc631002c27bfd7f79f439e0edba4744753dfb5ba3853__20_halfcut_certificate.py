"""Exact two-stage half-cut rank barrier (finite-field audit, not the proof).

The universal result, independent of these samples, is in HALFCUT_THEOREM.md.
"""
import json
from random import Random
from minor_certificate import MOD, rank_mod, stage, cut_bound, permutation

ROOT=3


def fourier_rect(n, row_ids, col_ids, row_gain=None, col_gain=None):
    assert (MOD-1)%n==0
    w=pow(ROOT,(MOD-1)//n,MOD)
    assert pow(w,n,MOD)==1
    out=[]
    for i,row_id in enumerate(row_ids):
        u=[]
        for j,col_id in enumerate(col_ids):
            z=pow(w,row_id*col_id,MOD)
            if row_gain is not None: z=z*row_gain[i]%MOD
            if col_gain is not None: z=z*col_gain[j]%MOD
            u.append(z)
        out.append(u)
    return out


def halfcut_selection(pi):
    n=len(pi)
    m=n//2
    left=set(range(m)); right=set(range(n-m,n))
    c_left=sum(pi[k] in left for k in range(m))
    c_right=sum(pi[k] in right for k in range(m))
    assert c_left + c_right <= m
    return {'m':m, 'left':[0,m], 'right':[n-m,n],
            'c_left':c_left,'c_right':c_right}


def rectangle(A,B,pi,rows,cols,which_k,weights):
    out=[[0]*len(cols) for _ in rows]
    for k in which_k:
        rowb=B[pi[k]]
        dk=weights[k]
        for ii,i in enumerate(rows):
            a=A[i][k]*dk%MOD
            if a:
                for jj,j in enumerate(cols):
                    out[ii][jj]=(out[ii][jj]+a*rowb[j])%MOD
    return out


def add_mod(*matrices):
    return [[sum(M[i][j] for M in matrices)%MOD
            for j in range(len(matrices[0][0]))]
            for i in range(len(matrices[0]))]


def verify(n, r_left, r_right, shuf='random', seed=4032, weighted=True, 
           output_reordered=False, input_reordered=False):
    """A has r_left, B r_right, M=A P B. External relabelings individually optional.

    For a general arbitrary output + input permutation at the same time,
    consecutive Vandermonde minors are *not* assured; we exclude that case.
    """
    assert n%2==0 and (MOD-1)%n==0
    assert not (input_reordered and output_reordered)
    A=stage(n,r_left,seed+1)
    B=stage(n,r_right,seed+2)
    if n<=64:
        cut_bound(A,r_left)
        cut_bound(B,r_right)
    pi=permutation(n,shuf,seed)
    rng=Random(seed+5)
    weights=[rng.randrange(1,MOD) for _ in range(n)] if weighted else [1]*n
    if weighted: assert len(set(weights))>1
    halves=halfcut_selection(pi)
    m=n//2
    I=list(range(m))
    Klo=list(range(m)); Khi=list(range(m,n))
    rows = permutation(n,'random',seed+11)[:m] if output_reordered else I
    cols_order = permutation(n,'random',seed+12) if input_reordered else list(range(n))
    audits=[]
    for side,J in [('left',Klo),('right',Khi)]:
        inside=set(J)
        kin=[k for k in Klo if pi[k] in inside]
        kout=[k for k in Klo if pi[k] not in inside]
        parts=[
          rectangle(A,B,pi,I,J,Khi,weights),
          rectangle(A,B,pi,I,J,kout,weights),
          rectangle(A,B,pi,I,J,kin,weights)
        ]
        ranks=[rank_mod(part) for part in parts]
        c=len(kin)
        assert ranks[0]<=r_left, (ranks, r_left)
        assert ranks[1]<=r_right, (ranks, r_right)
        assert ranks[2]<=c, (ranks,c)
        M=add_mod(*parts)
        rankM=rank_mod(M)
        assert rankM<=r_left+r_right+c
        F=fourier_rect(n,rows,[cols_order[j] for j in J])
        rankF=rank_mod(F)
        assert rankF==m, ('Vandermonde minor failed',side,rankF)
        audits.append(dict(side=side, count_inside=c, component_ranks=ranks,
                     rank_composed=rankM, rank_fourier=rankF, upper_bound=r_left+r_right+c))
    assert audits[0]['count_inside']+audits[1]['count_inside']==m
    necessary = r_left+r_right>=m/2
    if not necessary:
        assert min(audits[0]['upper_bound'],audits[1]['upper_bound'])<m
        assert any(a['rank_composed'] < m for a in audits)
    return dict(N=n,r_left=r_left,r_right=r_right,shuffle=shuf,
                weighted=weighted, row_relabeling=output_reordered,
                col_relabeling=input_reordered, theoretical_rejection=not necessary,
                audits=audits)


def main():
    cases=[]
    for n,r in ((16,1),(32,2),(32,3),(64,2),(64,4),(128,4)):
        for shuf in ('identity','reverse','bitrev','random'):
            cases.append(verify(n,r,r,shuf))
    for n,r in ((16,1),(32,2),(64,3)):
        cases.append(verify(n,r,r,output_reordered=True))
        cases.append(verify(n,r,r,input_reordered=True))
    return cases


if __name__=='__main__':
    print(json.dumps(main(),indent=2))
