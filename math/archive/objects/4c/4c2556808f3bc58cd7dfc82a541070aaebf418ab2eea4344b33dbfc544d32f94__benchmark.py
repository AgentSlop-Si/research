"""Native cold-call timings, exact-zero/approximate checks, and NumPy comparison."""
import ctypes as ct
import hashlib
import json
import os
import platform
from pathlib import Path
import random
import subprocess
import time
import numpy as np

ROOT=Path(__file__).resolve().parent
FIELDS=('butterflies visited_nodes threshold_tests pruned_nodes pruned_outputs '
        'computed_outputs norm_value_volume zero_value_tests root_pairs '
        'full_output_writes max_stack').split()
class Stats(ct.Structure):_fields_=[(x,ct.c_uint64) for x in FIELDS]


def build():
    command=['g++','-O3','-std=c++17','-march=native','-fPIC','-shared',
             str(ROOT/'native_fft.cpp'),'-o',str(ROOT/'native_fft.so')]
    subprocess.run(command,check=True,capture_output=True,text=True)
    return command


def load():
    lib=ct.CDLL(str(ROOT/'native_fft.so'))
    pointer=ct.POINTER(ct.c_double)
    lib.native_fft.argtypes=[pointer,pointer,ct.c_size_t,ct.c_int,ct.c_double,ct.POINTER(Stats)]
    lib.native_fft.restype=ct.c_int
    lib.consume.argtypes=[pointer,ct.c_size_t];lib.consume.restype=ct.c_double
    def transform(x,algorithm,epsilon=0.,instrument=False):
        out=np.empty_like(x);stats=Stats() if instrument else None
        status=lib.native_fft(x.ctypes.data_as(pointer),out.ctypes.data_as(pointer),len(x),
                              algorithm,epsilon,ct.byref(stats) if stats is not None else None)
        if status:raise ValueError(f'native FFT failed with status {status}')
        return out,{name:int(getattr(stats,name)) for name in FIELDS} if stats is not None else None
    def consume(out):return float(lib.consume(out.ctypes.data_as(pointer),len(out)))
    return transform,consume


def families(n,rng):
    j=np.arange(n)
    result={
        'gaussian':rng.normal(size=n)+1j*rng.normal(size=n),
        'pure_tone':np.exp(2j*np.pi*17*j/n),
        'constant_exact':np.ones(n,dtype=complex),
        'impulse_diffuse_spectrum':np.eye(1,n,dtype=complex).ravel(),
    }
    for name,support in [('fifteen_tones',15),('threshold_64_tones',64)]:
        spectrum=np.zeros(n,dtype=complex)
        indices=rng.choice(n,support,replace=False)
        spectrum[indices]=np.exp(1j*rng.uniform(-np.pi,np.pi,support))
        result[name]=np.fft.ifft(spectrum,norm='ortho')
    spectrum=np.exp(1j*rng.uniform(-np.pi,np.pi,n))/np.sqrt(np.arange(1,n+1))
    result['heavy_tail_spectrum']=np.fft.ifft(spectrum,norm='ortho')
    return result


def error_ratio(out,reference,x):
    scale=max(float(np.max(np.abs(x.real))),float(np.max(np.abs(x.imag))))
    if scale==0:return float(np.max(np.abs(out)))
    scaled=x.real/scale+1j*(x.imag/scale)
    diff=(out.real-reference.real)/scale+1j*((out.imag-reference.imag)/scale)
    return float(np.max(np.abs(diff))/np.linalg.norm(scaled))


def usefulness(out,reference,x):
    scale=max(float(np.max(np.abs(x.real))),float(np.max(np.abs(x.imag))))
    if scale==0:return {'relative_l2_error':0.,'all_zero_output':True,'retained_energy_fraction':1.}
    scaled=x.real/scale+1j*(x.imag/scale)
    diff=(out.real-reference.real)/scale+1j*((out.imag-reference.imag)/scale)
    out_scaled=out.real/scale+1j*(out.imag/scale)
    denominator=float(np.vdot(scaled,scaled).real)
    return {'relative_l2_error':float(np.linalg.norm(diff)/np.sqrt(denominator)),
            'all_zero_output':bool(np.all(out==0)),
            'retained_energy_fraction':float(np.vdot(out_scaled,out_scaled).real/denominator)}


def timing_summary(values):
    arr=np.asarray(values)
    return {'median_seconds':float(np.median(arr)),
            'q25_seconds':float(np.quantile(arr,.25)),
            'q75_seconds':float(np.quantile(arr,.75)),
            'minimum_seconds':float(np.min(arr)),
            'raw_seconds':list(map(float,arr))}


