"""Phase 6: fully charged four-leg Fourier tensor and endpoint-gauge rigidity.

Research-only exact field computations; no sub-FFT algorithm is claimed.
N = Q*M, x[t+Q*u], X[h+M*s].
T[s,h,t,u] = omega^(-h*t) * eta^(-h*u) * xi^(-s*t).
"""
from __future__ import annotations
from math import gcd
from typing import Sequence


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d*d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def prime_factors(n: int) -> list[int]:
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def field_for_length(n: int) -> tuple[int, int]:
    """Find a small prime field with a primitive n-th root, for testing only."""
    for mult in range(1, 10000):
        p = mult*n + 1
        if not is_prime(p):
            continue
        pf = prime_factors(n)
        for generator in range(2, p):
            omega = pow(generator, (p-1)//n, p)
            if pow(omega, n, p) == 1 and all(pow(omega,n//d,p) != 1 for d in pf):
                return p,omega
    raise RuntimeError('field not found')


def matmul(A: Sequence[Sequence[int]],B: Sequence[Sequence[int]],p:int) -> list[list[int]]:
    if not A:
        return []
    assert B and len(A[0]) == len(B)
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))%p
             for j in range(len(B[0]))] for i in range(len(A))]


def identity(n:int)->list[list[int]]:
    return [[int(i==j) for j in range(n)] for i in range(n)]


def rank_mod(M: Sequence[Sequence[int]],p:int) -> int:
    if not M:
        return 0
    a = [[x%p for x in row] for row in M]
    R,C=len(a),len(a[0]); j=0
    for col in range(C):
        piv=next((i for i in range(j,R) if a[i][col]),None)
        if piv is None:
            continue
        a[j],a[piv]=a[piv],a[j]
        iv=pow(a[j][col],-1,p)
        a[j][col:]=[z*iv%p for z in a[j][col:]]
        for row in range(j+1,R):
            v=a[row][col]
            if v:
                for k in range(col,C):
                    a[row][k]=(a[row][k]-v*a[j][k])%p
        j+=1
        if j==R:
            break
    return j


def invert_mod(M:Sequence[Sequence[int]],p:int)->list[list[int]]:
    n=len(M)
    assert all(len(row)==n for row in M)
    a=[[z%p for z in row]+identity(n)[i] for i,row in enumerate(M)]
    for col in range(n):
        piv=next((i for i in range(col,n) if a[i][col]),None)
        if piv is None:
            raise ValueError('singular')
        a[piv],a[col]=a[col],a[piv]
        iv=pow(a[col][col],-1,p)
        for j in range(col,2*n):
            a[col][j]=a[col][j]*iv%p
        for i in range(n):
            if i==col:
                continue
            c=a[i][col]
            if c:
                for j in range(col,2*n):
                    a[i][j]=(a[i][j]-c*a[col][j])%p
    return [row[n:] for row in a]


def dft_matrix(n:int,root:int,p:int,sign:int=-1)->list[list[int]]:
    return [[pow(root, (sign*i*j)%n,p) for j in range(n)] for i in range(n)]


def fourier_tensor(q:int,m:int,p:int,omega:int)->list[list[list[list[int]]]]:
    n=q*m
    assert pow(omega,n,p)==1
    eta=pow(omega,q,p);xi=pow(omega,m,p)
    return [[[[pow(omega,(-h*t)%n,p)*pow(eta,(-h*u)%m,p)*pow(xi,(-s*t)%q,p)%p
               for u in range(m)] for t in range(q)] for h in range(m)] for s in range(q)]


def flatten(T:list,which:str)->list[list[int]]:
    q=len(T);m=len(T[0]);
    if which=='output_input':
        return [[T[s][h][t][u] for t in range(q) for u in range(m)]
                for s in range(q) for h in range(m)]
    if which=='crossed':
        return [[T[s][h][t][u] for h in range(m) for u in range(m)]
                for s in range(q) for t in range(q)]
    if which=='alternating':
        return [[T[s][h][t][u] for h in range(m) for t in range(q)]
                for s in range(q) for u in range(m)]
    raise ValueError(which)


