"""Fresh deterministic audit controls, independent of uploaded executables.

Only this newly written file is executed. Numerical controls are not proofs.
Run: OPENBLAS_NUM_THREADS=1 python3 fresh_controls.py
"""
from pathlib import Path
import hashlib
import itertools
import json
import math
import numpy as np

SEED = 741803
rng = np.random.default_rng(SEED)
out = {'seed': SEED, 'numpy_version': np.__version__, 'counts': {}, 'max_residuals': {}}

def fourier(n):
    return np.array([[np.exp(-2j*np.pi*a*b/n)/np.sqrt(n) for b in range(n)] for a in range(n)])

def sv(a):
    return np.linalg.svd(a, compute_uv=False)

def norm(a):
    return float(sv(a)[0]) if min(a.shape) else 0.0

def rank(a, tol=1e-8):
    return int(np.count_nonzero(sv(a)>tol)) if min(a.shape) else 0

def record(name, residual):
    out['counts'][name] = out['counts'].get(name, 0)+1
    out['max_residuals'][name] = max(out['max_residuals'].get(name,0.0), float(abs(residual)))

# Deliberate missing-hypothesis counterexamples, with all equations exact symbolically.
out['zero_sparsity_counterexamples'] = []
for n in [1, 4, 9]:
    u=fourier(n)
    b=np.zeros_like(u); e=u.conj().T; m=u
    assert rank(e)==n
    out['zero_sparsity_counterexamples'].append({'N':n,'s':0,'r':n,'actual_error':0,'claimed_scalar_lower_bound':1})

# Nonvacuous, attained graph-quantile examples constructed from a unitary's subspace.
# I rows of H have forbidden entries J^c carried entirely by rank <=r E.
out['attaining_examples'] = []
for n in [5, 7, 10, 13, 18]:
    for family in ['DFT','Haar']:
        if family=='DFT': u=fourier(n)
        else:
            g=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
            u,_=np.linalg.qr(g)
        for rep in range(12):
            t=int(rng.integers(2,n)); msize=int(rng.integers(1,n))
            I=np.sort(rng.choice(n,t,replace=False)); J=np.sort(rng.choice(n,msize,replace=False))
            Ic=np.setdiff1d(np.arange(n),I); Jc=np.setdiff1d(np.arange(n),J)
            a=u[np.ix_(J,I)]
            L,svals,_=np.linalg.svd(a,full_matrices=False)
            d=int(rng.integers(1,min(t,msize)+1)); r=t-d
            if svals[d-1]<0.12: continue
            q=np.zeros((n,d),complex); q[J,:]=L[:,:d]
            correction=np.zeros((n,n),complex)
            correction[:,Ic]=q@(q.conj().T@u[:,Ic])
            M=u-correction; H=np.linalg.inv(M)
            E=np.zeros((n,n),complex); E[np.ix_(I,Jc)]=H[np.ix_(I,Jc)]
            B=H-E
            error=norm(M-u); expected=math.sqrt(max(0,1-svals[d-1]**2))
            residual=abs(error-expected)
            assert residual<2e-7,(n,family,error,expected)
            assert rank(E)<=r,(n,rank(E),r)
            assert np.count_nonzero(B[np.ix_(I,Jc)])==0
            assert norm(H@M-np.eye(n))<2e-9
            record('attained_quantile_'+family,residual)
            record('attained_quantile_squared_'+family,abs(error**2-expected**2))
            if 1e-5<expected<1-1e-5:
                record('nontrivial_attained_'+family,residual)
            # Independent complementary-rank identity.
            rho=rank(H[np.ix_(I,Jc)])
            qrank=rank(M[np.ix_(J,Ic)])
            assert rho==qrank+t-msize,(n,rho,qrank,t,msize)
            record('nullity_identity',rho-(qrank+t-msize))
            if len(out['attaining_examples'])<12:
                out['attaining_examples'].append({'N':n,'family':family,'I':I.tolist(),'J':J.tolist(),'r_budget':r,'rank_E':rank(E),'error':error,'quantile_bound':expected,'condition_M':float(np.linalg.cond(M))})

