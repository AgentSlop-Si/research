"""Exact audit of pruned orbit fusion and short Fourier-description weights."""
import json
import random
from pathlib import Path
from rank_one_orbit import (prepare_orbit,apply_orbit,expected_preparation,expected_online,
    prepare_modes,apply_modes,expected_modes_preparation,expected_modes_online,
    partial_forward,partial_transpose,Counted)
from fused_modulated import prepare_fused,apply_fused
from operators import prepare_sparse,horner_c
from prior_exact_arithmetic import PrimeField,CyclotomicField


def direct(field,plan,x,coefficients):
    n=plan.n
    bx=[field.mul(a,b) for a,b in zip(plan.right,x)]
    moments=[]
    for j in range(len(coefficients)):
        value=field.zero
        for k,a in enumerate(bx):
            value=field.add(value,field.mul(plan.roots[(j*k)%n],a))
        moments.append(field.mul(coefficients[j],value))
    result=[]
    for i,a in enumerate(plan.left):
        value=field.zero
        for j,b in enumerate(moments):
            value=field.add(value,field.mul(plan.roots[(i*j)%n],b))
        result.append(field.mul(a,value))
    return result


def audit(field,n,s,name,rng):
    q=field.root(n)
    assert field.power(q,n)==field.one and field.power(q,n//2)!=field.one
    coefficients=[field.integer(j+1) for j in range(s)]
    plan=prepare_orbit(field,n,q,coefficients)
    sparse=prepare_sparse(field,n,q)
    assert plan.preparation==expected_preparation(n)
    vectors=[[field.one if i==j else field.zero for i in range(n)] for j in range(n)]
    vectors.append([field.integer(rng.randrange(-4,5)) for _ in range(n)])
    highest=[field.zero]*(n-1)+[field.one]
    for x in vectors:
        y,count=apply_orbit(field,plan,x)
        assert y==direct(field,plan,x,coefficients),(name,n,s)
        assert count['field_operations']==expected_online(n,s),(n,s,count,expected_online(n,s))
        actual,_=horner_c(field,sparse,highest,x)
        scalar=field.zero
        for a,b in zip(plan.right,x):
            scalar=field.add(scalar,field.mul(a,b))
        assert actual==[field.mul(a,scalar) for a in plan.left]
    # Explicitly check both pruned graph orientations on a mixed vector.
    x=vectors[-1]
    frequencies=[]
    for j in range(plan.rounded):
        a=field.zero
        for k,v in enumerate(x):
            a=field.add(a,field.mul(plan.roots[j*k%n],v))
        frequencies.append(a)
    assert partial_forward(Counted(field),plan,x)==frequencies
    expected=[]
    for k in range(n):
        a=field.zero
        for j,v in enumerate(frequencies):
            a=field.add(a,field.mul(plan.roots[j*k%n],v))
        expected.append(a)
    assert partial_transpose(Counted(field),plan,frequencies)==expected
    generic=None
    if plan.rounded<=n//2:
        generic_plan=prepare_fused(field,n,1,q,[[a] for a in coefficients])
        value,stats=apply_fused(field,generic_plan,x)
        assert value==apply_orbit(field,plan,x)[0]
        generic=dict(preparation=generic_plan.preparation,online=stats['field_operations'])
    return dict(field=name,n=n,s=s,rounded=plan.rounded,basis_vectors=n,mixed_vectors=1,
                preparation=plan.preparation,online=count['field_operations'],
                generic_fusion_comparator=generic,status='PASS')


def audit_modes(field,n,name,rng):
    q=field.root(n)
    descriptions=[[(0,field.one)],[(1,field.integer(2))],
                  [(0,field.one),(1,field.integer(3))],
                  [(0,field.one),(1,field.integer(3)),(2,field.integer(9))]]
    records=[]
    sparse=prepare_sparse(field,n,q)
    for modes in descriptions:
        plan=prepare_modes(field,n,q,modes)
        assert plan.preparation==expected_modes_preparation(n,len(modes))
        coefficients=[]
        for j in range(n):
            a=field.zero
            for mode,gamma in modes:
                a=field.add(a,field.mul(gamma,plan.base.roots[mode*j%n]))
            coefficients.append(a)
        # These chosen examples have full rank: all Fourier diagonal entries
        # are nonzero. This checks a stated property of these examples only.
        assert all(a!=field.zero for a in coefficients)
        vectors=[[field.one if i==j else field.zero for i in range(n)] for j in range(n)]
        vectors.append([field.integer(rng.randrange(-4,5)) for _ in range(n)])
        for x in vectors:
            y,count=apply_modes(field,plan,x)
            assert y==direct(field,plan.base,x,coefficients)
            assert count['field_operations']==expected_modes_online(n,len(modes))
        records.append(dict(field=name,n=n,modes=len(modes),basis_vectors=n,mixed_vectors=1,
                            rank=n,preparation=plan.preparation,online=count['field_operations'],
                            transform_calls=count['transform_calls'],status='PASS'))
    # Last-column closure obstruction for the complete H_q(C).
    last=[field.zero]*(n-1)+[field.one]
    hlast,_=horner_c(field,sparse,plan.base.left,last)
    a=plan.base.left
    # Normalized last column is a nonzero geometric sequence q^-i.
    normalized=[field.mul(value,field.inv(left)) for value,left in zip(hlast,a)]
    assert normalized[0]!=field.zero
    assert normalized==[field.mul(normalized[0],plan.base.roots[(-i)%n]) for i in range(n)]
    if n>=4:
        previous=[field.zero]*n;previous[n-2]=field.one
        hprevious,_=horner_c(field,sparse,plan.base.left,previous)
        # The entries used in this certificate are off both altered diagonals,
        # so the same mismatch excludes H-alpha*I for every scalar alpha.
        actual=[];predicted=[]
        for i in (1,n-1):
            actual.append(field.mul(hprevious[i],field.inv(
                field.mul(plan.base.left[i],plan.base.right[n-2]))))
            predicted.append(field.mul(hlast[i-1],field.inv(
                field.mul(plan.base.left[i-1],plan.base.right[n-1]))))
        assert actual!=predicted
    return records


def main():
    rng=random.Random(20261009)
    orbit=[];modes=[]
    for prime in (65537,998244353):
        field=PrimeField(prime)
        for n in (2,4,8,16,32,64):
            for s in sorted({1,2,min(3,n),n//2,n}):
                orbit.append(audit(field,n,s,f'F_{prime}',rng))
            modes.extend(audit_modes(field,n,f'F_{prime}',rng))
    for n in (2,4,8):
        field=CyclotomicField(n)
        for s in sorted({1,2,min(3,n),n//2,n}):
            orbit.append(audit(field,n,s,f'Q(zeta_{n})',rng))
        modes.extend(audit_modes(field,n,f'Q(zeta_{n})',rng))
    result=dict(status='PASS',orbit_configurations=len(orbit),mode_configurations=len(modes),
                orbit_basis_vectors=sum(a['basis_vectors'] for a in orbit),
                orbit_mixed_vectors=len(orbit),mode_basis_vectors=sum(a['basis_vectors'] for a in modes),
                mode_mixed_vectors=len(modes),full_rank_mode_examples=len(modes),
                scope='exact noncommuting orbit families; full rank permitted; not H_q(C)',
                orbit_cases=orbit,mode_cases=modes)
    out=Path(__file__).parent/'results';out.mkdir(exist_ok=True)
    (out/'orbit_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('orbit_cases','mode_cases')},indent=2))
    for a in orbit:
        if a['field']=='F_65537' and a['n']==64:
            print(json.dumps({k:a[k] for k in ('n','s','preparation','online')}))
    for a in modes:
        if a['field']=='F_65537' and a['n']==64:
            print(json.dumps({k:a[k] for k in ('n','modes','rank','preparation','online')}))


if __name__=='__main__':main()
