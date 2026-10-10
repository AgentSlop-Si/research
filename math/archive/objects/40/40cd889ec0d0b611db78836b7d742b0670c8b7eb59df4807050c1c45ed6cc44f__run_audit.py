"""Independent exact C-Horner and block-tail checks."""
import json
import random
import sys
from pathlib import Path
from tail_blocks import prepare_tail,apply_tail,expected_online,expected_preparation
from operators import prepare_sparse,horner_c
from fixed_kernel import lower_convolution
from prior_exact_arithmetic import PrimeField,CyclotomicField
from full_similarity import (prepare_full,apply_full,
    expected_online as expected_full_online,expected_preparation as expected_full_preparation)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'fft_qweyl_resolvent_research'))
from resolvent import prepare_resolvent,solve


def audit_case(field,n,r,name,rng):
    q=field.root(n)
    assert field.power(q,n)==field.one
    assert field.power(q,n//2)!=field.one
    plan=prepare_tail(field,n,r,q)
    sparse=prepare_sparse(field,n,q)
    assert plan.preparation==expected_preparation(n,r),(n,r,plan.preparation,expected_preparation(n,r))
    p=[field.zero]*(n-r)+plan.polynomial
    vectors=[[field.one if i==j else field.zero for i in range(n)] for j in range(n)]
    vectors.append([field.integer(rng.randrange(-5,6)) for _ in range(n)])
    for x in vectors:
        y,counts=apply_tail(field,plan,x)
        expected,horner_counts=horner_c(field,sparse,p,x)
        assert y==expected,(name,n,r)
        assert counts['field_operations']==expected_online(n,r)
        # Independent direct calculation through the two triangular kernels.
        z=lower_convolution(field,plan.kernel.middle,x)[n-r:]
        scaled=[field.mul(g,a) for g,a in zip(plan.g_tail,z)]
        compressed=[]
        for i in range(r):
            v=field.zero
            for j in range(i,r):
                v=field.add(v,field.mul(plan.polynomial[j-i],scaled[j]))
            compressed.append(field.mul(plan.inverse_g_head[i],v))
        assert lower_convolution(field,plan.kernel.kernel,
                                 compressed+[field.zero]*(n-r))==y
    # Also check that the evaluator is not hard-coded to the H_q tail.
    arbitrary=[field.integer(2-3*j+j*j) for j in range(r)]
    other=prepare_tail(field,n,r,q,arbitrary)
    expected,_=horner_c(field,sparse,[field.zero]*(n-r)+arbitrary,vectors[-1])
    assert apply_tail(field,other,vectors[-1])[0]==expected
    aggregate_checks=0
    if n<=16:
        resolvent=prepare_resolvent(field,n,q)
        # Direct independent N-pole summation; reference only, not the fast path.
        for tested in (plan,other):
            combined=[field.zero]*n
            for j in range(n):
                lam=field.power(q,j)
                value=field.zero
                for coefficient in reversed(tested.polynomial):
                    value=field.add(field.mul(value,lam),coefficient)
                weight=field.mul(field.mul(field.power(lam,(1-r)%n),value),
                                 plan.kernel.kernel[-1])
                resolved,_=solve(field,resolvent,lam,vectors[-1])
                combined=[field.add(a,field.mul(weight,b))
                          for a,b in zip(combined,resolved)]
            assert combined==apply_tail(field,tested,vectors[-1])[0]
            aggregate_checks+=1
    comparator=None
    if isinstance(field,PrimeField):
        eta=field.root(2*n)
        assert field.mul(eta,eta)==q
        assert field.power(eta,n)==field.neg(field.one)
        full=prepare_full(field,n,r,eta)
        assert full.preparation==expected_full_preparation(n)
        value,full_counts=apply_full(field,full,vectors[-1])
        assert value==apply_tail(field,plan,vectors[-1])[0]
        assert full_counts['field_operations']==expected_full_online(n)
        comparator=dict(preparation=full.preparation,
                        online=full_counts['field_operations'],fft_length=2*n,
                        target='same C^(N-r)p(C), default H_q tail coefficients',
                        extra_assumption='supplied primitive 2N-th root eta with eta^2=q')
    return dict(field=name,n=n,r=r,basis_vectors=n,mixed_vectors=2,
                aggregate_identity_checks=aggregate_checks,
                full_similarity_comparator=comparator,
                fft_length=2*r,preparation=plan.preparation,
                online=counts['field_operations'],
                horner_online=horner_counts['field_operations'],
                forward_ffts=counts['forward_ffts'],inverse_ffts=counts['inverse_ffts'],
                total_tail_field_ops=sum(plan.preparation.values())+sum(counts['field_operations'].values()),
                status='PASS')


def main():
    rng=random.Random(20261009)
    records=[]
    for prime in (65537,998244353):
        f=PrimeField(prime)
        for n in (2,4,8,16,32,64):
            r=1
            while 2*r<=n:
                records.append(audit_case(f,n,r,f'F_{prime}',rng))
                r*=2
    for n in (2,4,8):
        r=1
        while 2*r<=n:
            records.append(audit_case(CyclotomicField(n),n,r,f'Q(zeta_{n})',rng))
            r*=2
    result=dict(status='PASS',configurations=len(records),
                basis_vectors=sum(r['basis_vectors'] for r in records),
                mixed_vectors=sum(r['mixed_vectors'] for r in records),
                aggregate_identity_checks=sum(r['aggregate_identity_checks'] for r in records),
                full_similarity_checks=sum(r['full_similarity_comparator'] is not None for r in records),
                scope='Exact rank-at-most-r high-degree tails, O(N log(r+1)) prep+online; not full H_q(C)',
                records=records)
    out=Path(__file__).parent/'results';out.mkdir(exist_ok=True)
    (out/'tail_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
    for row in records:
        if row['field']=='F_65537' and row['n']==64:
            print(json.dumps({k:row[k] for k in ('n','r','fft_length','preparation','online','horner_online')}))


if __name__=='__main__':main()
