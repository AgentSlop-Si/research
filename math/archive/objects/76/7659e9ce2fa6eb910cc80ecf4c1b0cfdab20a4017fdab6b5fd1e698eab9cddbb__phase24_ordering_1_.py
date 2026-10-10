"""Phase 24: exact permutation-defect ranks and a low-rank Green update.

Conventions: Z e_j=e_{j+1 mod n}; an order L specifies P^-1 e_k=e_{L[k]}.
W=P^-1 Z P is successor around L.  For a binary input, L is stable
sorting of zero-valued coordinates before one-valued coordinates.

This code does NOT implement a new worst-case sub-NlogN Fourier transform.
It exposes the cost hidden when one sorts inputs but has to conjugate the
shift defining the original DFT.
"""
from __future__ import annotations
from math import comb,ceil,log2,exp
from phase23_resolvent import RealGreenFourier, P, _normalized_fourier_to_real_residual


def stable_binary_order(bits):
    if any(v not in (0,1) for v in bits):
        raise ValueError('binary input required')
    return [j for j,b in enumerate(bits) if b==0]+[j for j,b in enumerate(bits) if b==1]


def successor_of_order(order):
    n=len(order)
    if sorted(order)!=list(range(n)):
        raise ValueError('order must permute all n coordinate indices')
    where=[0]*n
    for k,j in enumerate(order): where[j]=k
    return [order[(where[j]+1)%n] for j in range(n)]


def cycle_rank_difference(successor,a=1):
    """Exact rank over any field of W-Z^a; O(n), no linear algebra.

    Left-multiplication by Z^-a gives permutation V with
    V(j)=(W(j)-a) mod n, and rank(V-I)=n-#cycles(V).
    """
    n=len(successor)
    if n==0:return 0
    if sorted(successor)!=list(range(n)):
        raise ValueError('successor must represent a permutation')
    visited=[False]*n
    cycles=0
    for j in range(n):
        if not visited[j]:
            cycles+=1
            k=j
            while not visited[k]:
                visited[k]=True
                k=(successor[k]-a)%n
    return n-cycles


def transitions_noncyclic(bits):
    return sum(bits[j]!=bits[j+1] for j in range(len(bits)-1))


