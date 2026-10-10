"""Independent direct finite-field DFT output audit, including negatives."""
import json, random, itertools, time
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects
from rational_forcing import direct_dft_any
from reciprocal_union import transform_reciprocal_union

P=2013265921
rng=random.Random(210021)
checks=[]
entries=0
for n,number,three_factors in [(30,435,False),(64,130,False),(128,110,False),
                                (384,60,False),(64,28,True)]:
    eng=RecurrenceGreen(n,P,31)
    pairs=list(itertools.combinations(range(n),2)) if number==435 else [tuple(rng.sample(range(n),2)) for _ in range(number)]
    successes=fallbacks=0
    t0=time.monotonic()
    for idx,(u,v) in enumerate(pairs):
        ds=[7,13] if n==30 else rng.sample(range(1,n),3 if three_factors else 2)
        alphas=[17,29,41] if three_factors else [17,29]
        h=[0]*n;h[u]=7;h[v]=11
        r=h
        for d,a in zip(ds,alphas):r=dense_from_shift_defects(r,d,a,P)
        x=eng.P.solve(r)
        out,meta=transform_reciprocal_union(eng,x,max_terms=8 if three_factors else 4)
        truth=direct_dft_any(x,eng.omega,P)
        if out!=truth:
            raise AssertionError(('incorrect',n,idx,ds,u,v,meta))
        if meta['selected']=='fallback':fallbacks+=1
        else:
            successes+=1
            if not meta['discovery'].full_certificates:
                raise AssertionError('uncertified fast branch')
        entries+=n
    checks.append({'N':n,'filter_count':3 if three_factors else 2,
                   'cases':len(pairs),'fast_cases':successes,'fallback_cases':fallbacks,
                   'dft_outputs_checked':n*len(pairs),
                   'elapsed_seconds':round(time.monotonic()-t0,3)})
    print(checks[-1],flush=True)
# Arbitrary inputs always exact, and generic candidates should usually reject.
for n,number in [(30,20),(64,25),(128,20)]:
    eng=RecurrenceGreen(n,P,31)
    fast=0
    for _ in range(number):
        x=[rng.randrange(P) for _ in range(n)]
        out,meta=transform_reciprocal_union(eng,x)
        assert out==direct_dft_any(x,eng.omega,P)
        if meta['selected']!='fallback':fast+=1
        entries+=n
    checks.append({'N':n,'filter_count':0,'cases':number,'fast_cases':fast,
                   'fallback_cases':number-fast,'dft_outputs_checked':n*number})
    print(checks[-1],flush=True)
assert sum(z['dft_outputs_checked'] for z in checks)==entries
result={'results':checks,'exact_DFT_outputs_checked':entries,
        'claim':'Exact finite-field output comparisons against independent direct DFT; structured-input fast route has nondegeneracy conditions and generic data has an FFT fallback.'}
with open('PHASE21_AUDIT.json','w') as f:json.dump(result,f,indent=2)
print('TOTAL',entries,flush=True)
