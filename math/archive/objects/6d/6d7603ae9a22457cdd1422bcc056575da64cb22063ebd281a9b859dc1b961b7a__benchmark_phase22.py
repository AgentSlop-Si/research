"""Compared directly with exact Phase21 and Bluestein field-operation proxies.

All branches share preinitialized Nth roots and Green matrices. Numerical
Python wall-clock diagnostics are not claimed as cross-language speedups.
"""
import json,random,time
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects
from benchmark_phase19 import full_reference
from compressed_resultant import transform_compressed_reciprocal

p=2013265921;G=31
records=[]
for n in (1024,2048,4096,8192,16384,32768):
    engine=RecurrenceGreen(n,p,G)
    h=[0]*n;h[13]=11;h[n-37]=17
    d=n//2-45;e=n//3+7
    r=dense_from_shift_defects(dense_from_shift_defects(h,d,17,p),e,29,p)
    rng=random.Random(n)
    inputs=[('structured',engine.P.solve(r)),
            ('generic',[rng.randrange(1,p) for _ in range(n)])]
    for label,x in inputs:
        truth,base=full_reference(engine,x)
        t0=time.monotonic()
        y,meta=transform_compressed_reciprocal(engine,x)
        assert y==truth
        count=meta['work'].arithmetic()
        rec={'N':n,'case':label,'selected':meta['selected'],
             'phase22_ops':count,'bluestein_ops':base,
             'fraction_of_baseline':round(count/base,6),
             'savings_pct':round(100*(1-count/base),3),
             'trace_gcd_degree':meta['meta'].trace_gcd_degree,
             'trace_rejected':meta['meta'].trace_rejected,
             'trace_linear_extracted':meta['meta'].trace_linear_extracted,
             'trace_half_scan':meta['meta'].trace_half_scan,
             'trace_ops':meta['meta'].trace_sieve_ops,
             'candidate_shifts':meta['meta'].root_candidates,
             'phase22_python_seconds':round(time.monotonic()-t0,5)}
        records.append(rec)
        print(rec,flush=True)
with open('PHASE22_BENCHMARK.json','w') as f:
    json.dump({'records':records,
       'field':p,'model':('Exact finite-field additions, multiplications, inversions '
       'with unit charge, including all discovery/rejection/certification/fallback '
       'work but sharing preinitialized root and Green data. Not bit complexity '
       'or floating-point throughput.')},f,indent=2)