def predicted_binary_rank(bits):
    return 2*(transitions_noncyclic(bits)//2)


def binary_rank_probability(n,r):
    """Exact P(rank(W-Z)=r) under n iid fair binary bits, as (num,den)."""
    if n<2:raise ValueError('n>=2')
    if r<0 or r>=n or r%2:return (0,2**(n-1))
    return (comb(n,r+1),2**(n-1))


def all_stride_rank_lower_bound_probability(n):
    """Explicit high-probability guarantee simultaneously for ALL strides.

    For iid fair binary data of length n>=16, stable sorting defines W.
    With probability at least the value returned, for EVERY 1<=a<n,
        rank(W-Z^a) >= n/8.

    Proof: outside two bridge edges, each W(j)=j+a for a>0 requires
    the substring x[j:j+a+1] to be c,1-c,...,1-c,c, an event of
    probability 2^-a. The number Q_a of these events is concentrated.
    Q_1 is Binomial(n-1,1/2). For 2<=a<=A=ceil(3log2(n)), divide the
    length-(a+1) windows into a+1 independent families, apply Hoeffding
    with total deviation n/4, and union-bound. For a>A, bound the
    probability of ANY such substring by n*2^-A. If the number of
    matched edges is <=3n/4, the rank of two permutation matrices is
    >= (n - #matches)/2 >= n/8.

    The bound may be vacuous for moderate n; the asymptotic guarantee is
    rigorous and applies even to non-coprime strides (Z^a need not be
    an n-cycle).
    """
    if n<16:raise ValueError('n>=16')
    A=min(n-1,ceil(3*log2(n)))
    failure=exp(-n/32) + A*(A+1)*exp(-n/(16*(A+1))) + n*2**(-A)
    return max(0.,1.-failure)


def _C_column(j,engine):
    """Compute column j of real C in O(n) field operations."""
    n=engine.n
    step=pow(engine.omega,j,P)
    power=1
    f=[0]*n
    for k in range(n):
        f[k]=power*engine.inv_sqrt_n%P
        power=power*step%P
    return _normalized_fourier_to_real_residual(f,engine)


def _invert_block_resolvent(engine,z,v):
    """Apply (I-zR)^-1 to ANY RHS, using n/2-1 independent 2x2 blocks.

    For z^n!=1, every block is invertible. Uses O(n) field operations,
    with separate per-block inversions (fast enough for this exact audit).
    """
    n=engine.n;h=n//2;z%=P
    if pow(z,n,P)==1:raise ValueError('z lies on n-th roots of unity')
    y=[0]*n
    y[0]=v[0]*pow((1-z)%P,-1,P)%P
    y[1]=v[1]*pow((1+z)%P,-1,P)%P
    z2=z*z%P
    for j,(c,s) in enumerate(engine.angles,1):
        det=(1-2*z*c+z2)%P
        invdet=pow(det,-1,P)
        q=(1-z*c)%P;t=z*s%P
        a=v[j+1];b=v[h+j]
        y[j+1]=(q*a-t*b)*invdet%P
        y[h+j]=(t*a+q*b)*invdet%P
    return y


def _solve_linear_system(A,b):
    """Exact modular Gauss-Jordan solve for small matrices."""
    m=len(A)
    if m==0:return []
    V=[[(a%P) for a in row]+[rhs%P] for row,rhs in zip(A,b)]
    for j in range(m):
        pivot=next((i for i in range(j,m) if V[i][j]),None)
        if pivot is None:raise ArithmeticError('singular Woodbury correction')
        V[j],V[pivot]=V[pivot],V[j]
        d=pow(V[j][j],-1,P)
        for k in range(j,m+1):V[j][k]=V[j][k]*d%P
        for i in range(m):
            if i==j:continue
            c=V[i][j]
            for k in range(j,m+1):V[i][k]=(V[i][k]-c*V[j][k])%P
    return [V[i][-1] for i in range(m)]


def permuted_geometric_via_green_woodbury(order,z,engine):
    """Compute C P^-1 (1,z,...,z^(n-1)) by low-rank correction.

    If s=number of successor edges changed relative to standard Z, it costs
    O(n*s*s+s^3) modular operations (plus O(n*s) preparation) and O(ns)
    memory. Useful for s=O(1), NOT for random binary sorting where s=Theta(n).

    The formula is exact over F_998244353, z^n!=1. For z^n==1, use a
    separate Fourier-character branch (not implemented in this test module).
    """
    n=len(order)
    if engine.n!=n:raise ValueError('engine length mismatch')
    if pow(z,n,P)==1:raise ValueError('singular base resolvent (root z)')
    w=successor_of_order(order)
    changed=[j for j in range(n) if w[j]!=(j+1)%n]
    s=len(changed)
    # C P^-1 e_0 = C e_order[0], and C^-1=C^T.
    seed=_C_column(order[0],engine)
    base_seed=_invert_block_resolvent(engine,z,seed)
    if s==0:return [(1-pow(z,n,P))*q%P for q in base_seed]
    # C(E)e_j = C e_W(j) - C e_Z(j)
    u_cols=[]
    v_cols=[]
    for j in changed:
        col1=_C_column(w[j],engine)
        col2=_C_column((j+1)%n,engine)
        u_cols.append([(a-b)%P for a,b in zip(col1,col2)])
        v_cols.append(_C_column(j,engine))  # row e_j^T C^-1 = (Ce_j)^T
    au_cols=[_invert_block_resolvent(engine,z,u) for u in u_cols]
    small=[[(int(i==j)-z*sum(v_cols[i][k]*au_cols[j][k] for k in range(n)))%P
            for j in range(s)] for i in range(s)]
    rhs=[sum(v_cols[i][k]*base_seed[k] for k in range(n))%P for i in range(s)]
    coeffs=_solve_linear_system(small,rhs)
    factor=(1-pow(z,n,P))%P
    return [(factor*(base_seed[k]+z*sum(au_cols[j][k]*coeffs[j]
                                         for j in range(s))))%P for k in range(n)]


def direct_permuted_geometric_reference(order,z,engine):
    """O(nlogn) independent reference: use Phase23 modular FFT fallback."""
    from phase23_resolvent import adaptive_real_transform
    n=len(order);where=[0]*n
    for k,j in enumerate(order):where[j]=k
    x=[pow(z,where[j],P) for j in range(n)]
    return adaptive_real_transform(x,engine)[0]
