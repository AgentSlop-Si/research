#!/usr/bin/env python3
"""Held-out correctness, safety, API, and performance evaluation of adaptive FFT."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
import argparse
import ctypes as ct
import json
import math
from pathlib import Path
import platform
import random
import time
import numpy as np
from adaptive_fft import BinaryFFTPlan,METHODS,get_plan,binary_fft,clear_plan_cache,cache_info,_library

HERE=Path(__file__).resolve().parent

def stat(values):
    a=np.asarray(values);m=float(np.median(a))
    return {'median_us':m*1e6,'p10_us':float(np.percentile(a,10))*1e6,
            'p90_us':float(np.percentile(a,90))*1e6,
            'relative_mad':float(np.median(abs(a-m))/m),'samples_us':(a*1e6).tolist()}

def expect_error(fn,kind):
    try:fn()
    except kind:return True
    raise AssertionError('Expected '+str(kind))

def ordinary_setup(lib,n):
    lib.fft_plan_create.argtypes=[ct.c_size_t];lib.fft_plan_create.restype=ct.c_void_p
    lib.fft_plan_destroy.argtypes=[ct.c_void_p]
    times=[]
    for _ in range(9):
        start=time.perf_counter();p=lib.fft_plan_create(n);elapsed=time.perf_counter()-start
        assert p;lib.fft_plan_destroy(p);times.append(elapsed)
    return stat(times)

def benchmark_heldout(plan,pool,rounds=13,target_ms=20):
    out=np.empty(plan.n,np.complex128);methods=list(METHODS)+['selected'];samples={m:[] for m in methods};repeats={}
    for m in methods:
        estimate=plan.benchmark(m,pool,out,len(pool)*2)
        repeats[m]=max(len(pool),math.ceil(target_ms/1000/estimate/len(pool))*len(pool))
    rng=random.Random(0x9182817+plan.n)
    for _ in range(rounds):
        rng.shuffle(methods)
        for m in methods:samples[m].append(plan.benchmark(m,pool,out,repeats[m]))
    return {m:dict(stat(s),transforms_per_sample=repeats[m]) for m,s in samples.items()}

def benchmark_public(plan,pool,rounds=7,target_ms=12):
    out=np.empty(plan.n,np.complex128)
    calls={'plan_execute_out':lambda x:plan.execute(x,out=out),
           'plan_execute_allocating':lambda x:plan.execute(x),
           'cached_binary_fft_allocating':lambda x:binary_fft(x)}
    repeats={};samples={m:[] for m in calls}
    for m,f in calls.items():
        start=time.perf_counter()
        for x in pool:f(x)
        est=(time.perf_counter()-start)/len(pool)
        repeats[m]=max(len(pool),math.ceil(target_ms/1000/est/len(pool))*len(pool))
    rng=random.Random(0x238123+plan.n);order=list(calls)
    for _ in range(rounds):
        rng.shuffle(order)
        for m in order:
            start=time.perf_counter()
            for r in range(repeats[m]):calls[m](pool[r%len(pool)])
            samples[m].append((time.perf_counter()-start)/repeats[m])
    return {m:dict(stat(s),transforms_per_sample=repeats[m]) for m,s in samples.items()}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE/'adaptive_results.json');args=ap.parse_args()
    affinity=sorted(os.sched_getaffinity(0));os.sched_setaffinity(0,{affinity[0]})
    lib=_library();results={'methodology':{
        'candidates':METHODS,'lookup_margin':0.08,'paired_lookup_win_requirement':'At least 75% of randomized calibration rounds',
        'calibration':'Nine randomized rounds, target 8 ms per candidate sample, four seeded random inputs; correctness checked before selection.',
        'heldout':'13 independent randomized rounds, target 20 ms per candidate sample, eight new random seeds, fresh input pool; same reused plan.',
        'timed_c_work':'Binary-value validation, input gathers, arithmetic or key packing and full table copies, upper merges. Selected path dispatches once through a C function pointer.',
        'public_api':'Includes dtype/shape/contiguity checks, C binary validation, ctypes overhead, and output allocation where labeled. No input conversion/copy.',
        'overhead':'Ordinary shared plan setup, adaptive plan setup (including tiny tables), and calibration reported separately. Compilation/import excluded.',
        'break_even':'Only positive held-out measured savings yield break-even; otherwise null. Benchmarks are noisy VM observations, not guaranteed crossovers.',
        'cache':'Bounded process-local LRU keyed by N and uint8/bool dtype, capacity eight. Retuning explicit only.'},
        'metadata':{'platform':platform.platform(),'pinned_cpu':affinity[0],'numpy':np.__version__},'sizes':[]}
    for n in [4096,16384,65536,262144,1048576]:
        setup=ordinary_setup(lib,n)
        start=time.perf_counter();plan=get_plan(n,np.uint8);first_plan_ms=(time.perf_counter()-start)*1000
        selected=plan.method
        seeds=[700000+n+j*103 for j in range(8)]
        pool=np.stack([np.random.default_rng(seed).integers(0,2,n,dtype=np.uint8) for seed in seeds])
        errs=[];count=plan.calibration_count
        for x in pool:
            y=plan.execute(x);ref=np.fft.fft(x);errs.append(float(np.max(abs(y-ref))))
            np.testing.assert_allclose(y,ref,atol=2e-9,rtol=2e-11)
        # Verify repeated execution owns independent outputs and never recalibrates.
        saved=plan.execute(pool[0]);saved_copy=saved.copy();other=plan.execute(pool[1])
        assert not np.shares_memory(saved,other);np.testing.assert_array_equal(saved,saved_copy)
        assert get_plan(n,np.uint8) is plan and plan.calibration_count==count
        out=np.empty(n,np.complex128);assert plan.execute(pool[0],out=out) is out
        held=benchmark_heldout(plan,pool);public=benchmark_public(plan,pool)
        assert plan.calibration_count==count and plan.method==selected
        fastest=min(METHODS,key=lambda m:held[m]['median_us'])
        bestarith=min(METHODS[:4],key=lambda m:held[m]['median_us'])
        selected_us=held['selected']['median_us'];extra_setup_us=max(0,plan.setup_seconds*1e6-setup['median_us'])
        tune_us=plan.calibration['elapsed_ms']*1000
        break_even={}
        for m in ['radix2_fused2','codelet8',bestarith]:
            delta=held[m]['median_us']-selected_us
            break_even[m]={'savings_per_fft_us':delta,'calibration_only_calls':math.ceil(tune_us/delta) if delta>0 else None,
                           'calibration_plus_extra_setup_calls':math.ceil((tune_us+extra_setup_us)/delta) if delta>0 else None}
        record={'n':n,'dtype':'uint8','method':selected,'ordinary_plan_setup':setup,
                'adaptive_plan_setup_us':plan.setup_seconds*1e6,'first_get_plan_total_ms':first_plan_ms,
                'calibration':plan.calibration,'heldout_seeds':seeds,'correctness_max_abs_error':max(errs),
                'cached_identity_reused':True,'calibration_count_after_repeated_execution':plan.calibration_count,
                'heldout':held,'public_api':public,'heldout_fastest':fastest,'heldout_best_arithmetic':bestarith,
                'selected_dispatch_excess_us':selected_us-held[selected]['median_us'],
                'regret_vs_fastest_percent':100*(selected_us/held[fastest]['median_us']-1),
                'candidate_choice_regret_percent':100*(held[selected]['median_us']/held[fastest]['median_us']-1),
                'break_even':break_even}
        results['sizes'].append(record);args.output.write_text(json.dumps(results,indent=2)+'\n')
        print(f'N={n} selected={selected} cal={plan.calibration["elapsed_ms"]:.1f}ms; heldout selected={selected_us:.2f}us fastest={fastest} {held[fastest]["median_us"]:.2f}us; regret={record["regret_vs_fastest_percent"]:.1f}%',flush=True)
    # Safety and lifecycle checks on cached 4096 plan.
    p=get_plan(4096,np.uint8);x=np.zeros(4096,np.uint8);out=np.full(4096,123+2j,np.complex128)
    invalid=x.copy();invalid[-1]=2
    expect_error(lambda:p.execute(invalid,out=out),ValueError);assert np.all(out==123+2j)
    expect_error(lambda:p.execute(x.astype(np.float64)),TypeError)
    expect_error(lambda:binary_fft(np.array([0.5]*4096)),TypeError)
    expect_error(lambda:binary_fft(np.array([256]*4096,dtype=np.int64)),TypeError)
    expect_error(lambda:get_plan(4095),ValueError);expect_error(lambda:get_plan(8),ValueError)
    expect_error(lambda:get_plan(4096.0),ValueError);expect_error(lambda:get_plan(True),ValueError)
    expect_error(lambda:p.execute(np.zeros(8192,np.uint8)[::2]),ValueError)
    expect_error(lambda:p.execute(np.zeros((64,64),np.uint8)),ValueError)
    expect_error(lambda:p.execute(x,out=np.empty(4096,np.complex64)),ValueError)
    unaligned=np.ndarray((4096,),dtype=np.complex128,buffer=bytearray(4096*16+1),offset=1)
    expect_error(lambda:p.execute(x,out=unaligned),ValueError)
    readonly=np.empty(4096,np.complex128);readonly.flags.writeable=False
    expect_error(lambda:p.execute(x,out=readonly),ValueError)
    overlapping=np.zeros(4096,np.complex128)
    expect_error(lambda:p.execute(overlapping.view(np.uint8)[:4096],out=overlapping),ValueError)
    # bool plans are cached separately and use no conversion.
    b=get_plan(4096,np.bool_);assert b is get_plan(4096,np.bool_) and b is not p
    bx=np.random.default_rng(5111).integers(0,2,4096,dtype=np.uint8).view(np.bool_)
    np.testing.assert_allclose(b.execute(bx),np.fft.fft(bx),atol=2e-9,rtol=2e-11)
    own=BinaryFFTPlan(16,rounds=3,target_ms=1,pool_count=1);own.close();own.close()
    expect_error(lambda:own.execute(np.zeros(16,np.uint8)),RuntimeError)
    # Explicit retune changes the counter, unlike normal calls.
    before=b.calibration_count;b.retune(rounds=3,target_ms=1,pool_count=1,seed=1234567)
    assert b.calibration_count==before+1
    results['api_checks']={'passed':True,'input_rejection':True,'invalid_input_preserves_out':True,'independent_outputs':True,
                           'out_reuse':True,'overlap_rejection':True,'closed_plan_rejection':True,'double_close_safe':True,
                           'dtype_specific_cache':True,'explicit_retune_only':True,'cache_info':str(cache_info())}
    clear_plan_cache();assert not p.closed # user-held reference remains valid
    np.testing.assert_allclose(p.execute(x),np.zeros(4096,np.complex128))
    p.close();b.close();results['api_checks']['clear_cache_preserves_owned_references']=True
    args.output.write_text(json.dumps(results,indent=2)+'\n');print('All API/safety checks passed. Saved',args.output,flush=True)

if __name__=='__main__':main()
