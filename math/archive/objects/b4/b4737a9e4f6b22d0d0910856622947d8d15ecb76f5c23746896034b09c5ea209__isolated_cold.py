"""True fresh-process benchmark. Run via subprocess for cold Numba comparisons.

Usage: python isolated_cold.py --n 262144 --degree 3 --method generated
"""
import argparse
import json
import time
import numpy as np
from benchmark import setup,create_phase8,create_native,native_fresh_kernel,sink
from compiled_kernels import compile_prepared

p=argparse.ArgumentParser()
p.add_argument('--n',type=int,required=True)
p.add_argument('--degree',type=int,required=True,choices=[1,2,3])
p.add_argument('--method',required=True,choices=['scipy','phase8','generated','hand'])
p.add_argument('--versions',type=int,default=48)
a=p.parse_args()
arrays,changes=setup(a.n,a.degree)
changes=changes[:a.versions]
t0=time.perf_counter()
if a.method=='scipy':func=native_fresh_kernel(a.degree,arrays)
elif a.method=='phase8':func=create_phase8(a.degree,arrays)[1].single
elif a.method=='generated':func=compile_prepared(create_phase8(a.degree,arrays)[1],backend='numba').single
else:func=create_native(a.degree,arrays)
sumcheck=0.
for t,d in changes:
    out=func(t,d)
    sumcheck+=sink(out)
ms=1000*(time.perf_counter()-t0)
print(json.dumps({'n':a.n,'degree':a.degree,'method':a.method,'versions':len(changes),'cold_total_ms':round(ms,3),'checksum':sumcheck}))
