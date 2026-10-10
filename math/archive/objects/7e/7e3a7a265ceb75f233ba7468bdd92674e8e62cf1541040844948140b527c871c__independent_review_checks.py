"""Targeted multi-parent review: carry chains, mixed terms and highest degree."""
import hashlib
import json
from pathlib import Path
from multiparent import Ledger,make_seed_cache,polynomial_batch,secant_batch,signed_patch


def digits(value,n):return list(value.to_bytes(n,'little'))
def integer(values):return int.from_bytes(bytes(values),'little')
def exact(pairs,result):
    assert len(result['outputs'])==len(pairs)
    for (a,b),out in zip(pairs,result['outputs']):
        assert len(out)==2*len(a)
        assert integer(out)==integer(a)*integer(b)


def main():
    carry_cases=[];checked=0
    offsets=[-2,-1,0,1,3,4,5,7]
    for n in (3,64):
        center=256**(n-1);b=[255]*n
        pairs=[(digits(center+offset,n),b) for offset in offsets]
        result=secant_batch(pairs,max_patch=1)
        exact(pairs,result);checked+=len(pairs)
        assert result['counts']['seed_multiplications']==2
        assert result['residual_supports']==[0,0,1,1,0,1]
        carry_cases.append({'n':n,'offsets':offsets,'seed_multiplications':2,
                            'residual_supports':result['residual_supports']})
    pairs=[(digits(255+3*i,2),digits(256-2*i,2)) for i in range(10)]
    both=polynomial_batch(pairs)
    exact(pairs,both);checked+=len(pairs)
    assert both['degrees']==[1,1] and both['counts']['seed_multiplications']==3
    naive=2*integer(both['outputs'][2])-integer(both['outputs'][1])
    true=integer(both['outputs'][3])
    assert true-naive==-12 # 2*(delta A)*(delta B), the required mixed term.
    cache,creation=make_seed_cache(pairs,1)
    warm=polynomial_batch(pairs,cache=cache)
    exact(pairs,warm);checked+=len(pairs)
    assert warm['outputs']==both['outputs']
    assert creation['counts']['seed_multiplications']==1
    assert warm['counts']['seed_multiplications']==2
    # Maximum supported degree pair: order seven, including coefficients 35.
    pairs=[(digits(2**48-100+i**3,8),digits(2**48-200+2*i**3-i*i,8)) for i in range(11)]
    high=polynomial_batch(pairs)
    exact(pairs,high);checked+=len(pairs)
    assert high['degrees']==[3,3] and high['counts']['seed_multiplications']==7
    # Signed-width guard must reject silently truncated coefficients.
    try:signed_patch([-255,1],1,Ledger())
    except ValueError:pass
    else:raise AssertionError('oversize coefficient buffer was silently truncated')
    boundaries=0
    for width in (1,2,4):
        for value in (-256**width,-256**width+1,-1,0,1,256**width-1,256**width):
            if abs(value)>=256**width:
                try:signed_patch([value],width,Ledger())
                except ValueError:pass
                else:raise AssertionError('outside signed width accepted')
            else:
                patch=signed_patch([value],width,Ledger())
                assert sum(sign*digit*256**j for j,sign,digit in patch)==value
            boundaries+=1
    root=Path(__file__).resolve().parent
    result={'status':'PASS','exact_product_comparisons':checked,'long_carry_cases':carry_cases,
            'both_affine_degrees':[1,1],'mixed_term_negative_control_difference':true-naive,
            'partial_cache_seed_calls':{'creation':1,'warm':2,'cold':3},
            'highest_supported_degree_pair':[3,3],'highest_degree_seed_calls':7,
            'signed_width_boundary_controls':boundaries,'oversize_buffer_rejected':True,
            'source_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest()
                             for name in ('multiparent.py','audit.py')}}
    (root/'independent_review_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
