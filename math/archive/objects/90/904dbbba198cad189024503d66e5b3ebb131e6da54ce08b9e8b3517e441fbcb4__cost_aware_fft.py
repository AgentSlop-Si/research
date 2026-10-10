"""Relation-aware FFT dispatcher — research implementation, real 1D inputs only.

Supported relations are provided by the producer, not guessed from arbitrary
unrelated data: known sparse edits, known shifts, and known linear combinations.
Output can remain lazy (selected bins) or be materialized by several algorithms.

SciPy (or NumPy) implements the full numerical FFT. This does NOT implement
OpenAI's exact #130 algorithm and is not a new worst-case FFT theorem.
"""
from __future__ import annotations

from collections import Counter, OrderedDict
from dataclasses import dataclass
import hashlib
import math
import time
import weakref
from typing import Iterable, Sequence

import numpy as np
try:
    from scipy import fft as _fft
except ImportError:
    from numpy import fft as _fft

from phase import phases_tiled


def _signal(x):
    a = np.asarray(x)
    if a.ndim != 1 or a.size < 1 or np.iscomplexobj(a):
        raise ValueError('expected nonempty 1-D real input')
    if not np.issubdtype(a.dtype, np.number):
        raise ValueError('expected numeric real input')
    a = np.array(a, dtype=np.float64, order='C', copy=True)
    if not np.isfinite(a).all():
        raise ValueError('NaN/Inf not supported')
    return a


def _validate_spectrum(z, n):
    # Real-input rFFT must have real DC and (if N even) real Nyquist.
    z[0] = complex(z[0].real)
    if n % 2 == 0:
        z[-1] = complex(z[-1].real)
    return z


def _retained_array_bytes(array):
    """Count an ndarray's retained backing allocation, including view padding."""
    owner = array
    while isinstance(owner.base, np.ndarray):
        owner = owner.base
    return owner.nbytes


class Base:
    """Immutable raw input and rFFT shared by multiple state versions."""
    def __init__(self, signal, spectrum):
        self.signal = signal
        self.spectrum = spectrum
        self.signal.flags.writeable = False
        self.spectrum.flags.writeable = False

    @property
    def memory_bytes(self):
        return self.signal.nbytes + self.spectrum.nbytes


class SpectralState:
    """Linear combination of shifted cached bases plus sparse input edits.

    State never implicitly creates a new dense spectrum after a known edit.
    Editing and forking are cheap in the number of distinct terms/edits.
    Note: users must not mutate dictionary internals; public methods validate.
    """
    def __init__(self, engine, n, terms, edits=None):
        self.engine = engine
        self.n = int(n)
        self.terms = dict(terms)        # {(Base, right_shift): real scalar}
        self.edits = dict(edits or {})  # {input_index: real delta}
        self._cached_output = None
        self._cached_bytes = 0
        self._mutations = 0
        engine._states.add(self)

    @property
    def distinct_edits(self):
        return len(self.edits)

    @property
    def term_count(self):
        return len(self.terms)

    def fork(self):
        return SpectralState(self.engine, self.n, self.terms, self.edits)

    def edit(self, position, delta):
        p = int(position)
        d = float(delta)
        if not (0 <= p < self.n) or not math.isfinite(d):
            raise ValueError('invalid edit position/delta')
        value = self.edits.get(p, 0.0) + d
        if not math.isfinite(value):
            raise ValueError('edit overflow')
        if value == 0.0:
            self.edits.pop(p, None)
        else:
            self.edits[p] = value
        self._invalidate()
        self.engine.stats['edits'] += 1
        return self

    def _invalidate(self):
        self._cached_output = None
        self._cached_bytes = 0
        self._mutations += 1

    def shift(self, amount):
        """Return a new right-circular-shifted state without moving N samples."""
        s = int(amount) % self.n
        terms = {(base, (offset + s) % self.n): value
                 for (base, offset), value in self.terms.items()}
        edits = {(p+s) % self.n: value for p, value in self.edits.items()}
        return SpectralState(self.engine, self.n, terms, edits)

    def bin(self, frequency):
        return self.engine.bin(self, frequency)

    def bins(self, frequencies):
        return self.engine.bins(self, frequencies)

    def spectrum(self, method='auto', cache_output=False, copy=True):
        return self.engine.materialize(self, method, cache_output, copy)

    def signal(self):
        return self.engine.signal(self)


