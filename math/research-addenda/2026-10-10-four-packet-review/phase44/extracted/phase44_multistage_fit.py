"""Numerical (not certified) full Fourier target for multi-stage Green sums.

M=S_(d-1) D_(d-2)...D_0 S_0, S_i=sum_{s=1}^3 (I-W_is)^-1.
Analytic real Jacobian of all (N-1)^2 complex cross ratios.
"""
from __future__ import annotations
import argparse,json,sys,time
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
BASE=Path(__file__).resolve().parent
PHASE42=BASE.parent/'fft_green_phase42_three_row'
sys.path.insert(0,str(PHASE42))
from phase42_three_row_fit import direct_green
from phase44_multistage_rank import specs


def evaluation(n,depth,x,param,with_jac=True):
    total_edge=depth*(2*n+1)
    assert len(x)==total_edge+2*(depth-1)*(n-1)
    gs=[];S=[];W=[]
    curr=0
    for orders,edges,chords,ab in param:
        w=np.ones(3*n,dtype=complex)
        w[chords]=np.exp(1j*x[curr:curr+len(chords)])
        curr+=len(chords)
        green=[direct_green(n,orders[k],w[k*n:(k+1)*n]) for k in range(3)]
        S.append(sum(green));gs.append(green);W.append(w)
    D=[]
    for ell in range(depth-1):
        v=np.ones(n,dtype=complex)
        angles=x[curr:curr+n-1]
        amps=x[curr+n-1:curr+2*(n-1)]
        v[1:]=np.exp(amps+1j*angles)
        D.append(v)
        curr+=2*(n-1)
    assert curr==len(x)
    R=[np.eye(n,dtype=complex) for _ in range(depth)]
    L=[np.eye(n,dtype=complex) for _ in range(depth)]
    for ell in range(depth-1):R[ell+1]=D[ell][:,None]*(S[ell]@R[ell])
    for ell in reversed(range(depth-1)):L[ell]=(L[ell+1]@S[ell+1])*D[ell][None,:]
    M=S[-1]@R[-1]
    if not np.isfinite(M).all() or np.min(abs(M))<1e-11: raise ValueError('singular projective denominator')
    Q=M[1:,1:]*M[0,0]/(M[0,1:]*M[1:,[0]])
    if not with_jac:return Q,M,None
    size=len(x)
    J=np.empty((n-1,n-1,size),dtype=complex)
    def fill(col,row,scale,col_id):
        d00=scale*col[0]*row[0]/M[0,0]
        d0j=scale*col[0]*row[1:]/M[0,1:]
        dr0=scale*col[1:,None]*row[0]/M[1:,[0]]
        drj=scale*col[1:,None]*row[None,1:]/M[1:,1:]
        J[:,:,col_id]=Q*(drj+d00-d0j[None,:]-dr0)
    curr=0
    for ell,(_orders,edges,chords,_ab) in enumerate(param):
        for idx in chords:
            e=edges[idx];g=gs[ell][e.cycle]
            col=L[ell]@g[:,e.target]
            row=g[e.source,:]@R[ell]
            fill(col,row,1j*W[ell][idx],curr)
            curr+=1
    for ell in range(depth-1):
        left=L[ell+1]@S[ell+1]
        right=S[ell]@R[ell]
        for mode in ('phase','amp'):
            for k in range(1,n):
                fill(left[:,k],right[k,:],D[ell][k]*(1j if mode=='phase' else 1),curr)
                curr+=1
    assert curr==size
    return Q,M,J


def objective(n,depth,param):
    goal=np.exp(-2j*np.pi*np.outer(np.arange(1,n),np.arange(1,n))/n)
    sz=depth*(2*n+1)+2*(depth-1)*(n-1)
    def fun(x):
        try:Q,_,_=evaluation(n,depth,x,param,False)
        except (ValueError,OverflowError,FloatingPointError):return np.full(2*(n-1)**2,1e8)
        d=Q-goal
        return np.r_[d.real.ravel(),d.imag.ravel()]
    def jac(x):
        try:Q,M,J=evaluation(n,depth,x,param,True)
        except (ValueError,OverflowError,FloatingPointError):return np.zeros((2*(n-1)**2,sz))
        return np.concatenate((J.real.reshape(-1,sz),J.imag.reshape(-1,sz)),axis=0)
    return fun,jac


def fit(n=8,depth=4,attempts=3,max_nfev=500,seed=44003):
    param=specs(n,depth)
    fun,jac=objective(n,depth,param)
    rng=np.random.default_rng(seed)
    best=None
    for attempt in range(attempts):
        phase=rng.uniform(-1.9,1.9,depth*(2*n+1))
        inter=np.r_[tuple(np.r_[rng.uniform(-2,2,n-1),rng.normal(0,0.35,n-1)] for _ in range(depth-1))]
        x=np.r_[phase,inter]
        start=time.time()
        result=least_squares(fun,x,jac=jac,method='trf',max_nfev=max_nfev,
                 xtol=1e-12,ftol=1e-12,gtol=1e-12,verbose=0)
        residual=fun(result.x)
        maxerr=float(abs(residual).max())
        norm=float(np.linalg.norm(residual))
        try:rank=int(np.linalg.matrix_rank(jac(result.x),tol=1e-8))
        except (ValueError,np.linalg.LinAlgError):rank=-1
        print(f'N={n}, depth={depth}, attempt={attempt}, maxerr={maxerr:.4g}, l2={norm:.4g}, rank={rank}, nfev={result.nfev}, secs={time.time()-start:.1f}',flush=True)
        if best is None or norm<best['l2_projective_error']:
            best={'N':n,'depth':depth,'green_solves':3*depth,
               'trial':attempt,'maximum_real_component_projective_error':maxerr,
               'l2_projective_error':norm,'real_jacobian_rank':rank,
               'nfev':int(result.nfev), 'variables':result.x.tolist(),
               'exact_certification':False}
            (BASE/f'phase44_full_target_N{n}_d{depth}.json').write_text(json.dumps(best,indent=2)+'\n')
        if maxerr<1e-10:break
    return best

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=8);ap.add_argument('--depth',type=int,default=4)
    ap.add_argument('--attempts',type=int,default=2);ap.add_argument('--steps',type=int,default=300)
    args=ap.parse_args()
    fit(args.n,args.depth,args.attempts,args.steps)
