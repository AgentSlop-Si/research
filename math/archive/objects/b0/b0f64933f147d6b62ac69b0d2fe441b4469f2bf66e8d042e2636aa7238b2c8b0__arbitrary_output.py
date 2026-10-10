"""Shared output-pruned DFT plans for arbitrary requested Fourier bins.

For N = K*M, write a time index as n = m + M*r.  A Cooley--Tukey step gives

    X[j] = sum_m G[m, j mod K] * exp(-2*pi*i*m*j/N),

where G[m,:] is the K-point DFT of x[m + M*r] over r=0..K-1.

Thus one set of M length-K FFTs is shared by *all* requested outputs.  If K is
chosen on the order of q=|Q| (and K divides N), q arbitrary outputs cost
O(N log K + q*N/K) = O(N log q) arithmetic.  This is classical generic FFT
pruning; this module packages it for projected relation-aware Fourier views.

The plan stores only the final q-by-M phase matrix.  For K>=q this is at most
N complex numbers, independent of how scattered the requested bins are.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Sequence
import math
import time
import numpy as np

try:
    from scipy import fft as sp_fft
except ImportError:
    sp_fft = None


def _divisors(n: int) -> list[int]:
    small=[]; large=[]
    d=1
    while d*d<=n:
        if n%d==0:
            small.append(d)
            if d*d!=n: large.append(n//d)
        d+=1
    return small+large[::-1]


def candidate_radices(n:int,q:int) -> list[int]:
    """A small useful set of Cooley--Tukey inner sizes.

    The arithmetic proxy for one plan execution is log2(K)+q/K, ignoring
    backend constants.  Return divisors around the minimizer plus endpoints.
    """
    n=int(n); q=int(q)
    if n<1 or q<1 or q>n: raise ValueError('need 1<=q<=n')
    ds=_divisors(n)
    scored=[]
    for k in ds:
        score=(0.0 if k==1 else math.log2(k))+q/k
        scored.append((score,k))
    scored.sort()
    picks={1,n}
    for _,k in scored[:6]: picks.add(k)
    # Also include bracketing divisors around q; practical FFT constants often
    # move the optimum away from the arithmetic proxy.
    below=[d for d in ds if d<=q]
    above=[d for d in ds if d>=q]
    if below: picks.add(below[-1])
    if len(below)>1: picks.add(below[-2])
    if above: picks.add(above[0])
    if len(above)>1: picks.add(above[1])
    return sorted(picks)


def choose_radix(n:int,q:int) -> int:
    ds=candidate_radices(n,q)
    return min(ds,key=lambda k: ((0.0 if k==1 else math.log2(k))+q/k, k))


class FullFFTBinPlan:
    """Optimized full FFT fallback, gathering only requested bins."""
    strategy='full_fft'
    def __init__(self,n:int,bins:Sequence[int],*,backend='scipy'):
        self.n=int(n); self.backend=backend
        b=np.asarray(bins,dtype=np.int64)
        if b.ndim!=1 or b.size<1 or np.any(b<0) or np.any(b>=self.n):
            raise ValueError('bad bins')
        self.bins=b.astype(np.intp,copy=True); self.q=len(b)
    @property
    def plan_bytes(self): return int(self.bins.nbytes)
    def execute(self,x):
        a=np.asarray(x,dtype=np.complex128)
        if a.shape!=(self.n,): raise ValueError('input has wrong length')
        if self.backend=='scipy' and sp_fft is not None: y=sp_fft.fft(a)
        elif self.backend in ('scipy','numpy'): y=np.fft.fft(a)
        else: raise ValueError('backend must be scipy or numpy')
        return np.ascontiguousarray(y[self.bins])
    def project_stream(self,basis_vectors:Iterable[np.ndarray]):
        rows=[self.execute(row) for row in basis_vectors]
        return np.ascontiguousarray(np.stack(rows)) if rows else np.empty((0,self.q),np.complex128)


class ArbitraryBinsDFTPlan:
    """Reusable exact (up to floating-point roundoff) arbitrary-output plan."""
    strategy='arbitrary_pruned'
    def __init__(self,n:int,bins:Sequence[int],*,radix:int|str='auto',backend='scipy'):
        self.n=int(n); self.backend=backend
        if self.n<1: raise ValueError('n must be positive')
        b=np.asarray(bins,dtype=np.int64)
        if b.ndim!=1 or b.size<1 or np.any(b<0) or np.any(b>=self.n):
            raise ValueError('bad bins')
        self.bins=b.astype(np.intp,copy=True); self.q=len(self.bins)
        if radix=='auto': k=choose_radix(self.n,self.q)
        else: k=int(radix)
        if k<1 or self.n%k: raise ValueError('radix must be a positive divisor of n')
        self.k=k; self.m=self.n//self.k
        self.residue=np.asarray(self.bins % self.k,dtype=np.intp)
        mm=np.arange(self.m,dtype=np.float64)
        # phase[t,m] corresponds to requested global bin bins[t].
        self.phase=np.exp((-2j*np.pi/self.n)*np.outer(self.bins.astype(np.float64),mm))
    @property
    def plan_bytes(self):
        return int(self.phase.nbytes+self.bins.nbytes+self.residue.nbytes)
    @property
    def arithmetic_proxy(self):
        return (0.0 if self.k==1 else math.log2(self.k))+self.q/self.k
    def execute(self,x):
        a=np.asarray(x,dtype=np.complex128)
        if a.shape!=(self.n,): raise ValueError('input has wrong length')
        if self.k==1:
            # q is normally tiny here.  groups[:,0] is just x in the required
            # Cooley--Tukey ordering.
            col=a
            return np.einsum('qm,m->q',self.phase,col,optimize=False)
        groups=np.ascontiguousarray(a.reshape(self.k,self.m).T)
        if self.backend=='scipy' and sp_fft is not None:
            inner=sp_fft.fft(groups,axis=1)
        elif self.backend in ('scipy','numpy'):
            inner=np.fft.fft(groups,axis=1)
        else: raise ValueError('backend must be scipy or numpy')
        selected=inner[:,self.residue]  # M x q, one inner output per requested bin
        return np.einsum('mq,qm->q',selected,self.phase,optimize=False)
    def project_stream(self,basis_vectors:Iterable[np.ndarray]):
        rows=[self.execute(row) for row in basis_vectors]
        return np.ascontiguousarray(np.stack(rows)) if rows else np.empty((0,self.q),np.complex128)


@dataclass(frozen=True)
class PlanChoice:
    strategy:str
    radix:int|None
    execute_ms:float|None
    full_ms:float|None


class AutoOutputPlan:
    """Measured query-plan chooser over pruned radices and a full FFT.

    With ``sample`` supplied, nearby Cooley--Tukey radices are timed on the
    actual machine subject to ``max_plan_bytes``.  The fastest execution plan
    is retained.  ``calibration_ms`` is exposed and must be charged by callers;
    the tuner is intended for many repeated registrations/queries, not one-offs.

    Without a sample, a conservative arithmetic/memory heuristic is used.
    """
    def __init__(self,n:int,bins:Sequence[int],*,backend='scipy',sample=None,
                 reps=2,max_plan_bytes=128*1024*1024):
        self.n=int(n); self.bins=np.asarray(bins,dtype=np.intp); self.q=len(self.bins)
        self.backend=backend; self.max_plan_bytes=int(max_plan_bytes)
        if self.q<1: raise ValueError('bins must be nonempty')
        self.calibration_ms=0.0; self.candidates=[]; self.sample_result=None
        full=FullFFTBinPlan(n,bins,backend=backend)
        if sample is None:
            # Prefer a radix >= q when possible so the phase table is O(N),
            # then fall back to the arithmetic minimizer.
            ds=[k for k in candidate_radices(self.n,self.q) if self.n%k==0]
            feasible=[k for k in ds if self.q*(self.n//k)*16 <= self.max_plan_bytes]
            ge=[k for k in feasible if k>=self.q]
            k=min(ge) if ge else (min(feasible,key=lambda z: ((0 if z==1 else math.log2(z))+self.q/z)) if feasible else self.n)
            pruned=ArbitraryBinsDFTPlan(n,bins,radix=k,backend=backend)
            use_pruned=(self.q <= max(1,self.n//100))
            self.impl=pruned if use_pruned else full
            self.choice=PlanChoice(self.impl.strategy,k if use_pruned else None,None,None)
            return

        a=np.asarray(sample,dtype=np.complex128)
        if a.shape!=(self.n,): raise ValueError('sample has wrong length')
        reps=max(1,int(reps))
        t_cal=time.perf_counter_ns()
        # Full-FFT timing and result.
        full.execute(a)
        vals=[]; full_result=None
        for _ in range(reps):
            t=time.perf_counter_ns(); full_result=full.execute(a); vals.append((time.perf_counter_ns()-t)/1e6)
        full_ms=float(np.median(vals))
        best_impl=full; best_ms=full_ms; best_result=full_result; best_radix=None
        self.candidates.append({'strategy':'full_fft','radix':None,'execute_ms':full_ms,'plan_bytes':full.plan_bytes})

        for k in candidate_radices(self.n,self.q):
            if k>=self.n: continue
            phase_bytes=self.q*(self.n//k)*16
            if phase_bytes>self.max_plan_bytes: continue
            p=ArbitraryBinsDFTPlan(self.n,self.bins,radix=k,backend=backend)
            p.execute(a)  # warm
            vals=[]; result=None
            for _ in range(reps):
                t=time.perf_counter_ns(); result=p.execute(a); vals.append((time.perf_counter_ns()-t)/1e6)
            tm=float(np.median(vals))
            self.candidates.append({'strategy':'arbitrary_pruned','radix':k,'execute_ms':tm,'plan_bytes':p.plan_bytes})
            if tm<best_ms:
                best_impl=p; best_ms=tm; best_result=result; best_radix=k
            # Non-winning plans are dropped immediately; only their timing is retained.
        self.impl=best_impl; self.sample_result=np.ascontiguousarray(best_result)
        self.calibration_ms=(time.perf_counter_ns()-t_cal)/1e6
        self.choice=PlanChoice(self.impl.strategy,best_radix,best_ms,full_ms)

    @property
    def strategy(self): return self.impl.strategy
    @property
    def plan_bytes(self): return self.impl.plan_bytes
    def execute(self,x): return self.impl.execute(x)
    def project_stream(self,basis_vectors): return self.impl.project_stream(basis_vectors)

    def project_stream_with_sample(self,sample,basis_vectors):
        """Use the already-computed calibration output for the first basis row."""
        if self.sample_result is None:
            first=self.execute(sample)
        else:
            first=self.sample_result.copy()
        rows=[first]
        rows.extend(self.execute(row) for row in basis_vectors)
        return np.ascontiguousarray(np.stack(rows))



def productive_radices(n:int,q:int,max_plan_bytes=128*1024*1024,limit=4) -> list[int]:
    """Radices worth trying when every trial will process a real basis row."""
    ds=[d for d in _divisors(int(n)) if d<int(n)]
    if not ds: return []
    targets=[]
    # Practical measurements often prefer a larger K than the arithmetic
    # minimum because larger inner FFTs improve locality and shrink the final
    # phase-combination table.
    for mul in (1,2,4,8): targets.append(max(1,int(q)*mul))
    targets.append(choose_radix(n,q))
    picks=[]
    for target in targets:
        feasible=[d for d in ds if q*(n//d)*16<=max_plan_bytes]
        if not feasible: continue
        k=min(feasible,key=lambda d:(abs(math.log(max(d,1)/max(target,1))),d))
        if k not in picks:picks.append(k)
    # Prefer the practical 4q neighborhood first, then nearby alternatives.
    picks.sort(key=lambda k:(abs(math.log(max(k,1)/max(4*q,1))),k))
    return picks[:max(1,int(limit))]


@dataclass
class ProductivePlannerStats:
    chosen_strategy:str
    chosen_radix:int|None
    planning_ms:float
    trials:list
    basis_count:int


class ProductiveProjectionPlanner:
    """Autotune while doing useful basis registrations.

    Each candidate strategy is evaluated on a *different basis vector whose
    projection is required anyway*.  Hence no transform execution is thrown
    away.  Only construction of losing pruned plans is pure tuning overhead.
    After the productive trials, all remaining basis rows use the fastest
    observed strategy.
    """
    def __init__(self,n:int,bins:Sequence[int],*,backend='scipy',
                 max_plan_bytes=128*1024*1024,max_pruned_trials=3):
        self.n=int(n); self.bins=np.asarray(bins,dtype=np.intp); self.q=len(self.bins)
        self.backend=backend; self.max_plan_bytes=int(max_plan_bytes)
        self.max_pruned_trials=int(max_pruned_trials)
        self.stats=None

    def project(self,basis_vectors:Iterable[np.ndarray], *, expected_count:int|None=None):
        it=iter(basis_vectors); rows=[]; trials=[]; planning_ms=0.0
        full=FullFFTBinPlan(self.n,self.bins,backend=self.backend)
        # Strategy table stores (observed execution ms, plan object).
        strategies=[]
        try:first=next(it)
        except StopIteration:
            self.stats=ProductivePlannerStats('none',None,0.0,[],0)
            return np.empty((0,self.q),dtype=np.complex128)
        t=time.perf_counter_ns(); y=full.execute(first); ms=(time.perf_counter_ns()-t)/1e6
        rows.append(y); trials.append({'strategy':'full_fft','radix':None,'execute_ms':ms,'plan_bytes':full.plan_bytes})
        strategies.append((ms,full,None))
        count=1

        # Do not tune aggressively if the caller says there are too few rows to
        # amortize even plan construction.  Unknown count assumes a stream.
        max_trials=self.max_pruned_trials
        if expected_count is not None:
            max_trials=min(max_trials,max(0,int(expected_count)-2))
        for k in productive_radices(self.n,self.q,self.max_plan_bytes,max_trials):
            try: row=next(it)
            except StopIteration: break
            tp=time.perf_counter_ns(); p=ArbitraryBinsDFTPlan(self.n,self.bins,radix=k,backend=self.backend); planning_ms+=(time.perf_counter_ns()-tp)/1e6
            t=time.perf_counter_ns(); y=p.execute(row); ms=(time.perf_counter_ns()-t)/1e6
            rows.append(y); count+=1
            trials.append({'strategy':'arbitrary_pruned','radix':k,'execute_ms':ms,'plan_bytes':p.plan_bytes})
            strategies.append((ms,p,k))

        best_ms,best,best_k=min(strategies,key=lambda z:z[0])
        for row in it:
            rows.append(best.execute(row)); count+=1
        self.stats=ProductivePlannerStats(best.strategy,best_k,planning_ms,trials,count)
        return np.ascontiguousarray(np.stack(rows))
