"""Exact rank-at-most-r q-Weyl polynomial tails by shared block FFTs.

Computes C**(N-r) p(C) x, deg(p)<r, in O(N log(r+1)) total field work.
This does not apply all of H_q(C) sub-N-log-N, and is not a novelty claim.
"""
import sys
from pathlib import Path
from collections import Counter
from dataclasses import dataclass

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'fft_qbasis_research'))
from orbit_kernel import FFTPlan,fft
sys.path.insert(0,str(ROOT/'fft_qweyl_boundary_research'))
from fixed_kernel import Counted,prepare


@dataclass
class TailPlan:
    n: int
    r: int
    q: object
    polynomial: list
    kernel: object
    fft: FFTPlan
    projection_spectra: list
    decoding_spectra: list
    middle_spectrum: list
    g_tail: list
    inverse_g_head: list
    preparation: dict


def _window(field,kernel,center,r):
    """2r cyclic embedding of the r-by-r Toeplitz window kernel[center+i-j]."""
    out=[field.zero]*(2*r)
    for offset in range(r):
        index=center+offset
        if 0<=index<len(kernel):
            out[offset]=kernel[index]
    for distance in range(1,r):
        index=center-distance
        if 0<=index<len(kernel):
            out[2*r-distance]=kernel[index]
    return out


def prepare_tail(field,n,r,q,polynomial=None):
    if n<2 or n&(n-1) or r<1 or r&(r-1) or 2*r>n:
        raise ValueError('N and r powers of two, 1<=r<=N/2 required')
    kernel=prepare(field,n,q)
    if polynomial is None:
        polynomial=list(kernel.kernel[n-r:])
    else:
        if not polynomial or len(polynomial)>r:
            raise ValueError('polynomial must have 1..r coefficients')
        polynomial=list(polynomial)+[field.zero]*(r-len(polynomial))
    c=Counted(field)
    roots=[field.one]
    for _ in range(1,n):
        roots.append(c.mul(roots[-1],q))
    # g_j=product_(a=0)^(j-1)(q-q^(-a)); 1/g_j is kernel.middle[j].
    g=[field.one]
    for j in range(n-1):
        g.append(c.mul(g[-1],c.sub(q,roots[(-j)%n])))
    m=2*r
    powers=[roots[j*(n//m)] for j in range(m)]
    permutation=[0]
    while len(permutation)<m:
        doubled=[2*j for j in permutation]
        permutation=doubled+[j+1 for j in doubled]
    # 1/(2r) = (N/(2r))*(1/N), without a second field inversion.
    multiplier=field.one
    for _ in range((n//m).bit_length()-1):
        multiplier=c.add(multiplier,multiplier)
    inverse_length=c.mul(multiplier,kernel.kernel[-1])
    plan=FFTPlan(r,powers,permutation,inverse_length,inverse_length)
    blocks=n//r
    projection=[]
    decoding=[]
    for b in range(blocks):
        projection.append(fft(c,plan,_window(field,kernel.middle,(blocks-1-b)*r,r)))
        decoding.append(fft(c,plan,_window(field,kernel.kernel,b*r,r)))
    upper=[field.zero]*m
    upper[0]=polynomial[0]
    for j in range(1,r):
        upper[m-j]=polynomial[j]
    middle=fft(c,plan,upper)
    count=Counter(kernel.preparation)
    count.update(c.count)
    return TailPlan(n,r,q,polynomial,kernel,plan,projection,decoding,middle,
                    g[n-r:],kernel.middle[:r],dict(count))


def apply_tail(field,plan,x):
    if len(x)!=plan.n:
        raise ValueError('wrong input length')
    n,r=plan.n,plan.r
    m=2*r
    blocks=n//r
    c=Counted(field)
    aggregate=None
    # Every block contributes to the same r projected outputs, allowing a
    # frequency-domain sum and only ONE inverse FFT for the whole projection.
    for b in range(blocks):
        transformed=fft(c,plan.fft,list(x[b*r:(b+1)*r])+[field.zero]*r)
        product=[c.mul(a,v) for a,v in zip(plan.projection_spectra[b],transformed)]
        if aggregate is None:
            aggregate=product
        else:
            aggregate=[c.add(a,v) for a,v in zip(aggregate,product)]
    projected=fft(c,plan.fft,aggregate,inverse=True)[:r]
    middle_input=[c.mul(a,v) for a,v in zip(plan.g_tail,projected)]
    middle_input=fft(c,plan.fft,middle_input+[field.zero]*r)
    middle_product=[c.mul(a,v) for a,v in zip(plan.middle_spectrum,middle_input)]
    middle_output=fft(c,plan.fft,middle_product,inverse=True)[:r]
    small_state=[c.mul(a,v) for a,v in zip(plan.inverse_g_head,middle_output)]
    # One forward FFT of the r-state serves every one of the N/r output blocks.
    small_spectrum=fft(c,plan.fft,small_state+[field.zero]*r)
    out=[]
    for b in range(blocks):
        product=[c.mul(a,v) for a,v in zip(plan.decoding_spectra[b],small_spectrum)]
        out.extend(fft(c,plan.fft,product,inverse=True)[:r])
    return out,dict(field_operations=dict(c.count),
        forward_ffts=blocks+2,inverse_ffts=blocks+2,fft_length=m,
        source_input_reads=n,returned_output_count=n,full_output_writes=n,
        projection_state_length=r,decoding_state_length=r,
        logical_fft_input_value_volume=(2*blocks+4)*m,
        logical_fft_butterflies=(2*n+4*r)*(m.bit_length()-1),
        model='Exact field arithmetic with supplied primitive N-th root; logical arrays and word indexing')


def expected_online(n,r):
    s=(2*r).bit_length()-1
    fft_term=(2*n+4*r)*s
    return dict(mul=fft_term+6*n+8*r,add=fft_term+2*n-2*r,sub=fft_term)


def expected_preparation(n,r):
    l=n.bit_length()-1
    s=(2*r).bit_length()-1
    butterflies=(2*n+r)*s
    return dict(mul=8*n+l-5+butterflies,sub=2*n-2+butterflies,
                add=(l-s)+butterflies,neg=n-1,constant_inverse=1)
