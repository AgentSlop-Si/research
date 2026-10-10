"""Phase 21: exact chirp/Weyl Green identities and Hankel-rank obstruction.

Everything in this file is over the prime field 998244353.  The algebraic
identities in THEOREM.md also hold over C.  The direct polynomial executor is
O(N^2) by design; it is NOT a faster FFT.
"""
from __future__ import annotations
from dataclasses import dataclass
import random

P=998244353
GEN=3


def root(n:int)->int:
    if n<4 or (n & (n-1)) or (P-1)%n:
        raise ValueError('n must be power of two >=4 dividing p-1')
    return pow(GEN, -(P-1)//n, P)


def sqrt_mod(a:int)->int:
    """Deterministic Tonelli-Shanks, gives a square root if one exists."""
    a%=P
    if a==0:return 0
    if pow(a,(P-1)//2,P)!=1:raise ValueError('nonresidue')
    q=P-1;s=0
    while q%2==0:q//=2;s+=1
    z=2
    while pow(z,(P-1)//2,P)!=P-1:z+=1
    c=pow(z,q,P);x=pow(a,(q+1)//2,P);t=pow(a,q,P);m=s
    while t!=1:
        i=1;y=t*t%P
        while y!=1:y=y*y%P;i+=1
        b=pow(c,1<<(m-i-1),P)
        x=x*b%P;t=t*b*b%P;c=b*b%P;m=i
    return x


def ntt_reference(x:list[int])->list[int]:
    """Conventional O(N log N) reference DFT, normalized with sqrt(N)."""
    n=len(x);w=root(n);a=x[:]
    j=0
    for i in range(1,n):
        b=n>>1
        while j&b:j^=b;b>>=1
        j^=b
        if i<j:a[i],a[j]=a[j],a[i]
    size=2
    while size<=n:
        s=pow(w,n//size,P)
        for low in range(0,n,size):
            tw=1
            for j in range(size//2):
                u=a[low+j];v=a[low+j+size//2]*tw%P
                a[low+j]=(u+v)%P
                a[low+j+size//2]=(u-v)%P
                tw=tw*s%P
        size*=2
    scale=pow(sqrt_mod(n),-1,P)
    return [v*scale%P for v in a]


def twisted_shift(x:list[int],w:int)->list[int]:
    """T=D^{-1}Z,  T(x)[j]=w^{-j} x[j-1] with wrap."""
    n=len(x)
    result=[0]*n
    f=1;w_inv=pow(w,-1,P)
    for j in range(n):
        result[j]=f*x[j-1]%P
        f=f*w_inv%P
    return result


def chirp_coefficients(n:int,w:int|None=None)->list[int]:
    if w is None:w=root(n)
    return [pow(w,-m*(m-1)//2,P) for m in range(n)]


def direct_chirp_polynomial(x:list[int])->list[int]:
    """Computes P(T)x via N repeated twisted shifts, O(N^2) operations."""
    n=len(x);w=root(n);coeff=chirp_coefficients(n,w)
    out=[0]*n;v=x[:]
    for m in range(n):
        cm=coeff[m]
        out=[(a+cm*b)%P for a,b in zip(out,v)]
        v=twisted_shift(v,w)
    return out


def chirp_factorized_dft(x:list[int])->list[int]:
    """F_N = D_quad P(T)/sqrt(N). O(N^2) direct, *not* a new FFT."""
    n=len(x);w=root(n)
    y=direct_chirp_polynomial(x)
    sc=pow(sqrt_mod(n),-1,P)
    return [v*pow(w,j*j,P)*sc%P for j,v in enumerate(y)]


@dataclass
class CyclicGreen:
    """Exact cyclic *bidiagonal* solve (I-alpha*T)^-1, O(N) per vector.

    Assumes N even, w is a primitive Nth root.  Unpivoted recurrence is
    valid since 1+alpha^N != 0, even if any other candidate pivot vanishes.
    """
    n:int
    alpha:int
    w:int
    factors:list[int]
    denominator_inv:int

    @classmethod
    def prepare(cls,n:int,alpha:int)->'CyclicGreen':
        w=root(n)
        a=alpha%P
        den=(1+pow(a,n,P))%P
        if not den:raise ValueError('singular Weyl pencil')
        factors=[0]*n
        invw=pow(w,-1,P)
        f=a*invw%P
        for j in range(1,n):
            factors[j]=f
            f=f*invw%P
        return cls(n,a,w,factors,pow(den,-1,P))

    def apply(self,x:list[int])->list[int]:
        if len(x)!=self.n:raise ValueError('wrong length')
        # y_j = b_j + a_j*y_0 for j >= 1.
        a=1;b=0
        aa=[0]*self.n;bb=[0]*self.n
        for j in range(1,self.n):
            f=self.factors[j]
            a=a*f%P
            b=(x[j]+f*b)%P
            aa[j]=a;bb[j]=b
        y0=(x[0]+self.alpha*b)*self.denominator_inv%P
        result=[y0]
        result.extend([(aa[j]*y0+bb[j])%P for j in range(1,self.n)])
        return result

    def apply_geometric_control(self,x:list[int])->list[int]:
        # O(N^2) reference, not used in the fast solver.
        cur=x[:];out=[0]*self.n;alpha_power=1
        for _ in range(self.n):
            out=[(o+alpha_power*c)%P for o,c in zip(out,cur)]
            cur=twisted_shift(cur,self.w)
            alpha_power=alpha_power*self.alpha%P
        return [v*self.denominator_inv%P for v in out]


def polynomial_green_sum(x:list[int],alphas:list[int],weights:list[int])->list[int]:
    """Naive independent execution: q separate O(N) cyclic Green solves."""
    if len(alphas)!=len(weights):raise ValueError('lengths differ')
    out=[0]*len(x)
    for a,b in zip(alphas,weights):
        z=CyclicGreen.prepare(len(x),a).apply(x)
        out=[(u+b*v)%P for u,v in zip(out,z)]
    return out


def matrix_rank(A:list[list[int]])->int:
    a=[row[:] for row in A]
    n=len(a);m=len(a[0]) if n else 0
    r=0
    for j in range(m):
        pivot=next((i for i in range(r,n) if a[i][j]),None)
        if pivot is None:continue
        a[pivot],a[r]=a[r],a[pivot]
        inv=pow(a[r][j],-1,P)
        for k in range(j,m):a[r][k]=a[r][k]*inv%P
        for i in range(r+1,n):
            f=a[i][j]
            if not f:continue
            for k in range(j,m):a[i][k]=(a[i][k]-f*a[r][k])%P
        r+=1
        if r==n:break
    return r


def hankel(c:list[int],size:int)->list[list[int]]:
    if size*2-2>=len(c):raise ValueError('Hankel needs known coefficients')
    return [[c[i+j] for j in range(size)] for i in range(size)]


def linear_solve(A:list[list[int]],b:list[int])->list[int]:
    """Finite-field square solve, only used for small positive controls."""
    n=len(b);a=[A[i][:]+[b[i]%P] for i in range(n)]
    for j in range(n):
        p=next((i for i in range(j,n) if a[i][j]),None)
        if p is None:raise ValueError('singular matrix')
        a[j],a[p]=a[p],a[j]
        inv=pow(a[j][j],-1,P)
        for k in range(j,n+1):a[j][k]=a[j][k]*inv%P
        for i in range(j+1,n):
            f=a[i][j]
            if f:
                for k in range(j,n+1):a[i][k]=(a[i][k]-f*a[j][k])%P
    x=[0]*n
    for i in range(n-1,-1,-1):
        x[i]=(a[i][n]-sum(a[i][j]*x[j] for j in range(i+1,n)))%P
    return x


def full_green_dictionary(n:int)->tuple[list[int],list[int]]:
    """Find N resolvents realizing P(T); expensive explicit O(N^3) setup.

    This is a finite-field positive control, NOT a fast construction.
    """
    w=root(n);c=chirp_coefficients(n,w)
    alphas=[];a=1
    while len(alphas)<n:
        if (1+pow(a,n,P))%P:alphas.append(a)
        a+=1
    V=[[pow(alpha,m,P) for alpha in alphas] for m in range(n)]
    beta=linear_solve(V,c)
    weights=[beta[j]*(1+pow(alpha,n,P))%P for j,alpha in enumerate(alphas)]
    return alphas,weights


def raw_green_matrix(n:int,alpha:int)->list[list[int]]:
    g=CyclicGreen.prepare(n,alpha)
    cols=[]
    for k in range(n):
        e=[0]*n;e[k]=1
        cols.append(g.apply(e))
    return [[cols[k][j] for k in range(n)] for j in range(n)]


def column_ratio_distinct_count(A:list[list[int]],k:int,l:int)->int:
    ratios=set()
    for row in A:
        if row[k]==0 or row[l]==0:raise ValueError('zero entry')
        ratios.add(row[k]*pow(row[l],-1,P)%P)
    return len(ratios)


def chirp_adjacent_certificate(c:list[int],w:int)->bool:
    """True iff all interior cross-ratios match Fourier's omega."""
    return all(c[m]*c[m]*pow(c[m-1]*c[m+1]%P,-1,P)%P==w
               for m in range(1,len(c)-1))


def random_input(n:int,seed:int)->list[int]:
    rng=random.Random(seed)
    return [rng.randrange(P) for _ in range(n)]


def negacyclic_convolution(a:list[int],b:list[int])->list[int]:
    """Multiply polynomials mod z^N+1, matching T^N=-I."""
    n=len(a)
    if len(b)!=n:raise ValueError('length mismatch')
    out=[0]*n
    for i,ai in enumerate(a):
        if not ai:continue
        for j,bj in enumerate(b):
            ij=i+j
            if ij>=n:out[ij-n]=(out[ij-n]-ai*bj)%P
            else:out[ij]=(out[ij]+ai*bj)%P
    return out


def single_green_coeff(n:int,alpha:int)->list[int]:
    alpha%=P
    inv=pow((1+pow(alpha,n,P))%P,-1,P)
    return [pow(alpha,m,P)*inv%P for m in range(n)]


def product_of_parallel_green_coeffs(n:int,stages:list[list[tuple[int,int]]])->list[int]:
    """Commuting resolvents: each stage is a sum of (weight,alpha) Green terms.

    Output polynomial coefficients in T. This is an O(stages*q*N^2)
    *audit*, not the method for applying the actual stages.
    """
    total=[1]+[0]*(n-1)
    for stage in stages:
        coeff=[0]*n
        for weight,alpha in stage:
            g=single_green_coeff(n,alpha)
            coeff=[(c+weight*v)%P for c,v in zip(coeff,g)]
        total=negacyclic_convolution(total,coeff)
    return total


def second_shift(x:list[int],w:int)->list[int]:
    """U=ZD: (Ux)[j] = w^(j-1) x[j-1]."""
    n=len(x);v=pow(w,-1,P);out=[]
    for j in range(n):
        out.append(v*x[j-1]%P)
        v=v*w%P
    return out


@dataclass
class SecondCyclicGreen:
    """(I-beta*ZD)^-1 using one O(N) cyclic bidiagonal solve."""
    n:int
    beta:int
    w:int
    factors:list[int]
    inv_den:int

    @classmethod
    def prepare(cls,n:int,beta:int)->'SecondCyclicGreen':
        w=root(n);beta%=P
        den=(1+pow(beta,n,P))%P
        if not den:raise ValueError('singular second Weyl pencil')
        factors=[];tw=pow(w,-1,P)
        for j in range(n):
            factors.append(beta*tw%P)
            tw=tw*w%P
        return cls(n,beta,w,factors,pow(den,-1,P))

    def apply(self,x:list[int])->list[int]:
        n=self.n
        if len(x)!=n:raise ValueError('length mismatch')
        a=1;b=0;aa=[0]*n;bb=[0]*n
        for j in range(1,n):
            f=self.factors[j]
            a=a*f%P;b=(x[j]+f*b)%P
            aa[j]=a;bb[j]=b
        y0=(x[0]+self.factors[0]*b)*self.inv_den%P
        return [y0]+[(aa[j]*y0+bb[j])%P for j in range(1,n)]


def dense_matrix_apply(oracle,n:int)->list[list[int]]:
    cols=[]
    for k in range(n):
        v=[0]*n;v[k]=1
        cols.append(oracle(v))
    return [[cols[k][j] for k in range(n)] for j in range(n)]


def small_weyl_defect_counts(oracle,n:int)->tuple[int,int]:
    """Deterministic random-vector Weyl rejection, NOT an equality proof."""
    x=random_input(n,500+n)
    w=root(n)
    def Z(v):return [v[-1]]+v[:-1]
    def D(v):return [v[j]*pow(w,j,P)%P for j in range(n)]
    Mx=oracle(x)
    first=oracle(Z(x));second=oracle(D(x))
    Dx=D(Mx)
    invZ=Mx[1:]+Mx[:1]
    return (sum(a!=b for a,b in zip(first,Dx)),
            sum(a!=b for a,b in zip(second,invZ)))


@dataclass
class CyclicWeightedGreen:
    """Invert I-S where S has arbitrary cyclic forward edge weights w[j].

    (S y)[j] = w[j] y[j-1], indices interpreted modulo N.
    The inverse exists iff product_j(w[j]) != 1.
    """
    weights:list[int]
    inv_den:int

    @classmethod
    def prepare(cls,weights:list[int])->'CyclicWeightedGreen':
        product=1
        for w in weights:product=product*w%P
        den=(1-product)%P
        if not den:raise ValueError('singular cyclic weighted path')
        return cls([w%P for w in weights],pow(den,-1,P))

    def apply(self,x:list[int])->list[int]:
        n=len(self.weights)
        if len(x)!=n:raise ValueError('wrong length')
        a=1;b=0;aa=[0]*n;bb=[0]*n
        for j in range(1,n):
            w=self.weights[j]
            a=a*w%P;b=(x[j]+w*b)%P
            aa[j]=a;bb[j]=b
        y0=(x[0]+self.weights[0]*b)*self.inv_den%P
        return [y0]+[(aa[j]*y0+bb[j])%P for j in range(1,n)]


def random_weighted_green(n:int,seed:int)->CyclicWeightedGreen:
    rng=random.Random(seed)
    return CyclicWeightedGreen.prepare([rng.randrange(1,P) for _ in range(n)])


def sum_apply(terms:list,x:list[int])->list[int]:
    out=[0]*len(x)
    for t in terms:
        y=t.apply(x)
        out=[(a+b)%P for a,b in zip(out,y)]
    return out


def block_rank(oracle,n:int,cut:int)->int:
    """Rank of prefix-row / suffix-column block (dense testing only)."""
    cols=[]
    for k in range(cut,n):
        v=[0]*n;v[k]=1
        cols.append(oracle(v))
    B=[[cols[k-cut][j] for k in range(cut,n)] for j in range(cut)]
    return matrix_rank(B)


def prony_annihilator(n:int)->list[int]:
    """Monic h=N/2 recurrence polynomial annihilating chirp moments 0..N-1.

    A(z) obtained from the product of roots in the dual Vandermonde variable.
    Explicit formula: A_j = c_h/c_j * [z^j]prod_(k=0)^(h-1)(z-w^-k).
    """
    h=n//2;w=root(n);c=chirp_coefficients(n,w)
    R=[1]
    for k in range(h):
        a=pow(w,-k,P)
        nxt=[0]*(len(R)+1)
        for j,v in enumerate(R):
            nxt[j]=(nxt[j]-a*v)%P
            nxt[j+1]=(nxt[j+1]+v)%P
        R=nxt
    A=[R[j]*c[h]*pow(c[j],-1,P)%P for j in range(h+1)]
    assert A[-1]==1
    return A


def poly_trim(a:list[int])->list[int]:
    a=a[:]
    while a and a[-1]==0:a.pop()
    return a


def poly_gcd_degree(a:list[int],b:list[int])->int:
    """Exact Euclidean gcd degree over the selected prime field."""
    a=poly_trim(a);b=poly_trim(b)
    while b:
        lead_inv=pow(b[-1],-1,P)
        while len(a)>=len(b):
            factor=a[-1]*lead_inv%P
            offset=len(a)-len(b)
            if factor:
                for j,v in enumerate(b):a[offset+j]=(a[offset+j]-factor*v)%P
            a=poly_trim(a)
        a,b=b,a
    return len(a)-1


def prony_squarefree_certificate(n:int)->dict:
    """A modular gcd=1 result certifies corresponding char-0 result.

    Coefficients are integral in Z[zeta_N], and p=1 mod N, so a zero
    resultant in characteristic zero would reduce to zero in F_p.
    """
    a=prony_annihilator(n)
    deriv=[j*a[j]%P for j in range(1,len(a))]
    f=[1]+[0]*(n-1)+[1]
    gcd_derivative=poly_gcd_degree(a,deriv)
    gcd_forbidden=poly_gcd_degree(a,f)
    return {'n':n,'degree':len(a)-1,'gcd_derivative_degree':gcd_derivative,
            'gcd_forbidden_poles_degree':gcd_forbidden,
            'certifies_N_over_2_distinct_admissible_complex_poles':
                gcd_derivative==0 and gcd_forbidden==0}
