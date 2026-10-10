"""Focused adversarial detector checks; existing band solver is not re-audited."""
from collections import Counter
from pathlib import Path
import hashlib
import json
from detected_fourier import try_detected_fourier
from fourier_rational import Counted,prepare_fourier_rational,source_solve
from prior_exact_arithmetic import PrimeField,fourier,mv


def main():
    field=PrimeField(65537);n=8;q=field.root(n)
    plan=prepare_fourier_rational(field,n,q,field.integer(2))
    matrix=fourier(field,n)
    forcing=[field.zero]*n;forcing[-1]=field.one
    dense,_=source_solve(field,plan,forcing)
    hidden=list(dense);hidden[0]=field.zero
    forcing=[field.zero]*n;forcing[4]=field.one
    boundary,_=source_solve(field,plan,forcing)
    diagonal=[field.neg(field.power(q,i)) for i in range(n)]
    upper=[field.neg(field.mul(field.power(q,i),
                             field.sub(field.power(q,i+1),field.one)))
           for i in range(n-1)]
    eigen=[field.zero]*n;eigen[-1]=field.one
    for i in range(n-2,-1,-1):
        eigen[i]=field.mul(field.neg(field.mul(upper[i],eigen[i+1])),
                           field.inv(field.sub(diagonal[i],diagonal[-1])))
    zero_shift=[field.zero]*n
    for i in range(n-1,-1,-1):
        rhs=field.one if i==n-1 else field.neg(field.mul(upper[i],zero_shift[i+1]))
        zero_shift[i]=field.mul(rhs,field.inv(diagonal[i]))
    cases=[('zero',[0]*n,0,'sparse_input',None),
           ('support_2s',[1,2,3,4,0,0,0,0],2,'sparse_input',None),
           ('support_2s_plus_1',boundary,2,'detected_recurrence',None),
           ('dense_recurrence',dense,1,'detected_recurrence',None),
           ('defect_at_zero_coordinate',hidden,1,'declined','candidate_defect_too_dense'),
           ('zero_ratio_majority',zero_shift,1,'declined','zero_shift_excluded'),
           ('root_ratio_majority',eigen,0,'declined','root_of_unity_shift_excluded'),
           ('no_majority',list(range(1,n+1)),0,'declined','no_strict_ratio_majority')]
    rows=[]
    for name,query,cap,path,reason in cases:
        observed=Counted(field)
        output,meta=try_detected_fourier(observed,n,q,query,max_defects=cap)
        assert meta['path']==path
        assert Counter(meta['field_operations'])==observed.count
        staged=Counter()
        for count in meta['stages'].values():staged.update(count)
        assert staged==observed.count
        if output is not None:
            assert output==mv(field,matrix,query)
            assert meta['full_output_writes']==n
        else:
            assert meta['reason']==reason and meta['full_output_writes']==0
        if path!='sparse_input':
            assert sum(meta['stages']['root_powers_and_E_action'].values())==6*n-4
        if name=='defect_at_zero_coordinate':
            assert meta['detected_shift']==2 and meta['defect_support']==2
            assert meta['defect_support_comparisons']==n
        rows.append(dict(name=name,path=path,reason=reason,
                         field_operations=dict(observed.count),ledger_exact=True))
    root=Path(__file__).resolve().parent
    result=dict(status='PASS',cases=rows,accepted_full_dfts=4,adverse_declines=4,
                outer_field_ledger_matches=8,stage_ledger_matches=8,
                source_sha256=hashlib.sha256((root/'detected_fourier.py').read_bytes()).hexdigest())
    (root/'detector_independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
