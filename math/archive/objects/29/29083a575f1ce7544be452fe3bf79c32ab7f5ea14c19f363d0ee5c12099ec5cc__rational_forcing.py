"""Phase17 all-length exact nonunitary Green forcing with K-sparse residuals.

For K nonzero coefficients r_j, form the rational series
  Z(t)=sum_j r_j/(1-omega**j*t) = P(t)/D(t), deg(D)=K, deg(P)<K.
Produce the first N Fourier coordinates z_k=[t**k]Z by repeated
block convolutions of length O(K), without any N-length FFT.

Complexity over an NTT-friendly field: O(N log(K+1) + K log^2(K+1))
field operations for K>=1 (plus O(N) graph preconditioning/Green solve).
Generic K=Theta(N) falls back to length-N Bluestein O(N log N).
All operations below are exact modular arithmetic; no claims about bit-time
or generic sub-NlogN algorithms are made.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from green_sparse import CyclicSolver, Cost, P0, G0


@dataclass
class PolyStats:
    ntt_calls: int=0
    ntt_processed: int=0
    butterflies: int=0
    field_mults: int=0
    field_adds: int=0
    field_inversions: int=0
    coeff_writes: int=0
    naive_mult_pairs: int=0
    conv_calls: int=0
    max_conv_len: int=0
    rational_merge_calls: int=0
    rational_blocks: int=0
    max_ntt_length: int=0
    max_den_degree: int=0
    cached_kernel_transforms: int=0
    cached_kernel_hits: int=0
    twiddle_tables_built: int=0
    twiddle_table_hits: int=0
    twiddle_plan_setup_mults: int=0
    _twiddle_plans: dict=field(default_factory=dict, repr=False)
    _inv_scales: dict=field(default_factory=dict, repr=False)
    def total_field_ops(self):
        return self.field_mults+self.field_adds+self.field_inversions


def prime_divisors(n):
    out=[]
    d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out


def general_root(n,p=P0,primitive_gen=G0):
    if n<2 or (p-1)%n:
        raise ValueError('n must divide p-1 and n>=2')
    w=pow(primitive_gen,(p-1)//n,p)
    assert pow(w,n,p)==1
    if any(pow(w,n//q,p)==1 for q in prime_divisors(n)):
        raise ValueError('not a primitive root')
    return w


def nextpow2(x):
    return 1<<(max(1,x)-1).bit_length()


def pow_charged(x,e,p,stats:Optional[PolyStats]=None):
    """Implement canonical repeated squaring and charge its field products."""
    if e<0:
        if stats is not None:stats.field_inversions+=1
        x=pow(x,-1,p)
        e=-e
    result=1
    while e:
        if e&1:
            result=result*x%p
            if stats is not None:stats.field_mults+=1
        e>>=1
        if e:
            x=x*x%p
            if stats is not None:stats.field_mults+=1
    return result


def ntt(a,p,primitive_gen,invert=False,stats:Optional[PolyStats]=None):
    n=len(a)
    assert n and n&(n-1)==0 and (p-1)%n==0
    rev=0
    for i in range(1,n):
        bit=n>>1
        while rev&bit:
            rev^=bit
            bit>>=1
        rev^=bit
        if i<rev:a[i],a[rev]=a[rev],a[i]
    length=2
    while length<=n:
        h=length//2
        key=(p,primitive_gen,length,invert)
        if stats is not None and key in stats._twiddle_plans:
            twiddles=stats._twiddle_plans[key]
            stats.twiddle_table_hits+=1
        else:
            wlen=pow_charged(primitive_gen,(p-1)//length,p,stats)
            if invert:wlen=pow_charged(wlen,-1,p,stats)
            twiddles=[1]*h
            for j in range(1,h):twiddles[j]=twiddles[j-1]*wlen%p
            if stats is not None:
                stats._twiddle_plans[key]=twiddles
                stats.twiddle_tables_built+=1
                stats.field_mults+=max(0,h-1)
                stats.twiddle_plan_setup_mults+=max(0,h-1)
        for s in range(0,n,length):
            for j in range(h):
                u=a[s+j]
                v=a[s+j+h]*twiddles[j]%p
                a[s+j]=(u+v)%p
                a[s+j+h]=(u-v)%p
        if stats is not None:
            stats.butterflies+=n//2
            stats.field_mults+=n//2  # one twiddle product per butterfly
            stats.field_adds+=n
        length<<=1
    if invert:
        key=(p,n)
        if stats is not None and key in stats._inv_scales:
            scale=stats._inv_scales[key]
        else:
            scale=pow_charged(n,-1,p,stats)
            if stats is not None:stats._inv_scales[key]=scale
        for j in range(n):a[j]=a[j]*scale%p
        if stats is not None:stats.field_mults+=n
    if stats is not None:
        stats.ntt_calls+=1
        stats.ntt_processed+=n
        stats.max_ntt_length=max(stats.max_ntt_length,n)
        stats.coeff_writes+=n
    return a


def conv(a,b,p=P0,primitive_gen=G0,stats:Optional[PolyStats]=None):
    if not a or not b:return []
    output_len=len(a)+len(b)-1
    if stats is not None:
        stats.conv_calls+=1
        stats.max_conv_len=max(stats.max_conv_len,output_len)
    if len(a)*len(b)<=100:
        ans=[0]*output_len
        for i,va in enumerate(a):
            for j,vb in enumerate(b):ans[i+j]=(ans[i+j]+va*vb)%p
        if stats is not None:
            stats.naive_mult_pairs+=len(a)*len(b)
            stats.field_mults+=len(a)*len(b)
            stats.field_adds+=len(a)*len(b)
            stats.coeff_writes+=output_len
        return ans
    m=nextpow2(output_len)
    if (p-1)%m:raise ValueError('field cannot support this convolution length')
    aa=list(a)+[0]*(m-len(a))
    bb=list(b)+[0]*(m-len(b))
    ntt(aa,p,primitive_gen,stats=stats)
    ntt(bb,p,primitive_gen,stats=stats)
    for j in range(m):aa[j]=aa[j]*bb[j]%p
    if stats is not None:stats.field_mults+=m
    ntt(aa,p,primitive_gen,invert=True,stats=stats)
    return aa[:output_len]



class FixedKernelConvolver:
    """Within-one-call short NTT kernel sharing; setup and every use charged.

    Reuses transforms of the fixed denominator and inverse-series kernels
    across all frequency-output blocks. Cache is rebuilt for each transform
    and never depends on reusing any previous input vector.
    """
    def __init__(self,kernel,other_length,p=P0,primitive_gen=G0,
                 stats:Optional[PolyStats]=None):
        self.kernel=list(kernel)
        self.other_length=other_length
        self.p,self.gen,self.stats=p,primitive_gen,stats
        self.result_length=len(kernel)+other_length-1
        self.naive=(len(kernel)*other_length<=100)
        if self.naive:
            self.kernel_hat=None
        else:
            self.size=nextpow2(self.result_length)
            if (p-1)%self.size:raise ValueError('short kernel NTT unavailable')
            self.kernel_hat=self.kernel+[0]*(self.size-len(kernel))
            ntt(self.kernel_hat,p,primitive_gen,stats=stats)
            if stats is not None:stats.cached_kernel_transforms+=1

    def apply(self,operand):
        if len(operand)!=self.other_length:
            raise ValueError('fixed kernel convolution size mismatch')
        if self.naive:
            return conv(self.kernel,operand,self.p,self.gen,self.stats)
        q=self.stats
        vec=list(operand)+[0]*(self.size-len(operand))
        ntt(vec,self.p,self.gen,stats=q)
        for i in range(self.size):vec[i]=vec[i]*self.kernel_hat[i]%self.p
        if q is not None:
            q.field_mults+=self.size
            q.cached_kernel_hits+=1
            q.conv_calls+=1
            q.max_conv_len=max(q.max_conv_len,self.result_length)
        ntt(vec,self.p,self.gen,invert=True,stats=q)
        return vec[:self.result_length]

def polyadd(a,b,p=P0,stats:Optional[PolyStats]=None):
    n=max(len(a),len(b))
    out=[0]*n
    for j,v in enumerate(a):out[j]=v
    for j,v in enumerate(b):out[j]=(out[j]+v)%p
    if stats is not None:
        stats.field_adds+=len(b)
        stats.coeff_writes+=n
    return out


def rational_fraction(entries,omega,p=P0,primitive_gen=G0,
                      stats:Optional[PolyStats]=None):
    """Balanced sum of fractions: return P,D with sum_j r_j/(1-lambda_j t)."""
    data=[(j,z%p) for j,z in entries.items() if z%p]
    if not data:return [0],[1]
    if stats is not None:stats.max_den_degree=len(data)

    def merge(l,h):
        if h-l==1:
            j,z=data[l]
            lam=pow_charged(omega,j,p,stats)
            return [z],[1,(-lam)%p]
        m=(l+h)//2
        pl,dl=merge(l,m)
        pr,dr=merge(m,h)
        den=conv(dl,dr,p,primitive_gen,stats)
        t1=conv(pl,dr,p,primitive_gen,stats)
        t2=conv(pr,dl,p,primitive_gen,stats)
        num=polyadd(t1,t2,p,stats)
        if stats is not None:stats.rational_merge_calls+=1
        assert len(num)==len(den)-1
        return num,den
    num,den=merge(0,len(data))
    assert den[0]==1 and len(den)==len(data)+1
    return num,den


def inv_series(den, n,p=P0,primitive_gen=G0,stats:Optional[PolyStats]=None):
    """Newton: inv(den) mod t^n. Powers of two are fastest."""
    if not den or den[0]==0: raise ValueError('singular series')
    out=[pow_charged(den[0],-1,p,stats)]
    while len(out)<n:
        m=min(2*len(out),n)
        temp=conv(den[:m],out,p,primitive_gen,stats)[:m]
        term=[(-a)%p for a in temp]+[0]*max(0,m-len(temp))
        term[0]=(2-temp[0])%p
        out=conv(out,term,p,primitive_gen,stats)[:m]
    return out


def forcing_from_sparse(entries,n,omega,p=P0,primitive_gen=G0,
                        stats:Optional[PolyStats]=None,cache_fixed_kernels=True):
    """Return (unnormalized) N-point DFT of sparse input, any N|p-1.
    No N-length DFT/NTT: only convolutions of size <= O(K).
    """
    if stats is None:stats=PolyStats()
    data={j:(z%p) for j,z in entries.items() if z%p}
    if any(j<0 or j>=n for j in data):raise ValueError('bad support')
    k=len(data)
    if not k:return [0]*n,stats
    num,den=rational_fraction(data,omega,p,primitive_gen,stats)
    block_len=nextpow2(k)
    inverse=inv_series(den,block_len,p,primitive_gen,stats)
    cross_conv = (FixedKernelConvolver(den,k,p,primitive_gen,stats)
                  if cache_fixed_kernels else None)
    output_conv = (FixedKernelConvolver(inverse,block_len,p,primitive_gen,stats)
                   if cache_fixed_kernels else None)
    out=[]
    for s in range(0,n,block_len):
        rem=[0]*block_len
        if s==0:
            for j,v in enumerate(num):rem[j]=v
        else:
            prior=out[s-k:s]
            assert len(prior)==k
            cross=(cross_conv.apply(prior) if cross_conv is not None
                   else conv(den,prior,p,primitive_gen,stats))
            for j in range(k):rem[j]=(-cross[k+j])%p
        block=(output_conv.apply(rem) if output_conv is not None
               else conv(rem,inverse,p,primitive_gen,stats))[:block_len]
        out.extend(block[:min(block_len,n-s)])
        stats.rational_blocks+=1
        stats.coeff_writes+=block_len
    assert len(out)==n
    return out,stats


def bluestein_transform(x,n,omega,p=P0,primitive_gen=G0,
                        stats:Optional[PolyStats]=None):
    """Exact NTT-length O(NlogN) fallback for any N if 2N | (p-1).

    omega must be primitive n-th root derived from primitive_gen.
    Uses one 2n-root chirp and a power-of-two convolution >=2n-1.
    """
    if len(x)!=n:raise ValueError('length mismatch')
    if (p-1)%(2*n):raise ValueError('need 2n-th roots for universal chirp')
    if stats is None:stats=PolyStats()
    zeta=pow_charged(primitive_gen,(p-1)//(2*n),p,stats)
    assert zeta*zeta%p==omega
    size=nextpow2(2*n-1)
    if (p-1)%size:raise ValueError('insufficient 2-adic roots')
    chirp=[1]*n
    invchirp=[1]*n
    zeta2=zeta*zeta%p
    izeta=pow_charged(zeta,-1,p,stats)
    izeta2=izeta*izeta%p
    step=zeta;istep=izeta
    for j in range(1,n):
        chirp[j]=chirp[j-1]*step%p
        invchirp[j]=invchirp[j-1]*istep%p
        step=step*zeta2%p
        istep=istep*izeta2%p
    stats.field_mults+=4*n
    a=[0]*size
    b=[0]*size
    for j,v in enumerate(x):a[j]=v*chirp[j]%p
    for j,z in enumerate(invchirp):
        b[j]=z
        if j:b[size-j]=z
    stats.field_mults+=n
    ntt(a,p,primitive_gen,stats=stats)
    ntt(b,p,primitive_gen,stats=stats)
    for j in range(size):a[j]=a[j]*b[j]%p
    stats.field_mults+=size
    ntt(a,p,primitive_gen,invert=True,stats=stats)
    ans=[a[k]*chirp[k]%p for k in range(n)]
    stats.field_mults+=n
    stats.coeff_writes+=n
    return ans,stats


class AllLengthGreen:
    """Exact all-length Green factorization; returns F*x for any vector x."""
    def __init__(self,n,p=P0,primitive_gen=G0,a=7,b=2,c=1):
        self.n,self.p,self.primitive_gen=n,p,primitive_gen
        self.a,self.b,self.c=a,b,c
        self.omega=general_root(n,p,primitive_gen)
        powers=[1]*n
        for i in range(1,n):powers[i]=powers[i-1]*self.omega%p
        self.powers=powers
        self.L=CyclicSolver([(a+c*powers[i])%p for i in range(n)],b,p)
        self.P=CyclicSolver([(a+b*powers[-i%n])%p for i in range(n)],c,p)

    def sparse_residual(self,x):
        return self.P.apply(x)

    def structured_dense(self,entries):
        v=[0]*self.n
        for j,z in entries.items():v[j]=z%self.p
        return self.P.solve(v)

    def transform(self,x,method='auto'):
        if len(x)!=self.n:raise ValueError('length mismatch')
        r=self.sparse_residual(x)
        entries={j:z for j,z in enumerate(r) if z%self.p}
        k=len(entries)
        stats=PolyStats()
        if method=='auto':
            # The extra K log^2 K factor in fraction building is expensive
            # for dense residuals: switch to ordinary full-transform fallback.
            method='rational' if k<=max(2,self.n//max(4,(self.n.bit_length()-1)**2)) else 'bluestein'
        if method=='rational':forcing,_=forcing_from_sparse(entries,self.n,self.omega,self.p,self.primitive_gen,stats)
        elif method=='bluestein':forcing,_=bluestein_transform(r,self.n,self.omega,self.p,self.primitive_gen,stats)
        else:raise ValueError('choose auto, rational or bluestein')
        y=self.L.solve(forcing)
        return y,{'K':k,'method':method,'stats':stats}


def direct_dft_any(x,omega,p=P0):
    n=len(x)
    result=[]
    for k in range(n):
        wk=pow(omega,k,p)
        power=1
        total=0
        for v in x:
            total=(total+v*power)%p
            power=power*wk%p
        result.append(total)
    return result
