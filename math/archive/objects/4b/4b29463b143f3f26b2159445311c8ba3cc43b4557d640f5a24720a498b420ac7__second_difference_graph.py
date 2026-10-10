"""Exact second-difference graph-union Fourier transform.

Let y_t[u] = x[t+Q*u], t=0..Q-1, u=0..M-1, N=Q*M.
Both y_0 and y_1 may be completely arbitrary dense M-vectors.
Recognize each acceleration d_t=y_t-2*y_(t-1)+y_(t-2) as a sum
of Fourier characters, with GLOBAL frequency-mode budget R=O(Q).

Then C_t[h]=C_0[h]+t(C_1[h]-C_0[h])
                +M*sum_{j=2}^t sum_{e at j,h} c_e*(t-j+1).
Evaluating geometric sums and arithmetico-geometric sums gives
all N Fourier outputs in O(N+2*M^2+M*(Q+R)+Q*R), with prime-field
scalar arithmetic and prepared primitive root. O(N) when Q,M~sqrt(N),
R=O(Q). If unsupported, returns None in O(N) for balanced sizes.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional,Sequence
import phase_union_general as phase
from delta_graph import (
    balanced_q,direct_row_dft,batch_inverse_nonzero_phase_differences
)
from delta_graph_budget import modes_with_budget


@dataclass(frozen=True)
class AccelerationEvent:
    t:int
    h:int
    c:int


@dataclass(frozen=True)
class AccelerationCertificate:
    n:int
    q:int
    m:int
    p:int
    omega:int
    spectrum_0:tuple[int,...]
    spectrum_1:tuple[int,...]
    events:tuple[AccelerationEvent,...]
    budget:int


def recognize(x:Sequence[int],p:int,omega:int,total_modes:int,
              q:Optional[int]=None,balance_bound:int=4):
    n=len(x)
    if total_modes<0 or n<2 or balance_bound<1:
        raise ValueError('N>=2, total_modes>=0, balance>=1 required')
    q=balanced_q(n,balance_bound) if q is None else q
    if q is None:return None
    if n%q or q<2:raise ValueError('Need Q>=2 dividing N')
    m=n//q
    if q*q>balance_bound*n or m*m>balance_bound*n:
        raise ValueError('not a balanced factorization')
    table=phase.phase_table(n,p,omega)
    subroots=phase.phase_table(m,p,table[q%n])
    x=list(z%p for z in x)
    prev2=tuple(x[q*u] for u in range(m))
    prev1=tuple(x[1+q*u] for u in range(m))
    c0=direct_row_dft(prev2,p,subroots)
    c1=direct_row_dft(prev1,p,subroots)
    events=[];spent=0
    for t in range(2,q):
        row=tuple(x[t+q*u] for u in range(m))
        diff=tuple((row[u]-2*prev1[u]+prev2[u])%p for u in range(m))
        modes=modes_with_budget(diff,subroots,p,total_modes-spent)
        if modes is None:return None
        for h,c in modes:events.append(AccelerationEvent(t,h,c))
        spent+=len(modes)
        prev2,prev1=prev1,row
    return AccelerationCertificate(n,q,m,p,omega,c0,c1,tuple(events),total_modes)


def transform_certified(cert:AccelerationCertificate,with_counters=False):
    n,q,m,p=cert.n,cert.q,cert.m,cert.p
    tab=phase.phase_table(n,p,cert.omega)
    inv=batch_inverse_nonzero_phase_differences(tab,p)
    output=[0]*n
    initial_updates=0
    event_updates=0
    for h in range(m):
        c0=cert.spectrum_0[h]
        slope=(cert.spectrum_1[h]-c0)%p
        for s in range(q):
            k=h+m*s
            if k==0:
                S0=q
                S1=q*(q-1)//2
            else:
                z=tab[-k]
                zq=tab[(-k*q)%n]
                inv1=inv[k]
                inv2=inv1*inv1%p
                S0=(1-zq)*inv1%p
                S1=(z-q*zq+(q-1)*z*zq)*inv2%p
            output[k]=(c0*S0+slope*S1)%p
            initial_updates+=1
    for e in cert.events:
        L=q-e.t
        for s in range(q):
            k=e.h+m*s
            if k==0:
                H=L*(L+1)//2
            else:
                z=tab[-k]
                zL=tab[(-k*L)%n]
                # z^t * [sum_{v=0}^{L-1}(v+1)*z^v]
                numerator=1-(L+1)*zL+L*zL*z
                H=tab[(-k*e.t)%n]*numerator*inv[k]*inv[k]%p
            output[k]=(output[k]+m*e.c*H)%p
            event_updates+=1
    if with_counters:
        return output,dict(n=n,q=q,m=m,initial_updates=initial_updates,
                          event_updates=event_updates,events=len(cert.events),
                          baseline_dft_direct_ops=2*m*m)
    return output


def transform_if_recognized(x,p,omega,total_modes:int,q=None,balance_bound:int=4):
    cert=recognize(x,p,omega,total_modes,q,balance_bound)
    return (None,None) if cert is None else (transform_certified(cert),cert)


def make_acceleration_signal(n:int,p:int,omega:int,q:int,
                             row0:Sequence[int],row1:Sequence[int],
                             accelerations:Sequence[Sequence[tuple[int,int]]]):
    """Test-only input generator. Recognition sees only raw vectors."""
    if n%q or q<2 or len(accelerations)!=q:raise ValueError('bad Q')
    m=n//q
    if len(row0)!=m or len(row1)!=m:raise ValueError('bad rows')
    roots=phase.phase_table(m,p,pow(omega,q,p))
    x=[0]*n
    prev2=[z%p for z in row0]
    prev1=[z%p for z in row1]
    for u in range(m):x[q*u]=prev2[u];x[1+q*u]=prev1[u]
    for t in range(2,q):
        row=[(2*prev1[u]-prev2[u]+
             sum(c*roots[(h*u)%m] for h,c in accelerations[t]))%p
             for u in range(m)]
        for u in range(m):x[t+q*u]=row[u]
        prev2,prev1=prev1,row
    return x
