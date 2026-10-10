"""Fair identical-scope tests of Phase 9 generated native code.

Modes: (1) SciPy fresh modified input + prepared fixed FFTs;
(2) Phase 8 prepared jets Python+NumPy;
(3) generated JIT from Phase 8 jets;
(4) hand-specialized native kernels.

All full-output modes calculate N samples on every event and include
setup in cold totals. Warm medians exclude it explicitly. For partial
benchmarks all output only the same six coefficients.
"""
from __future__ import annotations
import gc
import json
import time
from pathlib import Path
import numpy as np
from scipy import fft
from numba import njit
from algebra_fft import AlgebraFFT
from compiled_kernels import compile_prepared


@njit(nogil=True)
def _manual1(base,b,t,d):
    n=base.shape[0]
    out=np.empty_like(base)
    for q in range(n):
        x=q-t
        if x<0:x+=n
        out[q]=base[q]+d*b[x]
    return out

@njit(nogil=True)
def _manual2(base,a,t,d):
    n=base.shape[0]
    out=np.empty_like(base)
    sh=(t%n)
    for q in range(n):
        idx=q-sh
        if idx<0:idx+=n
        out[q]=base[q]+(2*d)*a[idx]
    out[(2*t)%n]+=d*d
    return out

@njit(nogil=True)
def _manual3(base,k1,a,t,d):
    n=base.shape[0]
    out=np.empty_like(base)
    sh2=(2*t)%n
    for q in range(n):
        i=q-t
        if i<0:i+=n
        j=q-sh2
        if j<0:j+=n
        out[q]=base[q]+d*k1[i]+(3*d*d)*a[j]
    out[(3*t)%n]+=d*d*d
    return out


def setup(n,degree):
    rng=np.random.default_rng(20261009+n+17*degree)
    arrays=[rng.standard_normal(n).astype(np.float64)/np.sqrt(n) for _ in range(4)]
    changes=[(int(t),float(d)) for t,d in zip(rng.integers(0,n,size=64),rng.uniform(-.03,.03,size=64))]
    return arrays,changes


