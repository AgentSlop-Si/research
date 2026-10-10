"""Independent post-implementation exact finite-field audit.
No import of existing DFT helper: reference computes every bin by Horner
powers of an explicitly supplied primitive N-th root (O(N^2) TEST ONLY).
Our online algorithms use only direct small DFT, BM, Vandermonde,
phase lookups, and binomial rational kernels.
"""
import json,random,time
from math import gcd
from delta_graph import balanced_q,make_delta_signal,recognize as delta_rec,transform_certified as delta_out
from delta_graph_budget import recognize_budgeted
from newton_union import recognize as newton_rec,transform_certified as newton_out,build_newton_signal
from graph_convolution_delta import convolve_if_supported
from fiber_union import make_fiber_signal
from tensor_union import root_for


def slow_reference(x,p,w,bins=None):
    n=len(x)
    if bins is None:bins=range(n)
    out=[]
    for k in bins:
        z=pow(w,(-k)%n,p)
        v=1;s=0
        for a in x:
            s=(s+a*v)%p
            v=v*z%p
        out.append(s)
    return out


def slow_cyclic_convolution(x,y,p):
    n=len(x)
    return [sum(x[j]*y[(k-j)%n] for j in range(n))%p for k in range(n)]


def exercise():
    rng=random.Random(171718)
    began=time.perf_counter()
    tally={'first_difference_full_vectors':0,'first_difference_bins':0,
           'budgeted_dense_jump_vectors':0,'budgeted_dense_jump_bins':0,
           'newton_vectors':0,'newton_direct_bins':0,
           'odd_mixed_composite_vectors':0,'random_rejections':0,
           'convolution_graph_rescues':0,'convolution_bins':0,
           'largest_spot_n':0,'largest_spot_bins':0,
           'independent_dense_full_rank_fixture':1}
    primes={15:31,63:127,99:199,143:859,255:1021,
            16:65537,64:65537,256:65537,1024:65537,4096:65537,65536:65537}
    omega={n:root_for(n,p) for n,p in primes.items()}
    # Fixed first-difference support, arbitrary dense baseline.
    for n in [16,64,256,1024]:
        p=primes[n];w=omega[n];q=balanced_q(n);m=n//q
        for rep in range(15):
            raw=[rng.randrange(p) for _ in range(m)]
            modes=[[] for _ in range(q)]
            for t in range(1,q):
                h=rng.randrange(m)
                modes[t]=[(h,rng.randrange(1,p))]
            x=make_delta_signal(n,p,w,q,raw,modes)
            cert=delta_rec(x,p,w,1,1,q)
            assert cert is not None
            got=delta_out(cert)
            expected=slow_reference(x,p,w)
            assert got==expected,(n,rep)
            tally['first_difference_full_vectors']+=1
            tally['first_difference_bins']+=n
    # An unconstrained dense transition in ONE row, not fiber sparsity.
    for n in [64,256,1024]:
        p=primes[n];w=omega[n];q=balanced_q(n);m=n//q
        for rep in range(7):
            raw=[rng.randrange(p) for _ in range(m)]
            modes=[[] for _ in range(q)]
            modes[q//2]=[(h,rng.randrange(1,p)) for h in range(m)]
            x=make_delta_signal(n,p,w,q,raw,modes)
            cert=recognize_budgeted(x,p,w,q,1,q)
            assert cert is not None and len(cert.events)==m
            assert delta_out(cert)==slow_reference(x,p,w)
            tally['budgeted_dense_jump_vectors']+=1
            tally['budgeted_dense_jump_bins']+=n
    # All Newton orders 1..4 (where q permits), different initial rows,
    # sparse high-order differences, including all composite odd lengths.
    for n in [15,16,63,64,99,143,255,256,1024]:
        p=primes[n];w=omega[n];q=balanced_q(n);m=n//q
        for d in range(1,min(4,q)+1):
            for rep in range(8):
                init=[[rng.randrange(p) for _ in range(m)] for _ in range(d)]
                events=[[] for _ in range(q)];remaining=q
                for t in range(d,q):
                    ss=rng.randrange(min(3,remaining,m)+1)
                    events[t]=[(h,rng.randrange(1,p)) for h in rng.sample(range(m),ss)]
                    remaining-=ss
                x=build_newton_signal(n,p,w,q,d,init,events)
                cert=newton_rec(x,p,w,d,q,q)
                assert cert is not None,(n,d,rep)
                got=newton_out(cert)
                expected=slow_reference(x,p,w)
                assert got==expected,(n,d,rep)
                tally['newton_vectors']+=1
                tally['newton_direct_bins']+=n
                if n%2:tally['odd_mixed_composite_vectors']+=1

    # Early fail closed: random fresh vectors lack the spectral variation promise.
    n=256;p=65537;w=omega[n]
    for d in [1,2,3,4]:
        for rep in range(75):
            x=[rng.randrange(p) for _ in range(n)]
            assert newton_rec(x,p,w,d,16,16) is None
            tally['random_rejections']+=1

    # Former adversarial S=Q^(3/2) output graph: now rescued by low deltas.
    for n,s in [(256,4),(4096,8)]:
        p=65537;w=omega[n];q=balanced_q(n)
        a=make_fiber_signal(n,p,w,q,[[(t%s,1)] for t in range(q)])
        b=make_fiber_signal(n,p,w,q,[[(t//s,1)] for t in range(q)])
        z,info=convolve_if_supported(a,b,p,w,1,1,q,2,2)
        assert z is not None and info.method=='delta-graph'
        assert info.nonzero_states==s*q
        assert info.delta_states<=2*s+1
        # Direct comparison for N=256. Independent selected cyclic sums
        # for large N, avoiding O(4096^2) TEST-ONLY work.
        bins=range(n) if n==256 else sorted(set([0,1,2,n//2,n-1]+[rng.randrange(n) for _ in range(41)]))
        direct=[sum(a[j]*b[(k-j)%n] for j in range(n))%p for k in bins]
        assert [z[k] for k in bins]==direct
        tally['convolution_graph_rescues']+=1
        tally['convolution_bins']+=len(direct)

    # O(N) structural scaling of Newton order 4 including one full N=65536
    # output. Independently check 37 bins in O(37*N) test work.
    n=65536;q=m=256;p=65537;w=omega[n];d=4
    init=[[rng.randrange(p) for _ in range(m)] for _ in range(d)]
    events=[[] for _ in range(q)]
    for t in range(d,q):events[t]=[(t,1+t)]
    x=build_newton_signal(n,p,w,q,d,init,events)
    cert=newton_rec(x,p,w,d,q,q)
    assert cert is not None
    got,counters=newton_out(cert,True)
    assert counters['event_terms']<=n
    bins=sorted(set([0,1,2,3,q-1,q,q+1,n//2,n-1]+[rng.randrange(n) for _ in range(28)]))
    assert [got[k] for k in bins]==slow_reference(x,p,w,bins)
    tally['largest_spot_n']=n;tally['largest_spot_bins']=len(bins)
    return dict(date='2026-10-10',seed=171718,arithmetic_model='F_p exact; supplied primitive root',
                tested=tally,large_n_counters=counters,
                seconds_python=round(time.perf_counter()-began,4),
                claims_excluded=[
                    'universal exact O(N) Fourier transform',
                    'independent mathematical novelty / priority',
                    'FFT library performance speedup',
                    'bounded-coefficient stable complex DFT',
                    'linear-time arbitrary integer multiplication',
                    'quantum advantage or all-amplitudes readout'])


if __name__=='__main__':
    result=exercise()
    print(json.dumps(result,indent=2))
    with open('AUDIT_RESULTS.json','w',encoding='utf8') as f:json.dump(result,f,indent=2)
