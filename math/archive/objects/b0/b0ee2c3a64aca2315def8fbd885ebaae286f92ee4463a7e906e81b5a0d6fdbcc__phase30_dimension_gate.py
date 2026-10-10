"""Dimension theorem and empirical five-term control for full 3x3 minors.

The projective variety of 3x3 rank-one matrices is Segre P^2 x P^2,
of dimension 4 and codimension 4 in P^8. Any projective P^4
(5 independent Green components) must intersect this variety over C.
This is a limitation of 3x3 projective-minor witnesses, not existence of an
admissible invertible diagonal-mask Fourier factorization.
"""
from __future__ import annotations
from math import comb
from random import Random
from phase30_four_parameter import P,PRIMITIVE,inverse,random_cycle,green_matrix,build_four,SEEDS
from phase30_macaulay import rank_pivots,full_minor_quadrics,monomials


def minimum_minor_block(q:int)->int:
    """Smallest m for which q <= (m-1)^2, avoiding forced intersection."""
    m=2
    while (m-1)**2 < q:m+=1
    return m


def fifth_green(n:int,seed:int)->list[list[int]]:
    rng=Random(seed)
    z=pow(PRIMITIVE,-(P-1)//n,P)
    roots=[pow(z,j,P) for j in range(n)]
    g=green_matrix(random_cycle(n,rng),inverse(13))
    left=[roots[rng.randrange(n)] for _ in range(n)]
    right=[roots[rng.randrange(n)] for _ in range(n)]
    return [[left[i]*g[i][j]*right[j]%P for j in range(n)] for i in range(n)]


def general_minors(target,gens,rs,cs):
    q=len(gens)
    exps=monomials(2,q)
    idx={e:i for i,e in enumerate(exps)}
    def product(i,j,ip,jp):
        vec=[0]*len(exps)
        for a in range(q):
            for b in range(q):
                e=[0]*q;e[a]+=1;e[b]+=1
                pos=idx[tuple(e)]
                vec[pos]=(vec[pos]+gens[a][rs[i]][cs[j]]*gens[b][rs[ip]][cs[jp]])%P
        return vec
    polys=[]
    m=len(rs)
    assert len(cs)==m
    for i in range(m):
        for ip in range(i+1,m):
            for j in range(m):
                for jp in range(j+1,m):
                    a=target[i][jp]*target[ip][j]%P
                    b=target[i][j]*target[ip][jp]%P
                    prod1=product(i,j,ip,jp);prod2=product(i,jp,ip,j)
                    polys.append([(a*x-b*y)%P for x,y in zip(prod1,prod2)])
    return polys


def lifted_general(polys,q,degree):
    e2=monomials(2,q);eout=monomials(degree,q);emul=monomials(degree-2,q)
    pos={e:i for i,e in enumerate(eout)}
    rows=[]
    for poly in polys:
        for mult in emul:
            row=[0]*len(eout)
            for coeff,e in zip(poly,e2):
                k=pos[tuple(e[t]+mult[t] for t in range(q))]
                row[k]=coeff
            rows.append(row)
    return rows


def five_term_control(n:int=8,seed:int|None=None,trial:int=5):
    seed=SEEDS[n] if seed is None else seed
    t,g4=build_four(n,seed)
    g5=(*g4,fifth_green(n,seed*3+11))
    # variables ordered component index 0..4, instead of lambda-based order.
    rng=Random(25130+n)
    results=[]
    for k in range(trial):
        rs=rng.sample(range(n),3);cs=rng.sample(range(n),3)
        polys=general_minors(t,g5,rs,cs)
        ranks={}
        for d in (3,4,5):
            rows=lifted_general(polys,5,d)
            r,_=rank_pivots(rows)
            ranks[d]={'rank':r,'basis_dimension':len(rows[0]),'deficiency':len(rows[0])-r}
            assert r < len(rows[0]),(d,r,len(rows[0]))
        results.append({'rows':rs,'columns':cs,'degrees':ranks})
    return {'N':n,'prime':P,'generator_count':5,
            'expected_projective_intersection':True,'checks':results}

if __name__=='__main__':
    import json
    for q in (1,2,3,4,5,9,10,16):
        print(q,'minimum block m =',minimum_minor_block(q))
    report=five_term_control()
    print(json.dumps(report,indent=2))
