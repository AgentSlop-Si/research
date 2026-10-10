"""Reproducible same-output benchmark of Phase10 against SciPy and hand C++.

Cold totals: original seed FFTs + bivariate preparation + library loading +
all requested outputs, vs fixed-kernel preparation + fresh 2x FFT + inverse.
Offline g++ build time is printed separately by build_native.py.
All methods produce the *entire* length-N convolution output.
"""
from pathlib import Path
import ctypes
import json
import gc
import time
import statistics
import numpy as np
from scipy import fft
from algebra_fft import AlgebraFFT
from two_edit_engine import prepare_two, _native_path


def sample_case(n,seed=888,versions=48):
    rng=np.random.default_rng(seed+n)
    sigs=[rng.normal(size=n)/np.sqrt(n) for _ in range(4)]
    changes=[(int(rng.integers(n)),float(rng.normal(scale=.04)),
              int(rng.integers(n)),float(rng.normal(scale=.04))) for _ in range(versions)]
    return sigs,changes


def hand_compiled(libpath,plan):
    lib=ctypes.CDLL(libpath)
    fn=lib.fft10_hand_example
    P=ctypes.c_void_p
    fn.argtypes=[ctypes.c_int64,P,P,P,P,P,ctypes.c_int64,ctypes.c_double,
                 ctypes.c_int64,ctypes.c_double,P]
    fn.restype=ctypes.c_int
    degrees=list(zip(map(int,plan.dense_a),map(int,plan.dense_b)))
    expected=[(0,1),(1,0),(1,1),(2,0)]
    if degrees!=expected:
        raise AssertionError(f'unexpected correction ordering: {degrees}')
    def run(pa,alpha,pb,beta):
        out=np.empty(plan.n)
        ptr=lambda x:ctypes.c_void_p(x.ctypes.data)
        code=fn(plan.n,ptr(plan.base),*(ptr(plan.dense[i]) for i in range(4)),
                pa,alpha,pb,beta,ptr(out))
        if code:raise RuntimeError(code)
        return out
    return run


def benchmark_one(n,versions=48,repeats=4):
    sigs,changes=sample_case(n,versions=versions)
    a,b,c,d=sigs
    timings={key:[] for key in ['scipy_fresh','numpy_prepared','aot_native','aot_shape','hand_native']}
    setup_times=[]
    checks=[]
    mem=0
    for repetition in range(repeats):
        gc.collect()
        # Each repetition builds fresh engine, avoiding time-limited reused bases.
        setup_start=time.perf_counter()
        eng=AlgebraFFT(n)
        A,B,C,D=[eng.signal(v) for v in sigs]
        root=eng.add(eng.mul(A,A,B),eng.mul(A,B),eng.mul(B,B),eng.mul(C,D))
        plan=prepare_two(eng,root,A,B,max_total_degree=5)
        manual=hand_compiled(_native_path(),plan)
        native_first=plan.update(*changes[0],backend='native') # load once per benchmark iteration
        shape_first=plan.update(*changes[0],backend='aot_shape')
        setup_times.append(time.perf_counter()-setup_start)
        mem=plan.memory_bytes
        # Check full-output correctness on several different versions.
        fixed=fft.rfft(c)*fft.rfft(d)
        for pa,alpha,pb,beta in (changes[0],changes[-1]):
            ax=a.copy();bx=b.copy();ax[pa]+=alpha;bx[pb]+=beta
            fa=fft.rfft(ax);fb=fft.rfft(bx)
            ref=fft.irfft(fa*fa*fb+fa*fb+fb*fb+fixed,n=n)
            for backend in ['numpy','native','aot_shape']:
                ans=plan.update(pa,alpha,pb,beta,backend=backend)
                checks.append(float(np.max(np.abs(ans-ref))))
            checks.append(float(np.max(np.abs(manual(pa,alpha,pb,beta)-ref))))
        def reference_batch():
            # Prepared C*D spectrum reused by fresh-transform baseline.
            fixed=fft.rfft(c)*fft.rfft(d)
            for pa,alpha,pb,beta in changes:
                ax=a.copy();bx=b.copy()
                ax[pa]+=alpha;bx[pb]+=beta
                fa=fft.rfft(ax);fb=fft.rfft(bx)
                out=fft.irfft(fa*fa*fb+fa*fb+fb*fb+fixed,n=n)
            return out
        def run(method):
            if method=='scipy_fresh':return reference_batch()
            if method=='numpy_prepared':
                for args in changes:out=plan.update(*args,backend='numpy')
                return out
            if method=='aot_native':
                for args in changes:out=plan.update(*args,backend='native')
                return out
            if method=='aot_shape':
                for args in changes:out=plan.update(*args,backend='aot_shape')
                return out
            for args in changes:out=manual(*args)
            return out
        # Rotate order to mitigate systematic first-run effects.
        order=list(timings)
        order=order[repetition%len(order):]+order[:repetition%len(order)]
        for key in order:
            t=time.perf_counter()
            output=run(key)
            timings[key].append((time.perf_counter()-t)*1000)
            if not np.all(np.isfinite(output)):
                raise ArithmeticError('non-finite output')
    summary={x:round(statistics.median(vals),3) for x,vals in timings.items()}
    setup_median=statistics.median(setup_times)*1000
    summary.update({
        'phase10_setup_ms':round(setup_median,3),
        'aot_cold_total_ms':round(setup_median+statistics.median(timings['aot_native']),3),
        'aot_shape_cold_total_ms':round(setup_median+statistics.median(timings['aot_shape']),3),
        'scipy_cold_total_ms':summary['scipy_fresh'],
        'aot_vs_scipy_warm_ratio':round(summary['scipy_fresh']/summary['aot_native'],3),
        'aot_vs_scipy_cold_ratio':round(summary['scipy_fresh']/(setup_median+statistics.median(timings['aot_native'])),3),
        'aot_vs_hand_ratio':round(summary['hand_native']/summary['aot_native'],3),
        'aot_shape_vs_hand_ratio':round(summary['hand_native']/summary['aot_shape'],3),
        'aot_shape_vs_scipy_cold_ratio':round(summary['scipy_fresh']/(setup_median+statistics.median(timings['aot_shape'])),3),
    })
    return {'n':n,'versions':versions,'timings_ms':summary,
            'prepared_kernel_bytes':mem,'max_numerical_error':max(checks),
            'notes':'SciPy baseline fixed C*D spectrum prepared within each measured stream; AOT path charges all seed FFTs, symbolic prep and library first call. This cold comparison favors the baseline on setup cost.'}

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--sizes',type=int,nargs='+',default=[4096,65536,262144])
    parser.add_argument('--repeats',type=int,default=4)
    parser.add_argument('--versions',type=int,default=48)
    args=parser.parse_args()
    rows=[]
    for n in args.sizes:
        row=benchmark_one(n,versions=args.versions,repeats=args.repeats)
        rows.append(row)
        print('N =',n,'versions =',args.versions,row['timings_ms'],'max_err =',row['max_numerical_error'],flush=True)
    output={'model':'float64 real circular convolution, two known impulse edits',
            'aot_native_is_prior_compiled':True,
            'offline_build_cost_is_separate':True,
            'benchmarks':rows}
    Path('benchmark_results.json').write_text(json.dumps(output,indent=2)+'\n')
