import json
from pathlib import Path
import random
from cycle_flow import compile_flow, apply_compiled, apply_explicit
from prior_exact_arithmetic import PrimeField, CyclotomicField


def run():
    rng=random.Random(80721)
    cases=[]; bases=0; choices=0
    fields=[(PrimeField(65537),'F65537',(2,4,8,16)),
            (PrimeField(998244353),'F998244353',(2,4,8,16))]
    fields += [(CyclotomicField(n),f'Q(zeta{n})',(n,)) for n in (2,4,8)]
    for field,label,lengths in fields:
        for n in lengths:
            q=field.root(n)
            for logb in range(1,n.bit_length()):
                b=1<<logb
                standard=list(range(0,n,n//b))
                patterns=[('complete',standard),
                          ('one_forward',[(standard[0]+1)%n]+standard[1:]),
                          ('one_backward',[(standard[0]-1)%n]+standard[1:]),
                          ('random',[rng.randrange(n) for _ in range(b)])]
                for name,exps in patterns:
                    plan=compile_flow(n,exps)
                    brute=min(sum(abs(f-shift) for f in plan.raw_flow)
                              for shift in range(min(plan.raw_flow)-1,max(plan.raw_flow)+2))
                    assert plan.distance==brute
                    choices+=1
                    for j in range(n):
                        x=[field.one if k==j else field.zero for k in range(n)]
                        got,counts=apply_compiled(field,q,plan,x)
                        want,_=apply_explicit(field,n,q,exps,x)
                        assert got==want,(label,n,b,name,j)
                        assert counts['correction']['field_operations'].get('mul',0)==(n-1)*plan.distance
                        bases+=1
                    cases.append({'field':label,'n':n,'b':b,'pattern':name,
                                  'phase_exponents':exps,'cycle_distance':plan.distance,
                                  'flow':list(plan.flow),'basis_vectors':n})
    # Large instance follows the proved single-defect identity directly.
    n=4096; field=PrimeField(998244353); q=field.root(n)
    exps=list(range(n)); exps[0]=1
    plan=compile_flow(n,exps)
    x=[field.integer(rng.randrange(field.p)) for _ in range(n)]
    got,counts=apply_compiled(field,q,plan,x)
    expected=[x[0]]+[field.sub(x[j],x[j-1]) for j in range(1,n)]
    assert got==expected and plan.distance==1
    report={'status':'PASS','operator_cases':len(cases),'complete_basis_vectors':bases,
            'median_optimality_cases':choices,'cases':cases,
            'large_single_defect':{'n':n,'b':n,'distance':1,'counts':counts,
             'verification':'Compared with proved first-difference formula, not N explicit full convolutions.'},
            'scope':'Exact restricted-operator compiler; arbitrary inputs; no general FFT bound.'}
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('cases','large_single_defect')}))


if __name__=='__main__':run()
