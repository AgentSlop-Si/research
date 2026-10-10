"""Exact Galois-orbit descriptors for fresh integer/rational-input radix-two DFTs.

This constructs an O(N)-size *symbolic descriptor* of the whole Fourier vector.
It does NOT compute N exact complex register values with O(N) operations.
The field F_p tests check identities, not the Galois automorphism claim over Q.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
from cmath import exp
from math import tau


@dataclass(frozen=True)
class FrequencyDescriptor:
    m: int
    u: int
    orbit_index: int


@dataclass
class OrbitDFT:
    n: int
    primitive_coefficients: list[list[int]]
    dc: int
    add_sub_count: int

    @classmethod
    def build(cls, samples: Sequence[int]) -> 'OrbitDFT':
        """Exactly 2(N-1) integer adds/subs, retaining N shared integers."""
        n = len(samples)
        if n < 2 or n & (n-1):
            raise ValueError('length must be power of 2 >= 2')
        a = [int(v) for v in samples]
        levels: list[list[int]] = []
        cost = 0
        while len(a) > 1:
            half = len(a)//2
            r = [a[j]-a[j+half] for j in range(half)]
            a = [a[j]+a[j+half] for j in range(half)]
            levels.append(r)
            cost += 2*half
        assert cost == 2*(n-1)
        return cls(n, levels, a[0], cost)

    def descriptor(self, k:int) -> FrequencyDescriptor | None:
        if k<0 or k>=self.n:raise IndexError(k)
        if k==0:return None
        s=(k&-k).bit_length()-1
        return FrequencyDescriptor(m=self.n>>s,u=k>>s,orbit_index=s)

    def coefficients(self, k:int) -> list[int]:
        """Explicit rational cyclotomic power basis of X_k, O(phi(m)) output."""
        desc=self.descriptor(k)
        if desc is None:return [self.dc]
        m,u=desc.m,desc.u
        half=m//2
        rep=self.primitive_coefficients[desc.orbit_index]
        assert len(rep)==half and u%2==1
        out=[0]*half
        for j,v in enumerate(rep):
            e=(u*j)%m
            if e<half:out[e]+=v
            else:out[e-half]-=v
        # Multiplication by odd u is a signed permutation of cyclotomic basis.
        assert sorted(abs(v) for v in out)==sorted(abs(v) for v in rep)
        return out

    def evaluate_mod(self,k:int,p:int=998244353) -> int:
        """Materialize one scalar modulo a field containing the needed root."""
        desc=self.descriptor(k)
        if desc is None:return self.dc%p
        m=desc.m
        if (p-1)%m:raise ValueError('p has no mth primitive root')
        # 3 generates F_998244353^*; use slower fallback for other p.
        root=pow(3,(p-1)//m,p)
        if pow(root,m//2,p)==1:
            for candidate in range(2,min(p,1024)):
                root=pow(candidate,(p-1)//m,p)
                if pow(root,m//2,p)!=1:break
            else:raise ValueError('primitive root not located')
        coeff=self.coefficients(k)
        acc=0
        w=1
        for v in coeff:
            acc=(acc+v*w)%p
            w=w*root%p
        return acc

    def evaluate_complex(self, k: int) -> complex:
        """One numerical complex value, NOT an O(1) descriptor materialization."""
        desc=self.descriptor(k)
        if desc is None:return complex(self.dc)
        m=desc.m
        omega=exp(1j*tau/m)
        return sum(c*omega**j for j,c in enumerate(self.coefficients(k)))

    def representative_bins_mod(self,p:int=998244353)->dict[int,int]:
        """Only {0,1,2,4,...,N/2}, with O(N) arithmetic overall."""
        return {**{0:self.dc%p}, **{1<<s:self.evaluate_mod(1<<s,p)
                    for s in range(len(self.primitive_coefficients))}}

    @property
    def stored_coefficients(self)->int:
        return 1+sum(len(s) for s in self.primitive_coefficients)

    @property
    def expanded_coefficients(self)->int:
        """If *all* N spectra were emitted as explicit cyclotomic arrays."""
        # Each level m has phi(m)=m/2 frequencies and phi(m) basis coeffs.
        return 1+sum(len(s)**2 for s in self.primitive_coefficients)

    def expected_expanded(self)->int:
        return (self.n*self.n+2)//3


def reference_dft_mod(x:Sequence[int],p:int=998244353)->list[int]:
    n=len(x)
    if (p-1)%n:raise ValueError
    w=pow(3,(p-1)//n,p)
    return [sum(int(v)*pow(w,k*j,p) for j,v in enumerate(x))%p
            for k in range(n)]
