#!/usr/bin/env python3
"""Reusable calibrated binary-input FFT plans with a bounded process-local cache.

Inputs: C-contiguous 1-D NumPy uint8 or bool arrays containing only 0 and 1.
Lengths: powers of two from 16 through 2**31. Every execution validates values.
No dtype conversion occurs. Outputs: a fresh complex128 array or explicit out=.

A plan calibrates once at creation. Retuning is explicit via plan.retune().
Calibration uses seeded random inputs, not per-node or per-transform feedback.
"""
import ctypes as ct
from functools import lru_cache
import math
from pathlib import Path
import random
import subprocess
import time
import numpy as np

HERE=Path(__file__).resolve().parent
METHODS=('radix2_fused2','codelet4','codelet8','codelet16','lookup4','lookup8')
FLAGS=['-O3','-march=native','-DNDEBUG','-fno-math-errno','-ffp-contract=fast','-std=c11','-Wall','-Wextra','-fPIC','-shared']
_LIB=None


def _library():
    global _LIB
    if _LIB is not None:return _LIB
    binary=HERE/'libadaptive_fft.so'
    sources=[HERE/'adaptive_fft.c',HERE/'leaf_fft.c']
    if not binary.exists() or any(p.stat().st_mtime>binary.stat().st_mtime for p in sources):
        subprocess.run(['gcc',*FLAGS,str(sources[0]),'-lm','-o',str(binary)],check=True)
    lib=ct.CDLL(str(binary));P=ct.c_void_p;U=ct.c_uint
    lib.fft_adaptive_create.argtypes=[ct.c_size_t];lib.fft_adaptive_create.restype=P
    lib.fft_adaptive_destroy.argtypes=[P]
    lib.fft_adaptive_select.argtypes=[P,ct.c_int];lib.fft_adaptive_select.restype=ct.c_int
    lib.fft_adaptive_execute.argtypes=[P,P,P];lib.fft_adaptive_execute.restype=ct.c_int
    lib.fft_adaptive_execute_candidate.argtypes=[P,ct.c_int,P,P];lib.fft_adaptive_execute_candidate.restype=ct.c_int
    lib.fft_adaptive_bench_candidate.argtypes=[P,ct.c_int,P,U,P,U];lib.fft_adaptive_bench_candidate.restype=ct.c_double
    lib.fft_adaptive_bench_selected.argtypes=[P,P,U,P,U];lib.fft_adaptive_bench_selected.restype=ct.c_double
    _LIB=lib;return lib


def _ptr(a):return ct.c_void_p(a.ctypes.data)
def _check_status(status):
    if status==-2:raise ValueError('Input values must be exactly 0 or 1; output was not modified.')
    if status:raise RuntimeError(f'Native FFT returned status {status}')


def _length(n):
    if isinstance(n,bool) or not isinstance(n,(int,np.integer)) or n<16 or n&(n-1) or n>2**31:
        raise ValueError('N must be a power of two from 16 through 2**31.')
    return int(n)


def _dtype(dtype):
    d=np.dtype(dtype)
    if d not in (np.dtype(np.uint8),np.dtype(np.bool_)):
        raise TypeError('Only uint8 and bool are supported; no implicit dtype conversion is performed.')
    return d


