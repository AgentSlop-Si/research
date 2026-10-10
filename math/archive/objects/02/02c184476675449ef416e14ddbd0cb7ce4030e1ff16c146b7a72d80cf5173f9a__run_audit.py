from __future__ import annotations
import hashlib
import json
import random
from collections import Counter
from pathlib import Path
from composed_cycle import try_composed_fourier,composed_fft_or_fallback,ordinary_fft,DEPENDENCY
from affine_cycle import try_affine_fourier
from exact_fields import PrimeField,CyclotomicField,fourier,mv,inverse


class Traced:
    def __init__(self,field):self.field=field;self.calls=Counter()
    def __getattr__(self,name):
        value=getattr(self.field,name)
        if name not in ('add','sub','mul','inv'):return value
        def called(*args):self.calls[name if name!='inv' else 'inverse']+=1;return value(*args)
        return called


def independent_filter(field,x,q,descriptor,lambdas):
    n=len(x);a,b,shift,index=descriptor;parameter=lambdas[index]
    return [field.sub(x[j],field.mul(parameter,field.mul(field.power(q,b*j%n),x[(a*j+shift)%n])))
            for j in range(n)]


def generated_input(field,n,q,filters,lambdas,residual,use_gauss=False):
    current=list(residual)
    for descriptor in reversed(filters):
        a,b,shift,index=descriptor;parameter=lambdas[index]
        if use_gauss:
            columns=[]
            for j in range(n):
                basis=[field.zero]*n;basis[j]=field.one
                columns.append(independent_filter(field,basis,q,descriptor,lambdas))
            matrix=[list(row) for row in zip(*columns)]
            current=mv(field,inverse(field,matrix),current)
        else:
            # Independent forward recurrence y_next=(y-rhs)/edge with affine closure.
            order=[];j=0
            for _ in range(n):order.append(j);j=(a*j+shift)%n
            assert j==0 and len(set(order))==n
            coefficient=[field.mul(parameter,field.power(q,b*j%n)) for j in range(n)]
            alpha,beta=field.one,field.zero
            for j in order:
                reciprocal=field.inv(coefficient[j])
                alpha=field.mul(alpha,reciprocal)
                beta=field.mul(field.sub(beta,current[j]),reciprocal)
            first=field.mul(beta,field.inv(field.sub(field.one,alpha)))
            output=[field.zero]*n;value=first
            for j in order:
                output[j]=value
                value=field.mul(field.sub(value,current[j]),field.inv(coefficient[j]))
            assert value==first
            current=output
    return current


def checked(field,x,q,filters,lambdas,budget):
    traced=Traced(field)
    y,meta=try_composed_fourier(traced,x,q,filters,lambdas,budget)
    assert dict(traced.calls)==meta['field_operations']
    assert sum((Counter(s) for s in meta['stages'].values()),Counter())==traced.calls
    if y is not None:
        assert y==mv(field,fourier(field,len(x)),x)
        assert sum(traced.calls.values())==meta['expected_total']
    return y,meta