def cut_ranks(q:int,m:int,p:int,omega:int)->dict[str,int]:
    T=fourier_tensor(q,m,p,omega)
    return {k:rank_mod(flatten(T,k),p) for k in ('output_input','crossed','alternating')}


def transform_legs(T:list,maps:dict[str,list[list[int]]],p:int)->list:
    """Independent invertible linear changes on any of the 4 external legs.

    T has axes s,h,t,u. This is deliberately straightforward O(N^2 * sum(dims))
    to audit invariants, NOT a fast executor.
    """
    import numpy as np
    arr=np.array(T,dtype='int64')
    order=('s','h','t','u')
    for axis,name in enumerate(order):
        if name not in maps:
            continue
        A=np.array(maps[name],dtype='int64')
        assert A.shape==(arr.shape[axis],arr.shape[axis])
        # move selected index to front, multiply, restore
        arr=np.moveaxis(arr,axis,0)
        arr=np.tensordot(A,arr,axes=(1,0))%p
        arr=np.moveaxis(arr,0,axis)
    return arr.tolist()


def random_invertible(n:int,p:int,rng)->list[list[int]]:
    for _ in range(100):
        A=[[rng.randrange(p) for _ in range(n)] for _ in range(n)]
        if rank_mod(A,p)==n:
            return A
    raise RuntimeError('random GL sample failed')


def nnz(M:Sequence[Sequence[int]])->int:
    return sum(int(x!=0) for row in M for x in row)


def endpoint_gauges(q:int,m:int,p:int,omega:int,A:list[list[int]],B:list[list[int]]):
    """A acts on output digit s; B acts on input digit u (as tensor coordinate).

    Core[a,h,t,b] = (A F_q)[a,t] * omega^(-h*t) *
                    (F_m B^T)[h,b].
    """
    eta=pow(omega,q,p);xi=pow(omega,m,p)
    Fq=dft_matrix(q,xi,p)
    Fm=dft_matrix(m,eta,p)
    P=matmul(A,Fq,p)
    R=matmul(Fm,[[B[i][j] for i in range(m)] for j in range(m)],p)
    N=q*m
    tensor=[[[[P[a][t]*pow(omega,(-h*t)%N,p)*R[h][b]%p for b in range(m)]
                 for t in range(q)] for h in range(m)] for a in range(q)]
    return tensor,P,R


def endpoint_sparse_core(q:int,m:int,p:int,omega:int):
    """The endpoint bases are inverse Fourier transforms up to diagonal/perm."""
    eta=pow(omega,q,p);xi=pow(omega,m,p)
    A=[[pow(xi,(a*s)%q,p)*pow(q,-1,p)%p for s in range(q)] for a in range(q)]
    B=[[pow(eta,(b*u)%m,p)*pow(m,-1,p)%p for u in range(m)] for b in range(m)]
    core,P,R=endpoint_gauges(q,m,p,omega,A,B)
    assert P==identity(q) and R==identity(m)
    return A,B,core


def exact_dft(x:Sequence[int],p:int,omega:int)->list[int]:
    n=len(x)
    pw=[1]*n
    for j in range(1,n):
        pw[j]=pw[j-1]*omega%p
    return [sum(x[j]*pw[(-k*j)%n] for j in range(n))%p for k in range(n)]


def prepared_powers(n:int,omega:int,p:int)->tuple[list[int],int]:
    """Fully charge the input-independent Nth-root table: n-1 multiplies."""
    roots=[1]*n
    for i in range(1,n):
        roots[i]=roots[i-1]*omega%p
    # Root order is part of the supplied input contract, not re-discovered online.
    return roots,n-1


