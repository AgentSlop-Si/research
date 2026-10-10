"""Exact fusion of noncommuting, diagonally modulated q-Weyl tails.

Returns sum_j Q**j C**(N-r) p_j(C) Q**j x using one projected inverse
convolution and one decoding convolution. No full N-output term is formed.
This is a restricted aggregate, not the complete H_q(C) or a faster FFT.
"""
from pathlib import Path
import sys
from dataclasses import dataclass,replace
from collections import Counter
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'fft_resolvent_aggregate_research'))
from tail_blocks import (prepare_tail,apply_tail,Counted,FFTPlan,fft,
    expected_preparation as tail_preparation,expected_online as tail_online)


@dataclass
class FusionPlan:
    n: int
    r: int
    steps: int
    window: int
    projection: object
    middle_fft: object
    middle_spectra: list
    roots: list
    polynomials: list
    preparation: dict


def _polynomials(field,r,polynomials):
    if not polynomials or any(not p or len(p)>r for p in polynomials):
        raise ValueError('nonempty list of nonempty polynomials of degree <r required')
    return [list(p)+[field.zero]*(r-len(p)) for p in polynomials]


def _upper(field,polynomial,r):
    out=[field.zero]*(2*r)
    out[0]=polynomial[0]
    for j in range(1,r):
        out[2*r-j]=polynomial[j]
    return out


