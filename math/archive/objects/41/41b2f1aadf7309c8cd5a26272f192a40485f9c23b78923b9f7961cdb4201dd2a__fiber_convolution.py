"""Hero #17 -- exact convolution by frequency-graph union.

Precondition: two full-length raw sequences admit per-fiber sparse Fourier
certificates for the same N=QM. Their zero/nonzero character labels h
are discovered, not supplied. Matching labels form a bipartite graph.

For each edge (t1,h,c1)--(t2,h,c2), convolution contributes precisely
    M c1 c2 eta^(-h*carry)
into partial Fourier coefficient (t=(t1+t2)%Q,h), where
carry=floor((t1+t2)/Q) in {0,1}.

All edges are examined in O(r1*r2*Q^2) <= O_r(N) when Q^2=O(N).
After union/aggregation into S_z nonzero target (t,h) cells,
reconstructing the explicit N-vector takes O(N+M*S_z).

Thus when S_z=O(Q), the whole raw-input convolution is exact O_r(N)
even if both source Q-by-M matrices have full rank.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from fiber_union import FiberCertificate, recognize as recognize_fiber
import phase_union_general as phase


@dataclass
class ConvolutionGraphCertificate:
    n:int
    q:int
    m:int
    p:int
    omega:int
    input_modes_x:int
    input_modes_y:int
    matching_edges:int
    union_states:int
    # materialized partial Fourier support (t, h, coefficient)
    states:list[tuple[int,int,int]]


def union_and_convolve(c1:FiberCertificate,c2:FiberCertificate,
                       max_states_ratio:int=2):
    """Return (convolution,certificate) or (None, certificate for rejection).

    max_states_ratio is a fixed constant, requiring S_z<=ratio*Q.
    All work before rejection is O_r(N) in the balanced Q model.
    """
    if (c1.n,c1.q,c1.m,c1.p,c1.omega)!=(c2.n,c2.q,c2.m,c2.p,c2.omega):
        raise ValueError('certificates must use same N,Q,M,p,root')
    n,q,m,p=c1.n,c1.q,c1.m,c1.p
    if max_states_ratio<1:raise ValueError('state ratio must be >=1')
    eta=pow(c1.omega,q,p)
    sub_roots=phase.phase_table(m,p,eta)
    buckets=[[] for _ in range(m)]
    for t,row in enumerate(c1.modes):
        for h,c in row:buckets[h].append((t,c))
    states=[0]*n  # index=t*m+h
    active=[]
    edges=0
    for t2,row in enumerate(c2.modes):
        for h,c2val in row:
            for t1,c1val in buckets[h]:
                edges+=1
                summed=t1+t2
                t=summed%q
                carry=1 if summed>=q else 0
                w=m*c1val*c2val*sub_roots[(-h*carry)%m]%p
                index=t*m+h
                if states[index]==0:
                    active.append(index)
                states[index]=(states[index]+w)%p
    # Correct duplicate bookkeeping: active may repeat if coefficient
    # cancels to zero and a later edge revives the same (t,h) slot.
    # Since a slot appears at most once after dedup, deterministic O(N) marker.
    seen=[False]*n
    support=[]
    for idx in active:
        if not seen[idx]:
            seen[idx]=True
            if states[idx]:support.append((idx//m,idx%m,states[idx]))
    proof=ConvolutionGraphCertificate(n,q,m,p,c1.omega,c1.total_modes,
            c2.total_modes,edges,len(support),support)
    if len(support)>max_states_ratio*q:return None,proof
    out=[0]*n
    for t,h,c in support:
        for u in range(m):
            index=t+q*u
            out[index]=(out[index]+c*sub_roots[(h*u)%m])%p
    return out,proof


def convolve_if_supported(x,y,p:int,omega:int,r_x:int=2,r_y:int=2,
                          q:Optional[int]=None,max_states_ratio:int=2):
    if len(x)!=len(y):raise ValueError('Both inputs must have same length')
    cx=recognize_fiber(x,p,omega,r_x,q)
    if cx is None:return None,None
    cy=recognize_fiber(y,p,omega,r_y,q)
    if cy is None:return None,None
    return union_and_convolve(cx,cy,max_states_ratio)
