"""Every-cut (not just prefix) graph expansion obstruction for Green products.

For unitary Fourier U_N and R subset indices, C=R complement:
rank U[R,C] >= ceil(|R||C|/N), because ||U[R,C]||_F^2=|R||C|/N
and ||U[R,C]||_2<=1. The low-rank graph cut bound is weight-independent.
"""
from __future__ import annotations
import math
from cut_capacity import GreenGraph, circuit_cut_budget, exact_cut_certificate


def subset_capacity(graph:GreenGraph,subset:set[int]):
    n=len(graph.pi)
    if any(i<0 or i>=n for i in subset):raise ValueError('out of range')
    forward=sum(graph.weights[i]!=0 and graph.pi[i] not in subset for i in subset)
    backward=sum(graph.weights[i]!=0 and graph.pi[i] in subset
                 for i in range(n) if i not in subset)
    return forward,backward


def all_stage_capacity(layers:list[list[GreenGraph]],subset):
    subset=set(subset)
    p=q=0
    for layer in layers:
        for g in layer:
            f,b=subset_capacity(g,subset)
            p+=f;q+=b
    return p,q


def structural_rank_lower_bound(n,m):
    # ceil(m*(n-m)/n) exactly, no roundoff.
    return (m*(n-m)+n-1)//n


def error_barrier(n,m,capacity):
    """Lower bounds on unitarily normalized DFT operator approximation.

    capacity is an upper bound on rank of T[R,Rc]. Can apply to ANY R.
    No claim about average-case input error; operator norm is worst-case.
    """
    h=m*(n-m)/n
    q=min(m,n-m)
    r=min(capacity,q)
    frob=math.sqrt(max(h-r,0)/n)
    op=math.sqrt(max(h-r,0)/(q-r)) if r<q else 0
    return {'N':n,'subset_size':m,'cut_capacity':capacity,
            'certified_fourier_rank_at_least':structural_rank_lower_bound(n,m),
            'relative_frobenius_error_at_least':frob,
            'operator_error_at_least':op}


def subset_certificate(layers,subset):
    n=len(layers[0][0].pi)
    subset=set(subset)
    if not (0<len(subset)<n):raise ValueError('nontrivial proper subset needed')
    forward,backward=all_stage_capacity(layers,subset)
    lower=structural_rank_lower_bound(n,len(subset))
    return {'N':n,'subset':sorted(subset),'subset_size':len(subset),
            'cut_capacity_R_to_C':forward,
            'cut_capacity_C_to_R':backward,
            'Fourier_rank_lower_bound':lower,
            'rejects_all_weight_assignments_for_these_graph_supports':
                (min(forward,backward)<lower),
            'error_R_to_C':error_barrier(n,len(subset),forward),
            'error_C_to_R':error_barrier(n,len(subset),backward)}


def hidden_subset_graphs(n=128,subset=(7,38,69,100),seed=2504):
    """Four independently random permutations which preserve one hidden set.

    This is a negative control: all natural prefix cuts can have sufficient
    boundary capacity, but a NONCONTIGUOUS subset R has zero boundary.
    """
    from random import Random
    rng=Random(seed)
    subset=set(subset)
    if not (0<len(subset)<n):raise ValueError('subset')
    blocks=[sorted(subset),[i for i in range(n) if i not in subset]]
    graphs=[]
    for j in range(4):
        perm=[None]*n
        for domain in blocks:
            targets=domain[:]
            rng.shuffle(targets)
            for src,dst in zip(domain,targets):perm[src]=dst
        # Each cycle product 3^size != 1 mod 65537 for these sizes.
        g=GreenGraph(perm,[3]*n)
        graphs.append(g)
    return [[graphs[0],graphs[1]],[graphs[2],graphs[3]]]



def hidden_bottleneck_graphs(n=128, subset=(3,19,35,51,67,83,99,115),seed=1307):
    """Four permutations with exactly ONE cross edge each way per graph.

    The graph union is connected across the hidden 8/120 partition, but
    only has capacity 4; its natural prefix cuts typically look expansive.
    """
    from random import Random
    rng=Random(seed)
    R=set(subset)
    C=set(range(n))-R
    blocks=[sorted(R),sorted(C)]
    graphs=[]
    for _ in range(4):
        pi=[None]*n
        for domain in blocks:
            dest=domain[:] ; rng.shuffle(dest)
            for i,j in zip(domain,dest):pi[i]=j
        i=rng.choice(blocks[0]);j=rng.choice(blocks[1])
        pi[i],pi[j]=pi[j],pi[i]
        graphs.append(GreenGraph(pi,[3]*n))
    return [[graphs[0],graphs[1]],[graphs[2],graphs[3]]]

if __name__=='__main__':
    import json
    layers=hidden_subset_graphs()
    pref=exact_cut_certificate(layers)
    hidden=subset_certificate(layers,{7,38,69,100})
    print(json.dumps({'prefix_gate_rejects':pref['rejects'],
                      'min_prefix_capacity_margin':min(v-min(i,128-i)
                                                    for i,v in enumerate(pref['profile']) if 0<i<128),
                      'hidden_cut_certificate':hidden},indent=2))
