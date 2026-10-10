"""Compile q-kernel phase histograms into a norm and minimum cycle-flow correction.

Only sequential same-root, same-length triangular convolution nodes are accepted.
The operator class is restricted; every input vector is allowed.
"""
from dataclasses import dataclass
from collections import Counter
from fixed_kernel import Counted, prepare, lower_convolution
from linear_filters import apply_factor_powers, counted_power
from orbit_rewrite import collapsed_orbit


@dataclass(frozen=True)
class FlowPlan:
    n: int
    b: int
    exponents: tuple
    raw_flow: tuple
    median: int
    flow: tuple
    distance: int
    word_preparation_bound: str = 'O(N+b), deterministic counting median; b<=N'


def compile_flow(n, exponents):
    exponents=tuple(exponents)
    b=len(exponents)
    if n<2 or n&(n-1) or b<2 or b&(b-1) or b>n or n%b:
        raise ValueError('N,b powers of two, 2<=b<=N')
    if any(type(e) is not int or not 0<=e<n for e in exponents):
        raise ValueError('symbolic phase exponents must be integers in [0,N)')
    delta=[0]*n
    for e in exponents: delta[e]+=1
    for e in range(0,n,n//b): delta[e]-=1
    prefix=0; raw=[]
    for d in delta:
        prefix-=d
        raw.append(prefix)
    assert prefix==0
    # Raw flows lie in [-b,b]. Counting selects a median in linear word work.
    counts=[0]*(2*b+1)
    for f in raw: counts[f+b]+=1
    cumulative=0
    for i,c in enumerate(counts):
        cumulative+=c
        if cumulative>n//2:
            median=i-b
            break
    flow=tuple(f-median for f in raw)
    assert all(flow[(e-1)%n]-flow[e]==delta[e] for e in range(n))
    return FlowPlan(n,b,exponents,tuple(raw),median,flow,sum(abs(f) for f in flow))


def apply_compiled(field, q, plan, x):
    if len(x)!=plan.n: raise ValueError('wrong input length')
    base,base_counts=collapsed_orbit(field,plan.n,q,plan.b,x)
    corrections={e:f for e,f in enumerate(plan.flow) if f}
    result,correction_counts=apply_factor_powers(field,base,corrections,q)
    assert correction_counts['filter_passes']==plan.distance
    return result, {'base':base_counts,'correction':correction_counts,
                    'cycle_distance':plan.distance,'compiler_word_work':plan.word_preparation_bound}


def apply_explicit(field,n,q,exponents,x):
    """Independent direct full operator word; no norm or cycle-flow identity."""
    plan=prepare(field,n,q)
    c=Counted(field); traffic=Counter(); value=list(x)
    for e in exponents:
        phase=counted_power(c,q,e)
        power=field.one; kernel=[]
        for j in range(n):
            kernel.append(c.mul(plan.kernel[j],power))
            if j+1<n: power=c.mul(power,phase)
        value=lower_convolution(c,kernel,value,traffic)
    return value, {'kernel_preparation':plan.preparation,'field_operations':dict(c.count),
                   'logical_array_traffic':dict(traffic)}
