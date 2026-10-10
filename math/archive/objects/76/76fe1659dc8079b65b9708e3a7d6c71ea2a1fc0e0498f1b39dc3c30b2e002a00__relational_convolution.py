"""Phase 6: persistent, relation-aware circular convolution.

A signal is an exact *formal* combination of shifted basis signals and sparse
impulses. Cached core convolutions allow its product with another such signal
to be queried or materialized without new Fourier transforms.

The algebraic identities are exact. The numpy/scipy implementation uses
float64/complex128 and therefore offers numerical rather than bit-exact
circular convolution. DynamicBitProduct below is separately *exact*.

This is a structured/dynamic workload algorithm, NOT a new worst-case
sub-N-log-N algorithm for fresh arbitrary convolution.
"""
from __future__ import annotations

from collections import Counter, OrderedDict
from dataclasses import dataclass
import math
from time import perf_counter_ns
from typing import Sequence

import numpy as np
try:
    from scipy import fft as scipy_fft
except ImportError:
    from numpy import fft as scipy_fft

from cost_aware_fft import Base, RelationFFT, SpectralState


def _finite_scalar(v):
    a = float(v)
    if not math.isfinite(a):
        raise ValueError('nonfinite scalar')
    return a


@dataclass(frozen=True)
class Snapshot:
    """Immutable relation metadata; bases themselves are immutable."""
    n: int
    terms: tuple[tuple[Base, int, float], ...]
    edits: tuple[tuple[int, float], ...]

    @classmethod
    def from_state(cls, state: SpectralState):
        if not isinstance(state, SpectralState):
            raise TypeError('expected Phase-5 SpectralState')
        return cls(state.n,
                   tuple((base, int(shift)%state.n, _finite_scalar(c))
                         for (base, shift), c in state.terms.items() if c),
                   tuple((int(p), _finite_scalar(d)) for p,d in state.edits.items() if d))

    def signal(self):
        y = np.zeros(self.n, dtype=np.float64)
        for base,s,c in self.terms:
            if s:
                _roll_add(y, base.signal, s, c)
            else:
                y += c*base.signal
        for p,d in self.edits:
            y[p] += d
        return y


def _roll_add(out: np.ndarray, x: np.ndarray, shift: int, coeff: float):
    """out += coeff * roll(x, shift) without allocating a rolled N-array."""
    n = out.size
    s = int(shift) % n
    if s == 0:
        out += coeff*x
    else:
        out[s:] += coeff*x[:n-s]
        out[:s] += coeff*x[n-s:]


