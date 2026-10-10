"""Phase-Union on automatically discovered affine cyclic support cosets.

Exact O_r(N) DFT for raw signals supported on one coset (mod d),
whose length-(N/d) subsequence is bounded-rank quadratic dephased.
Also handles support-coset size <3r by direct short evaluation.
This extends the bounded-chirp-rank method to gapped/comb data,
including prime powers where CRT coprime splitting is impossible.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import gcd
from typing import Sequence, Optional
import sys
from pathlib import Path
# Bundled copy of verified prior module is located alongside this script.
try:
    import phase_union_general as phase
except ImportError as exc:
    raise ImportError('phase_union_general.py must accompany coset_union.py') from exc


@dataclass
class CosetCertificate:
    n:int
    p:int
    omega:int
    offset:int
    step:int
    reduced_length:int
    bound:int
    spectrum_reduced:list[int]
    chirp_certificate:object | None
    branch:str


def support_gcd(x:Sequence[int],p:int)->tuple[int,int]:
    """Return maximal affine subgroup coset containing all nonzero indices.

    Unit word comparisons/mod at each scanned sample, only O(log N)
    nontrivial gcd reductions because the divisor strictly decreases.
    For x=0 return (0, N).
    """
    n=len(x)
    first=next((i for i,z in enumerate(x) if z%p),None)
    if first is None:return 0,n
    d=n
    for i in range(first+1,n):
        if x[i]%p:
            diff=i-first
            if diff%d:
                d=gcd(d,diff)
    return first%d,d


def recognize_and_transform(x:Sequence[int],p:int,omega:int,r:int=2)->tuple[Optional[list[int]],Optional[CosetCertificate]]:
    """Return exact dense DFT if raw input belongs to support-coset family."""
    n=len(x)
    if n==0 or r<1:raise ValueError('Need nonempty input and rank bound r>=1')
    roots=phase.phase_table(n,p,omega)
    off,d=support_gcd(x,p)
    m=n//d
    if all(z%p==0 for z in x):
        cert=CosetCertificate(n,p,omega,0,n,1,r,[0],None,'zero')
        return [0]*n,cert
    values=[x[off+d*j]%p for j in range(m)]
    reduced_root=roots[d%n]
    if m < 3*r:
        # For fixed r, O(m^2) = O_r(1); no chirp promise required.
        rm=[sum(v*pow(reduced_root,(-j*k)%m,p) for j,v in enumerate(values))%p for k in range(m)]
        chirp=None
        branch='short-coset'
    else:
        chirp=phase.recognize(values,p,reduced_root,r)
        if chirp is None:return None,None
        rm=phase.transform_certified(chirp)
        branch='phase-coset'
    spectrum=[roots[(-off*k)%n]*rm[k%m]%p for k in range(n)]
    cert=CosetCertificate(n,p,omega,off,d,m,r,rm,chirp,branch)
    return spectrum,cert
