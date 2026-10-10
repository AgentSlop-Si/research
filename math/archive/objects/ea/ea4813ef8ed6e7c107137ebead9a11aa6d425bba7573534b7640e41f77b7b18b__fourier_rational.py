"""Verified dense rational edges for the FULL positive-sign DFT.

F E=J F, E upper bidiagonal, J cyclic with two upper bands. Related queries
solve (E-lambda I)x'=x and (J-lambda I)y'=y in linear field work.
"""
from collections import Counter
from dataclasses import dataclass
from rational_reuse import Counted, prepare_band, solve_band


@dataclass
class FourierRationalPlan:
    n: int
    q: object
    shift: object
    source_diagonal: list
    source_inverse_diagonal: list
    source_upper: list
    target: object
    common_preparation: dict
    preparation: dict


def batch_inverse(field, values):
    if any(value == field.zero for value in values):
        raise ValueError('singular source shift')
    prefixes=[field.one]
    for value in values:
        prefixes.append(field.mul(prefixes[-1],value))
    suffix=field.inv(prefixes[-1])
    out=[field.zero]*len(values)
    for i in range(len(values)-1,-1,-1):
        out[i]=field.mul(prefixes[i],suffix)
        suffix=field.mul(suffix,values[i])
    return out


def prepare_fourier_rational(field,n,q,shift):
    if n < 4 or n&(n-1) or shift == field.zero:
        raise ValueError('dyadic N>=4 and nonzero shift required')
    c=Counted(field)
    powers=[field.one]
    for _ in range(1,n): powers.append(c.mul(powers[-1],q))
    diagonal=[c.sub(c.neg(v),shift) for v in powers]
    upper=[c.neg(c.mul(powers[i],c.sub(powers[(i+1)%n],field.one))) for i in range(n)]
    inverse=batch_inverse(c,diagonal)
    # Common work generates the requested source vectors for both comparisons.
    common=dict(c.count)
    first=[c.sub(powers[(-i-1)%n],field.one) for i in range(n)]
    second=[c.neg(powers[(-i-1)%n]) for i in range(n)]
    target=prepare_band(field,c.neg(shift),[first,second])
    count=Counter(c.count);count.update(target.preparation)
    return FourierRationalPlan(n,q,shift,diagonal,inverse,upper,target,common,dict(count))


def source_action(field,plan,values):
    if len(values)!=plan.n: raise ValueError('wrong input length')
    out=[]
    for i in range(plan.n):
        acc=field.mul(plan.source_diagonal[i],values[i])
        if i+1<plan.n:
            acc=field.add(acc,field.mul(plan.source_upper[i],values[i+1]))
        out.append(acc)
    return out


def source_solve(field,plan,rhs):
    if len(rhs)!=plan.n: raise ValueError('wrong input length')
    c=Counted(field);out=[field.zero]*plan.n
    for i in range(plan.n-1,-1,-1):
        acc=rhs[i]
        if i+1<plan.n: acc=c.sub(acc,c.mul(plan.source_upper[i],out[i+1]))
        out[i]=c.mul(plan.source_inverse_diagonal[i],acc)
    return out,dict(c.count)


def verified_fourier_output(field,plan,anchor_input,anchor_output,query):
    if any(len(x)!=plan.n for x in (anchor_input,anchor_output,query)):
        raise ValueError('wrong vector length')
    c=Counted(field)
    if source_action(c,plan,query)!=list(anchor_input):
        raise ValueError('query does not satisfy supplied Fourier relation')
    result,counts=solve_band(field,plan.target,anchor_output)
    total=Counter(counts);total.update(c.count)
    return result,dict(field_operations=dict(total),relation_comparisons=plan.n,
                       full_output_writes=plan.n,new_fourier_calls=0)


def _power(c,value,exponent):
    result=c.one
    while exponent:
        if exponent&1:result=c.mul(result,value)
        exponent//=2
        if exponent:value=c.mul(value,value)
    return result


def corrected_fourier_output(field,plan,anchor_input,anchor_output,query,*,max_defects=8):
    """Allow a VERIFIED sparse recurrence residual, paying its full DFT.

    Returns (None,metadata) if the supplied edge has too many defects. Giving
    exact zero anchors yields a cold structured-input FFT; no paid cache is
    assumed in that special case. lambda and its plan remain supplied/paid.
    """
    if not isinstance(max_defects,int) or isinstance(max_defects,bool) or max_defects<0:
        raise ValueError('max_defects must be a nonnegative integer')
    if any(len(x)!=plan.n for x in (anchor_input,anchor_output,query)):
        raise ValueError('wrong vector length')
    c=Counted(field)
    recovered=source_action(c,plan,query)
    residual=[c.sub(a,b) for a,b in zip(recovered,anchor_input)]
    entries=[(j,a) for j,a in enumerate(residual) if a!=field.zero]
    meta=dict(accepted=len(entries)<=max_defects,defect_support=len(entries),
              support_comparisons=plan.n,field_operations=dict(c.count),
              new_full_fourier_calls=0,full_output_writes=0)
    if len(entries)>max_defects:return None,meta
    steps=[_power(c,plan.q,j) for j,_ in entries]
    terms=[a for _,a in entries]
    forcing=[]
    for k in range(plan.n):
        value=anchor_output[k]
        for j,term in enumerate(terms):
            value=c.add(value,term)
            if k+1<plan.n:terms[j]=c.mul(term,steps[j])
        forcing.append(value)
    result,counts=solve_band(field,plan.target,forcing)
    combined=Counter(c.count);combined.update(counts)
    meta.update(field_operations=dict(combined),full_output_writes=plan.n,
                sparse_phase_root_count=len(entries),sparse_frequency_values=plan.n)
    return result,meta


def try_recurrence_fourier(field,plan,query,*,max_defects=8):
    """Fresh-input exact full DFT when (E-lambda I)query has bounded support."""
    zeros=[field.zero]*plan.n
    result,info=corrected_fourier_output(field,plan,zeros,zeros,query,max_defects=max_defects)
    info.update(cold_structured_input=True,paid_anchor_transform_calls=0,
                initial_zero_values=plan.n)
    return result,info
