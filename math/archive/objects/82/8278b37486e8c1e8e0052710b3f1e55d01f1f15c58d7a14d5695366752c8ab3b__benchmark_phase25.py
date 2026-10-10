"""Repeatable operation census; NO wall-clock-performance claims."""
import json,random
from pathlib import Path
from gt3_deferred import DeferredGT3,ct3_baseline
from gt3_green import transform_deferred_conjugate_gt3
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects

rows=[]
for G in (16,32,128,512,2048,8192,16384):
    n=3*G
    rng=random.Random(257+G)
    x=[rng.randrange(2013265921) for _ in range(n)]
    session=DeferredGT3(x)
    request=list(range(10))+[n-1]
    session.preview(request)
    preview=session.stats()
    y=session.full()
    completed=session.stats()
    ct,cnt=ct3_baseline(x)
    if y!=ct:raise AssertionError('full mixed-radix outputs disagree')
    predicted=session.predicted_full_arithmetic()
    assert completed['arithmetic']==predicted
    assert cnt.arithmetic()-completed['arithmetic']==2*(G-1)
    rows.append(dict(N=n,G=G,preview_ops=preview['arithmetic'],
        full_good_thomas_ops=completed['arithmetic'],
        full_cooley_tukey_ops=cnt.arithmetic(),
        savings_in_field_multiplications=cnt.arithmetic()-completed['arithmetic'],
        saving_percent_vs_ct=round((1-completed['arithmetic']/cnt.arithmetic())*100,4),
        preview_fraction_of_full=round(preview['arithmetic']/completed['arithmetic'],6),
        preview_backup_peak=preview['peak_backup_words'],
        full_total_after_preview=completed['arithmetic'],
        full_no_repeat_count_confirmed=True))

hybrid=[]
for G in (32,128,512,2048):
    n=3*G
    e=RecurrenceGreen(n,2013265921,31)
    h=[0]*n;h[4]=7;h[n-9]=11
    r=dense_from_shift_defects(dense_from_shift_defects(h,n//2-3,17,e.p),n//2+7,29,e.p)
    x_struct=e.P.solve(r)
    x_generic=[random.Random(n+j).randrange(e.p) for j in range(n)]
    for kind,x in [('certified-structured',x_struct),('generic-fallback',x_generic)]:
        y,meta=transform_deferred_conjugate_gt3(e,x)
        check=DeferredGT3(x).full()
        assert y==check
        hybrid.append(dict(N=n,kind=kind,total_field_ops=meta['work'].arithmetic(),
            native_good_thomas_ops=meta['native_gt3_reference_ops'],
            native_ct3_ops=next(v['full_cooley_tukey_ops'] for v in rows if v['N']==n),
            preview_graph_ops=meta['preview']['arithmetic'],
            selected=meta['selected'],residual_computed=meta['residual_computed']))

receipt={'phase':'25','model':'exact prime-field arithmetic with common prepared roots; arithmetic plus memory/indexing separately',
    'full_length_benchmarks':rows,'green_certificate_benchmarks':hybrid,
    'all_input_asymptotic':'Theta(N log N) for N=3*2^t; no unrestricted sub-NlogN claim'}
Path('PHASE25_BENCHMARK.json').write_text(json.dumps(receipt,indent=2)+'\n')
for row in rows:
    print(f"N={row['N']:>6} GT={row['full_good_thomas_ops']:>9} CT3={row['full_cooley_tukey_ops']:>9} "
          f"save={row['saving_percent_vs_ct']:6.3f}% preview={row['preview_ops']:>8} "
          f"peak_backups={row['preview_backup_peak']}")
for h in hybrid:
    print(f"Green N={h['N']:>5} {h['kind']:>20}: {h['total_field_ops']:>9} "
          f"native GT={h['native_good_thomas_ops']:>8} selected={h['selected']}")
