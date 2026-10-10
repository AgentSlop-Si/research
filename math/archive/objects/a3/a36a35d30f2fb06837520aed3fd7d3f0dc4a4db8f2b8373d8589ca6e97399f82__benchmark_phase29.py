"""Charged full-input NTT benchmark: Phase29 120-tensor vs Phase28 60-tensor.
Root tables and 15-codelet constants prepared identically. No wall clock claims.
"""
import json,random,sys
from crt15 import P,GENERATOR,ALT_P,ALT_GENERATOR
from fused60 import make_fused60_plan,transform_fused,predicted_fused
from fused120 import make_fused120_plan,transform_fused120,predicted_fused120

def run(field=P,gen=GENERATOR,hs=(1,2,4,8,16,32,64,128,256,512)):
    records=[]
    for h in hs:
        n=120*h
        if (field-1)%n:continue
        old_plan=make_fused60_plan(n,p=field,gen=gen)
        new_plan=make_fused120_plan(n,p=field,gen=gen)
        rng=random.Random(9928121+n)
        x=[rng.randrange(field) for _ in range(n)]
        old,c_old=transform_fused(x,old_plan)
        new,c_new=transform_fused120(x,new_plan)
        assert old==new
        assert c_old.total()==predicted_fused(2*h)[-1]
        assert c_new.total()==predicted_fused120(h)[-1]
        assert new_plan.diagonal_ones==4
        common_setup=(new_plan.wfta.base.setup.total()+new_plan.wfta.preparation.total())
        cold_old=c_old.total()+common_setup+old_plan.extra_setup.total()
        cold_new=c_new.total()+common_setup+new_plan.extra_setup.total()
        assert c_old.total()-c_new.total()==13*h
        assert cold_old-cold_new==13*h-57
        rec=dict(n=n,h=h,field=field,new_additions=c_new.adds,new_multiplications=c_new.muls,
                 new_warm=c_new.total(),phase28_warm=c_old.total(),warm_saving=c_old.total()-c_new.total(),
                 warm_saving_pct=round(100*(c_old.total()-c_new.total())/c_old.total(),5),
                 common_setup=common_setup,phase28_extra_setup=old_plan.extra_setup.total(),
                 new_extra_setup=new_plan.extra_setup.total(),phase28_cold=cold_old,
                 new_cold=cold_new,cold_saving=cold_old-cold_new,
                 all_input_reference_agrees=True,root_table_size=len(new_plan.wfta.base.roots_g),
                 stage_diagonal_slots=144,identity_coefficients=new_plan.diagonal_ones,
                 stage_nonidentity_coefficients=144-new_plan.diagonal_ones)
        records.append(rec)
        print('N',n,'new',rec['new_warm'],'old',rec['phase28_warm'],
              'warm saved',rec['warm_saving'],'cold saved',rec['cold_saving'],flush=True)
    return dict(model='exact prime-field additions + nonidentity constant multiplications; setup separate',
                prior_baseline='Phase28 nested 60-point scalar graph',
                field=field,records=records,formula_new='180*h*log2(h)+1163*h+15',
                formula_old='180*h*log2(h)+1176*h+15',
                warm_saving='13*h',cold_saving='13*h-57',
                no_unrestricted_subnlogn=True)
if __name__=='__main__':
    field=P;gen=GENERATOR
    if len(sys.argv)>1 and sys.argv[1]=='alternate':field=ALT_P;gen=ALT_GENERATOR
    rows=run(field,gen)
    filename='BENCHMARK_PHASE29_ALT.json' if field==ALT_P else 'BENCHMARK_PHASE29.json'
    with open(filename,'w') as f:json.dump(rows,f,indent=2)
