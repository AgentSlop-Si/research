"""Single-thread Python exact NTT comparison, includes cold per-call arithmetic.

Arithmetic counts include even trivial multiplications executed by the two
kernels. They separately report root pow upper bounds, memory movements, and
layout index steps. Timing is illustrative, not an asymptotic claim.
"""
from __future__ import annotations
from collections import OrderedDict
from statistics import median
from time import perf_counter
import json,random,argparse
from exact_scan_macro import P,fft_via_mixed_scan_macros
from reference_ntt import radix2_ntt


def benchmark(ns=(256,1024,4096), repetitions=5, seed=20261009):
    rng=random.Random(seed)
    result=[]
    for n in ns:
        series={'scan':[],'reference':[]}
        countA=countB=None
        for trial in range(repetitions):
            x=[rng.randrange(P) for _ in range(n)]
            for name,fn in (('scan',fft_via_mixed_scan_macros),('reference',radix2_ntt)) if trial%2==0 else (('reference',radix2_ntt),('scan',fft_via_mixed_scan_macros)):
                start=perf_counter();y,gates=fn(x);elapsed=perf_counter()-start
                series[name].append(elapsed*1000)
                if name=='scan': scan=y;countA=gates
                else: ordinary=y;countB=gates
            assert scan==ordinary
        result.append({'n':n,'repetitions':repetitions,
                       'median_scan_ms':median(series['scan']),
                       'median_radix2_ms':median(series['reference']),
                       'scan_over_radix2_time_ratio':median(series['scan'])/median(series['reference']),
                       'scan_counts':countA,'radix2_counts':countB})
    return {'seed':seed,'modulus':P,'note':'Both fresh-input, exact, all outputs, same Python execution; operation counts include charged root-power and data-layout estimates.', 'results':result}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--sizes',type=int,nargs='+',default=[256,1024,4096]);parser.add_argument('--repetitions',type=int,default=5)
    args=parser.parse_args()
    answer=benchmark(ns=args.sizes,repetitions=args.repetitions)
    with open('benchmark_results.json','w') as f:json.dump(answer,f,indent=2)
    print(json.dumps(answer,indent=2))
