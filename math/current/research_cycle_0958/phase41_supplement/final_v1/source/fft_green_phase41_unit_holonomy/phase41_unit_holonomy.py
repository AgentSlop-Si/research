"""Phase 41: controlled complex unit-circle weighted Green cycles.

Numerical optimizer is exploratory, not proof. Uses first two Fourier rows' four anchored cross-ratios.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent/'fft_green_phase40_four_middle'))
import numpy as np
from scipy.optimize import least_squares
from phase40_holonomy import random_problem, normalize_gauge


def model(n, seed=40040):
    # edge enumerations independent of p; cycle order from project
    cycles, weights = random_problem(n, 998244353, seed)
    gauge = normalize_gauge(n,cycles,weights,998244353)
    edges = gauge['edges']
    chords = gauge['chord']
    return cycles, edges, chords


def matrices(n,theta,edges,chords,grad=False):
    weights=np.ones(2*n,dtype=np.complex128)
    weights[chords]=np.exp(1j*theta)
    Ws=[np.zeros((n,n),dtype=np.complex128) for _ in range(2)]
    for idx,e in enumerate(edges): Ws[e.cycle][e.target,e.source]=weights[idx]
    Gs=[np.linalg.inv(np.eye(n)-W) for W in Ws]
    M=Gs[0]+Gs[1]
    return M,Gs,weights


def ratios_and_jac(n,theta,edges,chords,jmax=4):
    M,Gs,ws=matrices(n,theta,edges,chords)
    values=np.array([M[0,j]*M[1,0]/(M[1,j]*M[0,0]) for j in range(1,jmax+1)])
    dlog=np.zeros((jmax,len(chords)),dtype=np.complex128)
    for k,idx in enumerate(chords):
        e=edges[idx];G=Gs[e.cycle];u,v=e.source,e.target
        def term(r,c): return G[r,v]*G[u,c]*1j*ws[idx]/M[r,c]
        for j in range(1,jmax+1):
            dlog[j-1,k]=term(0,j)+term(1,0)-term(1,j)-term(0,0)
    return values,values[:,None]*dlog


def four_target(n):
    return np.exp(-2j*np.pi*np.arange(1,5)/n)


def fit(n,tries=15,seed=42,windows=4):
    rng=np.random.default_rng(seed+n)
    cycles,edges,chords=model(n)
    target=four_target(n)[:windows]
    best=None
    for trial in range(tries):
        theta=rng.uniform(-np.pi,np.pi,len(chords))
        def res(t):
            try: z,_=ratios_and_jac(n,t,edges,chords,windows)
            except np.linalg.LinAlgError: return np.full(2*windows,1e4)
            return np.r_[np.real(z-target),np.imag(z-target)]
        def jac(t):
            try: _,J=ratios_and_jac(n,t,edges,chords,windows)
            except np.linalg.LinAlgError: return np.zeros((2*windows,len(chords)))
            return np.r_[J.real,J.imag]
        opt=least_squares(res,theta,jac=jac,max_nfev=300,xtol=1e-12,gtol=1e-12,ftol=1e-12)
        err=float(np.max(np.abs(res(opt.x))))
        if best is None or err<best['error']:
            best=dict(N=n,trial=trial,error=err,theta=opt.x,evals=opt.nfev,rank=int(np.linalg.matrix_rank(jac(opt.x))),chords=chords,cycles=cycles)
        if err<1e-10:break
    return best

if __name__=='__main__':
    import json
    for n in (8,16,32):
        result=fit(n,tries=12)
        print(json.dumps({k:v for k,v in result.items() if k not in ('theta','cycles','chords')}))
        Path(__file__).with_name(f'numeric_solution_N{n}.json').write_text(json.dumps({**{k:v for k,v in result.items() if k not in ('theta','chords')},'theta':result['theta'].tolist(),'chords':result['chords']},indent=2))
