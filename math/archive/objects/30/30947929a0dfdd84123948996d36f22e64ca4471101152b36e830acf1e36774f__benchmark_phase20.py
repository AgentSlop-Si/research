"""Exact field-operation ledger on shared Green/root setup, N=4096."""
from __future__ import annotations
import json,random
from math import gcd
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects
from resultant_gate import transform_resultant
from hybrid_phase20 import transform_hybrid_phase20
from benchmark_phase19 import full_reference

P=2013265921;N=4096
eng=RecurrenceGreen(N,P,31)
case=[]
delta=2003
h=[0]*N;h[31]=7;h[2997]=11
r=dense_from_shift_defects(h,delta,2,P)
case.append(('dense-hidden-K2',r))
# Cyclic phase segment: 2 defects in unknown, coprime, resonant graph.
delta2=2047
assert gcd(delta2,N)==1
alpha=pow(eng.omega,19,P)
r2=[0]*N
for t in range(N):
    r2[(t*delta2)%N]=pow(alpha,t,P)*(3 if t<1171 else 5)%P
assert all(r2)
assert sum((r2[j]-alpha*r2[(j-delta2)%N])%P!=0 for j in range(N))==2
case.append(('resonant-wrap-K2',r2))
rng=random.Random(202010)
case.append(('generic-random',[rng.randrange(1,P) for _ in range(N)]))
records=[]
for kind,r in case:
    x=eng.P.solve(r)
    baseline,base_ops=full_reference(eng,x)
    for mode,fn in [('resultant',transform_resultant),('hybrid',transform_hybrid_phase20)]:
        y,meta=fn(eng,x)
        assert y==baseline,(kind,mode)
        co=meta['work']
        records.append({'kind':kind,'mode':mode,'N':N,'selected':meta['selected'],
                        'new_field_ops':co.arithmetic(),'baseline_field_ops':base_ops,
                        'ratio':round(co.arithmetic()/base_ops,6),
                        'inversions':co.inversions,
                        'vector_reads':co.reads,'vector_writes':co.writes,
                        'spectral_root_degree':(meta['certificate'].reduced_degree
                          if mode=='resultant' else (None if meta['phase20_resultant'] is None
                          else meta['phase20_resultant'].reduced_degree))})
        print(kind,mode,meta['selected'],co.arithmetic(),base_ops,
              round(co.arithmetic()/base_ops,3),flush=True)
with open('BENCHMARK_PHASE20.json','w') as f:json.dump({'records':records,'scope':
    'Exact finite-field operation proxies sharing root and Green setup; field inversions treated as unit-cost primitives; Python timings and bit complexity not implied. Generic worst case falls back to O(N log N).'},f,indent=2)
