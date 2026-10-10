"""Fully charged support-adaptive sparse-annihilator decoder.

For stride b, distinct lambda=z_s**b give R_b(t)=prod(1-lambda*t).
The original exponential sum is annihilated by R_b(t**b), possibly much
sparser than its minimal denominator. Classical recurrence arithmetic;
no general sparse-FFT improvement is claimed.
"""
from pathlib import Path
import sys
from dataclasses import dataclass
from operator import index

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'fft_qweyl_boundary_research'))
from fixed_kernel import Counted
from prior_exact_arithmetic import PrimeField,CyclotomicField


def power(c,x,exponent):
    """Binary constant powering; every actual multiply is charged."""
    if exponent<0:
        raise ValueError('nonnegative exponent required')
    if exponent==0:
        return c.one
    result=None
    value=x
    while exponent:
        if exponent&1:
            result=value if result is None else c.mul(result,value)
        exponent//=2
        if exponent:
            value=c.mul(value,value)
    return result


def denominator(c,roots):
    q=[c.one]
    for root in roots:
        out=[q[0]]
        out.extend(c.sub(q[j],c.mul(root,q[j-1])) for j in range(1,len(q)))
        out.append(c.neg(c.mul(root,q[-1])))
        q=out
    return q


def initial_values(c,roots,amplitudes,length):
    """Direct modal prefix with O(length) workspace, no stored power table."""
    if len(roots)!=len(amplitudes):
        raise ValueError('amplitude length does not match support')
    out=[]
    value=amplitudes[0]
    for j in range(length):
        out.append(value)
        if j+1<length:
            value=c.mul(value,roots[0])
    for root,amplitude in zip(roots[1:],amplitudes[1:]):
        value=amplitude
        for j in range(length):
            out[j]=c.add(out[j],value)
            if j+1<length:
                value=c.mul(value,root)
    return out


@dataclass
class AdaptivePlan:
    n: int
    roots: list
    stride: int
    degree: int
    initial_length: int
    taps: list
    short_denominator: list
    candidates: list
    preparation: dict
    support_equality_tests: int
    coefficient_zero_tests: int


def default_strides(n,k):
    limit=min(n,k*k)
    values=[]
    b=1
    while b<=limit:
        values.append(b)
        b*=2
    return values


def expected_online(n,k,initial_length,tap_count):
    m=min(n,initial_length)
    return dict(mul=k*(m-1)+(n-m)*tap_count,
                add=(k-1)*m+(n-m)*(tap_count-1))


def prepare_adaptive(field,n,roots,strides=None):
    if n<1 or not roots:
        raise ValueError('positive output length and nonempty support required')
    roots=list(roots)
    if any(z==field.zero for z in roots):
        raise ValueError('support roots must be nonzero')
    k=len(roots)
    raw=default_strides(n,k) if strides is None else list(strides)
    normalized=[]
    for b in raw:
        if isinstance(b,bool):
            raise TypeError('strides must be integers, not booleans')
        b=index(b)
        if b<1:
            raise ValueError('strides must be positive')
        normalized.append(b)
    strides=sorted(set([1]+normalized))
    c=Counted(field)
    equality=0
    zero_tests=0
    records=[]
    best=None
    for b in strides:
        powered=[power(c,z,b) for z in roots]
        distinct=[]
        for value in powered:
            matched=False
            for previous in distinct:
                equality+=1
                if value==previous:
                    matched=True
                    break
            if not matched:
                distinct.append(value)
        if b==1 and len(distinct)!=k:
            raise ValueError('input support roots must be distinct')
        q=denominator(c,distinct)
        nonzero=[]
        for i in range(1,len(q)):
            zero_tests+=1
            if q[i]!=field.zero:
                nonzero.append(i)
        order=b*len(distinct)
        online=expected_online(n,k,order,len(nonzero))
        row=dict(stride=b,distinct_powers=len(distinct),annihilator_degree=order,
                 initial_length=min(n,order),tap_count=len(nonzero),online=online,
                 online_field_total=sum(online.values()))
        records.append(row)
        key=(row['online_field_total'],row['initial_length'],b)
        if best is None or key<best[0]:
            best=(key,b,q,nonzero,order)
    _,stride,q,nonzero,order=best
    taps=[(stride*i,c.neg(q[i])) for i in nonzero]
    return AdaptivePlan(n,roots,stride,len(q)-1,min(n,order),taps,q,records,
                        dict(c.count),equality,zero_tests)


def apply_adaptive(field,plan,amplitudes):
    if len(amplitudes)!=len(plan.roots):
        raise ValueError('wrong amplitude length')
    c=Counted(field)
    out=initial_values(c,plan.roots,amplitudes,plan.initial_length)
    for m in range(plan.initial_length,plan.n):
        distance,weight=plan.taps[0]
        value=c.mul(weight,out[m-distance])
        for distance,weight in plan.taps[1:]:
            value=c.add(value,c.mul(weight,out[m-distance]))
        out.append(value)
    count=dict(c.count)
    # Zero entries are retained in the closed ledger for easy comparison.
    count.setdefault('mul',0);count.setdefault('add',0)
    return out,dict(field_operations=count,full_output_writes=plan.n,
                    returned_output_count=plan.n,initial_prefix=plan.initial_length,
                    recurrence_outputs=plan.n-plan.initial_length,
                    recurrence_taps=len(plan.taps),transform_calls=0,
                    input_amplitude_reads=len(plan.roots),
                    model='exact field operations and explicit word indices')
