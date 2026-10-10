"""Exact implementation audit; no floating-point ranks or timings."""
import json
from pathlib import Path
from collections import Counter
from orbit_kernel import (Counted, prepare_orbit, prepare_radix, apply,
    coefficient_kernel, expected_preparation, expected_online)
from prior_exact_arithmetic import PrimeField, CyclotomicField


def horner(f, coefficients, z):
    y = f.zero
    for c in reversed(coefficients):
        y = f.add(f.mul(y,z), c)
    return y


def audit_case(f, n, name):
    eta = f.root(2*n)
    assert f.power(eta, 2*n) == f.one
    assert f.power(eta, n) == f.neg(f.one)
    plan = prepare_orbit(f,n,eta)
    baseline = prepare_radix(f,n,eta)
    t = coefficient_kernel(f,plan.fft)
    assert t[0] == f.one
    assert plan.preparation == expected_preparation(n,'orbit')
    assert baseline.preparation == expected_preparation(n,'radix')
    direct = [horner(f,t,z) for z in plan.fft.powers]
    assert plan.spectrum == baseline.spectrum == direct
    odd_product = f.one
    for k, z in enumerate(plan.fft.powers):
        forcing = plan.fft.inverse_n
        if k % 2:
            forcing = f.neg(forcing)
            odd_product = f.mul(odd_product, f.sub(f.one,z))
        rhs = f.add(f.mul(f.sub(f.one,z), direct[k]), forcing)
        assert direct[(k+2) % (2*n)] == rhs
    assert odd_product == f.integer(2)
    # Without the boundary, k=0 forces H(q)=0. Actual H(q)=1/N != 0.
    assert direct[2] == plan.fft.inverse_n != f.zero
    q = f.mul(eta,eta)
    for z in [f.integer(2), f.integer(3), eta]:
        lhs = horner(f,t,f.mul(q,z))
        rhs = f.add(f.mul(f.sub(f.one,z),horner(f,t,z)),
                    f.mul(f.power(z,n),plan.fft.inverse_n))
        assert lhs == rhs
    online = None
    for j in range(n):
        x = [f.zero]*n
        x[j] = f.one
        y, online = apply(f,plan,x)
        expected = [t[i-j] if i>=j else f.zero for i in range(n)]
        assert y == expected
        assert online['field_operations'] == expected_online(n)
    # Mixed input verifies that basis checks were not accidentally special-cased.
    x = [f.integer((j*j+3*j+7) % 17-8) for j in range(n)]
    y, _ = apply(f,plan,x)
    expected = []
    for i in range(n):
        total = f.zero
        for j in range(i+1):
            total = f.add(total,f.mul(t[i-j],x[j]))
        expected.append(total)
    assert y == expected
    # Full q-Pascal factorization: ordinary FFT remains much cheaper.
    full_basis = 0
    if n <= 16:
        factorial = [f.one]
        for j in range(1,n):
            factorial.append(f.mul(factorial[-1],f.sub(f.one,f.power(q,j))))
        middle = [f.mul(f.power(q,j*(j-1)//2),t[j]) for j in range(n)]
        middle = [f.neg(v) if j%2 else v for j,v in enumerate(middle)]
        for j in range(n):
            x = [f.zero]*n
            x[j] = f.one
            c = Counted(f)
            v = [c.mul(a,b) for a,b in zip(factorial,x)]
            v, first = apply(f,plan,list(reversed(v)))
            v = list(reversed(v))
            v = [c.mul(a,b) for a,b in zip(middle,v)]
            v, second = apply(f,plan,v)
            v = [c.mul(a,b) for a,b in zip(factorial,v)]
            assert v == [f.power(q,i*j) for i in range(n)]
            counts = Counter(c.count)
            counts.update(first['field_operations'])
            counts.update(second['field_operations'])
            l = n.bit_length()-1
            assert dict(counts) == dict(mul=4*n*l+15*n,
                                       add=4*n*(l+1),sub=4*n*(l+1))
            full_basis += 1
    return dict(field=name,n=n,spectrum_points=2*n,
                kernel_basis_vectors=n,full_fourier_basis_vectors=full_basis,
                orbit_preparation=plan.preparation,
                radix_preparation=baseline.preparation,
                online=online, boundary_negative_control='PASS',status='PASS')


def main():
    cases=[]
    for p in (65537,998244353):
        f=PrimeField(p)
        for l in range(1,8):
            cases.append(audit_case(f,2**l,f'F_{p}'))
    for n in (2,4,8):
        cases.append(audit_case(CyclotomicField(2*n),n,f'Q(zeta_{2*n})'))
    sizes=(16,64,256,1024,4096)
    cost_rows=[]
    for n in sizes:
        a,b=expected_preparation(n,'orbit'),expected_preparation(n,'radix')
        cost_rows.append(dict(n=n,orbit_field_ops=sum(a.values()),
            radix_field_ops=sum(b.values()),online_field_ops=sum(expected_online(n).values())))
    summary=dict(status='PASS',cases=len(cases),
        spectrum_points=sum(c['spectrum_points'] for c in cases),
        kernel_basis_vectors=sum(c['kernel_basis_vectors'] for c in cases),
        full_fourier_basis_vectors=sum(c['full_fourier_basis_vectors'] for c in cases),
        model='exact field arithmetic; primitive 2N-th root supplied; no bit or stability claim',
        cost_rows=cost_rows,details=cases)
    out=Path(__file__).parent/'results'
    out.mkdir(exist_ok=True)
    (out/'audit.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='details'},indent=2))


if __name__=='__main__':
    main()
