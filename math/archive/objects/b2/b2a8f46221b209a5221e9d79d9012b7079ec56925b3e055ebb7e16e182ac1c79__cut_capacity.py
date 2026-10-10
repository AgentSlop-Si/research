"""Hero #0 Phase 13: weight-independent graph-cut capacity certificates.

Exact modular arithmetic and O(total permutation edges) combinatorial gate.
This is an obstruction for a restricted Green-resolvent circuit grammar,
NOT a general FFT lower bound. Only standard Python is required.
"""
from __future__ import annotations
import random
from dataclasses import dataclass

@dataclass
class GreenGraph:
    pi: list[int]
    weights: list[int]
    def __post_init__(self):
        n=len(self.pi)
        if len(self.weights)!=n or set(self.pi)!=set(range(n)):
            raise ValueError('malformed weighted permutation')


def cycles(pi):
    seen=set()
    result=[]
    for seed in range(len(pi)):
        if seed in seen: continue
        cyc=[]
        j=seed
        while j not in seen:
            seen.add(j)
            cyc.append(j)
            j=pi[j]
        if j!=seed:
            raise AssertionError('permutation expected')
        result.append(cyc)
    return result


def graph_from_shift(n, step, q=65537, weight=3):
    # If weight^cycle_length == 1 (mod q), resolvent is singular;
    # change only that cycle's first weight, keeping the graph support.
    pi=[(i+step)%n for i in range(n)]
    w=[weight%q]*n
    for cyc in cycles(pi):
        prod=1
        for i in cyc: prod=prod*w[i]%q
        if prod==1:
            w[cyc[0]]=0
    return GreenGraph(pi,w)


def random_green(n,rng,q=65537,zero_prob=0.1):
    pi=list(range(n))
    rng.shuffle(pi)
    w=[0 if rng.random()<zero_prob else rng.randrange(2,q) for _ in range(n)]
    for cyc in cycles(pi):
        prod=1
        for i in cyc:prod=prod*w[i]%q
        if prod==1:
            w[cyc[0]]=0
    return GreenGraph(pi,w)


def exact_green(g: GreenGraph,q=65537):
    """Returns (I-P)^-1 with P[i,pi[i]]=weights[i], exactly modulo q."""
    n=len(g.pi)
    a=[[0]*n for _ in range(n)]
    for cyc in cycles(g.pi):
        prod=1
        for i in cyc:prod=prod*g.weights[i]%q
        if prod==1:raise ValueError('singular cycle')
        inv=pow((1-prod)%q,-1,q)
        for i in cyc:
            k=i
            path=1
            while True:
                a[i][k]=(path*inv)%q
                path=(path*g.weights[k])%q
                k=g.pi[k]
                if k==i:break
    return a


def mat_add(a,b,q):
    return [[(x+y)%q for x,y in zip(r,s)] for r,s in zip(a,b)]


def mat_mul(a,b,q):
    n=len(a)
    c=[[0]*n for _ in range(n)]
    for i in range(n):
        ci=c[i]
        for k in range(n):
            aik=a[i][k]
            if aik:
                bk=b[k]
                for j in range(n):ci[j]=(ci[j]+aik*bk[j])%q
    return c


def rank_mod(a,q=65537):
    if not a:return 0
    b=[list(row) for row in a]
    n=len(b);cols=len(b[0]);r=0
    for col in range(cols):
        piv=next((i for i in range(r,n) if b[i][col]%q),None)
        if piv is None:continue
        b[r],b[piv]=b[piv],b[r]
        inv=pow(b[r][col],-1,q)
        row=b[r]
        for j in range(col,cols):row[j]=row[j]*inv%q
        for i in range(r+1,n):
            mult=b[i][col]
            if mult:
                cur=b[i]
                for j in range(col,cols):cur[j]=(cur[j]-mult*row[j])%q
        r+=1
        if r==n:break
    return r


