"""Reproducible exploratory benchmarks (no claim to outperform SciPy)."""
import json,time,statistics
from pathlib import Path
import numpy as np
from lookup_fft import normalized_fft_quantized,QuantizedDFTTable
from sampled_pruned_fft import approximate_normalized_fft
from cost_model import summary

def run(seed=20261009):
    rng=np.random.default_rng(seed)
    results={'seed':seed,'quantized':[],'sampled':[],'precomputation':[],
             'symbolic_table_model':summary([8,12,20,64,128,256,1024,8192,65536])}
    for K,R in [(2,4),(4,1)]:
        t0=time.perf_counter();tbl=QuantizedDFTTable(K,R,'full');dt=time.perf_counter()-t0
        results['precomputation'].append({'K':K,'R':R,'table_entries':tbl.possible,
                                          'output_values':tbl.possible*K,'seconds':dt,
                                          'dense_numpy_bytes':tbl.complete.nbytes})
    for N in (256,1024,4096):
        x=(rng.normal(size=N)+1j*rng.normal(size=N))
        x=x/np.maximum(1,abs(x))
        ref=np.fft.fft(x)/N
        for t in (1,2,3):
            R=256
            start=time.perf_counter()
            output,stats,tables=normalized_fft_quantized(x,t,R,table_mode='lazy')
            dt=time.perf_counter()-start
            results['quantized'].append({'N':N,'grouped_layers':t,'R':R,
                    'max_abs_error':float(np.max(abs(output-ref))),
                    'safe_error_bound_with_exact_phases':(2*stats.group_count+1)/R,
                    'table_hits':stats.hits,'table_misses':stats.misses,
                    'time_ms':dt*1000,'warning':'lazy misses compute FFT kernels and are NOT O(1) precomputed-table lookups'})
        for eps in (.25,.5):
            start=time.perf_counter()
            approx,s=approximate_normalized_fft(x,epsilon=eps,failure_probability=.01,seed=seed+N)
            dt=time.perf_counter()-start
            results['sampled'].append({'N':N,'epsilon':eps,'sample_count':s['samples'],
                    'unique_samples':s['unique_sample_positions'],
                    'max_abs_error':float(np.max(abs(approx-ref))),
                    'butterfly_slots':s['butterfly_slots'],
                    'ordinary_butterfly_slots':s['standard_butterfly_slots'],
                    'time_ms':dt*1000,'guarantee':'For each fixed |x[j]|<=1, failure <= 0.01 by union Hoeffding'})
    path=Path(__file__).parent/'benchmark_results.json'
    path.write_text(json.dumps(results,indent=2),encoding='utf8')
    for r in results['quantized']:
        if r['N'] in (256,4096) and r['grouped_layers']==2:
            print('QUANT',r['N'],'max err',f"{r['max_abs_error']:.6g}",
                  'hits/misses',r['table_hits'],r['table_misses'],'ms',round(r['time_ms'],2))
    for r in results['sampled']:
        if r['N'] in (256,4096) and r['epsilon']==.5:
            print('SAMPLE',r['N'],'error',f"{r['max_abs_error']:.6g}",
                  'samples',r['sample_count'],'pruned/full slots',r['butterfly_slots'],r['ordinary_butterfly_slots'])
    print('Wrote:',path)
    return results
if __name__=='__main__':run()
