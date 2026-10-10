"""Reproducible independent finite-field audit, no NumPy FFT dependency."""
from __future__ import annotations
import json,random,time,hashlib
from collections import Counter
from pathlib import Path
from tensor_union import (root_for,direct_dft,direct_dft_bins,
                          make_low_rank,recognize as tensor_recognize,
                          transform_certified as tensor_transform,
                          direct_circular_convolution)
from fiber_union import (choose_q,make_fiber_signal,recognize as fiber_recognize,
                         transform_certified as fiber_transform)
from fiber_convolution import convolve_if_supported
from test_hero17 import matrix_rank

PRIMES={16:17,35:71,63:127,81:163,99:199,125:251,143:859,
        243:487,255:1021,256:65537,323:647,512:65537,1024:65537,2303:46061}


def run(seed:int=1717):
    rng=random.Random(seed)
    counts=Counter()
    observed=[]
    roots={n:root_for(n,p) for n,p in PRIMES.items()}
    t0=time.perf_counter()
    # Independent direct exact DFT all bins: random tensor factors.
    for a,b in [(5,7),(7,9),(9,11),(11,13),(15,17),(17,19)]:
        n=a*b;p=PRIMES[n];w=roots[n]
        for r in (1,2,3):
            for trial in range(4):
                f=[[rng.randrange(p) for _ in range(a)] for _ in range(r)]
                g=[[rng.randrange(p) for _ in range(b)] for _ in range(r)]
                raw=make_low_rank(a,b,p,w,f,g)
                cert=tensor_recognize(raw,p,w,r)
                assert cert is not None
                out=tensor_transform(cert)
                assert out==direct_dft(raw,p,w)
                counts['random_tensor_vectors']+=1
                counts['direct_fft_bins_verified']+=n
    # Independently check all bins for sparse per-fiber frequency patterns.
    for n in [16,81,125,243,256,512,1024]:
        p=PRIMES[n];w=roots[n];q=choose_q(n);m=n//q
        for r in (1,2,3):
            for trial in range(3):
                modes=[[(j,rng.randrange(1,p)) for j in rng.sample(range(m),r)] for t in range(q)]
                raw=make_fiber_signal(n,p,w,q,modes)
                cert=fiber_recognize(raw,p,w,r)
                assert cert is not None
                out=fiber_transform(cert)
                assert out==direct_dft(raw,p,w)
                counts['random_fiber_vectors']+=1
                counts['direct_fft_bins_verified']+=n
    # Full-rank row-basis examples and graph-joined exact circular products.
    for n in [16,256,1024]:
        p=PRIMES[n];w=roots[n];q=choose_q(n);m=n//q
        for trial in range(4):
            hx=list(range(q));hy=list(range(q))
            rng.shuffle(hx);rng.shuffle(hy)
            raw_x=make_fiber_signal(n,p,w,q,[[(h,rng.randrange(1,p))] for h in hx])
            raw_y=make_fiber_signal(n,p,w,q,[[(h,rng.randrange(1,p))] for h in hy])
            assert matrix_rank([[raw_x[t+q*u] for u in range(m)] for t in range(q)],p)==q
            assert matrix_rank([[raw_y[t+q*u] for u in range(m)] for t in range(q)],p)==q
            actual,graph=convolve_if_supported(raw_x,raw_y,p,w,1,1,max_states_ratio=2)
            assert actual is not None and graph.matching_edges==q and graph.union_states<=q
            assert actual==direct_circular_convolution(raw_x,raw_y,p)
            counts['full_rank_graph_products']+=1
            counts['direct_conv_bins_verified']+=n
    # Direct verification of arbitrary-degree polynomial chirps.
    for n in [81,125,243,256,512,1024]:
        p=PRIMES[n];w=roots[n]
        bound=5 if n==125 else (3 if n==243 else 1)
        for degree in [2,3,4,5,7,9]:
            x=[pow(w,(3*j**degree+5*j*j+7*j+11)%n,p) for j in range(n)]
            cert=fiber_recognize(x,p,w,bound)
            assert cert is not None
            assert fiber_transform(cert)==direct_dft(x,p,w)
            counts['polyphase_vectors']+=1
            counts['direct_fft_bins_verified']+=n
    # Large instance, independently test selected exact bins.
    n=2303;p=PRIMES[n];w=roots[n];a,b=47,49
    f=[[rng.randrange(p) for _ in range(a)] for _ in range(3)]
    g=[[rng.randrange(p) for _ in range(b)] for _ in range(3)]
    x=make_low_rank(a,b,p,w,f,g)
    cert=tensor_recognize(x,p,w,3)
    assert cert is not None
    z=tensor_transform(cert)
    bins=sorted(set([0,1,n-1]+[rng.randrange(n) for _ in range(100)]))
    assert [z[k] for k in bins]==direct_dft_bins(x,p,w,bins)
    counts['large_tensor_spot_vectors']+=1
    counts['direct_fft_bins_verified']+=len(bins)

    # False acceptance probes (only test rejection, not a distributional proof).
    for n in [143,256,512]:
        p=PRIMES[n];w=roots[n]
        for trial in range(250):
            x=[rng.randrange(p) for _ in range(n)]
            if n==143:
                assert tensor_recognize(x,p,w,2) is None
            else:
                assert fiber_recognize(x,p,w,2) is None
            counts['random_dense_rejections']+=1

    # Finite-cell graph stress: many edges, compact support vs expansive support.
    n,p=256,65537;w=roots[n];q=16
    same_x=make_fiber_signal(n,p,w,q,[[(2,rng.randrange(1,p))] for _ in range(q)])
    same_y=make_fiber_signal(n,p,w,q,[[(2,rng.randrange(1,p))] for _ in range(q)])
    product,proof=convolve_if_supported(same_x,same_y,p,w,1,1,max_states_ratio=2)
    assert proof.matching_edges==q*q and proof.union_states<=q
    assert product==direct_circular_convolution(same_x,same_y,p)
    counts['dense_edges_compact_union']+=1
    s=4
    stress_x=make_fiber_signal(n,p,w,q,[[(t%s,rng.randrange(1,p))] for t in range(q)])
    stress_y=make_fiber_signal(n,p,w,q,[[(t//s,rng.randrange(1,p))] for t in range(q)])
    product,proof=convolve_if_supported(stress_x,stress_y,p,w,1,1,max_states_ratio=2)
    assert product is None and proof.union_states==64
    counts['rejected_expansive_union']+=1

    report={
        'checkpoint':'2026-10-10',
        'model':'F_p exact field, p prime, N | (p-1), primitive omega supplied',
        'seed':seed,
        'audited_counts':dict(counts),
        'seconds_unoptimized_python':round(time.perf_counter()-t0,3),
        'not_claimed': ['universal arbitrary complex FFT O(N)', 'finite precision stability',
                        'publication-level novelty', 'optimized FFT/NTT benchmark win',
                        'arbitrary integer multiplication O(N)'],
        'examples':{
            'full_rank_graph':'Q=M=32, both QxM reshapes rank=Q, permutation frequency labels',
            'adversarial_union':'Q=16, E=64, S=64 states > 2Q threshold, correctly rejected',
        },
    }
    Path(__file__).with_name('AUDIT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':run()
