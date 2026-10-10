"""Exact full-output and operation audit for direct target scans/all shifts."""
from collections import Counter
import json
from pathlib import Path
from random import Random
import sys

from extended_recurrence import try_extended_fourier,Counted
from detected_fourier import try_detected_fourier
from prior_exact_arithmetic import PrimeField,CyclotomicField,fourier,mv

HERE=Path(__file__).resolve().parent


def source_data(field,n,q):
    powers=[field.power(q,j) for j in range(n)]
    diagonal=[field.neg(v) for v in powers]
    upper=[field.neg(field.mul(powers[i],field.sub(powers[i+1],field.one)))
           for i in range(n-1)]
    return diagonal,upper


def source_solve(field,diagonal,upper,shift,forcing):
    x=[field.zero]*len(forcing)
    for i in range(len(x)-1,-1,-1):
        value=forcing[i]
        if i+1<len(x):value=field.sub(value,field.mul(upper[i],x[i+1]))
        x[i]=field.mul(value,field.inv(field.sub(diagonal[i],shift)))
    return x


def source_eigenvector(field,diagonal,upper,t):
    x=[field.zero]*len(diagonal)
    x[t]=field.one
    for i in range(t-1,-1,-1):
        x[i]=field.mul(field.neg(field.mul(upper[i],x[i+1])),
                       field.inv(field.sub(diagonal[i],diagonal[t])))
    return x


def serialize(field,info):
    result=dict(info)
    if 'shift' in result:result['shift']=field.encode(result['shift'])
    return result


def checked(field,n,q,x,cap,F,shift=None,supplied=False):
    outer=Counted(field)
    options=dict(max_defects=cap)
    if supplied:options['shift']=shift
    result,info=try_extended_fourier(outer,n,q,x,**options)
    assert dict(outer.count)==info['field_operations']
    stages=Counter()
    for stage in info['stages'].values():stages.update(stage)
    assert dict(stages)==info['field_operations']
    if info['accepted']:
        assert result==mv(field,F,x)
        assert len(result)==info['full_output_writes']==n
    else:
        assert result is None and info['full_output_writes']==0
    return result,info


