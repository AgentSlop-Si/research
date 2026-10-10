"""Augment old frequency-graph convolution with sparse-delta reconstruction.

Previous method rejected if S = number of nonzero (t,h) output states was
large. Here materialize the same graph in O(N), but if the number of
*changes between neighboring spectral rows* is E=O(Q), inverse transform
all rows via one baseline plus sparse updates, in O(N+M^2+M*E).
The convolution graph-edge count is O(r1*r2*Q^2).
No uncounted input/output FFT, no generic dense algebra asserted.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from fiber_union import FiberCertificate, recognize
from fiber_convolution import union_and_convolve
import phase_union_general as phase


@dataclass(frozen=True)
class DeltaConvolutionReport:
    n:int
    graph_edges:int
    nonzero_states:int
    delta_states:int
    method:str
    accepted:bool


def convolve_certified(a:FiberCertificate,b:FiberCertificate,
                      sparse_state_ratio:int=2,delta_ratio:int=2):
    value,report=union_and_convolve(a,b,sparse_state_ratio)
    if value is not None:
        return value,DeltaConvolutionReport(a.n,report.matching_edges,
                       report.union_states,-1,'sparse-state',True)
    if delta_ratio<1:raise ValueError('delta_ratio>=1 required')
    n,q,m,p=a.n,a.q,a.m,a.p
    if m*m>4*n or q*q>4*n:
        raise ValueError('balanced dimensions required')
    state=[[0]*m for _ in range(q)]
    for t,h,c in report.states:
        state[t][h]=c
    differences=[]
    root=[(h,c) for h,c in enumerate(state[0]) if c]
    number_deltas=len(root)
    for t in range(1,q):
        d=[(h,(state[t][h]-state[t-1][h])%p)
           for h in range(m) if state[t][h]!=state[t-1][h]]
        differences.append(d)
        number_deltas+=len(d)
    info=DeltaConvolutionReport(n,report.matching_edges,
               report.union_states,number_deltas,'delta-graph',
               number_deltas<=delta_ratio*q)
    if not info.accepted:return None,info
    eta=pow(a.omega,q,p)
    roots=phase.phase_table(m,p,eta)
    cur=[sum(c*roots[(h*u)%m] for h,c in root)%p for u in range(m)]
    out=[0]*n
    for u,z in enumerate(cur):out[q*u]=z
    for t,d in enumerate(differences,1):
        for u in range(m):
            cur[u]=(cur[u]+sum(c*roots[(h*u)%m] for h,c in d))%p
            out[t+q*u]=cur[u]
    return out,info


def convolve_if_supported(x,y,p:int,omega:int,r_x:int=1,r_y:int=1,
                          q:Optional[int]=None,sparse_state_ratio:int=2,
                          delta_ratio:int=2):
    if len(x)!=len(y):raise ValueError('input size mismatch')
    a=recognize(x,p,omega,r_x,q)
    if a is None:return None,None
    b=recognize(y,p,omega,r_y,q)
    if b is None:return None,None
    return convolve_certified(a,b,sparse_state_ratio,delta_ratio)
