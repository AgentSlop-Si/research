"""Hero #17 -- CRT Tensor-Union exact full Fourier transform.

For N=A*B, gcd(A,B)=1, an arbitrary raw input becomes a matrix
M[u,v]=x[CRT(u,v)]. If rank(M)<=r, discover a rank factorization in
O(r*N), compute A and B direct short DFTs in O(r*(A*A+B*B)), then
all N output frequencies in O(r*N). Exact modular prime-field arithmetic.

When A,B=Theta(sqrt(N)) and fixed r, total O(N) field operations,
including input reading, rank discovery and full output materialization.
The routine does NOT claim arbitrary-input faster Fourier transforms.
"""
from dataclasses import dataclass
from math import gcd, isqrt
from typing import Optional, Sequence


@dataclass
class RankCertificate:
    n: int
    a: int
    b: int
    p: int
    omega: int
    rank: int
    max_rank: int
    e_a: int
    e_b: int
    coefficient_rows: list[list[int]]
    basis_rows: list[list[int]]
    # Coefficients alpha[u,t] and normalized basis[t][v]
    # give exactly x[CRT(u,v)] == sum_t alpha[u,t]*basis[t][v].


def coprime_split(n: int) -> Optional[tuple[int,int]]:
    """Find coprime factors with smallest A^2+B^2 in O(sqrt N log N).

    Selects only proper factors (A,B >=2), returns None for prime powers.
    A no-promise case is handled by the fallback (ordinary transform).
    """
    if n < 6:
        return None
    for a in range(isqrt(n),1,-1):
        if n % a == 0:
            b = n // a
            if gcd(a,b) == 1:
                return a,b
    return None


def roots_of_unity(n:int,p:int,omega:int)->list[int]:
    """Check primitive order in O(N); caller must certify p prime."""
    if n<1 or p<=n or omega%p==0:
        raise ValueError('Require N>=1, a prime p>N and nonzero root omega')
    roots=[1]*n
    for i in range(1,n):
        roots[i]=roots[i-1]*omega%p
        if roots[i]==1:
            raise ValueError('root has smaller order than N')
    if roots[-1]*omega%p!=1:
        raise ValueError('root has incorrect order')
    return roots


def crt_idempotents(a:int,b:int)->tuple[int,int]:
    if a < 1 or b < 1 or gcd(a,b)!=1:
        raise ValueError('A and B must be positive coprime')
    n=a*b
    e_a=b*pow(b,-1,a)%n if a>1 else 0
    e_b=a*pow(a,-1,b)%n if b>1 else 0
    assert (e_a+e_b)%n==1%n
    return e_a,e_b


def recognize(x:Sequence[int],p:int,omega:int,max_rank:int=2,
              factors:Optional[tuple[int,int]]=None)->Optional[RankCertificate]:
    """Detect CRT tensor rank and construct verified decomposition.

    When factor pair is balanced and max_rank is fixed, worst-case O(N).
    Assumes p prime and supplied primitive root has order N.
    """
    n=len(x)
    if max_rank<0:
        raise ValueError('max_rank must be >=0')
    root_table=roots_of_unity(n,p,omega)
    del root_table  # validation only, with linear-time overhead
    split=factors if factors is not None else coprime_split(n)
    if split is None:
        return None
    a,b=split
    if a<2 or b<2 or a*b!=n or gcd(a,b)!=1:
        raise ValueError('Need N=A*B with coprime A,B>=2')
    e_a,e_b=crt_idempotents(a,b)
    basis=[]
    pivots=[]
    coeff=[]
    # A row is an arbitrary B-vector, never assumed a chirp/sparse/etc.
    for u in range(a):
        row=[x[(u*e_a+v*e_b)%n]%p for v in range(b)]
        residual=row[:]
        alpha=[]
        for base,pivot in zip(basis,pivots):
            scale=residual[pivot]
            alpha.append(scale)
            if scale:
                for v in range(b):
                    residual[v]=(residual[v]-scale*base[v])%p
        pivot=next((i for i,z in enumerate(residual) if z),None)
        if pivot is not None:
            if len(basis)>=max_rank:
                return None
            factor=residual[pivot]
            inverse=pow(factor,-1,p)
            basis.append([z*inverse%p for z in residual])
            pivots.append(pivot)
            alpha.append(factor)
        coeff.append(alpha)
    r=len(basis)
    for alpha in coeff:
        alpha.extend([0]*(r-len(alpha)))
    return RankCertificate(n,a,b,p,omega,r,max_rank,e_a,e_b,coeff,basis)


def direct_small_dft(values:Sequence[int],p:int,root: int)->list[int]:
    """Deterministic direct transform in m^2 field operations, no FFT."""
    m=len(values)
    table=[1]*m
    for j in range(1,m):table[j]=table[j-1]*root%p
    result=[0]*m
    for k in range(m):
        acc=0
        for j,v in enumerate(values):
            acc += v*table[(-k*j)%m]
        result[k]=acc%p
    return result


