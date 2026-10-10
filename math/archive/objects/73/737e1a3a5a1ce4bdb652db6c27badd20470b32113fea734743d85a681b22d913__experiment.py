"""Export new v12 artifact results. No timing claims; arithmetic-proxy only."""
import json,math
import numpy as np
from pathlib import Path
import centered_lift as c
import prototype as base


def main():
    ranks=c.demo_rank_table()
    params=[]
    for n in [93,127,255,511,1001,4095,10007]:
        for tol in [1e-2,1e-4,1e-6,1e-8]:
            old=c.choose_parameters(n,tol,old_v11=True)
            new=c.choose_parameters(n,tol)
            params.append({'N':n,'target_deterministic_rel_error':tol,
                           'v11':old,'v12':new,
                           'proxy_ratio':new['work_proxy']/old['work_proxy'],
                           'proxy_saving_fraction':1-new['work_proxy']/old['work_proxy']})
    rng=np.random.default_rng(1005)
    trials=[]
    for n in [37,93,127,255,511]:
        x=rng.normal(size=n)+1j*rng.normal(size=n)
        Q=base.next_power_of_two(n)
        M=base.choose_dyadic_block(Q)
        for H in [0,1,2,3]:
            R=10
            center=c.centered_fused_center(x,R,M,H)
            target=np.fft.fft(x)/math.sqrt(n)
            eps=c.centered_deterministic_bound(n,R,M,H)
            measured=float(np.max(np.abs(center-target))/np.linalg.norm(x))
            trials.append({'N':n,'R':R,'H':H,
                           'measured_error_rel_l2':measured,
                           'certified_bound':eps,
                           'ratio':measured/eps})
    out={
      'research':'Hero #1 v12 centered shared Fourier correction',
      'scope':'randomized approximate Fourier transform only, no exact fast DFT claim',
      'source':'user v11 checkpoint; CrocSwap audited solely for independent transfer',
      'rank_table':ranks,
      'parameter_choices':params,
      'deterministic_samples':trials,
      'largest_sample_bound_ratio':max(r['ratio'] for r in trials),
      'n511_r_1e8':{'uncentered':c.certified_rank(511,1e-8,False),
                   'centered':c.certified_rank(511,1e-8,True)},
      'n511_parameter_example':next(r for r in params if r['N']==511 and r['target_deterministic_rel_error']==1e-4),
      'bessel_l1_centred_max':c.bessel_l1_envelope(math.pi/2),
      'finite_precision_caveat':'Balanced scans control multiplication rounding depth but NOT the error from repeated approximate transition constants: root errors must be o(error_target/N), or reanchor frequently.'
    }
    (Path(__file__).parent/'RESULT_SUMMARY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['n511_r_1e8','n511_parameter_example','largest_sample_bound_ratio','bessel_l1_centred_max']},indent=2))

if __name__=='__main__':main()