class RelationalConvolver:
    """Evaluate convolution of two persistent spectral snapshots.

    - core cache: LRU over unordered base pairs, bounded in bytes;
    - terms: arbitrary real scalars and circular shifts;
    - impulses: known sparse changes;
    - outputs: point, selected Fourier bins, dense FFT baseline, or
      time-domain reconstruction from reused basis convolutions.

    The 'reuse' first call must create core spectra/products if uncached.
    That cost is charged in the cold benchmark. `auto` uses a conservative
    cost heuristic to avoid making additional base convolution calls when
    there are many terms or edits.
    """
    def __init__(self, max_core_bytes=128*1024**2):
        self.max_core_bytes = int(max_core_bytes)
        if self.max_core_bytes < 0:
            raise ValueError('max_core_bytes must be >= 0')
        self._cores = OrderedDict()
        self._bytes = 0
        self.stats = Counter()
        self._sparse_thresholds = {}  # trained length -> maximum reused-edit count
        self.training_receipts = []

    @staticmethod
    def _key(b1, b2):
        # Object identity: input bases are immutable; cache holds strong refs.
        if b1 is b2:
            return b1,b2
        return (b1,b2) if id(b1)<id(b2) else (b2,b1)

    def core(self, b1: Base, b2: Base):
        if len(b1.signal) != len(b2.signal):
            raise ValueError('base length mismatch')
        key = self._key(b1,b2)
        if key in self._cores:
            self.stats['core_hits'] += 1
            self._cores.move_to_end(key)
            return self._cores[key]
        self.stats['core_misses'] += 1
        n=len(b1.signal)
        c=np.asarray(scipy_fft.irfft(b1.spectrum*b2.spectrum, n=n), dtype=np.float64)
        c.flags.writeable = False
        if c.nbytes <= self.max_core_bytes:
            self._cores[key]=c
            self._bytes+=c.nbytes
            while self._bytes > self.max_core_bytes:
                _,evicted=self._cores.popitem(last=False)
                self._bytes-=evicted.nbytes
                self.stats['core_evictions']+=1
        return c

    def memory_report(self):
        return {'core_cache_bytes':self._bytes, 'core_cache_budget':self.max_core_bytes,
                'cached_core_pairs':len(self._cores)}

    def calibrate_sparse(self, reference: SpectralState, fixed_kernel: SpectralState,
                         k_values=(1, 2, 4, 8, 16, 32), repeats=4, seed=123):
        """Measure prepared-kernel FFT vs reused output over varying edits.

        Calibration and core construction are fully charged and reported,
        although per-request decisions use the cached warm-cutoff later.
        Intended only for *many* future related requests with this same
        length, representation class and similar memory environment.
        """
        a=Snapshot.from_state(reference)
        b=Snapshot.from_state(fixed_kernel)
        if len(a.terms)!=1 or a.edits or len(b.terms)!=1 or b.edits:
            raise ValueError('calibration requires two unedited single-base states')
        if a.n!=b.n or repeats<2:
            raise ValueError('incompatible bases or too few repeats')
        if a.terms[0][1:]!=(0,1.0) or b.terms[0][1:]!=(0,1.0):
            raise ValueError('calibration requires unshifted unit-coefficient bases')
        rng=np.random.default_rng(seed)
        t_calibration=perf_counter_ns()
        t_init=perf_counter_ns()
        self.core(a.terms[0][0],b.terms[0][0])
        init_ms=(perf_counter_ns()-t_init)/1e6
        scores=[]
        for k in sorted(set(int(k) for k in k_values)):
            if not (1<=k<=a.n):
                continue
            state=reference.fork()
            for p in rng.choice(a.n,size=k,replace=False):
                state.edit(int(p),float(rng.normal()))
            view=self.product(state,fixed_kernel)
            expected=view.full('prepared')
            observed=view.full('reuse')
            np.testing.assert_allclose(observed,expected,rtol=1e-8,atol=1e-7)
            times={}
            for method in ('prepared','reuse'):
                values=[]
                for _ in range(repeats):
                    start=perf_counter_ns()
                    view.full(method)
                    values.append((perf_counter_ns()-start)/1e6)
                times[method]=float(np.median(values))
            scores.append({'k':k,'prepared_ms':times['prepared'],'reuse_ms':times['reuse'],
                           'speedup':times['prepared']/times['reuse']})
        cutoff=0
        for row in scores:
            if row['speedup'] >= 1.05:
                cutoff=row['k']
            else:
                break
        self._sparse_thresholds[a.n]=cutoff
        receipt={'n':a.n,'cutoff':cutoff,
                 'calibration_ms_excluding_basis_registration':(perf_counter_ns()-t_calibration)/1e6,
                 'core_initialization_ms':init_ms,'scores':scores}
        self.training_receipts.append(receipt)
        return receipt

    def product(self, left: SpectralState, right: SpectralState):
        l=Snapshot.from_state(left)
        r=Snapshot.from_state(right)
        if l.n != r.n:
            raise ValueError('circular convolution requires equal signal lengths')
        return ConvolutionView(self,l,r)