# Broad small-N graph and scalar sanity controls, including row-sparsity zero only
# in the separately excluded branch above. Their errors may exceed one.
for n in [2,3,5,8,12,17,24]:
    u=fourier(n)
    for s in sorted({1,min(2,n),min(4,n)}):
        for r in sorted({0,1,n//3,n}):
            B=np.diag(1.5+0.2*rng.random(n)).astype(complex)
            for i in range(n):
                choices=rng.choice(np.delete(np.arange(n),i),s-1,replace=False)
                B[i,choices]=0.1*(rng.normal(size=s-1)+1j*rng.normal(size=s-1))
            X=rng.normal(size=(n,r))+1j*rng.normal(size=(n,r))
            Y=rng.normal(size=(r,n))+1j*rng.normal(size=(r,n))
            E=(0.07/max(r,1))*(X@Y); H=B+E; M=np.linalg.inv(H)
            err=norm(M-u)
            scalar=math.sqrt(max(0,1-(4*s*r if r else s)/n))
            assert err+1e-9>=scalar
            record('positive_s_scalar',0)
            if r<n:
                for t in sorted({r+1,n}):
                    I=np.sort(rng.choice(n,t,replace=False))
                    J=np.flatnonzero(np.any(B[I,:]!=0,axis=0)); d=t-r
                    vals=sv(u[np.ix_(J,I)])
                    sigma=vals[d-1] if d<=len(vals) else 0
                    lb=math.sqrt(max(0,1-sigma*sigma))
                    trace=math.sqrt(max(0,1-t*len(J)/(n*d)))
                    assert err+1e-9>=lb and lb+1e-7>=trace
                    record('random_graph_quantile',0)

# All divisor-pair coset spectra through N=32, including nonzero offsets.
for n in range(1,33):
    u=fourier(n); divs=[v for v in range(1,n+1) if n%v==0]
    for di,dj in itertools.product(divs,repeat=2):
        I=np.arange(di-1,n,di); J=np.arange(dj-1,n,dj)
        h=n//math.gcd(n,di*dj)
        val=np.sqrt(len(I)*len(J)/(n*h))
        expected=np.zeros(min(len(I),len(J))); expected[:h]=val
        error=float(np.max(np.abs(sv(u[np.ix_(J,I)])-expected)))
        assert error<2e-13,(n,di,dj,error)
        record('coset_spectrum',error)

# Exact finite-field algebra for the parity correction rank, not a norm test.
def mod_rank(A,p):
    A=[row[:] for row in A]; piv=0
    for col in range(len(A[0])):
        k=next((k for k in range(piv,len(A)) if A[k][col]%p),None)
        if k is None:continue
        A[piv],A[k]=A[k],A[piv]
        scale=pow(A[piv][col]%p,p-2,p)
        A[piv]=[(x*scale)%p for x in A[piv]]
        for k in range(piv+1,len(A)):
            z=A[k][col]%p
            A[k]=[(x-z*y)%p for x,y in zip(A[k],A[piv])]
        piv+=1
        if piv==len(A):break
    return piv

out['exact_parity_cases']=[]
for n,p in [(4,5),(8,17),(12,13),(20,41),(28,29),(36,37)]:
    w=next(a for a in range(2,p) if pow(a,n,p)==1 and all(pow(a,k,p)!=1 for k in range(1,n)))
    A=[[pow(w,i*j,p) for j in range(1,n,2)] for i in range(0,n,2)]
    rho=mod_rank(A,p); assert rho==n//4
    out['exact_parity_cases'].append({'N':n,'prime':p,'root':w,'rank':rho})

out['parity_exact_threshold']=[]
for n in [4,12,20,28,36]:
    u=fourier(n); H=u.conj().T; I=np.arange(0,n,2); Jc=np.arange(1,n,2)
    E=np.zeros_like(H); E[np.ix_(I,Jc)]=H[np.ix_(I,Jc)]; B=H-E
    assert rank(E)==n//4 and np.count_nonzero(B[np.ix_(I,Jc)])==0
    out['parity_exact_threshold'].append({'N':n,'rank_E':rank(E),'error':0})
    for delta in [0.5,0.01,0.0001]:
        M=delta*np.eye(n); error=norm(M-u)
        assert error>1 and abs(error-(1+delta))<1e-12
        record('parity_infimum',abs(error-(1+delta)))

out['passed']=True
out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
dest=Path(__file__).with_name('FRESH_CONTROL_RESULTS.json')
dest.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['attaining_examples']},indent=2))
