#!/usr/bin/env python3
"""Composite-modulus independent identity, covariance, and accuracy audits."""
import math,time,json
from pathlib import Path
import numpy as np
import composite_cycle_core as c
import composite_lift as cl
from composite_explore import mu,totient,profile

ROOT=Path(__file__).parent


def assert_close(actual,expected,tol=2e-10,desc=''):
    err=float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
    if err>tol:raise AssertionError(f'{desc} error={err} tolerance={tol}')
    return err


def recurrence_check(n,m,seed):
    rng=np.random.default_rng(seed)
    x=rng.standard_normal(n)+1j*rng.standard_normal(n)
    s=c.draw_state(n,rng)
    # A single FFT over an n-long projected materialized vector is a
    # deliberately slow independent oracle, not the claimed fast runtime.
    d=c.compress_blocks(x,m,s)
    from_green=c.decode_balanced_scan(d,n,m,s)
    direct=np.fft.fft(c.materialize_projected_signal(x,m,s))/math.sqrt(n)
    e=assert_close(from_green,direct,tol=2e-9,desc=f'composite length {n}')
    return {'n':n,'m':m,'K':n//m,'a':s.a,'beta':s.beta,
            'direct_vs_greencycle_max_abs_error':e}


def covariance_empirical_vs_formula(n,m,k):
    tsets=[set(range(-t,m-t))-{0} for t in range(m)]
    pred=np.zeros((n,n),dtype=np.complex128)
    for i in range(n):
        for j in range(n):
            rho_sum=0.
            for d in tsets[i%m] & tsets[j%m]:
                z=n//math.gcd(n,d*(i-j))
                rho_sum+=mu(z)/totient(z)
            pred[i,j]=np.exp(2j*np.pi*k*(i-j)/n)*rho_sum/n
    # Formula's convention may be conjugate depending on row indexing; test
    # spectral norms independently even if phases differ by conjugation.
    outrow=np.exp(-2j*np.pi*k*np.arange(n)/n)/math.sqrt(n)
    real=np.zeros((n,n),dtype=np.complex128)
    means=np.zeros(n,dtype=np.complex128)
    count=0
    for a in range(1,n):
        if math.gcd(a,n)!=1:continue
        for beta in range(n):
            ss=c.local_phase_matrix(n,m,c.ChirpState(a,beta))
            product=(np.conj(ss)*np.sum(outrow.reshape(-1,m)*ss,axis=1)[:,None]).reshape(-1)
            e=product-outrow
            real+=np.outer(np.conj(e),e)
            means+=e
            count+=1
    real/=count;means/=count
    vactual=float(np.linalg.eigvalsh(real)[-1]);vpred=float(np.linalg.eigvalsh(pred)[-1]);upper=m*(m-1)/cl.totient(n)
    e1=assert_close(vactual,vpred,3e-11,f'{n} eig')
    # Check entrywise as well after numerical convention selection.
    ep=min(float(np.max(np.abs(real-pred))),float(np.max(np.abs(real-pred.conj()))))
    if ep>1e-10:raise AssertionError(f'{n} entrywise covariance formula error={ep}')
    if vactual>upper+1e-11:raise AssertionError(f'{n} variance bound failed: {vactual}>{upper}')
    eavg=float(np.max(np.abs(means)))
    if eavg>1e-11:raise AssertionError(f'{n} estimator biased')
    return {'n':n,'m':m,'k':k,'enumerated_states':count,
            'actual_covariance_max_eigenvalue':vactual,
            'analytic_covariance_max_eigenvalue':vpred,
            'proved_general_upper_bound':upper,
            'actual_to_prime_power_M_over_N':vactual/(m/n),
            'unbiasedness_row_coefficient_error':eavg,
            'max_covariance_entry_formula_error':ep}


