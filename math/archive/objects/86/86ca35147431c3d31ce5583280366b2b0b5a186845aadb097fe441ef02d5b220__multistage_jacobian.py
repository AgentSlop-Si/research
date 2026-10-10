"""Exact modular Jacobian of multi-stage separated-generator rank-one QS products.

M = S_t P_(t-1) S_(t-1) ... P_1 S_1, where (P_j X)[i,:]=X[perm_j[i],:].
Each S is diag(d)+tril(a b^T,-1)+triu(c e^T,1).

This is NOT an FFT construction. Uses numpy.int64 only with moduli such that
n*(p-1)**2 <= 2**63-1. Independent complete finite-difference checks.
"""
from pathlib import Path

SEED_MOD=12289

def stage(n,r,rng):
    a=lambda:np.array([[rng.randrange(1,SEED_MOD) for _ in range(r)] for _ in range(n)],dtype=np.int64)
    return {'L':a(),'V':a(),'U':a(),'W':a(),
            'd':np.array([rng.randrange(1,SEED_MOD) for _ in range(n)],dtype=np.int64)}

def variants(par):
    n=len(par['d']);r=par['L'].shape[1]
    for i in range(n):
        d=np.zeros((n,n),dtype=np.int64);d[i,i]=1
        yield ('d',i,0),d
    for typ,partner in [('L','V'),('V','L'),('U','W'),('W','U')]:
        for i in range(n):
            for k in range(r):
                d=np.zeros((n,n),dtype=np.int64)
                if typ=='L':d[i,:i]=par['V'][:i,k]
                elif typ=='V':d[i+1:,i]=par['L'][i+1:,k]
                elif typ=='U':d[i,i+1:]=par['W'][i+1:,k]
                elif typ=='W':d[:i,i]=par['U'][:i,k]
                yield (typ,i,k),d
import numpy as np
import random


def stage_value(par,p):
    n=len(par['d'])
    low=np.tril(par['L'] @ par['V'].T,k=-1)
    upp=np.triu(par['U'] @ par['W'].T,k=1)
    return (low+upp+np.diag(par['d']))%p


def multiply(A,B,p):
    return (A @ B) % p


def compose(mats,perms,p):
    x = mats[0]
    for j in range(1,len(mats)):
        x=multiply(mats[j],x[perms[j-1],:],p)
    return x


def materialize(n,t,perms,seed,p=12289):
    rng=random.Random(seed)
    pars=[stage(n,1,rng) for _ in range(t)]
    mats=[stage_value(v,p) for v in pars]
    output=compose(mats,perms,p)
    jcols=[]
    for k in range(t):
        before=compose(mats[:k],perms[:k-1],p) if k>0 else None
        for param_id,d in variants(pars[k]):
            if k==0:
                deriv=d%p
            else:
                deriv=multiply(d, before[perms[k-1],:],p)
            for j in range(k+1,t):
                deriv=multiply(mats[j],deriv[perms[j-1],:],p)
            jcols.append(deriv.reshape(n*n))
    J=np.array(jcols,dtype=np.int64).T%p
    return output,J,pars,mats


def check_differences(n,t,perms,pars,base,J,seed,p=12289,num=20):
    rng=random.Random(seed)
    orig=[{k:np.copy(v) for k,v in par.items()} for par in pars]
    count=5*n
    for x in rng.sample(range(t*count),min(num,t*count)):
        s,k=divmod(x,count)
        par=[{k:np.copy(v) for k,v in pa.items()} for pa in orig]
        # same coordinate enumeration as jacobian_gate.variants()
        label=list(variants(par[s]))[k][0]
        if label[0]=='d':
            par[s]['d'][label[1]]=(par[s]['d'][label[1]]+1)%p
        else:
            par[s][label[0]][label[1],label[2]]=(par[s][label[0]][label[1],label[2]]+1)%p
        got=compose([stage_value(pa,p) for pa in par],perms,p)
        if not np.array_equal((got-base).reshape(-1)%p,J[:,x]):
            raise AssertionError(('differential mismatch',x,label))
    return True


def rank_minor(A,p):
    """Returns (rank, pivot columns, det pivot rows/cols) by row Gauss elimination.
       At full-row-rank Jacobian the recorded full-row determinant is a certificate.
    """
    A=np.array(A,copy=True,dtype=np.int64)%p
    nr,nc=A.shape
    row=0; cols=[];pivrows=[]; determinant=1;sign=1
    for col in range(nc):
        if row>=nr:break
        inds=np.flatnonzero(A[row:,col]);
        if not len(inds): continue
        pivotrow=row+int(inds[0])
        if pivotrow!=row:
            A[[row,pivotrow],:]=A[[pivotrow,row],:];sign=-sign
        z=int(A[row,col]);determinant=determinant*z%p
        inverse=pow(z,-1,p)
        A[row,col:]=(A[row,col:]*inverse)%p
        below=np.flatnonzero(A[row+1:,col])+row+1
        if len(below):
            A[below,col:]=(A[below,col:]-A[below,col:col+1]*A[row:row+1,col:])%p
        cols.append(col);row+=1
    # invariant: row swaps among the N x N pivot-column minor reflected in sign
    return row,cols,(determinant*sign)%p


def evaluate(n,t,seed=99017,p=12289):
    rng=random.Random(seed+n*31+t*997)
    perms=[]
    for _ in range(t-1):
        a=list(range(n));rng.shuffle(a);perms.append(a)
    base,J,pars,mats=materialize(n,t,perms,seed,p)
    check_differences(n,t,perms,pars,base,J,seed+299,p)
    rk,pivs,det=rank_minor(J,p)
    upper=min(n*n,t*(5*n-6)-(t-1)*n)
    return {'n':n,'t':t,'p':p,'seed':seed,'permutations':perms,'jac_shape':list(J.shape),
            'rank':rk,'gauge_dimension_bound':upper,'pivot_columns':pivs,
            'pivot_minor_det_mod_p':det if rk==n*n else None,
            'finite_differences':'passed'}

if __name__=='__main__':
    import json
    for n,t in [(8,2),(8,3),(16,2),(16,3),(16,4),(16,5)]:
        x=evaluate(n,t);print(json.dumps({k:v for k,v in x.items() if k not in ('pivot_columns','permutations')}),flush=True)
