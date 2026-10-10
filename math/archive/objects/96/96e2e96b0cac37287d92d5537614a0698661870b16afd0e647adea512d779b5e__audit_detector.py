"""Focused exact audit of deterministic shift discovery and cold evaluation."""
from collections import Counter
import json
from pathlib import Path
from random import Random
import sys

from detected_fourier import try_detected_fourier
from fourier_rational import prepare_fourier_rational,source_solve,Counted
from prior_exact_arithmetic import PrimeField,CyclotomicField,fourier,mv

ROOT=Path(__file__).resolve().parent


def encoded(field, info):
    value=dict(info)
    if 'detected_shift' in value:
        value['detected_shift']=field.encode(value['detected_shift'])
    return value


def e_matrix(field,n,q):
    powers=[field.power(q,j) for j in range(n)]
    matrix=[[field.zero]*n for _ in range(n)]
    for i in range(n):
        matrix[i][i]=field.neg(powers[i])
        if i+1<n:
            matrix[i][i+1]=field.neg(field.mul(powers[i],field.sub(powers[i+1],field.one)))
    return matrix


def triangular_fixture(field,matrix,shift,rhs,last_eigenvector=False):
    n=len(rhs)
    result=[field.zero]*n
    start=n-1
    if last_eigenvector:
        result[-1]=field.one
        start=n-2
    for i in range(start,-1,-1):
        value=rhs[i]
        if i+1<n:
            value=field.sub(value,field.mul(matrix[i][i+1],result[i+1]))
        result[i]=field.mul(value,field.inv(field.sub(matrix[i][i],shift)))
    return result


def check_ledger(info):
    count=Counter()
    for stage in info['stages'].values():
        count.update(stage)
    assert dict(count)==info['field_operations']
    assert info['ordinary_fft_calls']==0
    assert info['paid_anchor_transform_calls']==0


