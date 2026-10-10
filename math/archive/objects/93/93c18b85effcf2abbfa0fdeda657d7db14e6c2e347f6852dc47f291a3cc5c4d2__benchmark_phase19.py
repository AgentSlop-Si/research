"""Exact-operation comparisons; shared root and Green setup, no wall-clock claims."""
from __future__ import annotations
import json,random
from math import gcd
from blind_discovery import RecurrenceGreen
from annihilator_engine import dense_from_shift_defects,far_coprime_shift
from rational_forcing import bluestein_transform,PolyStats

P=2013265921;G=31

def hidden_delay(n):
    k=n//3+1
    while gcd(k,n)!=1 or k in (1,n-1,far_coprime_shift(n)):
        k+=1
    return k

def full_reference(engine,x):
    r=engine.P.apply(x)
    s=PolyStats()
    v,_=bluestein_transform(r,engine.n,engine.omega,engine.p,engine.primitive_gen,s)
    return engine.L.solve(v),s.total_field_ops()+8*engine.n+1

def main():
    records=[]
    for n in (128,384,1024,4096):
        e=RecurrenceGreen(n,P,G)
        d=hidden_delay(n)
        h=[0]*n;h[n//5]=7
        r=dense_from_shift_defects(h,d,2,P)
        x=e.P.solve(r)
        assert all(r)
        cases=[('hidden-single',x,None)]
        d1=far_coprime_shift(n)
        r2=dense_from_shift_defects(r,d1,3,P)
        assert all(r2)
        cases.append(('hidden-second',e.P.solve(r2),[(d1,3)]))
        rng=random.Random(n)
        cases.append(('generic',[rng.randrange(1,P) for _ in range(n)],None))
        for kind,x,known in cases:
            y,m=(e.transform_blind_one(x) if known is None else e.transform_semiblind_union(x,known))
            y_ref,c0=full_reference(e,x)
            assert y==y_ref
            c1=m['work'].arithmetic()
            ds=m['discovery']
            record={'N':n,'kind':kind,'known_factors':known,'unknown_true_delay':d if kind!='generic' else None,
                    'selected':m['selected'],'detected_delay':m.get('delay',m.get('unknown_delay')),
                    'defects':m['K'],'resonant':m['resonant'],
                    'discover_field_multiplies':ds.field_products,
                    'discover_projective_comparisons':ds.projective_comparisons,
                    'candidate_full_scans':ds.candidate_full_scans,
                    'candidate_edge_checks':ds.candidate_edge_tests,
                    'discover_integer_inversions':ds.integer_inversions,
                    'field_ops_new':c1,'field_ops_bluestein':c0,
                    'field_ops_ratio':round(c1/c0,6)}
            records.append(record)
            print(f"{n:5} {kind:14} {m['selected']:20} {c1:9} {c0:9} {c1/c0:.3f}",flush=True)
    data={'records':records,
          'scope':'Exact GF(2013265921) algorithm, equal shared initialization, per-call field-operation counter. Integer Euclid cost in separate discover_integer_inversions column; field comparisons and address scans in separate columns. Not bit-complexity or wall-time.',
          'unrestricted_all_input_sub_nlogn':False}
    with open('BENCHMARK_PHASE19.json','w') as f:json.dump(data,f,indent=2)
    return data
if __name__=='__main__':main()
