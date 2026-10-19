#!/usr/bin/env python3
"""Fresh local controls for the ALG-036 thin-deficit proof. No network or legacy imports.
Finite exact checks and floating/Monte Carlo diagnostics are not the all-N proof.
"""
from __future__ import annotations
import json, math, platform
from fractions import Fraction
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import ncx2
import sympy as sp

SEED=202610190125
rng=np.random.default_rng(SEED)
counts={}
residuals={}
records={}

def tick(key,n=1): counts[key]=counts.get(key,0)+n

def note_max(key,v): residuals[key]=max(residuals.get(key,0.0),float(abs(v)))

def realify(A):
    return A.applyfunc(sp.re).row_join(-A.applyfunc(sp.im)).col_join(
        A.applyfunc(sp.im).row_join(A.applyfunc(sp.re)))

def logB(N,d,a):
    if a==0:return -math.inf
    t=N*a/d
    return d*(math.log(-math.expm1(-t)) if t<1 else math.log1p(-math.exp(-t)))

def B(N,d,a):return math.exp(logB(N,d,a))

def log_leverage(p,a):
    return sum(float(v)*(math.log(-math.expm1(-a/float(v))) if a/float(v)<1 else math.log1p(-math.exp(-a/float(v)))) for v in p if v>1e-15)

def scalar_tail_rate(e,upper):
    # Stable Taylor series when cancellation in e-log(1+e) would be appreciable.
    if e<1e-3:
        if upper:return sum(((-1)**k)*e**k/k for k in range(2,14))
        return sum(e**k/k for k in range(2,14))
    return e-math.log1p(e) if upper else -e-math.log1p(-e)

def norm_tail(N,e,upper):
    return math.exp(-N*scalar_tail_rate(e,upper))

def block_logprob(sizes,a):
    return sum((math.log(-math.expm1(-n*a)) if n*a<1 else math.log1p(-math.exp(-n*a))) for n in sizes)

def exact_sphere(N,d,a):
    if N==1:return Fraction(int(a>=1))
    total=Fraction(0)
    for k in range(d+1):
        base=1-k*a/d
        if base>0: total+=(-1)**k*math.comb(d,k)*base**(N-1)
    return total

# 1. Symbolic strict concavity, including the actual expression in the report.
p,a=sp.symbols('p a', positive=True)
h=p*sp.log(1-sp.exp(-a/p))
claimed=-(a/p)**2*sp.exp(a/p)/(p*(sp.exp(a/p)-1)**2)
assert sp.simplify(sp.diff(h,p,2)-claimed)==0
tick('symbolic_second_derivative')

