"""Independent NumPy implementation from the defining sketch algebra, no uploaded code."""
import json, time
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent
SEED = 20261009
TRIALS = 12
REPS = [1, 2, 4, 8, 16, 32]
rng = np.random.default_rng(SEED)

def sigma(M, K, a, b, d):
    t = np.arange(M, dtype=np.int64)
    r = np.arange(K, dtype=np.int64)
    phase = (a * t[None,:]**2 + (b + d*r[:,None])*t[None,:]) % M
    return np.exp(2j*np.pi*phase/M)

def reconstruct(x, s):
    y = np.sum(s*x, axis=1)
    return np.fft.fft((np.conj(s)*y[:,None]).ravel(), norm='ortho')

def signals(M,K):
    t=np.arange(M); r=np.arange(K)
    flat=np.ones((K,M),complex)
    mode=np.broadcast_to(np.exp(2j*np.pi*7*t/M),(K,M)).copy()
    phase=np.exp(2j*np.pi*rng.random((K,M)))
    spike=np.zeros((K,M),complex); spike[K//2,M//3]=1
    adversary=np.zeros((K,M),complex)
    # Fixed before drawing sketches: three coherent blocks aligned to seed a=1,b=0,d=1.
    adversary[:min(3,K)] = np.conj(sigma(M,K,1,0,1)[:min(3,K)])
    return {'flat':flat,'repeated_local_mode':mode,'random_phase':phase,
            'spike':spike,'fixed_coherent_three_blocks':adversary}

def resonance_checks():
    checks=[]
    for M in [16,64,256]:
      for K in [2,4,8]:
       if K>=M: continue
       for a,b,d in [(1,0,1),(3,5,7),(M-1,8,M-3)]:
        h=pow(d,-1,M); q=(2*a*h)%M
        out=reconstruct(np.ones((K,M)),sigma(M,K,a,b,d))
        actual=out[q*K]/np.sqrt(K*M)
        active=np.arange(K)[(b+d*np.arange(K))%2==0]
        predicted=(2/K)*np.exp(2j*np.pi*((a*h*h+b*h)%M)/M)*np.sum(np.exp(2j*np.pi*active/M))
        predicted_abs=2*np.sin(np.pi*K/M)/(K*np.sin(2*np.pi/M))
        checks.append({'M':M,'K':K,'a':a,'b':b,'d':d,'alias_q':q,
                       'complex_error':float(abs(actual-predicted)),
                       'magnitude_error':float(abs(abs(actual)-predicted_abs))})
    assert max(v['complex_error'] for v in checks)<1e-11
    assert max(v['magnitude_error'] for v in checks)<1e-11
    return checks

start=time.monotonic()
records=[]
checks=resonance_checks()
for family,M in [('dyadic_odd_a_odd_affine_d',256),('prime_uniform_a_b_d_including_zero',251)]:
 for K in [4,16,32]:
  xs=signals(M,K)
  truths={name:np.fft.fft(x.ravel(),norm='ortho') for name,x in xs.items()}
  scales={name:float(np.sum(abs(x))/np.sqrt(M*K)) for name,x in xs.items()}
  norms={name:float(np.linalg.norm(x)) for name,x in xs.items()}
  for scheme in ['shared_d_zero','affine_d_random']:
   metrics={}
   for trial in range(TRIALS):
    estimates={name:[] for name in xs}
    for j in range(max(REPS)):
     a=int(rng.integers(M//2))*2+1 if family.startswith('dyadic') else int(rng.integers(M))
     b=int(rng.integers(M))
     d=0 if scheme=='shared_d_zero' else (int(rng.integers(M//2))*2+1 if family.startswith('dyadic') else int(rng.integers(M)))
     s=sigma(M,K,a,b,d)
     for name,x in xs.items(): estimates[name].append(reconstruct(x,s))
    for name,es in estimates.items():
     es=np.array(es)
     for R in REPS:
      for aggregation in ['complex_mean','coordinate_median']:
       z=es[:R].mean(axis=0) if aggregation=='complex_mean' else np.median(es[:R].real,axis=0)+1j*np.median(es[:R].imag,axis=0)
       err=z-truths[name]
       key=(name,R,aggregation)
       metrics.setdefault(key,[]).append([float(np.max(abs(err))/scales[name]),float(np.sqrt(np.mean(abs(err)**2))/scales[name]),float(np.linalg.norm(err)/norms[name])])
   for (name,R,agg),values in metrics.items():
    ar=np.array(values)
    records.append({'family':family,'M':M,'K':K,'N':M*K,'scheme':scheme,'input':name,'repetitions':R,'aggregation':agg,'trials':TRIALS,
       'normalized_max_error':{'median':float(np.median(ar[:,0])),'p90':float(np.quantile(ar[:,0],.9)),'min':float(ar[:,0].min()),'max':float(ar[:,0].max())},
       'normalized_rms_error_median':float(np.median(ar[:,1])),
       'relative_l2_error_median':float(np.median(ar[:,2])),
       'trial_metrics_max_rms_relative_l2':values})
res={'seed':SEED,'runtime_seconds':time.monotonic()-start,'reference_decoder':'full unitary N-point FFT of conjugate(sigma)*sketch, NOT a fast algorithm','normalization':'max and RMS absolute errors divided by ||x||_1/sqrt(N); relative L2 = ||error||_2/||x||_2','resonance_checks':checks,'results':records}
(OUT/'results.json').write_text(json.dumps(res,indent=2))
print('runtime',res['runtime_seconds'],'rows',len(records),'resonance max discrepancy',max(c['complex_error'] for c in checks))
for z in records:
 if z['K']==16 and z['repetitions'] in [1,32]:
  print(z['family'],z['scheme'],z['input'],z['repetitions'],z['aggregation'],'max',round(z['normalized_max_error']['median'],4),'rms',round(z['normalized_rms_error_median'],4),'l2',round(z['relative_l2_error_median'],4))
