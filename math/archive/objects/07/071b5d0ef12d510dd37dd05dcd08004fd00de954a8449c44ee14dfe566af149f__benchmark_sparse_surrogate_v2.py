from __future__ import annotations
import json, math, time
from pathlib import Path
import numpy as np

from sparse_surrogate import (
    accuracy_tradeoff, make_head_tail_plan, plan_head_tail,
    approximate_dft_all_head_tail, flat_natural_scale_support_lower_bound,
    sparse_surrogate_linf_lower_bound,
)

OUT={}

# 1. Pure theorem tradeoff. Use powers of two so it maps directly to the backend.
rows=[]
for p in [12,16,20,24,32,48,64,96,128]:
    n=1<<p
    ln=math.log(n)
    delta=n**-2
    schedules={
        'eps=0.5':0.5,
        'eps=1/sqrt(logN)':1/math.sqrt(ln),
        'eps=1/logN':1/ln,
        'eps=exp(-sqrt(logN))':math.exp(-math.sqrt(ln)),
    }
    for name,eps in schedules.items():
        plan=accuracy_tradeoff(n,eps,delta)
        rows.append({
            'log2N':p,'schedule':name,'epsilon':eps,'delta':delta,
            'k':plan.samples,'log2_b':plan.inner_log2,
            'depth_ratio':plan.depth_ratio,
            'k_over_N_log10': math.log10(plan.samples)-p*math.log10(2),
        })
OUT['accuracy_tradeoff']=rows

# 2. Head/tail planning on a few signal families.
n=2**16
rng=np.random.default_rng(20261009)
inputs={
    'flat':np.ones(n,dtype=np.complex128),
    'gaussian':rng.normal(size=n)+1j*rng.normal(size=n),
    'power_0.8':np.exp(2j*np.pi*rng.random(n))/(np.arange(n)+1.0)**0.8,
    'power_1.2':np.exp(2j*np.pi*rng.random(n))/(np.arange(n)+1.0)**1.2,
    'exponential':np.exp(2j*np.pi*rng.random(n))*np.exp(-0.08*np.arange(n)),
    'spikes_plus_noise':(0.003*(rng.normal(size=n)+1j*rng.normal(size=n))),
}
inputs['spikes_plus_noise'][:32]+=np.linspace(20,3,32)*np.exp(2j*np.pi*rng.random(32))

head_rows=[]
eps=.18; delta=.02
for name,x in inputs.items():
    base=make_head_tail_plan(x,eps,delta,0)
    best=plan_head_tail(x,eps,delta,max_head=512)
    record={
        'name':name,'plain_support_bound':base.support_upper_bound,
        'best_head':best.head_size,'best_samples':best.requested_samples,
        'best_support_bound':best.support_upper_bound,
        'tail_ratio':best.tail_ratio,
        'support_reduction':(base.support_upper_bound/max(1,best.support_upper_bound)),
        'method':best.method,
    }
    # One numerical validation if the predicted support is still sparse enough.
    t0=time.perf_counter()
    out,p=approximate_dft_all_head_tail(x,eps,delta,plan=best,rng=np.random.default_rng(7),return_plan=True)
    t1=time.perf_counter()
    ref=np.fft.fft(x,norm='ortho')
    target=eps*np.linalg.norm(x,1)/math.sqrt(n)
    record.update({
        'observed_error':float(np.max(np.abs(out-ref))),
        'target_bound':float(target),
        'error_over_bound':float(np.max(np.abs(out-ref))/target if target else 0),
        'wall_ms':1000*(t1-t0),
    })
    head_rows.append(record)
OUT['head_tail']=head_rows

# 3. Rigorous sparse-surrogate ceiling on flat inputs.
ceil_rows=[]
n=2**20
for eta in [0.9,0.75,0.5,0.25,0.1,0.01]:
    k=flat_natural_scale_support_lower_bound(n,eta)
    ceil_rows.append({'eta':eta,'required_k':k,'required_fraction':k/n})
OUT['flat_natural_scale_ceiling']=ceil_rows

# Lower bound curve for k=N^alpha on a normalized flat vector.
lb=[]
# Formula avoids allocating 2^20 vector: error >= sqrt(1-k/N)/sqrt(N) for ||x||2=1.
for alpha in [0,0.1,0.25,0.5,0.75,0.9,0.99]:
    k=max(1,int(round(n**alpha)))
    natural_ratio=math.sqrt(max(0.0,1-k/n)) # lower bound divided by ||x||2/sqrt(N)
    lb.append({'alpha':alpha,'k':k,'k_fraction':k/n,'lower_bound_over_natural_scale':natural_ratio})
OUT['flat_lower_bound_curve']=lb

Path('benchmark_sparse_surrogate_v2_results.json').write_text(json.dumps(OUT,indent=2))
print(json.dumps(OUT,indent=2))
