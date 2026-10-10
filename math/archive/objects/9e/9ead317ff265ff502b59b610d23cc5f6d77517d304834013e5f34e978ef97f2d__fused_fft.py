"""Hero #17 exact input-adaptive FFT (structured modes, no arbitrary-input speedup).

Branches:
  1) balanced coprime CRT rank-r tensor recognition (any factor vectors),
  2) bounded per-fiber Fourier-sparse recognition (any N=Q*M),
  3) automatic support-coset dephased rank-r phase recognition.
All graph/recognition/transformation time charged; fixed r gives O(N).
Unrecognized arbitrary vectors require an ordinary NTT/FFT fallback.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
from tensor_union import coprime_split, recognize as tensor_recognize, transform_certified
from coset_union import recognize_and_transform as coset_transform
from fiber_union import transform_if_recognized as fiber_transform

@dataclass
class FusionResult:
    spectrum:list[int]
    branch:str
    rank:int
    certificate:object


def transform_if_supported(x:Sequence[int],p:int,omega:int,r:int=2):
    n=len(x)
    factors=coprime_split(n)
    if factors is not None:
        a,b=factors
        # Guarantee A^2+B^2 <= 4N for the direct short transforms.
        if a*a+b*b <= 4*n:
            cert=tensor_recognize(x,p,omega,r,factors)
            if cert is not None:
                return FusionResult(transform_certified(cert),'tensor-crt',cert.rank,cert)
    fiber_output,fiber_cert=fiber_transform(x,p,omega,r)
    if fiber_cert is not None:
        return FusionResult(fiber_output,'fiber-union',max((len(row) for row in fiber_cert.modes),default=0),fiber_cert)
    output,cert=coset_transform(x,p,omega,r)
    if cert is not None:
        rank = len(cert.chirp_certificate.modes) if cert.chirp_certificate is not None else 0
        return FusionResult(output,cert.branch,rank,cert)
    return None
