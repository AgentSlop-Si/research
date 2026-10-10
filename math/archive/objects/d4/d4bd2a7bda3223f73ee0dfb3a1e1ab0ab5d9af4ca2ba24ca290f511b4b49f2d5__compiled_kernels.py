"""Phase 9: bounded algebraic-jet code generation with fused native execution.

The symbolic expansion is built by the Phase-8 AlgebraFFT object. This module
specializes its already-verified coefficient kernels and emits a fused loop:
  y[q] = C0[q] + sum_h delta**h C_h[(q-h*pos) % n].
Symbolically sparse C_h are applied as point updates outside the dense loop.

Numba JIT is OPTIONAL. JIT compilation and all initial FFT/jet preparation
must be charged in cold-start timings. This is a dynamic convolution update,
not an arbitrary faster Fourier transform.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import math
import time
import numpy as np

try:
    from numba import njit
except ImportError:
    njit = None


def _valid_input(n: int, position: int, delta: float) -> tuple[int, float]:
    p = int(position)
    if p != position or not 0 <= p < n:
        raise IndexError("position must be an integer inside the signal")
    d = float(delta)
    if not np.isfinite(d):
        raise ValueError("edit amplitude must be finite")
    return p, d


def _generate_source(dense_degrees: tuple[int, ...],
                     sparse_degrees: tuple[int, ...],
                     *, partial: bool) -> str:
    """Generate only numeric literals from validated degrees (no source input)."""
    inputs = "base, dense, sparse_positions, sparse_amplitudes, indices, position, delta" if partial else "base, dense, sparse_positions, sparse_amplitudes, position, delta"
    src = [f"def run({inputs}):",
           "    n = len(base)"]
    if partial:
        src += ["    out = np.empty(len(indices), dtype=np.float64)"]
    else:
        src += ["    out = np.empty(n, dtype=np.float64)"]
    for j,h in enumerate(dense_degrees):
        src += [f"    shift_{j} = ({h} * position) % n",
                f"    scale_{j} = delta ** {h}"]
    for j,h in enumerate(sparse_degrees):
        src += [f"    sparse_at_{j} = (sparse_positions[{j}] + {h} * position) % n",
                f"    sparse_scale_{j} = (delta ** {h}) * sparse_amplitudes[{j}]"]
    src += ["    for ii in range(len(indices)):" if partial else "    for ii in range(n):"]
    src += ["        q = indices[ii]" if partial else "        q = ii",
            "        value = base[q]"]
    for j,h in enumerate(dense_degrees):
        src += [f"        idx_{j} = q - shift_{j}",
                f"        if idx_{j} < 0:",
                f"            idx_{j} += n",
                f"        value += scale_{j} * dense[{j}, idx_{j}]"]
    if partial:
        for j,h in enumerate(sparse_degrees):
            src += [f"        if q == sparse_at_{j}:",
                    f"            value += sparse_scale_{j}"]
    src += ["        out[ii] = value"]
    if not partial:
        for j,h in enumerate(sparse_degrees):
            src += [f"    out[sparse_at_{j}] += sparse_scale_{j}"]
    src += ["    return out"]
    return "\n".join(src) + "\n"


_FUNCTION_CACHE = {}  # reuse compiled kernels across plans and FFT sizes

def _build_function(source: str, use_numba: bool):
    key = (source, use_numba)
    if key in _FUNCTION_CACHE:
        return _FUNCTION_CACHE[key]
    scope = {"np": np}
    exec(compile(source, "<fft_phase9_generated>", "exec"), scope)
    f = scope["run"]
    if use_numba:
        if njit is None:
            raise RuntimeError("numba is not installed. Use backend='python'.")
        f = njit(f, fastmath=False, nogil=True, cache=False)
    _FUNCTION_CACHE[key] = f
    return f


@dataclass
class SpecializedJet:
    n: int
    degree: int
    base: np.ndarray
    dense: np.ndarray
    dense_degrees: tuple[int, ...]
    sparse_positions: np.ndarray
    sparse_amplitudes: np.ndarray
    sparse_degrees: tuple[int, ...]
    full_source: str
    partial_source: str
    _full: object
    _partial: object
    backend: str
    compiler_wall_s: float
    jit_wall_s: float

    @property
    def data_bytes(self) -> int:
        return (self.base.nbytes + self.dense.nbytes +
                self.sparse_positions.nbytes + self.sparse_amplitudes.nbytes)

    @property
    def generated_source(self) -> str:
        return self.full_source

    def single(self, position: int, delta: float, indices: Sequence[int] | None = None) -> np.ndarray:
        pos, d = _valid_input(self.n, position, delta)
        if indices is None:
            return self._full(self.base, self.dense, self.sparse_positions,
                              self.sparse_amplitudes, pos, d)
        q = np.asarray(indices)
        if q.ndim == 1 and q.size == 0:
            return np.empty(0, dtype=np.float64)
        if q.ndim != 1 or not np.issubdtype(q.dtype, np.integer):
            raise TypeError("indices must be a 1D integer array")
        if np.any(q < 0) or np.any(q >= self.n):
            raise IndexError("output coefficient index outside signal")
        q = np.ascontiguousarray(q, dtype=np.int64)
        return self._partial(self.base, self.dense, self.sparse_positions,
                             self.sparse_amplitudes, q, pos, d)


def compile_prepared(prepared, *, backend: str = "numba", max_degree: int = 8,
                     max_sparse_terms: int = 64,
                     warm_compile: bool = True) -> SpecializedJet:
    """Prepare code from Phase-8 PreparedEdit, without rediscovering its graph.

    Bounds on degree and sparse terms avoid pathological code generation.
    The compiler trusts Phase-8's symbolic sparsity certificates, NOT tiny
    float values rounded to zero.
    """
    t0 = time.perf_counter()
    if backend not in {"numba", "python"}:
        raise ValueError("backend must be 'numba' or 'python'")
    degree = int(prepared.degree)
    if not 0 <= degree <= max_degree or max_degree > 16:
        raise ValueError("degree exceeds bounded code-generation limit")
    n = int(prepared.n)
    base = np.ascontiguousarray(prepared.kernels[0], dtype=np.float64)
    dense_list, dense_degrees = [], []
    sparse_positions, sparse_amplitudes, sparse_degrees = [], [], []
    for h in range(1, degree + 1):
        sparse = prepared.sparse_coefficients[h] if prepared.sparse_coefficients else None
        if sparse is not None:
            for t, weight in sorted(sparse.items()):
                if weight:
                    sparse_positions.append(int(t))
                    sparse_amplitudes.append(float(weight))
                    sparse_degrees.append(h)
        else:
            dense_list.append(np.asarray(prepared.kernels[h], dtype=np.float64))
            dense_degrees.append(h)
    if len(sparse_positions) > max_sparse_terms:
        raise ValueError("too many symbolic sparse terms to inline")
    dense = np.ascontiguousarray(np.stack(dense_list, axis=0), dtype=np.float64) if dense_list else np.empty((0,n),dtype=np.float64)
    sp = np.asarray(sparse_positions, dtype=np.int64)
    sv = np.asarray(sparse_amplitudes, dtype=np.float64)
    dense_degree_tuple = tuple(dense_degrees)
    sparse_degree_tuple = tuple(sparse_degrees)
    full_source = _generate_source(dense_degree_tuple, sparse_degree_tuple, partial=False)
    partial_source = _generate_source(dense_degree_tuple, sparse_degree_tuple, partial=True)
    full = _build_function(full_source, use_numba=backend=="numba")
    partial = _build_function(partial_source, use_numba=backend=="numba")
    t1 = time.perf_counter()
    jit_s = 0.0
    if backend == "numba" and warm_compile:
        start = time.perf_counter()
        # Real code JIT compilation is a cost; do not silently omit it.
        _ = full(base,dense,sp,sv,0,0.0)
        _ = partial(base,dense,sp,sv,np.asarray([0],dtype=np.int64),0,0.0)
        jit_s = time.perf_counter() - start
    return SpecializedJet(n,degree,base,dense,dense_degree_tuple,sp,sv,sparse_degree_tuple,
                          full_source,partial_source,full,partial,backend,t1-t0,jit_s)


def compile_expression(engine, root:int, leaf:int, *, backend="numba", max_degree=4):
    """Public Phase-9 end-to-end compilation entrypoint."""
    prepared = engine.prepare(root,leaf,max_degree=max_degree)
    return compile_prepared(prepared,backend=backend,max_degree=max_degree)
