"""Exact fused noncommuting-tail aggregate verification."""
import json
import random
from pathlib import Path
from fused_modulated import (prepare_fused,apply_fused,expected_preparation,expected_online,
    prepare_independent,apply_independent,expected_independent_preparation,expected_independent_online)
from operators import prepare_sparse,horner_c
from fixed_kernel import lower_convolution
from prior_exact_arithmetic import PrimeField,CyclotomicField


def literal(field,plan,sparse,x):
    out=[field.zero]*plan.n
    current=list(x)
    diagonal=[field.one]*plan.n
    for p in plan.polynomials:
        tail,_=horner_c(field,sparse,[field.zero]*(plan.n-plan.r)+p,current)
        out=[field.add(a,field.mul(b,d)) for a,b,d in zip(out,tail,diagonal)]
        current=[field.mul(a,b) for a,b in zip(plan.roots,current)]
        diagonal=[field.mul(a,b) for a,b in zip(plan.roots,diagonal)]
    return out


def audit(field,n,r,s,name,rng):
    q=field.root(n)
    assert field.power(q,n)==field.one and field.power(q,n//2)!=field.one
    polynomials=[[field.integer((j+2)*(k+1)-k*k) for k in range(r)] for j in range(s)]
    plan=prepare_fused(field,n,r,q,polynomials)
    baseline=prepare_independent(field,n,r,q,polynomials)
    sparse=prepare_sparse(field,n,q)
    assert plan.preparation==expected_preparation(n,r,s),(plan.preparation,expected_preparation(n,r,s))
    assert baseline['preparation']==expected_independent_preparation(n,r,s)
    vectors=[[field.one if i==j else field.zero for i in range(n)] for j in range(n)]
    vectors.append([field.integer(rng.randrange(-4,5)) for _ in range(n)])
    for x in vectors:
        got,count=apply_fused(field,plan,x)
        expected=literal(field,plan,sparse,x)
        separately,separate_count=apply_independent(field,baseline,x)
        assert got==expected==separately,(name,n,r,s)
        assert count['field_operations']==expected_online(n,r,s),(n,r,s,count,expected_online(n,r,s))
        assert separate_count['field_operations']==expected_independent_online(n,r,s)
        # Independent conjugacy: T D = Q T, tested without the aggregate.
        dx=[field.mul(plan.roots[0],x[0])]
        dx.extend(field.sub(field.mul(plan.roots[i],x[i]),field.mul(plan.roots[i-1],x[i-1]))
                  for i in range(1,n))
        lhs=lower_convolution(field,plan.projection.kernel.kernel,dx)
        tx=lower_convolution(field,plan.projection.kernel.kernel,x)
        assert lhs==[field.mul(a,b) for a,b in zip(plan.roots,tx)]
    return dict(field=name,n=n,r=r,steps=s,window=plan.window,
                basis_vectors=n,mixed_vectors=1,preparation=plan.preparation,
                online=count['field_operations'],independent_preparation=baseline['preparation'],
                independent_online=separate_count['field_operations'],
                fused_cold=sum(plan.preparation.values())+sum(count['field_operations'].values()),
                independent_cold=sum(baseline['preparation'].values())+sum(separate_count['field_operations'].values()),
                full_output_terms_materialized=count['full_output_terms_materialized'],status='PASS')


def main():
    rng=random.Random(20261009)
    cases=[]
    pairs=((1,1),(1,2),(1,3),(2,2),(2,3),(4,2),(2,4),(4,4),(8,4))
    for prime in (65537,998244353):
        field=PrimeField(prime)
        for n in (2,4,8,16,32,64):
            for r,s in pairs:
                if 1<<(r+s-2).bit_length()<=n//2:
                    cases.append(audit(field,n,r,s,f'F_{prime}',rng))
    for n in (2,4,8):
        field=CyclotomicField(n)
        for r,s in pairs:
            if 1<<(r+s-2).bit_length()<=n//2:
                cases.append(audit(field,n,r,s,f'Q(zeta_{n})',rng))
    result=dict(status='PASS',configurations=len(cases),
                basis_vectors=sum(a['basis_vectors'] for a in cases),
                mixed_vectors=len(cases),
                scope='exact noncommuting modulated-tail aggregates; not full H_q(C)',cases=cases)
    directory=Path(__file__).parent/'results';directory.mkdir(exist_ok=True)
    (directory/'fusion_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
    for case in cases:
        if case['field']=='F_65537' and case['n']==64:
            print(json.dumps({k:case[k] for k in ('n','r','steps','window','fused_cold','independent_cold','online','independent_online')}))


if __name__=='__main__':main()
