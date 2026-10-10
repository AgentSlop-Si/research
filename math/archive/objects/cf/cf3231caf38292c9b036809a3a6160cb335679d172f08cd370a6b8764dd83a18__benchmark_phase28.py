"""Reproducible field-work ledger for Phase 27, WFTA15 and fused WFTA60.

Exact arithmetic count includes all scalar additions/subtractions and nonidentity
scalar multiplications. Cold plan counts root generation and extra tensor constants.
Index arithmetic, reads, writes, and big-int bit-cost are NOT included as field ops.
"""
import json,random,time
from pathlib import Path
from crt15 import P,GENERATOR
from crt15_engine import transform as transform27, predicted as pred27
from wfta15 import transform_wfta,predicted as pred15
from fused60 import make_fused60_plan,transform_fused,predicted_fused


def run(hs=(1,2,4,8,16,32,64,128,256,512,1024)):
    rows=[]
    for h in hs:
        n=60*h;g=4*h
        plan=make_fused60_plan(n,p=P,gen=GENERATOR)
        rng=random.Random(n*3321+8101)
        x=[rng.randrange(P) for _ in range(n)]
        t0=time.perf_counter()
        o,co=transform27(x,plan.wfta.base)
        w,cw=transform_wfta(x,plan.wfta)
        f,cf=transform_fused(x,plan)
        assert o==w==f
        elapsed=round(time.perf_counter()-t0,5)
        root=plan.wfta.base.w
        # independent direct checks, all outputs for n<=240, selected frequencies for larger.
        qs=range(n) if n<=240 else (0,1,2,3,n//7,n//5,n//3,n//2,n-1)
        rt=[pow(root,j,P) for j in range(n)]
        for k in qs:
            exact=sum((x[j]*rt[(j*k)%n] for j in range(n)))%P
            assert f[k]==exact,(n,k)
        assert (co.adds,co.muls,co.total())==pred27(g)
        assert (cw.adds,cw.muls,cw.total())==pred15(g)
        assert (cf.adds,cf.muls,cf.total())==predicted_fused(h)
        setup_old=plan.wfta.base.setup.total()
        setup_w15=setup_old+plan.wfta.preparation.total()
        setup_w60=setup_w15+plan.extra_setup.total()
        assert setup_w15-setup_old==12 and setup_w60-setup_old==29
        record={
            'N':n,'H':h,'phase27_adds':co.adds,'phase27_muls':co.muls,'phase27_warm':co.total(),
            'nested15_adds':cw.adds,'nested15_muls':cw.muls,'nested15_warm':cw.total(),
            'nested60_adds':cf.adds,'nested60_muls':cf.muls,'nested60_warm':cf.total(),
            'phase27_root_setup':setup_old,'nested15_root_and_coefficient_setup':setup_w15,
            'nested60_root_and_coefficient_setup':setup_w60,
            'phase27_cold':co.total()+setup_old,'nested15_cold':cw.total()+setup_w15,
            'nested60_cold':cf.total()+setup_w60,
            'phase27_minus_nested60_warm':co.total()-cf.total(),
            'phase27_minus_nested60_cold':co.total()+setup_old-cf.total()-setup_w60,
            'nested15_minus_nested60_warm':cw.total()-cf.total(),
            'warm_pct_vs_phase27':round(100*(co.total()-cf.total())/co.total(),5),
            'cold_pct_vs_phase27':round(100*(co.total()+setup_old-cf.total()-setup_w60)/(co.total()+setup_old),5),
            'prep_copy_extra_roots':0,
            'phase27_reference_root_powers':len(plan.wfta.base.roots_g),
            'extra_combined_coefficient_slots':72,
            'selected_or_all_direct_check_count':len(qs),
            'three_circuits_exactly_equal':True,
            'arithmetic_identity_verified':True,'elapsed_seconds_not_a_speed_claim':elapsed,
        }
        assert record['phase27_minus_nested60_warm']==46*h
        assert record['phase27_minus_nested60_cold']==46*h-29
        assert record['nested15_minus_nested60_warm']==14*h
        rows.append(record)
        print(f'N={n:>6} old={co.total():>9} w15={cw.total():>9} w60={cf.total():>9} '
              f'saving={record["warm_pct_vs_phase27"]:>6.2f}% cold={record["cold_pct_vs_phase27"]:>6.2f}%',flush=True)
    with open(str(Path(__file__).resolve().parent / 'BENCHMARK_PHASE28.json'),'w') as f:json.dump(rows,f,indent=2)
    return rows

if __name__=='__main__':run()
