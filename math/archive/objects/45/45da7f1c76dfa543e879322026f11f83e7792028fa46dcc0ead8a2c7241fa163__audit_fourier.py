from collections import Counter
import json
from pathlib import Path
import random
import sys
from fourier_rational import (prepare_fourier_rational,source_solve,source_action,
                             verified_fourier_output,Counted)
from rational_reuse import apply_band
from prior_exact_arithmetic import PrimeField,CyclotomicField,fourier,mv

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'fft_qbasis_research'))
from orbit_kernel import fft,fft_plan


def main():
    rng=random.Random(90261009)
    checks=[];basis=mixed=rejects=0
    cases=[(PrimeField(p),n) for p in (65537,998244353) for n in (4,8,16,32)]
    cases += [(CyclotomicField(n),n) for n in (4,8)]
    for field,n in cases:
        q=field.root(n)
        lam=next(field.integer(v) for v in range(2,100) if field.power(field.integer(v),n)!=field.one)
        plan=prepare_fourier_rational(field,n,q,lam)
        F=fourier(field,n)
        vectors=[[field.one if i==j else field.zero for i in range(n)] for j in range(n)]
        vectors += [[field.integer(rng.randrange(-5,6)) for _ in range(n)] for _ in range(3)]
        for index,x in enumerate(vectors):
            y=mv(field,F,x)
            query,source_count=source_solve(field,plan,x)
            result,detail=verified_fourier_output(field,plan,x,y,query)
            assert result==mv(field,F,query)
            assert source_action(field,plan,query)==x
            assert apply_band(field,plan.target,result)==y
            # Direct full-matrix intertwining, including the lambda shift.
            assert mv(field,F,source_action(field,plan,x))==apply_band(field,plan.target,y)
            if index<n:basis+=1
            else:mixed+=1
        for invalid in (field.zero,field.one,q,field.neg(q)):
            try:prepare_fourier_rational(field,n,q,invalid)
            except ValueError:rejects+=1
            else:raise AssertionError('bad shift accepted')
        bad=list(query);bad[0]=field.add(bad[0],field.one)
        try:verified_fourier_output(field,plan,x,y,bad)
        except ValueError:rejects+=1
        else:raise AssertionError('wrong relation accepted')
        checks.append(dict(n=n,field=getattr(field,'p',f'Q(zeta_{n})'),preparation=plan.preparation,
                           source_online=source_count,verified_output_online=detail))
    field=PrimeField(998244353);comparisons=[]
    for n in (128,512,2048,8192):
        q=field.root(n);c=Counted(field)
        ordinary=fft_plan(c,n//2,q)
        fft_setup=dict(c.count)
        plan=prepare_fourier_rational(field,n,q,field.integer(2))
        x=[field.integer(rng.randrange(-100,101)) for _ in range(n)]
        c=Counted(field);y=fft(c,ordinary,x);anchor=dict(c.count)
        graph=Counter(fft_setup);graph.update(anchor);graph.update(plan.preparation)
        fresh=Counter(fft_setup);fresh.update(anchor);fresh.update(plan.common_preparation)
        changes=[]
        for _ in range(16):
            query,source=source_solve(field,plan,x)
            output,detail=verified_fourier_output(field,plan,x,y,query)
            c=Counted(field);truth=fft(c,ordinary,query)
            assert output==truth
            graph.update(source);graph.update(detail['field_operations'])
            fresh.update(source);fresh.update(c.count)
            changes.append(sum(a!=b for a,b in zip(query,x)))
            x,y=query,output
        comparisons.append(dict(n=n,additional_queries=16,graph_scalar_operations=sum(graph.values()),
                                ordinary_scalar_operations=sum(fresh.values()),graph_ledger=dict(graph),
                                ordinary_ledger=dict(fresh),minimum_changed_coordinates=min(changes),
                                every_query_verified=True,all_n_outputs_returned=True,
                                supplied_root_order=n))
    report=dict(status='PASS',target='FULL positive-sign DFT, unnormalized',basis_vectors=basis,
                mixed_vectors=mixed,invalid_shift_or_relation_rejections=rejects,
                cases=checks,comparisons=comparisons,
                scope='Related-query batch, initial ordinary FFT, every relation, all setup/output charged. Field counts, not timings.')
    Path(__file__).with_name('fourier_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
