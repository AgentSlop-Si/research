"""Exploratory numerical fit of all N-1 Fourier ratios using arbitrary complex
edge gains. A tiny residual is NOT an exact algebraic Fourier construction.
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import least_squares
from phase41_unit_holonomy import model

def calculate(n,vars,edges,chords):
    m=len(chords)
    logs=vars[:m]+1j*vars[m:]
    ws=np.ones(2*n,dtype=complex)
    ws[chords]=np.exp(logs)
    W1=np.zeros((n,n),dtype=complex)
    W2=np.zeros_like(W1)
    for i,e in enumerate(edges):(W1 if e.cycle==0 else W2)[e.target,e.source]=ws[i]
    gs=[np.linalg.inv(np.eye(n)-W) for W in (W1,W2)]
    M=gs[0]+gs[1]
    return ws,gs,M

def values_jac(n,vars,edges,chords):
    ws,gs,M=calculate(n,vars,edges,chords)
    if np.any(abs(M[[0,1],:])<1e-12):raise ValueError('near-zero anchor')
    m=len(chords)
    vals=np.array([M[0,j]*M[1,0]/(M[1,j]*M[0,0]) for j in range(1,n)])
    J=np.empty((n-1,m),dtype=complex)
    for q,idx in enumerate(chords):
        e=edges[idx];G=gs[e.cycle];u,v=e.source,e.target
        def t(r,c):return ws[idx]*G[r,v]*G[u,c]/M[r,c]
        for j in range(1,n):J[j-1,q]=vals[j-1]*(t(0,j)+t(1,0)-t(1,j)-t(0,0))
    realJ=np.block([[J.real,-J.imag],[J.imag,J.real]])
    return vals, realJ

def fit(n,tries=20,seed=41,max_nfev=800):
    rng=np.random.default_rng(n+seed)
    cycles,edges,chords=model(n)
    m=len(chords)
    target=np.exp(-2j*np.pi*np.arange(1,n)/n)
    best=None
    for trial in range(tries):
        initial=np.r_[rng.normal(0,.1,m),rng.uniform(-np.pi,np.pi,m)]
        def fun(y):
            try: v,_=values_jac(n,y,edges,chords)
            except (np.linalg.LinAlgError,ValueError,OverflowError):return np.full(2*(n-1),1000.)
            return np.r_[(v-target).real,(v-target).imag]
        def jac(y):
            try:_,J=values_jac(n,y,edges,chords);return J
            except (np.linalg.LinAlgError,ValueError,OverflowError):return np.zeros((2*(n-1),2*m))
        out=least_squares(fun,initial,jac=jac,method='trf',max_nfev=max_nfev,xtol=1e-12,ftol=1e-12,gtol=1e-12)
        err=float(np.max(np.abs(fun(out.x))))
        if best is None or err<best['max_component_error']:
            best={'N':n,'trial':trial,'max_component_error':err,'cost':out.cost,'theta_logweights':out.x.tolist(),'evals':out.nfev,'jac_rank':int(np.linalg.matrix_rank(jac(out.x),tol=1e-8)),'cycles':cycles,'chords':chords}
            print('n',n,'trial',trial,'err',err,'rank',best['jac_rank'],flush=True)
        if err<1e-9:break
    return best

if __name__=='__main__':
    import json
    from pathlib import Path
    for n in (8,16):
        out=fit(n,tries=15,max_nfev=650)
        Path(__file__).with_name(f'phase41_nonunit_target_N{n}.json').write_text(json.dumps(out,indent=2))