def accuracy(n,rows,seed,kind):
    plan=cl.CompositePlan.build(n)
    rng=np.random.default_rng(seed)
    if kind=='complex_dense':x=rng.standard_normal(n)+1j*rng.standard_normal(n)
    elif kind=='flat':x=np.ones(n,dtype=np.complex128)
    elif kind=='spike':
        x=np.zeros(n,dtype=np.complex128);x[n//2]=1
    elif kind=='sinusoid':x=np.exp(2j*np.pi*17*np.arange(n)/n)
    elif kind=='alternating':x=(-1)**np.arange(n).astype(np.float64)
    else:raise ValueError(kind)
    start=time.perf_counter()
    guess=cl.robust_estimate(x,plan,rows,seed)
    runtime=time.perf_counter()-start
    err=np.max(abs(guess-cl.reference(x)))
    return {'n':n,'m':plan.m,'k':plan.k,'rows':rows,'kind':kind,
            'max_abs_error':float(err),'relative_to_l2_norm':float(err/np.linalg.norm(x)),
            'runtime_sec':runtime,'bound_variance_per_output':float(cl.variance_bound(x,plan))}


def broad_composite_fuzzer(max_n=600):
    """One independent oracle comparison for every usable composite factor pair."""
    rng=np.random.default_rng(20261009)
    cases=0
    worst=0.0
    hardest=None
    odd_composites=0
    for n in range(4,max_n+1):
        valid=[m for m in range(2,math.isqrt(n)+1) if n%m==0]
        if not valid:continue
        # Test up to three different block divisors, including extremes.
        tests=sorted(set([valid[0],valid[-1],valid[len(valid)//2]]))
        x=rng.normal(size=n)+1j*rng.normal(size=n)
        for m in tests:
            state=c.draw_state(n,rng)
            lhs=c.one_row_estimate(x,m,state)
            rhs=np.fft.fft(c.materialize_projected_signal(x,m,state))/math.sqrt(n)
            err=float(np.max(np.abs(lhs-rhs)))
            worst=max(worst,err)
            if err>1e-9:raise AssertionError(f'fuzzer failed n={n} m={m} err={err}')
            if (n%2)==1:odd_composites+=1
            hardest=(n,m) if err==worst else hardest
            cases+=1
    return {'max_n':max_n,'checked_factor_pairs':cases,'odd_length_pairs':odd_composites,
            'max_absolute_recursion_error':worst,'worst_case_pair':hardest}


def run():
    checks={}
    checks['broad_modulus_fuzz']=[broad_composite_fuzzer(600)]
    checks['greencycle_direct_oracle']=[recurrence_check(n,m,seed)
            for n,m,seed in [(12,3,31),(30,5,32),(60,6,33),(90,6,34),
                             (120,10,35),(210,14,36),(840,10,37),(3600,12,38),(20736,16,39)]]
    checks['full_covariance_enumeration']=[covariance_empirical_vs_formula(n,m,k)
            for n,m,k in [(12,3,1),(18,3,4),(30,5,7),(36,4,2),(60,6,7)]]
    checks['empirical_error']=[accuracy(n,9,seed,kind) for n,seed,kind in
           [(840,50,'complex_dense'),(3600,51,'complex_dense'),(3600,52,'flat'),
            (3600,53,'spike'),(3600,54,'sinusoid'),(3600,55,'alternating'),
            (20736,56,'complex_dense')]]
    checks['general_ratios']=[profile(n,m) for n,m in [(60,5),(60,6),(90,9),(120,10),(180,12),(210,14),(240,15)]]
    (ROOT/'composite_results.json').write_text(json.dumps(checks,indent=2)+'\n')
    print({k:len(v) for k,v in checks.items()})
    for r in checks['empirical_error']:
        print('n',r['n'],'m',r['m'],r['kind'],
              'relative_error',f"{r['relative_to_l2_norm']:.5f}",
              'runtime',f"{r['runtime_sec']:.3f}s")

if __name__=='__main__':run()
