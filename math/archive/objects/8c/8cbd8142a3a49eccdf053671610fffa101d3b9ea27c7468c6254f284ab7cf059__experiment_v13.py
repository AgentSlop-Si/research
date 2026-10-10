"""Reproduce analytic cost proxies and deterministic numerical checks for v13.

Proxy arithmetic is not library-level wall-time. All exact Fourier identities
are independent of the randomized sketching proposal.
"""
from pathlib import Path
import json,math
import numpy as np
import mixedradix as m
import centered_lift as c
import prototype as old

def main():
    rows=[]
    cases=[96,192,384,768,1536,3072,6144,12288,80,160,320,640,1280,2560,
           40,56,128,511,1001,1023,1024,10007]
    for n in cases:
        p=m.work_proxy(n)
        q=old.next_power_of_two(n)
        v12=c.choose_parameters(n,1e-6)
        v13=p['work_proxy']
        rows.append({'N':n,'G':p['g'],'odd_part':p['odd_part'],'M':p['block'],
                     'v12_rank':v12['rank'],'v12_local_halfwidth':v12['halfwidth'],
                     'v12_proxy':v12['work_proxy'], 'v13_proxy':v13,
                     'proxy_ratio_v13_over_v12':v13/v12['work_proxy'],
                     'mean_bias_exact':True, 'pointwise_variance_upper_coefficient':p['variance_factor'],
                     'v13_exact_frame_passes':p['block'] if p['g']>1 else 1})
    rng=np.random.default_rng(20261010)
    samples=[]
    for n in [96,384,768,1280]:
        x=rng.normal(size=n)+1j*rng.normal(size=n)
        target=np.fft.fft(x)/math.sqrt(n)
        g,od=m.dyadic_odd_split(n)
        M=m.sketch_block(g)
        errs=[]
        for trial in range(80):
            errs.append(m.one_row_mixedradix(x,rng,block=M)-target)
        errs=np.array(errs)
        samples.append({'N':n,'M':M,'odd_part':od,
                        'measured_max_coord_variance':float(np.max(np.mean(abs(errs)**2,axis=0))),
                        'certified_coord_variance_upper':m.mixedradix_variance_bound(x,M),
                        'measured_avg_total_squared_error':float(np.mean(np.sum(abs(errs)**2,axis=1))),
                        'exact_total_expected_squared_error':float((M-1)*np.vdot(x,x).real),
                        'measured_global_mse_ratio':float(np.mean(np.sum(abs(errs)**2,axis=1))/((M-1)*np.vdot(x,x).real))})
    out={'scope':'Approximate pointwise full-output transform for even N, exact for odd N fallback',
         'claims':'Exact arithmetic, independent dyadic states per odd-part column',
         'source':'v9 unit-step sketch + CT; v12 comparison, not external exponent construction',
         'comparison_target':'v12 deterministic kernel relative bound <=1e-6 (v13 zero bias but variance remains)',
         'fairness_note':'These work proxies count different precision/error contracts; not an identical-accuracy benchmark.',
         'proxies':rows,'empirical':samples,
         'critical_limit':'Each one-row linear map equals F_N P with P^2=M P, rank P=N/M; operator norm error M-1 and Frobenius error squared N(M-1). Exact beta frame needs M passes.'}
    (Path(__file__).parent/'EXPERIMENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    for n in [96,384,768,1536,1280,511,1001,10007]:
        r=next(v for v in rows if v['N']==n)
        print('N',n,'G',r['G'],'m',r['odd_part'],'v13 proxy',round(r['v13_proxy'],1),'v12',round(r['v12_proxy'],1),'ratio',round(r['proxy_ratio_v13_over_v12'],3))
    print('empirical global MSE / predicted:',[(r['N'],round(r['measured_global_mse_ratio'],3)) for r in samples])

if __name__=='__main__':main()