def sink(out):
    # Outputs are materialized; consume several samples so timing loop isn't dead code.
    return float(out[0]+out[len(out)//2]+out[-1])


def create_native(degree,arrays):
    a,b,c,d=arrays
    fa,fb,fc,fd=[fft.rfft(x) for x in arrays]
    if degree==1:
        base=fft.irfft(fa*fb+fc*fd,n=len(a))
        f=lambda t,delta:_manual1(base,b,t,delta)
    elif degree==2:
        base=fft.irfft(fa*fa+fb*fc,n=len(a))
        f=lambda t,delta:_manual2(base,a,t,delta)
    else:
        base=fft.irfft(fa**3+2*fa*fb+fc*fd,n=len(a))
        k1=fft.irfft(3*fa*fa+2*fb,n=len(a))
        f=lambda t,delta:_manual3(base,k1,a,t,delta)
    return f


def create_phase8(degree,arrays):
    n=len(arrays[0]);e=AlgebraFFT(n)
    a,b,c,d=[e.signal(arr) for arr in arrays]
    if degree==1:r=e.add(e.mul(a,b),e.mul(c,d))
    elif degree==2:r=e.add(e.mul(a,a),e.mul(b,c))
    else:r=e.add(e.mul(a,a,a),e.scale(e.mul(a,b),2),e.mul(c,d))
    prep=e.prepare(r,a,max_degree=degree)
    return e,prep


def native_fresh_kernel(degree,arrays):
    n=len(arrays[0]);a,b,c,d=arrays
    fa,fb,fc,fd=[fft.rfft(x) for x in arrays]
    other=fc*fd if degree != 2 else fb*fc
    def fn(t,delta):
        modified=a.copy()
        modified[t]+=delta
        w=fft.rfft(modified)
        if degree==1:freq=w*fb+other
        elif degree==2:freq=w*w+other
        else:freq=w**3+2*w*fb+other
        return fft.irfft(freq,n=n)
    return fn


def bench_one(n,degree,versions=48,repeats=4):
    arrays,changes=setup(n,degree)
    changes=changes[:versions]
    cases={}
    constructors={
        'scipy_prepared':lambda:native_fresh_kernel(degree,arrays),
        'phase8_numpy':lambda:create_phase8(degree,arrays)[1].single,
        'phase9_generated':lambda:compile_prepared(create_phase8(degree,arrays)[1],backend='numba').single,
        'hand_native':lambda:create_native(degree,arrays),
    }
    # Startup measured separately; includes seed FFTs, jet preparation and JIT.
    for label,cons in constructors.items():
        gc.collect()
        t0=time.perf_counter()
        fn=cons()
        first=fn(*changes[0])   # first call charges native compilation, where needed
        setup_ms=1000*(time.perf_counter()-t0)
        checks=[sink(first)]
        times=[]
        for it in range(repeats):
            t1=time.perf_counter()
            checksum=0.0
            for t,delta in changes:
                out=fn(t,delta)
                checksum+=sink(out)
            times.append(1000*(time.perf_counter()-t1))
            checks.append(checksum)
        cases[label]={'setup_ms':round(setup_ms,4),'stream_median_ms':round(float(np.median(times)),4),
                      'total_if_one_stream_ms':round(setup_ms+float(np.median(times)),4),
                      'checksum':float(checks[-1])}
    # Full-array reference checks before accepting a performance comparison.
    verify_cases=changes[:3]
    reference_fn=constructors['scipy_prepared']()
    reference_arrays=[reference_fn(*e) for e in verify_cases]
    verification={}
    for label,cons in constructors.items():
        candidate=cons()
        residuals=[float(np.max(np.abs(candidate(*e)-wanted))) for e,wanted in zip(verify_cases,reference_arrays)]
        verification[label]=max(residuals)
        if not np.all([np.allclose(candidate(*e),wanted,rtol=5e-9,atol=5e-9) for e,wanted in zip(verify_cases,reference_arrays)]):
            raise AssertionError((label,n,degree,residuals))
    target=cases['scipy_prepared']['checksum']
    for key,v in cases.items():
        if not np.isclose(v['checksum'],target,rtol=1e-8,atol=1e-8):
            raise AssertionError((n,degree,key,v['checksum'],target))
        v['warm_speedup_vs_scipy']=round(cases['scipy_prepared']['stream_median_ms']/v['stream_median_ms'],3)
        v['warm_vs_hand']=round(cases['hand_native']['stream_median_ms']/v['stream_median_ms'],3)
    return {'n':n,'degree':degree,'versions':versions,'methods':cases,'verification_max_abs_error':verification}


def bench_partial(n,degree=3,versions=48,repeats=5):
    arrays,changes=setup(n,degree)
    changes=changes[:versions]
    q=np.array([0,1,7,n//7,n//2,n-1],dtype=np.int64)
    eng,prepared=create_phase8(degree,arrays)
    compiled=compile_prepared(prepared,backend='numba')
    manual=prepared.kernels
    def custom(t,d):
        # hand-specialized 6-bin expression, no full convolution array
        return manual[0][q]+d*manual[1][(q-t)%n]+3*d*d*arrays[0][(q-2*t)%n]+d**3*(q==(3*t)%n)
    functions={'phase8':lambda t,d:prepared.single(t,d,indices=q),
               'phase9':lambda t,d:compiled.single(t,d,indices=q),
               'hand_six_bins':custom}
    results={}
    for name,fn in functions.items():
        samples=[];check=0.
        for z in range(repeats):
            start=time.perf_counter()
            check=0.
            for t,d in changes:
                out=fn(t,d)
                check+=float(np.sum(out))
            samples.append(1000*(time.perf_counter()-start))
        results[name]={'warm_median_ms':round(float(np.median(samples)),4),'checksum':float(check)}
    for v in results.values():
        assert np.isclose(v['checksum'],results['hand_six_bins']['checksum'],atol=1e-8)
    return {'n':n,'degree':3,'output_bins':q.tolist(),'setup_excluded':True,'methods':results}


def main():
    rows=[]
    for n in (4096,65536,262144):
        for d in (1,2,3):
            v=bench_one(n,d)
            rows.append(v)
            print(f"{n=} {d=}:",[(a,v['methods'][a]['stream_median_ms'],v['methods'][a]['total_if_one_stream_ms']) for a in v['methods']],flush=True)
    partial=[bench_partial(n) for n in (4096,65536,262144)]
    for r in partial:
        print('six bins',r['n'],r['methods'],flush=True)
    report={'context':{'backend':'Python NumPy SciPy Numba; real circular convolution; initial setup charged in cold totals',
                       'scope':'48 related single-edit versions, full N-length output each version',
                       'cold_rule':'JIT and all initial FFT/jet preparation included; warm medians reported separately',
                       'repeats':4},'full':rows,'partial':partial}
    path=Path(__file__).parent/'benchmark_results.json'
    path.write_text(json.dumps(report,indent=2)+'\n')
    print('wrote',path)

if __name__=='__main__':main()
