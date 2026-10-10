"""Warm performance sensitivity: rotate order of three kernels, same inputs."""
import json
import time
import gc
import numpy as np
from benchmark import setup,create_phase8,create_native,native_fresh_kernel,sink
from compiled_kernels import compile_prepared
from pathlib import Path
n=262144; degree=3; arrays,events=setup(n,degree)
events=events[:48]
p=create_phase8(degree,arrays)[1]
j=compile_prepared(p,backend='numba')
hand=create_native(degree,arrays)
fns={'phase8':p.single,'phase9':j.single,'hand':hand}
for f in fns.values(): f(*events[0])
scores={x:[] for x in fns}
for trial in range(12):
    order=['phase8','phase9','hand']
    order=np.roll(order,trial%3)
    for key in order:
        gc.collect()
        t0=time.perf_counter()
        v=0.
        for a,b in events:v+=sink(fns[key](a,b))
        scores[key].append((time.perf_counter()-t0)*1000)
        if not np.isfinite(v): raise ArithmeticError
for k,times in scores.items():print(k,'median=',np.median(times),'p10=',np.percentile(times,10),'p90=',np.percentile(times,90),'min=',np.min(times),'max=',np.max(times))
Path(__file__).with_name('repeatability_results.json').write_text(json.dumps({'n':n,'degree':degree,'versions':48,'repeats':12,'milliseconds':scores,'summary':{k:{'median':float(np.median(t)),'p10':float(np.percentile(t,10)),'p90':float(np.percentile(t,90))} for k,t in scores.items()}},indent=2)+'\n')
