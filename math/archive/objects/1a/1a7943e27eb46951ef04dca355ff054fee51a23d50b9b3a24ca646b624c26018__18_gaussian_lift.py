"""Hero #0 phase 3b: Gaussian 4x oversampling + composite Green projection.

Mathematical target:
    Arbitrary fresh complex x, ANY length N (including primes), every output.
    For L=max(12,ceil(log(N)/4)), sigma^2=L, H=ceil(N^(1/3)),
    9 independent rows and complex coordinatewise medians:
    O(N log log N) ideal complex/word operations and
    ||output-U_N x||_infty = O(N^(-1/3)||x||_2) with probability 1-o(1).

The proof uses Gaussian Poisson summation, the previously established
composite Green projector covariance, fixed-overhead prime padding to Q~4N,
and stride-4 reuse of short FFT convolution windows. See RESEARCH.md.

This code uses NumPy complex128 and exp; not a fixed-precision theorem. Slow
full-length FFTs are only used in separate test oracles, NEVER in this engine.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np
from composite_cycle_core import one_row_estimate,draw_state


def next_power_of_two(x:int)->int:
    return 1 << (int(x)-1).bit_length()


@dataclass(frozen=True)
class GaussianPlan:
    n:int
    c:int
    q:int
    m:int
    k:int
    slack:int
    halfwidth:int
    buckets:int
    sigma2:float
    block:int
    center:int

    @classmethod
    def create(cls,n:int,oversample:int=4,halfwidth:int|None=None,
               buckets:int|None=None,sigma2:float|None=None,
               m:int|None=None,block:int|None=None):
        if n<64:raise ValueError('prototype requires N>=64')
        if oversample<2:raise ValueError('oversample needs >=2')
        approx_q=oversample*n
        m=max(2,math.ceil(math.log2(approx_q))) if m is None else int(m)
        q=m*math.ceil(approx_q/m)
        k=q//m
        if k<m:raise ValueError('need K>=M')
        L=max(12,math.ceil(.25*math.log(n))) if halfwidth is None else int(halfwidth)
        H=math.ceil(n**(1./3.)) if buckets is None else int(buckets)
        if L<2 or H<1:raise ValueError('L>=2,H>=1')
        if 2*L+5>=q:raise ValueError('Gaussian support too wide')
        sig2=float(L if sigma2 is None else sigma2)
        if sig2<=0:raise ValueError('sigma2 must be positive')
        B=max(8,2*L) if block is None else int(block)
        if B<1:raise ValueError('block length positive')
        return cls(n,oversample,q,m,k,q-oversample*n,L,H,sig2,B,(n-1)//2)

    @property
    def tau(self)->float:
        return max(self.center,self.n-1-self.center)/self.q

    @property
    def trunc_fft_size(self)->int:
        return next_power_of_two(self.c*(self.block-1)+4*self.halfwidth+1)


def phase_bucket(k:int,p:GaussianPlan)->tuple[int,int]:
    offs, rem=divmod(k*p.slack,p.n)
    return offs, int((rem*p.buckets)//p.n)


def segment_runs(p:GaussianPlan):
    state=(*phase_bucket(0,p),)
    last=0
    for k in range(1,p.n):
        newer=phase_bucket(k,p)
        if newer!=state:
            yield last,k,state[0],state[1]
            last=k;state=newer
    yield last,p.n,state[0],state[1]


def prepare_centered_weighted_input(x:np.ndarray,p:GaussianPlan)->np.ndarray:
    arr=np.asarray(x,dtype=np.complex128).reshape(-1)
    if arr.size!=p.n:raise ValueError('invalid input length')
    centered=(np.arange(p.n,dtype=float)-p.center)/p.q
    # one O(N) preconditioning pass. Exact-complex model can generate these
    # quadratic exponential coefficients by a two-ratio O(N) recurrence.
    weights=np.exp(np.pi*p.sigma2*centered*centered)/math.sqrt(p.sigma2)
    y=np.zeros(p.q,dtype=np.complex128)
    y[(np.arange(p.n,dtype=np.int64)-p.center)%p.q]=arr*weights
    return y


def gaussian_weights(p:GaussianPlan,theta:float)->np.ndarray:
    ell=np.arange(-p.halfwidth,p.halfwidth+1,dtype=float)
    return np.exp(-np.pi*(ell-theta)**2/p.sigma2)


def gaussian_resample(zq:np.ndarray,p:GaussianPlan)->np.ndarray:
    """O(N log L) stride-c FIR gridding; Q-FFT input is already supplied.

    For each segment, floor(k*Q/N)=c*k+constant. Reuse a theta-bucket
    short convolution and read every c-th output, with FFT size O(c*L).
    """
    Z=np.asarray(zq,dtype=np.complex128).reshape(-1)
    if Z.size!=p.q:raise ValueError('spectrum must have Q entries')
    result=np.empty(p.n,dtype=np.complex128)
    fsize=p.trunc_fft_size
    window_size=p.c*(p.block-1)+2*p.halfwidth+1
    offsets=np.arange(window_size,dtype=np.int64)
    fft_kernel_cache={}
    block_positions=2*p.halfwidth+p.c*np.arange(p.block)
    for start,stop,grid_off,bucket in segment_runs(p):
        filt_fft=fft_kernel_cache.get(bucket)
        if filt_fft is None:
            theta=(bucket+.5)/p.buckets
            filt_fft=np.fft.fft(gaussian_weights(p,theta)[::-1],n=fsize)
            fft_kernel_cache[bucket]=filt_fft
        pos=start
        while pos<stop:
            actual=min(p.block,stop-pos)
            base=(p.c*pos+grid_off-p.halfwidth)%p.q
            window=Z[(base+offsets)%p.q]
            conv=np.fft.ifft(np.fft.fft(window,n=fsize)*filt_fft)
            result[pos:pos+actual]=conv[block_positions[:actual]]
            pos+=actual
    # center-shifted transform: e^{-2 pi i k center/N} multiplies back.
    kk=np.arange(p.n,dtype=float)
    phase=np.exp(-2j*np.pi*(kk*p.center/p.n))
    return result*math.sqrt(p.q/p.n)*phase


def slow_gaussian_resample(zq:np.ndarray,p:GaussianPlan,quantize:bool=True)->np.ndarray:
    """O(N L) independent oracle, used ONLY for testing short-FFT gridding."""
    z=np.asarray(zq,dtype=np.complex128).reshape(-1)
    d=np.arange(-p.halfwidth,p.halfwidth+1,dtype=np.int64)
    out=np.empty(p.n,dtype=np.complex128)
    for k in range(p.n):
        off,bucket=phase_bucket(k,p)
        theta=(bucket+.5)/p.buckets if quantize else (k*p.slack%p.n)/p.n
        idx=(p.c*k+off+d)%p.q
        out[k]=gaussian_weights(p,theta)@z[idx]
    kk=np.arange(p.n,dtype=float)
    return out*math.sqrt(p.q/p.n)*np.exp(-2j*np.pi*kk*p.center/p.n)


def gaussian_projected_row(x:np.ndarray,p:GaussianPlan,rng:np.random.Generator)->np.ndarray:
    z=prepare_centered_weighted_input(x,p)
    state=draw_state(p.q,rng)
    Y=one_row_estimate(z,p.m,state)
    return gaussian_resample(Y,p)


def gaussian_robust(x:np.ndarray,p:GaussianPlan,rows:int=9,seed:int=20261010)->np.ndarray:
    if rows<1 or rows%2==0:raise ValueError('rows must be positive odd')
    rng=np.random.default_rng(seed)
    vals=np.stack([gaussian_projected_row(x,p,rng) for _ in range(rows)])
    return np.median(vals.real,axis=0)+1j*np.median(vals.imag,axis=0)


def analytic_error_budget(p:GaussianPlan):
    """Conservative theorem bounds, using phi(Q) computed exactly for test sizes.

    D: deterministic error <= D ||x||2 for each frequency.
    V: mean square RANDOM error per row <= V ||x||2**2 (projector sampling).
    """
    s2=p.sigma2
    tau=p.tau
    L=p.halfwidth
    base=math.pi*s2*(1-2*tau)
    if base<=0:raise ValueError('need time support strictly inside half of Q')
    ep=math.exp(-base)
    alias=2*ep/(1-ep)
    # excluded offsets d>L; min |d-theta| is L, the bound below is safe.
    tail=2*math.exp(-math.pi*L**2/s2)/(1-math.exp(-2*math.pi*L/s2))
    preweight=math.exp(math.pi*s2*tau*tau)
    D=math.pi*tau/p.buckets+alias+preweight*tail/math.sqrt(s2)
    # Ramanujan covariance upper bound from composite Green theorem.
    t=p.q;phi=t
    d=2
    while d*d<=t:
        if t%d==0:
            phi=phi//d*(d-1)
            while t%d==0:t//=d
        d+=1
    if t>1:phi=phi//t*(t-1)
    unit_var=p.m*(p.m-1)/phi
    rms=(math.sqrt(p.q/p.n)*(1+1/math.sqrt(s2))*preweight*math.sqrt(unit_var))
    return {'deterministic_norm_bound':D,'noise_variance_norm_bound':rms*rms,
            'noise_std_norm_bound':rms,'phi_Q':phi,'pointwise_green_cov_bound':unit_var,
            'alias_bound':alias,'tail_bound':preweight*tail/math.sqrt(s2),
            'phase_round_bound':math.pi*tau/p.buckets,'max_preweight_amplification':preweight}


def work_profile(p:GaussianPlan,rows:int=9):
    runs=list(segment_runs(p))
    chunks=sum(math.ceil((end-start)/p.block) for start,end,_,_ in runs)
    fsize=p.trunc_fft_size
    return {
        'n':p.n,'q':p.q,'m':p.m,'k':p.k,'slack':p.slack,'L':p.halfwidth,
        'H':p.buckets,'spectrum_prime_length':p.n,
        'number_of_segments':len(runs),'fft_chunks_per_row':chunks,
        'fir_fft_size':fsize,'max_filter_count':p.buckets,
        'formula_arith_proxy': rows*(p.q + p.k*math.log2(p.k) +
                2*chunks*fsize*math.log2(fsize))+
                p.buckets*(2*p.halfwidth+1)*math.log2(max(2,2*p.halfwidth+1)),
        'longest_fft_in_executor':max(p.k,fsize),
        'baseline_N_FFT_arith_proxy':p.n*math.log2(p.n),
    }


if __name__=='__main__':
    p=GaussianPlan.create(1009)
    rng=np.random.default_rng(44)
    x=rng.normal(size=p.n)+1j*rng.normal(size=p.n)
    y=gaussian_robust(x,p,rows=9)
    ref=np.fft.fft(x)/math.sqrt(p.n)
    print(p)
    print('max normalized error',np.max(abs(y-ref))/np.linalg.norm(x))
    print(analytic_error_budget(p))
    print(work_profile(p))


def stronger_local_noise_budget(p:GaussianPlan):
    """Sharper *theorem-candidate* variance via cancellation of Gaussian weights.

    Compare the interpolated projected spectrum with the exactly dewindowed
    local Green error, instead of applying Minkowski to all grid bins. Input
    and output Gaussian weights almost cancel across O(M) block displacements.
    This is valid for the padded-centered support used by the algorithm.
    """
    tau=p.tau
    tau_p=tau+p.m/p.q
    if tau_p >= .5:
        raise ValueError('centered support and its block neighborhood must stay within Q/2')
    sigma2=p.sigma2
    L=p.halfwidth
    amp=math.exp(math.pi*sigma2*tau*tau)
    near=math.exp(math.pi*sigma2*(2*tau*p.m/p.q+(p.m/p.q)**2))
    decay=math.pi*sigma2*(1-2*tau_p)
    e=math.exp(-decay)
    alias=2*e/(1-e)
    tail=2*math.exp(-math.pi*L*L/sigma2)/(1-math.exp(-2*math.pi*L/sigma2))
    V=analytic_error_budget(p)['pointwise_green_cov_bound']
    # The projected signal Pz stays in at most the block-neighbor support of
    # centered input. Bound it conservatively by the whole Q-circle.
    remainder=math.sqrt(p.q/p.n)*p.m*amp*(alias+tail/math.sqrt(sigma2))
    phase=math.pi*tau/p.buckets
    noise_var=(p.q/p.n)*near*near*V
    return {
        'better_deterministic_norm_bound':phase+remainder,
        'phase_round_bound':phase,
        'projected_Gaussian_remainder_bound':remainder,
        'unwindowed_local_covariance_norm_bound':noise_var,
        'unwindowed_local_covariance_std_bound':math.sqrt(noise_var),
        'nearby_preconditioner_ratio_bound':near,
        'centered_extended_tau':tau_p,
        'local_Gaussian_alias_bound':alias,
        'local_Gaussian_weight_tail_bound':tail,
    }
