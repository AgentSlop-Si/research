"""Hero #17 -- independently recognizable sparse polyphase fibers.

For N=Q*M and Q^2 <= C*N, write j=t+Q*u. If each raw fiber
x[t+Q*u] contains at most r distinct length-M characters,
exact O_r(N) recognition and all-N DFT evaluation follow. The
frequencies may differ arbitrarily between fibers, and the ordinary
Q-by-M matrix may have full rank. No full FFT is hidden.

This mechanism works without gcd(Q,M)=1, including N=2^(2m).
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isqrt
from typing import Optional, Sequence
import phase_union_general as phase
from fast_vandermonde import solve_moments


@dataclass
class FiberCertificate:
    n:int
    q:int
    m:int
    p:int
    omega:int
    bound:int
    modes:list[tuple[tuple[int,int], ...]]
    total_modes:int


def choose_q(n:int)->int:
    """Largest divisor of N not exceeding sqrt N in O(sqrt N) word work."""
    for q in range(isqrt(n),0,-1):
        if n%q==0:return q
    return 1


def _direct_modes(y:Sequence[int],p:int,roots:Sequence[int],max_modes:int):
    m=len(y)
    inv_m=pow(m,-1,p)
    spec=[sum(v*roots[(-j*k)%m] for j,v in enumerate(y))%p for k in range(m)]
    found=tuple((k,z*inv_m%p) for k,z in enumerate(spec) if z)
    return found if len(found)<=max_modes else None



def _solve_modes_fast(y:Sequence[int],roots:Sequence[int],p:int,r:int):
    """All operations charged: O(r*M+r^2) per length-M fiber.

    Completeness for distinct character sums when M>=3r follows from BM.
    Full row verification protects against accidental recurrence fits.
    """
    recurrence=phase.bounded_bm(y,p,r)
    if recurrence is None:return None
    order=len(recurrence)-1
    if order==0:
        return () if all(z%p==0 for z in y) else None
    found=[]
    reversed_rec=list(reversed(recurrence))
    for b,z in enumerate(roots):
        if phase.evaluate_poly(reversed_rec,z,p)==0:
            found.append((b,z))
    if len(found)!=order:return None
    weights=solve_moments([z for _,z in found],y,p)
    if weights is None or any(w==0 for w in weights):return None
    powers=[1]*order
    for val in y:
        if (sum(c*z for c,z in zip(weights,powers))-val)%p:
            return None
        for j,(_,root) in enumerate(found):
            powers[j]=powers[j]*root%p
    return tuple((b,c) for (b,_),c in zip(found,weights))


def recognize(x:Sequence[int],p:int,omega:int,r:int=2,q:Optional[int]=None,ratio:int=4)->Optional[FiberCertificate]:
    """O_r(N) bounded-fiber Fourier character recognition.

    No oracle frequencies or producer-side metadata. The input is raw.
    ratio is fixed model constant, typically 1 or 4; reject too-large Q.
    """
    n=len(x)
    if n<1 or r<1 or ratio<1:raise ValueError('N>=1,r>=1,ratio>=1 required')
    q=choose_q(n) if q is None else q
    if q<1 or n%q or q*q>ratio*n:
        raise ValueError('Q must divide N and Q^2 <= ratio*N')
    full_roots=phase.phase_table(n,p,omega)
    m=n//q
    sub_roots=phase.phase_table(m,p,full_roots[q%n])
    modes=[]
    for t in range(q):
        y=[x[t+q*u]%p for u in range(m)]
        if m<3*r:
            found=_direct_modes(y,p,sub_roots,r)
        else:
            found=_solve_modes_fast(y,sub_roots,p,r)
        if found is None:return None
        modes.append(found)
    return FiberCertificate(n,q,m,p,omega,r,modes,sum(map(len,modes)))


def transform_certified(cert:FiberCertificate)->list[int]:
    """O(r*Q^2+N) explicit DFT; works for arbitrary character indices."""
    n,q,m,p=cert.n,cert.q,cert.m,cert.p
    roots=phase.phase_table(n,p,cert.omega)
    spectrum=[0]*n
    for t,row in enumerate(cert.modes):
        for h,c in row:
            for s in range(q):
                k=h+m*s
                spectrum[k]=(spectrum[k]+m*c*roots[(-k*t)%n])%p
    return spectrum


def transform_if_recognized(x:Sequence[int],p:int,omega:int,r:int=2,q:Optional[int]=None,ratio:int=4):
    cert=recognize(x,p,omega,r,q,ratio)
    return (None,None) if cert is None else (transform_certified(cert),cert)


def make_fiber_signal(n:int,p:int,omega:int,q:int,
                      modes:Sequence[Sequence[tuple[int,int]]]):
    """Test-only builder. Each row t has its own independent frequencies."""
    if n%q or len(modes)!=q:raise ValueError('Need N multiple of Q and Q mode lists')
    m=n//q
    roots=phase.phase_table(m,p,pow(omega,q,p))
    x=[0]*n
    for t in range(q):
        for u in range(m):
            x[t+q*u]=sum(c*roots[(h*u)%m] for h,c in modes[t])%p
    return x
