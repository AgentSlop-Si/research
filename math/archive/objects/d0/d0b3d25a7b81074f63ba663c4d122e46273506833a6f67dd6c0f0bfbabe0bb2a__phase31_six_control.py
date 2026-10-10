"""Six-term 3x4 control; the N=4 check is exhaustive, N=8/16 are sampled."""
from __future__ import annotations
from random import Random
from itertools import combinations,permutations
from phase31_rectangular import family,SEEDS,P,ROOT
from phase30_four_parameter import inverse,random_cycle,green_matrix,PRIMITIVE
from phase30_dimension_gate import monomials,lifted_general
from phase30_macaulay import rank_pivots


def additional_green(n,seed,den):
    rng=Random(seed)
    z=pow(PRIMITIVE,-(P-1)//n,P)
    roots=[pow(z,j,P) for j in range(n)]
    matrix=green_matrix(random_cycle(n,rng),inverse(den))
    left=[roots[rng.randrange(n)] for _ in range(n)]
    right=[roots[rng.randrange(n)] for _ in range(n)]
    return [[left[i]*matrix[i][j]*right[j]%P for j in range(n)]
            for i in range(n)]


def all_rect_minors(target,gens,rs,cs):
    q=len(gens)
    e2=monomials(2,q);index={e:i for i,e in enumerate(e2)}
    out=[]
    for i,ip in combinations(range(len(rs)),2):
        for j,jp in combinations(range(len(cs)),2):
            x=target[i][jp]*target[ip][j]%P
            y=target[i][j]*target[ip][jp]%P
            poly=[0]*len(e2)
            for a in range(q):
                for b in range(q):
                    exp=[0]*q;exp[a]+=1;exp[b]+=1
                    pos=index[tuple(exp)]
                    poly[pos]=(poly[pos]
                        +x*gens[a][rs[i]][cs[j]]*gens[b][rs[ip]][cs[jp]]
                        -y*gens[a][rs[i]][cs[jp]]*gens[b][rs[ip]][cs[j]])%P
            out.append(poly)
    return out


def run(n=4,samples=24):
    seed=SEEDS.get(n,2800+n)
    target,g5=family(n,seed)
    g6=additional_green(n,seed*7+29,17)
    gens=(*g5,g6)
    if n==4:
        mappings=((rs,cs) for rs in permutations(range(n),3)
                             for cs in permutations(range(n),4))
        expected=576
    else:
        rng=Random(619000+n)
        mappings=((rng.sample(range(n),3),rng.sample(range(n),4))
                  for _ in range(samples))
        expected=samples
    histogram={}
    for rs,cs in mappings:
        mat=lifted_general(all_rect_minors(target,gens,rs,cs),6,3)
        rk,_=rank_pivots(mat)
        histogram[rk]=histogram.get(rk,0)+1
    return {'N':n,'prime':P,'generators':6,'window':[3,4],
            'degree':3,'basis_dimension':56,'tested':expected,
            'exhaustive':n==4,'histogram':histogram}

if __name__=='__main__':
    import json
    for n in (4,8,16):
        print(json.dumps(run(n,24),sort_keys=True),flush=True)
