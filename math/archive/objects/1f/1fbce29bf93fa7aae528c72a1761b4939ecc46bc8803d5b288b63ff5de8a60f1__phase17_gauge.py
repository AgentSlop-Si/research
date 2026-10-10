"""HERO #0 Phase 17: two-sided gauge obstruction for Green/FFT research.

Arithmetic-level mathematics and finite-field tests. This is NOT an O(N) FFT.
Includes a complete monomial-Fourier intertwiner formula and a constant
quantitative error barrier for two independently gauged half-grid symmetries.
"""
from __future__ import annotations
import math
import numpy as np

P = 65537
GEN = 3


def half_grid_permutation(s: int) -> np.ndarray:
    if s < 2 or s % 2:
        raise ValueError('even grid side s>=2 required')
    return np.asarray([s*x+((y+s//2)%s) for x in range(s)
                       for y in range(s)], dtype=np.int64)


def unitary_fourier(n: int) -> np.ndarray:
    ids = np.arange(n, dtype=np.int64)
    return np.exp((-2j * np.pi/n) * np.outer(ids, ids))/np.sqrt(n)


def ratio_matrix(s: int) -> np.ndarray:
    """H[k,j]=omega^(k*tau(j)-tau(k)*j): independent of gauge weights."""
    tau = half_grid_permutation(s)
    k = np.arange(s*s, dtype=np.int64)
    exponent = (np.outer(k, tau) - np.outer(tau, k)) % (s*s)
    return np.exp((-2j*np.pi/(s*s))*exponent)


def ratio_c(s: int) -> float:
    if s < 2 or s % 2:
        raise ValueError('even s required')
    return 1.0/(s*math.sin(math.pi/s))


def ratio_singular_values(s: int) -> np.ndarray:
    """Exactly four potentially nonzero singular values, with zeros omitted."""
    n = s*s
    c = ratio_c(s)
    small = max(0.0, 0.25-c*c)
    return np.asarray([n*(0.5+c), n*math.sqrt(small),
                       n*math.sqrt(small), n*(0.5-c)])


def normalized_error_gap(s: int) -> float:
    """Lower bound for ||U-T||_F/sqrt(N) and ||U-T||_2 for phase gauges."""
    return 0.5*math.sqrt(max(0.0, 1.0-2.0*ratio_c(s)))


def rank_k_error_gap(s: int, k: int) -> float:
    """Uniform lower bound for phase-gauged core plus any rank-k correction."""
    n=s*s
    if k < 0 or k > n:
        raise ValueError('rank k must be in [0,N]')
    rho=2*ratio_c(s)
    return 0.5*math.sqrt(max(0.0,1.0-rho-8.0*k/n))


def minimum_rank_budget(s: int) -> int:
    """Necessary integer rank correction for exact Fourier, phase gauges."""
    n=s*s
    # Subtract tiny numerical tolerance to avoid a false upward rounding at equality.
    return math.ceil(n*(1.0-2*ratio_c(s))/8.0-1e-12)


def gauged_permutation_weights(s: int, diagonal: np.ndarray) -> np.ndarray:
    """Q = diag(diagonal) Pi diag(diagonal)^-1 has Q[tau(j),j]=q[j]."""
    tau=half_grid_permutation(s)
    diagonal=np.asarray(diagonal)
    if np.any(diagonal==0):
        raise ValueError('nonzero diagonal needed')
    return diagonal[tau]/diagonal


def optimal_intertwiner_for_gauges(s: int, input_diagonal: np.ndarray,
                                   output_diagonal: np.ndarray) -> np.ndarray:
    """Frobenius-closest T to U_N with T Q = R T, for fixed phase gauges.

    Q = D_in Pi D_in^-1, R=D_out Pi D_out^-1 must be unitary involutions.
    The result need not have a fast O(N) execution plan.
    """
    din=np.asarray(input_diagonal)
    dout=np.asarray(output_diagonal)
    if (not np.allclose(abs(din),1) or not np.allclose(abs(dout),1)):
        raise ValueError('phase-only diagonals required')
    tau=half_grid_permutation(s)
    n=s*s
    q=gauged_permutation_weights(s,din)
    r=gauged_permutation_weights(s,dout)
    Q=np.zeros((n,n),dtype=complex)
    R=np.zeros((n,n),dtype=complex)
    Q[tau,np.arange(n)]=q
    R[tau,np.arange(n)]=r
    U=unitary_fourier(n)
    return (U+R@U@Q)/2


def two_sided_defect(s: int, input_diagonal: np.ndarray,
                     output_diagonal: np.ndarray) -> np.ndarray:
    """Calculate UQ-RU, where Q=D_in Pi D_in^-1, R=D_out Pi D_out^-1."""
    tau=half_grid_permutation(s)
    U=unitary_fourier(s*s)
    q=gauged_permutation_weights(s,input_diagonal)
    r=gauged_permutation_weights(s,output_diagonal)
    return U[:,tau]*q[None,:]-r[tau,None]*U[tau,:]


def primitive_root(n: int, p: int=P, generator: int=GEN) -> int:
    if (p-1) % n:
        raise ValueError('n must divide p-1')
    root=pow(generator,(p-1)//n,p)
    # All tested lengths in this project are powers of two.
    if n >=2 and n & (n-1)==0 and pow(root,n//2,p)==1:
        raise AssertionError('root is not primitive')
    return root


def modular_fourier(n: int, p: int=P, generator: int=GEN,
                    inverse: bool=False) -> np.ndarray:
    z=primitive_root(n,p,generator)
    if inverse:
        z=pow(z,-1,p)
    powers=np.asarray([pow(z,k,p) for k in range(n)],dtype=np.int64)
    ids=np.arange(n,dtype=np.int64)
    return powers[np.outer(ids,ids)%n]


def mod_matmul(A: np.ndarray, B: np.ndarray, p: int=P) -> np.ndarray:
    A=np.asarray(A,dtype=np.int64)%p
    B=np.asarray(B,dtype=np.int64)%p
    assert A.shape[1]*(p-1)**2 < 2**63, 'potential 64bit overflow'
    return (A@B)%p


def modrank(A: np.ndarray, p: int=P) -> int:
    """Exact Gaussian rank over GF(p); no floating point."""
    A=np.array(A,dtype=np.int64,copy=True)%p
    m,n=A.shape; row=0
    for col in range(n):
        candidates=np.flatnonzero(A[row:,col])
        if not len(candidates):
            continue
        piv=row+int(candidates[0])
        if piv!=row:
            A[[row,piv]]=A[[piv,row]]
        pivot=int(A[row,col])
        A[row,col:]=(A[row,col:]*pow(pivot,-1,p))%p
        for i in range(row+1,m):
            t=int(A[i,col])
            if t:
                A[i,col:]=(A[i,col:]-t*A[row,col:])%p
        row+=1
        if row==m:
            break
    return row


def monomial_normalizer(n: int, u: int, a: int, b: int,
                        c: int=1, p: int=P) -> tuple[np.ndarray,np.ndarray]:
    """Exact (Q,R) with F_N Q=R F_N for affine input perm u*j+b.

    Q e_j = c*z^(a*j) e_(u*j+b).
    R e_m = c*z^(u^-1*(m-a)*b) e_(u^-1*(m-a)).
    """
    ui=pow(u,-1,n)
    z=primitive_root(n,p)
    Q=np.zeros((n,n),dtype=np.int64)
    R=np.zeros((n,n),dtype=np.int64)
    for j in range(n):
        Q[(u*j+b)%n,j] = (c*pow(z,(a*j)%n,p))%p
    for m in range(n):
        target=ui*(m-a)%n
        R[target,m]=(c*pow(z,(target*b)%n,p))%p
    return Q,R


def modular_gauged_symmetry_defect(s: int, din: np.ndarray,
                                   dout: np.ndarray, p: int=P) -> np.ndarray:
    n=s*s
    tau=half_grid_permutation(s)
    din=np.asarray(din,dtype=np.int64)%p
    dout=np.asarray(dout,dtype=np.int64)%p
    if np.any(din==0) or np.any(dout==0):
        raise ValueError('nonzero diagonal required')
    qi=np.asarray([int(din[tau[j]])*pow(int(din[j]),-1,p)%p for j in range(n)],dtype=np.int64)
    ro=np.asarray([int(dout[tau[j]])*pow(int(dout[j]),-1,p)%p for j in range(n)],dtype=np.int64)
    F=modular_fourier(n,p)
    return (F[:,tau]*qi[None,:]-ro[tau,None]*F[tau,:])%p


def margulis_permutations(s: int) -> list[np.ndarray]:
    maps=[]
    for typ in range(4):
        arr=[]
        for x in range(s):
            for y in range(s):
                if typ==0: xx,yy=(x+2*y)%s,y
                elif typ==1: xx,yy=(x+2*y+1)%s,y
                elif typ==2: xx,yy=x,(y+2*x)%s
                else: xx,yy=x,(y+2*x+1)%s
                arr.append(xx*s+yy)
        maps.append(np.asarray(arr,dtype=np.int64))
    return maps


def green_of_weighted_perm(perm: np.ndarray, weights: np.ndarray,
                           p: int=P) -> np.ndarray:
    """Exact modular Green inverse of I-P, suitable for small verification."""
    n=len(perm)
    perm=np.asarray(perm,dtype=np.int64)
    weights=np.asarray(weights,dtype=np.int64)%p
    A=np.eye(n,dtype=np.int64)
    A[np.arange(n),perm]=(A[np.arange(n),perm]-weights)%p
    # Gauss Jordan on the augmented matrix, including any fixed points.
    aug=np.concatenate([A,np.eye(n,dtype=np.int64)],axis=1)
    for col in range(n):
        rows=np.flatnonzero(aug[col:,col])
        if len(rows)==0:
            raise ValueError('singular Green')
        piv=col+int(rows[0])
        if piv!=col:
            aug[[col,piv]]=aug[[piv,col]]
        aug[col,:]=(aug[col,:]*pow(int(aug[col,col]),-1,p))%p
        for row in range(n):
            if row==col:continue
            t=int(aug[row,col])
            if t:
                aug[row,:]=(aug[row,:]-t*aug[col,:])%p
    return aug[:,n:]


def make_gauge_from_monomial(perm: np.ndarray, weights: np.ndarray,
                            p: int=P) -> np.ndarray:
    """Find diagonal D such that D Pi D^-1=Q, if involutory fixed-free Q."""
    n=len(perm)
    d=np.zeros(n,dtype=np.int64)
    for j in range(n):
        if d[j]:continue
        k=int(perm[j])
        if int(perm[k])!=j:
            raise ValueError('not an involution')
        if k==j:
            if int(weights[j])%p!=1:
                raise ValueError('invalid fixed point')
            d[j]=1
        else:
            d[j]=1
            d[k]=int(weights[j])%p
            if int(weights[j])*int(weights[k])%p!=1:
                raise ValueError('monomial not involutory')
    return d

if __name__ == '__main__':
    for s in [2,4,6,8,10,12]:
        print('s=',s,'rank4 singular values / N=',ratio_singular_values(s)/(s*s),
              'phase gauge FFT operator gap >=',normalized_error_gap(s))
