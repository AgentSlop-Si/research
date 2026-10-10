#!/usr/bin/env python3
"""Reproducible selective FFT leaf-table benchmark; writes results.json.

Run: python benchmark.py --output results.json
Table construction and plan creation are measured outside steady-state timing.
C receives binary uint8 input and returns the full complex128 FFT.
"""
import argparse
import ctypes as ct
import datetime as dt
import json
import math
import os
from pathlib import Path
import platform
import random
import statistics
import subprocess
import time

# Ensure optional backend worker pools stay single threaded before numpy import.
for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
import numpy as np
import scipy
from scipy import fft as spfft

HERE = Path(__file__).resolve().parent
FLAGS = ['-O3','-march=native','-DNDEBUG','-fno-math-errno','-ffp-contract=fast','-std=c11','-Wall','-Wextra','-fPIC','-shared']
METHODS = ['radix2_fused2','codelet4','codelet8','codelet16','lookup4','lookup8','lookup16']
LEAF = dict(codelet4=4, codelet8=8, codelet16=16, lookup4=4, lookup8=8, lookup16=16)


def build_load():
    cmd = ['gcc',*FLAGS,str(HERE/'leaf_fft.c'),'-lm','-o',str(HERE/'libleaf_fft.so')]
    subprocess.run(cmd, check=True)
    lib=ct.CDLL(str(HERE/'libleaf_fft.so'))
    P=ct.c_void_p; U=ct.c_uint
    lib.fft_plan_create.argtypes=[ct.c_size_t]; lib.fft_plan_create.restype=P
    lib.fft_plan_destroy.argtypes=[P]
    lib.fft_table_create.argtypes=[U]; lib.fft_table_create.restype=P
    lib.fft_table_destroy.argtypes=[P]
    lib.fft_execute.argtypes=[ct.c_int,P,P,P,P]
    lib.fft_bench.argtypes=[ct.c_int,P,P,U,P,P,U];lib.fft_bench.restype=ct.c_double
    return lib, cmd


def ptr(a): return ct.c_void_p(a.ctypes.data)
def stats(a):
    a=np.asarray(a,dtype=float)
    med=float(np.median(a))
    return {'median_us':med*1e6,'p10_us':float(np.percentile(a,10))*1e6,
            'p90_us':float(np.percentile(a,90))*1e6,
            'relative_mad':float(np.median(np.abs(a-med))/med),
            'samples_us':(a*1e6).tolist()}


def get_metadata(cmd, affinity, selected):
    cpu={}
    try:
        for line in Path('/proc/cpuinfo').read_text().split('\n\n')[0].splitlines():
            if ':' in line:
                k,v=line.split(':',1);cpu[k.strip()]=v.strip()
    except OSError: pass
    return dict(utc_timestamp=dt.datetime.now(dt.timezone.utc).isoformat(),
                platform=platform.platform(),cpu_model=cpu.get('model name'),cpu_flags=cpu.get('flags'),
                cpu_mhz_snapshot=cpu.get('cpu MHz'),available_affinity=affinity,pinned_cpu=selected,
                gcc_version=subprocess.check_output(['gcc','--version'],text=True).splitlines()[0],
                compile_command=cmd,numpy_version=np.__version__,scipy_version=scipy.__version__,
                precision='complex128 output / double arithmetic',input_dtype='uint8, values 0 or 1',
                threads=1,virtualized='hypervisor' in cpu.get('flags',''))