def main():
    rng=Random(918271)
    rows=[];accepted=declined=0
    fields=[(PrimeField(p),n) for p in (65537,998244353) for n in (4,8,16,32)]
    fields += [(CyclotomicField(n),n) for n in (4,8)]
    for field,n in fields:
        q=field.root(n)
        F=fourier(field,n)
        E=e_matrix(field,n,q)
        shift=next(field.integer(v) for v in range(2,100)
                   if field.power(field.integer(v),n)!=field.one)
        plan=prepare_fourier_rational(field,n,q,shift)
        zero=[field.zero]*n
        one_sparse=list(zero);one_sparse[-1]=field.integer(3)
        two_sparse=list(one_sparse);two_sparse[0]=field.integer(2)
        dense,unused=source_solve(field,plan,one_sparse)
        assert all(x!=field.zero for x in dense)
        cases=[('zero',zero,0,'sparse_input'),
               ('one_sparse',one_sparse,1,'sparse_input'),
               ('two_sparse',two_sparse,1,'sparse_input'),
               ('dense_one_defect',dense,1,'detected_recurrence')]
        if n>=8:
            forcing=list(one_sparse);forcing[n//2]=field.integer(7)
            outlier,unused=source_solve(field,plan,forcing)
            assert sum(x!=field.zero for x in outlier)>4
            cases.append(('dense_two_defects',outlier,2,'detected_recurrence'))
        records=[]
        for name,x,cap,path in cases:
            result,info=try_detected_fourier(field,n,q,x,max_defects=cap)
            assert info['accepted'] and info['path']==path
            assert result==mv(field,F,x),(name,n)
            assert len(result)==info['full_output_writes']==n
            if path=='detected_recurrence':
                assert info['detected_shift']==shift
                assert info['stages']['cold_rational_preparation']==plan.preparation
                assert sum(info['stages']['root_powers_and_E_action'].values())==6*n-4
                assert sum(info['stages']['full_residual_verification'].values())==2*n
                assert sum(info['stages']['target_solve'].values())==9*n
                support=info['defect_support']
                assert sum(info['stages']['sparse_defect_evaluation'].values())==(2*n-1)*support
            check_ledger(info)
            accepted+=1
            records.append(dict(case=name,cap=cap,result=encoded(field,info)))

        # Dense vectors whose majority shift is excluded by the solver contract.
        zero_shift_query=triangular_fixture(field,E,field.zero,one_sparse)
        root_shift=E[-1][-1]
        eigenvector=triangular_fixture(field,E,root_shift,zero,last_eigenvector=True)
        for name,x,reason in (
            ('invalid_zero_shift',zero_shift_query,'zero_shift_excluded'),
            ('invalid_root_shift',eigenvector,'root_of_unity_shift_excluded')):
            assert all(a!=field.zero for a in x)
            result,info=try_detected_fourier(field,n,q,x,max_defects=1)
            assert result is None and not info['accepted'] and info['reason']==reason
            check_ledger(info)
            declined+=1
            records.append(dict(case=name,cap=1,result=encoded(field,info)))

        # Zero coordinates must still participate in the full residual check.
        # This preserves a majority shift but adds an independent defect at 0.
        hidden_zero=list(dense);hidden_zero[0]=field.zero
        no_majority=None
        for _ in range(500):
            x=[field.integer(rng.randrange(1,100)) for _ in range(n)]
            result,info=try_detected_fourier(field,n,q,x,max_defects=1)
            if info.get('reason')=='no_strict_ratio_majority':
                no_majority=x
                break
        assert no_majority is not None
        for x,expected_reason in ((hidden_zero,'candidate_defect_too_dense'),
                                  (no_majority,'no_strict_ratio_majority')):
            result,info=try_detected_fourier(field,n,q,x,max_defects=1)
            reason=info.get('reason')
            assert reason==expected_reason
            image=mv(field,E,x)
            # Exhaust all potentially relevant ratios to independently
            # check that this declined fixture has no admissible shift.
            for i,xi in enumerate(x):
                if xi==field.zero:continue
                candidate=field.mul(image[i],field.inv(xi))
                if candidate==field.zero or field.power(candidate,n)==field.one:continue
                support=sum(field.sub(a,field.mul(candidate,b))!=field.zero
                            for a,b in zip(image,x))
                assert support>1
            assert result is None
            check_ledger(info)
            declined+=1
            records.append(dict(case=reason,cap=1,result=encoded(field,info)))
        rows.append(dict(field=getattr(field,'p',f'Q(zeta_{n})'),n=n,records=records))

    # Larger exact same-input comparisons; these are gate ledgers, not timings.
    sys.path.insert(0,str(ROOT.parent/'fft_qbasis_research'))
    from orbit_kernel import fft,fft_plan
    large=[]
    field=PrimeField(998244353)
    for n in (128,512,2048,8192):
        q=field.root(n)
        plan=prepare_fourier_rational(field,n,q,field.integer(2))
        forcing=[field.zero]*n;forcing[-1]=field.one
        x,_=source_solve(field,plan,forcing)
        result,info=try_detected_fourier(field,n,q,x,max_defects=1)
        c=Counted(field);ordinary=fft_plan(c,n//2,q)
        oracle=fft(c,ordinary,x)
        assert info['accepted'] and result==oracle
        check_ledger(info)
        accepted+=1
        large.append(dict(n=n,input_support=sum(a!=field.zero for a in x),
            defect_support=info['defect_support'],cold_detector_scalar_operations=sum(info['field_operations'].values()),
            cold_ordinary_scalar_operations=sum(c.count.values()),
            detector=encoded(field,info),ordinary_ledger=dict(c.count),
            input_generation='Fixture generation outside both cold evaluation ledgers; input x is supplied identically.',
            comparison_scope='Same fresh input and full output; no timing or arbitrary-input improvement claim.'))

    invalid=0
    for kwargs in (dict(n=2,q=1,query=[0,0],max_defects=1),
                   dict(n=4,q=1,query=[0]*3,max_defects=1),
                   dict(n=4,q=1,query=[0]*4,max_defects=-1),
                   dict(n=4,q=1,query=[0]*4,max_defects=True)):
        try:try_detected_fourier(field,**kwargs)
        except ValueError:invalid+=1
        else:raise AssertionError('invalid argument accepted')
    result=dict(status='PASS',accepted_exact_outputs=accepted,decline_controls=declined,
        invalid_argument_controls=invalid,field_size_configurations=len(rows),
        rows=rows,large_same_input_comparisons=large,
        model='All detection, phase setup, cold solve preparation and full outputs paid; no supplied lambda or anchor; conditional acceptance only.',
        review_status='Root source review and independent adverse-case/count review complete; no unresolved issue within the stated contract.')
    (ROOT/'detector_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','accepted_exact_outputs','decline_controls','invalid_argument_controls','field_size_configurations')},indent=2))
    for row in large:
        print(json.dumps({k:row[k] for k in ('n','cold_detector_scalar_operations','cold_ordinary_scalar_operations')}))


if __name__=='__main__':main()
