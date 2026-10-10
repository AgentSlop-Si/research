"""Honest O(N log N) comparator for H_q(C), using ordinary radix two.

Inputs: a field, N=power of two, and a supplied primitive 2N-th root eta.
This is not an independent sub-N-log-N Fourier algorithm.
"""
import sys
from pathlib import Path
from dataclasses import dataclass
from collections import Counter

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'fft_qbasis_research'))
from orbit_kernel import Counted,FFTPlan,KernelPlan,fft_plan,fft,apply as convolution


@dataclass
class FastPlan:
    kernel: KernelPlan
    forward: FFTPlan
    t: list
    inverse_gamma: list
    preparation: dict


def prepare_fast(field,n,eta):
    c=Counted(field)
    padded=fft_plan(c,n,eta)
    factors=[c.sub(c.one,z) for z in padded.powers]
    spectrum=[c.zero]*(2*n)
    # K(z)=(1-z)K(qz)+z^N/N: recurse BACKWARD through each orbit.
    spectrum[0]=padded.inverse_n
    for r in range(n-1,0,-1):
        k=2*r
        spectrum[k]=c.add(c.mul(factors[k],spectrum[(k+2)%(2*n)]),padded.inverse_n)
    b=c.zero
    for r in range(n-1,-1,-1):
        k=2*r+1
        b=c.sub(c.mul(factors[k],b),padded.inverse_n)
    spectrum[1]=c.neg(b)
    for r in range(n-1,0,-1):
        k=2*r+1
        spectrum[k]=c.sub(c.mul(factors[k],spectrum[(k+2)%(2*n)]),padded.inverse_n)
    # t=P^-1, generated backward from t[N-1]=1/N.
    t=[c.zero]*n
    t[-1]=padded.inverse_n
    for j in range(n-1,0,-1):
        t[j-1]=c.mul(factors[2*j],t[j])
    # Gamma^-1[j]=(-1)^j q^(-j(j-1)/2).
    inverse_gamma=[c.one]
    for j in range(n-1):
        inverse_gamma.append(c.neg(c.mul(inverse_gamma[-1],padded.powers[(-2*j)%(2*n)])))
    permutation=[index//2 for index in padded.permutation[:n]]
    forward=FFTPlan(n//2,padded.powers[::2],permutation,padded.inverse_n,padded.inverse_n)
    kernel=KernelPlan(padded,spectrum,{},'inverse-kernel-backward-orbit')
    return FastPlan(kernel,forward,t,inverse_gamma,dict(c.count))


def apply_hc(field,plan,x):
    """H(C)x=P^-1 F_N Gamma^-1 T^-1 x, retaining every output."""
    n=plan.kernel.fft.n
    z,detail=convolution(field,plan.kernel,x)
    c=Counted(field)
    z=[c.mul(a,b) for a,b in zip(plan.inverse_gamma,z)]
    traffic=Counter(detail['array_traffic'])
    z=fft(c,plan.forward,z,traffic=traffic)
    y=[c.mul(a,b) for a,b in zip(plan.t,z)]
    traffic['outer_diagonal_value_reads']+=4*n
    traffic['outer_diagonal_value_writes']+=2*n
    count=Counter(detail['field_operations'])
    count.update(c.count)
    return y,dict(field_operations=dict(count),logical_array_traffic=dict(traffic))


def expected_preparation(n):
    l=n.bit_length()-1
    return dict(mul=7*n+l-4,sub=4*n-1,add=n-1,neg=n,constant_inverse=1)


def expected_online(n):
    l=n.bit_length()-1
    return dict(mul=5*n*l//2+8*n,add=5*n*l//2+2*n,sub=5*n*l//2+2*n)


def fused_fourier(field,plan,x):
    """Compile P*H(C)*T*Gamma algebraically before evaluation: ordinary F_N.

This routine uses the already supplied plan; its count excludes that plan's
preparation. A compiler starting from the fused expression can prepare only an
ordinary length-N FFT plan and need not construct any convolution spectra.
"""
    c=Counted(field)
    out=fft(c,plan.forward,x)
    return out,dict(c.count)