def transform_certified(cert:RankCertificate)->list[int]:
    """Exact DFT_N in O(r*(N+A^2+B^2)+N) field work."""
    a,b,n,p,r=cert.a,cert.b,cert.n,cert.p,cert.rank
    omega_a=pow(cert.omega,b,p)
    omega_b=pow(cert.omega,a,p)
    F=[]
    G=[]
    for ell in range(r):
        F.append(direct_small_dft([cert.coefficient_rows[u][ell] for u in range(a)],p,omega_a))
        G.append(direct_small_dft(cert.basis_rows[ell],p,omega_b))
    output=[0]*n
    for s in range(a):
        for t in range(b):
            val=sum(F[ell][s]*G[ell][t] for ell in range(r))%p
            # Ruritanian output indexing (s*B + t*A) mod N.
            output[(s*b+t*a)%n]=val
    return output


def transform_if_recognized(x:Sequence[int],p:int,omega:int,max_rank:int=2,
                            factors:Optional[tuple[int,int]]=None):
    cert=recognize(x,p,omega,max_rank,factors)
    if cert is None:return None,None
    return transform_certified(cert),cert


def direct_dft(x:Sequence[int],p:int,omega:int)->list[int]:
    n=len(x)
    powers=roots_of_unity(n,p,omega)
    return [sum(v*powers[(-k*j)%n] for j,v in enumerate(x))%p for k in range(n)]


def direct_dft_bins(x:Sequence[int],p:int,omega:int,bins:Sequence[int])->list[int]:
    n=len(x)
    powers=roots_of_unity(n,p,omega)
    return [sum(v*powers[(-k*j)%n] for j,v in enumerate(x))%p for k in bins]


def make_low_rank(a:int,b:int,p:int,omega:int,
                 F:Sequence[Sequence[int]],G:Sequence[Sequence[int]])->list[int]:
    """Generate input for testing only; recognition sees only the raw x."""
    if len(F)!=len(G):raise ValueError('Number of factors must match')
    n=a*b
    roots_of_unity(n,p,omega)
    e_a,e_b=crt_idempotents(a,b)
    x=[0]*n
    for u in range(a):
        for v in range(b):
            x[(u*e_a+v*e_b)%n]=sum(f[u]*g[v] for f,g in zip(F,G))%p
    return x


def root_for(n:int,p:int):
    """Test helper only: primitive root supplied by sympy or brute scan."""
    if (p-1)%n:raise ValueError('N must divide p-1')
    for h in range(2,p):
        z=pow(h,(p-1)//n,p)
        v=1
        seen=True
        for i in range(1,n):
            v=v*z%p
            if v==1:
                seen=False
                break
        if seen and v*z%p==1:
            return z
    raise ValueError('no primitive root found')


def small_circular_convolution(f:Sequence[int],g:Sequence[int],p:int)->list[int]:
    """Exact cyclic convolution of same-length small vectors, O(m^2)."""
    m=len(f)
    if len(g)!=m:raise ValueError('Both input vectors must have same length')
    z=[0]*m
    for i,fi in enumerate(f):
        if fi%p:
            for j,gj in enumerate(g):
                z[(i+j)%m] += fi*gj
    return [v%p for v in z]


def circular_convolution_certified(c1:RankCertificate,c2:RankCertificate)->list[int]:
    """Exact length-N cyclic convolution, O(r1*r2*(N+A^2+B^2)).

    The product group CRT preserves the separability of cyclic convolution.
    Never calls a full FFT/NTT; all short cyclic convolutions use O(A^2+B^2).
    """
    if (c1.n,c1.a,c1.b,c1.p,c1.omega)!=(c2.n,c2.a,c2.b,c2.p,c2.omega):
        raise ValueError('Factorizations must have matching N,A,B,p,omega')
    a,b,n,p=c1.a,c1.b,c1.n,c1.p
    out=[0]*n
    for i in range(c1.rank):
        f1=[c1.coefficient_rows[u][i] for u in range(a)]
        g1=c1.basis_rows[i]
        for j in range(c2.rank):
            f2=[c2.coefficient_rows[u][j] for u in range(a)]
            g2=c2.basis_rows[j]
            ff=small_circular_convolution(f1,f2,p)
            gg=small_circular_convolution(g1,g2,p)
            for u in range(a):
                for v in range(b):
                    out[(u*c1.e_a+v*c1.e_b)%n] += ff[u]*gg[v]
    return [z%p for z in out]


def direct_circular_convolution(x:Sequence[int],y:Sequence[int],p:int)->list[int]:
    n=len(x)
    if len(y)!=n:raise ValueError('Input sizes must match')
    z=[0]*n
    for j,xx in enumerate(x):
        for k,yy in enumerate(y):
            z[(j+k)%n] += xx*yy
    return [v%p for v in z]
