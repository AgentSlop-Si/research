"""Bounded exact audits of adaptive joint decoding and paid FFT baseline."""
import json
import random
from pathlib import Path
from adaptive_recurrence import (PrimeField,CyclotomicField,prepare_adaptive,
    apply_adaptive,expected_online,Counted,denominator)
from fft_decoded_baseline import (prepare_baseline,apply_baseline,
    expected_online as baseline_online,expected_preparation as baseline_preparation)


def evaluate(field,q,z):
    out=field.zero
    for a in reversed(q):
        out=field.add(field.mul(out,z),a)
    return out


def direct(field,roots,amplitudes,n):
    return [sum_field(field,[field.mul(a,field.power(z,j))
                            for a,z in zip(amplitudes,roots)]) for j in range(n)]


def sum_field(field,values):
    out=field.zero
    for a in values:
        out=field.add(out,a)
    return out


def audit_case(field,n,period,root,indices,name,label,rng,strides=None,basis=True):
    roots=[field.power(root,i) for i in indices]
    k=len(roots)
    assert len(set(roots))==k and all(field.power(z,period)==field.one for z in roots)
    plan=prepare_adaptive(field,n,roots,strides)
    # Independent annihilator identity at every reciprocal support point.
    for z in roots:
        assert evaluate(field,plan.short_denominator,
                        field.power(field.inv(z),plan.stride))==field.zero
    l=max(2,1<<(k-1).bit_length())
    assert period%(2*l)==0
    eta=field.power(root,period//(2*l))
    assert field.power(eta,2*l)==field.one and field.power(eta,l)==field.neg(field.one)
    baseline=prepare_baseline(field,n,roots,eta)
    assert baseline.preparation==baseline_preparation(k)
    vectors=[]
    if basis:
        vectors=[[field.one if i==j else field.zero for i in range(k)] for j in range(k)]
    vectors.extend([[field.integer(rng.randrange(-5,6)) for _ in range(k)],
                    [field.zero]*k])
    for amplitudes in vectors:
        result,counts=apply_adaptive(field,plan,amplitudes)
        expected=direct(field,roots,amplitudes,n)
        other,basecounts=apply_baseline(field,baseline,amplitudes)
        assert result==other==expected,(name,n,indices,label)
        assert counts['field_operations']==expected_online(n,k,plan.initial_length,len(plan.taps))
        assert basecounts['field_operations']==baseline_online(n,k)
    # A stronger conventional comparator when the minimal Q is already sparse:
    # discover only b=1, then use its ordinary tapped recurrence.
    minimal=prepare_adaptive(field,n,roots,[1])
    minimal_value,minimal_counts=apply_adaptive(field,minimal,vectors[-2])
    assert minimal_value==apply_adaptive(field,plan,vectors[-2])[0]
    return dict(field=name,n=n,period=period,support=indices,k=k,label=label,
                basis_vectors=k if basis else 0,mixed_vectors=2,
                selected_stride=plan.stride,distinct_powers=plan.degree,
                initial_length=plan.initial_length,taps=len(plan.taps),
                candidate_count=len(plan.candidates),candidate_ledger=plan.candidates,
                adaptive_preparation=plan.preparation,
                support_equality_tests=plan.support_equality_tests,
                coefficient_zero_tests=plan.coefficient_zero_tests,
                root_zero_tests=k,
                adaptive_online=counts['field_operations'],
                baseline_preparation=baseline.preparation,
                baseline_online=basecounts['field_operations'],
                minimal_recurrence_preparation=minimal.preparation,
                minimal_recurrence_online=minimal_counts['field_operations'],
                minimal_recurrence_cold=sum(minimal.preparation.values())+sum(minimal_counts['field_operations'].values()),
                baseline_fft_calls=basecounts['fft_calls'],
                adaptive_cold=sum(plan.preparation.values())+sum(counts['field_operations'].values()),
                baseline_cold=sum(baseline.preparation.values())+sum(basecounts['field_operations'].values()),
                full_output_writes=n,status='PASS')


def main():
    rng=random.Random(20261010)
    cases=[]
    for prime in (65537,998244353):
        field=PrimeField(prime)
        for period in (8,16,32,64):
            root=field.root(period)
            for k in (1,2,min(3,period//2),min(5,period//2)):
                indices=rng.sample(range(period),k)
                cases.append(audit_case(field,period,period,root,indices,
                                        f'F_{prime}','arbitrary support',rng))
        period=4096;root=field.root(period)
        examples=[('complete coset',[1+256*j for j in range(16)]),
                  ('two partial fibers',[a+256*j for a in (1,3) for j in range(8)]),
                  ('three partial fibers',[a+256*j for a in (1,3,5) for j in range(6)]),
                  ('unstructured support',rng.sample(range(period),16))]
        for label,indices in examples:
            cases.append(audit_case(field,period,period,root,indices,
                                    f'F_{prime}',label,rng,basis=False))
    # Odd common powers: the planner accepts explicit non-dyadic candidates.
    field=PrimeField(97);root=5
    assert pow(root,96,97)==1 and pow(root,48,97)!=1 and pow(root,32,97)!=1
    cases.append(audit_case(field,96,96,root,[1,33,5,37],
                            'F_97','stride three, incomplete fibers',rng,[1,2,3,4,6]))
    for period in (8,16):
        field=CyclotomicField(period);root=field.root()
        for indices in ([1,1+period//2],[0,1,period//2],list(range(0,period,2))):
            cases.append(audit_case(field,period,period,root,indices,
                                    f'Q(zeta_{period})','cyclotomic support',rng))
    # API and degree sanity checks, separate from the arithmetic counts.
    f=PrimeField(97)
    invalid=0
    for roots,strides in (([1,1],[1]),([0,1],[1]),([1,2],[0]),([1,2],[True]),([1,2],[1.5])):
        try:prepare_adaptive(f,8,roots,strides)
        except (ValueError,TypeError):invalid+=1
        else:raise AssertionError((roots,strides))
    result=dict(status='PASS',configurations=len(cases),
                basis_vectors=sum(c['basis_vectors'] for c in cases),
                mixed_vectors=sum(c['mixed_vectors'] for c in cases),invalid_input_controls=invalid,
                full_output_coordinates=sum(c['n']*(c['basis_vectors']+c['mixed_vectors']) for c in cases),
                scope='support-adaptive sparse annihilators; no uniform arbitrary-support improvement',
                cases=cases)
    out=Path(__file__).parent/'results';out.mkdir(exist_ok=True)
    (out/'joint_decode_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
    for row in cases:
        if row['field']=='F_65537' and row['n']==4096:
            print(json.dumps({k:row[k] for k in ('label','k','selected_stride','distinct_powers',
                'initial_length','taps','adaptive_preparation','adaptive_online','baseline_preparation',
                'baseline_online','adaptive_cold','minimal_recurrence_cold','baseline_cold')}))


if __name__=='__main__':main()
