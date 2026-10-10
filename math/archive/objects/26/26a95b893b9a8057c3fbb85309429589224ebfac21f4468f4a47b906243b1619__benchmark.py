"""End-to-end, reproducible local benchmark. Conservative comparator definitions.

Set OPENBLAS_NUM_THREADS=1 when running. All methods produce requested output.
Performance is workload-, FFT backend-, and memory-bandwidth-dependent.
"""
from __future__ import annotations
import json
from time import perf_counter_ns
from pathlib import Path
import numpy as np
from scipy import fft
from persistent_chain import ChainEngine


def ms(t):return (perf_counter_ns()-t)/1e6


def run(repeat=3, sizes=(4096,65536,262144), versions=48, factors=8,seed=20261009):
    rows=[]
    for n in sizes:
        rng=np.random.default_rng(seed+n)
        signals=[]
        for i in range(factors):
            x=rng.normal(0,0.02 / np.sqrt(n),size=n)
            x[0]+=1.0
            signals.append(x)
        events=[(int(rng.integers(n)), float(rng.normal(0,.15))) for _ in range(versions)]

        def baseline():
            start=perf_counter_ns()
            seed_specs=[fft.rfft(x) for x in signals]
            # This prepared-kernel comparator caches all UNCHANGED factors.
            other=np.ones(n//2+1,dtype=np.complex128)
            for i,s in enumerate(seed_specs):
                if i!=2:other*=s
            checks=[]
            for pos, delta in events:
                x=signals[2].copy();x[pos]+=delta
                result=fft.irfft(fft.rfft(x)*other,n=n)
                checks.append((result[0],result[n//3],result[n-1]))
            return ms(start),np.asarray(checks)

        def adaptive():
            start=perf_counter_ns()
            eng=ChainEngine()
            seeds=[eng.seed(x) for x in signals]
            root=eng.chain(seeds)
            # Charge both base and complement prep in the benchmark.
            eng._base(root.root)
            eng._leave_one_out(tuple(x.seed.id for x in seeds),2)
            checks=[]
            for pos,delta in events:
                v=root.edit(2,pos,delta)
                out=v.dense()
                checks.append((out[0],out[n//3],out[n-1]))
            return ms(start),np.asarray(checks),eng.memory_report()

        b_trials=[]; a_trials=[]; memory=None
        for _ in range(repeat):
            tb,expected=baseline();ta,actual,memory=adaptive()
            np.testing.assert_allclose(expected,actual,atol=1e-7,rtol=1e-6)
            b_trials.append(tb);a_trials.append(ta)
        b=float(np.median(b_trials));a=float(np.median(a_trials))
        rows.append(dict(case='many_versions_one_changed_factor_full_output',n=n,factors=factors,
                         versions=versions,baseline_ms=round(b,5),adaptive_ms=round(a,5),
                         speedup=round(b/a,4),adaptive_memory=memory))

    # Compare graph output queries with direct, already-cached basis-bin products.
    n=8192;m=128;q=[0,3,41,300];count=128
    rng=np.random.default_rng(seed+12)
    x=[np.zeros(n) for _ in range(m)]
    for i in range(m):
        x[i][0]=1.0
        x[i][(i*67+17)%n]=float(rng.uniform(-.1,.1))
    changed_idx=53
    deltas=list(rng.uniform(-.05,.05,size=count))
    position=219

    def graph():
        start=perf_counter_ns()
        eng=ChainEngine(max_bin_cache=300000)
        seeds=[eng.seed(sig) for sig in x]
        ref=eng.chain(seeds)
        ref.frequencies(q)  # Charge cache warming.
        out=[]
        for delta in deltas:
            v=ref.edit(changed_idx,position,float(delta))
            out.append(v.frequencies(q))
        return ms(start),np.asarray(out),eng.stats.copy(),ref

    def direct():
        start=perf_counter_ns()
        spec=[fft.rfft(sig) for sig in x]
        vals=[]
        for delta in deltas:
            out=[]
            for k in q:
                # Already-precomputed individual base Fourier coefficients.
                z=1+0j
                for j,s in enumerate(spec):
                    val=s[k] if j!=changed_idx else s[k]+delta*np.exp(-2j*np.pi*((k*position)%n)/n)
                    z*=val
                out.append(z)
            vals.append(out)
        return ms(start),np.asarray(vals)

    ta,actual,stats,ref=graph()
    tb,expected=direct()
    np.testing.assert_allclose(actual,expected,atol=1e-7,rtol=1e-7)
    rows.append(dict(case='128_factor_persistent_lazy_frequency_queries',n=n,factors=m,
                     versions=count,queried_bins=len(q),direct_ms=round(tb,5),persistent_ms=round(ta,5),
                     speedup=round(tb/ta,4),graph_stats=dict(stats)))

    # Warm-only comparison (separate seed FFT prep explicitly labeled).
    eng=ChainEngine(max_bin_cache=300000)
    seeds=[eng.seed(sig) for sig in x];ref=eng.chain(seeds);ref.frequencies(q)
    start=perf_counter_ns()
    for delta in deltas:
        ref.edit(changed_idx,position,float(delta)).frequencies(q)
    graph_warm=ms(start)
    spec=[fft.rfft(sig) for sig in x]
    start=perf_counter_ns()
    for delta in deltas:
        for k in q:
            z=1+0j
            for j,s in enumerate(spec):
                z *= s[k] if j!=changed_idx else s[k]+delta*np.exp(-2j*np.pi*((k*position)%n)/n)
    direct_warm=ms(start)
    rows.append(dict(case='128_factor_lazy_frequency_queries_warm_preparation_excluded',n=n,
                     factors=m,versions=count,queried_bins=len(q),direct_ms=round(direct_warm,5),
                     persistent_ms=round(graph_warm,5),speedup=round(direct_warm/graph_warm,4)))

    # Strong analytic competitor: once the *same* leave-one-out frequency
    # factors are prepared, a branch needs only Q phase corrections. This
    # reveals generality/dispatch overhead rather than overstating speedups.
    import cmath,math
    start=perf_counter_ns()
    spec=[fft.rfft(sig) for sig in x]
    cached_base=[]; cached_except=[]
    for k in q:
        a=1+0j; b=1+0j
        for j,z in enumerate(spec):
            a*=z[k]
            if j!=changed_idx:b*=z[k]
        cached_base.append(a);cached_except.append(b)
    for delta in deltas:
        out=[a+delta*cmath.exp(-2j*math.pi*((k*position)%n)/n)*b
             for (k,a,b) in zip(q,cached_base,cached_except)]
    direct_analytic_ms=ms(start)
    rows.append(dict(case='128_factor_prepared_leave_one_out_analytic_comparator',n=n,
                     factors=m,versions=count,queried_bins=len(q),analytic_ms=round(direct_analytic_ms,5),
                     persistent_engine_ms=round(ta,5),speedup=round(direct_analytic_ms/ta,4),
                     note='Both methods prepare all seeds; analytic comparator specializes to the single-edit case.'))

    # Worst-case algebraic blowup demonstration: both operands of every factor
    # are modified, symbolic DAG size remains linear, but materialization needs FFT.
    n=16384;m=24
    eng=ChainEngine()
    factors=[]
    for j in range(m):
        sig=np.zeros(n);sig[0]=1.;sig[(j+10)%n]=0.02
        factors.append(eng.seed(sig))
    root=eng.chain(factors)
    mutated=root
    for j in range(m):mutated=mutated.edit(j,(j*21)%n,.03)
    start=perf_counter_ns();out=mutated.dense();full_ms=ms(start)
    expected=fft.irfft(np.prod(np.stack([fft.rfft(mutated.factor(j).values()) for j in range(m)]),axis=0),n=n)
    np.testing.assert_allclose(out,expected,atol=1e-8)
    rows.append(dict(case='all_24_factors_changed_factored_fallback',n=n,factors=m,
                     expanded_polynomial_terms=2**m,live_nodes=len(eng._intern),dense_ms=round(full_ms,5),
                     valid=True))

    return rows

if __name__=='__main__':
    res=run()
    target=Path(__file__).with_name('benchmark_results.json')
    target.write_text(json.dumps(res,indent=2))
    for r in res:print(r)
    print('Wrote:',target)
