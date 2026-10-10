"""Rectangular Fourier phase-obstruction certificates for five independently ordered Green terms.

Everything is modulo 998244353; any *full-rank* modular Macaulay witness
lifts to characteristic zero for the precise rational/cyclotomic input family.
No numerical fitting is involved.
"""
from __future__ import annotations
from pathlib import Path
from itertools import combinations, permutations
from random import Random
import sys, struct

ROOT = Path(__file__).resolve().parent
# Include self-contained vendored reference modules shipped with this checkpoint.
sys.path.insert(0,str(ROOT))
from phase30_four_parameter import build_four, SEEDS, P
from phase30_dimension_gate import fifth_green, lifted_general, monomials
from phase30_macaulay import rank_pivots, determinant_modp

ROW_PAIRS = tuple(combinations(range(3),2))
COL_PAIRS = tuple(combinations(range(4),2))
ALL_PAIRS = tuple((i,ip,j,jp) for i,ip in ROW_PAIRS for j,jp in COL_PAIRS)
# Drop one adjacent-column minor: the remaining 8 suffice on seeded instances.
FAST_PAIRS = tuple(pair for pair in ALL_PAIRS
                   if pair[3] == pair[2]+1 and pair!=(1,2,2,3))
assert len(FAST_PAIRS)==8


def family(n:int, seed:int|None=None):
    seed=SEEDS.get(n,2800+n) if seed is None else seed
    target,g4=build_four(n,seed)
    g5=fifth_green(n,seed*3+11)
    return target,(*g4,g5)


def rectangular_quadrics(target, gens, src_rows, src_cols,
                         target_rows=None,target_cols=None, pairs=FAST_PAIRS):
    q=len(gens)
    nr=len(src_rows);nc=len(src_cols)
    if target_rows is None:target_rows=tuple(range(nr))
    if target_cols is None:target_cols=tuple(range(nc))
    assert nr==3 and nc==4 and q==5
    assert len(target_rows)==nr and len(target_cols)==nc
    exp2=monomials(2,q);index={e:i for i,e in enumerate(exp2)}
    coeff=[[[gens[k][src_rows[i]][src_cols[j]] for k in range(q)]
            for j in range(nc)] for i in range(nr)]
    ans=[]
    for i,ip,j,jp in pairs:
        a=target[target_rows[i]][target_cols[jp]]*target[target_rows[ip]][target_cols[j]]%P
        b=target[target_rows[i]][target_cols[j]]*target[target_rows[ip]][target_cols[jp]]%P
        quad=[0]*len(exp2)
        for k in range(q):
            for l in range(q):
                e=[0]*q;e[k]+=1;e[l]+=1
                z=index[tuple(e)]
                quad[z]=(quad[z]+a*coeff[i][j][k]*coeff[ip][jp][l]
                              -b*coeff[i][jp][k]*coeff[ip][j][l])%P
        ans.append(quad)
    return ans


def certificate(target,gens,src_rows,src_cols,pairs=FAST_PAIRS):
    quad=rectangular_quadrics(target,gens,src_rows,src_cols,pairs=pairs)
    lifted=lifted_general(quad,5,3)
    rank,pivots=rank_pivots(lifted)
    det=determinant_modp([lifted[k] for k in pivots]) if rank==35 else None
    return rank,det,pivots


def export_input(filename:Path,n:int,seed:int|None=None,plant=False):
    t,g=family(n,seed)
    info=None
    if plant:
        rng=Random(310031+n)
        rs=list(range(n));cs=list(range(n))
        rng.shuffle(rs);rng.shuffle(cs)
        left=[rng.randrange(1,P) for _ in range(n)]
        right=[rng.randrange(1,P) for _ in range(n)]
        vals=[1,2,3,4,5]
        b=[[sum(vals[k]*g[k][i][j] for k in range(5))%P for j in range(n)] for i in range(n)]
        t=[[left[i]*b[rs[i]][cs[j]]*right[j]%P for j in range(n)] for i in range(n)]
        assert all(v!=0 for row in t for v in row)
        info={'rows':rs,'cols':cs,'coefficients':vals}
    with filename.open('wb') as fh:
        fh.write(struct.pack('<II',P,n))
        for mat in [t,*g]:
            fh.write(struct.pack('<'+'I'*(n*n),*(v for row in mat for v in row)))
    return info


def exhaustive_n4():
    n=4;t,g=family(n);hist={};first=[]
    for rs in permutations(range(n),3):
        for cs in permutations(range(n),4):
            rank,det,_=certificate(t,g,rs,cs)
            hist[rank]=hist.get(rank,0)+1
            if rank<35:first.append((rs,cs,rank))
    return hist,first

if __name__=='__main__':
    import argparse,json
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=8)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--plant',action='store_true')
    args=ap.parse_args()
    print(json.dumps(export_input(args.output,args.n,plant=args.plant)))
