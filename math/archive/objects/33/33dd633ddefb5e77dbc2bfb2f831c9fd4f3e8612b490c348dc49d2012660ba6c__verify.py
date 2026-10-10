"""Independent checks; asymptotic table sizes are NOT instantiated at huge N."""
from __future__ import annotations
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from random import Random

import mpmath as mp

from norm_tabulation import (
    BlockKernel,EagerBlockTable,FloatAlphabet,ReferenceFFT,dyadic_coefficient,
    pack,unpack,parameters,pow2,pi_interval,
)

mp.mp.dps=70
ROOT=Path(__file__).resolve().parent
RNG=Random(901027)


def mp_fraction(x:Fraction):
    return mp.mpf(x.numerator)/x.denominator


def independent_quantize(value:Fraction,a:FloatAlphabet):
    """Separate slow Fraction quantizer: no bit-length exponent arithmetic."""
    if not value or abs(value)<pow2(a.emin): return 0
    sign=value<0
    v=abs(value)
    e=a.emin
    while e<a.emax and v>=pow2(e+1): e+=1
    step=pow2(e-a.p)
    m=min((1 << (a.p+1))-1,int(v//step))
    if m < (1 << a.p): raise AssertionError('Independent quantizer invalid mantissa')
    return (int(sign) << (a.p+a.exponent_bits)) | ((e-a.emin+1) << a.p) | (m-(1 << a.p))


def quantizer_checks():
    tested=under=over=0
    for p in [0,1,3,8]:
        a=FloatAlphabet(p,-5,5)
        for _ in range(1500):
            num=RNG.randrange(-10000,10001)
            exp=RNG.randrange(-20,10)
            value=num*pow2(exp)
            code,ov=a.quantize(num,exp)
            assert code==independent_quantize(value,a)
            recovered=a.decode(code)*pow2(a.lattice_exp)
            if ov:
                over+=1
            else:
                assert abs(recovered-value)<=a.u*abs(value)+a.tau
                under+=int(value!=0 and code==0)
            tested+=1
    return dict(cases=tested,underflow_cases=under,explicit_saturation_cases=over)


def packed_checks():
    n=0
    for width in range(1,17):
        for count in range(1,10):
            for _ in range(15):
                codes=[RNG.randrange(1 << width) for _ in range(count)]
                assert unpack(pack(codes,width),count,width)==codes
                n+=1
    return dict(cases=n)


def coefficient_checks():
    cases=0
    max_ratio=mp.mpf(0)
    for bits in [8,16,32]:
        lo,hi=pi_interval(bits)
        assert mp_fraction(lo)<mp.pi<mp_fraction(hi)
        assert hi-lo < pow2(-bits)
        for order in [2,3,4,5,8,16,31,64]:
            for j in sorted(set([0,1,order//3,order//2,order-1])):
                for scale in [1,4]:
                    ar,ai,b,bound=dyadic_coefficient(j,order,scale,bits)
                    exact=mp.exp(-2j*mp.pi*j/order)/mp.sqrt(scale)
                    approx=mp.mpc(ar,ai)/mp.mpf(2)**b
                    err=abs(approx-exact)
                    assert err <= mp_fraction(bound)*(1+mp.mpf('1e-40'))
                    max_ratio=max(max_ratio,err/mp_fraction(bound))
                    cases+=1
    return dict(cases=cases,max_measured_to_certified_error=float(max_ratio),
                note='Coefficient bounds are exact rational; transcendental comparisons use 70-digit mpmath.')


def eager_checks():
    report=[]
    # Every padded key is checked, including invalid float codes mapped to zero.
    configs=[(FloatAlphabet(0,-1,0),2),(FloatAlphabet(0,0,0),4)]
    for a,m in configs:
        kernel=BlockKernel(a,m)
        table=EagerBlockTable(kernel,max_entries=1 << 17)
        checked_entries=0
        checked_coords=0
        for key,packed_output in enumerate(table.outputs):
            codes=unpack(key,m,a.complex_bits)
            values=[a.complex_fraction(c) for c in codes]
            expected=[]
            for k in range(m):
                re=im=Fraction(0)
                for j,(vr,vi) in enumerate(values):
                    ar,ai,b,_=kernel.coef[(j*k)%m]
                    cr=Fraction(ar,1 << b);ci=Fraction(ai,1 << b)
                    re+=vr*cr-vi*ci
                    im+=vr*ci+vi*cr
                rr=independent_quantize(re,a)
                ii=independent_quantize(im,a)
                expected.append(a.combine(rr,ii))
            assert unpack(packed_output,m,a.complex_bits)==expected
            checked_entries+=1;checked_coords+=m
        report.append(dict(radix=m,complex_bits=a.complex_bits,
                           complete_entries=checked_entries,complex_outputs_checked=checked_coords,
                           note='Toy precision verifies complete table and packing, not useful FFT accuracy.'))
    return report


@__import__('functools').lru_cache(None)
def direct_roots(N):
    return [mp.exp(-2j*mp.pi*k/N) for k in range(N)]


def direct_dft(x):
    N=len(x);roots=direct_roots(N);scale=mp.sqrt(N)
    values=[mp.mpc(a,b) for a,b in x]
    return [sum((values[j]*roots[(j*k)%N] for j in range(N)),mp.mpc(0))/scale for k in range(N)]


def accuracy_checks():
    records=[]
    for N in [2,4,8,16,32,64]:
        patterns={
            'all_zero':[(0,0)]*N,
            'constant':[(1,0)]*N,
            'impulse':[(int(j==N//3),0) for j in range(N)],
            'alternating':[((-1)**j,0) for j in range(N)],
            'dense_integer':[(RNG.randrange(-100,101),RNG.randrange(-100,101)) for _ in range(N)],
            'dynamic_range':[(1 << min(2*j,30),(-1)**j) for j in range(N)],
        }
        reference={name:direct_dft(x) for name,x in patterns.items()}
        for eps in [Fraction(1,16),Fraction(1,1000000)]:
            for radix in [2,4,8]:
                plan=ReferenceFFT(N,eps,radix)
                for name,x in patterns.items():
                    ans,stats=plan.run_integer(x)
                    error2=sum(abs(mp.mpc(mp_fraction(a),mp_fraction(b))-r)**2
                               for (a,b),r in zip(ans,reference[name]))
                    norm2=sum(a*a+b*b for a,b in x)
                    relative=mp.sqrt(error2/norm2) if norm2 else mp.mpf(0)
                    if not norm2:assert all(a==b==0 for a,b in ans)
                    assert relative <= mp_fraction(eps)
                    assert stats['overflows']==0
                    records.append(dict(N=N,epsilon=str(eps),forced_radix=radix,
                        input=name,relative_l2_error=float(relative),
                        error_over_epsilon=float(relative/mp_fraction(eps)),stats=stats))
    return dict(cases=len(records),complex_outputs=sum(r['N'] for r in records),
                max_error_over_epsilon=max(r['error_over_epsilon'] for r in records),
                note='Forced-radix lazy simulator: not an asymptotic speed measurement.',records=records)


def symbolic_budget_checks():
    records=[]
    for eps in [Fraction(1,16),Fraction(1,2**40)]:
        for n in [4,16,64,256,1024,4096,65536,1048576]:
            spec=parameters(n,eps)
            p=spec['p'];u=pow2(-p)
            tau_factor=pow2(spec['emin']+n) # N*tau; avoids building N=2^million.
            assert u<=eps/Fraction(1024*(n+1))
            assert tau_factor<=eps/Fraction(1024*(n+1))
            if not spec['ordinary_fallback']:
                assert spec['padded_table_key_bits'] <= spec['table_budget_bits']
                assert spec['radix']&(spec['radix']-1)==0
            # Conservative relative-error upper bound, using sqrt(2N)<=2N:
            # <=6 L u +4 L sqrt(2N)*tau <=6 L u+8 L N tau.
            L=2*n+1
            bound=6*L*u+8*L*tau_factor
            assert 3*L*u<=Fraction(1,2)
            assert bound < eps
            spec['conservative_error_budget_over_epsilon']=str(bound/eps)
            records.append(spec)
    return dict(cases=len(records),records=records,
                note='N is 2^log2_N. Large rows are symbolic schedules, not executed transforms.')


def zero_precision_boundary():
    records=[]
    for n in [256,1024,4096,65536]:
        # Polynomially shrinking epsilon forces p=Theta(log N) and bounded radix.
        eps=Fraction(1,1 << (n//8))
        spec=parameters(n,eps)
        assert spec['radix'] <= 1  # gamma=1/4 and complex coefficient size ~n/4.
        records.append({k:spec[k] for k in ['log2_N','p','complex_bits','radix','ordinary_fallback']})
    return dict(cases=len(records),records=records)


def run():
    report=dict(status='Approximate finite-word theorem; no exact universal faster FFT claimed.',
                groups={})
    functions=[('quantizer',quantizer_checks),('packing',packed_checks),
               ('coefficient_certificates',coefficient_checks),('complete_eager_tables',eager_checks),
               ('full_output_accuracy',accuracy_checks),('symbolic_cost_and_error',symbolic_budget_checks),
               ('polynomial_accuracy_boundary',zero_precision_boundary)]
    for name,fn in functions:
        print('RUN',name,flush=True)
        report['groups'][name]=fn()
        print('PASS',name,flush=True)
    report['passed_groups']=len(functions)
    (ROOT/'RESULTS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print('SHA256',hashlib.sha256((ROOT/'RESULTS.json').read_bytes()).hexdigest())

if __name__=='__main__':run()
