"""Phase 36: quantitative Fourier projective-phase barriers.

The inequalities in THEOREM.md cover arbitrary nonzero complex masks;
these utilities calculate bounds and finite-size controls, not a new FFT.
"""
from __future__ import annotations
import math
import numpy as np
from phase36_two_mask import CyclicMarkovGreen, cycle_from_seed, fourier_matrix


def phase_matrix(B):
    B=np.asarray(B,dtype=complex)
    if np.any(np.abs(B)==0):
        raise ValueError('phase matrix requires every entry nonzero')
    return B/np.abs(B)


def phase_rank_bound(n,r):
    """Any diagonal-gauged matrix with entrywise phase rank <= r."""
    if not 0<=r<=n: raise ValueError('rank must be from 0 to N')
    return 0.5*math.sqrt(1-r/n)


def outer_phase_rank_bound(n,r,da,dc):
    """A,C are delta-close to I in spectral norm, B phase-rank <= r."""
    assert 0<=da<1 and 0<=dc<1
    scale=(1-da)*(1-dc)
    return max(0.,scale*(1+phase_rank_bound(n,r))-1)



def necessary_middle_phase_rank(n,da,dc,maximum_spectral_error=0.):
    """Necessary rank for phase(B) in A D1 B D2 C to approximate F.

    Bound follows from outer_phase_rank_bound and makes no condition-number
    assumption about B or its diagonal masks. Returns a conservative integer.
    """
    assert n>=2 and 0<=da<1 and 0<=dc<1 and maximum_spectral_error>=0
    scale=(1-da)*(1-dc)
    eps=1/scale-1
    allowed=eps+maximum_spectral_error/scale
    if allowed>=0.5:return 0
    return max(0,min(n,math.ceil(n*(1-4*allowed**2)-1e-12)))

def root_phase_cyclic_green(n,k,rho=0.75,seed=36101):
    """Complex Green with alpha=rho*exp(2pi i k/N), phase-rank exactly 1."""
    cyc=cycle_from_seed(n,seed)
    G0=CyclicMarkovGreen(cyc,rho).dense()/(1-rho)
    phases=np.empty(n,dtype=complex)
    zeta=np.exp(2j*math.pi*k/n)
    for j,idx in enumerate(cyc):phases[idx]=zeta**j
    conjugated=phases[:,None]*G0*np.conjugate(phases)[None,:]
    # Construct independently via polynomial of W; inverse has coefficients
    # sum_d alpha^d W^d / (1-alpha^N).
    positions=np.empty(n,dtype=np.int64)
    for j,idx in enumerate(cyc):positions[idx]=j
    d=(positions[:,None]-positions[None,:])%n
    alpha=rho*zeta
    direct=alpha**d/(1-alpha**n)
    return conjugated,direct,G0,phases


def exact_four_point_certificate():
    """Compute four-point Fourier cross-ratio in Q(i), exact with SymPy."""
    import sympy as sp
    n=4
    eta=sp.Rational(1,100)
    beta=sp.Rational(3,4)
    def K(cycle):
        position={idx:i for i,idx in enumerate(cycle)}
        return sp.Matrix(n,n,lambda a,b:(1-beta)*beta**((position[a]-position[b])%n)/(1-beta**n))
    A=(1-eta)*sp.eye(n)+eta*K([0,2,1,3])
    C=(1-eta)*sp.eye(n)+eta*K([3,1,0,2])
    F=sp.Matrix(n,n,lambda a,b:(-sp.I)**(a*b))
    T=A.inv()*F*C.inv()
    ratio=sp.cancel(T[1,1]*T[0,0]/(T[1,0]*T[0,1]))
    imaginary=sp.simplify(sp.im(sp.expand_complex(ratio)))
    assert imaginary!=0
    return dict(N=4,exact_cross_ratio=str(ratio),
                imaginary_numerator=str(sp.numer(imaginary)),
                imaginary_denominator=str(sp.denom(imaginary)),
                imaginary_sign='negative' if imaginary<0 else 'positive',
                exact_nonreal=True)


def complex_gauge_audit(n):
    C,D,G0,phase=root_phase_cyclic_green(n,3 if n>4 else 1)
    err=float(np.max(np.abs(C-D)))
    pm=phase_matrix(D)
    singular=np.linalg.svd(pm,compute_uv=False)
    rank=int(np.sum(singular>1e-8*singular[0]))
    return dict(N=n,complex_cyclic_gauge_error=err,phase_rank=rank,
                phase_rank_floor=phase_rank_bound(n,rank),
                stronger_positive_floor=max(phase_rank_bound(n,1), math.sqrt((1-math.sqrt(math.gcd(2,n)/n))/2)))


if __name__=='__main__':
    for n in (4,8,16,32,64):
        print(complex_gauge_audit(n))
    print(exact_four_point_certificate())


def complex_single_cycle_phase_certificate(n,seed=36131):
    """Unit-modulus, 2Nth-root coupling: FULL phase rank but <=2 cross-ratios.

    G=(I-alpha W)^-1 with alpha=exp(pi*i/n), alpha**n=-1.
    In cycle-position order, its phase matrix is diagonally equivalent to
    H[i,j] = -1 (i<j) else 1. det(H)=2**(n-1) exactly.
    Moreover each 2x2 entrywise cross-ratio is either +1 or -1, since
    alpha**(n*Delta)=(-1)**Delta for Delta in {-1,0,1}.
    """
    assert n>=4
    cyclic=cycle_from_seed(n,seed)
    pos=np.empty(n,dtype=np.int64)
    for j,idx in enumerate(cyclic):pos[idx]=j
    alpha=np.exp(1j*np.pi/n)
    d=(pos[:,None]-pos[None,:])%n
    G=alpha**d/(1-alpha**n)
    Phi=phase_matrix(G)
    singular=np.linalg.svd(Phi,compute_uv=False)
    rows=[0,1,n//2,n-1];cols=[0,1,n//2,n-1]
    values=set()
    for i in range(len(rows)):
        for j in range(i+1,len(rows)):
            for k in range(len(cols)):
                for l in range(k+1,len(cols)):
                    p,q=rows[i],rows[j]
                    r,s=cols[k],cols[l]
                    ratio=G[p,r]*G[q,s]/(G[p,s]*G[q,r])
                    values.add(int(round(ratio.real)))
                    assert abs(ratio.imag)<1e-11
                    assert abs(abs(ratio)-1)<1e-10
    return dict(N=n,phase_rank=n,normalized_min_singular=float(singular[-1]/singular[0]),
                phase_determinant_magnitude_exact_formula=f'2^{n-1}',
                crossratio_value_set=sorted(values),
                Fourier_crossratio_value_count=n if n%4==0 else None,
                Weyl_Fourier_equivalent=False)


def general_cyclic_phase_rank(n,theta):
    """Rank of entrywise phase matrix for alpha=rho*exp(i theta), rho>0.

    Provided alpha != 0 and alpha**n != 1. Rank is 1 if exp(i*n*theta)=1,
    otherwise N. This function is only a numerical gauge demonstration;
    the exact mathematical criterion is in THEOREM.md.
    """
    z=np.exp(1j*n*theta)
    return 1 if abs(z-1)<1e-10 else n
