"""Explicit affine-permutation expander topology for a Green-sum FFT search.

All-size expansion certificate follows from the classical Gabber--Galil
8-regular Margulis graph eigenvalue bound ||A||_{1^perp} <= 5*sqrt(2).
For 3 copies of 4 permutation maps, L=12 I-(3/2)A, spectral gap
>= 12-(15/2)*sqrt(2) = 1.393398... > 1.
This means every cut passes the Phase 13 NECESSARY gate; it does NOT
imply that Green weights exist which factor the Fourier matrix.
"""
from __future__ import annotations
import math
from cut_capacity import GreenGraph,cycles


def margulis_maps(side):
    """Four exactly specified permutations on Z_side^2; O(N) construction."""
    if side<2:raise ValueError('side should be >=2')
    out=[]
    for k in range(4):
        pi=[]
        for x in range(side):
            for y in range(side):
                if k==0:xx,yy=(x+2*y)%side,y
                elif k==1:xx,yy=(x+2*y+1)%side,y
                elif k==2:xx,yy=x,(y+2*x)%side
                else:xx,yy=x,(y+2*x+1)%side
                pi.append(xx*side+yy)
        assert sorted(pi)==list(range(side*side))
        out.append(pi)
    return out


def construction(side,q=65537,copies=3):
    """2 layer Green grammar with 6 resolvents per layer (12 total).

    For each copy, weight each row by a nonzero finite-field element.
    Every cycle is adjusted to ensure the corresponding Green inverse exists.
    The Pi support is repeated, but weights change between copies.
    """
    base=margulis_maps(side)
    n=side*side
    graphs=[]
    for c in range(copies):
        for j,pi in enumerate(base):
            weights=[3+((i+17*c+11*j)%37) for i in range(n)]
            for cyc in cycles(pi):
                prod=1
                for idx in cyc:prod=prod*weights[idx]%q
                if prod==1:
                    weights[cyc[0]]+=1
                    assert weights[cyc[0]]<q
            graphs.append(GreenGraph(pi[:],weights))
    first=graphs[:len(graphs)//2]
    second=graphs[len(graphs)//2:]
    return [first,second]


def apply_green_in_linear_work(g,x,q=65537):
    if len(x)!=len(g.pi):raise ValueError('length mismatch')
    out=[0]*len(x)
    operations={'mul':0,'add_sub':0,'field_inv':0}
    for cyc in cycles(g.pi):
        num=0;prod=1
        for k in cyc:
            num=(num+prod*x[k])%q
            prod=prod*g.weights[k]%q
            operations['mul']+=2
            operations['add_sub']+=1
        denom=(1-prod)%q
        if denom==0:raise ValueError('singular Green cycle')
        inv=pow(denom,-1,q)
        operations['field_inv']+=1
        operations['add_sub']+=1
        out[cyc[0]]=num*inv%q
        operations['mul']+=1
        for i in range(len(cyc)-1,0,-1):
            k=cyc[i]
            out[k]=(x[k]+g.weights[k]*out[g.pi[k]])%q
            operations['mul']+=1
            operations['add_sub']+=1
    return out,operations


def uniform_gap_lower_bound(copies=3):
    return copies*(4-5*math.sqrt(2)/2)


def check_graph_gate(side):
    from cut_capacity import exact_cut_certificate
    from subset_gate import structural_rank_lower_bound
    layers=construction(side)
    report=exact_cut_certificate(layers)
    return {'N':side*side,'total_terms':sum(map(len,layers)),
            'spectral_gap_guarantee':uniform_gap_lower_bound(),
            'prefix_gate_rejects':report['rejects'],
            'mid_capacity':report['middle_capacity'],
            'mid_Fourier_rank':report['middle_fourier_rank'],
            'all_subset_gate_passes_by_Gabber_Galil':
                uniform_gap_lower_bound()>1}

if __name__=='__main__':
    import json
    for k in [4,8,16,32,64]:
        print(json.dumps(check_graph_gate(k)))
