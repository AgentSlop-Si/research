"""Cost-aware choice between an existing prepared Phase-8 jet and Phase-9 JIT.

This *deliberately* treats cold compilation as a resource cost, and it compares
against the already-optimized Phase-8 prepared kernel rather than against fresh
FFTs alone. It is a heuristic planner, not an optimality theorem.
"""
from __future__ import annotations
from dataclasses import dataclass
import time
from typing import Sequence
import numpy as np
from compiled_kernels import compile_prepared, _generate_source, _FUNCTION_CACHE, njit


@dataclass
class AdaptiveKernel:
    prepared: object
    native: object | None
    mode: str
    reason: str
    estimated_breakeven_versions: int | None
    planning_seconds: float

    def single(self, position: int, delta: float, indices: Sequence[int] | None = None):
        chosen = self.native if self.mode == 'native' else self.prepared
        return chosen.single(position, delta, indices=indices)


def plan_auto(prepared, *, expected_versions: int, output_bins: Sequence[int] | None = None,
              min_unseen_jit_versions: int = 2048, max_compiled_bytes: int = 256*1024**2,
              samples: int = 6) -> AdaptiveKernel:
    """Choose compiled only if predicted savings amortize compiled startup.

    If no compilation for this symbolic shape has been cached, small batches
    stay on the existing NumPy jet path. This avoids the cold JIT cliff.
    For large batches, sample both completed backends on the exact same valid
    updates, including array allocation and output generation. Calibration
    costs are included in planning_seconds and in the breakeven calculation.
    """
    start = time.perf_counter()
    if type(expected_versions) is not int or expected_versions < 1:
        raise ValueError('expected_versions must be a positive integer')
    if type(min_unseen_jit_versions) is not int or min_unseen_jit_versions < 1:
        raise ValueError('invalid minimum JIT reuse')
    n = prepared.n
    extra=0
    for h in range(1, prepared.degree+1):
        d=prepared.kernels[h]
        if d is not None:extra+=d.nbytes
    extra += prepared.kernels[0].nbytes
    if extra > max_compiled_bytes:
        return AdaptiveKernel(prepared,None,'numpy','compiled kernel would exceed memory budget',None,time.perf_counter()-start)
    sparse=[];dense=[]
    for h in range(1,prepared.degree+1):
        c=prepared.sparse_coefficients[h] if prepared.sparse_coefficients else None
        if c is None:dense.append(h)
        else:
            for pos,amp in sorted(c.items()):
                if amp:sparse.append(h)
    # Compiler memoizes functions by shape, not by numeric input values.
    signature=_generate_source(tuple(dense),tuple(sparse),partial=output_bins is not None)
    cache_present=((signature,True) in _FUNCTION_CACHE and getattr(_FUNCTION_CACHE[(signature,True)],'signatures',()))
    if expected_versions < min_unseen_jit_versions and not cache_present:
        return AdaptiveKernel(prepared,None,'numpy','batch too small to justify an unseen JIT compile',None,time.perf_counter()-start)
    try:
        compiled=compile_prepared(prepared,backend='numba',max_degree=max(8,prepared.degree))
    except (RuntimeError,ValueError) as ex:
        return AdaptiveKernel(prepared,None,'numpy',f'JIT unavailable: {ex}',None,time.perf_counter()-start)
    q=np.asarray(output_bins,dtype=np.int64) if output_bins is not None else None
    events=[((i*1667+3)%n, 0.0001*(i+1)) for i in range(max(samples,2))]
    def run(obj):
        t0=time.perf_counter()
        for t,d in events:
            out=obj.single(t,d,indices=q)
            if not np.all(np.isfinite(out)):
                raise ArithmeticError('nonfinite benchmark output')
        return (time.perf_counter()-t0)/len(events)
    t_numpy=run(prepared)
    t_jit=run(compiled)
    spent=time.perf_counter()-start
    benefit=t_numpy-t_jit
    if benefit <= 0:
        return AdaptiveKernel(prepared,None,'numpy','Numba not faster than prepared NumPy on sampled workload',None,spent)
    # Startup is sunk in this call. Count it for the amortization decision, too.
    need=int(np.ceil(spent/benefit))
    if expected_versions < need:
        return AdaptiveKernel(prepared,None,'numpy',f'cold compilation/calibration needs about {need} versions to amortize',need,spent)
    return AdaptiveKernel(prepared,compiled,'native','expected workload amortizes measured startup versus prepared NumPy',need,spent)
