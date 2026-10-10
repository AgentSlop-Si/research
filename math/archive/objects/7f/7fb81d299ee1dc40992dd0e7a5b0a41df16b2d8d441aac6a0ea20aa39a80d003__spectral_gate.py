"""Spectral sufficient certificate to PASS the all-subsets necessary cut gate.

IMPORTANT: passing is not an FFT factorization. For permutation edges P_k,
L = sum_k (I - (P_k+P_k.T)/2) is PSD and L*1=0.
For x=indicator(R), x.T L x=number of edges R -> R^c (all nonzero).
If lambda_2(L)>=1, then every subset meets the universal Fourier cut bound.
"""
from __future__ import annotations
import numpy as np
from cut_capacity import GreenGraph,random_green
from subset_gate import hidden_bottleneck_graphs,hidden_subset_graphs


def laplacian(graphs:list[GreenGraph]):
    n=len(graphs[0].pi)
    L=np.zeros((n,n),dtype=np.float64)
    for g in graphs:
        if len(g.pi)!=n or any(w==0 for w in g.weights):
            raise ValueError('only all-nonzero permutation edges supported')
        L[np.arange(n),np.arange(n)]+=1
        for i,j in enumerate(g.pi):
            L[i,j]-=.5
            L[j,i]-=.5
    return L


def gap(graphs):
    a=laplacian(graphs)
    vals=np.linalg.eigvalsh(a)
    assert abs(vals[0])<1e-8 and vals[-1]<=2*len(graphs)+1e-7
    return {'n':len(graphs[0].pi),'terms':len(graphs),
            'lambda_2':float(vals[1]),
            'passes_all_subset_cut_necessary_conditions_if_ge_1':bool(vals[1]>=1-1e-9),
            'largest_eigenvalue':float(vals[-1])}


def graph_collection(layers):
    return [g for layer in layers for g in layer]

if __name__=='__main__':
    from random import Random
    from cut_capacity import graph_from_shift
    import json
    n=128
    random_graphs=[random_green(n,Random(10_000+i),zero_prob=0) for i in range(4)]
    local_graphs=[graph_from_shift(n,s,weight=3) for s in (1,2,3,4)]
    bottleneck=graph_collection(hidden_bottleneck_graphs(n))
    for name,graphs in [('random_global',random_graphs),
                        ('local_shifts',local_graphs),('hidden_bottleneck',bottleneck)]:
        print(name,json.dumps(gap(graphs)))
