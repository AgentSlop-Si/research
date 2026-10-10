"""Phase 8: canonical real-valued circular convolution DAG + exact polynomial update identities.

This is a numerical research prototype: FFTs use scipy.fft/float64.
Algebraic update identities are exact over commutative rings; finite precision
may affect numeric results. It is NOT a faster worst-case arbitrary DFT algorithm.

Representation: operations are addition and circular convolution. DFT maps
addition to addition and convolution to pointwise multiplication.

Given a root F(x) polynomial in one *signal variable* x, polynomial jets
compute C_h (as time-domain sequences) such that, for ANY perturbation u,
  F(x + u) = sum_h C_h * u^{(*h)}.
For u = delta * unit_impulse(t),
  F(x + delta e_t) = sum_h delta**h roll(C_h, h*t).
This works even if x occurs multiple times in a DAG; the expansion's degree
is the algebraic degree of x in F. Max_degree limits preparation resources.
"""
from __future__ import annotations

import itertools
from collections import Counter, OrderedDict
from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np
try:
    from scipy import fft as _fft
except ImportError:
    from numpy import fft as _fft


@dataclass(frozen=True)
class Node:
    uid: int
    op: str
    args: tuple[int, ...] = ()
    weights: tuple[float, ...] = ()  # for sum
    scalar: float = 1.0  # for scalar, impulse, scale, product
    index: int = 0  # for impulse


class DegreeExceeded(ValueError):
    pass