class ConvolutionView:
    def __init__(self, engine: RelationalConvolver, left: Snapshot, right: Snapshot):
        self.engine=engine
        self.left=left
        self.right=right
        self.n=left.n
        self.last_method=None
        # These indexes are built once per persistent view, rather than
        # at every time-coefficient query.
        self._left_lookup=dict(left.edits)
        self._right_lookup=dict(right.edits)

    @property
    def relation_size(self):
        la,ra=self.left,self.right
        p,q=len(la.terms),len(ra.terms)
        a,b=len(la.edits),len(ra.edits)
        return p*q+p*b+a*q, a*b

    def at(self, index: int):
        """One time-domain convolution coefficient, no dense output."""
        j=int(index)
        if not 0 <= j < self.n:
            raise IndexError('time-domain convolution index out of bounds')
        a,b=self.left,self.right
        n=self.n
        total=0.0
        for x,s,c in a.terms:
            for y,t,d in b.terms:
                total += c*d*self.engine.core(x,y)[(j-s-t)%n]
        for x,s,c in a.terms:
            for t,d in b.edits:
                total += c*d*x.signal[(j-s-t)%n]
        for t,d in a.edits:
            for x,s,c in b.terms:
                total += c*d*x.signal[(j-s-t)%n]
        # Complete sparse-sparse pair using an indexed hash join:
        # sum over p in editsA where (j-p) mod n occurs in editsB.
        if len(a.edits) <= len(b.edits):
            for p,da in a.edits:
                total += da*self._right_lookup.get((j-p)%n,0.0)
        else:
            for p,db in b.edits:
                total += db*self._left_lookup.get((j-p)%n,0.0)
        return total

    @staticmethod
    def _spectral_bins_for(s:Snapshot, frequencies):
        q=np.asarray(frequencies, dtype=np.int64)
        n=s.n
        result=np.zeros(len(q),dtype=np.complex128)
        for base,shift,c in s.terms:
            result+=c*base.spectrum[q]*np.exp(-2j*np.pi*((q*shift)%n)/n)
        for p,d in s.edits:
            result+=d*np.exp(-2j*np.pi*((q*p)%n)/n)
        return result

    def frequency_bins(self, frequencies:Sequence[int]):
        """Selected circular-convolution frequency bins; no full spectrum."""
        q=np.asarray(list(frequencies),dtype=np.int64)
        if np.any((q<0)|(q>self.n//2)):
            raise IndexError('rfft frequency index out of range')
        return self._spectral_bins_for(self.left,q)*self._spectral_bins_for(self.right,q)

    @staticmethod
    def _fixed_base(s):
        if len(s.edits) or len(s.terms)!=1:
            return None
        base,shift,c=s.terms[0]
        return base if shift==0 and c==1.0 else None

    def full(self,method='auto'):
        if method not in ('auto','reuse','native','prepared'):
            raise ValueError('unknown method')
        n=self.n
        la,ra=self.left,self.right
        reuse_units,pair_impulses=self.relation_size
        if method=='auto':
            # Native libraries win for many edits; use explicitly trained
            # thresholds where available. A prepared fixed-kernel FFT is the
            # fair fallback for one fixed operand (not two fresh FFTs).
            cached = all(self.engine._key(x,y) in self.engine._cores
                         for x,_,_ in la.terms for y,_,_ in ra.terms)
            fixed_right = self._fixed_base(ra)
            fixed_left = self._fixed_base(la)
            k=max(len(la.edits),len(ra.edits))
            if (fixed_right or fixed_left) and len(la.terms)==1 and len(ra.terms)==1:
                cutoff=self.engine._sparse_thresholds.get(n,2 if n>=16384 else 0)
                method='reuse' if k<=cutoff and (cached or n>=8192) else 'prepared'
            else:
                method=('reuse' if ((reuse_units<=3 and pair_impulses<=max(2,n//128))
                                     and (cached or n>=8192)) else 'native')
        self.last_method=method
        if method=='prepared':
            left_base=self._fixed_base(la)
            right_base=self._fixed_base(ra)
            if right_base is not None:
                out=np.asarray(scipy_fft.irfft(scipy_fft.rfft(la.signal())*right_base.spectrum,n=n),dtype=np.float64)
            elif left_base is not None:
                out=np.asarray(scipy_fft.irfft(left_base.spectrum*scipy_fft.rfft(ra.signal()),n=n),dtype=np.float64)
            else:
                raise ValueError('prepared strategy requires one unedited unshifted basis')
            self.engine.stats['prepared_convolutions']+=1
            return out
        if method=='native':
            A=la.signal(); B=ra.signal()
            out=np.asarray(scipy_fft.irfft(scipy_fft.rfft(A)*scipy_fft.rfft(B),n=n),dtype=np.float64)
            self.engine.stats['native_convolutions']+=1
            return out
        out=np.zeros(n,dtype=np.float64)
        for x,s,c in la.terms:
            for y,t,d in ra.terms:
                _roll_add(out,self.engine.core(x,y),s+t,c*d)
        for x,s,c in la.terms:
            for t,d in ra.edits:
                _roll_add(out,x.signal,s+t,c*d)
        for p,d in la.edits:
            for y,t,c in ra.terms:
                _roll_add(out,y.signal,p+t,c*d)
        for p,d in la.edits:
            for q,c in ra.edits:
                out[(p+q)%n]+=d*c
        self.engine.stats['reuse_convolutions']+=1
        return out


class DynamicBitProduct:
    """Exact nonnegative integer product maintained under known bit flips.

    This maintains *an existing product*; it does not make a fresh arbitrary
    integer multiplication linear-time. All operations use Python big ints.
    """
    def __init__(self, a:int, b:int, bit_capacity:int|None=None):
        self.a=int(a)
        self.b=int(b)
        if min(self.a,self.b)<0:
            raise ValueError('only nonnegative integers supported')
        self.bit_capacity=(max(1,self.a.bit_length(),self.b.bit_length())
                           if bit_capacity is None else int(bit_capacity))
        if self.bit_capacity<1 or max(self.a.bit_length(),self.b.bit_length())>self.bit_capacity:
            raise ValueError('invalid capacity')
        self.product=self.a*self.b
        self.events=0

    def fork(self):
        other=object.__new__(DynamicBitProduct)
        other.a=self.a
        other.b=self.b
        other.product=self.product
        other.bit_capacity=self.bit_capacity
        other.events=self.events
        return other

    def flip(self,operand:str,index:int):
        t=int(index)
        if not 0<=t<self.bit_capacity:
            raise IndexError('bit position outside capacity')
        if operand=='a':
            was_set=(self.a>>t)&1
            sign=1-2*was_set
            self.a ^= (1<<t)
            self.product += sign * (self.b<<t)
        elif operand=='b':
            was_set=(self.b>>t)&1
            sign=1-2*was_set
            self.b ^= (1<<t)
            self.product += sign * (self.a<<t)
        else:
            raise ValueError("operand must be 'a' or 'b'")
        self.events+=1
        return self.product

    def verify(self):
        return self.product==self.a*self.b

class ConvolutionSubscription:
    """Maintain Q selected time-domain convolution values under known edits.

    If the opposite operand consists of r basis terms and a sparse dictionary,
    each subscribed edit costs O(Q*(r+1)) time, independent of the number
    of previous edits. The constructor first evaluates Q coefficients and
    may compile base-base core convolutions (FFT initialization charged).

    Consecutive events may change EITHER operand, with current opposite side
    always used in the delta formula. This is stronger than a fixed kernel.
    """
    def __init__(self, view:ConvolutionView, positions:Sequence[int]):
        self.engine=view.engine
        self.n=view.n
        self.indices=np.asarray(list(positions),dtype=np.int64)
        if np.any((self.indices<0)|(self.indices>=self.n)):
            raise IndexError('subscribed time index out of range')
        self.left_terms=view.left.terms
        self.right_terms=view.right.terms
        self.left_edits=dict(view.left.edits)
        self.right_edits=dict(view.right.edits)
        self._values=np.asarray([view.at(int(q)) for q in self.indices],dtype=np.float64)
        self.events=0

    def _evaluate_other_at(self, indices, terms, edits):
        result=np.zeros(len(indices),dtype=np.float64)
        for base,shift,c in terms:
            result += c*base.signal[(indices-shift)%self.n]
        # Indexed lookup instead of scanning every old edit.
        for i,q in enumerate(indices):
            result[i] += edits.get(int(q),0.0)
        return result

    def edit(self,side:str,position:int,delta:float):
        p=int(position); d=_finite_scalar(delta)
        if not 0<=p<self.n:
            raise IndexError('edit position out of range')
        if side=='left':
            target=self.left_edits
            other_terms=self.right_terms
            other_edits=self.right_edits
        elif side=='right':
            target=self.right_edits
            other_terms=self.left_terms
            other_edits=self.left_edits
        else:
            raise ValueError("side must be 'left' or 'right'")
        if d:
            samples=self._evaluate_other_at((self.indices-p)%self.n, other_terms, other_edits)
            self._values += d*samples
            total=target.get(p,0.)+d
            if not math.isfinite(total):
                raise ValueError('edit overflow')
            if total == 0.:
                target.pop(p,None)
            else:
                target[p]=total
        self.events+=1
        return self

    def values(self, copy=True):
        result=self._values.copy() if copy else self._values.view()
        if not copy:
            result.flags.writeable=False
        return result

    def snapshot_view(self):
        left=Snapshot(self.n, self.left_terms, tuple(self.left_edits.items()))
        right=Snapshot(self.n, self.right_terms, tuple(self.right_edits.items()))
        return ConvolutionView(self.engine,left,right)


def subscribe_convolution(view:ConvolutionView, positions:Sequence[int]):
    return ConvolutionSubscription(view,positions)
