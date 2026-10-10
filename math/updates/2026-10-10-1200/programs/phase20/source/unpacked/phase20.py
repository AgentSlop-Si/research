"""Hero #17 Phase 20: Fourier/Weyl Gaussian self-duality.

Exact prime-field mathematics. No sub-NlogN algorithm is claimed.
The 'fast' coefficient-action procedure invokes an explicitly counted ordinary
Fourier transform, revealing rather than hiding the cost.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Ledger:
    add: int = 0
    mul: int = 0
    inv: int = 0
    def plus(self,a,b,p):
        self.add += 1
        return (a+b)%p
    def minus(self,a,b,p):
        self.add += 1
        return (a-b)%p
    def times(self,a,b,p):
        self.mul += 1
        return (a*b)%p
    def inverse(self,a,p):
        self.inv += 1
        return pow(a%p,-1,p)
    def power(self,a,n,p):
        if n<0:
            return self.power(self.inverse(a,p),-n,p)
        a%=p;out=1
        while n:
            if n&1:out=self.times(out,a,p)
            n//=2
            if n:a=self.times(a,a,p)
        return out
    def total(self):return self.add+self.mul+self.inv
    def record(self):return {'additions_subtractions':self.add,'multiplications':self.mul,'inversions':self.inv,'field_operations':self.total()}


def factor_integer(n):
    d=2;out=[]
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out


def validate_root(n,p,q,c=None):
    if n<2 or p<=2 or (p-1)%n:
        raise ValueError('requires prime p odd with N dividing p-1')
    checked_power=(lambda exponent: c.power(q,exponent,p)) if c is not None else (lambda exponent: pow(q,exponent,p))
    if checked_power(n)!=1 or any(checked_power(n//r)==1 for r in factor_integer(n)):
        raise ValueError('root does not have exact order N')


def root_table(n,p,q,c):
    a=[1]*n
    for j in range(1,n):a[j]=c.times(a[j-1],q,p)
    return a


def direct_dft(x,q,p,c=None):
    """Independent O(N^2) negative-exponent DFT; charges all modular multiplications."""
    if c is None:c=Ledger()
    n=len(x); z=root_table(n,p,q,c); out=[]
    for k in range(n):
        y=0
        for t in range(n):
            y=c.plus(y,c.times(x[t],z[(-k*t)%n],p),p)
        out.append(y)
    return out


def radix2_dft(x,q,p,c=None):
    """Unnormalized negative-exponent iterative NTT with linear-size root table.

    Unlike the self-duality derivation, this is a conventional FFT.
    """
    if c is None:c=Ledger()
    n=len(x)
    if n&(n-1):raise ValueError('radix2 length required')
    powers=root_table(n,p,q,c)
    a=[v%p for v in x]
    j=0
    for i in range(1,n):
        bit=n//2
        while j&bit:
            j^=bit;bit//=2
        j^=bit
        if i<j:a[i],a[j]=a[j],a[i]
    stage=2
    while stage<=n:
        half=stage//2;step=n//stage
        for base in range(0,n,stage):
            for t in range(half):
                v=c.times(a[base+t+half],powers[(-step*t)%n],p)
                u=a[base+t]
                a[base+t]=c.plus(u,v,p)
                a[base+t+half]=c.minus(u,v,p)
        stage*=2
    return a


def dft_baseline(x,q,p,c=None):
    n=len(x)
    if n&(n-1)==0:return radix2_dft(x,q,p,c)
    return direct_dft(x,q,p,c)


def quadratic_gauss(n,p,q,k):
    return sum(pow(q,(-t*t-k*t)%n,p) for t in range(n))%p


def explicit_coefficient(n,p,q,a,b):
    """Independent trace of (S^a T^b)^(-1) F_N."""
    return quadratic_gauss(n,p,q,(a+b)%n)*pow(n,-1,p)%p


def full_coefficient_matrix(n,p,q):
    return [[explicit_coefficient(n,p,q,a,b) for b in range(n)] for a in range(n)]


def apply_coeff_direct(x,n,p,q,c=None):
    if c is None:c=Ledger()
    z=root_table(n,p,q,c)
    g=[]
    for k in range(n):
        v=0
        for t in range(n):v=c.plus(v,z[(-t*t-k*t)%n],p)
        g.append(v)
    n_inv=c.inverse(n,p)
    co=[c.times(s,n_inv,p) for s in g]
    y=[]
    for a in range(n):
        accum=0
        for b in range(n):
            accum=c.plus(accum,c.times(co[(a+b)%n],x[b],p),p)
        y.append(accum)
    return y


def apply_coeff_factorized(x,n,p,q,c=None,return_parts=False,ntt_root=None):
    """Apply full Weyl coefficient matrix using exact Gaussian chirps and DFTs.

    Odd N: one full N-DFT and O(N) chirp work.
    Even N: two N/2-DFTs and O(N) chirp work.
    Includes phase-table and prefactor preparation in field-operation ledger.
    """
    if c is None:c=Ledger()
    validate_root(n,p,q,c)
    if len(x)!=n:raise ValueError('wrong length')
    z=root_table(n,p,q,c)
    n_inv=c.inverse(n,p)
    if n%2:
        inv2=pow(2,-1,n);inv4=pow(4,-1,n)
        G=0
        for t in range(n):G=c.plus(G,z[(-t*t)%n],p)
        gamma=c.times(G,n_inv,p)
        if gamma==0:raise ArithmeticError('Gauss prefactor unexpectedly zero')
        diag=[z[(j*j*inv4)%n] for j in range(n)]
        fed=[c.times(diag[j],x[j],p) for j in range(n)]
        f=bluestein_dft(fed,q,p,ntt_root,c) if ntt_root is not None else dft_baseline(fed,q,p,c)
        # kernel is q^(a*b/2) instead of q^(-k*b); k=-a/2.
        out=[c.times(c.times(gamma,diag[a],p),f[(-inv2*a)%n],p) for a in range(n)]
        if return_parts:return out,dict(algorithm='one length-N DFT (Bluestein/NTT when ntt_root supplied)',N=n,dft_lengths=[n],gamma=gamma)
        return out
    m=n//2;kappa=m%2
    G=0
    for t in range(n):G=c.plus(G,z[(-t*t-kappa*t)%n],p)
    gamma=c.times(G,n_inv,p)
    if gamma==0:raise ArithmeticError('even Gauss prefactor unexpectedly zero')
    evenroot=c.times(q,q,p)
    out=[0]*n
    for inp_parity in (0,1):
        out_parity=(kappa-inp_parity)%2
        d=(out_parity+inp_parity-kappa)//2
        diag=[z[(j*j+(2*d+kappa)*j)%n] for j in range(m)]
        xblock=[c.times(diag[j],x[2*j+inp_parity],p) for j in range(m)]
        f=dft_baseline(xblock,evenroot,p,c)
        # positive-exponent m-point FFT: output at index -a.
        prefactor=c.times(gamma,z[(d*d+kappa*d)%n],p)
        for a in range(m):
            y=c.times(prefactor,diag[a],p)
            out[2*a+out_parity]=c.times(y,f[(-a)%m],p)
    if return_parts:return out,dict(algorithm='two length-N/2 DFTs',N=n,dft_lengths=[m,m],gamma=gamma,kappa=kappa)
    return out


def chart_weight_matrix(n,p,q,alpha,beta):
    """Fourier-specific double-character weights for original Green triangle.

    Only odd n; scalar factor gamma/delta included so weights synthesize
    the full *first-chart part* of the Weyl coefficient expansion.
    """
    if n%2==0:raise ValueError('odd N needed for full anti-diagonal')
    validate_root(n,p,q)
    alpha%=p;beta%=p
    delta=(1-pow(alpha,n,p)-pow(beta,n,p))%p
    if not alpha or not beta or not delta:raise ValueError('degenerate Green data')
    phi=[1]*n;z=[pow(q,i,p) for i in range(n)]
    for i in range(1,n):phi[i]=phi[i-1]*(1-z[i])%p
    gamma=quadratic_gauss(n,p,q,0)*pow(n,-1,p)%p
    if gamma==0:raise ArithmeticError('zero Gaussian')
    inv4=pow(4,-1,n)
    W=[[0]*n for _ in range(n)]
    for a in range(n):
        for b in range(n-a):
            deg=a+b
            numerator=delta*gamma*pow(q,(deg*deg*inv4)%n,p)*phi[a]*phi[b]
            denominator=pow(alpha,a,p)*pow(beta,b,p)*phi[deg]
            W[a][b]=numerator*pow(denominator%p,-1,p)%p
    return W


def rank_mod(A,p):
    A=[list(row) for row in A]; m=len(A);n=len(A[0]) if m else 0;r=0
    for j in range(n):
        pivot=next((i for i in range(r,m) if A[i][j]%p),None)
        if pivot is None:continue
        A[r],A[pivot]=A[pivot],A[r]
        inv=pow(A[r][j],-1,p)
        for k in range(j,n):A[r][k]=A[r][k]*inv%p
        for i in range(r+1,m):
            v=A[i][j]
            if v:
                for k in range(j,n):A[i][k]=(A[i][k]-v*A[r][k])%p
        r+=1
        if r==m:break
    return r


def primitive_root_of_order(n,p):
    """TEST ONLY; integer search not part of uniform operation ledger."""
    if (p-1)%n:raise ValueError('n does not divide p-1')
    for z in range(2,p):
        q=pow(z,(p-1)//n,p)
        if pow(q,n,p)==1 and all(pow(q,n//r,p)!=1 for r in factor_integer(n)):
            return q
    raise ArithmeticError('root not found')

class TriangularGreenChart:
    """O(N)-prepared, O(N)-stored FFT convolution evaluator for chart weights.

    W[a,b] = (Fourier Weyl coefficient c[a,b]) /
             (original two-axis Green sector scalar g[a,b]), when a+b<N.
    W=0 outside first chart. This matrix acts on its own coefficient-index
    input vector, NOT on the original input as a Fourier transform.
    N must be odd and a separate power-of-two NTT root of order L>=2N-1
    is supplied, with L|p-1. Preprocessing includes all scalar inversions.
    """
    def __init__(self,n,p,q,alpha,beta,rho,ledger=None):
        if n<3 or n%2==0:raise ValueError('odd n>=3 required')
        self.n,self.p,self.q=n,p,q
        self.alpha,self.beta=alpha%p,beta%p
        c=self.prep_ledger=ledger if ledger is not None else Ledger()
        validate_root(n,p,q,c)
        self.L=1<<(2*n-2).bit_length()
        if self.L&(self.L-1):raise AssertionError
        if (p-1)%self.L:raise ValueError('p cannot support convolution NTT length')
        validate_root(self.L,p,rho,c)
        self.rho=rho
        zp=root_table(n,p,q,c)
        a=self.alpha;b=self.beta
        if not a or not b:raise ValueError('nonzero alpha,beta required')
        delta=c.minus(c.minus(1,c.power(a,n,p),p),c.power(b,n,p),p)
        if not delta:raise ValueError('zero resolvent denominator')
        phi=[1]*n
        for t in range(1,n):
            phi[t]=c.times(phi[t-1],c.minus(1,zp[t],p),p)
        inv_phi=[1]*n
        inv_phi[-1]=c.inverse(phi[-1],p)
        for t in range(n-1,0,-1):
            inv_phi[t-1]=c.times(inv_phi[t],c.minus(1,zp[t],p),p)
        inva=c.inverse(a,p);invb=c.inverse(b,p)
        ap=1;bp=1
        self.A=[0]*n;self.B=[0]*n;self.H=[0]*n
        inv4=pow(4,-1,n)
        for t in range(n):
            self.A[t]=c.times(phi[t],ap,p)
            self.B[t]=c.times(phi[t],bp,p)
            self.H[t]=c.times(zp[(t*t*inv4)%n],inv_phi[t],p)
            if t<n-1:
                ap=c.times(ap,inva,p)
                bp=c.times(bp,invb,p)
        G=0
        for t in range(n):G=c.plus(G,zp[(-t*t)%n],p)
        self.gamma=c.times(G,c.inverse(n,p),p)
        self.scalar=c.times(delta,self.gamma,p)
        if not self.scalar:raise ArithmeticError('zero scalar on odd-n chart')

    def explicit_weight(self,a,b):
        if a+b>=self.n:return 0
        return self.scalar*self.A[a]*self.B[b]*self.H[a+b]%self.p

    def apply_naive(self,x,c=None):
        if len(x)!=self.n:raise ValueError('input length')
        if c is None:c=Ledger()
        n=self.n;p=self.p;out=[0]*n
        for a in range(n):
            v=0
            for b in range(n-a):
                z=c.times(c.times(self.B[b],self.H[a+b],p),x[b],p)
                v=c.plus(v,z,p)
            out[a]=c.times(c.times(self.scalar,self.A[a],p),v,p)
        return out

    def apply_fft(self,x,c=None):
        if len(x)!=self.n:raise ValueError('input length')
        if c is None:c=Ledger()
        n=self.n;p=self.p;L=self.L
        v=[c.times(self.B[b],x[b],p) for b in range(n)]
        a=[0]*L;b=[0]*L
        a[:n]=self.H
        b[:n]=v[::-1]
        Ah=radix2_dft(a,self.rho,p,c)
        Bv=radix2_dft(b,self.rho,p,c)
        prod=[c.times(Ah[k],Bv[k],p) for k in range(L)]
        ir=c.inverse(self.rho,p)
        t=radix2_dft(prod,ir,p,c)
        il=c.inverse(L,p)
        return [c.times(c.times(self.scalar,self.A[a],p),c.times(t[n-1+a],il,p),p) for a in range(n)]

    def record(self):
        return {'N':self.n,'convolution_ntt_length':self.L,'prepared_coefficients':3*self.n+1,
                'preparation':self.prep_ledger.record()}


def bluestein_dft(x,q,p,rho,c=None):
    """Classical Bluestein -> three explicitly charged length-L radix-2 NTTs.

    Exact negative-exponent n-point DFT for odd n. Requires independent
    supplied primitive L-th root rho for L=power-of-two >=2n-1.
    This is an existing FFT algorithm and does NOT prove a new upper bound.
    """
    if c is None:c=Ledger()
    n=len(x)
    if n<3 or n%2==0:raise ValueError('odd n>=3 needed')
    L=1<<(2*n-2).bit_length()
    validate_root(n,p,q,c);validate_root(L,p,rho,c)
    z=root_table(n,p,q,c)
    ih=pow(2,-1,n)
    a=[0]*L;b=[0]*L
    for t in range(n):
        theta=z[(-ih*t*t)%n]
        a[t]=c.times(x[t],theta,p)
        b[t]=z[(ih*t*t)%n]
    A=radix2_dft(a,rho,p,c)
    B=radix2_dft(b,rho,p,c)
    C=[c.times(A[k],B[k],p) for k in range(L)]
    r_inv=c.inverse(rho,p)
    y=radix2_dft(C,r_inv,p,c)
    il=c.inverse(L,p)
    out=[]
    for k in range(n):
        v=y[k]
        if k+n<2*n-1:
            v=c.plus(v,y[k+n],p)
        v=c.times(v,il,p)
        out.append(c.times(v,z[(-ih*k*k)%n],p))
    return out