class AlgebraFFT:
    """Canonical sum/convolution DAG for real, length-n circular signals.

    Canonical modulo scalar combination, associativity and commutativity of
    additions and convolutions (not full distributivity). Not an e-graph.
    Node IDs are engine-local and immutable. Original seed signals are copied.
    """
    def __init__(self, n: int, *, max_spectrum_cache_bytes: int = 64 * 1024 * 1024):
        if int(n) != n or n < 2:
            raise ValueError('length must be an integer >= 2')
        self.n = int(n)
        self.nfreq = self.n // 2 + 1
        self.nodes: dict[int, Node] = {}
        self._intern: dict[tuple, int] = {}
        self._seeds: dict[int, np.ndarray] = {}
        self._seed_fft: dict[int, np.ndarray] = {}
        self._names: dict[str, int] = {}
        self._external_seed_map: dict[int, tuple[object,int]] = {}
        self._spectrum_cache: OrderedDict[int, np.ndarray] = OrderedDict()
        self._spectrum_cache_bytes = 0
        self.max_spectrum_cache_bytes = int(max_spectrum_cache_bytes)
        if self.max_spectrum_cache_bytes < 0:
            raise ValueError('negative cache size')
        self.stats = Counter()
        self.zero = self.const(0.0)
        self.one = self.const(1.0)  # one is delta_0 (convolution identity)

    def _get(self, uid: int) -> Node:
        if type(uid) is not int or uid not in self.nodes:
            raise ValueError(f'unknown engine-local node {uid!r}')
        return self.nodes[uid]

    def _new(self, key: tuple, op: str, args: tuple[int, ...] = (),
             weights: tuple[float, ...] = (), scalar: float = 1., index: int = 0) -> int:
        prior = self._intern.get(key)
        if prior is not None:
            return prior
        uid = len(self.nodes)
        self.nodes[uid] = Node(uid, op, args, weights, float(scalar), index)
        self._intern[key] = uid
        return uid

    @staticmethod
    def _scalar(value) -> float:
        x = float(value)
        if not np.isfinite(x):
            raise ValueError('only finite real constants are supported')
        return 0.0 if x == 0 else x

    def const(self, c: float) -> int:
        c = self._scalar(c)
        return self._new(('const', c), 'const', scalar=c)

    def impulse(self, position: int, amplitude: float = 1.) -> int:
        t = int(position)
        if t != position or not 0 <= t < self.n:
            raise IndexError('invalid impulse index')
        amp = self._scalar(amplitude)
        if amp == 0.:
            return self.zero
        if t == 0:
            return self.const(amp)
        return self._new(('impulse',t,amp),'impulse',scalar=amp,index=t)

    def signal(self, values: Sequence[float], name: str | None = None) -> int:
        a = np.asarray(values, dtype=np.float64)
        if a.shape != (self.n,) or not np.all(np.isfinite(a)):
            raise ValueError(f'expect exactly {self.n} finite real values')
        if name is not None and name in self._names:
            raise ValueError('duplicate signal name')
        uid = self._new(('unique-seed',len(self._seeds)), 'seed')
        x = a.copy()
        x.flags.writeable = False
        self._seeds[uid] = x
        spectrum = np.asarray(_fft.rfft(x), dtype=np.complex128)
        spectrum.flags.writeable = False
        self._seed_fft[uid] = spectrum
        self.stats['input_ffts'] += 1
        if name is not None:
            self._names[name] = uid
        return uid

    def signal_with_spectrum(self, values: Sequence[float], half_spectrum,
                             name: str | None = None) -> int:
        """Import an already-computed trusted real FFT without recomputing it.

        The caller must guarantee half_spectrum=rfft(values); this is a
        provenance-checked/trusted-metadata API, not a numerical equality
        certification. Both arrays are defensively copied into immutable data.
        """
        a = np.asarray(values,dtype=np.float64)
        spec = np.asarray(half_spectrum,dtype=np.complex128)
        if a.shape != (self.n,) or spec.shape != (self.nfreq,):
            raise ValueError('import shape mismatch')
        if not np.all(np.isfinite(a)) or not np.all(np.isfinite(spec)):
            raise ValueError('nonfinite imported data')
        if name is not None and name in self._names:
            raise ValueError('duplicate signal name')
        uid=self._new(('unique-seed',len(self._seeds)),'seed')
        a=a.copy(); spec=spec.copy()
        a.flags.writeable=False;spec.flags.writeable=False
        self._seeds[uid]=a;self._seed_fft[uid]=spec
        self.stats['imported_spectra']+=1
        if name is not None:
            self._names[name]=uid
        return uid

    def import_phase7(self, version) -> int:
        """Import a Phase-7 ChainVersion into this canonical sum-product DAG.

        The source engine's immutable seed spectra are reused by copying them,
        avoiding another FFT. This API assumes trusted Phase-7 objects and
        imports their sparse edits/shifts symbolically, not as dense arrays.
        """
        if getattr(version,'n',None) != self.n or not hasattr(version,'root'):
            raise ValueError('expected a length-matched Phase-7 ChainVersion')
        seen={}
        def build(nd):
            ident=id(nd)
            if ident in seen:
                return seen[ident]
            f=nd.factor
            if f is not None:
                ref=id(f.seed)
                previous=self._external_seed_map.get(ref)
                if previous is None or previous[0] is not f.seed:
                    seed_uid=self.signal_with_spectrum(f.seed.signal,f.seed.half_spectrum)
                    self._external_seed_map[ref]=(f.seed,seed_uid)
                else:
                    seed_uid=previous[1]
                base=self.mul(seed_uid,self.impulse(int(f.shift),1))
                base=self.scale(base,float(f.gain))
                val=self.add(base,*(self.impulse(p,delta) for p,delta in f.edits))
            else:
                val=self.mul(build(nd.left),build(nd.right))
            seen[ident]=val
            return val
        return build(version.root)

    def scale(self, x: int, value: float) -> int:
        v = self._scalar(value)
        node = self._get(x)
        if v == 0 or (node.op == 'const' and node.scalar == 0):
            return self.zero
        if v == 1:
            return x
        if node.op == 'const':
            return self.const(v * node.scalar)
        if node.op == 'impulse':
            return self.impulse(node.index, v * node.scalar)
        if node.op == 'scale':
            return self.scale(node.args[0], v * node.scalar)
        return self._new(('scale', x, v), 'scale', args=(x,), scalar=v)

    def add(self, *items: int) -> int:
        if not items:
            return self.zero
        coefficients: dict[int, float] = {}
        constants = 0.0
        def ingest(u: int, weight: float) -> None:
            nonlocal constants
            nd = self._get(u)
            if nd.op == 'sum':
                for child, a in zip(nd.args, nd.weights):
                    ingest(child, weight * a)
            elif nd.op == 'scale':
                ingest(nd.args[0], weight * nd.scalar)
            elif nd.op == 'const':
                constants += weight * nd.scalar
            else:
                coefficients[u] = self._scalar(coefficients.get(u, 0.) + weight)
        for x in items:
            ingest(x, 1.)
        if constants != 0.:
            u = self.const(constants)
            coefficients[u] = self._scalar(coefficients.get(u, 0.) + 1.)
        pairs = [(u,c) for u,c in coefficients.items() if c != 0.]
        pairs.sort(key=lambda uc:uc[0])
        if not pairs:
            return self.zero
        if len(pairs)==1:
            return self.scale(pairs[0][0], pairs[0][1])
        args = tuple(u for u,_ in pairs)
        weights = tuple(c for _,c in pairs)
        return self._new(('sum',args,weights),'sum',args,weights)

    def mul(self, *items: int) -> int:
        if not items:
            return self.one
        factors = []
        constant = 1.
        def ingest(u: int) -> None:
            nonlocal constant
            nd = self._get(u)
            if nd.op == 'const':
                constant *= nd.scalar
            elif nd.op == 'scale':
                constant *= nd.scalar
                ingest(nd.args[0])
            elif nd.op == 'product':
                constant *= nd.scalar
                for child in nd.args:
                    ingest(child)
            else:
                factors.append(u)
        for x in items:
            ingest(x)
        constant = self._scalar(constant)
        if not constant:
            return self.zero
        if not factors:
            return self.const(constant)
        factors.sort()
        if len(factors)==1:
            return self.scale(factors[0],constant)
        args = tuple(factors)
        return self._new(('product',args,constant),'product',args,scalar=constant)

    def _topological(self, root: int) -> list[int]:
        self._get(root)
        visited = set()
        order = []
        def visit(u: int):
            if u in visited:
                return
            visited.add(u)
            for c in self.nodes[u].args:
                visit(c)
            order.append(u)
        visit(root)
        return order

    def reachable_count(self, root: int) -> int:
        return len(self._topological(root))

    def spectral_operation_estimate(self, root:int) -> dict[str,int]:
        """Approximate per-frequency pointwise ops excluding seed FFTs/phasors.

        Diagnostic, not a machine runtime or complexity lower bound.
        Each reachable DAG node is counted once.
        """
        additions=multiplications=0
        for uid in self._topological(root):
            nd=self.nodes[uid]
            if nd.op=='sum':
                additions+=max(0,len(nd.args)-1)
                multiplications+=sum(w!=1. for w in nd.weights)
            elif nd.op=='product':
                multiplications+=max(0,len(nd.args)-1)+int(nd.scalar!=1.)
            elif nd.op=='scale':
                multiplications+=1
        return {'additions':additions,'multiplications':multiplications,
                'reachable_nodes':self.reachable_count(root)}

    def factor_common(self, root:int) -> int:
        """One-pass local factoring of common convolution factors across sums.

        E.g. A*B + A*C becomes A*(B+C). Canonicalizes associativity and
        commutativity but intentionally does not attempt general polynomial
        factorization/equality saturation, which could cause exponential work.
        """
        rewritten={}
        for uid in self._topological(root):
            nd=self.nodes[uid]
            args=tuple(rewritten.get(ch,ch) for ch in nd.args)
            if nd.op=='scale':
                rewritten[uid]=self.scale(args[0],nd.scalar)
                continue
            if nd.op=='product':
                rewritten[uid]=self.scale(self.mul(*args),nd.scalar)
                continue
            if nd.op!='sum':
                rewritten[uid]=uid
                continue
            # Factor from all additive terms only; leave other shapes alone.
            terms=[]
            for ch,w in zip(args,nd.weights):
                cn=self.nodes[ch]
                scalar=w
                if cn.op=='scale':
                    scalar*=cn.scalar
                    cn=self.nodes[cn.args[0]]
                if cn.op=='product':
                    scalar*=cn.scalar
                    fac=list(cn.args)
                elif cn.op=='const':
                    scalar*=cn.scalar
                    fac=[]
                else:
                    fac=[cn.uid]
                terms.append((fac,scalar))
            if len(terms)<2 or any(not fac for fac,_ in terms):
                rewritten[uid]=self.add(*(self.scale(ch,w) for ch,w in zip(args,nd.weights)))
                continue
            common=set(terms[0][0])
            for fac,_ in terms[1:]:
                common.intersection_update(fac)
            if not common:
                rewritten[uid]=self.add(*(self.scale(ch,w) for ch,w in zip(args,nd.weights)))
                continue
            chosen=min(common)  # deterministic and idempotent in chosen grammar
            remainder=[]
            for fac,scalar in terms:
                fac.remove(chosen)
                remainder.append(self.scale(self.mul(*fac),scalar))
            rewritten[uid]=self.mul(chosen,self.add(*remainder))
        return rewritten[root]

    def evaluate_spectrum(self, root: int) -> np.ndarray:
        """Return full rFFT spectrum, with bounded LRU caching of node spectra."""
        memo = {}
        for uid in self._topological(root):
            if uid in self._spectrum_cache:
                memo[uid] = self._spectrum_cache[uid]
                self._spectrum_cache.move_to_end(uid)
                self.stats['spectrum_cache_hit'] += 1
                continue
            node = self.nodes[uid]
            if node.op == 'seed':
                out = self._seed_fft[uid]
            elif node.op == 'const':
                out = np.full(self.nfreq,node.scalar,dtype=np.complex128)
            elif node.op == 'impulse':
                k = np.arange(self.nfreq,dtype=np.float64)
                out = node.scalar*np.exp(-2j*np.pi*k*node.index/self.n)
            elif node.op == 'scale':
                out = node.scalar*memo[node.args[0]]
            elif node.op == 'sum':
                out = np.zeros(self.nfreq,dtype=np.complex128)
                for child,w in zip(node.args,node.weights):
                    out += w*memo[child]
            elif node.op == 'product':
                out = np.full(self.nfreq,node.scalar,dtype=np.complex128)
                for child in node.args:
                    out *= memo[child]
            else:
                raise AssertionError(node.op)
            memo[uid] = out
            self.stats['evaluated_spectra'] += 1
            if node.op not in ('seed',) and self.max_spectrum_cache_bytes >= out.nbytes:
                out = out.copy()  # no mutation of arrays cached by descendants
                out.flags.writeable = False
                self._spectrum_cache[uid] = out
                memo[uid] = out
                self._spectrum_cache_bytes += out.nbytes
                while self._spectrum_cache_bytes > self.max_spectrum_cache_bytes:
                    _old, val = self._spectrum_cache.popitem(last=False)
                    self._spectrum_cache_bytes -= val.nbytes
        return memo[root].copy()

    def evaluate_time(self, root:int) -> np.ndarray:
        return np.asarray(_fft.irfft(self.evaluate_spectrum(root),n=self.n),dtype=np.float64)

    def frequency(self, root: int, index: int) -> complex:
        """Query one complex frequency in O(number of distinct reachable DAG nodes)."""
        k = int(index)
        if k != index or not 0 <= k < self.n:
            raise IndexError('invalid frequency')
        half_index = k if k <= self.n//2 else self.n-k
        memo = {}
        for uid in self._topological(root):
            nd = self.nodes[uid]
            if nd.op == 'seed':
                v = self._seed_fft[uid][half_index]
                if k > self.n//2:
                    v = np.conj(v)
            elif nd.op == 'const':
                v = complex(nd.scalar)
            elif nd.op == 'impulse':
                v = nd.scalar*np.exp((-2j*np.pi/self.n)*((k*nd.index)%self.n))
            elif nd.op == 'scale':
                v = nd.scalar*memo[nd.args[0]]
            elif nd.op == 'sum':
                v = sum(w*memo[ch] for ch,w in zip(nd.args,nd.weights))
            else:
                v = complex(nd.scalar)
                for ch in nd.args:
                    v *= memo[ch]
            memo[uid] = v
        return complex(memo[root])

    def replace(self, root:int, target:int, replacement:int) -> int:
        """Persistent replacement: shared unchanged branches retain their IDs."""
        self._get(target)
        self._get(replacement)
        replacements = {target:replacement}
        for uid in self._topological(root):
            if uid in replacements:
                continue
            nd = self.nodes[uid]
            args = tuple(replacements.get(ch,ch) for ch in nd.args)
            if args == nd.args:
                replacements[uid] = uid
            elif nd.op == 'scale':
                replacements[uid] = self.scale(args[0],nd.scalar)
            elif nd.op == 'sum':
                replacements[uid] = self.add(*(self.scale(ch,w) for ch,w in zip(args,nd.weights)))
            elif nd.op == 'product':
                replacements[uid] = self.scale(self.mul(*args),nd.scalar)
            else:
                replacements[uid] = uid
        return replacements[root]

    def edit_version(self, root: int, leaf: int, changes:Mapping[int,float]) -> int:
        self._get(leaf)
        if self.nodes[leaf].op!='seed':
            raise ValueError('only registered input leaves can be edited')
        impulses=[self.impulse(pos,delta) for pos,delta in changes.items() if float(delta)!=0]
        return self.replace(root,leaf,self.add(leaf,*impulses)) if impulses else root

    def degree_in(self, root:int, leaf:int) -> int:
        if self._get(leaf).op!='seed':
            raise ValueError('target must be an input leaf')
        deg={}
        for uid in self._topological(root):
            nd=self.nodes[uid]
            if uid == leaf:
                deg[uid]=1
            elif nd.op in ('seed','const','impulse'):
                deg[uid]=0
            elif nd.op == 'scale':
                deg[uid]=deg[nd.args[0]]
            elif nd.op == 'sum':
                deg[uid]=max(deg[u] for u in nd.args)
            else:
                deg[uid]=sum(deg[u] for u in nd.args)
        return deg[root]

    def symbolic_jets(self, root:int, leaf:int, *, max_degree:int=4) -> tuple[int,...]:
        """Symbolic coefficients C_h of F(leaf + U) in the convolution ring.

        This is exact *symbolic* sharing, not numerical thresholding. It does
        not expand sums of products into monomials globally, only polynomial
        coefficients in the one variable U, capped at max_degree.
        """
        d=self.degree_in(root,leaf)
        if d>max_degree:
            raise DegreeExceeded(f'algebraic degree {d} exceeds max_degree={max_degree}')
        memo={}
        for uid in self._topological(root):
            nd=self.nodes[uid]
            if uid==leaf:
                memo[uid]=[uid,self.one]
            elif nd.op in ('seed','const','impulse'):
                memo[uid]=[uid]
            elif nd.op=='scale':
                memo[uid]=[self.scale(u,nd.scalar) for u in memo[nd.args[0]]]
            elif nd.op=='sum':
                depth=max(len(memo[u]) for u in nd.args)
                result=[self.zero]*depth
                for ch,w in zip(nd.args,nd.weights):
                    for j,v in enumerate(memo[ch]):
                        result[j]=self.add(result[j],self.scale(v,w))
                memo[uid]=result
            elif nd.op=='product':
                vals=[self.const(nd.scalar)]
                for child in nd.args:
                    rhs=memo[child]
                    result=[self.zero]*(len(vals)+len(rhs)-1)
                    for i,a in enumerate(vals):
                        for j,b in enumerate(rhs):
                            result[i+j]=self.add(result[i+j],self.mul(a,b))
                    vals=result
                memo[uid]=vals
            else:
                raise AssertionError(nd.op)
        return tuple(memo[root])

    def _known_impulses(self, uid:int, *, limit:int=12) -> dict[int,float] | None:
        """Recognize exactly represented sparse impulses, without using tolerance.

        Returns None if the expression contains a general signal or its
        symbolic impulse support would exceed the specified limit.
        """
        memo={}
        for u in self._topological(uid):
            nd=self.nodes[u]
            if nd.op=='seed':
                out=None
            elif nd.op=='const':
                out={0:nd.scalar} if nd.scalar else {}
            elif nd.op=='impulse':
                out={nd.index:nd.scalar}
            elif nd.op=='scale':
                c=memo[nd.args[0]]
                out=None if c is None else {i:nd.scalar*v for i,v in c.items() if nd.scalar*v}
            elif nd.op=='sum':
                out={}
                for ch,w in zip(nd.args,nd.weights):
                    c=memo[ch]
                    if c is None:
                        out=None
                        break
                    for t,v in c.items():
                        out[t]=out.get(t,0.)+w*v
                if out is not None:
                    out={t:v for t,v in out.items() if v}
            else:
                out={0:nd.scalar}
                for ch in nd.args:
                    c=memo[ch]
                    if c is None or len(c)*len(out)>4*limit:
                        out=None
                        break
                    nxt={}
                    for t,v in out.items():
                        for t2,v2 in c.items():
                            index=(t+t2)%self.n
                            nxt[index]=nxt.get(index,0.)+v*v2
                    out={t:v for t,v in nxt.items() if v}
            if out is not None and len(out)>limit:
                out=None
            memo[u]=out
        return memo[uid]

    def prepare(self, root:int, leaf:int, *, max_degree:int=4) -> 'PreparedEdit':
        """Build Taylor coefficients in frequency domain, inverse them once.

        Preparation for fixed small degree d takes O(d^2 E N + (d+1)NlogN)
        arithmetic for E DAG nodes, plus previously charged seed FFTs. Sparse
        single-sample versions then take O(dN) per full output / O(dQ)
        for Q time coefficients. Total precomputation and output are counted.
        """
        d=self.degree_in(root,leaf)
        if d>max_degree:
            raise DegreeExceeded(f'algebraic degree {d} exceeds max_degree={max_degree}')
        memo={}
        z = np.zeros(self.nfreq,dtype=np.complex128)
        o = np.ones(self.nfreq,dtype=np.complex128)
        # Real rFFTs are Hermitian; kernels obtained below are real sequences.
        for uid in self._topological(root):
            nd = self.nodes[uid]
            if nd.op == 'seed':
                data = self._seed_fft[uid]
                if uid == leaf:
                    memo[uid] = [data, o]
                else:
                    memo[uid] = [data]
            elif nd.op == 'const':
                memo[uid]=[np.full(self.nfreq,nd.scalar,dtype=np.complex128)]
            elif nd.op == 'impulse':
                k=np.arange(self.nfreq,dtype=np.float64)
                memo[uid]=[nd.scalar * np.exp(-2j*np.pi*k*nd.index/self.n)]
            elif nd.op == 'scale':
                memo[uid]=[nd.scalar*t for t in memo[nd.args[0]]]
            elif nd.op == 'sum':
                dim=max(map(lambda ch:len(memo[ch]),nd.args))
                arr=[np.zeros(self.nfreq,dtype=np.complex128) for _ in range(dim)]
                for ch,weight in zip(nd.args,nd.weights):
                    for i,v in enumerate(memo[ch]):
                        arr[i]+=weight*v
                memo[uid]=arr
            elif nd.op == 'product':
                a=[np.full(self.nfreq,nd.scalar,dtype=np.complex128)]
                for ch in nd.args:
                    b=memo[ch]
                    c=[np.zeros(self.nfreq,dtype=np.complex128) for _ in range(min(d,len(a)+len(b)-2)+1)]
                    for i,v in enumerate(a):
                        for j,w in enumerate(b):
                            if i+j<len(c):
                                c[i+j] += v*w
                    a=c
                memo[uid]=a
            else:
                raise AssertionError(nd.op)
        freq_coeffs=memo[root]
        symbolic_coeffs=self.symbolic_jets(root,leaf,max_degree=max_degree)
        sparse_coeffs=tuple(self._known_impulses(x) for x in symbolic_coeffs)
        # Sparse coefficients are mathematically known impulse combinations;
        # no inverse FFT or full time-domain kernel is required for them.
        coefficients=[(np.asarray(_fft.irfft(c,n=self.n),dtype=np.float64)
                       if h==0 or sparse_coeffs[h] is None else None)
                      for h,c in enumerate(freq_coeffs)]
        for c in coefficients:
            if c is not None:
                c.flags.writeable=False
        self.stats['prepared_jets']+=1
        self.stats['prepared_jet_coefficients']+=len(coefficients)
        return PreparedEdit(self,root,leaf,tuple(coefficients),tuple(freq_coeffs),sparse_coeffs)

    def plan_updates(self, root:int, leaf:int, *, expected_versions:int,
                     max_degree:int=4, minimum_amortization:int=8,
                     max_prepared_bytes:int=128*1024**2) -> 'UpdatePlan':
        """Conservative, deterministic dispatcher with explicit memory limits.

        This is a simple analytic policy, not claimed to be optimal and not a
        substitute for machine-specific calibration. Both paths are correct.
        """
        nversions=int(expected_versions)
        if nversions!=expected_versions or nversions<1:
            raise ValueError('expected_versions must be positive integer')
        d=self.degree_in(root,leaf)
        # Conservative allocation ESTIMATE, not an allocator-level hard cap.
        # Accounts for topological DAG intermediates and temporary complex
        # accumulators, plus prepared time-domain and frequency kernels.
        E=len(self._topological(root))
        memory_estimate=(4*E*(d+1)*self.nfreq*16
                         +(d+1)*self.n*8
                         +(d+1)*self.nfreq*16)
        if d>max_degree:
            return UpdatePlan(self,root,leaf,None,'fallback: degree above threshold')
        if memory_estimate>max_prepared_bytes:
            return UpdatePlan(self,root,leaf,None,'fallback: jet memory budget')
        if nversions<minimum_amortization:
            return UpdatePlan(self,root,leaf,None,'fallback: not enough expected reuse')
        return UpdatePlan(self,root,leaf,self.prepare(root,leaf,max_degree=max_degree),
                          'prepared: expected repeated single-variable updates')