def fft_radix2_prepared(a:Sequence[int],roots:Sequence[int],p:int)->tuple[list[int],int]:
    """Standard DIT with all roots fetched from the charged global O(N) table.

    The input length n must divide the prepared root table length N, and n is
    a power of 2. Every butterfly is two adds and one scalar multiplication.
    """
    n=len(a);N=len(roots)
    if n<=0 or n&(n-1) or N%n:
        raise ValueError('length must be power of 2 and divide root-table length')
    if n==1:
        return [a[0]%p],0
    ev,be=fft_radix2_prepared(a[::2],roots,p)
    od,bo=fft_radix2_prepared(a[1::2],roots,p)
    ans=[0]*n
    stride=N//n
    for k in range(n//2):
        z=od[k]*roots[(-k*stride)%N]%p
        ans[k]=(ev[k]+z)%p
        ans[k+n//2]=(ev[k]-z)%p
    return ans,be+bo+n//2


def charged_two_axis_fft(x:Sequence[int],q:int,m:int,p:int,omega:int)->tuple[list[int],dict]:
    """Exactly accounted classical Cooley-Tukey implementation (NOT a faster FFT).

    Supplied primitive Nth root omega. Roots generated in N-1 multiplications,
    no pow() or field inversions in any DFT/cross-twiddle inner loop.
    """
    if len(x)!=q*m or q<=0 or m<=0 or (q&(q-1)) or (m&(m-1)):
        raise ValueError('power-of-2 factors required')
    n=q*m
    roots,root_muls=prepared_powers(n,omega,p)
    C=[];butterflies=0
    for t in range(q):
        spectrum,b=fft_radix2_prepared([x[t+q*u] for u in range(m)],roots,p)
        C.append(spectrum);butterflies+=b
    out=[0]*n
    for h in range(m):
        temp=[C[t][h]*roots[(-h*t)%n]%p for t in range(q)]
        freq,b=fft_radix2_prepared(temp,roots,p);butterflies+=b
        for s in range(q):
            out[h+m*s]=freq[s]
    return out,{'butterflies':butterflies,
                'butterfly_multiplies':butterflies,
                'butterfly_addsubs':2*butterflies,
                'cross_twiddle_multiplies':n,
                'root_table_multiplies':root_muls,
                'field_multiplies_total':butterflies+n+root_muls,
                'field_addsubs_total':2*butterflies,
                'scalar_arithmetic_total':3*butterflies+n+root_muls,
                'root_table_storage':n,
                'input_output_words':2*n,
                'expected_butterflies':n*(q.bit_length()+m.bit_length()-2)//2}

def crossed_partial_fourier(q:int,m:int,p:int,omega:int)->list[list[int]]:
    return [[pow(omega,(-h*t)%(q*m),p) for h in range(m)] for t in range(q)]


def unitary_cut_singular_values(q:int,m:int):
    """Independent floating SVD to validate exact complex singular-spectrum lemma."""
    import numpy as np
    n=q*m
    s=np.arange(q).reshape(q,1,1,1)
    h=np.arange(m).reshape(1,m,1,1)
    t=np.arange(q).reshape(1,1,q,1)
    u=np.arange(m).reshape(1,1,1,m)
    T=np.exp(-2j*np.pi*(h*t/n+h*u/m+s*t/q))/np.sqrt(n)
    # flatten crossed (s,t) | (h,u)
    cross=np.transpose(T,(0,2,1,3)).reshape(q*q,m*m)
    alternative=np.transpose(T,(0,3,1,2)).reshape(n,n)
    direct=T.reshape(n,n)
    V=np.exp(-2j*np.pi*np.outer(np.arange(q),np.arange(m))/n)
    return {'direct':np.linalg.svd(direct,compute_uv=False),
            'alternative':np.linalg.svd(alternative,compute_uv=False),
            'crossed':np.linalg.svd(cross,compute_uv=False),
            'partial':np.linalg.svd(V,compute_uv=False)}