def main():
    configs=[(PrimeField(5),4),(PrimeField(17),4),(PrimeField(17),8)]
    configs += [(PrimeField(p),n) for p in (65537,998244353) for n in (4,8,16,32)]
    configs += [(CyclotomicField(n),n) for n in (4,8)]
    rng=Random(99231)
    rows=[];accepted=declined=0;branches=Counter()
    for field,n in configs:
        q=field.root(n)
        F=fourier(field,n)
        diagonal,upper=source_data(field,n,q)
        forcing=[field.zero]*n;forcing[-1]=field.one
        nonroot=next((field.integer(v) for v in range(2,100)
                     if field.integer(v)!=field.zero and
                        field.power(field.integer(v),n)!=field.one),None)
        fixtures=[]
        for shift,label in ((field.zero,'zero_shift'),(nonroot,'nonroot_shift')):
            if shift is None:continue
            x=source_solve(field,diagonal,upper,shift,forcing)
            assert all(a!=field.zero for a in x)
            fixtures.append((label,x,1,shift))
        for t in range(n):
            x=source_eigenvector(field,diagonal,upper,t)
            fixtures.append((f'root_eigenvector_{t}',x,0,diagonal[t]))
        records=[]
        for name,x,cap,shift in fixtures:
            result,info=checked(field,n,q,x,cap,F)
            assert info['accepted'] and info['shift']==shift
            accepted+=1
            branches[info.get('target',{}).get('branch','sparse_input')]+=1
            # Supplying the same shift bypasses discovery, still paying its
            # complete verification and target solve.
            supplied,supplied_info=checked(field,n,q,x,cap,F,shift=shift,supplied=True)
            assert supplied==result
            accepted+=1
            old,old_info=try_detected_fourier(field,n,q,x,max_defects=cap)
            if name=='nonroot_shift':assert old==result
            else:assert old is None and not old_info['accepted']
            records.append(dict(case=name,cap=cap,automatic=serialize(field,info),
                                supplied=serialize(field,supplied_info),old_accepted=old_info['accepted']))
        sparse=[field.zero]*n;sparse[-1]=field.one
        result,info=checked(field,n,q,sparse,1,F)
        assert info['path']=='sparse_input'
        accepted+=1
        records.append(dict(case='sparse_input',automatic=serialize(field,info)))

        # Dense unrelated controls decline with their complete discovery cost.
        for _ in range(100):
            x=[field.integer(rng.randrange(1,100)) for _ in range(n)]
            result,info=checked(field,n,q,x,0,F)
            if not info['accepted']:
                declined+=1
                records.append(dict(case='unrelated_decline',automatic=serialize(field,info)))
                break
        else:raise AssertionError('missing decline fixture')
        rows.append(dict(n=n,field=getattr(field,'p',f'Q(zeta_{n})'),records=records))
    assert branches['zero_shift_scan']>0
    assert branches['singular_missing_coordinate']>0

    sys.path.insert(0,str(HERE.parent/'fft_qbasis_research'))
    from orbit_kernel import fft,fft_plan
    field=PrimeField(998244353)
    comparisons=[]
    for n in (128,512,2048,8192,131072):
        q=field.root(n)
        diagonal,upper=source_data(field,n,q)
        forcing=[field.zero]*n;forcing[-1]=field.one
        x=source_solve(field,diagonal,upper,field.integer(2),forcing)
        outer=Counted(field)
        result,info=try_extended_fourier(outer,n,q,x,max_defects=1)
        assert info['accepted'] and dict(outer.count)==info['field_operations']
        assert sum(info['field_operations'].values())==25*n-10
        c=Counted(field);plan=fft_plan(c,n//2,q)
        expected=fft(c,plan,x)
        assert result==expected
        old,old_info=try_detected_fourier(field,n,q,x,max_defects=1)
        assert old==result
        accepted+=1
        comparisons.append(dict(n=n,input_support=n,defect_support=1,
            extended_cold_scalar_operations=sum(info['field_operations'].values()),
            previous_cold_scalar_operations=sum(old_info['field_operations'].values()),
            ordinary_cold_scalar_operations=sum(c.count.values()),
            extended=serialize(field,info),ordinary_ledger=dict(c.count),
            same_input_same_full_output=True,
            note='Fixture construction is excluded equally; both evaluate the same supplied fresh x. Gate counts, not timings.'))
    zero_comparisons=[]
    for n in (128,512,2048,8192):
        q=field.root(n)
        diagonal,upper=source_data(field,n,q)
        forcing=[field.zero]*n;forcing[-1]=field.one
        x=source_solve(field,diagonal,upper,field.zero,forcing)
        outer=Counted(field)
        result,info=try_extended_fourier(outer,n,q,x,max_defects=1)
        assert info['accepted'] and info['target']['branch']=='zero_shift_scan'
        assert dict(outer.count)==info['field_operations']
        assert sum(info['field_operations'].values())==14*n-10
        c=Counted(field);plan=fft_plan(c,n//2,q)
        expected=fft(c,plan,x)
        assert result==expected
        old,old_info=try_detected_fourier(field,n,q,x,max_defects=1)
        assert old is None and old_info['reason']=='zero_shift_excluded'
        accepted+=1
        zero_comparisons.append(dict(n=n,input_support=n,defect_support=1,
            extended_cold_scalar_operations=sum(info['field_operations'].values()),
            ordinary_cold_scalar_operations=sum(c.count.values()),
            previous_evaluator_declined=True,extended=serialize(field,info),
            same_input_same_full_output=True,
            note='Supplied fresh dense x, detected zero shift; fixture construction excluded equally; field gates, not timings.'))
    invalid=0
    for kwargs in (dict(n=2,q=1,query=[0,0]),dict(n=4,q=1,query=[0]*3),
                   dict(n=4,q=1,query=[0]*4,max_defects=-1),
                   dict(n=4,q=1,query=[0]*4,max_defects=True)):
        try:try_extended_fourier(field,**kwargs)
        except ValueError:invalid+=1
        else:raise AssertionError('invalid call accepted')
    report=dict(status='PASS',accepted_exact_outputs=accepted,declines=declined,
        invalid_argument_rejections=invalid,field_size_configurations=len(rows),
        target_branches=dict(branches),rows=rows,same_target_comparisons=comparisons,
        zero_shift_comparisons=zero_comparisons,
        scope='All shifts, paid deterministic discovery, exact full outputs for accepted restricted families; no universal faster FFT.')
    (HERE/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','accepted_exact_outputs','declines','invalid_argument_rejections','field_size_configurations','target_branches')},indent=2))
    for row in comparisons:
        print(json.dumps({k:row[k] for k in ('n','extended_cold_scalar_operations','previous_cold_scalar_operations','ordinary_cold_scalar_operations')}))
    for row in zero_comparisons:
        print(json.dumps(dict(shift='zero',**{k:row[k] for k in ('n','extended_cold_scalar_operations','ordinary_cold_scalar_operations')})))


if __name__=='__main__':main()
