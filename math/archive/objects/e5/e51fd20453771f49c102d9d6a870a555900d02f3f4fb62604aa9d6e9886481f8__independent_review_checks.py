"""Focused review controls for signed digit updates and conditional recovery."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
from structured_integer import try_structured_product,try_structured_convolution
from error_budget import convolution_rounding_bound,unique_integer_from_interval


def value(digits,base):
    result=0
    for digit in reversed(digits):result=result*base+digit
    return result


def main():
    dense=[(37*j+21)%256 for j in range(64)];dense[-1]=255
    near=[173]*64;near[0]=0;near[31]=12;near[-1]=255
    sparse=[0]*64;sparse[0]=255;sparse[31]=1;sparse[-1]=200
    rows=[]
    cases=[([255]*64,dense,256,1,'baseline-exceptions'),
           (near,dense,256,4,'baseline-exceptions'),
           (dense,near,256,4,'baseline-exceptions'),
           ([255]*17+[1]*31,dense,256,2,'constant-runs'),
           (sparse,dense,256,3,'sparse-digits'),
           ([1]*37,[j%2 for j in range(41)],2,1,'baseline-exceptions'),
           ([3,3,0,0],[2,1,0],4,4,None),
           ([0]*17,dense,256,0,None)]
    for a,b,base,cap,method in cases:
        out,info=try_structured_product(a,b,base,max_terms=cap)
        assert out is not None and value(out,base)==value(a,base)*value(b,base)
        assert len(out)==1 or out[-1]!=0
        if method:assert info['method']==method
        conv,cinfo=try_structured_convolution(a,b,base,max_terms=cap)
        assert conv is not None and len(conv)==len(a)+len(b)-1
        oracle=[0]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b):oracle[i+j]+=x*y
        assert conv==oracle
        rows.append({'n':len(a),'m':len(b),'base':base,'method':info.get('method','zero')})
    # Former bug: validation exhausted iterators, causing zero norms and a
    # falsely safe zero certificate. Bound must equal that of the same lists.
    args=([255,255],[255,255],1,1)
    expected=convolution_rounding_bound(*args)
    actual=convolution_rounding_bound(iter(args[0]),iter(args[1]),1,1)
    assert actual==expected and actual['total_coefficient_error_bound']==628320
    assert not actual['conditionally_safe_nearest_integer_rounding']
    for a,b in ((iter([]),iter([1])),(iter([1]),iter([]))):
        try:convolution_rounding_bound(a,b,0,0)
        except ValueError:pass
        else:raise AssertionError('empty iterator accepted')
    equal=convolution_rounding_bound([1],[1],Fraction(1,2),0)
    below=convolution_rounding_bound([1],[1],Fraction(499,1000),0)
    inverse=convolution_rounding_bound([1],[1],0,0,Fraction(1,2))
    assert not equal['conditionally_safe_nearest_integer_rounding']
    assert below['conditionally_safe_nearest_integer_rounding']
    assert not inverse['conditionally_safe_nearest_integer_rounding']
    assert unique_integer_from_interval(-1,-1)==-1
    assert unique_integer_from_interval(Fraction(-101,100),Fraction(-99,100))==-1
    root=Path(__file__).resolve().parent
    result={'status':'PASS','exact_products':len(rows),'exact_convolutions':len(rows),
            'cases':rows,'generator_equivalence':True,'empty_generators_rejected':2,
            'rounding_threshold_controls':3,'negative_interval_controls':2,
            'source_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest()
                             for name in ('structured_integer.py','error_budget.py')}}
    (root/'independent_review_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
