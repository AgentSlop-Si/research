"""Phase 7: persistent, relation-aware circular convolution chains.

Exact identities; numerical execution uses float64 / scipy.fft and is not
an exact integer multiplication or general sub-NlogN Fourier algorithm.

Factor = gain * circular_shift(immutable_seed, shift) + sparse impulses.
An immutable balanced product DAG represents convolution of many factors.
Full dense computation uses optimized real FFT, while sparse forks can reuse
base and leave-one-factor-out time-domain convolutions with O(k*N) work.
Frequency-bin queries reuse partial spectral products in a bounded LRU.
"""
from __future__ import annotations

import math
import cmath
import weakref
from collections import OrderedDict, Counter
from dataclasses import dataclass
from typing import Iterable
import numpy as np
try:
    from scipy import fft as _fft
except ImportError:
    from numpy import fft as _fft


def _real(x):
    y = float(x)
    if not math.isfinite(y):
        raise ValueError('finite real scalars required')
    return y


def _indices(n, pos):
    j = int(pos)
    if not 0 <= j < n:
        raise IndexError(f'index {j} must be between 0 and {n-1}')
    return j


def _phase(n, k, shift):
    # Reduction modulo n avoids enormous arguments to the exponential.
    return cmath.exp((-2j * math.pi / n) * ((int(k) * int(shift)) % n))


