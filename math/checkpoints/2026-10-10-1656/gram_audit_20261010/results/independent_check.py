"""Independent mathematical checks. No source programs imported or executed."""
import json, math, itertools, platform
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
rng=np.random.default_rng(20261010)
def fourier(ns):
    pts=list(itertools.product(*[range(n) for n in ns])); n=len(pts)
    q=np.array([[sum(x*y/d for x,y,d in zip(a,b,ns)) for b in pts] for a in pts])
    return pts,np.exp(-2j*np.pi*q)/np.sqrt(n)
def chirp_lift(ns,pts):
    ans=[]
    for p in pts:
        phase=0.0
        for k,n in zip(p,ns):
            m=n//math.gcd(2,n);r=k%m
            phase+=np.pi*r*(r+(m%2))/m
        ans.append(np.exp(1j*phase))
    return np.array(ans)
rows=[]
groups=[(n,) for n in range(1,33)]+[(2,2),(2,2,2),(2,2,2,2),(2,2,2,2,2),(3,3),(2,3),(2,4),(2,6),(2,8),(4,4),(3,6),(2,2,3),(2,2,4),(2,2,6),(2,3,3),(3,3,3),(4,8),(4,4,4),(2,2,2,3),(2,4,8)]
for ns in groups:
    pts,u=fourier(ns);n=len(pts);g=math.prod(math.gcd(2,x) for x in ns)
    w=n*u*u;b=chirp_lift(ns,pts);wb=w@b;a=np.conjugate(wb)/np.abs(wb)
    ur=np.exp(.5j*np.angle(a));vc=np.exp(.5j*np.angle(b));h=ur[:,None]*u*vc[None,:]
    bound=(n-np.sqrt(n*g))/2;attained=float(np.sum(h.imag**2));ww=w@w.conj().T
    expected=np.array([[n if all((2*(x-y))%d==0 for x,y,d in zip(p,q,ns)) else 0 for q in pts] for p in pts])
    sig=np.linalg.svd(w,compute_uv=False);rand_min=float('inf')
    for _ in range(40):
        rp=np.exp(2j*np.pi*rng.random(n));cp=np.exp(2j*np.pi*rng.random(n))
        rand_min=min(rand_min,float(np.sum((rp[:,None]*u*cp[None,:]).imag**2)))
    row={'cyclic_factors':ns,'N':n,'g':g,'formula':float(bound),'attained':attained,'absolute_error':abs(attained-bound),'flatness_error':float(np.max(abs(np.abs(wb)-np.sqrt(n*g)))),'gram_identity_error':float(np.max(abs(ww-expected))),'spectral_norm_error':float(abs(sig[0]-np.sqrt(n*g))),'numerical_rank':int(sum(sig>1e-8)),'expected_rank':n//g,'random_min_minus_bound':rand_min-bound}
    assert row['absolute_error']<1e-9 and row['flatness_error']<1e-9 and row['gram_identity_error']<1e-9 and row['spectral_norm_error']<1e-9
    assert row['numerical_rank']==row['expected_rank'] and row['random_min_minus_bound']>-1e-9
    rows.append(row)
opt=[]
for ns in [(3,),(4,),(5,),(6,),(2,2),(2,3),(2,4),(3,3)]:
    _,u=fourier(ns);n=u.shape[0];g=math.prod(math.gcd(2,x) for x in ns)
    def f(t):
        h=np.exp(1j*t[:n])[:,None]*u*np.exp(1j*t[n:])[None,:]
        return np.sum(h.imag**2)
    def jac(t):
        h=np.exp(1j*t[:n])[:,None]*u*np.exp(1j*t[n:])[None,:];z=2*h.real*h.imag
        return np.r_[np.sum(z,axis=1),np.sum(z,axis=0)]
    found=[minimize(f,rng.uniform(-np.pi,np.pi,2*n),jac=jac,method='BFGS',options={'gtol':1e-10,'maxiter':2000}) for _ in range(6)]
    best=min(r.fun for r in found);bound=(n-np.sqrt(n*g))/2
    opt.append({'cyclic_factors':ns,'expected':float(bound),'best_random_start':float(best),'gap':float(best-bound),'starts':6});assert abs(best-bound)<1e-8
n=4;aa=np.eye(n)+np.ones((n,n));bb=np.linalg.inv(aa);identity_error=float(np.linalg.norm(aa@bb-np.eye(n)))
aa2=np.array([[1.,1.],[1.,2.]]);bb2=np.array([[3.,5/3],[1.,1.]])
mm2=np.diag([1/(2*np.sqrt(2)),1/np.sqrt(2)])@aa2@np.diag([1.,-1.])@bb2@np.diag([1.,3.]);_,u2=fourier((2,));n2_error=float(np.linalg.norm(mm2-u2))
import sympy as s
K=s.Matrix([[2,1,0],[1,2,1],[0,1,2]]);Ds=s.diag(1,-2,3);Di=s.diag(1,s.I,1)
assert all(s.im(x)==0 for x in Ds.conjugate().T*K*Ds)
assert s.im((Di.conjugate().T*K*Di)[0,1])==1
_,u3=fourier((3,));vals,q=np.linalg.eigh(u3.real+2*u3.imag);lam=np.diag(q.T@u3@q)
real_stage_fourier_error=float(np.linalg.norm(q@np.diag(lam)@q.T-u3));assert real_stage_fourier_error<1e-12
out={'method':'Independent direct character matrices, new code only; no source program run or import. Numerics corroborate proofs, not a universal numerical proof.','versions':{'python':platform.python_version(),'numpy':np.__version__},'group_checks':rows,'optimizer_checks':opt,'scope_examples':{'identity_positive_first_stage_error':identity_error,'N2_factorization_error':n2_error,'N3_real_orthogonal_one_mask_fourier_error':real_stage_fourier_error,'N3_diagonal_eigenvalues':[[float(z.real),float(z.imag)] for z in lam]},'summary':{'groups':len(rows),'largest_N':max(r['N'] for r in rows),'max_witness_error':max(r['absolute_error'] for r in rows),'max_flatness_error':max(r['flatness_error'] for r in rows),'max_gram_error':max(r['gram_identity_error'] for r in rows)}}
Path('independent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary'],indent=2));print(json.dumps(out['scope_examples'],indent=2));print(json.dumps(opt,indent=2))
