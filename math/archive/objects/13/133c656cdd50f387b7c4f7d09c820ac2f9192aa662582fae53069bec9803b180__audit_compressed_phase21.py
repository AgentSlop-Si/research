"""Independent exact direct-DFT comparisons for compressed-resultant route."""
import json,random,itertools
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects
from compressed_resultant import transform_compressed_reciprocal
from rational_forcing import direct_dft_any

rng=random.Random(212101);p=2013265921
out=[];entries=0
for n,count,t in [(30,100,2),(64,70,2),(128,50,2),(384,30,2),
                  (64,8,3)]:
    eng=RecurrenceGreen(n,p,31)
    fast=0;fallback=0
    for j in range(count):
        u,v=rng.sample(range(n),2)
        shifts=rng.sample(range(1,n),t)
        h=[0]*n;h[u]=7;h[v]=11
        r=h
        for k,d in enumerate(shifts):
            r=dense_from_shift_defects(r,d,[17,29,41][k],p)
        x=eng.P.solve(r)
        y,meta=transform_compressed_reciprocal(eng,x,s=2**t)
        ref=direct_dft_any(x,eng.omega,p)
        assert y==ref,(n,j,t,shifts,meta)
        if meta['selected']=='fallback':fallback+=1
        else:
            fast+=1
            assert meta['meta'].full_certificate_entries==n
        entries+=n
    rec={'N':n,'filters':t,'cases':count,'fast':fast,'fallback':fallback,
         'direct_DFT_outputs_checked':count*n,'field':p}
    print(rec,flush=True);out.append(rec)
# Second independent prime with exact Nth roots.
p=998244353
for n in (64,128):
    eng=RecurrenceGreen(n,p,3)
    fast=fallback=0;count=15
    for j in range(count):
        u,v=rng.sample(range(n),2);d,e=rng.sample(range(1,n),2)
        h=[0]*n;h[u]=7;h[v]=11
        r=dense_from_shift_defects(dense_from_shift_defects(h,d,17,p),e,29,p)
        x=eng.P.solve(r)
        y,meta=transform_compressed_reciprocal(eng,x,s=4)
        assert y==direct_dft_any(x,eng.omega,p)
        if meta['selected']=='fallback':fallback+=1
        else:fast+=1
        entries+=n
    rec={'N':n,'filters':2,'cases':count,'fast':fast,'fallback':fallback,
         'direct_DFT_outputs_checked':count*n,'field':p}
    print(rec,flush=True);out.append(rec)
for n,count in [(30,15),(64,20),(128,20)]:
    p=2013265921;eng=RecurrenceGreen(n,p,31);fast=0
    for _ in range(count):
        x=[rng.randrange(p) for _ in range(n)]
        y,m=transform_compressed_reciprocal(eng,x,s=4)
        assert y==direct_dft_any(x,eng.omega,p)
        if m['selected']!='fallback':fast+=1
        entries+=n
    rec={'N':n,'filters':0,'cases':count,'fast':fast,'fallback':count-fast,
         'direct_DFT_outputs_checked':count*n,'field':p}
    print(rec,flush=True);out.append(rec)
assert entries==sum(v['direct_DFT_outputs_checked'] for v in out)
with open('COMPRESSED_AUDIT.json','w') as f:
    json.dump({'samples':out,'independent_exact_DFT_outputs':entries,
       'method':'Direct N^2 finite-field DFT; exact equality for all tested output frequencies'},f,indent=2)
print('TOTAL',entries,flush=True)