@dataclass(frozen=True)
class PreparedEdit:
    """Exact algebraic single-variable expansion; numerical arrays are float64."""
    engine: AlgebraFFT
    root: int
    leaf: int
    kernels: tuple[np.ndarray | None, ...]
    frequency_coefficients: tuple[np.ndarray, ...]
    sparse_coefficients: tuple[dict[int,float] | None, ...] = ()

    @property
    def degree(self) -> int:
        return len(self.kernels)-1

    @property
    def n(self) -> int:
        return self.engine.n

    def single(self, position:int, delta:float, indices:Sequence[int] | None=None):
        t=int(position)
        if t != position or not 0<=t<self.n:
            raise IndexError('invalid edit position')
        delta=float(delta)
        if not np.isfinite(delta):
            raise ValueError('nonfinite edit')
        if indices is None:
            result=self.kernels[0].copy()
            for h in range(1,self.degree+1):
                sparse=self.sparse_coefficients[h] if self.sparse_coefficients else None
                if sparse is not None:
                    for pos,value in sparse.items():
                        result[(pos+h*t)%self.n] += (delta**h)*value
                else:
                    result += (delta**h)*np.roll(self.kernels[h], (h*t)%self.n)
            return result
        q=np.asarray(indices,dtype=np.int64)
        if np.any(q<0) or np.any(q>=self.n):
            raise IndexError('invalid output coefficient index')
        out=self.kernels[0][q].copy()
        for h in range(1,self.degree+1):
            sparse=self.sparse_coefficients[h] if self.sparse_coefficients else None
            if sparse is not None:
                for pos,value in sparse.items():
                    out += (delta**h)*value*(q==((pos+h*t)%self.n))
            else:
                out += (delta**h)*self.kernels[h][(q-h*t)%self.n]
        return out

    def _normalized_edits(self,changes:Mapping[int,float]):
        e={}
        for p,amplitude in changes.items():
            t=int(p)
            if t!=p or not 0<=t<self.n:
                raise IndexError('invalid edit position')
            v=float(amplitude)
            if not np.isfinite(v):
                raise ValueError('nonfinite edit')
            e[t]=e.get(t,0.0)+v
        return [(t,v) for t,v in sorted(e.items()) if v!=0.0]

    def many(self, changes:Mapping[int,float], indices:Sequence[int] | None=None,
             *, max_shift_terms:int=96, method:str='auto'):
        """Exact polynomial update in sparse correction; no truncation.

        For small k,d use sum over at most sum(k^h) impulse products.
        Otherwise form sparse delta spectrum and perform one inverse FFT.
        """
        edits=self._normalized_edits(changes)
        if not edits or self.degree==0:
            if indices is None:
                return self.kernels[0].copy()
            q=np.asarray(indices,dtype=np.int64)
            if np.any(q<0) or np.any(q>=self.n):
                raise IndexError('invalid output coefficient index')
            return self.kernels[0][q].copy()
        nterms=sum(len(edits)**h for h in range(1,self.degree+1))
        if method not in ('auto','shifts','spectral'):
            raise ValueError('method must be auto, shifts or spectral')
        use_shifts = (method=='shifts' or (method=='auto' and nterms<=max_shift_terms))
        if self.degree==1:
            use_shifts=True
        if indices is None:
            if use_shifts:
                out=self.kernels[0].copy()
                for h in range(1,self.degree+1):
                    kernel=self.kernels[h]
                    # Aggregate identical phase-shift offsets before writing N outputs.
                    aggregated={}
                    for combo in itertools.product(edits, repeat=h):
                        t=sum(item[0] for item in combo)%self.n
                        coeff=float(np.prod([item[1] for item in combo]))
                        aggregated[t]=aggregated.get(t,0.)+coeff
                    for t,amp in aggregated.items():
                        if amp:
                            sparse=self.sparse_coefficients[h] if self.sparse_coefficients else None
                            if sparse is not None:
                                for pos,value in sparse.items():
                                    out[(pos+t)%self.n] += amp*value
                            else:
                                out += amp*np.roll(kernel,t)
                return out
            k=np.arange(self.engine.nfreq,dtype=np.float64)
            correction=np.zeros(self.engine.nfreq,dtype=np.complex128)
            for t,amp in edits:
                correction += amp*np.exp(-2j*np.pi*k*t/self.n)
            poly=self.frequency_coefficients[-1].copy()
            for h in range(self.degree-1,-1,-1):
                poly=poly*correction + self.frequency_coefficients[h]
            return np.asarray(_fft.irfft(poly,n=self.n),dtype=np.float64)
        q=np.asarray(indices,dtype=np.int64)
        if np.any(q<0) or np.any(q>=self.n):
            raise IndexError('invalid output coefficient index')
        if not use_shifts:
            return self.many(dict(edits),indices=None,method='spectral')[q]
        out=self.kernels[0][q].copy()
        for h in range(1,self.degree+1):
            aggregated={}
            for combo in itertools.product(edits,repeat=h):
                t=sum(item[0] for item in combo)%self.n
                coeff=float(np.prod([item[1] for item in combo]))
                aggregated[t]=aggregated.get(t,0.)+coeff
            for t,amp in aggregated.items():
                if amp:
                    sparse=self.sparse_coefficients[h] if self.sparse_coefficients else None
                    if sparse is not None:
                        for pos,value in sparse.items():
                            out += amp*value*(q==((pos+t)%self.n))
                    else:
                        out += amp*self.kernels[h][(q-t)%self.n]
        return out

    def single_frequency(self,position:int,delta:float,k:int) -> complex:
        t=int(position)
        k=int(k)
        delta=float(delta)
        if not np.isfinite(delta):
            raise ValueError('nonfinite edit')
        if not 0<=t<self.n or not 0<=k<self.n:
            raise IndexError('invalid position or frequency')
        index=k if k<=self.n//2 else self.n-k
        out=0j
        phase=np.exp((-2j*np.pi/self.n)*((t*k)%self.n))
        for h,coef in reversed(list(enumerate(self.frequency_coefficients))):
            v=coef[index] if k<=self.n//2 else np.conj(coef[index])
            out=out*phase*float(delta)+v
        return complex(out)


@dataclass(frozen=True)
class UpdatePlan:
    engine: AlgebraFFT
    root: int
    leaf: int
    compiled: PreparedEdit | None
    reason: str

    @property
    def mode(self) -> str:
        return 'jets' if self.compiled is not None else 'fallback'

    def single(self, position:int, delta:float,
               indices:Sequence[int] | None=None):
        if self.compiled is not None:
            return self.compiled.single(position,delta,indices=indices)
        newer=self.engine.edit_version(self.root,self.leaf,{position:delta})
        out=self.engine.evaluate_time(newer)
        return out if indices is None else out[indices]
