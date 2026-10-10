"""Exact field-op comparison on dyadic sizes, honest radix-2 baseline."""
import json,random,time
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects
from lazy_dif import LazyDIF,transform_conjugate_lazy
from deferred_dif import transform_deferred_conjugate
from short_probe_fusion import transform_short_probe

P=2013265921;G=31
records=[]
for n in (256,1024,4096,8192,16384,32768):
    engine=RecurrenceGreen(n,P,G)
    h=[0]*n;h[13%n]=11;h[(n-37)%n]=17
    d=n//2-45;e=n//3+7
    r=dense_from_shift_defects(dense_from_shift_defects(h,d,17,P),e,29,P)
    rng=random.Random(n*17+7)
    inputs=[('structured',engine.P.solve(r)),
            ('generic',[rng.randrange(1,P) for _ in range(n)])]
    for label,x in inputs:
        direct=LazyDIF(x,engine.powers,P)
        expected=direct.full()
        eager_native=direct.stats.arithmetic()
        t0=time.perf_counter();lazy,old_lazy=transform_conjugate_lazy(engine,x);td1=time.perf_counter()-t0
        t0=time.perf_counter();new,new_meta=transform_deferred_conjugate(engine,x);td2=time.perf_counter()-t0
        assert new==lazy==expected
        record=dict(N=n,input_class=label,
            native_radix2_field_ops=eager_native,
            conjugated_eager_field_ops=old_lazy['work'].arithmetic(),
            conjugated_deferred_field_ops=new_meta['work'].arithmetic(),
            branch=new_meta['selected'],
            conjugated_deferred_preview_ops=new_meta['preview']['arithmetic'],
            conjugated_eager_preview_ops=old_lazy['preview']['additions']+old_lazy['preview']['multiplications'],
            cached_backup_peak=new_meta['storage']['peak_backup_words'],
            residual_computed=new_meta['residual_computed'],
            completed_fft_ops=new_meta['final_fft']['arithmetic'],
            pure_fft_fraction=round(new_meta['work'].arithmetic()/eager_native,6),
            deferred_preview_saving_pct=round(100*(1-new_meta['preview']['arithmetic']/(old_lazy['preview']['additions']+old_lazy['preview']['multiplications'])),3),
            old_lazy_seconds=round(td1,5),deferred_seconds=round(td2,5))
        records.append(record)
        print(record,flush=True)
with open('PHASE24_BENCHMARK.json','w') as f:
    json.dump({'model':'Prime-field additions/multiplications/inversions unit cost; '
      'power-of-two N; shared supplied primitive root and root powers; '
      'native radix-2 baseline (not Bluestein); exact transform of input x; '
      'compiler and certification charged, full FFT fallback shares its graph; '
      'memory accesses counted separately, not included in field-arithmetic column.',
      'prime':P,'records':records},f,indent=2)
