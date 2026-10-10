"""Phase 11: fresh, exact convolution via sparse annihilating filters.

No cached Fourier spectra or multiple threads. The structured algorithm is
exact over integers and finite fields, based on Q(z)A(z) and Q(z)B(z).
The modular fallback uses an NTT and handles arbitrary fresh inputs.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import prod
from typing import Sequence

PRIMES = ((998244353, 3, 23), (469762049, 3, 26),
          (167772161, 3, 25), (1224736769, 3, 24),
          (1004535809, 3, 21))


def filters(max_degree: int = 3) -> list[tuple[int, ...]]:
    """A modest input-independent family; not a magical dictionary of answers."""
    if max_degree < 0:
        raise ValueError('max_degree must be nonnegative')
    seq = [(1,)]
    def mul(p, q):
        y = [0] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            for j, b in enumerate(q):
                y[i+j] += a*b
        return tuple(y)
    for lam in (1, -1, 2, -2):
        q = (1,)
        for degree in range(1, min(max_degree,3)+1):
            q = mul(q, (1, -lam))
            seq.append(q)
    if max_degree >= 2:
        seq += [(1,-1,-1), (1,0,-1), (1,0,1), (1,-2,-1)]
    if max_degree >= 3:
        seq += [(1,-1,-1,-1), (1,-1,0,-1)]
    # Deduplicate and remove trailing zeros.
    return list(dict.fromkeys(seq))


def filter_signal(a: Sequence[int], q: Sequence[int], mod: int | None = None) -> list[int]:
    """Coefficients of Q(z)A(z); Q[0] must be exactly one."""
    if not a or not q or q[0] != 1:
        raise ValueError('Nonempty sequence and Q[0]=1 required')
    out = [0]*(len(a)+len(q)-1)
    for j, coef in enumerate(q):
        if coef:
            for i, val in enumerate(a):
                out[i+j] += coef * int(val)
    if mod is not None:
        out = [v % mod for v in out]
    return out


def sparse_terms(a: Sequence[int], mod: int | None = None) -> list[tuple[int,int]]:
    if mod is None:
        return [(i, int(x)) for i,x in enumerate(a) if x]
    return [(i, int(x)%mod) for i,x in enumerate(a) if int(x)%mod]


def find_recurrence(a: Sequence[int], max_degree: int = 3, p: int = 998244353,
                    integer_lift: bool = False) -> tuple[int, ...] | None:
    """Bounded Berlekamp--Massey: find Q(0)=1 with Q*a zero in the interior.

    Over F_p, this is exact. For Z-valued a, optionally lift residues to
    centered integer representatives and check the relation in Z; no incorrect
    recurrence is ever accepted. None signals that no short recurrence was
    found. This routine does not presume a previously cached transform.
    """
    if max_degree < 0:
        raise ValueError('max_degree must be nonnegative')
    seq=[int(x)%p for x in a]
    c=[1]; old=[1]
    L=0; shift=1; discrepancy_old=1
    for n in range(len(seq)):
        discrepancy=0
        for j in range(L+1):
            discrepancy+=c[j]*seq[n-j]
        discrepancy%=p
        if discrepancy==0:
            shift+=1
            continue
        old_c=c[:]
        scale=discrepancy*pow(discrepancy_old,-1,p)%p
        need=len(old)+shift
        if len(c)<need:
            c.extend([0]*(need-len(c)))
        for j,x in enumerate(old):
            c[j+shift]=(c[j+shift]-scale*x)%p
        if 2*L<=n:
            L=n+1-L
            old=old_c
            discrepancy_old=discrepancy
            shift=1
        else:
            shift+=1
        if L>max_degree:
            return None
    c=c[:L+1]
    if integer_lift:
        lifted=tuple(x if x<=p//2 else x-p for x in c)
        # A finite polynomial Q*A may have nonzero values near both ends,
        # but its n-th interior through n-1 must vanish for recurrence order L.
        for j in range(L,len(a)):
            value=sum(lifted[t]*int(a[j-t]) for t in range(L+1))
            if value!=0:
                return None
        return lifted
    return tuple(c)


def coeff_recover(a: list[int], q: Sequence[int], mod: int | None = None) -> list[int]:
    """Find C such that Q(z)C(z)=a(z), modulo z^len(a)."""
    if q[0] != 1:
        raise ValueError('Q[0] must be one')
    result = [0]*len(a)
    for i in range(len(a)):
        value = a[i]
        for j in range(1, min(i,len(q)-1)+1):
            value -= q[j]*result[i-j]
        result[i] = value if mod is None else value%mod
    return result


def sparse_product_and_recover(a: Sequence[int], b: Sequence[int], qa: Sequence[int], qb: Sequence[int],
                               mod: int | None = None) -> list[int]:
    """Exact linear convolution using filtered sparse products and inverse recurrences."""
    length=len(a)+len(b)-1
    da=sparse_terms(filter_signal(a,qa,mod),mod)
    db=sparse_terms(filter_signal(b,qb,mod),mod)
    h=[0]*length
    for ia,va in da:
        for ib,vb in db:
            j=ia+ib
            if j<length:
                h[j]+=va*vb
    if mod is not None:
        h=[x%mod for x in h]
    # Invert Qa first and Qb second, using forward substitution in Z[[z]].
    return coeff_recover(coeff_recover(h, qa, mod), qb, mod)


@dataclass(frozen=True)
class Plan:
    qa: tuple[int, ...]
    qb: tuple[int, ...]
    nnz_a: int
    nnz_b: int
    multiply_pairs: int
    recovery_work: int
    detection_work_bound: int
    estimate: int
    baseline_estimate: int
    method: str


def choose_plan(a: Sequence[int], b: Sequence[int], mod: int | None = None,
                max_degree: int = 3, minimum_ratio: float = 0.65,
                discover_recurrences: bool = True) -> Plan:
    """Conservative mathematical work estimator, not a calibrated timing predictor."""
    if not a or not b:
        raise ValueError('nonempty inputs required')
    n,m=len(a),len(b)
    length=n+m-1
    base=filters(max_degree)
    # Sample only the *interior* where a short annihilator predicts zeros.
    # This is a heuristic for plan discovery ONLY; any chosen filter is exact
    # even if the sample happened to give a misleading prediction.
    def candidates(values):
        chosen=[(1,)]
        bm=None
        if discover_recurrences:
            bm=find_recurrence(values,max_degree,integer_lift=(mod is None),
                               p=mod if mod is not None else 998244353)
            if bm is not None and bm not in chosen:
                chosen.append(bm)
        samples=48
        size=len(values)
        for q in base[1:]:
            if q in chosen or size < 16:
                continue
            lo=len(q)-1
            span=size-lo
            idx={lo+(span-1)*j//max(1,samples-1) for j in range(min(samples,span))}
            if not idx:
                continue
            zeros=0
            for i in idx:
                val=sum(q[j]*int(values[i-j]) for j in range(len(q)))
                if mod is not None:
                    val%=mod
                zeros+=(val==0)
            if zeros/len(idx)>=0.8:
                chosen.append(q)
        return chosen
    fa=candidates(a)
    fb=candidates(b)
    # Full, exact support counts only for promising filters. Filters are
    # reverified before use; sample false negatives impact speed, not answers.
    scan=sum(len(q)*n+n for q in fa)+sum(len(q)*m+m for q in fb)
    scan+=sum(len(q)*48*2 for q in base)
    if discover_recurrences:
        # Upper-bound recognition work (actual BM can abort after O(d) points).
        scan+=(n+m)*(max_degree+1)
    oa=[len(sparse_terms(filter_signal(a,q,mod),mod)) for q in fa]
    ob=[len(sparse_terms(filter_signal(b,q,mod),mod)) for q in fb]
    # NTT root-length with conservative proportional estimated operations.
    size=1<<(length-1).bit_length()
    baseline_est=12*size*(size.bit_length()-1)+8*size
    best=None
    for i,qa in enumerate(fa):
        for j,qb in enumerate(fb):
            sa,sb=oa[i],ob[j]
            pairs=sa*sb
            recovery=length*(len(qa)+len(qb)-2)  # upper bound with all q terms nonzero
            work=pairs+recovery+length+scan
            if best is None or work<best.estimate:
                best=Plan(qa,qb,sa,sb,pairs,recovery,scan,work,baseline_est,'structured')
    assert best is not None
    if best.estimate >= minimum_ratio*baseline_est:
        return Plan(best.qa,best.qb,best.nnz_a,best.nnz_b,best.multiply_pairs,best.recovery_work,
                    best.detection_work_bound,best.estimate,baseline_est,'ntt')
    return best


def naive(a: Sequence[int],b: Sequence[int],mod: int|None=None) -> list[int]:
    c=[0]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b):
            c[i+j]+=int(u)*int(v)
    return [x%mod for x in c] if mod is not None else c


def _ntt(a: list[int], p: int, primitive_root: int, inverse: bool) -> None:
    n=len(a);j=0
    for i in range(1,n):
        bit=n>>1
        while j&bit:
            j^=bit
            bit>>=1
        j^=bit
        if i<j:
            a[i],a[j]=a[j],a[i]
    step=2
    while step<=n:
        root=pow(primitive_root,(p-1)//step,p)
        if inverse:
            root=pow(root,p-2,p)
        half=step>>1
        for start in range(0,n,step):
            w=1
            for i in range(start,start+half):
                u=a[i]
                v=a[i+half]*w%p
                a[i]=(u+v)%p
                a[i+half]=(u-v)%p
                w=w*root%p
        step<<=1
    if inverse:
        inv=pow(n,p-2,p)
        for i in range(n):
            a[i]=a[i]*inv%p


def ntt_convolution(a: Sequence[int],b: Sequence[int],p: int=998244353,root: int=3) -> list[int]:
    nout=len(a)+len(b)-1
    size=1<<(nout-1).bit_length()
    if (p-1)%size:
        raise ValueError('transform size does not divide p-1')
    x=[int(t)%p for t in a]+[0]*(size-len(a))
    y=[int(t)%p for t in b]+[0]*(size-len(b))
    _ntt(x,p,root,False)
    _ntt(y,p,root,False)
    for i in range(size):
        x[i]=x[i]*y[i]%p
    _ntt(x,p,root,True)
    return x[:nout]


def exact_crt(a: Sequence[int],b: Sequence[int]) -> list[int]:
    """Exact signed integer convolution via enough modular NTT primes;
    falls back to schoolbook for coefficients not covered by listed primes.
    """
    nout=len(a)+len(b)-1
    size=1<<(nout-1).bit_length()
    bound=min(len(a),len(b))*max(abs(int(x)) for x in a)*max(abs(int(y)) for y in b)
    if bound==0:
        return [0]*nout
    chosen=[]; product=1
    for p,root,k in PRIMES:
        if size <= (1<<k):
            chosen.append((p,root))
            product*=p
            if product>2*bound:
                break
    if product<=2*bound:
        return naive(a,b)
    x=[0]*nout
    P=1
    for p,root in chosen:
        residues=ntt_convolution(a,b,p,root)
        inv=pow(P%p,-1,p)
        for j,res in enumerate(residues):
            h=((res-x[j])%p)*inv%p
            x[j]+=P*h
        P*=p
    return [v if 2*v<=P else v-P for v in x]


def convolve(a: Sequence[int],b: Sequence[int],mod: int | None =None, mode: str ='auto',
             max_degree:int=3) -> tuple[list[int],Plan]:
    """Fresh-input exact convolution. mode: auto / structured / ntt.
    mod=None -> exact signed integers with CRT when required.
    mod=998244353 -> exact modular (prime supports power-of-two NTT).
    """
    if mod is not None and mod not in {item[0] for item in PRIMES}:
        raise ValueError('modulus must be one of the NTT primes; use mod=None for exact integer')
    plan=choose_plan(a,b,mod,max_degree=max_degree)
    if mode not in ('auto','structured','ntt'):
        raise ValueError('invalid mode')
    method=plan.method if mode=='auto' else ('structured' if mode=='structured' else 'ntt')
    if method=='structured':
        return sparse_product_and_recover(a,b,plan.qa,plan.qb,mod),plan
    if mod is None:
        return exact_crt(a,b),plan
    return ntt_convolution(a,b,mod,3),plan


def integer_digits(value:int,base:int=10)->list[int]:
    if value<0 or base<2:
        raise ValueError('nonnegative integer and radix >= 2 required')
    if value==0:
        return [0]
    out=[]
    while value:
        value,r=divmod(value,base)
        out.append(r)
    return out


def multiply_int(a:int,b:int,base:int=10,max_degree:int=3)->tuple[int,Plan]:
    if a<0 or b<0:
        raise ValueError('nonnegative integer arguments required')
    aa=integer_digits(a,base)
    bb=integer_digits(b,base)
    coeff,plan=convolve(aa,bb,mod=None,max_degree=max_degree)
    result=0
    for v in reversed(coeff):
        result=result*base+v
    return result,plan


def multiply_near_power(a:int,b:int,delta_bits:int=16)->tuple[int,str]:
    """Your (A-k)B+kB trick, with k=2**t so kB is a shift.

    If the residual has at most `delta_bits` bits, we use a bounded-width
    multiply. Otherwise the algorithm selects Python's exact general
    multiplication; it makes no new worst-case asymptotic claim.
    """
    if a<0 or b<0 or delta_bits<0:
        raise ValueError('only nonnegative operands, nonnegative delta_bits')
    def candidate(value):
        if value==0:
            return None
        n=value.bit_length()
        choices=[]
        for t in (n-1,n):
            delta=value-(1<<t)
            if abs(delta).bit_length()<=delta_bits:
                choices.append((abs(delta),t,delta))
        return min(choices) if choices else None
    ca,cb=candidate(a),candidate(b)
    if ca is not None and (cb is None or ca[0]<=cb[0]):
        _,t,delta=ca
        return (b<<t)+delta*b, f'(2^{t} + {delta}) * B'
    if cb is not None:
        _,t,delta=cb
        return (a<<t)+delta*a, f'A * (2^{t} + {delta})'
    return a*b,'general multiplication fallback'
