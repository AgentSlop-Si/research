"""Ordinary FFT implementation of the supplied decoded-state J_Q primitive.

Extends consecutive length-L coefficient blocks by -T_(1/Q) U_Q. Uses
four length-2L FFTs per new block; all fixed spectra and initial data paid.
Supplied primitive 2Lth root eta is an additional comparator assumption.
"""
from dataclasses import dataclass
from adaptive_recurrence import ROOT,Counted,denominator,initial_values
import sys
sys.path.insert(0,str(ROOT/'fft_qbasis_research'))
from orbit_kernel import fft_plan,fft


@dataclass
class DecodedPlan:
    n: int
    roots: list
    length: int
    q: list
    reciprocal: list
    fft: object
    upper_spectrum: list
    lower_spectrum: list
    preparation: dict


def prepare_baseline(field,n,roots,eta):
    if n<1 or not roots:
        raise ValueError('positive output length and nonempty support required')
    roots=list(roots)
    k=len(roots)
    length=max(2,1<<(k-1).bit_length())
    c=Counted(field)
    q=denominator(c,roots)
    h=[field.one]
    for j in range(1,length):
        terms=[c.mul(q[i],h[j-i]) for i in range(1,min(k,j)+1)]
        value=terms[0]
        for v in terms[1:]:
            value=c.add(value,v)
        h.append(c.neg(value))
    plan=fft_plan(c,length,eta)
    upper=[field.zero]*(2*length)
    upper[0]=q[length] if length<=k else field.zero
    for distance in range(1,length):
        j=length-distance
        upper[2*length-distance]=q[j] if j<=k else field.zero
    upper_spectrum=fft(c,plan,upper)
    lower_spectrum=fft(c,plan,h+[field.zero]*length)
    return DecodedPlan(n,roots,length,q,h,plan,upper_spectrum,lower_spectrum,dict(c.count))


def apply_baseline(field,plan,amplitudes):
    if len(amplitudes)!=len(plan.roots):
        raise ValueError('wrong amplitude length')
    n,l=plan.n,plan.length
    c=Counted(field)
    state=initial_values(c,plan.roots,amplitudes,l)
    result=state[:n]
    blocks=0
    def convolve(values,spectrum):
        transformed=fft(c,plan.fft,values+[field.zero]*l)
        product=[c.mul(a,b) for a,b in zip(transformed,spectrum)]
        return fft(c,plan.fft,product,inverse=True)[:l]
    while len(result)<n:
        middle=convolve(state,plan.upper_spectrum)
        tail=convolve(middle,plan.lower_spectrum)
        state=[c.neg(a) for a in tail]
        result.extend(state[:n-len(result)])
        blocks+=1
    counts=dict(c.count);counts.setdefault('mul',0);counts.setdefault('add',0)
    return result,dict(field_operations=counts,blocks=blocks,
                       fft_calls=4*blocks,fft_length=2*l,
                       full_output_writes=n,returned_output_count=n,
                       initial_prefix=l,extra_computed_values=(blocks+1)*l-n)


def expected_online(n,k):
    l=max(2,1<<(k-1).bit_length())
    levels=l.bit_length()-1
    blocks=max(0,(n+l-1)//l-1)
    out=dict(mul=k*(l-1)+blocks*(4*l*levels+12*l),
             add=(k-1)*l+blocks*4*l*(levels+1))
    if blocks:
        out['sub']=blocks*4*l*(levels+1)
        out['neg']=blocks*l
    return out


def expected_preparation(k):
    l=max(2,1<<(k-1).bit_length())
    levels=l.bit_length()-1
    reciprocal_products=sum(min(k,j) for j in range(1,l))
    transforms=2*l*(levels+1)
    return dict(mul=k*(k+1)//2+reciprocal_products+2*l+levels+transforms,
                add=reciprocal_products-l+1+transforms,
                sub=k*(k-1)//2+transforms,neg=k+l-1,constant_inverse=1)