def main():
    rng=random.Random(53730)
    results={'status':'PASS','scope':'exact supplied composed low-defect family only',
             'accepted_checks':0,'declines':0,'gaussian_generated_checks':0,
             'cyclotomic_checks':0,'fallback_checks':0,'singular_checks':0,
             'zero_parameter_checks':0,'invalid_checks':0,'benchmarks':[]}
    descriptors=[(5,1,1,0),(9,3,5,0),(13,-3,-1,0)]
    for p in (97,257,65537):
        field=PrimeField(p)
        for n in (4,8,16,32):
            q=field.root(n)
            choices=[field.integer(v) for v in range(2,p) if field.power(field.integer(v),n)!=field.integer(-1)]
            for depth in (1,2,3):
                for pooled in (True,False):
                    lambdas=[choices[0]] if pooled else choices[:depth]
                    filters=[(*item[:3],0 if pooled else i) for i,item in enumerate(descriptors[:depth])]
                    for s in (1,2):
                        residual=[field.zero]*n
                        for j in rng.sample(range(n),s):residual[j]=field.integer(rng.randrange(1,p))
                        gauss=n<=8
                        x=generated_input(field,n,q,filters,lambdas,residual,use_gauss=gauss)
                        y,meta=checked(field,x,q,filters,lambdas,s)
                        assert y is not None
                        assert meta['actual_defects']==s
                        results['accepted_checks']+=1
                        results['gaussian_generated_checks']+=gauss
            for _ in range(2):
                x=[field.integer(rng.randrange(p)) for _ in range(n)]
                filters=descriptors[:2];lambdas=[choices[0]]
                y,meta=checked(field,x,q,filters,lambdas,1)
                assert y is None;results['declines']+=1
                traced=Traced(field)
                y,meta=composed_fft_or_fallback(traced,x,q,filters,lambdas,1)
                assert y==mv(field,fourier(field,n),x)
                assert meta['field_operations']==dict(traced.calls)
                assert sum((Counter(s) for s in meta['stages'].values()),Counter())==traced.calls
                assert meta['ordinary_fft_calls']==1
                results['fallback_checks']+=1
            if (p-1)%(2*n)==0:
                x=[field.integer(rng.randrange(p)) for _ in range(n)]
                y,meta=checked(field,x,q,descriptors[:2],[field.root(2*n)],1)
                assert y is None and meta['reason']=='singular_filter'
                results['singular_checks']+=1
            x=[field.zero]*n;x[0]=field.one
            y,meta=checked(field,x,q,descriptors[:2],[field.zero],1)
            assert y is not None;results['zero_parameter_checks']+=1
    for n in (4,8):
        field=CyclotomicField(n);q=field.root(n)
        for depth in (2,3):
            filters=descriptors[:depth];lambdas=[field.integer(2)]
            residual=[field.zero]*n;residual[0]=field.one
            x=generated_input(field,n,q,filters,lambdas,residual,use_gauss=True)
            y,meta=checked(field,x,q,filters,lambdas,1)
            assert y is not None;results['cyclotomic_checks']+=1
    field=PrimeField(65537);n=32;q=field.root(n)
    filters=descriptors[:2];lambdas=[field.integer(2)]
    residual=[field.zero]*n;residual[0]=field.one
    x=generated_input(field,n,q,filters,lambdas,residual)
    single_support=[];single_declines=[]
    for a,b,shift,index in filters:
        single_support.append(sum(v!=field.zero for v in independent_filter(field,x,q,(a,b,shift,index),lambdas)))
        y,meta=try_affine_fourier(field,x,q,a=a,b=b,shift=shift,max_defects=1)
        single_declines.append(y is None)
    y,meta=try_composed_fourier(field,x,q,filters,lambdas,1)
    left=independent_filter(field,independent_filter(field,x,q,filters[0],lambdas),q,filters[1],lambdas)
    wrong=independent_filter(field,independent_filter(field,x,q,filters[1],lambdas),q,filters[0],lambdas)
    results['composition_witness']={'N':n,'filters':filters,'shared_lambda':2,
        'input_nonzero_entries':sum(v!=field.zero for v in x),
        'single_filter_residual_supports':single_support,
        'single_filter_discovery_declines':single_declines,
        'ordered_composed_residual_support':sum(v!=field.zero for v in left),
        'reversed_composed_residual_support':sum(v!=field.zero for v in wrong),
        'noncommuting_on_this_input':left!=wrong,
        'new_operation_count':sum(meta['field_operations'].values())}
    assert all(single_declines) and min(single_support)>1 and left!=wrong
    for n in (1024,4096,8192,32768):
        q=field.root(n);lambdas=[field.integer(2)]
        residual=[field.zero]*n;residual[0]=field.one
        x=generated_input(field,n,q,filters,lambdas,residual)
        y,meta=try_composed_fourier(field,x,q,filters,lambdas,1)
        baseline,counts=ordinary_fft(field,x,q)
        assert y==baseline and y is not None
        total=sum(meta['field_operations'].values())
        assert total==16*n+n.bit_length()+3
        results['benchmarks'].append({'N':n,'composed_operations':total,
            'ordinary_operations':sum(counts.values()),
            'nonzero_input_entries':sum(v!=field.zero for v in x),
            'intermediate_support':meta['intermediate_support'],
            'field_operations':meta['field_operations'],'stages':meta['stages']})
    for bad_filters,bad_pool,budget in (([],[2],1),([(3,1,1,0)],[2],1),
            ([(5,2,1,0)],[2],1),([(5,1,2,0)],[2],1),([(5,1,1,1)],[2],1),
            ([(5,1,1,0)],[2,3],1),([(5,1,1,0)],[2],-1)):
        try:try_composed_fourier(field,[1]*8,field.root(8),bad_filters,bad_pool,budget)
        except ValueError:results['invalid_checks']+=1
        else:raise AssertionError('invalid descriptor accepted')
    for bad_filters,bad_pool in ((iter(()),[2]),([(5,1,1,0)],iter(()))):
        try:try_composed_fourier(field,[1]*8,field.root(8),bad_filters,bad_pool,1)
        except ValueError:results['invalid_checks']+=1
        else:raise AssertionError('empty generator accepted')
    results['source_sha256']=hashlib.sha256(Path('composed_cycle.py').read_bytes()).hexdigest()
    results['dependency_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (DEPENDENCY/'affine_cycle.py',DEPENDENCY/'exact_fields.py')}
    Path('results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:v for k,v in results.items() if k!='benchmarks'},indent=2))
    print('benchmarks:',[(v['N'],v['composed_operations'],v['ordinary_operations']) for v in results['benchmarks']])


if __name__=='__main__':main()