def main():
    command=build();transform,consume=load()
    rng=np.random.default_rng(20261011);schedule_rng=random.Random(9382)
    rows=[];checks=[];consumed=[]
    repeats=int(os.getenv('FFT_BENCH_REPEATS','9'))
    sizes=tuple(map(int,os.getenv('FFT_BENCH_SIZES','4096,65536,262144').split(',')))
    for n in sizes:
        for family,x in families(n,rng).items():
            reference=np.fft.fft(x,norm='ortho')
            methods={'native_dit':(0,0.),'native_dif':(1,0.),
                     'zero_pruned':(2,0.),'epsilon_0.125':(2,.125),
                     'epsilon_0.25':(2,.25),'epsilon_0.5':(2,.5),'numpy':None}
            outputs={};stats={};timings={name:[] for name in methods}
            for name,spec in methods.items():
                out,stat=(reference,None) if spec is None else transform(x,*spec,instrument=True)
                outputs[name]=out;stats[name]=stat
                err=error_ratio(out,reference,x)
                allowed=spec[1] if spec is not None else 0.
                assert err<=allowed+2e-12,(n,family,name,err,allowed)
            # One untimed warmup of code/caches; each measured call still rebuilds
            # roots/workspace. This is cold algorithmic setup, not cold hardware.
            for name,spec in methods.items():
                out=np.fft.fft(x,norm='ortho') if spec is None else transform(x,*spec)[0]
                consumed.append(consume(out))
            for _ in range(repeats):
                order=list(methods);schedule_rng.shuffle(order)
                for name in order:
                    spec=methods[name]
                    started=time.perf_counter_ns()
                    out=np.fft.fft(x,norm='ortho') if spec is None else transform(x,*spec)[0]
                    checksum=consume(out)
                    elapsed=(time.perf_counter_ns()-started)*1e-9
                    consumed.append(checksum);timings[name].append(elapsed)
            fast_baseline=min(np.median(timings['native_dit']),np.median(timings['native_dif']))
            for name,spec in methods.items():
                row={'n':n,'family':family,'method':name,
                     **timing_summary(timings[name]),
                     'ratio_to_faster_native_baseline':float(np.median(timings[name])/fast_baseline),
                     'ratio_to_numpy':float(np.median(timings[name])/np.median(timings['numpy'])),
                     'max_error_over_input_l2':error_ratio(outputs[name],reference,x),
                     **usefulness(outputs[name],reference,x),
                     'stats':stats[name]}
                rows.append(row)
            print(f'completed n={n} {family}',flush=True)
    # Dynamic range and cancellation controls, not included in ordinary timing medians.
    for n in (1,2,8,1024):
        for scale in (0.,1e-200,1.,1e200):
            x=(rng.normal(size=n)+1j*rng.normal(size=n))*scale
            reference=np.fft.fft(x,norm='ortho')
            for eps in (0.,.125,.25,.5):
                out,stat=transform(x,2,eps,instrument=True)
                err=error_ratio(out,reference,x)
                assert err<=eps+3e-12,(n,scale,eps,err)
                assert stat['computed_outputs']+stat['pruned_outputs']==n
                checks.append({'n':n,'scale':scale,'epsilon':eps,'error_ratio':err})
    # A tiny nonzero branch must not be discarded by squared-norm underflow
    # in zero-only mode. eps=0 uses component comparisons directly.
    x=np.zeros(8,dtype=complex);x[0]=x[4]=1.;x[1]=1e-200;x[5]=-1e-200
    out,stat=transform(x,2,0.,instrument=True)
    reference=np.fft.fft(x,norm='ortho')
    assert np.all(out[1::2]!=0),out
    assert error_ratio(out,reference,x)<1e-14
    special={'zero_mode_component_tests':True,'underflow_prone_odd_outputs_preserved':4,
             'near_underflow_error':error_ratio(out,reference,x)}
    report={'status':'PASS','compiler_command':command,
            'compiler':subprocess.run(['g++','--version'],capture_output=True,text=True).stdout.splitlines()[0],
            'platform':platform.platform(),'python':platform.python_version(),'numpy_version':np.__version__,
            'hardware':subprocess.run(['lscpu'],capture_output=True,text=True).stdout,
            'affinity_cpu_count':len(os.sched_getaffinity(0)) if hasattr(os,'sched_getaffinity') else None,
            'thread_environment':{key:os.environ.get(key) for key in (
                'OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')},
            'repeats':repeats,'sizes':sizes,'methodology':[
                'Fresh native work/root allocation and root preparation on every measured call.',
                'Native validation, input scaling, threshold tests, full output and output checksum included.',
                'Code warmed once; repeated identical given inputs; no prepared FFT plans retained.',
                'Randomized method ordering; medians, quartiles and all raw samples retained.',
                'Instrumentation disabled for timings and collected in separate executions.',
                'Native baseline is faster median of iterative DIT and DIF with identical cold setup.',
                'NumPy comparison is its ordinary FFT plus identical output checksum; implementation/setup differ.',
                'Ideal-arithmetic threshold theorem is not a certified floating-point error bound.'
            ],'results':rows,'dynamic_range_checks':checks,'negative_controls':special,
            'checksum_calls':len(consumed),'checksum_digest':hashlib.sha256(np.asarray(consumed).tobytes()).hexdigest()}
    (ROOT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    subset=[r for r in rows if r['method'].startswith('epsilon')]
    print(json.dumps({'cases':len(subset),'wins_native':sum(r['ratio_to_faster_native_baseline']<1 for r in subset),
        'ratio_native_min':min(r['ratio_to_faster_native_baseline'] for r in subset),
        'ratio_native_max':max(r['ratio_to_faster_native_baseline'] for r in subset),
        'wins_numpy':sum(r['ratio_to_numpy']<1 for r in subset)},indent=2))


if __name__=='__main__':main()
