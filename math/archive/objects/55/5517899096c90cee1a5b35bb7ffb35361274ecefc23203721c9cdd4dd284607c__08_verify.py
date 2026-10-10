#!/usr/bin/env python3
"""Independent checks of the proposed offset-class chirp lift."""
import json,math,sys,time
from pathlib import Path
import numpy as np
import mpmath as mp
import offset_class_lift as oc
import unit_step_core as core

OUT=Path(__file__).parent

def assert_le(a,b,msg):
    if not (a<=b):raise AssertionError(f'{msg}: {a} > {b}')

def numerical_cycle_projection_check(n,m,seed,radix=2):
    rng=np.random.default_rng(seed)
    plan=oc.OffsetPlan.build(n,m,radix=radix)
    x=rng.normal(size=n)+1j*rng.normal(size=n)
    state=core.draw_state(plan.q,rng)
    estimate=oc.row_estimate(x,plan,state)
    ref=np.empty(n,dtype=np.complex128)
    padded=np.zeros(plan.q,dtype=np.complex128)
    for t,ks in plan.classes():
        phase=np.exp(-2j*np.pi*(t/plan.n)*np.arange(n)/plan.q)
        padded[:n]=x*phase
        spec=core.direct_row_estimate(padded,plan.m,state)
        ref[ks]=math.sqrt(plan.q/plan.n)*spec[plan.indices[ks]]
    err=float(np.max(np.abs(estimate-ref)))
    assert_le(err,5e-10,f'n={n} Green recurrence mismatch')
    return {'n':n,'q':plan.q,'m':m,'classes':plan.cofactor,'projector_direct_fft_max_diff':err}

def high_precision_identity(n,dps=75):
    mp.mp.dps=dps
    q=oc.next_power_of_two(n)
    rnd=np.random.default_rng(4100+n)
    x=[mp.mpc(int(a),int(b)) for a,b in zip(rnd.integers(-5,6,n),rnd.integers(-5,6,n))]
    biggest=mp.mpf(0)
    for k in range(n):
        j=(2*k*q+n)//(2*n)
        theta=mp.mpf(k*q-j*n)/n
        a=mp.fsum(x[t]*mp.exp(-2j*mp.pi*k*t/n) for t in range(n))/mp.sqrt(n)
        b=mp.sqrt(mp.mpf(q)/n)*mp.fsum(x[t]*mp.exp(-2j*mp.pi*(j+theta)*t/q) for t in range(n))/mp.sqrt(q)
        biggest=max(biggest,abs(a-b))
    assert biggest < mp.mpf('1e-65'),f'High precision modulation identity failed at n={n}: {biggest}'
    return {'n':n,'q':q,'precision_digits':dps,'maximum_modulation_identity_error':mp.nstr(biggest,7)}

def covariance_eig_by_full_enumeration(q,m,frequency=1):
    """Directly enumerate all (a,beta) states, derive one-output error rows."""
    rng=np.random.default_rng(1)
    _=rng
    coeffs=np.exp(-2j*np.pi*frequency*np.arange(q)/q)/math.sqrt(q)
    cov=np.zeros((q,q),dtype=np.complex128)
    count=0
    mean=np.zeros(q,dtype=np.complex128)
    for a in range(1,q):
        if math.gcd(a,q)!=1:continue
        for beta in range(q):
            phase=core.local_phase_matrix(q,m,core.ChirpState(a,beta))
            # (U_q[k,:] P)[bM+t] = conj(phase[b,t]) sum_u U[k,bM+u]*phase[b,u]
            product=np.conj(phase)*np.sum(coeffs.reshape(-1,m)*phase,axis=1)[:,None]
            error=product.reshape(-1)-coeffs
            cov+=np.outer(np.conj(error),error)
            mean+=error
            count+=1
    cov/=count;mean/=count
    ev=np.linalg.eigvalsh(cov)
    k=q//m
    eigerr=max(abs(ev[-1]-m/q),abs(ev[0]))
    assert_le(abs(ev[-1]-m/q),5e-12,'Covariance max eig wrong')
    assert_le(abs(ev[k]-m/q),5e-12,'Covariance nonzero eig wrong')
    assert_le(abs(ev[k-1]),5e-12,'Covariance zero eig wrong')
    assert_le(float(np.max(abs(mean))),5e-12,'Estimator not unbiased')
    return {'q':q,'m':m,'enumerated_states':count,'frequency':frequency,'min_eig':float(ev[0]),'max_eig':float(ev[-1]),'predicted_max_eig':m/q,'max_abs_mean_error_coefficient':float(np.max(abs(mean))),'eig_error':float(eigerr)}