class BinaryFFTPlan:
    """Owns an immutable FFT plan and 1/32 KiB lookup tables after calibration.

    Caller owns inputs and outputs. Concurrent execute calls with separate output
    arrays are supported; close/retune must not run concurrently with execution.
    Shared cached plans should not be closed by individual callers. Use
    clear_plan_cache() to release cache references; explicitly held plans remain
    open and can be closed individually when no longer in use.
    """
    def __init__(self,n,dtype=np.uint8,*,method=None,margin=0.08,rounds=9,target_ms=8,pool_count=4,seed=None):
        self.n=_length(n);self.dtype=_dtype(dtype);self._handle=None;self._lib=_library()
        self._margin=float(margin)
        if not 0<=self._margin<1:raise ValueError('margin must be in [0,1).')
        start=time.perf_counter();self._handle=self._lib.fft_adaptive_create(self.n)
        if not self._handle:raise MemoryError('Could not allocate native FFT plan.')
        self.setup_seconds=time.perf_counter()-start
        self.calibration_count=0
        try:
            if method is None:
                self.retune(rounds=rounds,target_ms=target_ms,pool_count=pool_count,seed=seed)
            else:
                _check_status(self._lib.fft_adaptive_select(self._handle,METHODS.index(method)))
                self.method=method
                self.calibration={'method':method,'status':'skipped_explicit_method','elapsed_ms':0.,'calibration_count':0}
        except BaseException:self.close();raise

    @property
    def closed(self):return self._handle is None
    def _open(self):
        if self.closed:raise RuntimeError('This FFT plan is closed.')

    def close(self):
        if self._handle is not None:self._lib.fft_adaptive_destroy(self._handle);self._handle=None
    def __enter__(self):self._open();return self
    def __exit__(self,*args):self.close()
    def __del__(self):
        try:self.close()
        except Exception:pass

    def _input(self,x):
        self._open()
        if not isinstance(x,np.ndarray):raise TypeError('Input must be a NumPy array; no implicit conversion is performed.')
        if x.dtype!=self.dtype:raise TypeError(f'Plan expects {self.dtype}; got {x.dtype}.')
        if x.ndim!=1 or x.size!=self.n:raise ValueError(f'Expected a one-dimensional array of length {self.n}.')
        if not x.flags.c_contiguous:raise ValueError('Input must be C-contiguous.')
        return x

    def _output(self,x,out):
        if out is None:return np.empty(self.n,dtype=np.complex128)
        if not isinstance(out,np.ndarray) or out.dtype!=np.complex128 or out.shape!=(self.n,) or not out.flags.c_contiguous or not out.flags.writeable or not out.flags.aligned:
            raise ValueError('out must be an aligned, writable C-contiguous complex128 array of matching length.')
        if np.shares_memory(x,out):raise ValueError('Input and output buffers must not overlap.')
        return out

    def execute(self,x,*,out=None):
        x=self._input(x);out=self._output(x,out)
        _check_status(self._lib.fft_adaptive_execute(self._handle,_ptr(x),_ptr(out)))
        return out

    def execute_candidate(self,method,x,*,out=None):
        """Explicit diagnostic control; normal callers should use execute()."""
        x=self._input(x);out=self._output(x,out);idx=METHODS.index(method)
        _check_status(self._lib.fft_adaptive_execute_candidate(self._handle,idx,_ptr(x),_ptr(out)))
        return out

    def benchmark(self,method,pool,out,repeats):
        """Timed C batch, including input-value validation and all FFT work."""
        self._open()
        if not isinstance(pool,np.ndarray) or pool.dtype!=self.dtype or pool.ndim!=2 or pool.shape[1]!=self.n or not pool.flags.c_contiguous:
            raise ValueError('pool must be a contiguous (count, N) array matching the plan dtype.')
        if len(pool)<1 or repeats<1 or repeats>2**32-1:raise ValueError('Invalid pool/repeat count.')
        self._output(pool,out)
        if method=='selected':
            value=self._lib.fft_adaptive_bench_selected(self._handle,_ptr(pool),len(pool),_ptr(out),int(repeats))
        else:
            value=self._lib.fft_adaptive_bench_candidate(self._handle,METHODS.index(method),_ptr(pool),len(pool),_ptr(out),int(repeats))
        if value<0:_check_status(int(value))
        return value

    def retune(self,*,rounds=9,target_ms=8,pool_count=4,seed=None):
        """Explicit one-time recalibration; never called by execute()."""
        self._open()
        if not 3<=rounds<=31 or not 1<=target_ms<=100 or not 1<=pool_count<=32:
            raise ValueError('Calibration requires 3..31 rounds, 1..100 target ms, and 1..32 inputs.')
        start=time.perf_counter()
        seed=int(seed if seed is not None else 0xA17F00+self.n+int(self.dtype==np.dtype(np.bool_)))
        pool=np.random.default_rng(seed).integers(0,2,(pool_count,self.n),dtype=np.uint8)
        if self.dtype==np.dtype(np.bool_):pool=pool.view(np.bool_)
        out=np.empty(self.n,dtype=np.complex128);samples={m:[] for m in METHODS};repeats={}
        reference=np.fft.fft(pool[0]);max_error=0.
        for m in METHODS:
            self.execute_candidate(m,pool[0],out=out)
            max_error=max(max_error,float(np.max(np.abs(out-reference))))
            np.testing.assert_allclose(out,reference,atol=2e-9,rtol=2e-11)
            estimate=self.benchmark(m,pool,out,pool_count*2)
            repeats[m]=max(pool_count,int(math.ceil(target_ms/1000/estimate/pool_count)*pool_count))
        order=list(METHODS);rng=random.Random(seed^0xBEEFF00D)
        for _ in range(rounds):
            rng.shuffle(order)
            for m in order:samples[m].append(self.benchmark(m,pool,out,repeats[m]))
        medians={m:float(np.median(s)) for m,s in samples.items()}
        arithmetic=min(METHODS[:4],key=medians.get);lookup=min(METHODS[4:],key=medians.get)
        advantage=1-medians[lookup]/medians[arithmetic]
        paired_wins=sum(a<b for a,b in zip(samples[lookup],samples[arithmetic]))
        stable=paired_wins>=math.ceil(0.75*rounds)
        chosen=lookup if advantage>=self._margin and stable else arithmetic
        _check_status(self._lib.fft_adaptive_select(self._handle,METHODS.index(chosen)))
        self.method=chosen;self.calibration_count+=1
        self.calibration={
            'method':chosen,'status':'calibrated','best_arithmetic':arithmetic,'best_lookup':lookup,
            'lookup_advantage_fraction':advantage,'required_lookup_advantage_fraction':self._margin,
            'arithmetic_fallback_used':chosen==arithmetic,'lookup_paired_round_wins':paired_wins,
            'required_lookup_paired_round_wins':math.ceil(0.75*rounds),'seed':seed,'rounds':rounds,
            'target_sample_ms':target_ms,'pool_count':pool_count,
            'samples_us':{m:[v*1e6 for v in s] for m,s in samples.items()},
            'median_us':{m:v*1e6 for m,v in medians.items()},'transforms_per_sample':repeats,
            'max_correctness_error':max_error,'elapsed_ms':(time.perf_counter()-start)*1000,
            'calibration_count':self.calibration_count,
        }
        return self.calibration


