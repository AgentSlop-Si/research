"""Charged mixed-family choice: no hidden supplied delay/factor parameters."""
import json,random
from hybrid_engine import RecurrenceGreen
from annihilator_engine import dense_from_shift_defects,far_coprime_shift
from benchmark_phase19 import hidden_delay,full_reference

p,g,n=2013265921,31,4096
engine=RecurrenceGreen(n,p,g)
d=hidden_delay(n)
h1=[0]*n;h1[53]=7
h2=[0]*n;h2[53]=7;h2[3000]=11
r1=dense_from_shift_defects(h1,d,2,p)
r2=dense_from_shift_defects(h2,d,2,p)
r3=dense_from_shift_defects(dense_from_shift_defects(h1,d,2,p),far_coprime_shift(n),3,p)
signals=[('unknown-shift-K1',r1),('unknown-shift-K2',r2),('unknown-two-factor-K1',r3)]
rng=random.Random(1009)
signals.append(('generic-random',[rng.randrange(1,p) for _ in range(n)]))
records=[]
for kind,r in signals:
    x=engine.P.solve(r)
    y,detail=engine.transform_phase19_hybrid(x)
    ref,base=full_reference(engine,x)
    assert y==ref
    work=detail['work'].arithmetic()
    record={'N':n,'family':kind,'selection':detail['selected'],'new_field_ops':work,
            'full_fft_field_ops':base,'ratio':round(work/base,6),
            'graph_trials':detail['graph_discovery'].candidate_full_scans,
            'inverse_taps':detail.get('inverse_support'),
            'inverse_certificate_status':None if detail['inverse_certificate'] is None else
                      detail['inverse_certificate'].fallback_reason}
    records.append(record)
    print(kind,detail['selected'],work,base,round(work/base,3))
with open('BENCHMARK_HYBRID.json','w') as f:json.dump({'records':records},f,indent=2)
