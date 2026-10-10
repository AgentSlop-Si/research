"""Phase 15: exact Weyl-support, chirp-convolution and dyadic-Green certificates.

No FFTs, external math dependencies, GPUs, parallelism or lookup oracles.
Arithmetic takes place in finite prime fields with n | p-1 (2*n | p-1 for
chirp identities). Symbolic support statements also hold over the complex field.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from math import isqrt

P = 998244353
PRIMITIVE_GENERATOR = 3


def prime_factors(n: int) -> list[int]:
    factors = []
    k = 2
    while k * k <= n:
        if n % k == 0:
            factors.append(k)
            while n % k == 0:
                n //= k
        k += 1 if k == 2 else 2
    if n > 1:
        factors.append(n)
    return factors


def generator(p: int) -> int:
    fac = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise ValueError('No primitive generator found')


def root_of_unity(n: int, p: int = P, g: int | None = None) -> int:
    if (p - 1) % n:
        raise ValueError('n must divide p-1')
    g = PRIMITIVE_GENERATOR if p == P and g is None else (generator(p) if g is None else g)
    w = pow(g, (p - 1) // n, p)
    if any(pow(w, n // q, p) == 1 for q in prime_factors(n)):
        raise ValueError('The supplied generator did not yield order n')
    return w


def direct_dft(vec: list[int], omega: int, p: int = P, positive: bool = False) -> list[int]:
    n = len(vec)
    base = omega if positive else pow(omega, n - 1, p)
    powers = [1] * n
    for j in range(1, n):
        powers[j] = powers[j - 1] * base % p
    out = []
    for k in range(n):
        row_step = powers[k]
        phase = 1
        accumulator = 0
        for v in vec:
            accumulator = (accumulator + v * phase) % p
            phase = phase * row_step % p
        out.append(accumulator)
    return out


def gauss_table(n: int, omega: int, p: int = P) -> list[int]:
    """G[d]=sum_j omega^(j*j+d*j), evaluated by a direct O(n^2) loop."""
    pw = [1]
    for _ in range(n - 1):
        pw.append(pw[-1] * omega % p)
    values = []
    for d in range(n):
        values.append(sum(pw[(j * j + d * j) % n] for j in range(n)) % p)
    return values


def fourier_weyl_support_size(n: int) -> int:
    return n * n if n % 2 else n * n // 2


def weyl_coefficients_fourier_inverse(n: int, omega: int, p: int = P) -> dict[tuple[int,int], int]:
    """The *inverse* of F_-[i,j]=omega^(-i*j) is F_+/n.

    W_{a,b}=S^a T^b, so coefficient = G(a-b)/n^2.
    """
    g = gauss_table(n, omega, p)
    inv_n2 = pow((n * n) % p, p - 2, p)
    return {(a, b): (g[(a-b)%n] * inv_n2) % p
            for a in range(n) for b in range(n)
            if g[(a-b)%n] % p}


def multiply_weyl(a: dict[tuple[int,int],int], b: dict[tuple[int,int],int],
                  n: int, omega: int, p: int = P) -> dict[tuple[int,int],int]:
    """(S^a T^b)(S^c T^d)=omega^(b*c) S^(a+c) T^(b+d)."""
    result: dict[tuple[int,int],int] = defaultdict(int)
    pw = [1] * n
    for i in range(1, n):
        pw[i] = pw[i-1] * omega % p
    for (u,v),av in a.items():
        for (s,t),bv in b.items():
            idx = ((u+s)%n, (v+t)%n)
            result[idx] = (result[idx] + av * bv * pw[(v*s)%n]) % p
    return {k:v for k,v in result.items() if v}


def three_atom_factor(n: int, s: int, b: int, alpha: int, beta: int,
                      p: int = P) -> dict[tuple[int,int],int]:
    r = defaultdict(int)
    r[(0,0)] = 1
    r[(s%n,0)] = (r[(s%n,0)]-alpha)%p
    r[(0,b%n)] = (r[(0,b%n)]-beta)%p
    return {k:v for k,v in r.items() if v}


def multiscale_inverse_polynomial(n: int, shifts: list[int], modulations: list[int],
                                  alphas: list[int], betas: list[int],
                                  omega: int, p: int = P) -> dict[tuple[int,int],int]:
    """Symbolically multiply inverse factors, in their listed order."""
    poly = {(0,0):1}
    for s,b,a,be in zip(shifts,modulations,alphas,betas,strict=True):
        poly = multiply_weyl(poly, three_atom_factor(n,s,b,a,be,p), n, omega,p)
    return poly


def apply_three_atom(x: list[int], s: int, b: int, alpha: int, beta: int,
                     omega: int, p: int=P) -> list[int]:
    n=len(x); s%=n; b%=n
    pw=[1]*n
    omega_b=pow(omega,b,p)
    for j in range(1,n):
        pw[j]=pw[j-1]*omega_b%p
    return [((1-beta*pw[j])*x[j] - alpha*x[(j-s)%n])%p for j in range(n)]


def apply_weyl_polynomial(x:list[int], poly:dict[tuple[int,int],int],
                          omega:int,p:int=P) -> list[int]:
    n=len(x)
    pows=[1]*n
    for j in range(1,n):
        pows[j]=pows[j-1]*omega%p
    out=[0]*n
    for (a,b),c in poly.items():
        for j,v in enumerate(x):
            out[(j+a)%n]=(out[(j+a)%n]+c*v*pows[(b*j)%n])%p
    return out


def power_of_two(n:int)->bool:
    return n>=1 and (n&(n-1))==0


def weyl_stage_lower_bound(n:int)->int:
    """smallest L with 3**L >= rank-support(F_n^(-1))."""
    target=fourier_weyl_support_size(n); stages=0; possibilities=1
    while possibilities<target:
        possibilities*=3; stages+=1
    return stages


def chirp_kernel(n:int,zeta:int,p:int=P, inverse:bool=False)->list[int]:
    if not power_of_two(n) or n<2:
        raise ValueError('This cyclic chirp certificate uses even power-of-two n')
    if inverse:
        zeta=pow(zeta,-1,p)
        scale=pow(n,-1,p)
    else:
        scale=1
    return [scale*pow(zeta,j*j,p)%p for j in range(n)]


def cyclic_convolution(a:list[int],b:list[int],p:int=P)->list[int]:
    n=len(a)
    if n!=len(b):
        raise ValueError('input lengths must match')
    return [sum(a[j]*b[(k-j)%n] for j in range(n))%p for k in range(n)]


def chirp_direct_transform(x:list[int],zeta:int,p:int=P)->list[int]:
    """F_-(x)=D^-1 * C_chirp * D^-1(x); direct circular convolution."""
    n=len(x)
    zinv=pow(zeta,-1,p)
    dechirp=[pow(zinv,j*j,p) for j in range(n)]
    pre=[x[j]*dechirp[j]%p for j in range(n)]
    mid=cyclic_convolution(pre,chirp_kernel(n,zeta,p),p)
    return [mid[j]*dechirp[j]%p for j in range(n)]


def dyadic_cross_ratio(n:int,zeta:int,p:int=P)->tuple[int,int]:
    """q_0*q_3 vs q_1*q_2 for inverse chirp convolution."""
    q=chirp_kernel(n,zeta,p,inverse=True)
    return q[0]*q[3]%p, q[1]*q[2]%p


@dataclass
class Count:
    additions: int=0
    multiplications: int=0
    inversions: int=0
    writes: int=0
    reads: int=0
    def total(self)->int:
        return self.additions+self.multiplications+self.inversions
    def as_dict(self)->dict:
        return {'additions':self.additions,'multiplications':self.multiplications,
                'inversions':self.inversions,'field_ops':self.total(),
                'writes':self.writes,'reads':self.reads}


def dyadic_binomial_product(x:list[int],alpha:int,p:int=P)->tuple[list[int],Count]:
    """Literal m-stage application of prod_j(I+alpha^(2^j) S^(2^j))."""
    n=len(x)
    if not power_of_two(n): raise ValueError('requires n=2^m')
    cnt=Count(); out=x.copy(); a=alpha%p
    for j in range(n.bit_length()-1):
        stride=1<<j
        nxt=[0]*n
        for i in range(n):
            nxt[i]=(out[i]+a*out[(i-stride)%n])%p
            cnt.reads+=2;cnt.multiplications+=1;cnt.additions+=1;cnt.writes+=1
        out=nxt
        if j<n.bit_length()-2:
            a=(a*a)%p;cnt.multiplications+=1
    return out,cnt


def fused_dyadic_binomial(x:list[int],alpha:int,p:int=P)->tuple[list[int],Count]:
    """O(n) *same operator* via one cyclic Green solve plus final scaling.

    prod_j (I+alpha^(2^j) S^(2^j)) = (1-alpha^n)(I-alpha S)^(-1).
    """
    n=len(x)
    if not power_of_two(n):raise ValueError('requires n=2^m')
    alpha%=p; cnt=Count()
    # Weighted wraparound initial value: num=y_0*(1-alpha^n).
    num=x[0];cnt.reads+=1
    pw=alpha
    for k in range(1,n):
        num=(num+pw*x[n-k])%p
        cnt.multiplications+=1; cnt.additions+=1;cnt.reads+=1
        if k<n-1:
            pw=pw*alpha%p;cnt.multiplications+=1
    alpha_n=(pw*alpha)%p if n>1 else alpha  # pw=alpha^(n-1)
    cnt.multiplications+=1
    d=(1-alpha_n)%p;cnt.additions+=1
    if d==0:
        raise ValueError('Green denominator 1-alpha^n is zero')
    dinv=pow(d,-1,p);cnt.inversions+=1
    first=num*dinv%p;cnt.multiplications+=1
    y=[0]*n;y[0]=first;cnt.writes+=1
    for i in range(1,n):
        y[i]=(x[i]+alpha*y[i-1])%p
        cnt.multiplications+=1;cnt.additions+=1;cnt.reads+=2;cnt.writes+=1
    # Absorb denominator in the output; do not hide N output multiplies.
    out=[d*v%p for v in y];cnt.multiplications+=n;cnt.reads+=n;cnt.writes+=n
    return out,cnt


def inverse_chirp_linear_generation(n:int,zeta:int,p:int=P)->tuple[list[int],Count]:
    """Generate q[j]=zeta^(-j*j)/n in O(n) field operations.

    This creates a high tensor-rank *kernel vector*; it does NOT compute
    its cyclic convolution with a fresh, unrelated length-n input.
    """
    if n<2 or not power_of_two(n):
        raise ValueError('n must be a power of two >=2')
    cnt=Count()
    inv_n=pow(n,-1,p);cnt.inversions+=1
    z_inv=pow(zeta,-1,p);cnt.inversions+=1
    z_inv_squared=(z_inv*z_inv)%p;cnt.multiplications+=1
    q=[0]*n;q[0]=inv_n;cnt.writes+=1
    ratio=z_inv
    for j in range(1,n):
        q[j]=q[j-1]*ratio%p;cnt.multiplications+=1;cnt.reads+=1;cnt.writes+=1
        if j<n-1:
            ratio=ratio*z_inv_squared%p;cnt.multiplications+=1
    return q,cnt


def exact_rank_mod(rows:list[list[int]],p:int=P)->int:
    if not rows:return 0
    mat=[r.copy() for r in rows]
    h=len(mat); w=len(mat[0]); rank=0
    for j in range(w):
        pivot=next((i for i in range(rank,h) if mat[i][j]%p),None)
        if pivot is None:continue
        mat[rank],mat[pivot]=mat[pivot],mat[rank]
        inv=pow(mat[rank][j],-1,p)
        # Eliminate only below; avoids wasted work.
        for i in range(rank+1,h):
            if mat[i][j]%p:
                mult=mat[i][j]*inv%p
                for k in range(j+1,w):
                    mat[i][k]=(mat[i][k]-mult*mat[rank][k])%p
                mat[i][j]=0
        rank+=1
        if rank==h:break
    return rank


def chirp_digit_cut_rank(n:int,zeta:int,split:int,p:int=P)->int:
    """Rows low split bits, columns high remaining bits."""
    if not power_of_two(n):raise ValueError('power-of-two n only')
    m=n.bit_length()-1
    if not (0<split<m):raise ValueError('cut must be between bits')
    h=1<<split; w=n//h
    invn=pow(n,-1,p); invz=pow(zeta,-1,p)
    mat=[[invn*pow(invz,(u+h*v)**2,p)%p for v in range(w)] for u in range(h)]
    return exact_rank_mod(mat,p)


def oriented_three_atom_factor(n:int, direction_one:tuple[int,int],
                               direction_two:tuple[int,int], alpha:int,beta:int,
                               p:int=P)->dict[tuple[int,int],int]:
    """I-alpha W_{u,v}-beta W_{r,s}: directions need not be axial."""
    out:dict[tuple[int,int],int]=defaultdict(int)
    out[(0,0)]=1
    first=(direction_one[0]%n,direction_one[1]%n)
    second=(direction_two[0]%n,direction_two[1]%n)
    out[first]=(out[first]-alpha)%p
    out[second]=(out[second]-beta)%p
    return {k:v for k,v in out.items() if v}


def oriented_inverse_chain_polynomial(n:int,
    factors:list[tuple[tuple[int,int],tuple[int,int],int,int]],
    omega:int,p:int=P)->dict[tuple[int,int],int]:
    """Multiply all q<=3 inverse-symbol factors; no commuting assumption."""
    result={(0,0):1}
    for u,v,alpha,beta in factors:
        result=multiply_weyl(result,oriented_three_atom_factor(n,u,v,alpha,beta,p),n,omega,p)
    return result


def exact_fourier_intertwining_certificate(
    matrix:list[list[int]],omega:int,p:int=P)->bool:
    """True iff M*S=T^(-1)*M and M*e_0=ones, hence M=F_-.

    Uses O(n^2) checks for a *candidate matrix*. A future fast circuit
    must prove these symbolically rather than construct its dense matrix.
    """
    n=len(matrix)
    if n==0 or any(len(r)!=n for r in matrix):return False
    invw=pow(omega,-1,p)
    phase=1
    for row in matrix:
        if row[0]%p != 1:return False
        for j in range(n):
            if row[(j+1)%n]%p != (phase*row[j])%p:
                return False
        phase=phase*invw%p
    return True
