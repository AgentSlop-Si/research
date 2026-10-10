import json,time
import numpy as np
try:
    from scipy.fft import fft
except ImportError:
    from numpy.fft import fft
from lazy_spectrum import LazySpectrum, PreparedBinView

rng=np.random.default_rng(202610091)
rows=[]

def once(fn):
    t0=time.perf_counter_ns(); out=fn(); return (time.perf_counter_ns()-t0)/1e6,out

for n in [16384,65536,262144]:
    updates=500
    q=64
    support_k=32
    x0=rng.standard_normal(n)+1j*rng.standard_normal(n)
    support=rng.choice(n,size=support_k,replace=False)
    bins=np.sort(rng.choice(n,size=q,replace=False))
    update_slots=rng.integers(0,support_k,size=updates)
    deltas=rng.normal(scale=.05,size=updates)+1j*rng.normal(scale=.05,size=updates)

    def fresh():
        x=x0.copy(); _=fft(x); out=None
        for slot,d in zip(update_slots,deltas):
            x[support[slot]]+=d
            out=fft(x)[bins]
        return out

    def eager_full_phase_bank():
        x=x0.copy(); cached=fft(x)
        phases=np.exp((-2j*np.pi/n)*np.multiply.outer(support.astype(float),np.arange(n,dtype=float)))
        out=None
        for slot,d in zip(update_slots,deltas):
            x[support[slot]]+=d
            cached += d*phases[slot]
            out=cached[bins]
        return out, phases.nbytes

    def lazy():
        x=x0.copy(); state=LazySpectrum.from_spectrum(fft(x)); out=None
        for slot,d in zip(update_slots,deltas):
            j=int(support[slot]);x[j]+=d;state.add_edit(j,d);out=state.bins(bins)
        return out

    def prepared():
        x=x0.copy(); base=fft(x); view=PreparedBinView(base,support.tolist(),bins.tolist()); out=None
        for slot,d in zip(update_slots,deltas):
            j=int(support[slot]);x[j]+=d;view.add_edit(j,d);out=view.values()
        return out,view.phase_bytes,view.full_phase_cache_equivalent_bytes

    tf,of=once(fresh)
    te,oe=once(eager_full_phase_bank)
    tl,ol=once(lazy)
    tp,op=once(prepared)
    x=x0.copy()
    for slot,d in zip(update_slots,deltas):x[support[slot]]+=d
    truth=fft(x)[bins]
    assert np.allclose(of,truth,rtol=1e-9,atol=1e-7)
    assert np.allclose(oe[0],truth,rtol=1e-9,atol=1e-7)
    assert np.allclose(ol,truth,rtol=1e-9,atol=1e-7)
    assert np.allclose(op[0],truth,rtol=1e-9,atol=1e-7)
    row=dict(n=n,updates=updates,support_k=support_k,bins=q,
             fresh_ms=tf,eager_full_phase_bank_ms=te,lazy_dynamic_ms=tl,prepared_bin_view_ms=tp,
             prepared_vs_fresh=tf/tp,prepared_vs_eager=te/tp,prepared_vs_lazy=tl/tp,
             selective_phase_bytes=op[1],full_phase_bank_bytes=op[2],memory_reduction=op[2]/max(1,op[1]))
    rows.append(row);print(row)

with open('benchmark_prepared_bins_results.json','w') as f: json.dump(rows,f,indent=2)
