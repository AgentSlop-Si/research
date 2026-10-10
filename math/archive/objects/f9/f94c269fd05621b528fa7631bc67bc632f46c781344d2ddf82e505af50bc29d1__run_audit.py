from __future__ import annotations
import hashlib
import json
import random
from collections import Counter
from pathlib import Path
from affine_cycle import Counted, cycle_order, ordinary_fft, try_affine_fourier, affine_fft_or_fallback
from exact_fields import PrimeField, CyclotomicField, fourier, mv, rank


class Traced:
    def __init__(self, field): self.field=field; self.calls=Counter()
    def __getattr__(self,name):
        value=getattr(self.field,name)
        if name not in ('add','sub','mul','inv'): return value
        def called(*args): self.calls[name if name!='inv' else 'inverse']+=1; return value(*args)
        return called


def make_input(field,n,q,parameter,a,b,shift,defects):
    """Independent forward-affine closure; no calls to production cycle solver."""
    powers=[field.power(q,j) for j in range(n)]
    permutation=[(a*j+shift)%n for j in range(n)]
    order=cycle_order(permutation)
    coefficients=[field.mul(parameter,powers[(b*j)%n]) for j in range(n)]
    rhs=[defects.get(j,field.zero) for j in range(n)]
    alpha,beta=field.one,field.zero
    for j in order:
        reciprocal=field.inv(coefficients[j])
        alpha=field.mul(alpha,reciprocal)
        beta=field.mul(field.sub(beta,rhs[j]),reciprocal)
    first=field.mul(beta,field.inv(field.sub(field.one,alpha)))
    out=[field.zero]*n; value=first
    for j in order:
        out[j]=value
        value=field.mul(field.sub(value,rhs[j]),field.inv(coefficients[j]))
    assert value==first
    return out


def checked(field,x,q,**kwargs):
    traced=Traced(field)
    y,meta=try_affine_fourier(traced,x,q,**kwargs)
    assert dict(traced.calls)==meta['field_operations']
    assert sum((Counter(v) for v in meta['stages'].values()),Counter())==traced.calls
    if y is not None:
        expected=mv(field,fourier(field,len(x)),x)
        assert y==expected
    return y,meta


