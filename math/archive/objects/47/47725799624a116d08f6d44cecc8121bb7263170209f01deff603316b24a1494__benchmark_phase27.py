"""Reproducible exact scalar-count comparison; only executes feasible tested sizes."""
import json,random
from crt15 import P,GENERATOR,direct_dft
from crt15_engine import make_plan,transform,predicted

def run():
    rows=[]
    for G in (1,2,4,8,16,32,64,128,256,512,1024,2048,4096):
        n=15*G
        rng=random.Random(27*n)
        x=[rng.randrange(P) for _ in range(n)]
        gt=make_plan(n,mode='gt');ct=make_plan(n,mode='ct')
        a,ca=transform(x,gt)
        b,cb=transform(x,ct)
        d,cd=transform(x,ct,inner='ct')
        assert a==b==d
        if n<=480:assert a==direct_dft(x)
        else:
            powers=[pow(gt.w,i,P) for i in range(n)]
            for k in (0,1,2,3,n//3,n//2,n-1):
                z=sum(x[j]*powers[(j*k)%n] for j in range(n))%P
                assert a[k]==z
        assert (ca.adds,ca.muls,ca.total())==predicted(G)
        assert cb.total()-ca.total()==14*(G-1)
        assert cd.total()-ca.total()==22*G-14
        record={
            'N':n,'G':G,'GT_warm_adds':ca.adds,'GT_warm_muls':ca.muls,
            'GT_warm_total':ca.total(),'CT_same_kernels_warm':cb.total(),
            'CT_fully_mixed_warm':cd.total(),
            'GT_cold_setup':gt.setup.total(),'CT_cold_setup':ct.setup.total(),
            'GT_cold_total':ca.total()+gt.setup.total(),
            'CT_fully_mixed_cold_total':cd.total()+ct.setup.total(),
            'warm_saving_ops':cd.total()-ca.total(),
            'warm_saving_pct':round((cd.total()-ca.total())/cd.total()*100,5),
            'cold_saving_ops':cd.total()+ct.setup.total()-ca.total()-gt.setup.total(),
            'cold_saving_pct':round((cd.total()+ct.setup.total()-ca.total()-gt.setup.total())/(cd.total()+ct.setup.total())*100,5),
            'CT_minus_GT_extra_root_table_cells':n+15,
            'pairwise_exact':True,
        }
        rows.append(record)
        print(f'N={n:>6} GT={ca.total():>8} CTfull={cd.total():>8} '
              f'warm saving={record["warm_saving_pct"]:5.2f}%  '
              f'cold saving={record["cold_saving_pct"]:5.2f}%')
    with open('BENCHMARK_PHASE27.json','w') as f:json.dump(rows,f,indent=2)
if __name__=='__main__':run()