def _phase_half(n, shift):
    # Moderate-size, vectorized phase construction. Output is not cached.
    j = np.arange(n//2 + 1, dtype=np.int64)
    return np.exp((-2j * np.pi / n) * ((j * (int(shift) % n)) % n))


@dataclass(eq=False, frozen=True)
class Seed:
    id: int
    signal: np.ndarray
    half_spectrum: np.ndarray

    @property
    def n(self):
        return self.signal.size


@dataclass(frozen=True)
class Factor:
    """Persistent signal represented relative to one immutable seed.

    Every edit is an impulse in the CURRENT signal coordinates, not in the
    coordinates of the original seed. Repeated edits at a position are merged.
    """
    seed: Seed
    shift: int = 0
    gain: float = 1.0
    edits: tuple[tuple[int, float], ...] = ()

    @property
    def n(self):
        return self.seed.n

    def edit(self, position: int, delta: float):
        position = _indices(self.n, position)
        delta = _real(delta)
        if not delta:
            return self
        d = dict(self.edits)
        x = _real(d.get(position, 0.0) + delta)
        if x == 0.0:
            d.pop(position, None)
        else:
            d[position] = x
        return Factor(self.seed, self.shift, self.gain, tuple(sorted(d.items())))

    def shifted(self, amount: int):
        s = int(amount) % self.n
        if s == 0:
            return self
        changes = tuple(sorted(((p+s) % self.n, d) for p,d in self.edits))
        return Factor(self.seed, (self.shift+s)%self.n, self.gain, changes)

    def scaled(self, scalar: float):
        c = _real(scalar)
        if c == 1.0:
            return self
        return Factor(self.seed, self.shift, _real(self.gain*c),
                      tuple((p, _real(d*c)) for p,d in self.edits if d*c != 0))

    def values(self):
        out = self.gain * np.roll(self.seed.signal, self.shift)
        for pos, value in self.edits:
            out[pos] += value
        return out

    def bin(self, k: int):
        k = _indices(self.n, k)
        half = self.seed.half_spectrum
        if k <= self.n//2:
            base = half[k]
        else:
            base = np.conj(half[self.n-k])
        v = self.gain * _phase(self.n, k, self.shift) * base
        for pos, delta in self.edits:
            v += delta * _phase(self.n, k, pos)
        return complex(v)

    def spectrum_half(self):
        v = self.seed.half_spectrum * (self.gain * _phase_half(self.n, self.shift))
        for pos,delta in self.edits:
            v += delta * _phase_half(self.n, pos)
        return v

    def is_base(self):
        return (self.shift == 0 and self.gain == 1.0 and not self.edits)


class _Node:
    __slots__ = ('uid', 'left', 'right', 'factor', 'size', '__weakref__')
    def __init__(self, uid, left=None, right=None, factor=None):
        self.uid = uid
        self.left = left
        self.right = right
        self.factor = factor
        self.size = 1 if factor is not None else left.size + right.size


class ChainEngine:
    """Owns immutable seeds, persistent nodes, and bounded caches.

    Supports many *related versions* of the same circular-convolution chain.
    Baselines and complement convolutions are computed lazily and charged.
    No division by Fourier bins (zeros are safe).
    """
    def __init__(self, max_complement_bytes=128*1024**2, max_bin_cache=200000,
                 max_base_bytes=128*1024**2):
        self.max_complement_bytes = int(max_complement_bytes)
        self.max_bin_cache = int(max_bin_cache)
        self.max_base_bytes = int(max_base_bytes)
        if self.max_complement_bytes < 0 or self.max_bin_cache < 0 or self.max_base_bytes < 0:
            raise ValueError('cache budgets must not be negative')
        self._seeds = []
        self._external_bases = {}  # phase-5 immutable basis identity -> imported seed
        self._uid = 0
        self._intern = weakref.WeakValueDictionary()
        self._bins = OrderedDict()
        self._complements = OrderedDict()
        self._complement_bytes = 0
        self._root_products = OrderedDict()
        self._base_bytes = 0
        self.stats = Counter()

    def seed(self, data):
        raw = np.asarray(data)
        if (raw.ndim != 1 or not raw.size or np.iscomplexobj(raw)
                or not np.issubdtype(raw.dtype, np.number)):
            raise ValueError('seed must be a nonempty finite real vector')
        x = np.asarray(raw, dtype=np.float64)
        if x.ndim != 1 or not x.size or not np.all(np.isfinite(x)):
            raise ValueError('seed must be a nonempty finite real vector')
        x = x.copy()
        x.flags.writeable = False
        spectrum = np.asarray(_fft.rfft(x), dtype=np.complex128)
        spectrum.flags.writeable = False
        seed = Seed(len(self._seeds), x, spectrum)
        self._seeds.append(seed)
        self.stats['seed_ffts'] += 1
        return Factor(seed)

    def from_phase5(self, states):
        """Import Phase-5 SpectralState metadata without detecting relations.

        For an existing single basis term we import the immutable base's
        already-computed rFFT and keep shift/scale/sparse edits symbolically.
        For multi-basis combinations, fall back to materializing that input
        once and registering it as a new seed. This keeps the API exact while
        the general multi-basis symbolic transfer remains future work.
        """
        factors=[]
        for state in states:
            if not hasattr(state,'terms') or not hasattr(state,'edits') or not hasattr(state,'signal'):
                raise TypeError('expected Phase-5 SpectralState instances')
            if len(state.terms)==1:
                (external, shift),gain=next(iter(state.terms.items()))
                key=id(external)
                prior=self._external_bases.get(key)
                if prior is None or prior[0] is not external:
                    a=np.asarray(external.signal)
                    spec=np.asarray(external.spectrum)
                    if a.ndim!=1 or spec.size!=a.size//2+1 or                       a.dtype!=np.float64 or spec.dtype!=np.complex128 or                       a.flags.writeable or spec.flags.writeable:
                        raise ValueError('import requires immutable Phase-5 float64 base and rFFT')
                    seed=Seed(len(self._seeds),a,spec)
                    self._seeds.append(seed)
                    self._external_bases[key]=(external,seed)
                    self.stats['imported_phase5_bases']+=1
                else:
                    seed=prior[1]
                edits=tuple(sorted((int(p), _real(d)) for p,d in state.edits.items() if d))
                factors.append(Factor(seed,int(shift)%seed.n,_real(gain),edits))
            else:
                # Multi-term states are preserved mathematically, although
                # the general symbolic basis representation is not imported.
                factors.append(self.seed(state.signal()))
                self.stats['materialized_phase5_states']+=1
        return self.chain(factors)

    def _intern_node(self, left=None, right=None, factor=None):
        if factor is not None:
            key = ('leaf', factor.seed.id, factor.shift, factor.gain, factor.edits)
        else:
            key = ('prod', left.uid, right.uid)
        obj = self._intern.get(key)
        if obj is not None:
            self.stats['intern_hits'] += 1
            return obj
        self._uid += 1
        obj = _Node(self._uid, left, right, factor)
        self._intern[key] = obj
        self.stats['new_nodes'] += 1
        return obj

    def chain(self, factors: Iterable[Factor]):
        factors = tuple(factors)
        if not factors:
            raise ValueError('at least one factor is required')
        n = factors[0].n
        if any(not isinstance(f, Factor) or f.n != n or
               f.seed not in self._seeds for f in factors):
            raise ValueError('all factors must have equal lengths and belong to this engine')
        def build(start, end):
            if end-start == 1:
                return self._intern_node(factor=factors[start])
            mid=(start+end)//2
            return self._intern_node(build(start,mid),build(mid,end))
        return ChainVersion(self, build(0,len(factors)), n,
                            tuple(f.seed.id for f in factors), frozenset(j for j,f in enumerate(factors) if not f.is_base()))

    def _rewrite(self, node, index, new_factor):
        # Composition can create a deep tree. Preserve its sharing without
        # relying on Python recursion; this is still O(tree height).
        path = []
        while node.factor is None:
            left = index < node.left.size
            path.append((node, left))
            if left:
                node = node.left
            else:
                index -= node.left.size
                node = node.right
        assert index == 0
        revised = self._intern_node(factor=new_factor)
        for parent, left in reversed(path):
            revised = (self._intern_node(revised, parent.right) if left else
                       self._intern_node(parent.left, revised))
        return revised

    def _factor(self, node, index):
        while node.factor is None:
            if index < node.left.size:
                node = node.left
            else:
                index -= node.left.size
                node = node.right
        assert index == 0
        return node.factor

    def _all_factors(self, root):
        stack = [root]
        while stack:
            node = stack.pop()
            if node.factor is not None:
                yield node.factor
            else:
                stack.append(node.right)
                stack.append(node.left)

    def _cache_bin(self, key, producer):
        if key in self._bins:
            self._bins.move_to_end(key)
            self.stats['bin_hits']+=1
            return self._bins[key]
        value=producer()
        self.stats['bin_misses']+=1
        if self.max_bin_cache:
            self._bins[key]=value
            while len(self._bins)>self.max_bin_cache:
                self._bins.popitem(last=False)
                self.stats['bin_evictions']+=1
        return value

    def _seed_bin(self, sid, k):
        seed=self._seeds[sid]
        if k<=seed.n//2:
            return complex(seed.half_spectrum[k])
        return complex(np.conj(seed.half_spectrum[seed.n-k]))

    def _fixed_product_bin(self, seed_ids, k, exclude=None):
        key=('base-bin',seed_ids,k) if exclude is None else ('except-bin',seed_ids,exclude,k)
        def evaluate():
            val=1+0j
            for j,sid in enumerate(seed_ids):
                if j!=exclude:
                    val*=self._seed_bin(sid,k)
            return val
        return self._cache_bin(key,evaluate)

    def _bin_value(self, node, k):
        # Explicit postorder traversal is safe for unbalanced compositions.
        # Local values also remain available if the LRU evicts a child while
        # its sibling is being evaluated.
        values = {}
        stack = [(node, False)]
        while stack:
            current, expanded = stack.pop()
            if current.uid in values:
                continue
            key = ('node', current.uid, k)
            if key in self._bins:
                values[current.uid] = self._cache_bin(key, lambda: None)
            elif current.factor is not None:
                values[current.uid] = self._cache_bin(
                    key, lambda: current.factor.bin(k))
            elif expanded:
                values[current.uid] = self._cache_bin(
                    key, lambda: values[current.left.uid]*values[current.right.uid])
            else:
                stack.append((current, True))
                stack.append((current.right, False))
                stack.append((current.left, False))
        return values[node.uid]

    def _base(self, root, seed_ids=None):
        # This is a seed-only reference for the tree's factor positions.
        seeds=(tuple(seed_ids) if seed_ids is not None else
               tuple(f.seed.id for f in self._all_factors(root)))
        key=seeds
        found=self._root_products.get(key)
        if found is not None:
            self.stats['base_product_hits'] += 1
            self._root_products.move_to_end(key)
            return found
        n=self._all_factors(root)
        first=next(n)
        half=np.ones(first.n//2+1, dtype=np.complex128)
        for f in self._all_factors(root):
            half *= f.seed.half_spectrum
        out=np.asarray(_fft.irfft(half,n=first.n), dtype=np.float64)
        out.flags.writeable = False
        if out.nbytes <= self.max_base_bytes:
            self._root_products[key]=(seeds,out)
            self._base_bytes+=out.nbytes
            while self._base_bytes > self.max_base_bytes:
                _,old=self._root_products.popitem(last=False)
                self._base_bytes-=old[1].nbytes
                self.stats['base_evictions']+=1
        self.stats['base_product_builds']+=1
        return seeds,out

    def _leave_one_out(self, base_seeds, at):
        key=(base_seeds, at)
        if key in self._complements:
            self._complements.move_to_end(key)
            self.stats['complement_hits'] += 1
            return self._complements[key]
        n=self._seeds[base_seeds[0]].n
        half=np.ones(n//2+1,dtype=np.complex128)
        for j, sid in enumerate(base_seeds):
            if j != at:
                half *= self._seeds[sid].half_spectrum
        out=np.asarray(_fft.irfft(half,n=n),dtype=np.float64)
        out.flags.writeable=False
        self.stats['complement_builds'] += 1
        if out.nbytes <= self.max_complement_bytes:
            self._complements[key]=out
            self._complement_bytes += out.nbytes
            while self._complement_bytes > self.max_complement_bytes:
                _,ev=self._complements.popitem(last=False)
                self._complement_bytes -= ev.nbytes
                self.stats['complement_evictions']+=1
        return out

    def memory_report(self):
        seed_bytes=sum(s.signal.nbytes+s.half_spectrum.nbytes for s in self._seeds)
        base_bytes=self._base_bytes
        return dict(seeds=len(self._seeds), seed_bytes=seed_bytes,
                    base_products=len(self._root_products), base_bytes=base_bytes,
                    base_budget=self.max_base_bytes,
                    complements=len(self._complements), complement_bytes=self._complement_bytes,
                    complement_budget=self.max_complement_bytes,
                    bin_cache_entries=len(self._bins), bin_cache_budget=self.max_bin_cache,
                    live_interned_nodes=len(self._intern))


class ChainVersion:
    __slots__=('engine','root','n','_seed_ids','_modified')
    def __init__(self, engine, root, n, seed_ids=None, modified=None):
        self.engine,self.root,self.n=engine,root,n
        self._seed_ids=(tuple(seed_ids) if seed_ids is not None else
                        tuple(f.seed.id for f in engine._all_factors(root)))
        self._modified=(frozenset(modified) if modified is not None else
                        frozenset(j for j,f in enumerate(engine._all_factors(root)) if not f.is_base()))

    def factor(self, at):
        at=_indices(self.root.size,at)
        return self.engine._factor(self.root,at)

    def with_factor(self, at, new_factor):
        at=_indices(self.root.size,at)
        if new_factor.n != self.n or new_factor.seed not in self.engine._seeds:
            raise ValueError('factor incompatible with engine or length')
        if self.factor(at) == new_factor:
            return self
        updated_seeds=(self._seed_ids if new_factor.seed.id==self._seed_ids[at] else
                       self._seed_ids[:at]+(new_factor.seed.id,)+self._seed_ids[at+1:])
        updated_modified=(self._modified-{at}) if new_factor.is_base() else (self._modified|{at})
        return ChainVersion(self.engine,self.engine._rewrite(self.root,at,new_factor),self.n,
                            updated_seeds,updated_modified)

    def edit(self, at, pos, delta):
        return self.with_factor(at,self.factor(at).edit(pos,delta))

    def shift(self, at, amount):
        return self.with_factor(at,self.factor(at).shifted(amount))

    def scale(self, at, amount):
        return self.with_factor(at,self.factor(at).scaled(amount))

    def convolve_with(self, other):
        if not isinstance(other,ChainVersion) or other.engine is not self.engine or other.n != self.n:
            raise ValueError('can only convolve matching versions in one engine')
        return ChainVersion(self.engine,self.engine._intern_node(self.root,other.root),self.n,
                            self._seed_ids+other._seed_ids,
                            self._modified|{j+self.root.size for j in other._modified})

    def frequencies(self, bins):
        ks=np.atleast_1d(np.asarray(bins,dtype=np.int64))
        if np.any((ks<0)|(ks>=self.n)):
            raise IndexError('frequency outside [0,n)')
        if not self._modified:
            out=[self.engine._fixed_product_bin(self._seed_ids,int(k)) for k in ks]
        elif len(self._modified)==1:
            at=next(iter(self._modified))
            f=self.factor(at)
            out=[]
            for k in ks:
                k=int(k)
                base=self.engine._fixed_product_bin(self._seed_ids,k)
                # Gain and shift are applied to the one modified seed term.
                gainshift=f.gain*_phase(self.n,k,f.shift)
                corr=0j
                for p,d in f.edits:
                    corr+=d*_phase(self.n,k,p)
                if f.edits:
                    except_bin=self.engine._fixed_product_bin(self._seed_ids,k,exclude=at)
                    out.append(gainshift*base + corr*except_bin)
                else:
                    out.append(gainshift*base)
        else:
            out=[self.engine._bin_value(self.root,int(k)) for k in ks]
        return np.asarray(out,dtype=np.complex128)

    def spectral_half(self):
        result=np.ones(self.n//2+1,dtype=np.complex128)
        for f in self.engine._all_factors(self.root):
            result *= f.spectrum_half()
        return result

    def _one_changed(self):
        if len(self._modified)!=1:
            return None
        at=next(iter(self._modified))
        return at,self.factor(at)

    def time(self, indices):
        """Selected time-domain coefficients. Single changed factor has a
        fast exact algebraic formula, other cases compute a full result.
        """
        idx=np.atleast_1d(np.asarray(indices,dtype=np.int64))
        if np.any((idx<0)|(idx>=self.n)):
            raise IndexError('time index outside [0,n)')
        changed=self._one_changed()
        if changed is None:
            if not self._modified:
                return self.engine._base(self.root,self._seed_ids)[1][idx].copy()
            return self.dense()[idx].copy()
        at,f=changed
        seeds, base=self.engine._base(self.root,self._seed_ids)
        result=f.gain*base[(idx-f.shift)%self.n]
        if f.edits:
            other=self.engine._leave_one_out(seeds,at)
            for t,delta in f.edits:
                result=result+delta*other[(idx-t)%self.n]
        return np.asarray(result,dtype=np.float64)

    def dense(self, method='auto'):
        """Return full circular convolution. Methods: auto, sparse, native.

        Sparse method supports arbitrary shift/scale plus impulse edits to
        ONE factor. More changed factors use a factored Fourier evaluation.
        """
        if method not in ('auto','sparse','native'):
            raise ValueError('method must be auto, sparse or native')
        changed=self._one_changed()
        if method=='sparse' and changed is None:
            if not self._modified:
                return self.engine._base(self.root,self._seed_ids)[1].copy()
            raise ValueError('sparse path requires exactly one modified factor')
        if changed is not None and (method=='sparse' or (method=='auto' and len(changed[1].edits)<=4)):
            at,f=changed
            seeds, base=self.engine._base(self.root,self._seed_ids)
            result=f.gain*np.roll(base,f.shift)
            if f.edits:
                other=self.engine._leave_one_out(seeds,at)
                for t,delta in f.edits:
                    result+=delta*np.roll(other,t)
            self.engine.stats['sparse_materializations']+=1
            return result
        if method=='auto' and not self._modified:
            return self.engine._base(self.root,self._seed_ids)[1].copy()
        self.engine.stats['native_materializations'] += 1
        return np.asarray(_fft.irfft(self.spectral_half(),n=self.n),dtype=np.float64)

    def count_reused_nodes(self, other):
        """Diagnostic counts by object identity, including shared leaves."""
        def walk(n):
            nodes=set()
            stack=[n]
            while stack:
                x=stack.pop()
                # UIDs are engine-local, whereas this diagnostic promises
                # object identity and may compare versions from two engines.
                identity=id(x)
                if identity in nodes: continue
                nodes.add(identity)
                if x.factor is None:
                    stack.extend((x.left,x.right))
            return nodes
        a,b=walk(self.root),walk(other.root)
        return dict(left_nodes=len(a),right_nodes=len(b),shared_nodes=len(a&b),
                    new_nodes=len(b-a))
