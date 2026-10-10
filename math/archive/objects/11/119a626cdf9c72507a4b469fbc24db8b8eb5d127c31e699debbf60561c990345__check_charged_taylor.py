#!/usr/bin/env python3
"""Fresh, independently authored checks. No uploaded module is executed/imported."""
from fractions import Fraction as F
import json, math, random
from pathlib import Path
import numpy as np
import mpmath as mp
mp.mp.dps=160
ROOT=Path(__file__).resolve().parent

def machin(m):
    def atan(q):
        z=F(1,q); z2=z*z; term=z; total=F(0)
        for j in range(m):
            total += term/F(2*j+1)
            term *= -z2
        return total
    rho=16*atan(5)-4*atan(239)
    err=F(16,(2*m+1)*5**(2*m+1))+F(4,(2*m+1)*239**(2*m+1))
    return rho,err

def mm(f): return mp.mpf(f.numerator)/f.denominator

def nearest(n): # nonnegative rational, round to integer ties to even
    q,r=divmod(n.numerator,n.denominator)
    return q+int(2*r>n.denominator or (2*r==n.denominator and q%2))

def rnd(x,p):
    x=F(x)
    if not x:return x
    sign=1 if x>0 else -1; x=abs(x)
    e=x.numerator.bit_length()-x.denominator.bit_length()
    if x < (F(2)**e):e-=1
    step=F(2)**(e-p+1)
    return sign*nearest(x/step)*step

result={"provenance":"Fresh standalone checker; no uploaded source executed or imported.","machin":[],"kernel":{},"finite_recurrence":{},"lift_and_covariance":[],"ledger":{}}
for m in [1,2,4,8,16,32,64]:
    rho,eta=machin(m); error=abs(mm(rho)-mp.pi)
    assert error<=mm(eta)
    result['machin'].append({'m':m,'certified_bound':float(eta),'error_over_bound':float(error/mm(eta)),'numerator_bits':rho.numerator.bit_length(),'denominator_bits':rho.denominator.bit_length()})

rho,eta=machin(32); q=abs(rho)
rng=random.Random(17012026); worst=0.; cases=0
for R in [1,2,3,4,5,8,12,20,32,48,64]:
    tail=mm(eta)+mm(q**R/F(math.factorial(R)))
    for j in range(200):
        s=mp.mpf(1) if j==0 else mp.mpf(rng.randrange(10001))/10000
        theta=mp.mpf('0.5') if j==0 else mp.mpf(rng.randrange(-5000,5001))/10000
        w=-2j*mm(rho)*s*theta; poly=mp.mpc(1); term=mp.mpc(1)
        for r in range(1,R):term*=w/r;poly+=term
        ratio=abs(mp.exp(-2j*mp.pi*s*theta)-poly)/tail
        assert ratio<=1+mp.mpf('1e-60')
        worst=max(worst,float(ratio));cases+=1
result['kernel']={'sampled_cases':cases,'maximum_error_over_certified_tail':worst}

