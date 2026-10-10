"""Charged unit-cost finite-field work proxies for the exact Phase21 methods."""
import json,random,time
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects
from benchmark_phase19 import full_reference
from reciprocal_union import transform_reciprocal_union
from reciprocal_resultant import transform_resultant_reciprocal
from compressed_resultant import transform_compressed_reciprocal

P=2013265921;G=31
records=[]
for n in (1024,2048,4096,8192,16384,32768):
    eng=RecurrenceGreen(n,P,G)
    h=[0]*n;h[13]=11;h[n-37]=17
    d=n//2-45;e=n//3+7
    r=dense_from_shift_defects(dense_from_shift_defects(h,d,17,P),e,29,P)
    x=eng.P.solve(r)
    truth,base=full_reference(eng,x)
    funcs=[('compressed',transform_compressed_reciprocal)]
    if n in (4096,16384):
        funcs.extend([('scan',transform_reciprocal_union),
                      ('full-resultant',transform_resultant_reciprocal)])
    for mode,fn in funcs:
        t=time.monotonic();got,meta=fn(eng,x);secs=time.monotonic()-t
        assert got==truth
        count=meta['work'].arithmetic()
        result={'N':n,'case':'two-unknown-factors-two-defects',
                'method':mode,'selected':meta['selected'],
                'field_ops':count,'baseline_ops':base,
                'ratio':round(count/base,6),
                'savings_percent':round(100*(1-count/base),3),
                'python_seconds':round(secs,4),
                'inversions':meta['work'].inversions,
                'vector_reads':meta['work'].reads,'vector_writes':meta['work'].writes}
        if mode=='compressed':
            result['resultant_samples']=meta['meta'].resultant_samples
            result['candidate_shift_roots']=meta['meta'].root_candidates
        records.append(result)
        print(result,flush=True)
    if n in (4096,16384):
        rng=random.Random(n)
        gx=[rng.randrange(1,P) for _ in range(n)]
        truth_g,base_g=full_reference(eng,gx)
        t=time.monotonic();ans,meta=transform_compressed_reciprocal(eng,gx)
        assert ans==truth_g
        count=meta['work'].arithmetic()
        rec={'N':n,'case':'generic-random','method':'compressed',
             'selected':meta['selected'],'field_ops':count,
             'baseline_ops':base_g,'ratio':round(count/base_g,6),
             'savings_percent':round(100*(1-count/base_g),3),
             'python_seconds':round(time.monotonic()-t,4)}
        records.append(rec)
        print(rec,flush=True)
with open('PHASE21_BENCHMARK.json','w') as f:
    json.dump({'records':records,'model':'Field addition/multiplication/inversion count, shared preinitialized Nth roots and Green operator; field inversion treated as one operation. Wall-clock is Python diagnostic, not a machine-independent speedup, and excludes root/field construction costs. General inputs fall back to full FFT.'},f,indent=2)
