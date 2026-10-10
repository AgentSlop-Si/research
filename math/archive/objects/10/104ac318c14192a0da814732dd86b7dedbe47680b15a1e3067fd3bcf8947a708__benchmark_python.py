"""Reproducible binary FFT lookup experiment (Python controls).
Run from this directory or any working directory with Python 3 + numpy.
Original Library prototype is expected at ../original/fft_collision_research.py.
No network, external state changes or packages are required.
"""
import argparse, cmath, gc, importlib.util, json, math, os, platform, random
import statistics, sys, time
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent
sp = importlib.util.spec_from_file_location('original', ROOT.parent/'original/fft_collision_research.py')
original = importlib.util.module_from_spec(sp); sp.loader.exec_module(original)


def twiddle_plan(n):
    return {m: tuple(cmath.exp(-2j*math.pi*k/m) for k in range(m//2))
            for m in (1 << j for j in range(1,n.bit_length()))}


def standard_warm(signal, twiddles):
    def rec(offset,stride,size):
        if size == 1: return (complex(signal[offset]),)
        even=rec(offset,stride*2,size//2); odd=rec(offset+stride,stride*2,size//2)
        factors=twiddles[size]; half=size//2; out=[0j]*size
        for k in range(half):
            t=factors[k]*odd[k]; out[k]=even[k]+t; out[k+half]=even[k]-t
        return tuple(out)
    return rec(0,1,len(signal))


def canonical_no_stats(signal, twiddles=None):
    """Original algorithm, removing only counters and summary statistics.
    Optional reusable twiddles; dictionaries, DAG, tuple allocation remain.
    """
    n=len(signal); intern={}; nodes=[]
    def build(offset,stride,size):
        if size==1:
            value=signal[offset]; key=(1,value); spec=(1,-1,-1,value)
        else:
            left=build(offset,stride*2,size//2); right=build(offset+stride,stride*2,size//2)
            key=(size,left,right); spec=(size,left,right,None)
        ident=intern.get(key)
        if ident is None:
            ident=len(nodes); intern[key]=ident; nodes.append(spec)
        return ident
    root=build(0,1,n); results={}
    if twiddles is None: twiddles={}
    def evaluate(ident):
        if ident in results: return results[ident]
        size,left_id,right_id,value=nodes[ident]
        if size==1: out=(complex(value),)
        else:
            left=evaluate(left_id); right=evaluate(right_id); half=size//2
            factors=twiddles.get(size)
            if factors is None:
                factors=[cmath.exp(-2j*math.pi*k/size) for k in range(half)]
                twiddles[size]=factors
            out=[0j]*size
            for k in range(half):
                t=factors[k]*right[k]; out[k]=left[k]+t; out[k+half]=left[k]-t
            out=tuple(out)
        results[ident]=out
        return out
    return evaluate(root)


def make_table(b):
    """Python-object table; mathematical compact complex128 size is reported separately."""
    plan=twiddle_plan(b)
    return tuple(standard_warm([(key>>j)&1 for j in range(b)],plan) for key in range(1<<b))


def lookup_warm(signal,twiddles,b,table):
    """Packing follows natural order of the actual decimated subproblem.
    N/b lookups, exactly N bit gathers/shifts/ORs; no dictionary or DAG.
    A leaf returns a read-only tuple; upper merges allocate outputs normally.
    """
    def rec(offset,stride,size):
        if size==b:
            key=0
            for j in range(b): key |= signal[offset+j*stride] << j
            return table[key]
        even=rec(offset,stride*2,size//2); odd=rec(offset+stride,stride*2,size//2)
        factors=twiddles[size]; half=size//2; out=[0j]*size
        for k in range(half):
            t=factors[k]*odd[k]; out[k]=even[k]+t; out[k+half]=even[k]-t
        return tuple(out)
    return rec(0,1,len(signal))


def timed_once(fn):
    start=time.perf_counter_ns(); value=fn(); elapsed=(time.perf_counter_ns()-start)*1e-9
    # deallocation of the returned array is excluded equally for all kernels.
    return elapsed,value


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default=str(ROOT/'python_results.json'))
    args=parser.parse_args()
    res={'meta':{'python':sys.version,'numpy':np.__version__,'platform':platform.platform(),
        'seeds':[101,202,303],'repetitions_per_seed':5,'clock':'perf_counter_ns',
        'timing':'randomized method order; explicit GC before each sample and disabled within sample; end-to-end kernel includes input gathers, keys, output allocations, upper merges; input generation excluded; warm plans/tables exclude setup',
        'date':'2026-10-08'},'tables':{},'cases':[]}
    tables={}
    for b in (4,8,16):
        elapsed,tab=timed_once(lambda b=b:make_table(b)); tables[b]=tab
        obj_bytes=sys.getsizeof(tab)+sum(sys.getsizeof(row)+sum(sys.getsizeof(z) for z in row) for row in tab)
        res['tables'][str(b)]={'entries':1<<b,'complex_values':b*(1<<b),'compact_complex128_bytes':16*b*(1<<b),'python_object_bytes':obj_bytes,'build_seconds_single_run':elapsed}
        print('TABLE',b,res['tables'][str(b)],flush=True)
    for n in (4096,16384,65536):
        plan_time,tw=timed_once(lambda:twiddle_plan(n))
        # All setup except original functions' per-call plan allocation is outside warm timing.
        methods={
          'original_standard_cold':lambda x: original.standard_fft(x),
          'original_full_cache_cold':lambda x: original.canonical_fft(x)[0],
          'full_cache_no_stats_cold':lambda x: canonical_no_stats(x),
          'standard_warm':lambda x: standard_warm(x,tw),
          'full_cache_no_stats_warm':lambda x: canonical_no_stats(x,tw),
          **{'lookup%d_warm'%b:lambda x,b=b:lookup_warm(x,tw,b,tables[b]) for b in tables}}
        samples={name:[] for name in methods}; errors={name:0.0 for name in methods}
        seed_results=[]
        for seed in (101,202,303):
            rng=random.Random(seed+n); x=[rng.randrange(2) for _ in range(n)]; ref=np.fft.fft(x)
            local={name:[] for name in methods}
            for name,fn in methods.items():
                out=fn(x); err=float(np.max(np.abs(np.asarray(out)-ref))); errors[name]=max(errors[name],err)
                assert np.allclose(out,ref,rtol=1e-11,atol=1e-9),(n,name,err)
            order=list(methods); shuffler=random.Random(17+seed+n)
            gc.collect(); gc.disable()
            try:
                for repetition in range(5):
                    shuffler.shuffle(order)
                    for name in order:
                        gc.collect()  # reclaim closure cycles before each method, outside timer
                        elapsed,_=timed_once(lambda:methods[name](x)); samples[name].append(elapsed); local[name].append(elapsed)
            finally: gc.enable()
            seed_results.append({'seed':seed,'median_seconds':{k:statistics.median(v) for k,v in local.items()}})
        stats={k:{'median_seconds':statistics.median(v),'min_seconds':min(v),'max_seconds':max(v),'samples_seconds':v,'max_abs_error':errors[k]} for k,v in samples.items()}
        row={'n':n,'plan_build_seconds_single_run':plan_time,'methods':stats,'by_seed':seed_results}
        res['cases'].append(row)
        Path(args.output).write_text(json.dumps(res,indent=2)+'\n')
        print('N',n,{k:round(v['median_seconds']*1000,3) for k,v in stats.items()},flush=True)
        print('lookup8 speedup vs warm standard',stats['standard_warm']['median_seconds']/stats['lookup8_warm']['median_seconds'],flush=True)
    # Exhaust every b=4 and b=8 table row; all-zero/all-one/alternating extra cases.
    for b in (4,8):
        for key,row in enumerate(tables[b]):
            ref=np.fft.fft([(key>>j)&1 for j in range(b)])
            assert np.allclose(row,ref,rtol=1e-11,atol=1e-10)
    for n in (16,256,4096):
        tw=twiddle_plan(n)
        for x in ([0]*n,[1]*n,[j%2 for j in range(n)]):
            for b in (4,8,16): assert np.allclose(lookup_warm(x,tw,b,tables[b]),np.fft.fft(x),rtol=1e-11,atol=1e-9)
    res['correctness']='Passed numpy FFT comparisons: 3 random seeds x 3 N x 8 methods; every 4/8-bit table row; 27 structured-input lookup tests.'
    Path(args.output).write_text(json.dumps(res,indent=2)+'\n')
    print(res['correctness'],flush=True)

if __name__=='__main__': main()