def primitive_root_of_power_of_two(n,q=65537):
    assert n>1 and n&(n-1)==0 and (q-1)%n==0
    # 3 is a primitive generator for GF(65537)^*.
    w=pow(3,(q-1)//n,q)
    assert pow(w,n,q)==1 and pow(w,n//2,q)!=1
    return w


def fourier_mod(n,q=65537):
    w=primitive_root_of_power_of_two(n,q)
    return [[pow(w,i*j,q) for j in range(n)] for i in range(n)]


def cut_profile(g:GreenGraph):
    """Exact number of NONZERO outgoing permutation edges across all prefix cuts.

    O(N) integer operations: each edge (i->j) increases capacities for m=i+1..j
    iff j>i. Return profile[m], with profile[0]=profile[N]=0.
    """
    n=len(g.pi)
    diff=[0]*(n+2)
    for i,j in enumerate(g.pi):
        if g.weights[i]!=0 and i<j:
            diff[i+1]+=1
            diff[j+1]-=1
    out=[0]*(n+1);value=0
    for m in range(1,n):
        value+=diff[m];out[m]=value
    return out


def reverse_cut_profile(g:GreenGraph):
    """Outgoing edges from suffix C to prefix R for every prefix cut m."""
    n=len(g.pi)
    diff=[0]*(n+2)
    for i,j in enumerate(g.pi):
        if g.weights[i]!=0 and j<i:
            diff[j+1]+=1
            diff[i+1]-=1
    out=[0]*(n+1);value=0
    for m in range(1,n):
        value+=diff[m];out[m]=value
    return out


def reverse_circuit_budget(layers):
    n=len(layers[0][0].pi)
    out=[0]*(n+1)
    for layer in layers:
        for g in layer:
            profile=reverse_cut_profile(g)
            for m in range(1,n):out[m]+=profile[m]
    return out


def circuit_cut_budget(layers:list[list[GreenGraph]]):
    if not layers or not layers[0]:raise ValueError('empty circuit')
    n=len(layers[0][0].pi)
    budget=[0]*(n+1)
    for layer in layers:
        for graph in layer:
            if len(graph.pi)!=n:raise ValueError('length mismatch')
            cap=cut_profile(graph)
            for m in range(1,n):budget[m]+=cap[m]
    return budget


def exact_cut_certificate(layers):
    """NECESSARY topological conditions for equality to the N-point DFT.

    The test checks both upper-right and lower-left Fourier cut ranks.
    If either rank exceeds its graph-edge budget, reject ALL weights with
    these supports. Passing is NOT sufficient for a Fourier factorization.
    """
    cap=circuit_cut_budget(layers)
    rev=reverse_circuit_budget(layers)
    n=len(cap)-1
    bad=[]
    for m in range(1,n):
        requirement=min(m,n-m)
        if cap[m]<requirement:
            bad.append({'cut':m,'direction':'prefix_to_suffix',
               'capacity':cap[m],'fourier_rank':requirement,
               'rank_deficit':requirement-cap[m]})
        if rev[m]<requirement:
            bad.append({'cut':m,'direction':'suffix_to_prefix',
               'capacity':rev[m],'fourier_rank':requirement,
               'rank_deficit':requirement-rev[m]})
    mid=n//2
    return {'n':n,'rejects':bool(bad),'violating_cuts':len(bad),
            'first_violation':bad[0] if bad else None,
            'strongest_violation':max(bad,key=lambda d:d['rank_deficit']) if bad else None,
            'middle_cut':mid,'middle_capacity':cap[mid],
            'reverse_middle_capacity':rev[mid],
            'middle_fourier_rank':min(mid,n-mid),
            'profile':cap,'reverse_profile':rev}


def approx_barrier_even_n(n,c):
    """Lower bounds for unitary Fourier approximation in our circuit grammar.

    Any matrix T with rank(T[:n//2, n//2:]) <= c has
      ||U-T||_2 >= sqrt((n/4-c)/(n/2-c)) if c<n/4,
      ||U-T||_F/||U||_F >= sqrt(max(n/4-c,0)/n).
    """
    import math
    if n%2:raise ValueError('n must be even')
    q=n//2
    frob_rel=math.sqrt(max(n/4-c,0)/n)
    op=math.sqrt((n/4-c)/(q-c)) if c<n/4 else 0.0
    return {'N':n,'capacity':c,'global_relative_frobenius_lower_bound':frob_rel,
            'operator_norm_lower_bound':op,'exact_rank_gap':max(q-c,0)}


def modular_cut_audit(layers,cuts,q=65537):
    """Exact matrix verification of the weight-independent capacity bound."""
    n=len(layers[0][0].pi)
    budget=circuit_cut_budget(layers)
    totals=[]
    for layer in layers:
        L=None
        for g in layer:
            G=exact_green(g,q)
            L=G if L is None else mat_add(L,G,q)
        totals.append(L)
    T=totals[0]
    for L in totals[1:]:T=mat_mul(T,L,q)
    report=[]
    for cut in cuts:
        block=[row[cut:] for row in T[:cut]]
        rank=rank_mod(block,q)
        report.append({'cut':cut,'actual_rank':rank,'capacity':budget[cut]})
        assert rank<=budget[cut],(rank,budget[cut],cut)
    return report


def main():
    import json
    n=128
    layers=[[graph_from_shift(n,1), graph_from_shift(n,2)],
            [graph_from_shift(n,3), graph_from_shift(n,4)]]
    audit=exact_cut_certificate(layers)
    print(json.dumps({k:v for k,v in audit.items() if k not in ('profile','reverse_profile')},indent=2))
    print(json.dumps(approx_barrier_even_n(n,audit['middle_capacity']),indent=2))

if __name__=='__main__':main()
