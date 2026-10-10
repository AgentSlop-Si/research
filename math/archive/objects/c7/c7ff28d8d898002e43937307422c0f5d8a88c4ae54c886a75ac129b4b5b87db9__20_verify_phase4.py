#!/usr/bin/env python3
"""Independent Phase 4 verification of the coprime padding and exact covariance.

The only full-length FFT here is the independent oracle for tests; the
proposed executor uses the prior Green-cycle decoder and short gridding FFTs.
"""
from __future__ import annotations
import json,math,time,pathlib
import numpy as np
from coprime_pad import build_plan,profile
from gaussian_lift import gaussian_robust,work_profile,stronger_local_noise_budget,GaussianPlan
from composite_cycle_core import ChirpState, materialize_projected_signal

RNG=np.random.default_rng(20261010)
ROOT=pathlib.Path(__file__).resolve().parent


def totient(x):
    out=x;v=x;prime=2
    while prime*prime<=v:
        if v%prime==0:
            out=out//prime*(prime-1)
            while v%prime==0:v//=prime
        prime+=1
    if v>1:out=out//v*(v-1)
    return out


def covariance_matrix(n,q,m,sigma2,k):
    """An independent Gram-matrix derivation; no FFT or projected row calls."""
    assert q>=4*n and q%m==0 and q//m>=m
    center=(n-1)//2
    src=(np.arange(n,dtype=int)-center)%q
    tsrc=np.where(src<=(q-1)//2,src,src-q)/q
    xi=k*q/n
    units=[a for a in range(1,q) if math.gcd(a,q)==1]
    cov=np.zeros((n,n),dtype=np.complex128)
    for d in range(-m+1,m):
        if not d:continue
        out=src+d
        valid=(out>=0)&(out<q)&(src//m==out//m)
        if not valid.any():continue
        dst=out[valid]
        tdst=np.where(dst<=(q-1)//2,dst,dst-q)/q
        srcv=src[valid]
        vbase=np.exp(math.pi*sigma2*(tsrc[valid]**2-tdst**2))*np.exp(-2j*np.pi*xi*tdst)
        for a in units:
            vec=np.zeros(n,dtype=np.complex128)
            vec[valid]=vbase*np.exp(-2j*np.pi*a*d*srcv/q)
            cov += np.outer(vec.conjugate(),vec)
    cov/=n*len(units)
    assert np.linalg.norm(cov-cov.conj().T)<1e-12
    return cov


def direct_projector_covariance(n,q,m,sigma2,k,x):
    center=(n-1)//2
    src=(np.arange(n)-center)%q
    allindices=np.arange(q)
    t=np.where(allindices<=(q-1)//2,allindices,allindices-q)/q
    g=np.exp(math.pi*sigma2*t*t)/math.sqrt(sigma2)
    z=np.zeros(q,dtype=np.complex128)
    z[src]=x*g[src]
    xi=k*q/n
    row=np.exp(-2j*np.pi*xi*t)/g/math.sqrt(n)
    units=[a for a in range(1,q) if math.gcd(a,q)==1]
    acc=0.;mean=0j;cnt=0
    for a in units:
        for beta in range(q):
            projected=materialize_projected_signal(z,m,ChirpState(a,beta))
            er=np.dot(row,projected-z)
            acc+=abs(er)**2
            mean+=er
            cnt+=1
    return acc/cnt,mean/cnt,cnt


def verify_exact_covariance():
    cases=[]
    for n,q,m,sigma2,k in [(11,55,5,8.0,3),(17,85,5,8.0,5),(23,115,5,12.0,7)]:
        assert q//m>=m and q>=4*n
        assert all(math.gcd(q,d)==1 for d in range(1,m))
        xx=RNG.normal(size=n)+1j*RNG.normal(size=n)
        cov=covariance_matrix(n,q,m,sigma2,k)
        gram=float((np.vdot(xx,cov@xx)).real)
        empirical,mean,cnt=direct_projector_covariance(n,q,m,sigma2,k,xx)
        tau=max((n-1)//2,n-1-(n-1)//2)/q
        ratio=math.exp(math.pi*sigma2*(2*tau*m/q+(m/q)**2))
        bound=q/n*ratio**2*(m-1)/totient(q)
        eigmax=float(np.linalg.eigvalsh(cov)[-1]);norm=float(np.linalg.norm(xx)**2)
        assert abs(gram-empirical)<=max(1e-9,1e-10*gram), (gram,empirical)
        assert abs(mean)<1e-11,(n,mean)
        assert eigmax<=bound*(1+1e-11),(n,eigmax,bound)
        cases.append(dict(n=n,q=q,m=m,phi_q=totient(q),states=cnt,
            gram_expectation=gram,exhaustive_expectation=empirical,
            relative_agreement=abs(gram-empirical)/max(gram,1e-300),
            maximum_covariance_eigenvalue=eigmax,improved_norm_bound=bound,
            worstcase_covariance_to_bound=eigmax/bound,
            legacy_bound_same_padding=bound*m))
    return cases


def verify_padding():
    ns=[67,127,257,509,1009,2003,4093,10007,20011,100003,1000003]
    result=[]
    for n in ns:
        p=build_plan(n)
        for d in range(1,p.m):assert math.gcd(p.q,d)==1
        oldq=p.m*math.ceil(4*n/p.m)
        assert p.q>=oldq
        assert p.slack<p.q//5 or n<128  # asymptotic valid; actual small gaps
        coeff=(p.q/n)*math.exp(2*math.pi*p.sigma2*(2*p.tau*p.m/p.q+(p.m/p.q)**2))
        improved=coeff*(p.m-1)/totient(p.q)
        legacy=coeff*p.m*(p.m-1)/totient(p.q)
        result.append({**profile(n),'phi_q':totient(p.q),
                       'covariance_upper_bound':improved,
                       'legacy_covariance_upper_bound':legacy,
                       'proven_ratio':legacy/improved})
    return result


def verify_end_to_end():
    results=[]
    for n in [127,257,509,1009,2003,4093,10007]:
        plan=build_plan(n,halfwidth=max(12,math.ceil(math.log(n)/4)),
                        sigma2=max(12,math.ceil(math.log(n)/4)))
        x=RNG.normal(size=n)+1j*RNG.normal(size=n)
        for kind in ['random','impulse']:
            xx=x if kind=='random' else np.eye(1,n,n//2,dtype=complex).reshape(-1)
            t=time.perf_counter()
            y=gaussian_robust(xx,plan,rows=7,seed=20261010)
            sec=time.perf_counter()-t
            ref=np.fft.fft(xx)/math.sqrt(n)
            err=float(np.max(abs(y-ref))/np.linalg.norm(xx))
            assert np.all(np.isfinite(y)),(n,kind)
            assert err < max(.5,4*n**(-1/3)),(n,kind,err)
            wp=work_profile(plan,rows=7)
            results.append({'n':n,'kind':kind,'q':plan.q,'m':plan.m,
                            'max_error_over_x_norm2':err,
                            'comparison_N_minus_one_third':n**(-1/3),
                            'seconds':sec,'small_fft_length':wp['fir_fft_size'],
                            'green_fft_length':plan.k,'segments':wp['number_of_segments']})
    return results


def main():
    time0=time.perf_counter()
    results={}
    for name,fn in [('padding',verify_padding),('exact_covariance',verify_exact_covariance),('end_to_end',verify_end_to_end)]:
        t=time.perf_counter();results[name]=fn()
        print('PASS',name,'time',round(time.perf_counter()-t,2),'s',flush=True)
    results['total_seconds']=time.perf_counter()-time0
    (ROOT/'verification_phase4.json').write_text(json.dumps(results,indent=2))
    print(json.dumps({'covariance':results['exact_covariance'],
                      'end_to_end_random':[r for r in results['end_to_end'] if r['kind']=='random'],
                      'total_seconds':results['total_seconds']},indent=2))

if __name__=='__main__':main()
