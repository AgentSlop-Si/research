import numpy as np, math, json, time
from scipy.optimize import linprog


def solve_support(N,S,complex_weights=True,positive=False):
    S=np.array(sorted(set(S)),dtype=int); k=len(S)
    f=np.arange(1,N,dtype=float)[:,None]
    z=np.exp(-2j*np.pi*f*S[None,:]/N)
    A=z.real; B=z.imag
    if complex_weights:
        # vars [a(k), b(k), t]
        rows=[]; rhs=[]
        re=np.hstack([A,-B,-np.ones((N-1,1))])
        im=np.hstack([B, A,-np.ones((N-1,1))])
        rows += [re,-np.hstack([A,-B,np.ones((N-1,1))])]
        # easier explicitly: re<=t, -re<=t
        rows=[]
        rows.append(np.hstack([ A,-B,-np.ones((N-1,1))]))
        rows.append(np.hstack([-A, B,-np.ones((N-1,1))]))
        rows.append(np.hstack([ B, A,-np.ones((N-1,1))]))
        rows.append(np.hstack([-B,-A,-np.ones((N-1,1))]))
        Aub=np.vstack(rows); bub=np.zeros(4*(N-1))
        Aeq=np.zeros((2,2*k+1)); Aeq[0,:k]=1; Aeq[1,k:2*k]=1
        beq=np.array([1.,0.]); c=np.zeros(2*k+1); c[-1]=1
        bounds=[(None,None)]*(2*k)+[(0,None)]
        res=linprog(c,A_ub=Aub,b_ub=bub,A_eq=Aeq,b_eq=beq,bounds=bounds,method='highs')
        if not res.success: return None
        w=res.x[:k]+1j*res.x[k:2*k]
    else:
        # real weights only
        rows=[np.hstack([ A,-np.ones((N-1,1))]),np.hstack([-A,-np.ones((N-1,1))]),
              np.hstack([ B,-np.ones((N-1,1))]),np.hstack([-B,-np.ones((N-1,1))])]
        Aub=np.vstack(rows); bub=np.zeros(4*(N-1))
        Aeq=np.zeros((1,k+1)); Aeq[0,:k]=1; beq=np.array([1.]); c=np.zeros(k+1); c[-1]=1
        bounds=([(0,None)]*k if positive else [(None,None)]*k)+[(0,None)]
        res=linprog(c,A_ub=Aub,b_ub=bub,A_eq=Aeq,b_eq=beq,bounds=bounds,method='highs')
        if not res.success: return None
        w=res.x[:k].astype(complex)
    coeff=z@w
    return {'rect_t':float(res.fun),'maxmag':float(np.max(np.abs(coeff))),
            'support':S.tolist(),'weights':[[float(v.real),float(v.imag)] for v in w]}


def search(N,k,trials,rng,complex_weights=True,positive=False):
    candidates=[]
    # deterministic arithmetic-ish supports
    candidates.append(np.arange(k))
    candidates.append(np.floor(np.linspace(0,N-1,k)).astype(int))
    if N%k==0: candidates.append(np.arange(k)*(N//k))
    for _ in range(trials):
        rest=rng.choice(np.arange(1,N),size=k-1,replace=False) if k>1 else np.array([],dtype=int)
        candidates.append(np.r_[0,rest])
    best=None
    for S in candidates:
        if len(set(S.tolist()))<k: continue
        r=solve_support(N,S,complex_weights,positive)
        if r and (best is None or r['maxmag']<best['maxmag']): best=r
    return best

rng=np.random.default_rng(20261009)
out=[]
for N in [32,64,128,256]:
    for k in [2,3,4,5,6,8,10,12,16]:
        if k>N: continue
        bc=search(N,k,40,rng,True,False)
        bp=search(N,k,20,rng,False,True)
        out.append({'N':N,'k':k,'complex':bc,'positive':bp})
        print(N,k,'complex',bc['maxmag'] if bc else None,'positive',bp['maxmag'] if bp else None)
open('sparse_surrogate_research/complex_surrogate_search_results.json','w').write(json.dumps(out,indent=2))
