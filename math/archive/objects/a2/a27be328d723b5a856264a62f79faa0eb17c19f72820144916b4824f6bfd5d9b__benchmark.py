"""Reproducible, honest arithmetic-count and wall-time measurements."""
from __future__ import annotations
from statistics import median
from pathlib import Path
import json
import platform
import random
import time
import numpy as np
from structural_fft import FFTGraph, CompactSplitRadix, SharedLookupTable, fwht_mod, tabulated_fwht_mod


def timed(fn, repeats=5):
    res=[]
    for _ in range(repeats):
        st=time.perf_counter()
        fn()
        res.append(time.perf_counter()-st)
    return median(res)


def run():
    data={
        'metadata': {
            'note': 'Educational Python graphs and tabulation; not a sub-NlogN complex FFT',
            'python': platform.python_version(),
            'numpy':np.__version__,
            'system':platform.platform(),
            'units':'seconds',
        },
        'fft_circuits':[],
        'tabulated_wht':[],
    }
    rng=np.random.default_rng(20261009)
    for n in [16,32,64,128,256,512,1024,2048,4096]:
        x=rng.standard_normal(n) + 1j*rng.standard_normal(n)
        simple=FFTGraph(n,'radix2')
        split=FFTGraph(n,'split_radix')
        compact=CompactSplitRadix(n)
        s0=simple.stats()
        s1=split.stats()
        actual=np.array(split.execute(x))
        assert np.allclose(actual,np.fft.fft(x),rtol=1e-12,atol=1e-10)
        assert np.allclose(compact.execute(x),np.fft.fft(x),rtol=1e-12,atol=1e-10)
        data['fft_circuits'].append({
            'n':n,
            'radix2':s0,
            'split_radix':s1,
            'compact_template':compact.stats(),
            'generic_multiplication_reduction_pct':100*(1-s1['nontrivial_complex_multiplies']/s0['nontrivial_complex_multiplies']),
            'radix2_exec_seconds':timed(lambda:simple.execute(x),3),
            'split_exec_seconds':timed(lambda:split.execute(x),3),
            'compact_exec_seconds':timed(lambda:compact.execute(x),3),
            'numpy_fft_seconds':timed(lambda:np.fft.fft(x),9),
            'max_split_vs_numpy_abs_error':float(np.max(np.abs(actual-np.fft.fft(x)))),
        })
    p=3
    cache=SharedLookupTable(p)
    cache.ensure(8)
    cache_info=cache.stats()
    data['lookup_precomputation']=cache_info
    r=random.Random(20261009)
    for n in (256,1024,4096,16384):
        x=[r.randrange(p) for _ in range(n)]
        direct=fwht_mod(x,p)
        for b in [2,4,8]:
            y,info=tabulated_fwht_mod(x,p,b,cache)
            assert direct==y, f'mismatch N={n}, block={b}'
            data['tabulated_wht'].append({
                **info,
                'python_baseline_seconds':timed(lambda:fwht_mod(x,p),4),
                'python_lookup_seconds':timed(lambda:tabulated_fwht_mod(x,p,b,cache),4),
                'precomputation_amortized':True,
            })
    path=Path(__file__).with_name('benchmark_results.json')
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print(f'Results saved: {path}')
    print('Complex FFT (all inputs):')
    print(' N   Radix-2 mul   Split mul reduction  expanded (ms) compact (ms) NumPy (ms)')
    for row in data['fft_circuits']:
        a=row['radix2']['nontrivial_complex_multiplies']
        b=row['split_radix']['nontrivial_complex_multiplies']
        print(f"{row['n']:>4} {a:>12} {b:>11} {row['generic_multiplication_reduction_pct']:>8.1f}% "
              f"{row['split_exec_seconds']*1000:>14.3f} {row['compact_exec_seconds']*1000:>12.3f} "
              f"{row['numpy_fft_seconds']*1000:>10.3f}")
    print('Lookup compiler:',cache_info)
    print('WHT mod 3, block=8:')
    print(' N    baseline butterfly additions  lookups passes  baseline (ms) lookup (ms)')
    for row in data['tabulated_wht']:
        if row['block']==8:
            print(f"{row['n']:>5} {row['baseline_modular_add_sub']:>27} {row['lookups']:>8} "
                  f"{row['passes']:>6} {row['python_baseline_seconds']*1000:>12.3f} "
                  f"{row['python_lookup_seconds']*1000:>11.3f}")


if __name__=='__main__':
    run()
