"""Charged known-factor graph-union vs same-data full Bluestein.

Does not claim that the supplied factor list is automatically discovered.
"""
import json
from annihilator_engine import RecurrenceGreen,far_coprime_shift,dense_from_shift_defects,shift_binomial_apply
from operation_benchmark import baseline

def main():
    records=[]
    for n in [128,256,384,1024,4096]:
        engine=RecurrenceGreen(n)
        delta1=far_coprime_shift(n); delta2=n-1
        h=[0]*n
        for j,v in [(0,1),(n//3,2),(n//2,3)]:h[j]=v
        intermediate=dense_from_shift_defects(h,delta1,2,engine.p)
        r=dense_from_shift_defects(intermediate,delta2,3,engine.p)
        x=engine.P.solve(r)
        first_nz=sum(bool(v) for v in shift_binomial_apply(r,delta1,2,1,engine.p))
        second_nz=sum(bool(v) for v in shift_binomial_apply(r,delta2,3,1,engine.p))
        actual,meta=engine.transform_known_factors(x,[(delta1,2),(delta2,3)])
        reference,base,_=baseline(engine,x)
        assert actual==reference and meta['K']==3
        assert first_nz==second_nz==n
        ops=meta['work'].arithmetic()
        rec={'N':n,'delay_1':delta1,'delay_2':delta2,
             'input_nonzero':sum(bool(v) for v in x),
             'green_residual_nonzero':sum(bool(v) for v in r),
             'first_factor_defects':first_nz,'second_factor_defects':second_nz,
             'joint_defects':meta['K'],'phase18_known_factor_proxy':ops,
             'full_bluestein_proxy':base,'ratio':round(ops/base,6),
             'supplied_parameters':{'alpha1':2,'alpha2':3,'delta1':delta1,'delta2':delta2}}
        records.append(rec)
        print(n,'separate',first_nz,second_nz,'joint',meta['K'], 'ops',ops,'fallback',base,'ratio',round(ops/base,4),flush=True)
    out={'result':'Exact known-factor input class, not discovery of unknown factors',
         'records':records,'same_engine_shared_root_green_setup':True}
    with open('UNION_BENCHMARK.json','w') as f:json.dump(out,f,indent=2)
    return out
if __name__=='__main__':main()