def correctness(lib,tables,sizes):
    worst={m:0. for m in METHODS};cases=0
    # Complete 4-, 8- and 16-input table validation, not just sampled patterns.
    table_errors={}
    for leaf,t in tables.items():
        rows=1<<leaf;bits=int(math.log2(leaf))
        rev=np.array([int(f'{i:0{bits}b}'[::-1],2) for i in range(leaf)])
        v=((np.arange(rows,dtype=np.uint32)[:,None]>>np.arange(leaf))&1).astype(np.float64)
        expected=np.fft.fft(v[:,rev],axis=1)
        actual=np.ctypeslib.as_array(ct.cast(t,ct.POINTER(ct.c_double)),shape=(rows*leaf*2,)).view(np.complex128).reshape(rows,leaf)
        err=float(np.max(np.abs(expected-actual)))
        np.testing.assert_allclose(actual,expected,atol=1e-12,rtol=1e-12)
        table_errors[str(leaf)]=err
    for n in sorted(set([16,32,64,128,512,*sizes])):
        p=lib.fft_plan_create(n); assert p
        y=np.empty(n,dtype=np.complex128)
        inputs=[np.zeros(n,dtype=np.uint8),np.ones(n,dtype=np.uint8),np.arange(n,dtype=np.uint8)%2]
        impulse=np.zeros(n,dtype=np.uint8);impulse[n//3]=1;inputs.append(impulse)
        for seed in [7,19,123,2026,58127]:
            inputs.append(np.random.default_rng(seed).integers(0,2,n,dtype=np.uint8))
        for x in inputs:
            ref=np.fft.fft(x)
            for method,m in enumerate(METHODS):
                t=tables.get(LEAF.get(m,0)) if m.startswith('lookup') else None
                lib.fft_execute(method,p,ptr(x),ptr(y),t)
                err=float(np.max(np.abs(y-ref)));worst[m]=max(worst[m],err)
                np.testing.assert_allclose(y,ref,atol=2e-9,rtol=2e-11)
                cases+=1
        lib.fft_plan_destroy(p)
    return dict(passed=True,full_fft_cases=cases,random_seeds=[7,19,123,2026,58127],
                max_absolute_error=worst,exhaustive_leaf_table_max_absolute_error=table_errors,
                asserted_atol=2e-9,asserted_rtol=2e-11)


def measure_tables(lib):
    tables={};summary={}
    for leaf in (4,8,16):
        times=[]
        # 11 independent allocate-and-populate calls. OS/cache state is uncontrolled;
        # these are construction costs, not claims of first-page-fault cold latency.
        for _ in range(11):
            start=time.perf_counter();t=lib.fft_table_create(leaf);elapsed=time.perf_counter()-start
            assert t;times.append(elapsed);lib.fft_table_destroy(t)
        tables[leaf]=lib.fft_table_create(leaf)
        summary[str(leaf)]={'entries':1<<leaf,'bytes':(1<<leaf)*leaf*16,
                            'construction':stats(times),'first_construction_us':times[0]*1e6}
    return tables,summary


def bench_size(lib,tables,n,rounds,target,pool_count,seed):
    rng=np.random.default_rng(seed)
    pool=rng.integers(0,2,(pool_count,n),dtype=np.uint8)
    output=np.empty(n,dtype=np.complex128)
    start=time.perf_counter();p=lib.fft_plan_create(n);plan_s=time.perf_counter()-start;assert p
    records={m:[] for m in METHODS}; repeats={}
    for method,m in enumerate(METHODS):
        t=tables.get(LEAF.get(m,0)) if m.startswith('lookup') else None
        estimate=lib.fft_bench(method,p,ptr(pool),pool_count,ptr(output),t,pool_count*2)
        repeats[m]=max(pool_count,int(math.ceil(target/estimate/pool_count)*pool_count))
    order_rng=random.Random(seed)
    for _ in range(rounds):
        order=list(range(len(METHODS)));order_rng.shuffle(order)
        for method in order:
            m=METHODS[method]; t=tables.get(LEAF.get(m,0)) if m.startswith('lookup') else None
            records[m].append(lib.fft_bench(method,p,ptr(pool),pool_count,ptr(output),t,repeats[m]))
    lib.fft_plan_destroy(p)
    summary={m:dict(stats(v),transforms_per_sample=repeats[m]) for m,v in records.items()}
    base=summary['radix2_fused2']['median_us']
    bestcode=min((summary[m]['median_us'],m) for m in METHODS if not m.startswith('lookup'))
    for m,s in summary.items():
        s['speedup_vs_radix2']=base/s['median_us']
        s['speedup_vs_best_arithmetic']=bestcode[0]/s['median_us']
    return dict(n=n,input_seed=seed,input_pool_count=pool_count,plan_create_us=plan_s*1e6,
                best_arithmetic=bestcode[1],methods=summary),pool


def bench_python_baselines(pool,rounds,target,seed):
    count,n=pool.shape
    floats=pool.astype(np.float64)
    methods={
      'scipy_fft_uint8': lambda j: spfft.fft(pool[j],workers=1),
      'scipy_fft_float64': lambda j: spfft.fft(floats[j],workers=1),
      'numpy_fft_uint8': lambda j: np.fft.fft(pool[j]),
      'scipy_rfft_float64_half_spectrum': lambda j: spfft.rfft(floats[j],workers=1),
    }
    repeats={};records={m:[] for m in methods}
    for m,f in methods.items():
        start=time.perf_counter()
        for r in range(count): f(r)
        estimate=(time.perf_counter()-start)/count
        repeats[m]=max(count,int(math.ceil(target/estimate/count)*count))
    order_rng=random.Random(seed)
    for _ in range(rounds):
        order=list(methods);order_rng.shuffle(order)
        for m in order:
            start=time.perf_counter()
            for r in range(repeats[m]): methods[m](r%count)
            records[m].append((time.perf_counter()-start)/repeats[m])
    return {m:dict(stats(v),transforms_per_sample=repeats[m]) for m,v in records.items()}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--sizes',nargs='+',type=int,default=[4096,16384,65536,262144,1048576])
    ap.add_argument('--rounds',type=int,default=11)
    ap.add_argument('--target-ms',type=float,default=40)
    ap.add_argument('--pool-count',type=int,default=16)
    ap.add_argument('--output',type=Path,default=HERE/'results.json')
    ap.add_argument('--quick',action='store_true',help='Use three samples, 10 ms target, and only N=4096/16384 for a smoke test')
    ap.add_argument('--skip-practical',action='store_true',help='Skip Python library baselines, e.g. for a focused C rerun')
    args=ap.parse_args()
    if args.quick:
        args.sizes=[4096,16384];args.rounds=3;args.target_ms=10
    affinity=sorted(os.sched_getaffinity(0));selected=None
    try: os.sched_setaffinity(0,{affinity[0]});selected=affinity[0]
    except OSError: pass
    lib,cmd=build_load();tables,table_summary=measure_tables(lib)
    result={'metadata':get_metadata(cmd,affinity,selected),'methodology':{
        'description':'Single-threaded full complex FFT of binary uint8 inputs, preallocated C output and plans, identical merge engine.',
        'timed_operations':'Input bit-reversal gathers, key packing, complete row copies or arithmetic leaves, every upper merge stage; C calls inside a timed C batch.',
        'excluded_operations':'Plan/table creation, random input generation, validation, C output allocation.',
        'baseline':'Iterative radix-2 with fused bit reversal and length-2 arithmetic, specialized length-4 stage; no recursion or hashes.',
        'codelet_controls':'Fused bit reversal and real-input arithmetic length-4/8/16 leaves with the same upper merges.',
        'key_order':'Key bit j is input[global_bit_reverse(leaf_start+j)]. Table spectra are computed from this bit-reversed leaf layout.',
        'input_pool':'16 distinct seeded random arrays cycled per sample by default; each sample is a whole number of cycles.',
        'warmup':'At least two input-pool cycles per method before samples. No artificial cache flushing.',
        'samples':'Randomized method order every round; median of batch per-transform averages.',
        'python_baselines':'SciPy and NumPy end-to-end calls include output allocation/Python dispatch; not allocation-matched to C. float64 conversion is outside timing for float64 variants.',
        'half_spectrum_note':'rfft returns N/2+1 values, so its performance is context only, not an equivalent full-output comparison.',
        'table_build_note':'Allocation and populate measured separately; first and 11-call median shown. No claim of a controlled cache-cold first use.',
        'benchmark_rounds':args.rounds,'target_sample_ms':args.target_ms},'tables':table_summary}
    result['correctness']=correctness(lib,tables,args.sizes)
    print('Correctness:',json.dumps(result['correctness']),flush=True)
    result['sizes']=[]
    for n in args.sizes:
        rec,pool=bench_size(lib,tables,n,args.rounds,args.target_ms/1000,args.pool_count,18000+n)
        rec['practical_baselines']=({} if args.skip_practical else bench_python_baselines(pool,args.rounds,args.target_ms/1000,38000+n))
        # Construction amortization only when lookup beats best arithmetic leaf.
        for leaf in (4,8,16):
            delta=rec['methods'][rec['best_arithmetic']]['median_us']-rec['methods'][f'lookup{leaf}']['median_us']
            rec['methods'][f'lookup{leaf}']['table_build_break_even_transforms_vs_best_arithmetic']=(table_summary[str(leaf)]['construction']['median_us']/delta if delta>0 else None)
        result['sizes'].append(rec)
        args.output.write_text(json.dumps(result,indent=2)+'\n')
        print(f'N={n}: '+', '.join(f'{m}={s["median_us"]:.2f} us' for m,s in rec['methods'].items()),flush=True)
        print('  practical: '+', '.join(f'{m}={s["median_us"]:.2f} us' for m,s in rec['practical_baselines'].items()),flush=True)
    for t in tables.values():lib.fft_table_destroy(t)
    print('Saved',args.output,flush=True)

if __name__=='__main__':main()
