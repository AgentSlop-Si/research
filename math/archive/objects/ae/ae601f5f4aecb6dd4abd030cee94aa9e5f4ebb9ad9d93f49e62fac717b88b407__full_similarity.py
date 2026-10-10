"""Ordinary full-length three-convolution comparator for the SAME tail map.

This deliberately general polynomial evaluator is O(N log N). It is not the
special H_q(C) Fourier comparator, which computes a different operator.
An additional primitive 2N-th root eta with eta**2=q is supplied.
"""
from collections import Counter
from dataclasses import dataclass
from tail_blocks import Counted,prepare,fft
from orbit_kernel import fft_plan


@dataclass
class FullPlan:
    n: int
    fft: object
    inverse_spectrum: list
    upper_spectrum: list
    forward_spectrum: list
    g: list
    inverse_g: list
    preparation: dict


def prepare_full(field,n,r,eta,polynomial=None):
    if n<2 or n&(n-1) or not 1<=r<=n:
        raise ValueError('N power of two and 1<=r<=N required')
    c=Counted(field)
    q=c.mul(eta,eta)
    kernel=prepare(field,n,q)
    plan=fft_plan(c,n,eta)
    if polynomial is None:
        polynomial=kernel.kernel[n-r:]
    if not polynomial or len(polynomial)>r:
        raise ValueError('polynomial must have 1..r coefficients')
    polynomial=list(polynomial)+[field.zero]*(r-len(polynomial))
    g=[field.one]
    for j in range(n-1):
        g.append(c.mul(g[-1],c.sub(q,plan.powers[(-2*j)%(2*n)])))
    upper=[field.zero]*(2*n)
    for j,value in enumerate(polynomial,start=n-r):
        upper[(-j)%(2*n)]=value
    inverse_spectrum=fft(c,plan,kernel.middle+[field.zero]*n)
    upper_spectrum=fft(c,plan,upper)
    forward_spectrum=fft(c,plan,kernel.kernel+[field.zero]*n)
    counts=Counter(kernel.preparation);counts.update(c.count)
    return FullPlan(n,plan,inverse_spectrum,upper_spectrum,forward_spectrum,
                    g,kernel.middle,dict(counts))


def apply_full(field,plan,x):
    n=plan.n
    if len(x)!=n:
        raise ValueError('wrong input length')
    c=Counted(field)
    def convolution(values,spectrum):
        transformed=fft(c,plan.fft,values+[field.zero]*n)
        product=[c.mul(a,b) for a,b in zip(transformed,spectrum)]
        return fft(c,plan.fft,product,inverse=True)[:n]
    z=convolution(list(x),plan.inverse_spectrum)
    z=[c.mul(a,b) for a,b in zip(plan.g,z)]
    z=convolution(z,plan.upper_spectrum)
    z=[c.mul(a,b) for a,b in zip(plan.inverse_g,z)]
    out=convolution(z,plan.forward_spectrum)
    return out,dict(field_operations=dict(c.count),forward_ffts=3,inverse_ffts=3,
                    fft_length=2*n,returned_output_count=n,full_output_writes=n)


def expected_online(n):
    l=n.bit_length()-1
    return dict(mul=6*n*l+20*n,add=6*n*(l+1),sub=6*n*(l+1))


def expected_preparation(n):
    l=n.bit_length()-1
    return dict(mul=3*n*l+12*n+2*l-4,sub=2*n-2+3*n*(l+1),
                add=3*n*(l+1),neg=n-1,constant_inverse=2)
