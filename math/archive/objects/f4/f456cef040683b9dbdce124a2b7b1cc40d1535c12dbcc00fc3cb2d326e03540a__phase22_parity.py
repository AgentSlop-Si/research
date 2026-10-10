"""Exact Fourier parity splitting F = H Q C.

H: real reflection/Haar-pair transform with O(N) apply and inverse.
Q: diagonal values 1 and -i (O(N) apply).
C: real orthogonal cosine/sine residual; currently executed via direct
O(N^2) dense matrix or an existing fast transform O(N log N).
This is NOT a new sub-NlogN Fourier algorithm.
"""
from __future__ import annotations
from phase22_gram import MOD,root,sqrt_mod,fft_matrix,transpose,matmul,identity


def parity_factors(n:int):
    """Dense certificate matrices H,Q,C; creation O(N^3) for small tests.
    For production use apply_H/apply_Ht instead of forming H.
    """
    if n<4 or n&(n-1):raise ValueError('power-of-two n>=4 required')
    h=n//2
    inv_sqrt2=pow(sqrt_mod(2),-1,MOD)
    H=[[0]*n for _ in range(n)]
    H[0][0]=1
    H[h][1]=1
    for j in range(1,h):
        H[j][j+1]=inv_sqrt2
        H[n-j][j+1]=inv_sqrt2
        H[j][h+j]=inv_sqrt2
        H[n-j][h+j]=-inv_sqrt2%MOD
    imaginary_unit_negative=pow(root(n),n//4,MOD) # -i
    diag=[1]*(h+1)+[imaginary_unit_negative]*(h-1)
    F=fft_matrix(n)
    HtF=matmul(transpose(H),F)
    C=[[v*pow(diag[i],-1,MOD)%MOD for v in row] for i,row in enumerate(HtF)]
    return H,diag,C


def apply_H(x:list[int])->list[int]:
    """O(N) multiplication H x; H = H^T only for N<=? (not assumed)."""
    n=len(x);h=n//2
    r=pow(sqrt_mod(2),-1,MOD)
    out=[0]*n
    out[0]=x[0];out[h]=x[1]
    for j in range(1,h):
        a=x[j+1];b=x[h+j]
        out[j]=(a+b)*r%MOD
        out[n-j]=(a-b)*r%MOD
    return out


def apply_Ht(x:list[int])->list[int]:
    n=len(x);h=n//2
    r=pow(sqrt_mod(2),-1,MOD)
    out=[0]*n
    out[0]=x[0];out[1]=x[h]
    for j in range(1,h):
        a=x[j];b=x[n-j]
        out[j+1]=(a+b)*r%MOD
        out[h+j]=(a-b)*r%MOD
    return out


def residual_entropy(n:int)->tuple[float,float]:
    """Compute numerical C entropy for audit; O(N^2)."""
    import math
    h=n//2
    entropy=0.
    for j in range(n):
        if j==0 or j==1:entropy+=math.log2(n)
        elif 2<=j<=h:
            t=j-1
            for k in range(n):
                p=2*math.cos(2*math.pi*t*k/n)**2/n
                if p>0: entropy-=p*math.log2(p)
        else:
            t=j-h
            for k in range(n):
                p=2*math.sin(2*math.pi*t*k/n)**2/n
                if p>0: entropy-=p*math.log2(p)
    return entropy,n*(math.log2(n)-1)

if __name__=='__main__':
    for n in (8,16,32,64):
        H,q,C=parity_factors(n)
        print(n, 'orthogonal residual',matmul(transpose(C),C)==identity(n),
              'entropy', tuple(round(z,4) for z in residual_entropy(n)))


def real_rotation_coefficients(n:int):
    """Return (cos(theta_j), sin(theta_j)) in Fp for theta_j=2pi*j/n.
    Basis sym/anti ordering is the one from parity_factors().
    """
    w=root(n); q=pow(w,n//4,MOD) # -i
    complex_i=pow(q,-1,MOD)
    inv2=pow(2,-1,MOD)
    inv2i=pow(2*complex_i%MOD,-1,MOD)
    return [((pow(w,j,MOD)+pow(w,-j,MOD))*inv2%MOD,
             (pow(w,-j,MOD)-pow(w,j,MOD))*inv2i%MOD)
            for j in range(1,n//2)]


def apply_R(x:list[int])->list[int]:
    """Sparse O(N) real-rotation operator R, satisfying C Z = R C."""
    n=len(x);h=n//2
    coeffs=real_rotation_coefficients(n)
    out=[0]*n
    out[0]=x[0];out[1]=(-x[1])%MOD
    for j,(c,s) in enumerate(coeffs,1):
        a=j+1;b=h+j
        out[a]=(c*x[a]-s*x[b])%MOD
        out[b]=(s*x[a]+c*x[b])%MOD
    return out


def real_C_first_column(n:int)->list[int]:
    inv_sqrt2=pow(sqrt_mod(2),-1,MOD)
    sc=pow(sqrt_mod(n),-1,MOD)
    h=n//2
    return [sc,sc]+[(2*sc*inv_sqrt2)%MOD]*(h-1)+[0]*(h-1)


def cyclic_shift(x):
    return [x[-1]]+x[:-1]


def real_covariance_gate(oracle,n:int,seed=22,trials=2):
    """Finite-field Monte Carlo exact rejection for C Z = R C; first
    column is separately calibrated. Uses 1+2*trials circuit calls, and
    O(N) other work. Passing finitely many randomized trials is NOT a proof.
    """
    import random
    e=[0]*n;e[0]=1
    correct_seed=oracle(e)==real_C_first_column(n)
    rng=random.Random(seed)
    failures=0
    for _ in range(trials):
        v=[rng.randrange(MOD) for _ in range(n)]
        out=oracle(v)
        lhs=oracle(cyclic_shift(v))
        rhs=apply_R(out)
        failures+=sum(a!=b for a,b in zip(lhs,rhs))
    return {'calibration':correct_seed,'defect_entries':failures,
            'passes_sample':correct_seed and not failures,
            'circuit_calls':1+2*trials}