def lift_full_state_covariance(n,m,radix,k):
    """Directly enumerate projected ORIGINAL length-n linear rows (not only Q core)."""
    plan=oc.OffsetPlan.build(n,m,radix=radix)
    q=plan.q
    j=int(plan.indices[k]);theta=int(plan.theta_numerators[k])/n
    u_q=np.exp(-2j*np.pi*j*np.arange(q)/q)/math.sqrt(q)
    u_n=np.exp(-2j*np.pi*k*np.arange(n)/n)/math.sqrt(n)
    mod=np.exp(-2j*np.pi*theta*np.arange(n)/q)
    cov=np.zeros((n,n),dtype=np.complex128)
    avg=np.zeros(n,dtype=np.complex128)
    count=0
    for a in range(1,q):
        if math.gcd(a,q)!=1:continue
        for beta in range(q):
            phase=core.local_phase_matrix(q,m,core.ChirpState(a,beta))
            projected_row=(np.conj(phase)*np.sum(u_q.reshape(-1,m)*phase,axis=1)[:,None]).reshape(-1)
            row=math.sqrt(q/n)*projected_row[:n]*mod
            e=row-u_n
            cov+=np.outer(np.conj(e),e)
            avg+=e
            count+=1
    cov/=count;avg/=count
    max_eig=float(np.linalg.eigvalsh(cov)[-1]);upper=m/n
    assert_le(max_eig,upper+1e-12,'Full-lift variance ceiling')
    assert_le(float(np.max(np.abs(avg))),1e-12,'Full-lift unbiasedness')
    return {'n':n,'q':q,'m':m,'radix':radix,'k':k,'states':count,
            'worst_eigenvalue':max_eig,'uniform_upper_bound':upper,
            'max_mean_coefficient_error':float(np.max(np.abs(avg)))}

def empirical_accuracy(n,rows,seed,kind='random_complex',radix=2):
    rng=np.random.default_rng(seed)
    plan=oc.OffsetPlan.build(n,radix=radix)
    if kind=='random_complex':
        x=rng.normal(size=n)+1j*rng.normal(size=n)
    elif kind=='flat':
        x=np.ones(n,dtype=np.complex128)
    elif kind=='spike':
        x=np.zeros(n,dtype=np.complex128);x[n//3]=1
    elif kind=='sinusoid':
        x=np.exp(2j*np.pi*17*np.arange(n)/n)
    else:raise ValueError(kind)
    start=time.perf_counter()
    y=oc.robust_estimate(x,plan,rows,seed)
    dt=time.perf_counter()-start
    gold=oc.reference(x)
    err=np.max(np.abs(y-gold));norm=np.linalg.norm(x)
    return {'n':n,'q':plan.q,'m':plan.m,'h':plan.cofactor,'rows':rows,'kind':kind,'max_normalized_error':float(err/norm),'absolute_max_error':float(err),'elapsed_seconds':dt,'math_per_row_variance_ceiling':float(oc.expected_variance_ceiling(x,plan)),'n_minus_one_third':float(n**(-1/3))}

def main():
    checks={}
    checks['offset_class_counts']=[{'n':n,'h':oc.OffsetPlan.build(n).cofactor,'distinct_offsets':len(oc.OffsetPlan.build(n).classes())} for n in [1,2,3,15,32,96,127,192,768,1000,1280,1792,3072,4096]]
    checks['phase_identity_high_precision']=[high_precision_identity(n) for n in [7,15,21,45]]
    checks['dyadic_projection_equivalence']=[numerical_cycle_projection_check(n,m,seed) for n,m,seed in [(96,4,11),(192,8,19),(768,8,23),(1280,8,31),(1792,8,42)]]
    checks['odd_prime_projection_equivalence']=[numerical_cycle_projection_check(486,9,43,radix=3)]
    checks['full_state_covariance_enumeration']=[covariance_eig_by_full_enumeration(q,m,freq) for q,m,freq in [(16,2,1),(16,4,3),(32,4,7),(27,3,5)]]
    checks['lift_full_state_covariance']=[lift_full_state_covariance(n,m,p,k) for n,m,p,k in [(12,2,2,1),(12,2,2,7),(18,3,3,7)]]
    checks['empirical_accuracy']=[empirical_accuracy(n,rows,seed,kind) for (n,rows,seed,kind) in [(486,9,30,'random_complex'),(768,9,31,'random_complex'),(768,9,31,'flat'),(768,9,31,'spike'),(768,9,31,'sinusoid'),(1280,9,32,'random_complex'),(1792,9,33,'random_complex'),(3072,9,34,'random_complex')]]
    checks['radix3_accuracy']=[empirical_accuracy(n,9,62,'random_complex',radix=p) for n,p in [(486,3),(1458,3),(2*5**4,5)]]
    checks['radix3_demo']=[{'n':n,'base':p,'q':oc.OffsetPlan.build(n,radix=p).q,'m':oc.OffsetPlan.build(n,radix=p).m,'h':oc.OffsetPlan.build(n,radix=p).cofactor} for n,p in [(486,3),(1458,3),(2*5**4,5),(5*3**5,3),(3*2**9,2)]]
    checks['asymptotic_failure_exponents']=[{'alpha':a,'rows':r,'majority':(r+1)//2,'n_exponent':1-((r+1)//2)*(1-2*a)} for a,r in [(1/4,7),(1/3,7),(1/3,9),(2/5,13)]]
    (OUT/'results.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps({k:len(v) for k,v in checks.items()},indent=2))
    for el in checks['empirical_accuracy']:
        print(f"N={el['n']} h={el['h']} {el['kind']} normalized_error={el['max_normalized_error']:.5e} time={el['elapsed_seconds']:.3f}s")

if __name__=='__main__':main()
