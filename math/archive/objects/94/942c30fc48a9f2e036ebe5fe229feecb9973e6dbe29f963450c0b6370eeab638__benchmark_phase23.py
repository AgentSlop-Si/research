"""Reproducible exact field-operation comparison. No wall-clock speedup claim."""
import json,random,time
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects
from benchmark_phase19 import full_reference
from compressed_resultant import transform_compressed_reciprocal
from short_probe_fusion import transform_short_probe

P=2013265921;PRIMITIVE=31
records=[]
for n in (1024,2048,4096,8192,16384,32768):
    eng=RecurrenceGreen(n,P,PRIMITIVE)
    h=[0]*n;h[13]=11;h[n-37]=17
    d=n//2-45;e=n//3+7
    r=dense_from_shift_defects(dense_from_shift_defects(h,d,17,P),e,29,P)
    rng=random.Random(n+23)
    xs=(('structured',eng.P.solve(r)),('generic',[rng.randrange(1,P) for _ in range(n)]))
    for label,x in xs:
        ref,base=full_reference(eng,x)
        t=time.monotonic()
        original,orig_meta=transform_compressed_reciprocal(eng,x)
        oldsecs=time.monotonic()-t
        t=time.monotonic()
        improved,new_meta=transform_short_probe(eng,x)
        newsecs=time.monotonic()-t
        assert improved==original==ref
        old=orig_meta['work'].arithmetic()
        new=new_meta['work'].arithmetic()
        r={'N':n,'input_class':label,'phase22_field_ops':old,
           'phase23_field_ops':new,'baseline_field_ops':base,
           'phase23_selected':new_meta['selected'],
           'phase22_selected':orig_meta['selected'],
           'phase23_saving_vs22_pct':round(100*(1-new/old),3),
           'phase23_saving_vsFFT_pct':round(100*(1-new/base),3),
           'trace_gcd_degree':new_meta['meta'].trace_gcd_degree,
           'candidate_shifts':new_meta['meta'].candidate_shifts,
           'cyclic_certificates':new_meta['meta'].cyclic_checks,
           'failed_certificates':new_meta['meta'].failed_certificates,
           'phase23_python_seconds':round(newsecs,4),
           'phase22_python_seconds':round(oldsecs,4)}
        records.append(r)
        print(r,flush=True)
with open('PHASE23_BENCHMARK.json','w') as f:
    json.dump({'model':'Field addition + multiplication + inversion each costs 1. '
      'Shared preinitialized Nth roots and Green operators for both comparisons. '
      'All discovery, candidate validation and fallback arithmetic included. '
      'This is not word/bit complexity nor float stability. '
      'Python seconds diagnostic only.',
      'prime':P,'records':records},f,indent=2)