def prepare_fused(field,n,r,q,polynomials):
    polynomials=_polynomials(field,r,polynomials)
    steps=len(polynomials)
    window=1<<(r+steps-2).bit_length()
    if r<1 or r&(r-1) or 2*window>n:
        raise ValueError('r power of two; next_power_of_two(r+s-1)<=N/2 required')
    # Reuse the old projection/decode implementation's fixed banks. Its
    # unused zero-polynomial spectrum is conservatively charged too.
    base=prepare_tail(field,n,window,q,[field.zero])
    c=Counted(field)
    roots=[field.one]
    for _ in range(1,n):
        roots.append(c.mul(roots[-1],q))
    multiplier=field.one
    for _ in range((window//r).bit_length()-1):
        multiplier=c.add(multiplier,multiplier)
    inverse_length=c.mul(base.fft.inverse_length,multiplier)
    permutation=[0]
    while len(permutation)<2*r:
        doubled=[2*j for j in permutation]
        permutation=doubled+[j+1 for j in doubled]
    small=FFTPlan(r,base.fft.powers[::window//r],permutation,
                  inverse_length,inverse_length)
    spectra=[fft(c,small,_upper(field,p,r)) for p in polynomials]
    counts=Counter(base.preparation);counts.update(c.count)
    return FusionPlan(n,r,steps,window,base,small,spectra,roots,
                      polynomials,dict(counts))


def _project(c,plan,x):
    m=plan.window
    combined=None
    for b,spectrum in enumerate(plan.projection.projection_spectra):
        value=fft(c,plan.projection.fft,list(x[b*m:(b+1)*m])+[c.zero]*m)
        value=[c.mul(a,b) for a,b in zip(value,spectrum)]
        combined=value if combined is None else [c.add(a,b) for a,b in zip(combined,value)]
    return fft(c,plan.projection.fft,combined,inverse=True)[:m]


def _decode(c,plan,state):
    m=plan.window
    value=fft(c,plan.projection.fft,state+[c.zero]*(2*m-len(state)))
    out=[]
    for spectrum in plan.projection.decoding_spectra:
        product=[c.mul(a,b) for a,b in zip(value,spectrum)]
        out.extend(fft(c,plan.projection.fft,product,inverse=True)[:m])
    return out


def apply_fused(field,plan,x):
    if len(x)!=plan.n:
        raise ValueError('wrong input length')
    n,r,s,m=plan.n,plan.r,plan.steps,plan.window
    c=Counted(field)
    suffix=_project(c,plan,x)
    start=n-m
    heads=[]
    for j in range(s):
        scaled=[c.mul(g,a) for g,a in zip(plan.projection.g_tail[-r:],suffix[-r:])]
        transformed=fft(c,plan.middle_fft,scaled+[field.zero]*r)
        product=[c.mul(a,b) for a,b in zip(transformed,plan.middle_spectra[j])]
        small=fft(c,plan.middle_fft,product,inverse=True)[:r]
        heads.append([c.mul(g,a) for g,a in zip(plan.projection.inverse_g_head[:r],small)])
        if j+1<s:
            # D=(I-A)Q; discard the first coordinate, whose predecessor is
            # unavailable. All retained coordinates use known predecessors.
            suffix=[c.sub(c.mul(plan.roots[start+i],suffix[i]),
                          c.mul(plan.roots[start+i-1],suffix[i-1]))
                    for i in range(1,len(suffix))]
            start+=1
    state=heads[-1]
    for j in range(s-2,-1,-1):
        # Reverse Horner: u_j + D*(u_(j+1)+D*(...)). The prefix grows by one.
        next_state=[c.mul(plan.roots[0],state[0])]
        next_state.extend(c.sub(c.mul(plan.roots[i],state[i]),
                                c.mul(plan.roots[i-1],state[i-1]))
                          for i in range(1,len(state)))
        next_state.append(c.neg(c.mul(plan.roots[len(state)-1],state[-1])))
        for i in range(r):
            next_state[i]=c.add(next_state[i],heads[j][i])
        state=next_state
    result=_decode(c,plan,state)
    return result,dict(field_operations=dict(c.count),
        projected_coordinates=m,decoded_state_coordinates=len(state),
        stored_middle_coordinates=s*r,full_output_terms_materialized=0,
        returned_output_count=n,full_output_writes=n,
        projection_decode_fft_length=2*m,middle_fft_length=2*r,
        projection_decode_forward_ffts=n//m+1,
        projection_decode_inverse_ffts=n//m+1,
        middle_forward_ffts=s,middle_inverse_ffts=s,
        logical_source_input_reads=n,
        model='exact field arithmetic; logical arrays, not interpreter allocation counts')


def expected_preparation(n,r,s):
    m=1<<(r+s-2).bit_length()
    out=Counter(tail_preparation(n,m))
    b=s*r*((2*r).bit_length()-1)
    out.update(mul=n+b,add=(m//r).bit_length()-1+b,sub=b)
    return dict(out)


def expected_online(n,r,s):
    m=1<<(r+s-2).bit_length()
    f=2*(n+m)*((2*m).bit_length()-1)+2*s*r*((2*r).bit_length()-1)
    si=(s-1)*(m-1)-(s-1)*(s-2)//2
    so=(s-1)*r+(s-1)*(s-2)//2
    out=dict(mul=f+6*n+2*m+6*s*r+2*(si+so),
             add=f+2*n-2*m+(s-1)*r,
             sub=f+si+so-(s-1))
    if s>1:
        out['neg']=s-1
    return out


def prepare_independent(field,n,r,q,polynomials):
    """Same aggregate, shared constant banks, but one full tail output/term."""
    polynomials=_polynomials(field,r,polynomials)
    base=prepare_tail(field,n,r,q,polynomials[0])
    c=Counted(field)
    plans=[base]
    for p in polynomials[1:]:
        spectrum=fft(c,base.fft,_upper(field,p,r))
        plans.append(replace(base,polynomial=p,middle_spectrum=spectrum))
    roots=[field.one]
    for _ in range(1,n):
        roots.append(c.mul(roots[-1],q))
    counts=Counter(base.preparation);counts.update(c.count)
    return dict(n=n,r=r,steps=len(plans),plans=plans,roots=roots,preparation=dict(counts))


def apply_independent(field,plan,x):
    n=plan['n']
    if len(x)!=n:
        raise ValueError('wrong input length')
    c=Counted(field)
    current=list(x)
    diagonal=[field.one]*n
    result=None
    count=Counter()
    for j,tail in enumerate(plan['plans']):
        if j:
            current=[c.mul(a,b) for a,b in zip(plan['roots'],current)]
            diagonal=[c.mul(a,b) for a,b in zip(plan['roots'],diagonal)]
        value,details=apply_tail(field,tail,current)
        count.update(details['field_operations'])
        if j:
            value=[c.mul(a,b) for a,b in zip(diagonal,value)]
            result=[c.add(a,b) for a,b in zip(result,value)]
        else:
            result=value
    count.update(c.count)
    return result,dict(field_operations=dict(count),full_output_terms_materialized=plan['steps'])


def expected_independent_preparation(n,r,s):
    out=Counter(tail_preparation(n,r))
    f=(s-1)*r*((2*r).bit_length()-1)
    out.update(mul=n-1+f,add=f,sub=f)
    return dict(out)


def expected_independent_online(n,r,s):
    out=Counter({k:s*v for k,v in tail_online(n,r).items()})
    out.update(mul=3*n*(s-1),add=n*(s-1))
    return dict(out)
