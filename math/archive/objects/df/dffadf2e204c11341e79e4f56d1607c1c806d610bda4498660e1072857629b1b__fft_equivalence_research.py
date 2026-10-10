"""FFT symmetry-cache research prototype.

Illustrates how circular shifts, reversals, and binary complements can share
an FFT result. It is NOT a faster general FFT; canonicalization, lookup,
complex arithmetic, output materialization, and numerical precision cost time.

Python >= 3.10, standard library only.
"""
from __future__ import annotations
import cmath
import math
import random
import statistics
from time import perf_counter


def ordinary_fft(a):
    n = len(a)
    if n == 1: return (complex(a[0]),)
    E=ordinary_fft(a[0::2]); O=ordinary_fft(a[1::2]); out=[0j]*n
    for k in range(n//2):
        v=cmath.exp(-2j*math.pi*k/n)*O[k]
        out[k]=E[k]+v
        out[k+n//2]=E[k]-v
    return tuple(out)


def least_rotation(v):
    """Booth algorithm: starting position of minimal cyclic rotation, O(m)."""
    n=len(v)
    if n==1:return 0
    doubled=v+v
    i,j,k=0,1,0
    while i<n and j<n and k<n:
        a=doubled[i+k]; b=doubled[j+k]
        if a==b:
            k+=1
        elif a>b:
            i=i+k+1
            if i<=j:i=j+1
            k=0
        else:
            j=j+k+1
            if j<=i:j=i+1
            k=0
    return min(i,j)


def canonical_binary(v):
    """Return (lexically minimal orbit representative, sign, shift, complement).

    Representative c[j] = (1 - v[(shift+sign*j)%m]) if complement else
                       v[(shift+sign*j)%m].
    sign is +1 or -1; use inverse DFT identity to get FFT(v) from FFT(c).
    Symmetry group size <= 4m (shift, reversal, optional complement).
    """
    n=len(v)
    v=tuple(v)
    assert all(x in (0,1) for x in v)
    best=None
    info=None
    for sign in (1,-1):
        base=tuple(v[(sign*j)%n] for j in range(n))
        for complement in (False,True):
            arr=tuple(1-x for x in base) if complement else base
            start=least_rotation(arr)
            candidate=arr[start:]+arr[:start]
            shift=(sign*start)%n
            order=(bool(complement),sign==-1,shift)
            if best is None or candidate<best or (candidate==best and order<info[3]):
                best=candidate
                info=(sign,shift,complement,order)
    sign,shift,complement,_=info
    return best,sign,shift,complement


def recover_fft(canonical_output, sign, shift, complement):
    """Reconstruct FFT(v) from FFT(c), where c is an orbit transform of v."""
    n=len(canonical_output)
    if sign==1 and shift==0 and not complement:
        return canonical_output
    out=[]
    z=1+0j
    step=cmath.exp(-2j*math.pi*shift/n)
    for k in range(n):
        value=canonical_output[(sign*k)%n]
        if complement:
            value=(n if k==0 else 0)-value
        out.append(z*value)
        z*=step
    return tuple(out)


class SymmetryFFT:
    def __init__(self):
        self.cache={}
        self.hits=0
        self.misses=0
        self.butterflies=0
        self.reconstructed=0
        self.canonical_scanned=0

    def fft(self, v):
        n=len(v)
        if n==1:
            return (complex(v[0]),)
        key,sign,shift,comp=canonical_binary(v)
        self.canonical_scanned+=n
        cache_key=(n,key)
        F=self.cache.get(cache_key)
        if F is None:
            self.misses+=1
            even=self.fft(key[0::2]); odd=self.fft(key[1::2])
            out=[0j]*n
            for k in range(n//2):
                w=cmath.exp(-2j*math.pi*k/n)*odd[k]
                out[k]=even[k]+w
                out[k+n//2]=even[k]-w
                self.butterflies+=1
            F=tuple(out)
            self.cache[cache_key]=F
        else:
            self.hits+=1
        if sign!=1 or shift!=0 or comp:
            self.reconstructed+=n
        return recover_fft(F,sign,shift,comp)


def interleaved_orbit_inputs(n, block_len=128, seed=7):
    """At radix-2 recursion depth, length-block_len children are orbit variants."""
    assert n%block_len==0
    rand=random.Random(seed)
    template=[rand.randrange(2) for _ in range(block_len)]
    groups=n//block_len
    vec=[0]*n
    for offset in range(groups):
        orientation=rand.choice((-1,1))
        shift=rand.randrange(block_len)
        comp=rand.randrange(2)
        for j in range(block_len):
            vec[offset+groups*j]=template[(shift+orientation*j)%block_len]^comp
    return vec


def exact_tests():
    rng=random.Random(20261008)
    for n in (2,4,8,16,32,64,128):
        for t in range(8):
            seq=tuple(rng.randrange(2) for _ in range(n))
            canon,sgn,shift,comp=canonical_binary(seq)
            assert all(canon[j]==(seq[(shift+sgn*j)%n]^int(comp)) for j in range(n))
            naive=ordinary_fft(seq)
            improved=recover_fft(ordinary_fft(canon),sgn,shift,comp)
            err=max(abs(a-b) for a,b in zip(naive,improved))
            assert err<1e-7,(n,t,err)
            cached=SymmetryFFT().fft(seq)
            err=max(abs(a-b) for a,b in zip(naive,cached))
            assert err<1e-7,(n,t,err)
    print('PASS: 56 random binary inputs versus independent radix-2 FFT, length 2..128')
    for n in (8,16,64,128,512):
        src=tuple(rng.randrange(2) for _ in range(n))
        shift=rng.randrange(n); sgn=rng.choice((-1,1)); comp=rng.randrange(2)
        dest=tuple(src[(shift+sgn*j)%n]^comp for j in range(n))
        actual=ordinary_fft(dest)
        z=cmath.exp(-2j*math.pi*shift/n)
        f=ordinary_fft(src)
        prediction=[]
        # dest[j]=src[shift+sgn*j]^comp. FFT(dest)[k]=omega^(-sgn*shift*k)*(m*d0-F(src)[sgn*k])
        phase=1+0j
        step=cmath.exp(2j*math.pi*sgn*shift/n)
        for k in range(n):
            fval=f[(sgn*k)%n]
            if comp:fval=(n if k==0 else 0)-fval
            prediction.append(phase*fval)
            phase*=step
        err=max(abs(a-b) for a,b in zip(actual,prediction))
        # comment above intentionally isn't the core tested identity; test canonical recovery instead
        assert err<1e-7,(n,err)
    print('PASS: 5 shift / reversal / complement transformations against independent FFT')


def experiment():
    print('N,case,standard_butterflies,cache_butterflies,arithmetic_saved_percent,lookup_hits,lookup_misses,canonical_scanned,reconstruction_entries,max_abs_error,normal_seconds,cache_seconds')
    for n in (1024,4096,16384):
        rr=random.Random(n+77)
        cases={
            'random_binary':[rr.randrange(2) for _ in range(n)],
            'period8':([1,0,0,1,1,0,1,0]*(n//8)),
            'orbit128':interleaved_orbit_inputs(n,128,seed=n+777),
        }
        for label,seq in cases.items():
            t=perf_counter(); standard=ordinary_fft(seq); t_std=perf_counter()-t
            solver=SymmetryFFT()
            t=perf_counter(); shared=solver.fft(seq); t_shared=perf_counter()-t
            err=max(abs(a-b) for a,b in zip(standard,shared))
            assert err<1e-6,(n,label,err)
            normal=n*int(math.log2(n))//2
            savings=100*(normal-solver.butterflies)/normal
            print(f'{n},{label},{normal},{solver.butterflies},{savings:.2f},{solver.hits},{solver.misses},{solver.canonical_scanned},{solver.reconstructed},{err:.4g},{t_std:.5f},{t_shared:.5f}')


if __name__=='__main__':
    exact_tests()
    experiment()


def affine_fft_from_base(base_fft, a, b, complement=False):
    """FFT of B[j]=A[(a*j+b)%m] xor complement (for binary A).

    Requires gcd(a,m)=1. Reconstruction is O(m) without recomputing an FFT.
    """
    n=len(base_fft)
    ainv=pow(a,-1,n)
    out=[]
    phase=1+0j
    step=cmath.exp(2j*math.pi*ainv*b/n)
    for k in range(n):
        value=phase*base_fft[(ainv*k)%n]
        if complement:
            value=(n if k==0 else 0)-value
        out.append(value)
        phase*=step
    return tuple(out)


def sparse_edit_fft(base_fft, changes):
    """FFT of modified input using a list of (position, additive_delta).

    O(n * number_of_changes) operations plus O(n) output writes.
    """
    n=len(base_fft)
    out=list(base_fft)
    for pos,delta in changes:
        w=cmath.exp(-2j*math.pi*pos/n)
        z=1+0j
        for k in range(n):
            out[k]+=delta*z
            z*=w
    return tuple(out)


def expanded_tests():
    rng=random.Random(73029)
    errors=[]
    count=0
    for n in (8,16,32,64,128,256):
        A=[rng.randrange(2) for _ in range(n)]
        FA=ordinary_fft(A)
        for _ in range(10):
            a=rng.randrange(n//2)*2+1 # odd, invertible mod power-of-two
            b=rng.randrange(n)
            complement=rng.randrange(2)
            B=[A[(a*j+b)%n]^complement for j in range(n)]
            expected=ordinary_fft(B)
            actual=affine_fft_from_base(FA,a,b,bool(complement))
            errors.append(max(abs(x-y) for x,y in zip(actual,expected)))
            count+=1
        for edits in (1,2,3):
            pos=rng.sample(range(n),edits)
            changes=[(j,(1 if A[j]==0 else -1)) for j in pos]
            B=A[:]
            for j,delta in changes:B[j]+=delta
            expected=ordinary_fft(B)
            actual=sparse_edit_fft(FA,changes)
            errors.append(max(abs(x-y) for x,y in zip(actual,expected)))
            count+=1
    assert max(errors)<1e-7,max(errors)
    print(f'PASS: {count} affine-index-permutation/complement or sparse-edit FFT reconstructions; max error {max(errors):.4g}')


if __name__=='__main__':
    expanded_tests()
