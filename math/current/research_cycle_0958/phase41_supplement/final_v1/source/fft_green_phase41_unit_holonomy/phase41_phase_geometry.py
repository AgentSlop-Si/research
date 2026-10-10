"""Exact phase-only cycle-Green obstruction and an amplitude-relaxed escape template.

The theorem proved in THEOREM.md: a projectively flat row pair in a sum of
TWO unit-edge weighted cyclic Green inverses has at most 8 distinct ratios.
No numerical sampling is used in that proof.
"""
from __future__ import annotations
import cmath
from math import pi
from typing import Sequence

def cycle_edges(cycle:Sequence[int],weights:Sequence[complex]):
    n=len(cycle)
    assert sorted(cycle)==list(range(n)) and len(weights)==n
    return [(cycle[j-1],cycle[j],weights[j]) for j in range(n)]

def dense_cycle_green(cycle,weights):
    n=len(cycle)
    H=1+0j
    for w in weights:H*=w
    if abs(H-1)<1e-12:raise ValueError('singular weighted cycle')
    # Independent direct path-product formula, no numpy matrix inversion.
    ans=[[0j]*n for _ in range(n)]
    for j in range(n):
        index=cycle.index(j)
        v=j;prod=1+0j
        ans[v][j]=prod/(1-H)
        for step in range(1,n):
            index=(index+1)%n
            prod*=weights[index]
            v=cycle[index]
            ans[v][j]=prod/(1-H)
    return ans

def distinct_quotients(G,a,b,eps=1e-9):
    val=[G[a][j]/G[b][j] for j in range(len(G))]
    unique=[]
    for z in val:
        if all(abs(z-u)>eps for u in unique):unique.append(z)
    return val,unique

def signatures(G1,G2,a,b,tol=1e-8):
    n=len(G1)
    r1,_=distinct_quotients(G1,a,b,tol)
    r2,_=distinct_quotients(G2,a,b,tol)
    groups=[]
    for j in range(n):
        for key,indices in groups:
            if abs(r1[j]-key[0])<tol and abs(r2[j]-key[1])<tol:
                indices.append(j);break
        else: groups.append(((r1[j],r2[j]),[j]))
    return groups

def fourier_pair_ratios(n):
    omega=cmath.exp(2j*pi/n)
    return [omega**(-j) for j in range(n)]

def blaschke_template(n):
    """An algebraic local escape: one nonunit amplitude ratio can cover all
    Fourier phases via a nonconstant circle-preserving Mobius map.

    This does NOT construct a globally consistent two-Green FFT circuit.
    """
    omega=cmath.exp(2j*pi/n)
    targets=[omega**j for j in range(n)]
    ts=[(2-z)/(z-.5) for z in targets]
    outputs=[(2+.5*t)/(1+t) for t in ts]
    return {'N':n,'max_target_error':max(abs(a-b) for a,b in zip(outputs,targets)),
            'max_modulus_error':max(abs(abs(t)-2) for t in ts)}

if __name__=='__main__':
    for n in (16,32,64,256):
        print(blaschke_template(n))