def main():
    rng=random.Random(948320)
    results={'status':'PASS','scope':'Detected affine-cycle low-defect inputs; not arbitrary-input sub-NlogN FFT',
             'accepted_checks':0,'declines':0,'singular_declines':0,'intertwining_basis_checks':0,
             'invalid_checks':0,'exact_cyclotomic_checks':0,'hybrid_checks':0,'benchmarks':[]}
    for p in (97,257,65537):
        field=PrimeField(p)
        for n in (4,8,16,32):
            if (p-1)%n: continue
            q=field.root(n)
            for a,b,shift in ((5,1,1),(9,3,5),(13,-3,-1)):
                inverse_a=pow(a,-1,n); powers=[field.power(q,j) for j in range(n)]
                # Operator identity is tested independently on every basis input.
                for j in range(n):
                    x=[field.zero]*n;x[j]=field.one
                    source=[field.mul(powers[b*i%n],x[(a*i+shift)%n]) for i in range(n)]
                    fs=mv(field,fourier(field,n),source)
                    fx=mv(field,fourier(field,n),x)
                    target=[field.mul(powers[-shift*(inverse_a*(k+b)%n)%n],fx[inverse_a*(k+b)%n]) for k in range(n)]
                    assert fs==target
                    results['intertwining_basis_checks']+=1
                for s in (1,2):
                    parameter=next(field.integer(v) for v in range(2,p) if field.power(field.integer(v),n)!=field.integer(-1))
                    defects={j:field.integer(rng.randrange(1,p)) for j in rng.sample(range(n),s)}
                    x=make_input(field,n,q,parameter,a,b,shift,defects)
                    y,meta=checked(field,x,q,max_defects=s,a=a,b=b,shift=shift)
                    if y is not None: results['accepted_checks']+=1
                    else: assert meta['reason']=='insufficient_majority_support';results['declines']+=1
                    # Supplied parameter still verifies every source coordinate.
                    y,meta=checked(field,x,q,max_defects=s,a=a,b=b,shift=shift,supplied_lambda=parameter)
                    assert y is not None; results['accepted_checks']+=1
            for _ in range(3):
                x=[field.integer(rng.randrange(p)) for _ in range(n)]
                y,meta=checked(field,x,q,max_defects=1)
                results['accepted_checks' if y is not None else 'declines']+=1
            y,meta=checked(field,[field.zero]*n,q)
            assert y is not None;results['accepted_checks']+=1
            # lambda=0: a sparse input, tested through the same verified engine.
            x=[field.zero]*n;x[n//2]=field.one
            y,meta=checked(field,x,q,supplied_lambda=field.zero)
            assert y is not None;results['accepted_checks']+=1
            if (p-1)%(2*n)==0:
                parameter=field.root(2*n)
                order=cycle_order([(5*j+1)%n for j in range(n)])
                x=[field.zero]*n;value=field.one
                for j in order:
                    x[j]=value;value=field.mul(value,field.inv(field.mul(parameter,field.power(q,j))))
                assert value==field.one
                y,meta=checked(field,x,q,max_defects=0)
                assert y is None and meta['reason']=='singular_target_cycle'
                results['singular_declines']+=1
    for n in (4,8,16):
        field=CyclotomicField(n);q=field.root(n)
        for a,b,shift in ((5,1,1),(9,3,5)):
            x=make_input(field,n,q,field.integer(2),a,b,shift,{0:field.one})
            y,meta=checked(field,x,q,a=a,b=b,shift=shift)
            assert y is not None;results['exact_cyclotomic_checks']+=1
    field=PrimeField(65537);n=32;q=field.root(n)
    x=make_input(field,n,q,field.integer(2),5,1,1,{0:field.one})
    powers=[field.power(q,j) for j in range(n)]
    relation_rows=[[x[j],field.mul(powers[j],x[j]),x[j+1],field.mul(powers[j],x[j+1])] for j in range(n-1)]
    results['distinctness_witness']={
        'N':n,'a':5,'b':1,'shift':1,'lambda':2,
        'nonzero_input_entries':sum(v!=0 for v in x),
        'nearest_neighbor_qlinear_relation_rank':rank(field,relation_rows),
        'untwisted_P5_minus_I_defects':sum(x[(5*j)%n]!=x[j] for j in range(n))}
    assert results['distinctness_witness']['nearest_neighbor_qlinear_relation_rank']==4
    for n in (8,16,32,64):
        q=field.root(n)
        for _ in range(2):
            x=[field.integer(rng.randrange(field.p)) for _ in range(n)]
            traced=Traced(field)
            y,meta=affine_fft_or_fallback(traced,x,q)
            assert dict(traced.calls)==meta['field_operations']
            assert y==mv(field,fourier(field,n),x)
            assert meta['ordinary_fft_calls']==1
            results['hybrid_checks']+=1
    for n in (1024,4096,8192,32768):
        q=field.root(n)
        parameter=next(field.integer(v) for v in range(2,field.p) if field.power(field.integer(v),n)!=field.integer(-1))
        x=make_input(field,n,q,parameter,5,1,1,{0:field.one})
        y,meta=try_affine_fourier(field,x,q)
        z,baseline=ordinary_fft(field,x,q)
        assert y==z and y is not None
        total=sum(meta['field_operations'].values());normal=sum(baseline.values())
        results['benchmarks'].append({'N':n,'nonzero_input_entries':meta['nonzero_input_entries'],
            'new_operations':total,'ordinary_fft_operations':normal,
            'new_field_operations':meta['field_operations'],'ordinary_field_operations':baseline,
            'stages':meta['stages'],'new_over_ordinary':total/normal})
    for kwargs in ({'a':3},{'b':2},{'shift':0},{'max_defects':-1}):
        try: try_affine_fourier(field,[field.one]*8,field.root(8),**kwargs)
        except ValueError: results['invalid_checks']+=1
        else: raise AssertionError('invalid parameter accepted')
    try: try_affine_fourier(field,[field.one]*8,field.one)
    except ValueError: results['invalid_checks']+=1
    else: raise AssertionError('invalid root accepted')
    results['source_sha256']=hashlib.sha256(Path('affine_cycle.py').read_bytes()).hexdigest()
    Path('results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:v for k,v in results.items() if k!='benchmarks'},indent=2))
    print('benchmarks:',[(v['N'],v['new_operations'],v['ordinary_fft_operations']) for v in results['benchmarks']])


if __name__=='__main__':main()