# 2. Exact rational complex isometries, projector diagonals, and real rank-two data.
for N in range(2,9):
    Q=sp.eye(N)
    for k in range(2*N+1):
        i=k%N;j=(k+1+(k//N))%N
        if i==j:j=(j+1)%N
        G=sp.eye(N);c=sp.Rational(3,5);s=sp.Rational(4,5)
        phase=[1,sp.I,-1,-sp.I][k%4]
        G[i,i]=G[j,j]=c;G[i,j]=s*phase;G[j,i]=-s*sp.conjugate(phase)
        Q=(G*Q).applyfunc(sp.expand)
    assert (Q.H*Q).applyfunc(sp.expand)==sp.eye(N)
    for d in sorted(set([1,max(1,N//2),N])):
        V=Q[:,:d];P=(V*V.H).applyfunc(sp.expand)
        assert P.H==P and (P*P).applyfunc(sp.expand)==P and sp.trace(P)==d
        acc=sp.zeros(2*d)
        for j in range(N):
            row=V[j:j+1,:];pj=sp.expand((row*row.H)[0])
            assert pj==P[j,j] and 0<=pj<=1
            if pj==0:tick('exact_zero_leverage_rows');continue
            R=realify(row)
            assert (R*R.T).applyfunc(sp.expand)==pj*sp.eye(2)
            acc+=(R.T*R).applyfunc(sp.expand)
            tick('exact_rank_two_row_checks')
        assert acc.applyfunc(sp.expand)==sp.eye(2*d)
        tick('exact_complex_projectors')
# Explicit zero-leverage datum.
V=sp.eye(7)[:,:3]
assert [int((V*V.H)[i,i]) for i in range(7)]==[1,1,1,0,0,0,0]
tick('explicit_zero_leverage_projector')

# 3. Floating QR datum, product/Jensen monotonicity, arbitrary shifts in scalar disks.
for N in [2,3,5,8,13,21]:
    for d in sorted(set([1,max(1,N//3),max(1,N-1),N])):
        A=rng.normal(size=(N,d))+1j*rng.normal(size=(N,d))
        V=np.linalg.qr(A)[0]
        pp=np.sum(abs(V)**2,axis=1)
        acc=np.zeros((2*d,2*d))
        for row,pj in zip(V,pp):
            R=np.block([[row.real[None,:],-row.imag[None,:]],
                        [row.imag[None,:],row.real[None,:]]])
            Bj=R/math.sqrt(pj)
            note_max('real_coisometry_error',np.max(abs(Bj@Bj.T-np.eye(2))))
            acc+=pj*Bj.T@Bj
        note_max('real_identity_error',np.max(abs(acc-np.eye(2*d))))
        for a0 in [0.03,0.2,0.7,1.0,3.0,12.0]:
            lp=log_leverage(pp,a0);lb=logB(N,d,a0)
            assert lp<=lb+2e-12
            note_max('positive_jensen_roundoff',max(0,lp-lb))
            tick('leverage_jensen_bounds')
        tick('floating_complex_projectors')
for v in [0.001,0.1,0.5,1,3]:
    for r in [0,0.01,0.3,1,4]:
        for shift in [0,0.05,0.7,2,9]:
            exact=ncx2.cdf(2*r*r/v,df=2,nc=2*shift*shift/v)
            bound=-math.expm1(-r*r/v)
            assert exact<=bound+2e-14
            tick('translated_scalar_disks')
for N in [2,7,31,100]:
    for a0 in [.01,.3,1,5]:
        vals=[logB(N,d,a0) for d in range(1,N+1)]
        assert all(vals[i+1]<=vals[i]+2e-14 for i in range(len(vals)-1))
        tick('rank_monotonicity_chains')

# 4. Equal/unequal block probability agrees with refined leverage product.
for N in range(1,65):
    for d in range(1,N+1):
        m,k=divmod(N,d);sizes=[m]*(d-k)+[m+1]*k
        pp=[1/n for n in sizes for _ in range(n)]
        for a0 in [.1,1,2.7]:
            exact=block_logprob(sizes,a0);lev=log_leverage(pp,a0);upper=logB(N,d,a0)
            assert abs(exact-lev)<5e-12
            assert exact<=upper+5e-12
            if k==0:
                assert abs(exact-upper)<5e-12
                tick('equal_block_equalities')
            else:tick('unequal_block_bounds')
            note_max('block_leverage_log_error',exact-lev)

# 5. Gaussian cube Monte Carlo diagnostics: orientations, shifts, zero leverage.
mc=[]
for N,d,r,shift,kind in [
 (5,1,.4,0,'random'),(5,2,.7,.2,'random'),(8,3,1,.2,'random'),
 (10,4,.8,.4,'random'),(7,7,1.2,0,'random'),(6,2,.9,0,'block'),
 (8,4,.6,.1,'block'),(7,3,1,.1,'coordinate')]:
    if kind=='random':
        V=np.linalg.qr(rng.normal(size=(N,d))+1j*rng.normal(size=(N,d)))[0]
    elif kind=='coordinate':V=np.eye(N,d,dtype=complex)
    else:
        V=np.zeros((N,d),dtype=complex)
        for l,ix in enumerate(np.array_split(np.arange(N),d)):V[ix,l]=1/math.sqrt(len(ix))
    b=shift*np.exp(1j*np.arange(N))
    n=160000
    g=(rng.normal(size=(n,d))+1j*rng.normal(size=(n,d)))/math.sqrt(2)
    vals=g@V.T
    estimate=float(np.mean(np.max(abs(vals-b),axis=1)<=r))
    pp=np.sum(abs(V)**2,axis=1)
    upper_lev=0.0 if any(abs(b[j])>r for j in range(N) if pp[j]<1e-15) else math.exp(log_leverage(pp,r*r))
    upper=B(N,d,r*r)
    # Six standard deviations of a Bernoulli mean, with an additive rare-event term.
    tolerance=6*math.sqrt(max(estimate*(1-estimate),1/n)/n)+6/n
    assert estimate<=upper_lev+tolerance
    mc.append(dict(N=N,d=d,r=r,shift=shift,kind=kind,samples=n,estimate=estimate,
                   leverage_upper=upper_lev,ambient_upper=upper,tolerance=tolerance))
    tick('gaussian_cube_monte_carlo_cases')
records['gaussian_cube_monte_carlo']=mc

# 6. Exact sphere inclusion-exclusion controls and an independent Gaussian-ratio simulation.
assert exact_sphere(2,1,Fraction(1))==1
assert exact_sphere(4,2,Fraction(1))==Fraction(3,4)
assert exact_sphere(4,4,Fraction(1))==0
assert exact_sphere(1,1,Fraction(1))==1
sphere=[]
for N,d,a0 in [(4,2,Fraction(1)),(6,2,Fraction(1,2)),(8,4,Fraction(1)),
               (12,3,Fraction(1)),(6,6,Fraction(3,2)),(2,1,Fraction(1))]:
    exact=exact_sphere(N,d,a0)
    assert 0<=exact<=1
    n=180000
    E=rng.exponential(size=(n,N))
    empirical=float(np.mean(np.max(E[:,:d]/E.sum(axis=1)[:,None],axis=1)<=float(a0/d)))
    tol=6*math.sqrt(max(float(exact*(1-exact)),1/n)/n)+6/n
    assert abs(empirical-float(exact))<=tol
    sphere.append(dict(N=N,d=d,C_squared=str(a0),exact_fraction=str(exact),exact=float(exact),
                       empirical=empirical,samples=n,tolerance=tol))
    tick('sphere_inclusion_exclusion_cases')
records['sphere']=sphere

# 7. Exact adaptive branches and redundant queries; no historical checker is run.
N=5
paths=[]
for seed in [0,1]:
    for v0 in [-2,-1,0,1,2]:
        x=sp.Matrix([v0,1+seed*sp.I,-1+sp.I,2-sp.I,sp.Rational(1,2)])
        P=sp.eye(N);mu=sp.zeros(N,1);rows=[];answers=[];path=[]
        e0=sp.eye(N)[:,0]
        candidates=[e0]
        first=e0.dot(x)
        if sp.re(first)>0:
            a=sp.Matrix([0,1,sp.I,0,0])
        else:
            a=sp.Matrix([0,0,1,1+sp.I,0])
        candidates.append(a)
        if seed==1:candidates.append(e0+2*a)  # Redundant transcript-only query.
        second=(a.H*x)[0]
        if abs(second)**2>2:candidates.append(sp.Matrix([0,0,0,0,1]))
        for a in candidates:
            y=sp.simplify((a.H*x)[0]);v=sp.simplify((a.H*P*a)[0])
            rows.append(a.H);answers.append(y)
            oldrank=P.rank()
            if v!=0:
                mu=(mu+P*a*(y-(a.H*mu)[0])/v).applyfunc(sp.simplify)
                P=(P-P*a*a.H*P/v).applyfunc(sp.simplify)
                assert P.rank()==oldrank-1
                path.append('informative')
            else:
                assert sp.simplify(y-(a.H*mu)[0])==0
                path.append('redundant')
            assert (P*P).applyfunc(sp.simplify)==P and P.H==P and (P*mu).applyfunc(sp.simplify)==sp.zeros(N,1)
            A=sp.Matrix.vstack(*rows);ys=sp.Matrix(answers)
            independent=A.rowspace()
            H=sp.Matrix.vstack(*independent)
            Pref=sp.eye(N)-H.H*(H*H.H).inv()*H
            assert sp.simplify(P-Pref)==sp.zeros(N)
            assert (A*mu-ys).applyfunc(sp.simplify)==sp.zeros(len(answers),1)
            assert P.rank()==N-A.rank()
            tick('exact_adaptive_posterior_updates')
        assert P.rank()>=2
        paths.append(dict(seed=seed,input_first=v0,queries=len(candidates),rank_deficit=P.rank(),types=path))
        tick('adaptive_stopping_paths')
records['adaptive_paths']=paths

# 8. Exact block dimensions approaching the critical law, with shrinking norm envelopes.
critical=[]
for C2 in [0.5,1.0,2.0]:
    for target in [-2.0,0.0,2.0]:
        for m in [4,8,16,32,64]:
            d=max(1,round(math.exp(m*C2-target)));N=m*d
            w=N*C2/d-math.log(d)
            fixed=B(N,d,C2)
            eps=N**(-.25)
            low=max(0,B(N,d,C2*(1-eps))-norm_tail(N,eps,False)) if eps<1 else 0
            high=min(1,B(N,d,C2*(1+eps))+norm_tail(N,eps,True)) if eps<1 else 1
            assert low<=fixed+2e-14<=high+2e-14
            target_limit=math.exp(-math.exp(-target))
            critical.append(dict(C_squared=C2,target_w=target,m=m,d=d,N=N,w=w,fixed_probability=fixed,
                                  epsilon=eps,relative_lower=low,relative_upper=high,limit=target_limit))
            if m*C2>=64:
                assert abs(fixed-target_limit)<1e-12
                assert abs(high-target_limit)<1e-5 and abs(low-target_limit)<1e-5
            tick('critical_window_rows')
records['critical_window']=critical

# 9. Nondivisible rounding coefficient is retained, not silently discarded.
rounding=[]
for theta in [.2,.5,.8]:
    for target in [-1,0,1]:
        m=32;d=round(math.exp(m+theta-target));k=round(theta*d);N=m*d+k
        th=k/d;w=N/d-math.log(d)
        A=(1-th)*math.exp(th)+th*math.exp(-(1-th))
        predicted=math.exp(-A*math.exp(-w))
        # Stable large-exponent log factors preserve tiny per-block failure probabilities.
        stable_log=(d-k)*math.log1p(-math.exp(-m))+k*math.log1p(-math.exp(-(m+1)))
        stable=math.exp(stable_log)
        assert abs(stable-predicted)<1e-12
        assert A>=1
        rounding.append(dict(theta=th,w=w,A=A,block_success=stable,limit_prediction=predicted,
                             ambient_bound=math.exp(d*math.log1p(-math.exp(-N/d)))))
        tick('nondivisible_rounding_cases')
records['rounding']=rounding

# 10. First-order transition examples, using stable logs throughout.
transition=[]
for N in [10**4,10**8,10**16,10**32,10**64]:
    for ratio in [.5,1,1.5,2]:
        d=max(1,int(ratio*N/math.log(N)));m,k=divmod(N,d)
        upper=math.exp(d*math.log1p(-math.exp(-N/d)))
        lower=math.exp((d-k)*math.log1p(-math.exp(-m))+k*math.log1p(-math.exp(-(m+1))))
        transition.append(dict(N=N,ratio=ratio,d=d,w=N/d-math.log(d),ambient_fixed_radius=upper,
                               unequal_block_fixed_radius=lower))
        tick('first_order_transition_rows')
records['first_order_transition']=transition

# These normalizations should be within ordinary floating roundoff.
assert residuals['real_coisometry_error']<1e-12
assert residuals['real_identity_error']<1e-12

result=dict(status='PASS',seed=SEED,python=platform.python_version(),numpy=np.__version__,
            scipy=scipy.__version__,sympy=sp.__version__,counts=counts,max_residuals=residuals,
            evidence_policy='Exact finite controls and numerical diagnostics only; proof is REPORT.md.',
            records=records)
Path(__file__).with_name('RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','seed','counts','max_residuals']},indent=2))
