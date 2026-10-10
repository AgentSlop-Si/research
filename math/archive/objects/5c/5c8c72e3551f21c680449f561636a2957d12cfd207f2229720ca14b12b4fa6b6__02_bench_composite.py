#!/usr/bin/env python3
"""Python-only prototype comparison; NOT competitive native FFT benchmark."""
import sys,math,time,json
from pathlib import Path
import numpy as np
import composite_lift as new
import composite_cycle_core as composite
v11dir=Path('fft_hero0_work/v11/fft_all_length_fused_fp_v11')
if not v11dir.exists():
    print('Historical v11 project absent; omit comparison.')
    raise SystemExit(0)
sys.path.append(str(v11dir))
import prototype as previous
import unit_step_core as old_core
rng=np.random.default_rng(20261009)
checks=[]
for n in [840,3600,20736]:
    plan=new.CompositePlan.build(n)
    dyadic_q=previous.next_power_of_two(n)
    dyadic_m=previous.choose_dyadic_block(dyadic_q)
    rank=previous.bessel_rank_for_tail(1e-8)
    x=rng.normal(size=n)+1j*rng.normal(size=n)
    state=composite.draw_state(n,rng)
    oldstate=old_core.draw_state(dyadic_q,rng)
    funcs={
        'composite_green':lambda:new.row_estimate(x,plan,state),
        'prior_v11_15_order':lambda:previous.fused_addition_bessel_chirp_row(x,rank,dyadic_m,oldstate,halfwidth=0),
        'numpy_fft':lambda:new.reference(x)
    }
    gold=new.reference(x)
    metrics={}
    for label,func in funcs.items():
        func()
        times=[]
        for rep in range(5):
            start=time.perf_counter();res=func();times.append(time.perf_counter()-start)
        metrics[label]={'median_seconds':float(np.median(times)),
                        'normalized_max_error':float(np.max(np.abs(res-gold))/np.linalg.norm(x))}
    checks.append({'n':n,'m':plan.m,'rank_v11':rank,'classes_new':1,
                  'q_v11':dyadic_q,'m_v11':dyadic_m,'metrics':metrics,
                  'old_to_new_single_row_ratio':metrics['prior_v11_15_order']['median_seconds']/metrics['composite_green']['median_seconds']})

Path(__file__).parent.joinpath('composite_benchmark.json').write_text(json.dumps(checks,indent=2)+'\n')
for a in checks:
 print('n',a['n'],'m',a['m'],'v11 rank',a['rank_v11'],'v11/core gain',f"{a['old_to_new_single_row_ratio']:.1f}x",
       'green',f"{a['metrics']['composite_green']['median_seconds']:.5f}s",
       'v11',f"{a['metrics']['prior_v11_15_order']['median_seconds']:.5f}s",
       'native',f"{a['metrics']['numpy_fft']['median_seconds']:.6f}s")
