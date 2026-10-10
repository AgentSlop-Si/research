"""Independent direct N^2 finite-field DFT audit for trace sieve and fallback."""
import json,random
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects
from compressed_resultant import transform_compressed_reciprocal
from rational_forcing import direct_dft_any
rng=random.Random(220026)
rows=[];total=0
for p,g in ((2013265921,31),(998244353,3)):
    for n,count in ((30,30),(64,30),(128,24),(384,12)):
        if (p-1)%n:continue
        eng=RecurrenceGreen(n,p,g)
        selected={'compressed-reciprocal-certified':0,'fallback':0}
        trace_linear=0;trace_rejected=0
        for j in range(count):
            if j%3==2:
                x=[rng.randrange(p) for _ in range(n)]
            else:
                u,v=rng.sample(range(n),2)
                d,e=rng.sample(range(1,n),2)
                h=[0]*n;h[u]=7;h[v]=11
                r=dense_from_shift_defects(dense_from_shift_defects(h,d,17,p),e,29,p)
                x=eng.P.solve(r)
            out,m=transform_compressed_reciprocal(eng,x)
            direct=direct_dft_any(x,eng.omega,p)
            assert out==direct,(p,n,j,m)
            selected[m['selected']]+=1
            trace_linear+=m['meta'].trace_linear_extracted
            trace_rejected+=m['meta'].trace_rejected
            total+=n
        rec={'field':p,'N':n,'tests':count,'exact_DFT_outputs':count*n,
             'selected':selected,'trace_linear':trace_linear,
             'trace_rejected':trace_rejected}
        print(rec,flush=True);rows.append(rec)
with open('PHASE22_AUDIT.json','w') as f:
    json.dump({'records':rows,'total_exact_DFT_outputs':total,
               'method':'Independent O(N^2) direct finite-field DFT'},f,indent=2)
print('TOTAL',total)