@dataclass(frozen=True)
class Profile:
    n: int
    k: int
    r: int
    has_shift: bool
    median_seconds: dict
    best_method: str


class RelationFFT:
    """Cost-aware dispatcher with bounded *internal* caches.

    max_cache_bytes limits strong references held for implicit exact lookup.
    max_phase_bytes limits cached phase-vector bytes. Explicitly held states
    and bases belong to the caller; they are separately reported as live bytes.
    max_temp_bytes is a conservative pruned work-array eligibility budget,
    not a hard allocator/RSS limit. Backend/runtime hidden allocations and
    separately budgeted persistent phase-cache storage are excluded.

    The conservative fallback avoids expensive data-driven relation searches.
    Relation metadata (edit index/shift/basis coefficients) is passed explicitly.
    Optional calibrate(state) benchmarks methods on actual state and selects a
    method for future states of the same size/shape.
    """
    def __init__(self, *, max_cache_bytes=64*1024**2,
                 max_phase_bytes=32*1024**2,
                 max_temp_bytes=192*1024**2,
                 small_native_cutoff=4096):
        self.max_cache_bytes = int(max_cache_bytes)
        self.max_phase_bytes = int(max_phase_bytes)
        self.max_temp_bytes = int(max_temp_bytes)
        self.small_native_cutoff = int(small_native_cutoff)
        if min(self.max_cache_bytes, self.max_phase_bytes, self.max_temp_bytes) < 0:
            raise ValueError('byte budgets must be nonnegative')
        self._exact: OrderedDict[tuple, Base] = OrderedDict()
        self._exact_bytes = 0
        self._phase: OrderedDict[tuple, np.ndarray] = OrderedDict()
        self._phase_bytes = 0
        self._states = weakref.WeakSet()
        self._bases = weakref.WeakSet()
        self._profiles: dict[tuple, Profile] = {}
        self._auto_cache_misses = 0
        self._auto_cache_skips = 0
        self.stats = Counter()
        self.last_method = None

    @staticmethod
    def _key(a):
        # Digest then mandatory full-array verification: hashes alone NEVER prove equality.
        return (int(a.size), hashlib.blake2b(a.tobytes(), digest_size=16).digest())

    def _fetch(self, a, *, populate):
        key = self._key(a)
        base = self._exact.get(key)
        if base is not None and np.array_equal(a, base.signal):
            self._exact.move_to_end(key)
            self.stats['exact_hits'] += 1
            return base
        self.stats['exact_misses'] += 1
        z = np.asarray(_fft.rfft(a), dtype=np.complex128)
        base = Base(a, z)
        self._bases.add(base)
        if populate and base.memory_bytes <= self.max_cache_bytes:
            prior = self._exact.pop(key, None)
            if prior is not None:
                self._exact_bytes -= prior.memory_bytes
            self._exact[key] = base
            self._exact_bytes += base.memory_bytes
            while self._exact_bytes > self.max_cache_bytes:
                _, victim = self._exact.popitem(last=False)
                self._exact_bytes -= victim.memory_bytes
                self.stats['cache_evictions'] += 1
        return base

    def register(self, signal, *, cache_exact=False):
        x = _signal(signal)
        base = self._fetch(x, populate=cache_exact) if cache_exact else Base(x, np.asarray(_fft.rfft(x), dtype=np.complex128))
        self._bases.add(base)
        self.stats['reference_ffts'] += 1
        return SpectralState(self, len(x), {(base, 0): 1.0})

    def fft(self, signal, *, cache='auto', copy=True):
        """Unannotated input: conservative exact cache or native FFT.

        cache=True: always hash, exact-verify hits, store when within budget.
        cache=False: always invoke native FFT.
        cache='auto' (default): stop hashing after three consecutive misses;
            periodically probe (1 of every 8 later requests) so it can resume.
        Explicitly supplied relations never need this slow discovery route.
        """
        if cache not in (True, False, 'auto'):
            raise ValueError("cache must be True, False, or 'auto'")
        x = _signal(signal)
        should_try = cache is True or (cache == 'auto' and self._auto_cache_misses < 3)
        if cache == 'auto' and not should_try:
            self._auto_cache_skips += 1
            should_try = self._auto_cache_skips % 8 == 0
        if not should_try or self.max_cache_bytes == 0:
            self.last_method = 'native'
            self.stats['native_ffts'] += 1
            if cache == 'auto': self.stats['hash_bypasses'] += 1
            return np.asarray(_fft.rfft(x), dtype=np.complex128)
        prev_hits=self.stats['exact_hits']
        base = self._fetch(x, populate=True)
        hit=self.stats['exact_hits']>prev_hits
        if cache == 'auto':
            self._auto_cache_misses = 0 if hit else self._auto_cache_misses + 1
        self.last_method = 'exact_hit' if hit else 'native_cached'
        z = base.spectrum.copy() if copy else base.spectrum.view()
        if not copy: z.flags.writeable = False
        return z

    def combine(self, states: Sequence[SpectralState], coefficients: Sequence[float]):
        """Build x=sum c_i * x_i, without forming any signal or spectrum."""
        if len(states) != len(coefficients) or not states:
            raise ValueError('states and coefficients must have same positive length')
        n = states[0].n
        terms, edits = {}, {}
        for state, raw_c in zip(states, coefficients):
            if state.engine is not self or state.n != n:
                raise ValueError('states must belong to this engine and share length')
            c = float(raw_c)
            if not math.isfinite(c):
                raise ValueError('nonfinite combination coefficient')
            for key, a in state.terms.items():
                terms[key] = terms.get(key, 0.0) + c*a
            for p, delta in state.edits.items():
                edits[p] = edits.get(p, 0.0) + c*delta
        terms = {key: val for key, val in terms.items() if val}
        edits = {key: val for key, val in edits.items() if val}
        return SpectralState(self, n, terms, edits)

    def states_from_bases(self, basis_signals, coefficient_matrix):
        """M different signals described by M x r supplied coefficients.

        Cost of forming spectra after preparation: O(M*r*N).
        """
        matrix = np.asarray(coefficient_matrix, dtype=np.float64)
        if matrix.ndim != 2 or not np.isfinite(matrix).all():
            raise ValueError('coefficient_matrix must be finite 2D')
        bases = [self.register(x) for x in basis_signals]
        if len(bases) != matrix.shape[1]:
            raise ValueError('number of bases != coefficient columns')
        return [self.combine(bases, row) for row in matrix]

    def _phase_vector(self, n, position, count):
        position = int(position) % n
        key = (int(n), position, int(count))
        existing = self._phase.get(key)
        if existing is not None:
            self._phase.move_to_end(key)
            self.stats['phase_hits'] += 1
            return existing
        self.stats['phase_misses'] += 1
        phase = phases_tiled(n, position, count=count)
        phase.flags.writeable = False
        retained_bytes = _retained_array_bytes(phase)
        if retained_bytes <= self.max_phase_bytes:
            self._phase[key] = phase
            self._phase_bytes += retained_bytes
            while self._phase_bytes > self.max_phase_bytes:
                _, old = self._phase.popitem(last=False)
                self._phase_bytes -= _retained_array_bytes(old)
        return phase

    @staticmethod
    def _profile_key(state):
        return (state.n, state.distinct_edits, state.term_count,
                any(shift for (_,shift) in state.terms))

    def recommend(self, state):
        self._check_state(state)
        k, r, n = state.distinct_edits, state.term_count, state.n
        if r == 1 and k == 0:
            ((base,shift), c), = state.terms.items()
            if shift == 0 and c == 1.0:
                return 'reuse'
        if r == 0 and k == 0:
            return 'zero'
        key = self._profile_key(state)
        if key in self._profiles:
            selected = self._profiles[key].best_method
            # Budgets are mutable; a previously admissible calibrated method
            # must not remain an automatic choice after its budget shrinks.
            if selected != 'pruned' or self._pruned_required_bytes(state) <= self.max_temp_bytes:
                return selected
        # Deliberately conservative: SciPy is far faster than Python bookkeeping
        # on modest arrays. Only inexpensive known relationships are preferred.
        if n < self.small_native_cutoff:
            return 'native'
        if not k and r <= 2:
            return 'linear'
        if k == 1 and r <= 2 and n >= 16384:
            return 'direct'
        if k <= 2 and r <= 2 and n >= 65536:
            return 'direct'
        return 'native'

    def _check_state(self, state):
        if not isinstance(state, SpectralState) or state.engine is not self:
            raise TypeError('state must belong to this RelationFFT instance')

    def signal(self, state):
        self._check_state(state)
        out = np.zeros(state.n, dtype=np.float64)
        for (base, shift), c in state.terms.items():
            if shift:
                out += c*np.roll(base.signal, shift)
            else:
                out += c*base.signal
        for position, delta in state.edits.items():
            out[position] += delta
        return out

    def bin(self, state, frequency):
        self._check_state(state)
        q = int(frequency)
        if not 0 <= q <= state.n//2:
            raise IndexError('rfft frequency index out of range')
        val = 0j
        for (base, shift), c in state.terms.items():
            angle = -2*math.pi*((q*shift)%state.n)/state.n
            val += c*base.spectrum[q]*complex(math.cos(angle), math.sin(angle))
        for p, d in state.edits.items():
            angle = -2*math.pi*((q*p)%state.n)/state.n
            val += d*complex(math.cos(angle),math.sin(angle))
        if q == 0 or (state.n % 2 == 0 and q == state.n//2):
            return complex(val.real)
        return val

    def bins(self, state, frequencies: Iterable[int]):
        self._check_state(state)
        q = np.asarray(list(frequencies), dtype=np.int64)
        if (q < 0).any() or (q > state.n//2).any():
            raise IndexError('rfft frequency index out of range')
        out = np.zeros(q.size, dtype=np.complex128)
        for (base, shift), c in state.terms.items():
            if shift:
                phase = np.exp(-2j*np.pi*((q*shift) % state.n)/state.n)
                out += c*base.spectrum[q]*phase
            else:
                out += c*base.spectrum[q]
        for p,d in state.edits.items():
            out += d*np.exp(-2j*np.pi*((q*p) % state.n)/state.n)
        mask = (q==0) | ((state.n%2==0) & (q==state.n//2))
        out[mask] = out[mask].real
        return out

    def _linear_spectrum(self, state):
        n=state.n
        out = np.zeros(n//2+1, dtype=np.complex128)
        for (base, shift), c in state.terms.items():
            if shift:
                phase = self._phase_vector(n, shift, out.size)
                out += c*base.spectrum*phase
            else:
                out += c*base.spectrum
        return out

    def _direct_spectrum(self, state):
        out = self._linear_spectrum(state)
        for p,d in state.edits.items():
            out += d*self._phase_vector(state.n,p,out.size)
        return _validate_spectrum(out, state.n)

    @staticmethod
    def _pruned_required_bytes(state):
        """Conservative visible-array estimate shared by dispatch and execution.

        Charge six length-N complex buffers for rows, FFT output, transpose
        copy, half-spectrum output/addition, phase/multiplication staging and
        workspace reserve; also six length-m float buffers and 64 KiB for
        tile padding/small allocations. This intentionally overestimates the
        normal array peak. Unspecified FFT/runtime hidden allocations are
        not bounded; this is not a hard process-memory guarantee.
        """
        n, k = state.n, state.distinct_edits
        if not k:
            return 0  # no sparse/pruned kernel is needed
        if n & (n-1):
            raise ValueError('pruned mode requires power-of-two length')
        b = 1 << (k-1).bit_length()
        if b > n:
            raise ValueError('more edited coordinates than signal positions')
        return 96*n + 48*(n//b) + 64*1024

    def _pruned_spectrum(self,state):
        """Residue-class decomposition for known sparse changes.

        b=2^ceil(log2 k), m=n/b. For k edits at t=r+b*l,
        B[q,r] += delta * exp(-2*pi*i*q*t/n), q in [0,m).
        Then FFT_b(B[q,:])[j] = D[q+j*m]. Only O(N) input preparation
        (because m*k<=N), plus N/b length-b FFTs and O(N) output.
        Fully explicit complex temporary array takes 16*N bytes.
        This implementation is NUMERICAL, not OpenAI #130.
        """
        n = state.n
        k = state.distinct_edits
        if not k:
            return _validate_spectrum(self._linear_spectrum(state),n)
        if n & (n-1):
            raise ValueError('pruned mode requires power-of-two length')
        b=1 << (k-1).bit_length()
        if self._pruned_required_bytes(state) > self.max_temp_bytes:
            raise MemoryError('pruned work-array estimate exceeds temporary budget')
        m = n//b
        rows = np.zeros((m,b),dtype=np.complex128)
        q = np.arange(m,dtype=np.float64)
        for t,d in state.edits.items():
            # Floating phase in bounded range; avoid huge multipliers where possible.
            angle = -2*np.pi*(np.remainder(q*t,n))/n
            rows[:,t%b] += d*np.exp(1j*angle)
        transformed = _fft.fft(rows,axis=1)
        # DFT[k] is indexed as k=q+m*j.
        delta = transformed.T.ravel()[:n//2+1]
        return _validate_spectrum(self._linear_spectrum(state)+delta,n)

    def materialize(self, state, method='auto', cache_output=False, copy=True):
        self._check_state(state)
        if method not in ('auto','reuse','zero','linear','direct','pruned','native'):
            raise ValueError('unknown materialization strategy')
        # A cached result must not change whether an explicitly requested
        # strategy is valid for this state and the current work-array budget.
        if method == 'reuse':
            if state.distinct_edits != 0 or state.term_count != 1:
                raise ValueError('reuse only valid for one unedited base')
            ((base, shift), c), = state.terms.items()
            if shift or c != 1.0:
                raise ValueError('reuse requires unshifted unit coefficient')
        elif method == 'zero' and (state.term_count or state.distinct_edits):
            raise ValueError('zero strategy only for identically zero state')
        elif method == 'linear' and state.distinct_edits:
            raise ValueError('linear strategy requires no pending edits')
        elif method == 'pruned' and state.distinct_edits:
            if self._pruned_required_bytes(state) > self.max_temp_bytes:
                raise MemoryError('pruned work-array estimate exceeds temporary budget')
        if state._cached_output is not None:
            self.last_method='stored_output'
            out=state._cached_output.copy() if copy else state._cached_output.view()
            if not copy: out.flags.writeable=False
            return out
        if method=='auto':
            method=self.recommend(state)
        self.last_method=method
        self.stats['strategy_'+method]+=1
        if method=='reuse':
            if state.distinct_edits!=0 or state.term_count!=1:
                raise ValueError('reuse only valid for one unedited base')
            ((base,shift),c),=state.terms.items()
            if shift or c!=1.0:
                raise ValueError('reuse requires unshifted unit coefficient')
            out=base.spectrum.copy()  # protect cache from client modification
        elif method=='zero':
            if state.term_count or state.distinct_edits:
                raise ValueError('zero strategy only for identically zero state')
            out=np.zeros(state.n//2+1,dtype=np.complex128)
        elif method=='linear':
            if state.distinct_edits:
                raise ValueError('linear strategy requires no pending edits')
            out=_validate_spectrum(self._linear_spectrum(state),state.n)
        elif method=='direct':
            out=self._direct_spectrum(state)
        elif method=='pruned':
            out=self._pruned_spectrum(state)
        elif method=='native':
            out=np.asarray(_fft.rfft(self.signal(state)),dtype=np.complex128)
        if cache_output:
            # Explicit opt-in. Live output memory is caller-held, not an LRU item.
            state._cached_output=out.copy()
            state._cached_output.flags.writeable=False
            state._cached_bytes=state._cached_output.nbytes
        if not copy:
            out.flags.writeable=False
        return out

    def calibrate(self, state, *, repeats=4, include_pruned=True):
        """Measure true end-to-end reconstruction of this state.

        The first trial includes cold setup for a given method, the median
        represents repeat-query throughput (warm-cache). No input relationship
        discovery is assumed; it is supplied by the producer.
        """
        self._check_state(state)
        if repeats < 2:
            raise ValueError('repeats must be >=2')
        if state._cached_output is not None:
            raise ValueError('cannot calibrate a state with a stored dense result; use a fork()')
        methods=['native']
        if state.distinct_edits:
            methods+=['direct']
            if (include_pruned and state.n & (state.n-1)==0
                    and self._pruned_required_bytes(state) <= self.max_temp_bytes):
                methods+=['pruned']
        else:
            methods+=['linear']
        benchmark={}
        reference=np.asarray(_fft.rfft(self.signal(state)),dtype=np.complex128)
        for method in methods:
            runs=[]
            for run in range(repeats):
                t0=time.perf_counter_ns()
                try:
                    out=self.materialize(state,method=method,cache_output=False)
                except MemoryError:
                    if method != 'pruned':
                        raise
                    # A backend allocation may fail despite the estimate.
                    # Do not select a candidate that did not finish all trials.
                    runs=[]
                    self.stats['calibration_pruned_memory_skips'] += 1
                    break
                elapsed=(time.perf_counter_ns()-t0)*1e-9
                np.testing.assert_allclose(out,reference,rtol=2e-8,atol=2e-7)
                runs.append(elapsed)
            if len(runs) == repeats:
                benchmark[method] = float(np.median(runs))
        best=min(benchmark,key=benchmark.get)
        prof=Profile(state.n,state.distinct_edits,state.term_count,
                     any(shift for (_,shift) in state.terms),benchmark,best)
        self._profiles[self._profile_key(state)]=prof
        return prof

    def memory_report(self):
        # These live-state holdings are not subject to the internal LRU budget;
        # they remain resident because the caller owns a handle to the state.
        live_bases=list(self._bases)
        states=list(self._states)
        return {
            'internal_exact_cache_bytes':self._exact_bytes,
            'internal_phase_cache_bytes':self._phase_bytes,
            'live_base_bytes':sum(base.memory_bytes for base in live_bases),
            'live_state_dense_output_bytes':sum(s._cached_bytes for s in states),
            'live_states':len(states),
            'live_bases':len(live_bases),
            'internal_cache_budget':self.max_cache_bytes,
            'phase_cache_budget':self.max_phase_bytes,
            'max_temp_bytes':self.max_temp_bytes,
        }


def sparse_from_known_changes(base_spectrum, n, changes, method='direct'):
    """Reference rFFT plus known edits, with no stored time-domain reference.

    'auto' conservatively means 'direct' in this spectrum-only interface.
    Native recomputation cannot be used without reconstructing missing input;
    no inverse FFT or other hidden reconstruction is performed.
    """
    e=RelationFFT(max_cache_bytes=0)
    original=np.zeros(n)
    spectrum=np.array(base_spectrum,dtype=np.complex128,copy=True)
    if spectrum.shape != (n//2+1,):
        raise ValueError('wrong spectrum shape')
    b=Base(original,spectrum)
    state=SpectralState(e,n,{(b,0):1.0})
    for p,d in changes:
        state.edit(p,d)
    if method=='native':
        raise ValueError('reference spectrum alone insufficient for native recompute')
    if method=='auto':
        method='direct'
    return e.materialize(state,method=method)

class TrackedBins:
    """Maintain Q selected frequencies under known edits in O(Q) per event.

    This is a live subscription to a FORK of a SpectralState. Edits must be
    performed via this object's .edit()/.edit_many() methods; external edits of
    tracked.state cause a RuntimeError instead of silently returning stale bins.
    It does not construct a new N-element FFT after each edit.
    """
    def __init__(self, state: SpectralState, frequencies: Iterable[int],
                 max_phase_entries=16):
        self.state=state.fork()
        self.n=self.state.n
        q=np.asarray(list(frequencies),dtype=np.int64)
        if (q<0).any() or (q>self.n//2).any():
            raise IndexError('rfft frequency index out of range')
        self.frequencies=q
        self._values=self.state.bins(q)
        self._version=self.state._mutations
        self.max_phase_entries=max(0,int(max_phase_entries))
        self._phases: OrderedDict[int,np.ndarray]=OrderedDict()
        self.events=0

    def _check(self):
        if self.state._mutations!=self._version:
            raise RuntimeError('TrackedBins.state mutated outside the tracked edit API')

    def _phase(self,p):
        phase=self._phases.get(p)
        if phase is not None:
            self._phases.move_to_end(p)
            return phase
        phase=np.exp(-2j*np.pi*((self.frequencies*p)%self.n)/self.n)
        if self.max_phase_entries:
            self._phases[p]=phase
            while len(self._phases)>self.max_phase_entries:
                self._phases.popitem(last=False)
        return phase

    def edit(self,position,delta):
        self._check()
        p=int(position); d=float(delta)
        self.state.edit(p,d)
        self._values += d*self._phase(p)
        self._version=self.state._mutations
        self.events += 1
        return self

    def edit_many(self,changes):
        # Merge repeated positions within an event packet before updating bins.
        self._check()
        merged={}
        for p,d in changes:
            p=int(p); d=float(d)
            if not 0<=p<self.n or not math.isfinite(d):
                raise ValueError('invalid edit')
            merged[p]=merged.get(p,0.0)+d
        for p,d in merged.items():
            if d: self.edit(p,d)
        return self

    def values(self,copy=True):
        self._check()
        out=self._values.copy() if copy else self._values.view()
        if not copy:
            out.flags.writeable=False
        return out

    def current_state(self):
        self._check()
        return self.state.fork()


def subscribe(state: SpectralState, frequencies, **kwargs):
    return TrackedBins(state,frequencies,**kwargs)
