"""Exploratory three-unitary-Green-cycle synthesis of Fourier two-row cross-ratios.

This fits all N-1 projective ratios numerically. It does NOT compute the DFT.
"""
from __future__ import annotations
import numpy as np
import random,json
from pathlib import Path
from scipy.optimize import least_squares
import sys
sys.path.insert(0,str(Path(__file__).parent.parent/'fft_green_phase40_four_middle'))
from phase40_holonomy import Edge,DSU

def graph(n,seed=41041):
    rng=random.Random(seed+n)
    cycles=[list(range(n))]
    for _ in range(2):
        c=list(range(n));rng.shuffle(c);cycles.append(c)
    edges=[];tree=[];chords=[];dsu=DSU(n)
    for s,c in enumerate(cycles):
        for j in range(n):
            e=Edge(s,c[j],c[j-1],1)
            idx=len(edges);edges.append(e)
            (tree if dsu.union(e.source,e.target) else chords).append(idx)
    assert len(chords)==2*n+1 and len(tree)==n-1
    return cycles,edges,chords

def apply_matrices(n,angles,edges,chords):
    ws=np.ones(3*n,dtype=complex);ws[chords]=np.exp(1j*angles)
    W=[np.zeros((n,n),dtype=complex) for _ in range(3)]
    for i,e in enumerate(edges):W[e.cycle][e.target,e.source]=ws[i]
    G=[np.linalg.inv(np.eye(n)-z) for z in W]
    M=G[0]+G[1]+G[2]
    return M,G,ws

def values_jac(n,angles,edges,chords):
    M,G,ws=apply_matrices(n,angles,edges,chords)
    vals=np.array([M[0,j]*M[1,0]/(M[1,j]*M[0,0]) for j in range(1,n)])
    J=np.empty((n-1,len(chords)),dtype=complex)
    for k,idx in enumerate(chords):
        e=edges[idx];g=G[e.cycle];u,v=e.source,e.target
        def term(r,c):return (1j*ws[idx])*g[r,v]*g[u,c]/M[r,c]
        for j in range(1,n):J[j-1,k]=vals[j-1]*(term(0,j)+term(1,0)-term(1,j)-term(0,0))
    return vals,np.r_[J.real,J.imag]

def fit(n,tries=10,max_nfev=750,seed=41):
    rng=np.random.default_rng(n+seed)
    cycles,edges,chords=graph(n)
    target=np.exp(-2j*np.pi*np.arange(1,n)/n)
    best=None
    for t in range(tries):
        init=rng.uniform(-np.pi,np.pi,len(chords))
        def fun(y):
            try:v,_=values_jac(n,y,edges,chords);return np.r_[(v-target).real,(v-target).imag]
            except (ValueError,np.linalg.LinAlgError,OverflowError):return np.full(2*(n-1),1e5)
        def jac(y):
            try:_,j=values_jac(n,y,edges,chords);return j
            except (ValueError,np.linalg.LinAlgError,OverflowError):return np.zeros((2*(n-1),len(chords)))
        sol=least_squares(fun,init,jac=jac,method='trf',max_nfev=max_nfev,xtol=1e-12,ftol=1e-12,gtol=1e-12)
        err=float(np.max(abs(fun(sol.x))))
        if best is None or err<best['max_component_error']:
            rank=int(np.linalg.matrix_rank(jac(sol.x),tol=1e-8))
            best={'N':n,'trial':t,'max_component_error':err,'real_jac_rank':rank,'evals':sol.nfev,'angles':sol.x.tolist(),'cycles':cycles,'chords':chords}
            print(n,'trial',t,'err',err,'rank',rank,flush=True)
        if err<1e-9:break
    return best

if __name__=='__main__':
    for n in (8,16,32):
        r=fit(n,tries=8,max_nfev=650)
        Path(__file__).with_name(f'phase41_three_cycle_fit_N{n}.json').write_text(json.dumps(r,indent=2))
