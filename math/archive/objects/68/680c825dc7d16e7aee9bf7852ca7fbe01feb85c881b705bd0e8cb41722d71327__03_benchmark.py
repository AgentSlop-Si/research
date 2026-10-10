#!/usr/bin/env python3
"""Same Python/SciPy environment benchmarks (not FFTW or complexity proof)."""
import json,math,sys,time
from pathlib import Path
import numpy as np
import offset_class_lift as oc
import unit_step_core as core
v11dir=Path('fft_hero0_work/v11/fft_all_length_fused_fp_v11')
if not v11dir.exists():
    print('v11 comparison unavailable; saved offset-class tests remain standalone.')
    raise SystemExit(0)
sys.path.append(str(v11dir))
import prototype as old

rng=np.random.default_rng(20261009)
res=[]
for n in [768,1280,3072,486]:
    radix=3 if n==486 else 2
    plan=oc.OffsetPlan.build(n,radix=radix)
    # For a fair v11 dyadic comparison use radix 2; skip radix-3-only length.
    if radix!=2:continue
    rank=old.bessel_rank_for_tail(1e-8)
    x=rng.normal(size=n)+1j*rng.normal(size=n)
    state=core.draw_state(plan.q,rng)
    def run_class():return oc.row_estimate(x,plan,state)
    def run_v11():return old.fused_addition_bessel_chirp_row(x,rank,plan.m,state,halfwidth=0)
    def run_native():return oc.reference(x)
    metrics={}
    for key,fn in [('offset_class',run_class),('v11_fused',run_v11),('numpy_fft',run_native)]:
        fn()
        times=[]
        for i in range(7):
            start=time.perf_counter();resv=fn();times.append(time.perf_counter()-start)
        metrics[key]={'median_seconds':float(np.median(times)),
                      'normalized_error':float(np.max(np.abs(resv-oc.reference(x)))/np.linalg.norm(x))}
    res.append({'n':n,'h':plan.cofactor,'rank_v11':rank,'m':plan.m,'metrics':metrics,
                'speedup_vs_v11':metrics['v11_fused']['median_seconds']/metrics['offset_class']['median_seconds']})
Path(__file__).parent.joinpath('benchmark.json').write_text(json.dumps(res,indent=2)+'\n')
for a in res:
 print('N',a['n'],'h',a['h'],'rank',a['rank_v11'],'gain_vs_v11',f"{a['speedup_vs_v11']:.2f}x",
       'class',a['metrics']['offset_class']['median_seconds'],
       'v11',a['metrics']['v11_fused']['median_seconds'],
       'numpy',a['metrics']['numpy_fft']['median_seconds'])
