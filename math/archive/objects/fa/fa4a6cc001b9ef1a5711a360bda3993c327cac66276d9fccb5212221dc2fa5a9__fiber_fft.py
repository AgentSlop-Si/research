"""Certified growing-fiber Fourier transforms over prime fields.

Exact structured-input algorithm, not a faster worst-case FFT.  Root supply is
an explicit input.  Pure Python; no third-party dependencies.  Arithmetic and
coarse word-operation counts are instrumented.  Positive-exponent convention:
F_w(x)[k] = sum_j x[j] * w**(j*k).
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable

@dataclass
class Count:
    add: int = 0
    mul: int = 0
    inv: int = 0
    compare: int = 0
    word: int = 0
    def snapshot(self):
        return asdict(self)
    @property
    def arithmetic(self):
        return self.add + self.mul + self.inv

class Field:
    def __init__(self, p: int, count: Count | None = None):
        if p < 3: raise ValueError('Use an odd prime field; primality is supplied.')
        self.p, self.c = p, count or Count()
    def add(self, a, b): self.c.add += 1; return (a+b) % self.p
    def sub(self, a, b): self.c.add += 1; return (a-b) % self.p
    def neg(self, a): self.c.add += 1; return (-a) % self.p
    def mul(self, a, b): self.c.mul += 1; return a*b % self.p
    def inv(self, a):
        self.c.inv += 1
        if a % self.p == 0: raise ZeroDivisionError('Zero field denominator')
        return pow(a, -1, self.p)
    def div(self, a, b): return self.mul(a, self.inv(b))
    def zero(self, a): self.c.compare += 1; return a == 0


def is_pow2(n): return n >= 1 and n & (n-1) == 0

class Roots:
    def __init__(self, n: int, root: int, f: Field):
        if not is_pow2(n): raise ValueError('Length must be a power of two')
        self.n, self.f = n, f
        self.values = [1]*n
        for j in range(1,n):
            self.values[j] = f.mul(self.values[j-1], root)
            f.c.word += 2
        if (n>1 and self.values[n//2] != f.p-1) or f.mul(self.values[-1],root) != 1:
            raise ValueError('The supplied root is not primitive at this length')
    def at(self, exponent: int):
        self.f.c.word += 2
        return self.values[exponent % self.n]


def sparse_fft(entries: Iterable[tuple[int,int]], n: int, step: int, roots: Roots) -> list[int]:
    """Input-pruned radix 2.  Empty subtrees are not expanded.

    step denotes the root roots.values[step] of order n.  Distinct indices in
    [0,n) are required; this is maintained by all internal callers.
    Output work is charged even for all-zero transforms.
    """
    if not is_pow2(n) or roots.n % n: raise ValueError('Invalid pruned transform length')
    f=roots.f
    data=[]
    for i,a in entries:
        f.c.word += 2
        if not 0 <= i < n: raise ValueError('Sparse index out of range')
        a %= f.p
        if not f.zero(a): data.append((i,a))
    def rec(items, m, stride):
        f.c.word += 1
        if not items:
            f.c.word += m
            return [0]*m
        if m==1:
            f.c.word += 1
            return [items[0][1]]
        even=[];odd=[]
        for i,a in items:
            (odd if i&1 else even).append((i//2,a))
            f.c.word += 4
        e=rec(even,m//2,stride*2) if even else None
        o=rec(odd,m//2,stride*2) if odd else None
        out=[0]*m;f.c.word += m
        for k in range(m//2):
            f.c.word += 3
            if o is None:
                out[k]=out[k+m//2]=e[k]
            else:
                t=f.mul(roots.at(stride*k),o[k])
                if e is None:
                    out[k]=t;out[k+m//2]=f.neg(t)
                else:
                    out[k]=f.add(e[k],t);out[k+m//2]=f.sub(e[k],t)
        return out
    return rec(data,n,step)


def dense_fft_reference(x: list[int], root: int, p: int) -> list[int]:
    """Independent dense iterative radix-2 reference, not used by recovery."""
    n=len(x)
    if not is_pow2(n): raise ValueError('Power-of-two length required')
    a=[v % p for v in x];j=0
    for i in range(1,n):
        bit=n>>1
        while j & bit: j ^= bit;bit >>= 1
        j ^= bit
        if i<j: a[i],a[j]=a[j],a[i]
    length=2
    while length<=n:
        wlen=pow(root,n//length,p)
        for i in range(0,n,length):
            w=1
            for j in range(i,i+length//2):
                u=a[j];v=a[j+length//2]*w % p
                a[j]=(u+v)%p;a[j+length//2]=(u-v)%p;w=w*wlen%p
        length*=2
    return a


def direct_dft(x: list[int], root: int, p: int) -> list[int]:
    return [sum(a*pow(root,j*k,p) for j,a in enumerate(x))%p for k in range(len(x))]


def berlekamp_massey(samples: list[int], f: Field) -> list[int]:
    """Return C=[1,c1,..,cr], s[n]+sum_i ci*s[n-i]=0 on supplied prefix.
    A prefix fit is NOT a full signal certificate.
    """
    C=[1];B=[1];L=0;m=1;last=1
    for n in range(len(samples)):
        delta=samples[n]
        for i in range(1,L+1): delta=f.add(delta,f.mul(C[i],samples[n-i]))
        f.c.word += L+1
        if f.zero(delta): m+=1;continue
        old=C.copy();coef=f.div(delta,last)
        if len(C)<len(B)+m: C += [0]*(len(B)+m-len(C))
        for j,b in enumerate(B): C[j+m]=f.sub(C[j+m],f.mul(coef,b))
        if 2*L<=n:
            L=n+1-L;B=old;last=delta;m=1
        else:m+=1
    C += [0]*max(0,L+1-len(C))
    return C[:L+1]


def horner(poly: list[int], z: int, f: Field) -> int:
    value=0
    for a in reversed(poly): value=f.add(f.mul(value,z),a)
    return value


def recover_fiber(y: list[int], budget: int, roots: Roots, step: int):
    """Recover <=budget character modes, then check all raw coordinates.

    Returns [(frequency,amplitude),...] or None. The signal convention is
    y[u]=sum_h amplitude[h]*(root_M)**(-h*u).
    """
    m=len(y);f=roots.f
    if not (1 <= budget and 2*budget <= m):
        raise ValueError('Require 1 <= budget <= M/2')
    C=berlekamp_massey(y[:2*budget],f);r=len(C)-1
    if r>budget: return None
    if r==0:
        for a in y:
            if not f.zero(a): return None
        return []
    # Grid evaluation of recurrence polynomial: O(M log(r+2)), NOT O(M*r).
    vals=sparse_fft(list(enumerate(C)),m,step,roots)
    positions=[h for h,v in enumerate(vals) if f.zero(v)]
    if len(positions)!=r: return None
    # Numerator P=(C(z)*sum y[u]z**u) mod z**r.
    numerator=[0]*r
    for k in range(r):
        for j in range(k+1): numerator[k]=f.add(numerator[k],f.mul(C[j],y[k-j]))
    derivative=[f.mul(j,C[j]) for j in range(1,r+1)]
    modes=[]
    for h in positions:
        z=roots.at(step*h);lam=roots.at(-step*h)
        den=horner(derivative,z,f)
        if f.zero(den): return None
        amp=f.div(f.neg(f.mul(lam,horner(numerator,z,f))),den)
        if f.zero(amp): return None
        modes.append((h,amp))
    # Reconstruction is input-pruned, not one geometric stream per mode.
    recovered=sparse_fft(modes,m,-step,roots)
    for a,b in zip(y,recovered):
        f.c.compare+=1
        if a!=b:return None
    return modes


def sparse_diagonal_shift_solve(diag: list[int], shift_weight: int, x: list[int], f: Field):
    """Solve (diag(diag)+shift_weight*S)y=x by a charged cycle scan.

    S e_j=e_{j+1}.  Individual diagonals must be nonzero. Invalid finite-field
    choices are rejected rather than silently importing a complex norm bound.
    """
    n=len(x)
    if len(diag)!=n: raise ValueError('Shape mismatch')
    a=[];b=[]
    for d,v in zip(diag,x):
        inv=f.inv(d);a.append(f.neg(f.mul(shift_weight,inv)));b.append(f.mul(v,inv))
    # y_j=a_j*y_{j-1}+b_j. Compose j=1..N-1 and close at j=0.
    aa=1;bb=0
    for j in range(1,n):
        aa=f.mul(a[j],aa);bb=f.add(f.mul(a[j],bb),b[j])
    y0=f.div(f.add(f.mul(a[0],bb),b[0]),f.sub(1,f.mul(a[0],aa)))
    y=[y0]
    for j in range(1,n):y.append(f.add(f.mul(a[j],y[-1]),b[j]))
    f.c.word += 8*n
    return y


def precondition(x: list[int], roots: Roots) -> list[int]:
    """P=7I+S+2D^-1; Fourier P = (7I+D+2S) Fourier."""
    f=roots.f;n=len(x);r=[]
    for j,a in enumerate(x):
        r.append(f.add(f.add(f.mul(7,a),x[(j-1)%n]),f.mul(2,f.mul(roots.at(-j),a))))
    return r


def undo_precondition_output(y: list[int], roots: Roots) -> list[int]:
    f=roots.f
    diag=[f.add(7,roots.at(j)) for j in range(len(y))]
    return sparse_diagonal_shift_solve(diag,2,y,f)


def generate_preconditioned_input(r: list[int], roots: Roots) -> list[int]:
    f=roots.f
    diag=[f.add(7,f.mul(2,roots.at(-j))) for j in range(len(r))]
    return sparse_diagonal_shift_solve(diag,1,r,f)


def certified_fiber_fft(x: list[int], p: int, root: int, budget: int,
                        green: bool=False, fallback: bool=False) -> dict:
    """Exact transform on certified fibers; otherwise explicit rejection.

    With fallback=True, every input gets a correct answer, but failed cases
    retain O(N log N) worst-case work. Root-generation and failed work are charged.
    """
    n=len(x)
    if not is_pow2(n) or n<4: raise ValueError('N must be a power of two >=4')
    k=n.bit_length()-1;q=1<<(k//2);m=n//q
    if not 1 <= budget <= m//2: raise ValueError('Require 1 <= budget <= M/2')
    f=Field(p);roots=Roots(n,root,f);x=[v%p for v in x];f.c.word+=n
    r=precondition(x,roots) if green else x
    source_count=f.c.snapshot()
    buckets=[[] for _ in range(m)];ranks=[];K=0
    for t in range(q):
        fiber=[r[t+q*u] for u in range(m)];f.c.word+=m
        modes=recover_fiber(fiber,budget,roots,q)
        if modes is None:
            rejection_count=f.c.snapshot()
            result={'accepted':False,'fallback':fallback,'failure_fiber':t,
                    'N':n,'Q':q,'M':m,'budget':budget,'green':green,
                    'count_at_rejection':rejection_count}
            if fallback:
                result['output']=sparse_fft(list(enumerate(x)),n,1,roots)
            result['count']=f.c.snapshot()
            return result
        ranks.append(len(modes));K+=len(modes)
        for h,a in modes:
            buckets[h].append((t,f.mul(a,roots.at(h*t))))
            f.c.word+=2
    recovery_count=f.c.snapshot()
    out=[0]*n;f.c.word+=n
    for h,entries in enumerate(buckets):
        if not entries:continue
        values=sparse_fft(entries,q,m,roots)
        for v,a in enumerate(values):
            out[h+m*v]=f.mul(m,a);f.c.word+=2
    synthesis_count=f.c.snapshot()
    if green:out=undo_precondition_output(out,roots)
    return {'accepted':True,'fallback':False,'output':out,'N':n,'Q':q,'M':m,
            'budget':budget,'green':green,'K':K,'fiber_ranks':ranks,
            'bucket_ranks':[len(a) for a in buckets],
            'count_source':source_count,'count_recovery':recovery_count,
            'count_synthesis':synthesis_count,'count':f.c.snapshot()}


def make_fiber_signal(n: int, p: int, root: int, mode_lists: list[list[tuple[int,int]]]):
    """Test-data generator; its cost is NOT attributed to raw-input recovery."""
    k=n.bit_length()-1;q=1<<(k//2);m=n//q
    if len(mode_lists)!=q:raise ValueError('One mode list per fiber required')
    eta=pow(root,q,p);r=[0]*n
    for t,modes in enumerate(mode_lists):
        for u in range(m):r[t+q*u]=sum(a*pow(eta,(-h*u)%m,p) for h,a in modes)%p
    return r


def certified_aggregate_fft(x: list[int], p: int, root: int, total_budget: int,
                            green: bool=False, fallback: bool=False) -> dict:
    """Exact global-mode-budget variant; arbitrarily heavy fibers are permitted.

    Let a=max(1,ceil(total_budget/Q)), ell=log2(M), b=min(M/2,a*ell).
    Light fibers use the verified pruned recognizer; failed light recovery
    certifies >b modes and triggers a charged full M-point transform. A final
    over-budget fiber is allowed in the rejection-time bound.

    For total_budget=O(Q*polylog(N)), asymptotic accepted AND rejection work is
    O(N log log N), including discovery. This is still a structured condition.
    """
    n=len(x)
    if not is_pow2(n) or n<4: raise ValueError('N must be a power of two >=4')
    if not isinstance(total_budget,int) or not 0<=total_budget<=n:
        raise ValueError('Require integer 0 <= total_budget <= N')
    k=n.bit_length()-1;q=1<<(k//2);m=n//q;ell=m.bit_length()-1
    avg=max(1,(total_budget+q-1)//q);b=min(m//2,max(1,avg*ell))
    f=Field(p);roots=Roots(n,root,f);x=[v%p for v in x];f.c.word+=n
    r=precondition(x,roots) if green else x
    buckets=[[] for _ in range(m)];K=0;ranks=[];heavy=[]
    inverse_m=None
    for t in range(q):
        y=[r[t+q*u] for u in range(m)];f.c.word+=m
        modes=recover_fiber(y,b,roots,q)
        if modes is None:
            # Soundness/completeness imply the true mode count is >b.
            coeff=sparse_fft(list(enumerate(y)),m,q,roots)
            if inverse_m is None:inverse_m=f.inv(m)
            modes=[(h,f.mul(v,inverse_m)) for h,v in enumerate(coeff) if not f.zero(v)]
            if len(modes)<=b:raise AssertionError('Light recognizer missed a valid fiber')
            heavy.append(t)
        K+=len(modes);ranks.append(len(modes))
        if K>total_budget:
            result={'accepted':False,'fallback':fallback,'failure_fiber':t,
                    'N':n,'Q':q,'M':m,'total_budget':total_budget,'threshold':b,
                    'K_seen':K,'heavy_fibers':heavy,'green':green,
                    'count_at_rejection':f.c.snapshot()}
            if fallback:result['output']=sparse_fft(list(enumerate(x)),n,1,roots)
            result['count']=f.c.snapshot();return result
        for h,a in modes:
            buckets[h].append((t,f.mul(a,roots.at(h*t))));f.c.word+=2
    recovery_count=f.c.snapshot()
    out=[0]*n;f.c.word+=n
    for h,entries in enumerate(buckets):
        if not entries:continue
        values=sparse_fft(entries,q,m,roots)
        for v,a in enumerate(values):out[h+m*v]=f.mul(m,a);f.c.word+=2
    if green:out=undo_precondition_output(out,roots)
    return {'accepted':True,'fallback':False,'output':out,'N':n,'Q':q,'M':m,
            'total_budget':total_budget,'threshold':b,'green':green,
            'K':K,'fiber_ranks':ranks,'bucket_ranks':[len(z) for z in buckets],
            'heavy_fibers':heavy,'count_recovery':recovery_count,'count':f.c.snapshot()}
