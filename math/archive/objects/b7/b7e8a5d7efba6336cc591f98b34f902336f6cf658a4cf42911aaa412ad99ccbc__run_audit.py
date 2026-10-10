import json
from pathlib import Path
import random

from exact_fields import PrimeField,CyclotomicField,fourier,mv
from qlinear import Counted,cycle_solve,try_qlinear_fourier


def encoded(field,v):
    if isinstance(v,dict):return {k:encoded(field,x) for k,x in v.items()}
    if isinstance(v,list):return [encoded(field,x) for x in v]
    if isinstance(v,tuple):return field.encode(v)
    return v


def main():
    rng=random.Random(20261009);accepted=declined=singular=0;rows=[]
    fields=[(PrimeField(p),n) for p in (97,65537,998244353) for n in (4,8,16,32)]
    fields += [(CyclotomicField(n),n) for n in (4,8)]
    for f,n in fields:
        q=f.root(n);F=fourier(f,n)
        fixtures=[('zero',[f.zero]*n)]
        for j in range(n):
            x=[f.zero]*n;x[j]=f.one;fixtures.append(('basis',x))
        for t in range(min(n,5)):
            fixtures.append(('geometric',[f.power(q,t*i) for i in range(n)]))
        fixtures.append(('chirp',[f.power(q,i*(i-1)//2) for i in range(n)]))
        for sample in range(5):
            for attempt in range(100):
                pars=[f.integer(rng.randrange(1,40)) for _ in range(4)]
                den=[f.add(pars[2],f.mul(pars[3],f.power(q,i))) for i in range(n-1)]
                if all(v!=f.zero for v in den):break
            x=[f.integer(sample+1)]
            for i in range(n-1):
                a=f.add(pars[0],f.mul(pars[1],f.power(q,i)))
                x.append(f.neg(f.mul(f.mul(a,x[-1]),f.inv(den[i]))))
            fixtures.append(('linear_fractional_ratio',x))
        details=[]
        for name,x in fixtures:
            observed=Counted(f)
            y,meta=try_qlinear_fourier(observed,n,q,x)
            assert meta['accepted'] and y==mv(f,F,x),(n,name,meta)
            assert dict(observed.count)==meta['field_operations']
            summed={}
            for ledger in meta['stages'].values():
                for key,val in ledger.items():summed[key]=summed.get(key,0)+val
            assert summed==meta['field_operations']
            accepted+=1;singular+=meta['target_nullity']
            details.append(dict(kind=name,dense=all(v!=f.zero for v in x),metadata=encoded(f,meta)))
        for _ in range(6):
            x=[f.integer(rng.randrange(100)) for _ in range(n)]
            observed=Counted(f)
            y,meta=try_qlinear_fourier(observed,n,q,x)
            assert dict(observed.count)==meta['field_operations']
            if y is None:
                assert meta['relation_rank']==4;declined+=1
            else:
                assert y==mv(f,F,x);accepted+=1;singular+=meta['target_nullity']
        rows.append(dict(n=n,field=getattr(f,'p',f'Q(zeta_{n})'),cases=details))

    # Focused cycle edge controls, with an independent known solution.
    f=PrimeField(97);c=Counted(f);n=8;x=list(range(1,n+1));cycle_cases=0
    for a,b in [([1]*n,[2]*n),([1]*n,[96]*n),
                ([0]+[1]*(n-1),[2]*n),([1]*n,[0]+[2]*(n-1)),
                ([1]*n,[0]*n),([0]+[1]*(n-1),[0]*n),
                ([0]+[1]*(n-1),[0]+[2]*(n-1)),
                ([0]+[1]*(n-1),[2,0]+[2]*(n-2))]:
        rhs=[f.add(f.mul(a[i],x[i]),f.mul(b[i],x[(i+1)%n])) for i in range(n)]
        p,kernels=cycle_solve(c,a,b,rhs)
        assert [f.add(f.mul(a[i],p[i]),f.mul(b[i],p[(i+1)%n])) for i in range(n)]==rhs
        for h in kernels:assert all(f.add(f.mul(a[i],h[i]),f.mul(b[i],h[(i+1)%n]))==0 for i in range(n))
        cycle_cases+=1
    invalid=0
    for n,q,x in [(2,96,[0]*2),(8,1,[0]*8),(8,2,[0]*8),(8,33,[0]*7)]:
        try:try_qlinear_fourier(f,n,q,x)
        except ValueError:invalid+=1
        else:raise AssertionError('bad root/shape accepted')

    report=dict(status='PASS',accepted_exact_full_outputs=accepted,declined_unstructured=declined,
                singular_reconstructions=singular,cycle_edge_controls=cycle_cases,
                invalid_root_or_shape_controls=invalid,field_size_configurations=len(rows),cases=rows,
                scope='Fresh inputs with verified degree-one q-recurrence; adaptive exact-field model; no universal FFT improvement.')
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