# Cache is bounded to eight (N, dtype) entries. Eviction releases the cache's
# reference; explicitly held plans remain alive until closed/released.
@lru_cache(maxsize=8)
def _cached_plan(n,dtype_str):return BinaryFFTPlan(n,np.dtype(dtype_str))


def get_plan(n,dtype=np.uint8):
    """Return the same calibrated plan on repeated requests for N and dtype."""
    n=_length(n);d=_dtype(dtype)
    plan=_cached_plan(n,d.str)
    if plan.closed:
        # Explicitly closing a shared cached plan invalidates it. Recreate on the
        # next access rather than returning a dangling native pointer.
        _cached_plan.cache_clear();plan=_cached_plan(n,d.str)
    return plan


def cache_info():return _cached_plan.cache_info()
def clear_plan_cache():
    """Release cached references. User-held plans remain open until close()."""
    _cached_plan.cache_clear()


def binary_fft(x,*,out=None):
    """Convenience API with a plan cache; returns independent outputs by default."""
    if not isinstance(x,np.ndarray):raise TypeError('Input must be a NumPy array.')
    d=_dtype(x.dtype)
    if x.ndim!=1:raise ValueError('Input must be one-dimensional.')
    return get_plan(x.size,d).execute(x,out=out)


if __name__=='__main__':
    import argparse,json
    ap=argparse.ArgumentParser();ap.add_argument('--size',type=int,default=4096);args=ap.parse_args()
    x=np.random.default_rng(7).integers(0,2,args.size,dtype=np.uint8)
    p=get_plan(x.size,x.dtype);y=p.execute(x)
    print(json.dumps({'n':p.n,'method':p.method,'plan_setup_ms':p.setup_seconds*1000,
                      'calibration_ms':p.calibration['elapsed_ms'],'cache_reused':p is get_plan(x.size,x.dtype),
                      'max_error':float(np.max(np.abs(y-np.fft.fft(x))))},indent=2))
