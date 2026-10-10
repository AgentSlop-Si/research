"""Phase 10: persistent two-factor convolution edits using exact bivariate jets.

Given a sum/convolution DAG F(A,B), compile coefficient kernels K_{h,l}:
 F(A+alpha*e_s,B+beta*e_t)[q]
 = sum_{h,l} alpha**h beta**l K_{h,l}[(q-h*s-l*t) mod N].

The identity holds over any commutative ring. Numeric prepared kernels here
use scipy's float64 real FFT, so production answers are approximate.
AOT native work is performed by the prebuilt C++ library; there is NO
runtime C++ compilation, Numba JIT, or eval/exec in this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from functools import lru_cache
import ctypes
import json
import sys
import time
import numpy as np
from algebra_fft import AlgebraFFT, DegreeExceeded

C_INT64=ctypes.c_int64
C_DBL=ctypes.c_double
PTR=ctypes.c_void_p

@lru_cache(maxsize=2)
def _load_aot(path: str):
    lib=ctypes.CDLL(path)
    fun=lib.fft10_eval
    fun.argtypes=[C_INT64,PTR,PTR,C_INT64,PTR,PTR,C_INT64,PTR,PTR,PTR,PTR,
                  C_INT64,C_DBL,C_INT64,C_DBL,PTR,C_INT64,PTR]
    fun.restype=ctypes.c_int
    return fun


def _native_path():
    filename=('fft_phase10.dll' if sys.platform=='win32' else
              'libfft_phase10.dylib' if sys.platform=='darwin' else
              'libfft_phase10.so')
    path=Path(__file__).resolve().parent/filename
    return str(path) if path.is_file() else None



@lru_cache(maxsize=2)
def _load_shape(path):
    lib=ctypes.CDLL(path)
    fn=lib.fft10_shape_eval
    fn.argtypes=[C_INT64,PTR,PTR,PTR,PTR,C_INT64,C_DBL,C_INT64,C_DBL,PTR,C_INT64,PTR]
    fn.restype=ctypes.c_int
    return fn


@lru_cache(maxsize=1)
def _offline_shape_manifest():
    """Read the build-time signature once, never scan or JIT during updates."""
    root=Path(__file__).resolve().parent
    manifest=root/'shape_manifest.json'
    if not manifest.exists():return None
    try:
        info=json.loads(manifest.read_text())
        path=root/info['native_library']
        if path.is_file():return info,str(path)
    except (OSError,KeyError,TypeError,ValueError):
        pass
    return None


def _matching_shape(plan):
    """Only select the AOT kernel if all symbolic coefficient degrees match."""
    info=_offline_shape_manifest()
    if info is None:return None
    manifest,path=info
    spec=manifest['shape']
    dense=list(map(list,zip(map(int,plan.dense_a),map(int,plan.dense_b))))
    sparse=list(map(list,zip(map(int,plan.sparse_a),map(int,plan.sparse_b))))
    return path if spec['dense']==dense and spec['sparse']==sparse else None


def _pointer(arr):
    return ctypes.c_void_p(arr.ctypes.data)


def _validate_pos(n, pos, delta, name):
    if not isinstance(pos,(int,np.integer)) or isinstance(pos,(bool,np.bool_)) or not 0 <= pos < n:
        raise IndexError(f'{name} position must be an integer in [0,{n})')
    if not np.isscalar(delta) or not np.isfinite(delta):
        raise ValueError(f'{name} delta must be finite scalar')
    return int(pos),float(delta)


def _output_indices(n, indices):
    if indices is None:
        return None
    q=np.asarray(indices)
    if q.ndim==1 and q.size==0:
        return np.empty(0,dtype=np.int64)
    if q.ndim !=1 or not np.issubdtype(q.dtype,np.integer):
        raise TypeError('indices must be a one-dimensional integer array')
    if np.any((q < 0) | (q >= n)):
        raise IndexError('output index out of bounds')
    return np.ascontiguousarray(q,dtype=np.int64)


def _freeze(arr, dtype):
    x=np.ascontiguousarray(arr,dtype=dtype)
    x.flags.writeable=False
    return x


@dataclass(frozen=True)
class TwoEditPlan:
    n: int
    root: int
    target_a: int
    target_b: int
    total_degree: int
    base: np.ndarray
    dense: np.ndarray
    dense_a: np.ndarray
    dense_b: np.ndarray
    sparse_a: np.ndarray
    sparse_b: np.ndarray
    sparse_positions: np.ndarray
    sparse_weights: np.ndarray
    symbolic_terms: tuple[tuple[int,int], ...]
    preparation_seconds: float
    number_original_nodes: int
    number_symbolic_nodes: int
    linear_direct_coefficients: int = 0

    @property
    def memory_bytes(self):
        return sum(v.nbytes for v in (
            self.base,self.dense,self.dense_a,self.dense_b,self.sparse_a,self.sparse_b,
            self.sparse_positions,self.sparse_weights))

    @property
    def native_available(self):
        return _native_path() is not None

    @property
    def shape_available(self):
        return _matching_shape(self) is not None

    @property
    def coefficient_count(self):
        return len(self.symbolic_terms)

    def update(self, pos_a, delta_a, pos_b, delta_b, indices=None, *, backend='auto'):
        """Both edits are relative to the two immutable base factors.
        backend='native': generic compiled library must exist.
        backend='aot_shape': previously generated and compiled symbolic-shape library required.
        backend='numpy': vectorized fallback.
        backend='auto': AOT shape if matching; otherwise generic AOT, then NumPy.
        There is never any runtime compilation.
        """
        sa,alpha=_validate_pos(self.n,pos_a,delta_a,'A')
        sb,beta=_validate_pos(self.n,pos_b,delta_b,'B')
        q=_output_indices(self.n,indices)
        if backend not in ('auto','native','aot_shape','numpy'):
            raise ValueError('backend must be auto, native, aot_shape or numpy')
        if backend in ('auto','aot_shape'):
            path=_matching_shape(self)
            if path is not None:
                return self._shape(path,sa,alpha,sb,beta,q)
            if backend=='aot_shape':
                raise RuntimeError('No precompiled shape library matches this plan')
        if backend in ('auto','native'):
            path=_native_path()
            if path is not None:
                return self._native(path,sa,alpha,sb,beta,q)
            if backend=='native':
                raise RuntimeError('Generic AOT library missing; run python build_native.py once')
        return self._numpy(sa,alpha,sb,beta,q)

    def _native(self,path,pa,alpha,pb,beta,q):
        out=np.empty(self.n if q is None else len(q), dtype=np.float64)
        status=_load_aot(path)(
            self.n, _pointer(self.base), _pointer(self.dense),
            len(self.dense_a), _pointer(self.dense_a), _pointer(self.dense_b),
            len(self.sparse_a), _pointer(self.sparse_a), _pointer(self.sparse_b),
            _pointer(self.sparse_positions), _pointer(self.sparse_weights),
            pa, alpha, pb, beta,
            None if q is None else _pointer(q), len(out), _pointer(out))
        if status:
            raise RuntimeError(f'Native kernel failed with error code {status}')
        return out

    def _shape(self,path,pa,alpha,pb,beta,q):
        out=np.empty(self.n if q is None else len(q),dtype=np.float64)
        code=_load_shape(path)(
            self.n,_pointer(self.base),_pointer(self.dense),
            _pointer(self.sparse_positions),_pointer(self.sparse_weights),
            pa,alpha,pb,beta,None if q is None else _pointer(q),len(out),_pointer(out))
        if code:raise RuntimeError(f'AOT shape kernel failed with code {code}')
        return out

    def _numpy(self,pa,alpha,pb,beta,q):
        n=self.n
        out=self.base.copy() if q is None else self.base[q].copy()
        for h,(da,db) in enumerate(zip(self.dense_a,self.dense_b)):
            shift=(int(da)*pa+int(db)*pb)%n
            coeff=(alpha**int(da))*(beta**int(db))
            if coeff==0: continue
            if q is None:
                out+=coeff*np.roll(self.dense[h],shift)
            else:
                out+=coeff*self.dense[h,(q-shift)%n]
        for da,db,p,weight in zip(self.sparse_a,self.sparse_b,
                                   self.sparse_positions,self.sparse_weights):
            shifted=(int(p)+int(da)*pa+int(db)*pb)%n
            incr=float(weight)*(alpha**int(da))*(beta**int(db))
            if q is None:out[shifted]+=incr
            else:out[q==shifted]+=incr
        return out


def _bivariate_symbolic(engine:AlgebraFFT, root:int, a:int, b:int,
                        max_degree:int, max_terms:int):
    """Exact algebraic DAG expansion; no numerical zero thresholds."""
    if a==b or engine._get(a).op!='seed' or engine._get(b).op!='seed':
        raise ValueError('two distinct seed nodes required')
    da=engine.degree_in(root,a)
    db=engine.degree_in(root,b)
    if da+db>max_degree:
        raise DegreeExceeded(f'combined upper degree {da+db} exceeds bound {max_degree}')
    original_nodes=engine.reachable_count(root)
    memo={}
    zero=engine.zero
    for uid in engine._topological(root):
        nd=engine.nodes[uid]
        if uid==a:
            memo[uid]={(0,0):uid,(1,0):engine.one}
        elif uid==b:
            memo[uid]={(0,0):uid,(0,1):engine.one}
        elif nd.op in ('seed','const','impulse'):
            memo[uid]={(0,0):uid}
        elif nd.op=='scale':
            memo[uid]={p:engine.scale(v,nd.scalar) for p,v in memo[nd.args[0]].items()}
        elif nd.op=='sum':
            result={}
            for child,weight in zip(nd.args,nd.weights):
                for p,v in memo[child].items():
                    term=engine.scale(v,weight)
                    result[p]=engine.add(result.get(p,zero),term)
            memo[uid]=result
        elif nd.op=='product':
            res={(0,0):engine.const(nd.scalar)}
            for child in nd.args:
                nxt={}
                for (i,j),lhs in res.items():
                    for (h,l),rhs in memo[child].items():
                        coord=(i+h,j+l)
                        if coord[0]+coord[1]>max_degree:
                            raise DegreeExceeded('unexpected degree overflow')
                        nxt[coord]=engine.add(nxt.get(coord,zero), engine.mul(lhs,rhs))
                res=nxt
                if len(res)>max_terms:
                    raise DegreeExceeded('too many bivariate coefficients')
            memo[uid]=res
        else:
            raise AssertionError(f'unknown graph node: {nd.op}')
    result={p:u for p,u in memo[root].items() if u!=zero}
    if (0,0) not in result:result[(0,0)]=zero
    if len(result)>max_terms:
        raise DegreeExceeded('too many bivariate coefficients')
    return result,original_nodes



def _direct_time_if_affine(engine, uid, *, max_terms=24):
    """Evaluate affine combinations of shifted original signals in O(terms*N).

    If the expression contains a convolution of two general signals, return
    None and use the verified frequency-domain fallback. This is an exact
    syntactic certificate, not a test for numerically tiny coefficients.
    """
    def merge_scaled(dst, src, mul):
        for key, value in src.items():
            dst[key]=dst.get(key,0.) + mul*value
        return {k:v for k,v in dst.items() if v}

    results={}
    for v in engine._topological(uid):
        nd=engine.nodes[v]
        if nd.op=='seed':
            current=({(v,0):1.}, {})
        elif nd.op=='const':
            current=({}, {0:nd.scalar} if nd.scalar else {})
        elif nd.op=='impulse':
            current=({}, {nd.index:nd.scalar})
        elif nd.op=='scale':
            child=results[nd.args[0]]
            current=None if child is None else (
                {key:nd.scalar*x for key,x in child[0].items() if nd.scalar*x},
                {key:nd.scalar*x for key,x in child[1].items() if nd.scalar*x})
        elif nd.op=='sum':
            dense={};sparse={}
            for child_id,weight in zip(nd.args,nd.weights):
                child=results[child_id]
                if child is None:
                    dense=None
                    break
                dense=merge_scaled(dense,child[0],weight)
                sparse=merge_scaled(sparse,child[1],weight)
            current=None if dense is None else (dense,sparse)
        elif nd.op=='product':
            dense={};sparse={0:nd.scalar}
            for child_id in nd.args:
                child=results[child_id]
                if child is None or (dense and child[0]):
                    dense=None
                    break
                cd,cs=child
                new_dense={};new_sparse={}
                for (seed,off),value in dense.items():
                    for t,w in cs.items():
                        key=(seed,(off+t)%engine.n)
                        new_dense[key]=new_dense.get(key,0.)+value*w
                for (seed,off),value in cd.items():
                    for t,w in sparse.items():
                        key=(seed,(off+t)%engine.n)
                        new_dense[key]=new_dense.get(key,0.)+value*w
                for t,v0 in sparse.items():
                    for u,v1 in cs.items():
                        key=(t+u)%engine.n
                        new_sparse[key]=new_sparse.get(key,0.)+v0*v1
                dense={k:v for k,v in new_dense.items() if v}
                sparse={k:v for k,v in new_sparse.items() if v}
                if len(dense)+len(sparse)>max_terms:
                    dense=None
                    break
            current=None if dense is None else (dense,sparse)
        else:
            current=None
        if current is not None and len(current[0])+len(current[1])>max_terms:
            current=None
        results[v]=current
    result=results[uid]
    if result is None:return None
    dense,sparse=result
    out=np.zeros(engine.n,dtype=np.float64)
    for (seed,offset),amp in dense.items():
        out += amp*np.roll(engine._seeds[seed],offset)
    for offset,amp in sparse.items():
        out[offset]+=amp
    return out


def prepare_two(engine:AlgebraFFT, root:int, target_a:int, target_b:int,
                *, max_total_degree=5,max_terms=24,max_sparse_positions=24,
                max_kernel_bytes=256*1024*1024):
    """Prepare a bivariate *exact algebraic* update from Phase 8's graph.

    Prep requires transformed coefficient kernels, up to O(terms N log N)
    for inverse FFT and O(terms N) spectral DAG calculations (plus graph work).
    High-degree expressions are rejected, not silently truncated.
    """
    if max_total_degree<1 or max_total_degree>12 or max_terms<1:
        raise ValueError('invalid compilation bounds')
    start=time.perf_counter()
    coeffs,orig=_bivariate_symbolic(engine,root,target_a,target_b,max_total_degree,max_terms)
    n=engine.n
    if 8*n*(len(coeffs)+1)>max_kernel_bytes:
        raise MemoryError('prepared kernel estimate exceeds memory budget')
    sparse_a=[];sparse_b=[];sparse_pos=[];sparse_vals=[]
    dense_a=[];dense_b=[];dense_data=[]
    fast_coeff=0
    for (h,l),sym in sorted(coeffs.items()):
        if (h,l)==(0,0):
            directly=_direct_time_if_affine(engine,sym)
            base=engine.evaluate_time(sym) if directly is None else directly
            fast_coeff += (directly is not None)
            continue
        sparse=engine._known_impulses(sym,limit=max_sparse_positions)
        if sparse is not None:
            for pos,amp in sorted(sparse.items()):
                if amp:
                    sparse_a.append(h);sparse_b.append(l)
                    sparse_pos.append(pos);sparse_vals.append(amp)
        else:
            dense_a.append(h);dense_b.append(l)
            directly=_direct_time_if_affine(engine,sym)
            dense_data.append(engine.evaluate_time(sym) if directly is None else directly)
            fast_coeff += (directly is not None)
    dense=_freeze(np.stack(dense_data,axis=0) if dense_data else np.empty((0,n)),np.float64)
    return TwoEditPlan(
        n,root,target_a,target_b,max_total_degree,_freeze(base,np.float64),dense,
        _freeze(np.asarray(dense_a),np.int32),_freeze(np.asarray(dense_b),np.int32),
        _freeze(np.asarray(sparse_a),np.int32),_freeze(np.asarray(sparse_b),np.int32),
        _freeze(np.asarray(sparse_pos),np.int64),_freeze(np.asarray(sparse_vals),np.float64),
        tuple(sorted(coeffs)),time.perf_counter()-start,orig,
        engine.reachable_count(root),fast_coeff)
