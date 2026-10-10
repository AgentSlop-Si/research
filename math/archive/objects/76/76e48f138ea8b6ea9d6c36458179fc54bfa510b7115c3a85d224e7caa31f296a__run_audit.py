import json
from fractions import Fraction
from pathlib import Path
import random
from structured_integer import try_structured_product,try_structured_convolution
from error_budget import convolution_rounding_bound,unique_integer_from_interval


def value(digits,base):
    out=0
    for digit in reversed(digits):out=out*base+digit
    return out


def check(a,b,base,max_terms,rows):
    original_a,original_b=list(a),list(b)
    result,stats=try_structured_product(a,b,base,max_terms=max_terms)
    assert a==original_a and b==original_b
    if result is not None:
        assert value(result,base)==value(a,base)*value(b,base)
        assert all(0<=d<base for d in result)
        assert len(result)==1 or result[-1]!=0
    convolution_checked=False
    if max(len(a),len(b))<=131:
        coefficients,conv_stats=try_structured_convolution(a,b,base,max_terms=max_terms)
        if coefficients is not None:
            expected=[0]*(len(a)+len(b)-1)
            for i,u in enumerate(a):
                for j,v in enumerate(b):expected[i+j]+=u*v
            assert coefficients==expected
            assert value(coefficients,base)==value(a,base)*value(b,base)
            convolution_checked=True
    rows.append({'n':len(a),'m':len(b),'base':base,
                 'accepted':bool(stats['accepted']),
                 'method':stats.get('method','zero'),
                 'structural_terms':stats.get('structural_terms',0),
                 'full_convolution_checked':convolution_checked,
                 'digit_kernel_steps':stats.get('digit_kernel_steps',0)})
    return result,stats


def main():
    rng=random.Random(909)
    rows=[]
    for base in [2,3,10,256,65536]:
        for n in [1,2,7,32,128]:
            b=[rng.randrange(base) for _ in range(n+3)]
            b[-1]=max(1,b[-1])
            repeated=[base-1]*n
            check(repeated,b,base,8,rows)
            near=[max(1,base//2)]*n
            if n>2:
                near[n//3]=0
                near[2*n//3]=base-1
            check(near,b,base,8,rows)
            runs=[1]*(n//3)+[0]*(n//3)+[base-1]*(n-2*(n//3))
            check(runs,b,base,8,rows)
            sparse=[0]*n
            sparse[0]=1;sparse[-1]=base-1
            check(sparse,b,base,8,rows)
            check([0]*n,b,base,0,rows)
            check(b,repeated,base,8,rows)
    # Unstructured operands decline instead of hiding a generic slow multiplication.
    hard=[j%17 for j in range(512)];hard[-1]=16
    result,decline=check(hard,list(reversed(hard)),256,4,rows)
    assert result is None and not decline['accepted']
    # Larger constructive cases measure digit kernels, not a native speedup.
    scaling=[]
    for n in [64,256,1024,4096]:
        a=[173]*n;a[n//3]=12;a[2*n//3]=255
        b=[rng.randrange(256) for _ in range(n)];b[-1]=255
        result,stats=check(a,b,256,3,rows)
        assert result is not None
        scaling.append({'n':n,'m':n,'structural_terms':stats['structural_terms'],
                        'method':stats['method'],'digit_kernel_steps':stats['digit_kernel_steps']})
    rounding=[]
    for n in [1,2,8,32,128]:
        a=[j%7+1 for j in range(n)];b=[j%5+1 for j in range(n+1)]
        probe=convolution_rounding_bound(a,b,0,0)
        la,lb=probe['norm_one_a'],probe['norm_one_b']
        qa,qb=probe['norm_two_upper_a'],probe['norm_two_upper_b']
        ea,eb,ei=Fraction(1,16*la*qb),Fraction(1,16*lb*qa),Fraction(1,16*qa*qb)
        bound=convolution_rounding_bound(a,b,ea,eb,ei)
        assert bound['conditionally_safe_nearest_integer_rounding']
        # Even Lambda>=1 already forces the residual sample bound >= support.
        for tail_size in range(1,n+1):
            mass=sum(abs(v) for v in a[-tail_size:])
            sample_lower=4*Fraction(mass,la)**2/(ea*ea)
            assert sample_lower>tail_size
        rounding.append({'n':n,'epsilon_forward_a':str(ea),
                         'epsilon_inverse':str(ei),
                         'total_coefficient_error_bound':str(bound['total_coefficient_error_bound'])})
    assert unique_integer_from_interval(Fraction(151,100),Fraction(249,100))==2
    assert unique_integer_from_interval(Fraction(-1,10),Fraction(1,10))==0
    for lo,hi in [(0,1),(Fraction(1,10),Fraction(9,10)),(2,1)]:
        try:unique_integer_from_interval(lo,hi)
        except ValueError:pass
        else:raise AssertionError('non-unique/invalid interval accepted')
    report={'status':'PASS','integer_product_cases':len(rows),
            'accepted_products':sum(r['accepted'] for r in rows),
            'declined_products':sum(not r['accepted'] for r in rows),
            'full_convolution_cases':sum(r['full_convolution_checked'] for r in rows),
            'rounding_budget_cases':len(rounding),'product_cases':rows,
            'scaling':scaling,'rounding':rounding,
            'scope':'Exact digit products and rational error algebra. Python whole integers are used only as test oracles; no FFT or approximation enters the fast path.'}
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('product_cases','rounding')},indent=2))


if __name__=='__main__':main()
