"""Independent direct DFT audit of Phase23 correctness on two exact prime fields.

The direct O(N^2) oracle is not used by the algorithm itself.
All generated instances and seeds are deterministic.
"""
import random,json
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects
from short_probe_fusion import transform_short_probe
from rational_forcing import direct_dft_any

checks=[];entries=0;fast=0;fallback=0
for p,g,ns in ((2013265921,31,(16,30,64,96,128,384)),
               (998244353,3,(16,32,64,128,256))):
    for n in ns:
        rng=random.Random(23*n+p)
        eng=RecurrenceGreen(n,p,g)
        types=['two-factor']*18 + ['generic']*8 + ['prefix-adversary']*3
        local={'prime':p,'N':n,'cases':0,'fast':0,'fallback':0,'checked_outputs':0}
        for typ in types:
            if typ=='generic':
                x=[rng.randrange(p) for _ in range(n)]
            else:
                h=[0]*n
                a,b=rng.sample(range(n),2)
                h[a]=rng.randrange(1,p)
                h[b]=rng.randrange(1,p)
                d,e=rng.sample(range(1,n),2)
                al=rng.randrange(1,p)
                be=rng.randrange(1,p)
                r=dense_from_shift_defects(dense_from_shift_defects(h,d,al,p),e,be,p)
                if typ=='prefix-adversary':
                    mode=rng.randrange(10,n)
                    node=eng.powers[mode]
                    delta=1
                    step=pow(node,-1,p)
                    for j in range(n):
                        r[j]=(r[j]+delta)%p
                        delta=delta*step%p
                x=eng.P.solve(r)
            y,stats=transform_short_probe(eng,x)
            oracle=direct_dft_any(x,eng.omega,p)
            assert y==oracle,(p,n,typ,stats['meta'])
            local['cases']+=1;local['checked_outputs']+=n
            if stats['selected']=='short-prefix-certified':
                assert typ=='two-factor'
                fast+=1;local['fast']+=1
            else:
                fallback+=1;local['fallback']+=1
        entries+=local['checked_outputs']
        checks.append(local)
        print(local,flush=True)
report={'prime_fields':[2013265921,998244353],
        'checked_outputs':entries,'fast_certified':fast,'fallback':fallback,
        'checks':checks,
        'oracle':'independent quadratic-time exact DFT, not reused in solver',
        'model':'One check is one output coordinate equality; sample-size proof is analytical'}
with open('PHASE23_AUDIT.json','w') as f:json.dump(report,f,indent=2)
print('SUMMARY',entries,fast,fallback,flush=True)
