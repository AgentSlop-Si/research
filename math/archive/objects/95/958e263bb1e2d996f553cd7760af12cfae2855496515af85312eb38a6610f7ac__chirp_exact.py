"""An exact finite-field audit of global Fourier/chirp algebra.

All operations take place in F_998244353.  Lengths N are even powers of two
with 2*N | (P-1).  No floating arithmetic, hashing, or cached input results.
This is a research verifier, NOT a faster Fourier transform.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

P = 998244353
GENERATOR = 3


def _ensure_n(n: int) -> None:
    if n < 2 or (n & (n - 1)) or ((P - 1) % (2 * n)):
        raise ValueError("N must be an even power of two with 2N dividing P-1")


@dataclass(frozen=True)
class Chirp:
    n: int
    zeta: int
    omega: int
    h: tuple[int, ...]
    d: tuple[int, ...]
    g: tuple[int, ...]


def make_chirp(n: int) -> Chirp:
    _ensure_n(n)
    z = pow(GENERATOR, (P - 1) // (2 * n), P)
    if pow(z, 2 * n, P) != 1 or pow(z, n, P) != P - 1:
        raise AssertionError("Root must have exact order 2N")
    d = tuple(pow(z, (j * j) % (2 * n), P) for j in range(n))
    h = tuple(pow(t, P - 2, P) for t in d)
    g = tuple(pow(z, (-(2 * k + 1)) % (2 * n), P) for k in range(n))
    return Chirp(n, z, z*z % P, h, d, g)


def dft_direct(x: Sequence[int], omega: int) -> list[int]:
    n = len(x)
    return [sum(int(x[j]) * pow(omega, (j*k) % n, P)
                for j in range(n)) % P for k in range(n)]


def dft_ntt(x: Sequence[int], omega: int, inverse: bool = False) -> list[int]:
    """Independent in-place radix-2 NTT. Positive-exponent forward convention."""
    n = len(x)
    if n == 0 or (n & (n-1)):
        raise ValueError("Input length must be a power of two")
    data = [int(v) % P for v in x]
    j = 0
    for i in range(1,n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            data[i],data[j] = data[j],data[i]
    w = pow(omega, P-2, P) if inverse else omega
    size = 2
    while size <= n:
        step_root = pow(w, n // size, P)
        for start in range(0,n,size):
            phase = 1
            half = size // 2
            for k in range(start,start+half):
                u = data[k]
                v = data[k+half] * phase % P
                data[k] = (u+v) % P
                data[k+half] = (u-v) % P
                phase = phase * step_root % P
        size *= 2
    if inverse:
        inv_n = pow(n, P-2, P)
        data = [v*inv_n % P for v in data]
    return data


def cyclic_convolution(x: Sequence[int],h: Sequence[int]) -> list[int]:
    n=len(x)
    if n!=len(h):
        raise ValueError('Mismatched lengths')
    return [sum(x[j]*h[(k-j)%n] for j in range(n))%P for k in range(n)]


def chirp_dft_direct(x: Sequence[int], c: Chirp) -> list[int]:
    if len(x)!=c.n:
        raise ValueError('Mismatched lengths')
    a=[x[j]*c.d[j]%P for j in range(c.n)]
    b=cyclic_convolution(a,c.h)
    return [b[k]*c.d[k]%P for k in range(c.n)]


def chirp_convolution_from_ntt(x: Sequence[int], c: Chirp) -> list[int]:
    """C_h(x)=D^-1 F_N D^-1 x; makes its hidden FFT explicit."""
    if len(x)!=c.n:
        raise ValueError('Mismatched lengths')
    a=[x[j]*c.h[j]%P for j in range(c.n)]
    b=dft_ntt(a,c.omega)
    return [b[k]*c.h[k]%P for k in range(c.n)]


def variable_filter(y: Sequence[int], c: Chirp) -> list[int]:
    """(Ly)[k]=y[k+1]-zeta^(-2k-1)y[k], indices cyclic."""
    return [(y[(k+1)%c.n]-c.g[k]*y[k])%P for k in range(c.n)]


def modular_rank(matrix: Sequence[Sequence[int]]) -> int:
    if not matrix: return 0
    m=[list(int(v)%P for v in row) for row in matrix]
    cols=len(m[0]);rows=len(m)
    if any(len(row)!=cols for row in m):
        raise ValueError('Ragged matrix')
    rank=0
    for col in range(cols):
        pivot=next((i for i in range(rank,rows) if m[i][col]),None)
        if pivot is None:continue
        m[rank],m[pivot]=m[pivot],m[rank]
        inv=pow(m[rank][col],P-2,P)
        for i in range(rank+1,rows):
            if not m[i][col]:continue
            factor=m[i][col]*inv%P
            # No need to reduce already eliminated columns.
            for j in range(col,cols):
                m[i][j]=(m[i][j]-factor*m[rank][j])%P
        rank+=1
        if rank==rows:break
    return rank


def matrix_c_h(c: Chirp) -> list[list[int]]:
    return [[c.h[(k-j)%c.n] for j in range(c.n)] for k in range(c.n)]


def matrix_lc_h(c: Chirp) -> list[list[int]]:
    return [[(c.h[((k+1)-j)%c.n]-c.g[k]*c.h[(k-j)%c.n])%P
             for j in range(c.n)] for k in range(c.n)]


def moment(x: Sequence[int], c: Chirp, r: int, k: int) -> int:
    n=c.n
    return sum(x[j]*pow(c.omega,(r*j)%n,P)*c.h[(k-j)%n]
               for j in range(n))%P


def moment_matrix(c: Chirp) -> list[list[int]]:
    """M_r(0)=sum_j x_j omega^(rj) h[-j]; independent rows."""
    return [[pow(c.omega,(r*j)%c.n,P)*c.h[(-j)%c.n]%P
             for j in range(c.n)] for r in range(c.n)]


def cyclic_hankel(y: Sequence[int]) -> list[list[int]]:
    n=len(y)
    return [[y[(r+j)%n] for j in range(n)] for r in range(n)]


def predicted_full_spectral_probability(n: int, p: int = P) -> float:
    """For uniform x over F_p^N: Pr(Fx has no zero coordinates)."""
    return (1.0-1.0/p)**n

if __name__=='__main__':
    import json, random
    rng=random.Random(20261009)
    outcome=[]
    for n in (4,8,16,32,64):
        c=make_chirp(n)
        x=[rng.randrange(P) for _ in range(n)]
        y=cyclic_convolution(x,c.h)
        xhat=dft_direct(x,c.omega)
        check=chirp_dft_direct(x,c)
        assert check==xhat==dft_ntt(x,c.omega)
        assert chirp_convolution_from_ntt(x,c)==y
        hhat=dft_ntt(c.h,c.omega)
        gauss=sum(c.h)%P
        assert gauss and all(hhat[k]==gauss*c.d[k]%P for k in range(n))
        assert variable_filter(c.h,c)==[0]*n
        assert all(moment(x,c,r,(k+1)%n) == c.g[k]*moment(x,c,(r+1)%n,k)%P
                   for r in range(n) for k in range(n))
        assert modular_rank(moment_matrix(c))==n
        assert modular_rank(matrix_c_h(c))==n
        rank_lch=modular_rank(matrix_lc_h(c))
        assert rank_lch==n-1
        filt=variable_filter(y,c)
        assert all(filt[k]==sum(matrix_lc_h(c)[k][j]*x[j] for j in range(n))%P for k in range(n))
        nonzeros=sum(v!=0 for v in filt)
        assert modular_rank(cyclic_hankel(y))==sum(bool(v) for v in dft_ntt(y,c.omega))
        outcome.append({'n':n,'gauss_nonzero':True,'rank_chirp':n,'rank_filtered_chirp':rank_lch,'moment_rank':n,
                        'filtered_nonzero':nonzeros,'recurrence_order_periodic':modular_rank(cyclic_hankel(y)),
                        'full_spectral_probability':predicted_full_spectral_probability(n),
                        'modular_butterflies':(n//2)*(n.bit_length()-1),
                        'dense_chirp_products':n*n})
    print(json.dumps(outcome,indent=2))
