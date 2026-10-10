"""Exact fast H(C), backward-spectrum, and shifted-resolvent audit."""
import sys
import json
import random
from pathlib import Path
from fast_hc import prepare_fast,apply_hc,expected_preparation,expected_online,fused_fourier
from resolvent import (prepare_resolvent,solve,
    expected_preparation as expected_resolvent_preparation,expected_solve)
from operators import prepare_sparse,apply_sparse_c,horner_c
from fixed_kernel import prepare,lower_convolution
from prior_exact_arithmetic import PrimeField,CyclotomicField
from covariance import prepare_covariance,apply_s,apply_k,chain


def horner(field,coefficients,z):
    value=field.zero
    for c in reversed(coefficients):
        value=field.add(field.mul(value,z),c)
    return value


def audit_case(field,n,name,rng):
    eta=field.root(2*n)
    assert field.power(eta,n)==field.neg(field.one)
    assert field.power(eta,2*n)==field.one
    q=field.mul(eta,eta)
    fast=prepare_fast(field,n,eta)
    coefficients=prepare(field,n,q)
    sparse=prepare_sparse(field,n,q)
    resolvent=prepare_resolvent(field,n,q)
    covariance=prepare_covariance(field,fast)
    assert covariance.preparation==dict(sub=n-1)
    assert fast.preparation==expected_preparation(n)
    assert resolvent.preparation==expected_resolvent_preparation(n)
    assert fast.t==coefficients.kernel
    assert [horner(field,coefficients.middle,z) for z in fast.kernel.fft.powers]==fast.kernel.spectrum
    # Exact polynomial, including its finite top boundary.
    for z in (field.one,eta,field.integer(2)):
        kz=horner(field,coefficients.middle,z)
        rhs=field.add(field.mul(field.sub(field.one,z),
                     horner(field,coefficients.middle,field.mul(q,z))),
                     field.mul(field.power(z,n),fast.kernel.fft.inverse_n))
        assert kz==rhs
    assert fast.kernel.spectrum[0]==fast.kernel.fft.inverse_n!=field.zero
    vectors=[[field.one if i==j else field.zero for i in range(n)] for j in range(n)]
    vectors.append([field.integer(rng.randrange(-20,21)) for _ in range(n)])
    resolvent_cases=0
    for x in vectors:
        actual,counts=apply_hc(field,fast,x)
        expected,_=horner_c(field,sparse,coefficients.kernel,x)
        assert actual==expected
        assert counts['field_operations']==expected_online(n)
        sx,scount=apply_s(field,covariance,x)
        ky,kcount=apply_k(field,covariance,actual)
        assert scount==dict(mul=n,add=n-1)
        assert kcount==dict(mul=n)
        assert apply_hc(field,fast,sx)[0]==ky
        cx=apply_sparse_c(field,sparse,x)
        difference=[field.sub(a,b) for a,b in zip(x,cx)]
        assert apply_s(field,covariance,difference)[0]==apply_k(field,covariance,x)[0]
        # The compiler cancellation returns the ordinary N-point FFT.
        gamma_x=[field.mul(field.power(q,j*(j-1)//2),v) for j,v in enumerate(x)]
        gamma_x=[field.neg(v) if j%2 else v for j,v in enumerate(gamma_x)]
        tx=lower_convolution(field,coefficients.kernel,gamma_x)
        hc_tx,_=apply_hc(field,fast,tx)
        unfused=[field.mul(v,f) for v,f in zip(hc_tx,coefficients.factorial)]
        fused,fused_counts=fused_fourier(field,fast,x)
        assert fused==unfused
        l=n.bit_length()-1
        assert fused_counts==dict(mul=n*l//2,add=n*l//2,sub=n*l//2)
        # Includes lambda exactly equal to a diagonal entry; no singular cut.
        for lam in (field.one,q,field.integer(2)):
            y,details=solve(field,resolvent,lam,x)
            assert details['field_operations']==expected_solve(n)
            cy=apply_sparse_c(field,sparse,y)
            assert [field.sub(field.mul(lam,a),b) for a,b in zip(y,cy)]==x
            resolvent_cases+=1
    # The N-resolvent identity is verified on a mixed vector for small sizes.
    batch_cases=0
    if n<=16:
        x=vectors[-1]
        combined=[field.zero]*n
        for j in range(n):
            lam=field.power(q,j)
            weight=field.mul(field.mul(lam,fast.kernel.fft.inverse_n),
                             horner(field,coefficients.kernel,lam))
            value,_=solve(field,resolvent,lam,x)
            combined=[field.add(a,field.mul(weight,b)) for a,b in zip(combined,value)]
        assert combined==apply_hc(field,fast,x)[0]
        batch_cases=1
    # Reversible orbit and a completely charged related-input family.
    sx=kx=vectors[-1]
    for _ in range(n):
        sx=apply_s(field,covariance,sx)[0]
        kx=apply_k(field,covariance,kx)[0]
    assert sx==kx==vectors[-1]
    steps=4
    cached=chain(field,covariance,vectors[-1],steps,True)
    baseline=chain(field,covariance,vectors[-1],steps,False)
    assert cached['outputs']==baseline['outputs']
    online=expected_online(n)
    assert cached['field_operations']==dict(mul=online['mul']+2*n*steps,
        add=online['add']+(n-1)*steps,sub=online['sub'])
    assert baseline['field_operations']==dict(mul=(steps+1)*online['mul']+n*steps,
        add=(steps+1)*online['add']+(n-1)*steps,sub=(steps+1)*online['sub'])
    return dict(field=name,n=n,basis_vectors=n,mixed_vectors=1,
                inverse_spectrum_values=2*n,resolvent_cases=resolvent_cases,
                resolvent_batch_identity_cases=batch_cases,
                preparation=fast.preparation,fast_online=expected_online(n),
                horner_online=dict(mul=3*n*n-2*n,add=2*n*n-2*n),
                resolvent_preparation=resolvent.preparation,
                resolvent_query=expected_solve(n),
                covariance_basis_vectors=n,covariance_mixed_vectors=1,
                covariance_chain_outputs=steps+1,
                cached_chain_total=sum(fast.preparation.values())+sum(covariance.preparation.values())+sum(cached['field_operations'].values()),
                baseline_chain_total=sum(fast.preparation.values())+sum(baseline['field_operations'].values()),
                status='PASS')


def main():
    rng=random.Random(20261009)
    cases=[]
    for p in (65537,998244353):
        field=PrimeField(p)
        for n in (2,4,8,16,32,64):
            cases.append(audit_case(field,n,f'F_{p}',rng))
    for n in (2,4,8):
        cases.append(audit_case(CyclotomicField(2*n),n,f'Q(zeta_{2*n})',rng))
    result=dict(status='PASS',configurations=len(cases),
        basis_vectors=sum(c['basis_vectors'] for c in cases),
        mixed_vectors=sum(c['mixed_vectors'] for c in cases),
        inverse_spectrum_values=sum(c['inverse_spectrum_values'] for c in cases),
        shifted_resolvent_vectors=sum(c['resolvent_cases'] for c in cases),
        resolvent_batch_identity_cases=sum(c['resolvent_batch_identity_cases'] for c in cases),
        covariance_vectors=sum(c['covariance_basis_vectors']+c['covariance_mixed_vectors'] for c in cases),
        covariance_chain_outputs=sum(c['covariance_chain_outputs'] for c in cases),
        scope='O(N log N) ordinary-FFT comparator for H(C), not an independent faster Fourier algorithm',
        cases=cases)
    out=Path(__file__).parent/'results'
    out.mkdir(exist_ok=True)
    (out/'fast_hc_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
    for c in cases[:6]:
        print(f"N={c['n']}: fast online={sum(c['fast_online'].values())}, Horner online={sum(c['horner_online'].values())}, fast prep={sum(c['preparation'].values())}")


if __name__=='__main__':
    main()