rec=0; maxratio=0.
for p in [12,24,53]:
    u=F(1,2**p)
    rr=rnd(rho,p)
    for N in [7,31,1009,2**20+1]:
        Q=1<<(N-1).bit_length()
        for n in [0,1,N//2,N-1]:
            s=F(n,Q); ss=rnd(s,p); a=F(1)
            x=rnd(F(17,13),p)
            for r in range(65):
                exact=s**r; y=rnd(x*a,p)
                dy=(1+u)**(2*r+1)-1
                if exact:
                    ratio=abs(y-x*exact)/(abs(x*exact)*dy)
                    assert ratio<=1
                    maxratio=max(maxratio,float(ratio))
                else:assert y==0
                rec+=1;a=rnd(a*ss,p)
        for k in [0,1,N//2,N-1]:
            jk=(2*k*Q+N)//(2*N);th=F(k*Q-jk*N,N);tt=rnd(th,p)
            base=rnd(2*rr*tt,p);b=F(1)
            for r in range(65):
                exact=(2*rho*th)**r/F(math.factorial(r))
                db=(1+u)**(5*r)-1
                if r and exact:
                    ratio=abs(b-exact)/(abs(exact)*db)
                    assert ratio<=1
                    maxratio=max(maxratio,float(ratio))
                else:assert b==exact
                rec+=1;b=rnd(rnd(b*base,p)/F(r+1),p)
result['finite_recurrence']={'exact_rational_checks':rec,'maximum_relative_error_over_bound':maxratio,'precisions':[12,24,53],'rounding':'Exact rational nearest-even binary rounding; unbounded exponent range.'}

rngn=np.random.default_rng(1717)
for N in [3,5,7,10,15,17,23,31]:
    Q=1<<(N-1).bit_length();M=2
    if Q>=16:M=4
    K=Q//M
    js=np.array([(2*k*Q+N)//(2*N) for k in range(N)],dtype=int)
    th=np.array([float(F(k*Q-int(js[k])*N,N)) for k in range(N)])
    sn=np.arange(N)/Q
    U=np.exp(-2j*np.pi*np.outer(np.arange(Q),np.arange(Q))/Q)/math.sqrt(Q)
    UN=np.exp(-2j*np.pi*np.outer(np.arange(N),np.arange(N))/N)/math.sqrt(N)
    x=rngn.normal(size=N)+1j*rngn.normal(size=N);X=np.linalg.norm(x)
    for R in [2,5,10]:
        bs=np.ones((N,R),complex);ys=np.zeros((Q,R),complex);ys[:N,0]=x
        for r in range(1,R):
            bs[:,r]=bs[:,r-1]*(-2j*float(rho)*th)/r
            ys[:N,r]=ys[:N,r-1]*sn
        pk=np.zeros((N,N),complex)
        for r in range(R):pk+=bs[:,r,None]*(sn**r)[None,:]
        center=np.einsum('kn,n,kn->k',np.exp(-2j*np.pi*np.outer(js,np.arange(N))/Q),x,pk)/math.sqrt(N)
        sep=math.sqrt(Q/N)*np.sum(bs*(U@ys)[js,:],axis=1)
        identity=float(np.max(np.abs(center-sep)))
        tau=float(eta+q**R/F(math.factorial(R)))
        trunc=float(np.max(np.abs(center-UN@x))/(tau*X))
        estimates=[];max_shared=0.
        for a in range(1,Q,2):
            for beta in range(Q):
                P=np.zeros((Q,Q),complex)
                for block in range(K):
                    ss=np.array([np.exp(2j*np.pi*((a*(t*(t-1)//2)+(a*M*block+beta)*t)%Q)/Q) for t in range(M)])
                    P[block*M:(block+1)*M,block*M:(block+1)*M]=np.outer(ss.conj(),ss)
                A=U@P
                lifted=math.sqrt(Q/N)*np.sum(bs*(A@ys)[js,:],axis=1)
                combined=math.sqrt(Q/N)*np.einsum('kn,n,kn->k',A[js,:N],x,pk)
                max_shared=max(max_shared,float(np.max(np.abs(lifted-combined))))
                estimates.append(lifted)
        rows=np.array(estimates);meanerr=float(np.max(np.abs(rows.mean(axis=0)-center)))
        variance=np.mean(np.abs(rows-center)**2,axis=0)
        vr=float(np.max(variance)/((M/N)*(1+tau)**2*X**2))
        assert identity<1e-12 and max_shared<1e-12 and meanerr<1e-12
        assert trunc<=1+1e-12 and vr<=1+1e-12
        result['lift_and_covariance'].append({'N':N,'Q':Q,'M':M,'R':R,'states':Q*Q//2,'lift_identity_residual':identity,'shared_state_residual':max_shared,'mean_residual':meanerr,'truncation_ratio':trunc,'variance_ratio':vr})

# Verify the generic deterministic composition ledger with independent adversarial
# bounded perturbations. This supplements, and does not replace, the proof.
maxratio=0.
for trial in range(600):
    N=int(rngn.integers(2,25));Q=1<<(N-1).bit_length();R=int(rngn.integers(1,30));M=2
    t=10**rngn.uniform(-7,-3);delta=10**rngn.uniform(-7,-2);dc=t;eps=10**rngn.uniform(-7,-2)
    C=math.sqrt(Q/N);ER=sum(float(q)**r/math.factorial(r) for r in range(R))
    x=rngn.normal(size=N)+1j*rngn.normal(size=N);X=np.linalg.norm(x)
    # One norm-M row operator, sufficient for the general per-output lemma.
    av=rngn.normal(size=N)+1j*rngn.normal(size=N);av*=M/np.linalg.norm(av)
    s=rngn.random(N);theta=rngn.uniform(-.5,.5);ideal=0j;running=0j
    phase=lambda: np.exp(2j*np.pi*rngn.random())
    for r in range(R):
        y=x*s**r;by=(-2j*float(rho)*theta)**r/math.factorial(r);B=float(q)**r/math.factorial(r)
        yt=y*(1+delta*np.exp(2j*np.pi*rngn.random(N)))
        bt=by+delta*B*phase();ft=av@yt+eps*np.linalg.norm(yt)*phase()
        term=bt*ft;term+=t*abs(term)*phase()
        if r==0:running=term
        else:
            running=running+term+t*(abs(running)+abs(term))*phase()
        ideal+=by*(av@y)
    computed=C*(1+dc)*running;computed+=t*abs(computed)*phase()
    H=(1+dc)*(1+t)**2*(1+t)**(R-1)*(1+delta)**2
    bound=C*ER*(H*eps+M*(H-1))*X
    ratio=abs(computed-C*ideal)/bound
    assert ratio<=1+1e-12;maxratio=max(maxratio,float(ratio))
result['ledger']={'adversarial_bounded_perturbation_cases':600,'maximum_error_over_ledger':maxratio}
result['status']='PASS'
(ROOT/'check_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','machin_cases':len(result['machin']),'kernel':result['kernel'],'finite_recurrence':result['finite_recurrence'],'enumerated_lift_cases':len(result['lift_and_covariance']),'max_variance_ratio':max(d['variance_ratio'] for d in result['lift_and_covariance']),'max_shared_state_residual':max(d['shared_state_residual'] for d in result['lift_and_covariance']),'ledger':result['ledger']},indent=2))
