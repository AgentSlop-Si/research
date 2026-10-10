"""Independent finite-field review: no source input generator or audit helper.

Exhaustive smallest-input rejection/acceptance checks, noncommuting order,
closure singularity, zero parameters, supplied-pool accounting, and fallback.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib
import json
from composed_cycle import try_composed_fourier, composed_fft_or_fallback, DEPENDENCY


class Probe:
    def __init__(self,p):
        self.p,self.zero,self.one = p,0,1
        self.calls=Counter()
    def add(self,a,b):
        self.calls['add']+=1
        return (a+b)%self.p
    def sub(self,a,b):
        self.calls['sub']+=1
        return (a-b)%self.p
    def mul(self,a,b):
        self.calls['mul']+=1
        return a*b%self.p
    def inv(self,a):
        self.calls['inverse']+=1
        return pow(a,-1,self.p)


def direct(x,q,p):
    n=len(x)
    return [sum(value*pow(q,j*k,p) for j,value in enumerate(x))%p for k in range(n)]


def apply_filter(x,q,descriptor,pool,p):
    a,b,h,index=descriptor;n=len(x)
    return [(x[j]-pool[index]*pow(q,b*j%n,p)*x[(a*j+h)%n])%p for j in range(n)]


def matrix_of_filter(n,q,descriptor,pool,p):
    columns=[apply_filter([int(i==j) for i in range(n)],q,descriptor,pool,p) for j in range(n)]
    return [list(row) for row in zip(*columns)]


def mm(a,b,p):
    return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*b)] for row in a]


def inverse(a,p):
    n=len(a)
    a=[row[:]+[int(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None:raise ValueError('singular')
        a[j],a[pivot]=a[pivot],a[j]
        factor=pow(a[j][j],-1,p)
        a[j]=[x*factor%p for x in a[j]]
        for i in range(n):
            if i!=j:
                factor=a[i][j]
                a[i]=[(x-factor*y)%p for x,y in zip(a[i],a[j])]
    return [row[n:] for row in a]


def generate(n,q,filters,pool,residual,p):
    matrix=[[int(i==j) for j in range(n)] for i in range(n)]
    for descriptor in filters:
        matrix=mm(matrix_of_filter(n,q,descriptor,pool,p),matrix,p)
    return [sum(a*b for a,b in zip(row,residual))%p for row in inverse(matrix,p)]


def checked(x,q,filters,pool,budget,p,fallback=False):
    probe=Probe(p)
    fn=composed_fft_or_fallback if fallback else try_composed_fourier
    y,meta=fn(probe,x,q,filters,pool,budget)
    assert meta['field_operations']==dict(probe.calls)
    assert sum((Counter(s) for s in meta['stages'].values()),Counter())==probe.calls
    if y is not None:
        assert y==direct(x,q,p)
        if meta['ordinary_fft_calls']==0:
            n=len(x);d=len(filters);r=len(pool);s=meta['actual_defects']
            bill=(1+r+6*d+2*s)*n+r*((n.bit_length()-1)+2)+d
            assert sum(probe.calls.values())==bill==meta['expected_total']
    return y,meta


def exhaustive():
    p,n,q=5,4,2
    filters=[(5,1,1,0),(9,3,1,0)];pool=[2]
    result={'cases':0,'accepted':0,'declined':0}
    for values in product(range(p),repeat=n):
        residual=list(values)
        for descriptor in filters:
            residual=apply_filter(residual,q,descriptor,pool,p)
        support=sum(bool(v) for v in residual)
        for budget in (0,1):
            y,meta=checked(list(values),q,filters,pool,budget,p)
            assert (y is not None)==(support<=budget)
            result['cases']+=1
            result['accepted' if y is not None else 'declined']+=1
    assert result['accepted']==18
    return result


def special_cases():
    p,n,q=17,8,9
    cases=[([(5,1,1,0),(9,3,5,0)],[2]),
           ([(5,1,1,0),(9,3,5,1)],[2,2]),
           ([(5,1,1,0),(9,3,5,1)],[0,2]),
           ([(-3,-1,-3,0),(9,3,5,1),(13,-3,-1,0)],[2,4])]
    records=[]
    for filters,pool in cases:
        residual=[1]+[0]*(n-1)
        x=generate(n,q,filters,pool,residual,p)
        y,meta=checked(x,q,filters,pool,1,p)
        assert y is not None
        wrong=list(x)
        for descriptor in reversed(filters):
            wrong=apply_filter(wrong,q,descriptor,pool,p)
        records.append({'filters':filters,'pool':pool,'operations':sum(meta['field_operations'].values()),
                        'swapped_residual_support':sum(bool(v) for v in wrong),
                        'ordered_residual_support':meta['actual_defects'],
                        'noncommuting_on_input':wrong!=residual})
    assert records[0]['noncommuting_on_input']
    assert records[0]['operations']==16*n+3+4
    return records


def fallback_cases():
    p,n,q=17,8,9;filters=[(5,1,1,0),(9,3,5,0)]
    x=[i*i%p for i in range(n)]
    for pool,reason in [([3],'singular_filter'),([2],'composed_defect_budget_exceeded')]:
        y,meta=checked(x,q,filters,pool,0,p)
        assert y is None and meta['reason']==reason
        y,meta=checked(x,q,filters,pool,0,p,True)
        assert y is not None and meta['ordinary_fft_calls']==1
    return 2


def validation_cases():
    fn=try_composed_fourier
    p,n,q=17,8,9;valid=[(5,1,1,0)]
    cases=[(iter(()),[2],1),(valid,iter(()),1),
           ([(5,1,1,1)],[2],1),(valid,[2,3],1),
           ([(5,1,0,0)],[2],1),(valid,[2],-1)]
    for filters,pool,budget in cases:
        try:fn(Probe(p),[1]*n,q,filters,pool,budget)
        except ValueError:pass
        else:raise AssertionError('invalid parameters accepted')
    try:fn(Probe(p),[1]*n,1,valid,[2],1)
    except ValueError:pass
    else:raise AssertionError('nonprimitive root accepted')
    return len(cases)+1


def main():
    folder=Path(__file__).parent
    result={'status':'PASS','exhaustive_F5_N4':exhaustive(),
            'special_cases':special_cases(),'fallback_cases':fallback_cases(),
            'invalid_cases':validation_cases(),
            'source_sha256':{name:hashlib.sha256((folder/name).read_bytes()).hexdigest()
                             for name in ('README.md','composed_cycle.py','run_audit.py','review_edge_checks.py')},
            'dependency_sha256':{name:hashlib.sha256((DEPENDENCY/name).read_bytes()).hexdigest()
                                 for name in ('affine_cycle.py','exact_fields.py')}}
    (folder/'review_edge_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
