import json
from pathlib import Path
from fourier_rational import (prepare_fourier_rational,source_solve,
                             corrected_fourier_output,try_recurrence_fourier)
from prior_exact_arithmetic import PrimeField,CyclotomicField,fourier,mv


def main():
    accepted=declined=0;rows=[]
    cases=[(PrimeField(p),n) for p in (65537,998244353) for n in (4,8,16,32)]
    cases += [(CyclotomicField(n),n) for n in (4,8)]
    for field,n in cases:
        q=field.root(n)
        lam=next(field.integer(v) for v in range(2,100) if field.power(field.integer(v),n)!=field.one)
        plan=prepare_fourier_rational(field,n,q,lam)
        F=fourier(field,n)
        for support in (0,1,2):
            forcing=[field.zero]*n
            for j in range(support):forcing[n-1-j]=field.integer(j+1)
            x,_=source_solve(field,plan,forcing)
            output,info=try_recurrence_fourier(field,plan,x,max_defects=support)
            assert info['accepted'] and info['defect_support']==support
            assert output==mv(field,F,x)
            if support==1:assert all(a!=field.zero for a in x)
            accepted+=1
            if support:
                output,bad=try_recurrence_fourier(field,plan,x,max_defects=support-1)
                assert output is None and not bad['accepted'];declined+=1
            rows.append(dict(n=n,field=getattr(field,'p',f'Q(zeta_{n})'),support=support,
                             dense_input=all(a!=field.zero for a in x),
                             cold_preparation=plan.preparation,online=info))
        anchor=[field.integer(j+1) for j in range(n)]
        anchor_y=mv(field,F,anchor)
        forcing=list(anchor);forcing[n//2]=field.add(forcing[n//2],field.integer(7))
        query,_=source_solve(field,plan,forcing)
        output,info=corrected_fourier_output(field,plan,anchor,anchor_y,query,max_defects=1)
        assert output==mv(field,F,query) and info['defect_support']==1;accepted+=1
        # A truly dense residual must decline at the small advertised cap.
        query,_=source_solve(field,plan,[field.one]*n)
        output,info=try_recurrence_fourier(field,plan,query,max_defects=2)
        assert output is None and info['defect_support']==n;declined+=1
    report=dict(status='PASS',accepted_exact_full_dfts=accepted,declined_controls=declined,
                cases=rows,scope='Fresh structured or sparse-corrected related input; supplied shift, no universal FFT bound.')
    Path(__file__).with_name('defect_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
